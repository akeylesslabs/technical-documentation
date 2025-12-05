#!/usr/bin/env python3
"""
Safe markdown heading fixer.

Run from anywhere (e.g. `.github/heading-audit`); it will default to the repo root.

What it does, for each *.md file:
- Skips files in IGNORE_FILES.
- Ignores headings inside fenced code blocks (```).
- Fixes multiple H1s:
    - First H1 is kept.
    - Any additional H1 in the same file is downgraded to H2.
- Fixes out-of-sequence heading jumps:
    - If heading level jumps up by more than 1 (e.g. H2 -> H4),
      it is lowered to previous_level + 1 (e.g. H4 -> H3).
- Does NOT change:
    - Heading text/content
    - Anything inside code fences

Default: dry run (prints planned changes only).
Use --apply to write changes to disk.
"""

import argparse
import pathlib
import re
from typing import List, Tuple, Iterable

# Keep this in sync with your workflow's IGNORE_FILES if desired
IGNORE_FILES = {
    "docs/ignore-this.md",
    "docs/path/to/file.md",
    "README.md",
}

HEADING_RE = re.compile(r'^(\s*)(#{1,6})(\s+)(.+)$')

def should_ignore(path: pathlib.Path) -> bool:
    # Relative POSIX-style path, no leading "./"
    rel = path.as_posix()
    if rel.startswith("./"):
        rel = rel[2:]
    return rel in IGNORE_FILES

def fix_headings_in_file(lines: List[str], path: pathlib.Path) -> Tuple[List[str], List[str]]:
    """
    Return (new_lines, changes_descriptions).

    Rules:
    - Only operates outside fenced code blocks.
    - If there are multiple H1s, the first is kept as H1, subsequent H1s -> H2.
    - Prevent heading level jumps upwards by > 1 (e.g. H2 -> H4 becomes H3).
    """
    new_lines = list(lines)
    changes: List[str] = []

    in_code_fence = False
    prev_level_effective = 0
    seen_h1 = False

    for i, line in enumerate(lines):
        stripped = line.lstrip()

        # Toggle fenced code block on lines starting with ```
        if stripped.startswith("```"):
            in_code_fence = not in_code_fence
            continue

        if in_code_fence:
            continue

        m = HEADING_RE.match(line)
        if not m:
            continue

        indent, hashes, space, title = m.groups()
        orig_level = len(hashes)
        new_level = orig_level

        # Rule 1: multiple H1s -> downgrade later H1s to H2
        if orig_level == 1:
            if not seen_h1:
                seen_h1 = True
            else:
                new_level = 2  # safe, predictable downgrade

        # Rule 2: out-of-sequence jumps upward by > 1
        # Use the "current" new_level compared to previous effective level
        if prev_level_effective > 0 and new_level > prev_level_effective + 1:
            new_level = prev_level_effective + 1
            if new_level > 6:
                new_level = 6  # very defensive; should basically never happen

        # If we changed the level, update the line
        if new_level != orig_level:
            new_hashes = "#" * new_level
            new_line = f"{indent}{new_hashes}{space}{title}\n"
            if new_line != line:
                new_lines[i] = new_line
                changes.append(
                    f"{path}: line {i+1}: H{orig_level} -> H{new_level}"
                )
            effective_level = new_level
        else:
            effective_level = orig_level

        prev_level_effective = effective_level

    return new_lines, changes

def find_markdown_files(root: pathlib.Path) -> Iterable[pathlib.Path]:
    for p in root.rglob("*.md"):
        if p.is_file():
            yield p

def detect_repo_root(script_path: pathlib.Path) -> pathlib.Path:
    """
    Detect repo root assuming script is under .github/heading-audit/
    """
    parents = list(script_path.parents)
    # script_path: repo/.github/heading-audit/script.py
    # parents[2] = repo root
    if len(parents) >= 3 and parents[1].name == ".github":
        return parents[2]
    # Fallback: repo root is parent of .github or similar
    return script_path.parent.parent

def resolve_docs_root(script_path: pathlib.Path) -> pathlib.Path:
    repo_root = detect_repo_root(script_path)
    return repo_root / "docs"

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Safely fix out-of-sequence and multiple H1 markdown headings."
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Actually write changes to files (default is dry-run).",
    )
    parser.add_argument(
        "--root",
        type=str,
        default=None,
        help="Root directory to scan (default: repo root inferred from script location).",
    )
    args = parser.parse_args()

    script_path = pathlib.Path(__file__).resolve()
    root = resolve_docs_root(script_path)

    print(f"Scanning markdown files under: {root}")

    if not root.exists():
        print("WARNING: docs/ directory not found. Nothing to scan.")
        return

    print(f"Scanning markdown files under: {root}")

    total_changes = 0

    for path in find_markdown_files(root):
        if should_ignore(path):
            continue

        text = path.read_text(encoding="utf-8")
        lines = text.splitlines(keepends=True)

        new_lines, changes = fix_headings_in_file(lines, path)

        if changes:
            print()
            for ch in changes:
                print("  -", ch)
            total_changes += len(changes)

            if args.apply:
                path.write_text("".join(new_lines), encoding="utf-8")

    print("\nSummary:")
    if total_changes == 0:
        print("  No headings needed changes.")
    else:
        print(f"  {total_changes} heading(s) adjusted.")
        if not args.apply:
            print("  (Dry run only; rerun with --apply to write changes.)")

if __name__ == "__main__":
    main()
