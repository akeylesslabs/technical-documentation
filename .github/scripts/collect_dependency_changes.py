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


class RateLimitError(RuntimeError):
    def __init__(self, message: str, reset_epoch: str | None = None):
        super().__init__(message)
        self.reset_epoch = reset_epoch


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Collect dependency release signals and classify docs-impacting alerts."
    )
    parser.add_argument(
        "--registry",
        default=".github/dependency-monitor/registry.json",
        help="Path to dependency registry JSON",
    )
    parser.add_argument(
        "--out-json",
        default=".github/dependency-monitor/dependency-monitor-report.json",
        help="Output JSON report path",
    )
    parser.add_argument(
        "--out-md",
        default=".github/dependency-monitor/dependency-monitor-report.md",
        help="Output markdown report path",
    )
    parser.add_argument(
        "--state-in",
        default=".github/dependency-monitor/state/last-seen.json",
        help="Path to previous state snapshot JSON",
    )
    parser.add_argument(
        "--state-out",
        default=".github/dependency-monitor/state/last-seen.json",
        help="Path to write updated state snapshot JSON",
    )
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
    validated: list[dict[str, Any]] = []
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
            raise ValueError(
                f"Dependency {dep_id} has unsupported source_type: {source_type}"
            )

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
                sleep_for = (2 ** (attempt - 1)) + random.random()
                time.sleep(sleep_for)
                continue
            raise
        except (urllib.error.URLError, TimeoutError) as err:
            last_error = err
            if attempt < retries:
                sleep_for = (2 ** (attempt - 1)) + random.random()
                time.sleep(sleep_for)
                continue
            raise
    if last_error:
        raise last_error
    raise RuntimeError("Unexpected fetch retry failure")


def fetch_json(url: str) -> dict[str, Any]:
    raw = request_with_retries(url, accept_json=True)
    return json.loads(raw)


def fetch_text(url: str) -> str:
    return request_with_retries(url, accept_json=False).strip()


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


def is_docs_impacting(change_kind: str) -> bool:
    return change_kind in {"new", "major", "minor", "patch", "changed"}


def escalation_for_keywords(text: str) -> int:
    lowered = text.lower()
    if any(token in lowered for token in ["cve", "critical", "breaking", "removed", "deprecat"]):
        return 2
    if any(token in lowered for token in ["security", "migration", "incompatible", "behavior change"]):
        return 1
    return 0


def severity_rank(name: str) -> int:
    ranks = {"low": 0, "medium": 1, "high": 2, "critical": 3}
    return ranks.get(name, 1)


def severity_name(rank: int) -> str:
    names = {0: "low", 1: "medium", 2: "high", 3: "critical"}
    return names[max(0, min(3, rank))]
    req = urllib.request.Request(
        url,
        headers={
            "Accept": "application/json",
            "User-Agent": "akeyless-docs-dependency-monitor/1.0",
        },
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        raw = resp.read().decode("utf-8")
    return json.loads(raw)


def normalize_version(value: str) -> str:
    return value.strip()


def fetch_dependency(entry: dict[str, Any], previous_version: str | None) -> dict[str, Any]:
    source_type = entry["source_type"]
    source = entry["source"]

    if source_type == "github_latest_release":
        try:
            payload = fetch_json(f"https://api.github.com/repos/{source}/releases/latest")
            version = normalize_version(
                str(payload.get("tag_name") or payload.get("name") or "unknown")
            )
            return {
                "version": version,
                "release_url": payload.get("html_url") or entry.get("source_url") or "",
                "release_published_at": payload.get("published_at") or "",
                "release_name": payload.get("name") or payload.get("tag_name") or "",
                "degraded": False,
                "warning": "",
            }
        except RateLimitError as err:
            fallback_version = previous_version or "rate-limited"
            warning = "GitHub API rate limit exceeded; used fallback source URL"
            if err.reset_epoch:
                warning += f" (reset epoch {err.reset_epoch})"
            return {
                "version": fallback_version,
                "release_url": entry.get("source_url") or "",
                "release_published_at": "",
                "release_name": "GitHub rate limit fallback",
                "degraded": True,
                "warning": warning,
            }

    if source_type == "kubernetes_stable_release":
        version = normalize_version(fetch_text(source))
        return {
            "version": version,
            "release_url": entry.get("source_url") or source,
            "release_published_at": "",
            "release_name": f"Kubernetes stable {version}",
            "degraded": False,
            "warning": "",
        }

    if source_type == "google_cloud_sdk_manifest":
        payload = fetch_json(source)
        version = normalize_version(str(payload.get("version", "unknown")))
        return {
            "version": version,
            "release_url": entry.get("source_url") or source,
            "release_published_at": "",
            "release_name": f"Google Cloud SDK {version}",
            "degraded": False,
            "warning": "",
        }

    if source_type == "hashicorp_checkpoint":
        payload = fetch_json(source)
        version = normalize_version(str(payload.get("current_version", "unknown")))
        return {
            "version": version,
            "release_url": entry.get("source_url") or source,
            "release_published_at": "",
            "release_name": f"Terraform {version}",
            "degraded": False,
            "warning": "",
        }

    raise ValueError(f"Unsupported source_type: {source_type}")


def classify_severity(raw: str) -> str:
    raw_lower = (raw or "").lower()
    if raw_lower in {"critical", "high", "medium", "low"}:
        return raw_lower
    return "medium"


def extract_major(version: str) -> int | None:
    match = re.search(r"(\d+)", version)
    if not match:
        return None
    return int(match.group(1))


def render_markdown(report: dict[str, Any]) -> str:
    lines: list[str] = []
    lines.append("# Dependency Change Monitor Report")
    lines.append("")
    lines.append(f"- Collected at: {report['generated_at_utc']}")
    lines.append(f"- Dependencies configured: {report['dependencies_configured']}")
    lines.append(f"- Categories covered: {', '.join(report['categories_covered'])}")
    lines.append(f"- Successful fetches: {report['successful_fetches']}")
    lines.append(f"- Fetch errors: {report['fetch_errors']}")
    lines.append(f"- Previous state found: {report['previous_state_found']}")
    lines.append(f"- Changed dependencies: {report['changed_dependencies']}")
    lines.append(f"- Docs-impacting findings: {report['docs_impacting_findings']}")
    lines.append(f"- Alert mode: {report['alert_mode']}")
    lines.append(f"- Digest key: {report['digest_key']}")
    lines.append(f"- Dedupe label: {report['dedupe_label']}")
    lines.append("")

    if report.get("warnings"):
        lines.append("## Warnings")
        lines.append("")
        for warning in report["warnings"]:
            lines.append(f"- {warning}")
        lines.append("")

    if report["fetch_error_items"]:
        lines.append("## Fetch errors")
        lines.append("")
        for item in report["fetch_error_items"]:
            lines.append(f"- `{item['id']}`: {item['error']}")
        lines.append("")

    lines.append("## Findings")
    lines.append("")
    if not report["findings"]:
        lines.append("No docs-impacting dependency findings were generated.")
        lines.append("")
        return "\n".join(lines)

    for finding in report["findings"]:
        docs_paths = ", ".join(finding["suggested_docs"])
        lines.append(
            f"- [{finding['severity'].upper()}] `{finding['name']}` changed `{finding['previous_version']}` -> `{finding['version']}`"
        )
        lines.append(f"  - Change type: {finding['change_type']}")
        lines.append(f"  - Source: {finding['release_url']}")
        lines.append(f"  - Impacted capability: {finding['impacted_capability']}")
        lines.append(f"  - Suggested docs to review: {docs_paths}")
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    args = parse_args()
    registry_path = Path(args.registry)
    out_json_path = Path(args.out_json)
    out_md_path = Path(args.out_md)
    state_in_path = Path(args.state_in)
    state_out_path = Path(args.state_out)

    if not registry_path.exists():
        print(f"Registry file not found: {registry_path}", file=sys.stderr)
        return 1

    registry = load_json(registry_path, default={})
    defaults, dependencies = validate_registry(registry)

    previous_state = load_json(state_in_path, default={})
    previous_versions: dict[str, str] = {}
    if isinstance(previous_state, dict):
        maybe_versions = previous_state.get("versions", {})
        if isinstance(maybe_versions, dict):
            previous_versions = {
                str(key): str(value) for key, value in maybe_versions.items() if str(value).strip()
            }

    findings: list[dict[str, Any]] = []
    fetch_error_items: list[dict[str, str]] = []
    warnings: list[str] = []
    current_versions: dict[str, str] = {}
    categories_covered = sorted(
        {str(dep.get("category", "unknown")) for dep in dependencies}
    )
    changed_dependencies = 0

    for dep in dependencies:
        dep_id = str(dep.get("id", "unknown"))
        previous_version = previous_versions.get(dep_id)
        severity = classify_severity(
            str(dep.get("default_severity") or defaults.get("severity") or "medium")
        )
        owner = str(dep.get("owner") or defaults.get("owner") or "unknown")
        suggested_docs = [str(item) for item in dep.get("suggested_docs", [])]

        try:
            fetched = fetch_dependency(dep, previous_version=previous_version)
            version = str(fetched.get("version") or "unknown")
            current_versions[dep_id] = version

            if fetched.get("degraded"):
                warning_text = str(fetched.get("warning") or "Degraded fetch mode used")
                warnings.append(f"{dep_id}: {warning_text}")

            delta = change_type(previous_version, version)
            if delta == "unchanged":
                continue

            changed_dependencies += 1
            if not is_docs_impacting(delta):
                continue

            rank = severity_rank(severity)
            if delta == "major":
                rank += 1
            if str(dep.get("category", "")) in {"kubernetes-container", "authentication-identity"}:
                rank += 1

            keyword_text = " ".join(
                [
                    str(fetched.get("release_name") or ""),
                    str(fetched.get("warning") or ""),
                ]
            )
            rank += escalation_for_keywords(keyword_text)
            severity = severity_name(rank)

            finding = {
                "id": dep_id,
                "name": str(dep.get("name", "unknown")),
                "kind": str(dep.get("kind", "ecosystem")),
                "category": str(dep.get("category", "unknown")),
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
                "impacted_capability": str(dep.get("impacted_capability") or "Documentation examples and guidance"),
                "suggested_docs": suggested_docs,
                "summary": f"{dep.get('name', 'Dependency')} changed from {previous_version or '<none>'} to {version}",
            }
            findings.append(finding)
        except Exception as exc:  # noqa: BLE001
            fetch_error_items.append(
                {
                    "id": dep_id,
                    "error": str(exc),
                }
            )
            if previous_version:
                current_versions[dep_id] = previous_version
                warnings.append(
                    f"{dep_id}: using previous version snapshot due to fetch failure"
                )

    findings.sort(key=lambda item: (-severity_rank(item["severity"]), item["name"]))

    digest_parts = [f"{item['id']}:{item['version']}" for item in findings]
    digest_blob = "|".join(sorted(digest_parts)).encode("utf-8")
    digest_key = hashlib.sha256(digest_blob).hexdigest()[:12] if digest_parts else "no-findings"
    dedupe_label = f"depkey-{digest_key}"

    high_or_critical = sum(1 for item in findings if item["severity"] in {"critical", "high"})
    alert_mode = "immediate" if findings and high_or_critical > 0 else "digest"

    state_snapshot = {
        "updated_at_utc": dt.datetime.now(tz=dt.timezone.utc).strftime(
            "%Y-%m-%d %H:%M:%S UTC"
        ),
        "versions": current_versions,
    }

    state_out_path.parent.mkdir(parents=True, exist_ok=True)
    state_out_path.write_text(json.dumps(state_snapshot, indent=2), encoding="utf-8")

    report = {
        "generated_at_utc": dt.datetime.now(tz=dt.timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC"),
        "dependencies_configured": len(dependencies),
        "categories_covered": categories_covered,
        "successful_fetches": len(current_versions),
        "fetch_errors": len(fetch_error_items),
        "fetch_error_items": fetch_error_items,
        "warnings": warnings,
        "previous_state_found": bool(previous_versions),
        "changed_dependencies": changed_dependencies,
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
                "impacted_capability": item["impacted_capability"],
                "suggested_docs": item["suggested_docs"],
            }
            for item in findings[:5]
        ],
    }

    out_json_path.parent.mkdir(parents=True, exist_ok=True)
    out_json_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    out_md_path.write_text(render_markdown(report), encoding="utf-8")

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
