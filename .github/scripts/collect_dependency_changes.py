#!/usr/bin/env python3

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import random
import re
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

ALLOWED_SOURCE_TYPES = {
    "github_latest_release",
    "google_cloud_sdk_manifest",
    "hashicorp_checkpoint",
    "kubernetes_stable_release",
}
ALLOWED_KINDS = {"cli", "ecosystem"}
ALLOWED_CATEGORIES = {
    "authentication-identity",
    "cloud-providers",
    "helm-packaging",
    "kubernetes-container",
    "observability-operations",
    "security-crypto",
    "targets-integrations",
}
SEVERITY_RANK = {"low": 0, "medium": 1, "high": 2, "critical": 3}
RANK_SEVERITY = {0: "low", 1: "medium", 2: "high", 3: "critical"}


class RateLimitError(RuntimeError):
    def __init__(self, message: str, reset_epoch: str | None = None):
        super().__init__(message)
        self.reset_epoch = reset_epoch


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Collect dependency release signals and classify docs-impacting alerts."
    )
    parser.add_argument("--registry", default=".github/dependency-monitor/registry.json")
    parser.add_argument("--out-json", default=".github/dependency-monitor/dependency-monitor-report.json")
    parser.add_argument("--out-md", default=".github/dependency-monitor/dependency-monitor-report.md")
    parser.add_argument("--out-metrics", default=".github/dependency-monitor/dependency-monitor-metrics.json")
    parser.add_argument("--state-in", default=".github/dependency-monitor/state/last-seen.json")
    parser.add_argument("--state-out", default=".github/dependency-monitor/state/last-seen.json")
    parser.add_argument("--min-severity", choices=["low", "medium", "high", "critical"], default="low")
    parser.add_argument("--categories", default="", help="Comma-separated categories filter")
    parser.add_argument("--force-alert-mode", choices=["auto", "immediate", "digest"], default="auto")
    parser.add_argument("--stale-suppression-days", type=int, default=7)
    return parser.parse_args()


def load_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def validate_registry(registry: dict[str, Any]) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    if not isinstance(registry, dict):
        raise ValueError("Registry must be a JSON object")

    defaults = registry.get("defaults", {})
    dependencies = registry.get("dependencies", [])
    if not isinstance(defaults, dict):
        raise ValueError("Registry defaults must be an object")
    if not isinstance(dependencies, list) or not dependencies:
        raise ValueError("Registry dependencies must be a non-empty array")

    seen_ids: set[str] = set()
    required_fields = {
        "id",
        "name",
        "kind",
        "category",
        "source_type",
        "source",
        "source_url",
        "impacted_capability",
        "suggested_docs",
    }
    validated: list[dict[str, Any]] = []

    for index, item in enumerate(dependencies, start=1):
        if not isinstance(item, dict):
            raise ValueError(f"Dependency entry #{index} must be an object")

        missing = sorted(required_fields - set(item.keys()))
        if missing:
            raise ValueError(
                f"Dependency entry #{index} ({item.get('id', 'unknown')}) missing required fields: {', '.join(missing)}"
            )

        dep_id = str(item["id"]).strip()
        if not dep_id:
            raise ValueError(f"Dependency entry #{index} has empty id")
        if dep_id in seen_ids:
            raise ValueError(f"Duplicate dependency id found: {dep_id}")
        seen_ids.add(dep_id)

        kind = str(item["kind"]).strip()
        if kind not in ALLOWED_KINDS:
            raise ValueError(f"Dependency {dep_id} has unsupported kind: {kind}")

        category = str(item["category"]).strip()
        if category not in ALLOWED_CATEGORIES:
            raise ValueError(f"Dependency {dep_id} has unsupported category: {category}")

        source_type = str(item["source_type"]).strip()
        if source_type not in ALLOWED_SOURCE_TYPES:
            raise ValueError(f"Dependency {dep_id} has unsupported source_type: {source_type}")

        source_url = str(item["source_url"]).strip()
        if not source_url.startswith("https://"):
            raise ValueError(f"Dependency {dep_id} source_url must use https://")

        source = str(item["source"]).strip()
        if source_type == "github_latest_release":
            if not re.match(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$", source):
                raise ValueError(
                    f"Dependency {dep_id} source must be owner/repo for github_latest_release"
                )
        elif not source.startswith("https://"):
            raise ValueError(
                f"Dependency {dep_id} source must use https:// for source_type {source_type}"
            )

        suggested_docs = item.get("suggested_docs")
        if not isinstance(suggested_docs, list) or not suggested_docs:
            raise ValueError(f"Dependency {dep_id} suggested_docs must be a non-empty array")

        validated.append(item)

    return defaults, validated


def request_url(url: str, accept_json: bool, timeout: int = 30) -> str:
    headers: dict[str, str] = {"User-Agent": "akeyless-docs-dependency-monitor/1.0"}
    if accept_json:
        headers["Accept"] = "application/json"
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read().decode("utf-8")


def request_with_retries(url: str, accept_json: bool, retries: int = 3) -> str:
    last_error: Exception | None = None
    for attempt in range(1, retries + 1):
        try:
            return request_url(url, accept_json=accept_json, timeout=30)
        except urllib.error.HTTPError as err:
            if (
                "api.github.com/repos/" in url
                and err.code == 403
                and str(err.headers.get("X-RateLimit-Remaining", "")) == "0"
            ):
                raise RateLimitError(
                    "GitHub API rate limit exceeded",
                    reset_epoch=str(err.headers.get("X-RateLimit-Reset", "")),
                ) from err
            if err.code in {429, 500, 502, 503, 504} and attempt < retries:
                time.sleep((2 ** (attempt - 1)) + random.random())
                continue
            raise
        except (urllib.error.URLError, TimeoutError) as err:
            last_error = err
            if attempt < retries:
                time.sleep((2 ** (attempt - 1)) + random.random())
                continue
            raise
    if last_error:
        raise last_error
    raise RuntimeError("Unexpected fetch retry failure")


def fetch_json(url: str) -> dict[str, Any]:
    return json.loads(request_with_retries(url, accept_json=True))


def fetch_text(url: str) -> str:
    return request_with_retries(url, accept_json=False).strip()


def normalize_version(value: str, source_type: str) -> str:
    normalized = value.strip()
    if source_type in {"github_latest_release", "kubernetes_stable_release", "hashicorp_checkpoint"}:
        normalized = re.sub(r"^v", "", normalized, flags=re.IGNORECASE)
    if source_type == "google_cloud_sdk_manifest":
        normalized = normalized.split()[0]
    normalized = re.sub(r"\s+", "", normalized)
    return normalized or "unknown"


def parse_semver_like(version: str) -> tuple[int, int, int] | None:
    matches = re.findall(r"\d+", version)
    if not matches:
        return None
    parts = [int(part) for part in matches[:3]]
    while len(parts) < 3:
        parts.append(0)
    return (parts[0], parts[1], parts[2])


def change_type(previous: str | None, current: str) -> str:
    if not previous:
        return "new"
    if previous == current:
        return "unchanged"

    prev_sem = parse_semver_like(previous)
    curr_sem = parse_semver_like(current)
    if prev_sem and curr_sem:
        if curr_sem[0] != prev_sem[0]:
            return "major"
        if curr_sem[1] != prev_sem[1]:
            return "minor"
        if curr_sem[2] != prev_sem[2]:
            return "patch"
    return "changed"


def severity_name(rank: int) -> str:
    return RANK_SEVERITY[max(0, min(3, rank))]


def escalation_for_keywords(text: str) -> tuple[int, list[str]]:
    lowered = text.lower()
    hits: list[str] = []

    strong = ["cve", "critical", "breaking", "removed", "deprecat"]
    medium = ["security", "migration", "incompatible", "behavior change"]

    strong_count = 0
    medium_count = 0
    for token in strong:
        if token in lowered:
            hits.append(token)
            strong_count += 1
    for token in medium:
        if token in lowered:
            hits.append(token)
            medium_count += 1

    # Strong keywords accumulate: each strong hit is +1, capped at +2
    score = min(strong_count, 2)
    # Medium keywords add +1 if found, capped so total doesn't exceed +2 when strong hits exist
    if medium_count > 0 and strong_count == 0:
        score = 1
    elif medium_count > 0 and strong_count > 0:
        score = min(strong_count + 1, 2)

    return score, hits


def parse_timestamp(value: str) -> dt.datetime | None:
    try:
        return dt.datetime.fromisoformat(value.replace("Z", "+00:00"))
    except Exception:
        return None


def in_cooldown(health: dict[str, Any], sequence: int) -> bool:
    return int(health.get("cooldown_until_sequence", 0)) >= sequence


def fetch_dependency(entry: dict[str, Any], previous_version: str | None) -> dict[str, Any]:
    source_type = str(entry["source_type"])
    source = str(entry["source"])

    if source_type == "github_latest_release":
        try:
            payload = fetch_json(f"https://api.github.com/repos/{source}/releases/latest")
            version = normalize_version(
                str(payload.get("tag_name") or payload.get("name") or "unknown"),
                source_type=source_type,
            )
            return {
                "version": version,
                "release_url": payload.get("html_url") or entry.get("source_url") or "",
                "release_published_at": payload.get("published_at") or "",
                "release_name": payload.get("name") or payload.get("tag_name") or "",
                "release_body": payload.get("body") or "",
                "degraded": False,
                "warning": "",
            }
        except RateLimitError as err:
            warning = "GitHub API rate limit exceeded; used previous state fallback"
            if err.reset_epoch:
                warning += f" (reset epoch {err.reset_epoch})"
            return {
                "version": previous_version or "rate-limited",
                "release_url": entry.get("source_url") or "",
                "release_published_at": "",
                "release_name": "GitHub rate limit fallback",
                "release_body": "",
                "degraded": True,
                "warning": warning,
            }

    if source_type == "kubernetes_stable_release":
        version = normalize_version(fetch_text(source), source_type=source_type)
        return {
            "version": version,
            "release_url": entry.get("source_url") or source,
            "release_published_at": "",
            "release_name": f"Kubernetes stable {version}",
            "release_body": "",
            "degraded": False,
            "warning": "",
        }

    if source_type == "google_cloud_sdk_manifest":
        payload = fetch_json(source)
        version = normalize_version(str(payload.get("version", "unknown")), source_type=source_type)
        return {
            "version": version,
            "release_url": entry.get("source_url") or source,
            "release_published_at": "",
            "release_name": f"Google Cloud SDK {version}",
            "release_body": "",
            "degraded": False,
            "warning": "",
        }

    if source_type == "hashicorp_checkpoint":
        payload = fetch_json(source)
        version = normalize_version(
            str(payload.get("current_version", "unknown")), source_type=source_type
        )
        return {
            "version": version,
            "release_url": entry.get("source_url") or source,
            "release_published_at": "",
            "release_name": f"Terraform {version}",
            "release_body": "",
            "degraded": False,
            "warning": "",
        }

    raise ValueError(f"Unsupported source_type: {source_type}")


def should_suppress_stale(
    dep_id: str,
    version: str,
    alert_history: dict[str, Any],
    now_utc: dt.datetime,
    suppression_days: int,
) -> bool:
    if suppression_days <= 0:
        return False
    record = alert_history.get(dep_id)
    if not isinstance(record, dict):
        return False
    if str(record.get("version", "")) != version:
        return False
    alerted_at = parse_timestamp(str(record.get("last_alerted_at", "")))
    if not alerted_at:
        return False
    delta = now_utc - alerted_at
    return delta.total_seconds() < suppression_days * 86400


def render_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# Dependency Change Monitor Report",
        "",
        f"- Collected at: {report['generated_at_utc']}",
        f"- Dependencies configured: {report['dependencies_configured']}",
        f"- Categories covered: {', '.join(report['categories_covered'])}",
        f"- Successful fetches: {report['successful_fetches']}",
        f"- Fetch errors: {report['fetch_errors']}",
        f"- Previous state found: {report['previous_state_found']}",
        f"- Suppress new findings without baseline: {report.get('suppress_new_without_baseline', False)}",
        f"- Changed dependencies: {report['changed_dependencies']}",
        f"- Suppressed stale alerts: {report['stale_suppressed']}",
        f"- Suppressed new alerts without baseline: {report.get('new_without_baseline_suppressed', 0)}",
        f"- Cooldown source skips: {report['cooldown_skips']}",
        f"- Docs-impacting findings: {report['docs_impacting_findings']}",
        f"- Alert mode: {report['alert_mode']}",
        f"- Digest key: {report['digest_key']}",
        f"- Dedupe label: {report['dedupe_label']}",
        "",
    ]

    if report.get("warnings"):
        lines.extend(["## Warnings", ""])
        lines.extend([f"- {item}" for item in report["warnings"]])
        lines.append("")

    if report.get("fetch_error_items"):
        lines.extend(["## Fetch errors", ""])
        lines.extend([f"- `{item['id']}`: {item['error']}" for item in report["fetch_error_items"]])
        lines.append("")

    lines.extend(["## Findings", ""])
    if not report["findings"]:
        lines.extend(["No docs-impacting dependency findings were generated.", ""])
        return "\n".join(lines)

    for finding in report["findings"]:
        lines.append(
            f"- [{finding['severity'].upper()}] `{finding['name']}` changed `{finding['previous_version']}` -> `{finding['version']}`"
        )
        lines.append(f"  - Change type: {finding['change_type']}")
        lines.append(f"  - Why docs-impacting: {', '.join(finding['reasons'])}")
        lines.append(f"  - Source: {finding['release_url']}")
        lines.append(f"  - Impacted capability: {finding['impacted_capability']}")
        lines.append(f"  - Suggested docs to review: {', '.join(finding['suggested_docs'])}")
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    args = parse_args()
    registry_path = Path(args.registry)
    out_json_path = Path(args.out_json)
    out_md_path = Path(args.out_md)
    out_metrics_path = Path(args.out_metrics)
    state_in_path = Path(args.state_in)
    state_out_path = Path(args.state_out)

    if not registry_path.exists():
        print(f"Registry file not found: {registry_path}", file=sys.stderr)
        return 1

    registry = load_json(registry_path, default={})
    defaults, dependencies = validate_registry(registry)

    requested_categories = {
        item.strip() for item in args.categories.split(",") if item.strip()
    }

    previous_state = load_json(state_in_path, default={})
    previous_versions: dict[str, str] = {}
    source_health = {}
    alert_history = {}
    sequence = 0
    if isinstance(previous_state, dict):
        sequence = int(previous_state.get("sequence", 0))
        versions = previous_state.get("versions", {})
        if isinstance(versions, dict):
            previous_versions = {
                str(k): str(v) for k, v in versions.items() if str(v).strip()
            }
        source_health = previous_state.get("source_health", {})
        if not isinstance(source_health, dict):
            source_health = {}
        alert_history = previous_state.get("alert_history", {})
        if not isinstance(alert_history, dict):
            alert_history = {}

    now_utc = dt.datetime.now(tz=dt.timezone.utc)
    sequence += 1

    has_prior_baseline = bool(previous_versions)
    suppress_new_without_baseline = not has_prior_baseline

    findings: list[dict[str, Any]] = []
    fetch_error_items: list[dict[str, str]] = []
    warnings: list[str] = []
    current_versions: dict[str, str] = {}

    metrics = {
        "generated_at_utc": now_utc.strftime("%Y-%m-%d %H:%M:%S UTC"),
        "dependencies_configured": len(dependencies),
        "successful_fetches": 0,
        "fetch_errors": 0,
        "changed_dependencies": 0,
        "docs_impacting_findings": 0,
        "findings_by_severity": {"low": 0, "medium": 0, "high": 0, "critical": 0},
        "degraded_fetches": 0,
        "cooldown_skips": 0,
        "stale_suppressed": 0,
        "new_without_baseline_suppressed": 0,
    }

    categories_covered = sorted({str(dep.get("category", "unknown")) for dep in dependencies})
    min_rank = SEVERITY_RANK[args.min_severity]

    for dep in dependencies:
        dep_id = str(dep.get("id", "unknown"))
        category = str(dep.get("category", "unknown"))
        if requested_categories and category not in requested_categories:
            continue

        previous_version = previous_versions.get(dep_id)
        health = source_health.get(dep_id, {})
        if not isinstance(health, dict):
            health = {}

        if in_cooldown(health, sequence):
            metrics["cooldown_skips"] += 1
            warnings.append(
                f"{dep_id}: source in cooldown until sequence {health.get('cooldown_until_sequence')}"
            )
            if previous_version:
                current_versions[dep_id] = previous_version
            continue

        base_severity = str(dep.get("default_severity") or defaults.get("severity") or "medium").lower()
        base_rank = SEVERITY_RANK.get(base_severity, 1)
        owner = str(dep.get("owner") or defaults.get("owner") or "unknown")
        suggested_docs = [str(item) for item in dep.get("suggested_docs", [])]

        try:
            fetched = fetch_dependency(dep, previous_version=previous_version)
            metrics["successful_fetches"] += 1
            if fetched.get("degraded"):
                metrics["degraded_fetches"] += 1
                warning_text = str(fetched.get("warning") or "Degraded fetch mode used")
                warnings.append(f"{dep_id}: {warning_text}")

            health["consecutive_failures"] = 0
            health["cooldown_until_sequence"] = 0
            source_health[dep_id] = health
        except Exception as exc:  # noqa: BLE001
            metrics["fetch_errors"] += 1
            fetch_error_items.append({"id": dep_id, "error": str(exc)})

            failures = int(health.get("consecutive_failures", 0)) + 1
            health["consecutive_failures"] = failures
            if failures >= 3:
                health["cooldown_until_sequence"] = sequence + 2
                warnings.append(
                    f"{dep_id}: source entered cooldown for 2 runs after {failures} consecutive failures"
                )
            source_health[dep_id] = health

            if previous_version:
                current_versions[dep_id] = previous_version
            continue

        version = str(fetched.get("version") or "unknown")
        current_versions[dep_id] = version

        delta = change_type(previous_version, version)
        if delta == "unchanged":
            continue

        metrics["changed_dependencies"] += 1

        # Avoid alert floods when state cache is missing and everything appears as "new".
        if suppress_new_without_baseline and delta == "new":
            metrics["new_without_baseline_suppressed"] += 1
            continue

        if should_suppress_stale(
            dep_id=dep_id,
            version=version,
            alert_history=alert_history,
            now_utc=now_utc,
            suppression_days=args.stale_suppression_days,
        ):
            metrics["stale_suppressed"] += 1
            warnings.append(
                f"{dep_id}: suppressed duplicate alert for version {version} within {args.stale_suppression_days} days"
            )
            continue

        rank = base_rank
        reasons = [f"change:{delta}", f"base-severity:{severity_name(base_rank)}"]

        # Escalate for major version bumps
        if delta == "major":
            rank += 1
            reasons.append("major-version-bump")

        # De-escalate for patch-level changes (floor at 0)
        if delta == "patch":
            rank = max(0, rank - 1)
            reasons.append("patch-release-deescalation")

        # Escalate for high-risk categories
        if category in {"kubernetes-container", "authentication-identity", "security-crypto"}:
            rank += 1
            reasons.append(f"category-escalation:{category}")

        # Floor new entries in high-risk categories to at least medium
        if delta == "new" and category in {"kubernetes-container", "authentication-identity", "security-crypto"}:
            rank = max(rank, 1)  # medium severity
            reasons.append("new-entry-high-risk-category")

        # Scan release notes for security keywords
        keyword_text = " ".join([
            str(fetched.get("release_name") or ""),
            str(fetched.get("release_body") or ""),
            str(fetched.get("warning") or "")
        ])
        keyword_boost, keyword_hits = escalation_for_keywords(keyword_text)
        if keyword_boost:
            rank += keyword_boost
            reasons.append("keyword-escalation:" + ",".join(sorted(set(keyword_hits))))

        severity = severity_name(rank)
        if SEVERITY_RANK[severity] < min_rank:
            continue

        finding = {
            "id": dep_id,
            "name": str(dep.get("name", "unknown")),
            "kind": str(dep.get("kind", "ecosystem")),
            "category": category,
            "owner": owner,
            "source_url": str(dep.get("source_url") or ""),
            "release_url": str(fetched.get("release_url") or dep.get("source_url") or ""),
            "previous_version": previous_version or "<none>",
            "version": version,
            "change_type": delta,
            "release_name": str(fetched.get("release_name") or ""),
            "release_published_at": str(fetched.get("release_published_at") or ""),
            "severity": severity,
            "docs_impacting": True,
            "reasons": reasons,
            "impacted_capability": str(dep.get("impacted_capability") or "Documentation examples and guidance"),
            "suggested_docs": suggested_docs,
            "summary": f"{dep.get('name', 'Dependency')} changed from {previous_version or '<none>'} to {version}",
        }
        findings.append(finding)

        alert_history[dep_id] = {
            "version": version,
            "last_alerted_at": now_utc.isoformat(),
        }

    findings.sort(key=lambda item: (-SEVERITY_RANK[item["severity"]], item["name"]))
    metrics["docs_impacting_findings"] = len(findings)
    for item in findings:
        metrics["findings_by_severity"][item["severity"]] += 1

    digest_parts = [f"{item['id']}:{item['version']}" for item in findings]
    digest_blob = "|".join(sorted(digest_parts)).encode("utf-8")
    digest_key = hashlib.sha256(digest_blob).hexdigest()[:12] if digest_parts else "no-findings"
    dedupe_label = f"depkey-{digest_key}"

    high_or_critical = sum(1 for item in findings if item["severity"] in {"critical", "high"})
    if args.force_alert_mode == "auto":
        alert_mode = "immediate" if findings and high_or_critical > 0 else "digest"
    else:
        alert_mode = args.force_alert_mode

    state_snapshot = {
        "updated_at_utc": now_utc.strftime("%Y-%m-%d %H:%M:%S UTC"),
        "sequence": sequence,
        "versions": current_versions,
        "source_health": source_health,
        "alert_history": alert_history,
    }

    report = {
        "generated_at_utc": now_utc.strftime("%Y-%m-%d %H:%M:%S UTC"),
        "dependencies_configured": len(dependencies),
        "categories_covered": categories_covered,
        "successful_fetches": metrics["successful_fetches"],
        "fetch_errors": metrics["fetch_errors"],
        "fetch_error_items": fetch_error_items,
        "warnings": warnings,
        "previous_state_found": has_prior_baseline,
        "suppress_new_without_baseline": suppress_new_without_baseline,
        "changed_dependencies": metrics["changed_dependencies"],
        "stale_suppressed": metrics["stale_suppressed"],
        "new_without_baseline_suppressed": metrics["new_without_baseline_suppressed"],
        "cooldown_skips": metrics["cooldown_skips"],
        "docs_impacting_findings": len(findings),
        "findings": findings,
        "alert_mode": alert_mode,
        "high_or_critical_count": high_or_critical,
        "digest_key": digest_key,
        "dedupe_label": dedupe_label,
        "top_findings": [
            {
                "id": item["id"],
                "name": item["name"],
                "previous_version": item["previous_version"],
                "version": item["version"],
                "change_type": item["change_type"],
                "severity": item["severity"],
                "release_url": item["release_url"],
                "reasons": item["reasons"],
                "impacted_capability": item["impacted_capability"],
                "suggested_docs": item["suggested_docs"],
            }
            for item in findings[:5]
        ],
        "metrics": metrics,
    }

    out_json_path.parent.mkdir(parents=True, exist_ok=True)
    state_out_path.parent.mkdir(parents=True, exist_ok=True)
    out_metrics_path.parent.mkdir(parents=True, exist_ok=True)

    out_json_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    out_md_path.write_text(render_markdown(report), encoding="utf-8")
    out_metrics_path.write_text(json.dumps(metrics, indent=2), encoding="utf-8")
    state_out_path.write_text(json.dumps(state_snapshot, indent=2), encoding="utf-8")

    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except ValueError as err:
        print(f"Validation error while collecting dependency changes: {err}", file=sys.stderr)
        raise SystemExit(1)
    except urllib.error.HTTPError as err:
        print(f"HTTP error while collecting dependency changes: {err}", file=sys.stderr)
        raise SystemExit(1)
