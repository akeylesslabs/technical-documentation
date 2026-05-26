#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import re
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


@dataclass
class FrontMatterViolation:
    path: str
    reason: str


@dataclass
class IndexTitleParentViolation:
    path: str
    title: str
    parent_directory: str
    reason: str


@dataclass
class ApiReferenceSuffixViolation:
    path: str
    reason: str


@dataclass
class NavigationViolation:
    path: str
    reason: str


@dataclass
class RequiredOrderFileViolation:
    path: str
    reason: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Validate docs constraints for ReadMe compatibility: duplicate Markdown "
            "filenames, docs nesting depth, front matter schema, and _order.yaml "
            "navigation integrity for added/renamed PR files."
        )
    )
    parser.add_argument("--docs-root", default="docs", help="Docs root path")
    parser.add_argument(
        "--required-order-roots",
        nargs="+",
        default=["docs", "reference", "recipes"],
        help="Root directories where every directory must contain _order.yaml",
    )
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


def collect_index_parent_groups(docs_files: Iterable[str]) -> dict[str, list[str]]:
    by_parent_name: dict[str, list[str]] = {}
    for path in docs_files:
        normalized = normalize_path(path)
        parsed = Path(normalized)
        if parsed.name.lower() != "index.md":
            continue

        parent_name = parsed.parent.name.lower()
        by_parent_name.setdefault(parent_name, []).append(normalized)

    return by_parent_name


def changed_docs_markdown_files(changed_files: list[dict]) -> list[str]:
    candidates: list[str] = []
    for item in changed_files:
        if item["status"] not in {"added", "renamed"}:
            continue
        if not is_docs_markdown(item["filename"]):
            continue
        candidates.append(item["filename"])
    return sorted(set(candidates))


def changed_docs_index_files_for_title_validation(changed_files: list[dict]) -> list[str]:
    candidates: list[str] = []
    for item in changed_files:
        if item["status"] not in {"added", "renamed", "modified"}:
            continue
        filename = item["filename"]
        if not is_docs_markdown(filename):
            continue
        if Path(filename).name.lower() != "index.md":
            continue
        candidates.append(filename)
    return sorted(set(candidates))


def split_front_matter(text: str) -> list[str] | None:
    lines = text.splitlines()
    if not lines:
        return None
    if lines[0].strip() != "---":
        return None

    end_idx = None
    for idx in range(1, len(lines)):
        if lines[idx].strip() == "---":
            end_idx = idx
            break

    if end_idx is None:
        return None

    return lines[1:end_idx]


def validate_front_matter(path: Path) -> list[str]:
    if not path.exists():
        return ["File does not exist in repository state"]

    text = path.read_text(encoding="utf-8", errors="ignore")
    front_matter_lines = split_front_matter(text)

    if front_matter_lines is None:
        return ["Missing YAML front matter block at top of file"]

    block = "\n".join(front_matter_lines)

    required_top_level = ["title", "excerpt", "deprecated", "hidden", "metadata"]
    errors: list[str] = []

    for key in required_top_level:
        if not re.search(rf"(?m)^{re.escape(key)}\s*:", block):
            errors.append(f"Missing required front matter key '{key}'")

    if re.search(r"(?m)^deprecated\s*:", block) and not re.search(
        r"(?m)^deprecated\s*:\s*(true|false)\s*$", block, flags=re.IGNORECASE
    ):
        errors.append("Front matter key 'deprecated' must be a boolean (true/false)")

    if re.search(r"(?m)^hidden\s*:", block) and not re.search(
        r"(?m)^hidden\s*:\s*(true|false)\s*$", block, flags=re.IGNORECASE
    ):
        errors.append("Front matter key 'hidden' must be a boolean (true/false)")

    if re.search(r"(?m)^metadata\s*:", block):
        for subkey in ["title", "description", "robots"]:
            if not re.search(rf"(?m)^\s{{2,}}{re.escape(subkey)}\s*:", block):
                errors.append(f"Missing required metadata key '{subkey}'")

    return errors


def extract_front_matter_title(path: Path) -> str | None:
    if not path.exists():
        return None

    text = path.read_text(encoding="utf-8", errors="ignore")
    front_matter_lines = split_front_matter(text)
    if front_matter_lines is None:
        return None

    for line in front_matter_lines:
        match = re.match(r"^title\s*:\s*(.+?)\s*$", line.strip())
        if not match:
            continue
        return match.group(1).strip().strip('"').strip("'")

    return None


def normalize_title_parent_match_value(value: str) -> str:
    normalized = value.strip().lower()
    normalized = normalized.replace("_", "-")
    normalized = re.sub(r"\s+", "-", normalized)
    normalized = re.sub(r"-+", "-", normalized)
    return normalized.strip("-")


def parse_order_entries(order_file: Path) -> tuple[list[str], list[str]]:
    if not order_file.exists():
        return [], ["Missing _order.yaml"]

    text = order_file.read_text(encoding="utf-8", errors="ignore")
    stripped = text.strip()
    if stripped in {"[]", "[ ]"}:
        return [], []

    entries: list[str] = []
    errors: list[str] = []

    for idx, line in enumerate(text.splitlines(), start=1):
        raw = line.strip()
        if not raw or raw.startswith("#"):
            continue
        if not raw.startswith("- "):
            errors.append(f"Invalid _order.yaml format on line {idx}; expected list item '- <entry>'")
            continue

        item = raw[2:].strip()
        if not item:
            errors.append(f"Empty _order.yaml entry on line {idx}")
            continue

        if len(item) >= 2 and item[0] == item[-1] and item[0] in {'"', "'"}:
            item = item[1:-1].strip()

        if item:
            entries.append(item)

    return entries, errors


def entry_matches(entries: list[str], expected: str) -> bool:
    expected_lower = expected.lower()
    return any(item.lower() == expected_lower for item in entries)


def resolve_expected_order_target(markdown_path: Path) -> tuple[Path | None, str | None]:
    if markdown_path.name.lower() == "index.md":
        parent = markdown_path.parent
        grandparent = parent.parent
        if str(grandparent) == ".":
            return None, None
        return grandparent / "_order.yaml", parent.name

    return markdown_path.parent / "_order.yaml", markdown_path.stem


def order_entry_target_exists(order_file: Path, entry: str) -> bool:
    base_dir = order_file.parent
    return (base_dir / entry).exists() or (base_dir / f"{entry}.md").exists()


def collect_required_order_file_violations(roots: Iterable[str]) -> list[RequiredOrderFileViolation]:
    violations: list[RequiredOrderFileViolation] = []

    for root in roots:
        root_path = Path(root)
        if not root_path.exists() or not root_path.is_dir():
            continue

        dirs_to_check = [root_path] + [p for p in sorted(root_path.rglob("*")) if p.is_dir()]
        for directory in dirs_to_check:
            order_file = directory / "_order.yaml"
            if not order_file.exists():
                violations.append(
                    RequiredOrderFileViolation(
                        path=directory.as_posix(),
                        reason="Missing required _order.yaml",
                    )
                )

    return violations

def collect_api_reference_suffix_violations(api_reference_root: Path) -> list[ApiReferenceSuffixViolation]:
    violations: list[ApiReferenceSuffixViolation] = []

    if not api_reference_root.exists() or not api_reference_root.is_dir():
        return violations

    for markdown_file in sorted(api_reference_root.rglob("*.md")):
        if not markdown_file.is_file():
            continue
        if markdown_file.name.lower().endswith("-1.md"):
            violations.append(
                ApiReferenceSuffixViolation(
                    path=markdown_file.as_posix(),
                    reason="API reference page filenames must not end with '-1'",
                )
            )

    return violations


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
    changed_docs = changed_docs_markdown_files(changed_files)
    changed_docs_indexes = changed_docs_index_files_for_title_validation(changed_files)

    docs_files = collect_docs_files(docs_root)
    duplicate_groups = collect_duplicate_groups(docs_files)
    index_parent_groups = collect_index_parent_groups(docs_files)

    duplicate_lookup = {group.basename: group.paths for group in duplicate_groups}

    duplicate_violations: list[DuplicateGroup] = []
    depth_violations: list[DepthViolation] = []
    front_matter_violations: list[FrontMatterViolation] = []
    index_title_parent_violations: list[IndexTitleParentViolation] = []
    navigation_violations: list[NavigationViolation] = []
    required_order_file_violations = collect_required_order_file_violations(args.required_order_roots)
    api_reference_suffix_violations = collect_api_reference_suffix_violations(Path("reference") / "Akeyless API")

    order_files_to_validate: set[Path] = set()

    for filename in changed_docs:
        basename = Path(filename).name.lower()
        if basename == "index.md":
            parent_name = Path(filename).parent.name.lower()
            matching_index_paths = sorted(index_parent_groups.get(parent_name, []))
            if len(matching_index_paths) > 1:
                duplicate_violations.append(
                    DuplicateGroup(
                        basename=f"index.md (parent: {parent_name})",
                        paths=matching_index_paths,
                    )
                )
        else:
            matching = duplicate_lookup.get(basename)
            if matching:
                duplicate_violations.append(DuplicateGroup(basename=basename, paths=matching))

        depth = docs_depth(filename)
        if depth > args.max_depth:
            depth_violations.append(DepthViolation(path=filename, depth=depth, max_depth=args.max_depth))

        file_path = Path(filename)
        for reason in validate_front_matter(file_path):
            front_matter_violations.append(FrontMatterViolation(path=filename, reason=reason))

        order_file, expected_entry = resolve_expected_order_target(file_path)
        if order_file is not None and expected_entry is not None:
            order_files_to_validate.add(order_file)
            entries, order_errors = parse_order_entries(order_file)
            if order_errors:
                for error in order_errors:
                    navigation_violations.append(NavigationViolation(path=order_file.as_posix(), reason=error))
            elif not entry_matches(entries, expected_entry):
                navigation_violations.append(
                    NavigationViolation(
                        path=order_file.as_posix(),
                        reason=(
                            f"Missing navigation entry '{expected_entry}' required by changed file '{filename}'"
                        ),
                    )
                )

    for filename in changed_docs_indexes:
        file_path = Path(filename)
        title = extract_front_matter_title(file_path)
        parent_directory = file_path.parent.name

        if title is None:
            index_title_parent_violations.append(
                IndexTitleParentViolation(
                    path=filename,
                    title="",
                    parent_directory=parent_directory,
                    reason="index.md page is missing a parsable front matter 'title'",
                )
            )
            continue

        normalized_title = normalize_title_parent_match_value(title)
        normalized_parent = normalize_title_parent_match_value(parent_directory)
        if normalized_title != normalized_parent:
            index_title_parent_violations.append(
                IndexTitleParentViolation(
                    path=filename,
                    title=title,
                    parent_directory=parent_directory,
                    reason=(
                        f"index.md title '{title}' must match parent directory name "
                        f"'{parent_directory}'"
                    ),
                )
            )

    # Validate target existence for entries in impacted _order.yaml files.
    for order_file in sorted(order_files_to_validate):
        entries, order_errors = parse_order_entries(order_file)
        if order_errors:
            continue
        for entry in entries:
            if not order_entry_target_exists(order_file, entry):
                navigation_violations.append(
                    NavigationViolation(
                        path=order_file.as_posix(),
                        reason=f"Navigation entry '{entry}' does not match an existing child file or directory",
                    )
                )

    # De-duplicate duplicate violations by basename.
    seen_dupes: set[str] = set()
    uniq_duplicate_violations: list[DuplicateGroup] = []
    for item in duplicate_violations:
        if item.basename in seen_dupes:
            continue
        seen_dupes.add(item.basename)
        uniq_duplicate_violations.append(item)

    # De-duplicate front matter and navigation violations.
    fm_seen: set[tuple[str, str]] = set()
    uniq_front_matter_violations: list[FrontMatterViolation] = []
    for item in front_matter_violations:
        key = (item.path, item.reason)
        if key in fm_seen:
            continue
        fm_seen.add(key)
        uniq_front_matter_violations.append(item)

    nav_seen: set[tuple[str, str]] = set()
    uniq_navigation_violations: list[NavigationViolation] = []
    for item in navigation_violations:
        key = (item.path, item.reason)
        if key in nav_seen:
            continue
        nav_seen.add(key)
        uniq_navigation_violations.append(item)

    title_parent_seen: set[tuple[str, str]] = set()
    uniq_index_title_parent_violations: list[IndexTitleParentViolation] = []
    for item in index_title_parent_violations:
        key = (item.path, item.reason)
        if key in title_parent_seen:
            continue
        title_parent_seen.add(key)
        uniq_index_title_parent_violations.append(item)

    failed = bool(
        uniq_duplicate_violations
        or depth_violations
        or uniq_front_matter_violations
        or uniq_index_title_parent_violations
        or uniq_navigation_violations
        or required_order_file_violations
        or api_reference_suffix_violations
    )

    report = {
        "failed": failed,
        "max_depth": args.max_depth,
        "docs_markdown_files_scanned": len(docs_files),
        "changed_files_scanned": len(changed_files),
        "changed_docs_markdown_scanned": len(changed_docs),
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
        "front_matter_violations": [
            {
                "path": item.path,
                "reason": item.reason,
            }
            for item in sorted(uniq_front_matter_violations, key=lambda x: (x.path, x.reason))
        ],
        "index_title_parent_violations": [
            {
                "path": item.path,
                "title": item.title,
                "parent_directory": item.parent_directory,
                "reason": item.reason,
            }
            for item in sorted(uniq_index_title_parent_violations, key=lambda x: (x.path, x.reason))
        ],
        "navigation_violations": [
            {
                "path": item.path,
                "reason": item.reason,
            }
            for item in sorted(uniq_navigation_violations, key=lambda x: (x.path, x.reason))
        ],
        "required_order_file_violations": [
            {
                "path": item.path,
                "reason": item.reason,
            }
            for item in sorted(required_order_file_violations, key=lambda x: x.path)
        ],
        "api_reference_suffix_violations": [
            {
                "path": item.path,
                "reason": item.reason,
            }
            for item in sorted(api_reference_suffix_violations, key=lambda x: x.path)
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
        f"- Changed docs markdown files scanned: {len(changed_docs)}",
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

    if uniq_front_matter_violations:
        md_lines.append("## Front Matter Schema Violations")
        md_lines.append("")
        for violation in sorted(uniq_front_matter_violations, key=lambda x: (x.path, x.reason)):
            md_lines.append(f"- `{violation.path}`: {violation.reason}")
        md_lines.append("")

    if uniq_index_title_parent_violations:
        md_lines.append("## Index Title/Directory Match Violations")
        md_lines.append("")
        for violation in sorted(uniq_index_title_parent_violations, key=lambda x: (x.path, x.reason)):
            md_lines.append(f"- `{violation.path}`: {violation.reason}")
        md_lines.append("")

    if uniq_navigation_violations:
        md_lines.append("## Navigation Integrity Violations")
        md_lines.append("")
        for violation in sorted(uniq_navigation_violations, key=lambda x: (x.path, x.reason)):
            md_lines.append(f"- `{violation.path}`: {violation.reason}")
        md_lines.append("")

    if required_order_file_violations:
        md_lines.append("## Required _order.yaml Violations")
        md_lines.append("")
        for violation in sorted(required_order_file_violations, key=lambda x: x.path):
            md_lines.append(f"- `{violation.path}`: {violation.reason}")
        md_lines.append("")

    if api_reference_suffix_violations:
        md_lines.append("## API Reference Suffix Violations")
        md_lines.append("")
        for violation in sorted(api_reference_suffix_violations, key=lambda x: x.path):
            md_lines.append(f"- `{violation.path}`: {violation.reason}")
        md_lines.append("")

    if (
        not uniq_duplicate_violations
        and not depth_violations
        and not uniq_front_matter_violations
        and not uniq_index_title_parent_violations
        and not uniq_navigation_violations
        and not required_order_file_violations
        and not api_reference_suffix_violations
    ):
        md_lines.append("No violations detected.")
        md_lines.append("")

    out_md.write_text("\n".join(md_lines), encoding="utf-8")

    print(
        "failed={failed} duplicate_violations={dupes} depth_violations={depth} "
        "front_matter_violations={fm} index_title_parent_violations={title_parent} navigation_violations={nav} "
        "required_order_file_violations={order} api_reference_suffix_violations={api_suffix}".format(
            failed=failed,
            dupes=len(uniq_duplicate_violations),
            depth=len(depth_violations),
            fm=len(uniq_front_matter_violations),
            title_parent=len(uniq_index_title_parent_violations),
            nav=len(uniq_navigation_violations),
            order=len(required_order_file_violations),
            api_suffix=len(api_reference_suffix_violations),
        )
    )

    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
