#!/usr/bin/env python3

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any


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
    return parser.parse_args()


def fetch_json(url: str) -> dict[str, Any]:
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


def fetch_text(url: str) -> str:
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "akeyless-docs-dependency-monitor/1.0",
        },
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.read().decode("utf-8").strip()


def normalize_version(value: str) -> str:
    return value.strip()


def fetch_dependency(entry: dict[str, Any]) -> dict[str, Any]:
    source_type = entry["source_type"]
    source = entry["source"]

    if source_type == "github_latest_release":
        payload = fetch_json(f"https://api.github.com/repos/{source}/releases/latest")
        version = normalize_version(
            payload.get("tag_name") or payload.get("name") or "unknown"
        )
        return {
            "version": version,
            "release_url": payload.get("html_url") or entry.get("source_url") or "",
            "release_published_at": payload.get("published_at") or "",
            "release_name": payload.get("name") or payload.get("tag_name") or "",
        }

    if source_type == "kubernetes_stable_release":
        version = normalize_version(fetch_text(source))
        return {
            "version": version,
            "release_url": entry.get("source_url") or source,
            "release_published_at": "",
            "release_name": f"Kubernetes stable {version}",
        }

    if source_type == "google_cloud_sdk_manifest":
        payload = fetch_json(source)
        version = normalize_version(str(payload.get("version", "unknown")))
        return {
            "version": version,
            "release_url": entry.get("source_url") or source,
            "release_published_at": "",
            "release_name": f"Google Cloud SDK {version}",
        }

    if source_type == "hashicorp_checkpoint":
        payload = fetch_json(source)
        version = normalize_version(str(payload.get("current_version", "unknown")))
        return {
            "version": version,
            "release_url": entry.get("source_url") or source,
            "release_published_at": "",
            "release_name": f"Terraform {version}",
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
    lines.append(f"- Docs-impacting findings: {report['docs_impacting_findings']}")
    lines.append(f"- Alert mode: {report['alert_mode']}")
    lines.append(f"- Digest key: {report['digest_key']}")
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
            f"- [{finding['severity'].upper()}] `{finding['name']}` observed `{finding['version']}`"
        )
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

    if not registry_path.exists():
        print(f"Registry file not found: {registry_path}", file=sys.stderr)
        return 1

    registry = json.loads(registry_path.read_text(encoding="utf-8"))
    defaults = registry.get("defaults", {})
    dependencies = registry.get("dependencies", [])

    findings: list[dict[str, Any]] = []
    fetch_error_items: list[dict[str, str]] = []
    categories_covered = sorted(
        {str(dep.get("category", "unknown")) for dep in dependencies}
    )

    for dep in dependencies:
        severity = classify_severity(
            str(dep.get("default_severity") or defaults.get("severity") or "medium")
        )
        owner = str(dep.get("owner") or defaults.get("owner") or "unknown")
        suggested_docs = [str(item) for item in dep.get("suggested_docs", [])]

        try:
            fetched = fetch_dependency(dep)
            version = str(fetched.get("version") or "unknown")
            major = extract_major(version)
            if major is not None and major >= 2 and severity == "medium":
                severity = "high"

            finding = {
                "id": str(dep.get("id", "unknown")),
                "name": str(dep.get("name", "unknown")),
                "kind": str(dep.get("kind", "ecosystem")),
                "category": str(dep.get("category", "unknown")),
                "owner": owner,
                "source_url": str(dep.get("source_url") or ""),
                "release_url": str(fetched.get("release_url") or dep.get("source_url") or ""),
                "version": version,
                "release_name": str(fetched.get("release_name") or ""),
                "release_published_at": str(fetched.get("release_published_at") or ""),
                "severity": severity,
                "docs_impacting": True,
                "impacted_capability": str(dep.get("impacted_capability") or "Documentation examples and guidance"),
                "suggested_docs": suggested_docs,
                "summary": f"{dep.get('name', 'Dependency')} latest observed version is {version}",
            }
            findings.append(finding)
        except Exception as exc:  # noqa: BLE001
            fetch_error_items.append(
                {
                    "id": str(dep.get("id", "unknown")),
                    "error": str(exc),
                }
            )

    findings.sort(key=lambda item: (item["severity"], item["name"]))

    digest_parts = [f"{item['id']}:{item['version']}" for item in findings]
    digest_blob = "|".join(sorted(digest_parts)).encode("utf-8")
    digest_key = hashlib.sha256(digest_blob).hexdigest()[:12] if digest_parts else "no-findings"

    high_or_critical = sum(1 for item in findings if item["severity"] in {"critical", "high"})
    alert_mode = "immediate" if high_or_critical > 0 else "digest"

    report = {
        "generated_at_utc": dt.datetime.now(tz=dt.timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC"),
        "dependencies_configured": len(dependencies),
        "categories_covered": categories_covered,
        "successful_fetches": len(findings),
        "fetch_errors": len(fetch_error_items),
        "fetch_error_items": fetch_error_items,
        "docs_impacting_findings": len(findings),
        "findings": findings,
        "alert_mode": alert_mode,
        "high_or_critical_count": high_or_critical,
        "digest_key": digest_key,
        "top_findings": [
            {
                "name": item["name"],
                "version": item["version"],
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
    except urllib.error.HTTPError as err:
        print(f"HTTP error while collecting dependency changes: {err}", file=sys.stderr)
        raise SystemExit(1)
