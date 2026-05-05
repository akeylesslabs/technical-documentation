#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from pathlib import Path


@dataclass
class LinkViolation:
    path: str
    line: int
    url: str
    reason: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Validate docs link policy: links that target docs.akeyless.io content "
            "must use absolute https://docs.akeyless.io/docs/... URLs."
        )
    )
    parser.add_argument("--root", default=".", help="Repository root path")
    parser.add_argument(
        "--out-json",
        default=".github/lychee/absolute-docs-link-policy.json",
        help="Path to JSON report output",
    )
    parser.add_argument(
        "--out-md",
        default=".github/lychee/absolute-docs-link-policy.md",
        help="Path to Markdown report output",
    )
    return parser.parse_args()


def should_skip_url(url: str) -> bool:
    lower = url.lower()
    return (
        lower.startswith("http://")
        or lower.startswith("https://")
        or lower.startswith("mailto:")
        or lower.startswith("#")
        or lower.startswith("tel:")
        or lower.startswith("javascript:")
    )


def docs_relative_violation(url: str) -> str | None:
    lower = url.lower()

    # Enforce absolute links for docs site content.
    if lower.startswith("/docs/"):
        return "Use an absolute docs URL instead of /docs/..."
    if lower.startswith("docs/"):
        return "Use an absolute docs URL instead of docs/..."
    if lower.startswith("../docs/") or lower.startswith("./docs/"):
        return "Use an absolute docs URL instead of relative docs/..."

    # Disallow docs.akeyless.io links that are not /docs/ paths.
    if lower.startswith("http://docs.akeyless.io/"):
        return "Use https://docs.akeyless.io/docs/... URLs for docs links"
    if lower.startswith("https://docs.akeyless.io/") and not lower.startswith("https://docs.akeyless.io/docs/"):
        return "Use https://docs.akeyless.io/docs/... URLs for docs links"

    return None


def scan_markdown_file(path: Path) -> list[LinkViolation]:
    violations: list[LinkViolation] = []

    md_link_re = re.compile(r"\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
    html_href_re = re.compile(r"href\s*=\s*[\"']([^\"']+)[\"']", re.IGNORECASE)

    in_fence = False
    fence_delim = ""

    for idx, raw_line in enumerate(path.read_text(encoding="utf-8", errors="ignore").splitlines(), start=1):
        line = raw_line.strip()

        fence_match = re.match(r"^(```+|~~~+)", line)
        if fence_match:
            marker = fence_match.group(1)
            if not in_fence:
                in_fence = True
                fence_delim = marker[0]
            elif fence_delim == marker[0]:
                in_fence = False
            continue

        if in_fence:
            continue

        for match in md_link_re.finditer(raw_line):
            url = match.group(1).strip()
            if should_skip_url(url):
                reason = docs_relative_violation(url)
                if reason:
                    violations.append(LinkViolation(path=path.as_posix(), line=idx, url=url, reason=reason))
                continue

            reason = docs_relative_violation(url)
            if reason:
                violations.append(LinkViolation(path=path.as_posix(), line=idx, url=url, reason=reason))

        for match in html_href_re.finditer(raw_line):
            url = match.group(1).strip()
            reason = docs_relative_violation(url)
            if reason:
                violations.append(LinkViolation(path=path.as_posix(), line=idx, url=url, reason=reason))

    return violations


def main() -> int:
    args = parse_args()
    root = Path(args.root)
    out_json = Path(args.out_json)
    out_md = Path(args.out_md)

    md_files = [
        p
        for p in sorted(root.rglob("*.md"))
        if ".github" not in p.parts and p.is_file()
    ]

    violations: list[LinkViolation] = []
    for md_file in md_files:
        violations.extend(scan_markdown_file(md_file))

    failed = bool(violations)

    report = {
        "failed": failed,
        "files_scanned": len(md_files),
        "violations_count": len(violations),
        "violations": [
            {
                "path": item.path,
                "line": item.line,
                "url": item.url,
                "reason": item.reason,
            }
            for item in violations
        ],
    }

    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_json.write_text(json.dumps(report, indent=2), encoding="utf-8")

    md_lines = [
        "# Absolute Docs Link Policy Report",
        "",
        f"- Failed: {'yes' if failed else 'no'}",
        f"- Markdown files scanned: {len(md_files)}",
        f"- Violations: {len(violations)}",
        "",
    ]

    if violations:
        md_lines.append("## Violations")
        md_lines.append("")
        for item in violations:
            md_lines.append(
                f"- `{item.path}:{item.line}` uses `{item.url}`. {item.reason}"
            )
        md_lines.append("")
    else:
        md_lines.append("No violations detected.")
        md_lines.append("")

    out_md.write_text("\n".join(md_lines), encoding="utf-8")

    print(f"failed={failed} files_scanned={len(md_files)} violations={len(violations)}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
