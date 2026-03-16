#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


@dataclass
class DuplicateGroup:
    basename: str
    paths: list[str]


@dataclass
class DepthViolation:
    path: str
    depth: int
    max_depth: int


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Validate docs constraints for ReadMe compatibility: duplicate Markdown "
            "filenames and docs nesting depth for added/renamed PR files."
        )
    )
    parser.add_argument("--docs-root", default="docs", help="Docs root path")
    parser.add_argument(
        "--changed-files-json",
        required=True,
        help="Path to JSON list of changed PR files with filename and status fields",
    )
    parser.add_argument("--max-depth", type=int, default=3, help="Maximum allowed nesting depth under docs/")
    parser.add_argument(
        "--out-json",
        default=".github/automation-reports/readme-constraints-report.json",
        help="Path to JSON report output",
    )
    parser.add_argument(
        "--out-md",
        default=".github/automation-reports/readme-constraints-report.md",
        help="Path to Markdown report output",
    )
    return parser.parse_args()


def normalize_path(value: str) -> str:
    return value.replace("\\", "/").strip()


def is_docs_markdown(path: str) -> bool:
    normalized = normalize_path(path).lower()
    return normalized.startswith("docs/") and normalized.endswith(".md")


def load_changed_files(path: Path) -> list[dict]:
    raw = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(raw, list):
        raise ValueError("changed files JSON must be a list")
    out: list[dict] = []
    for item in raw:
        if not isinstance(item, dict):
            continue
        filename = normalize_path(str(item.get("filename", "")))
        status = str(item.get("status", "")).lower()
        previous_filename = normalize_path(str(item.get("previous_filename", "")))
        out.append(
            {
                "filename": filename,
                "status": status,
                "previous_filename": previous_filename,
            }
        )
    return out


def docs_depth(path: str) -> int:
    parts = Path(normalize_path(path)).parts
    # Example: docs/a/b/file.md => depth 2 (a, b)
    return max(len(parts) - 2, 0)


def collect_docs_files(docs_root: Path) -> list[str]:
    return [p.as_posix() for p in sorted(docs_root.rglob("*.md")) if p.is_file()]


def collect_duplicate_groups(docs_files: Iterable[str]) -> list[DuplicateGroup]:
    by_basename: dict[str, list[str]] = {}
    for path in docs_files:
        basename = Path(path).name.lower()
        by_basename.setdefault(basename, []).append(path)

    groups: list[DuplicateGroup] = []
    for basename, paths in sorted(by_basename.items()):
        if len(paths) > 1:
            groups.append(DuplicateGroup(basename=basename, paths=sorted(paths)))
    return groups


def main() -> int:
    args = parse_args()
    docs_root = Path(args.docs_root)
    changed_files_json = Path(args.changed_files_json)
    out_json = Path(args.out_json)
    out_md = Path(args.out_md)

    if not docs_root.exists():
        raise SystemExit(f"Docs root does not exist: {docs_root}")
    if not changed_files_json.exists():
        raise SystemExit(f"Changed files JSON does not exist: {changed_files_json}")

    changed_files = load_changed_files(changed_files_json)
    docs_files = collect_docs_files(docs_root)
    duplicate_groups = collect_duplicate_groups(docs_files)

    duplicate_lookup = {group.basename: group.paths for group in duplicate_groups}

    duplicate_violations: list[DuplicateGroup] = []
    depth_violations: list[DepthViolation] = []

    for item in changed_files:
        filename = item["filename"]
        status = item["status"]

        if status not in {"added", "renamed"}:
            continue
        if not is_docs_markdown(filename):
            continue

        basename = Path(filename).name.lower()
        matching = duplicate_lookup.get(basename)
        if matching:
            duplicate_violations.append(DuplicateGroup(basename=basename, paths=matching))

        depth = docs_depth(filename)
        if depth > args.max_depth:
            depth_violations.append(DepthViolation(path=filename, depth=depth, max_depth=args.max_depth))

    # De-duplicate duplicate violations by basename.
    seen: set[str] = set()
    uniq_duplicate_violations: list[DuplicateGroup] = []
    for item in duplicate_violations:
        if item.basename in seen:
            continue
        seen.add(item.basename)
        uniq_duplicate_violations.append(item)

    failed = bool(uniq_duplicate_violations or depth_violations)

    report = {
        "failed": failed,
        "max_depth": args.max_depth,
        "docs_markdown_files_scanned": len(docs_files),
        "changed_files_scanned": len(changed_files),
        "duplicate_violations": [
            {
                "basename": item.basename,
                "paths": item.paths,
            }
            for item in uniq_duplicate_violations
        ],
        "depth_violations": [
            {
                "path": item.path,
                "depth": item.depth,
                "max_depth": item.max_depth,
            }
            for item in sorted(depth_violations, key=lambda x: x.path)
        ],
    }

    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_json.write_text(json.dumps(report, indent=2), encoding="utf-8")

    md_lines: list[str] = [
        "# ReadMe Docs Constraints Report",
        "",
        f"- Failed: {'yes' if failed else 'no'}",
        f"- Max allowed docs depth: {args.max_depth}",
        f"- Docs markdown files scanned: {len(docs_files)}",
        f"- Changed files scanned: {len(changed_files)}",
        "",
    ]

    if uniq_duplicate_violations:
        md_lines.append("## Duplicate Filename Violations")
        md_lines.append("")
        for group in uniq_duplicate_violations:
            md_lines.append(f"- `{group.basename}`")
            for path in group.paths:
                md_lines.append(f"  - `{path}`")
        md_lines.append("")

    if depth_violations:
        md_lines.append("## Nesting Depth Violations")
        md_lines.append("")
        for violation in sorted(depth_violations, key=lambda x: x.path):
            md_lines.append(
                f"- `{violation.path}` has depth `{violation.depth}` (max allowed: `{violation.max_depth}`)"
            )
        md_lines.append("")

    if not uniq_duplicate_violations and not depth_violations:
        md_lines.append("No violations detected.")
        md_lines.append("")

    out_md.write_text("\n".join(md_lines), encoding="utf-8")

    print(
        f"failed={failed} duplicate_violations={len(uniq_duplicate_violations)} "
        f"depth_violations={len(depth_violations)}"
    )

    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
