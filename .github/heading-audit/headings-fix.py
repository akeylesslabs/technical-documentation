#!/usr/bin/env python3
"""
Safe markdown heading fixer for docs/.

Behavior:

- Only scans the docs/ directory of the repo (no --root needed).
- Skips files listed in IGNORE_FILES (paths relative to repo root).
- Ignores headings inside fenced code blocks (```).
- Per file:
    - If any H1 (#) exists outside code fences:
        - Demote ALL headings by 1 level:
          H1->H2, H2->H3, ..., capped at H6.
    - Then enforce: no upward jump of more than 1 level,
      e.g., H2 -> H4 becomes H3.
- Applies conservative capitalization to heading text:
    - Title-style capitalization with small-word rules.
    - Preserves acronyms, mixed case, CLI flags, placeholders,
      URLs, and backticked text.
- Removes trailing periods from headings (safe punctuation cleanup).
- Does NOT change text inside fenced code blocks.

Usage:

    python3 .github/heading-audit/headings-fix.py
    python3 .github/heading-audit/headings-fix.py --apply
"""

import argparse
import pathlib
import re
import string
from typing import Iterable, List, Tuple

IGNORE_FILES = {
    "docs/ignore-this.md",
    "docs/path/to/file.md",
    "README.md",
}

HEADING_RE = re.compile(r'^(\s*)(#{1,6})(\s+)(.+)$')

SMALL_WORDS = {
    "a", "an", "the",
    "and", "or", "but",
    "for", "nor",
    "on", "at", "to", "from", "by", "in", "of",
}

def detect_repo_root(script_path: pathlib.Path) -> pathlib.Path:
    parents = list(script_path.parents)
    if len(parents) >= 3 and parents[1].name == ".github":
        return parents[2]
    return script_path.parent.parent

def resolve_docs_root(script_path: pathlib.Path) -> Tuple[pathlib.Path, pathlib.Path]:
    repo_root = detect_repo_root(script_path)
    docs_root = repo_root / "docs"
    return repo_root, docs_root

def should_ignore(path: pathlib.Path, repo_root: pathlib.Path) -> bool:
    try:
        rel = path.relative_to(repo_root).as_posix()
    except ValueError:
        return False
    return rel in IGNORE_FILES

def should_preserve_word(core: str) -> bool:
    if core.startswith("<") and core.endswith(">"):
        return True
    if core.startswith("{") and core.endswith("}"):
        return True
    if core.startswith("--"):
        return True
    if core.startswith("http://") or core.startswith("https://"):
        return True
    if core.startswith("`") and core.endswith("`"):
        return True
    if core.isupper() and len(core) > 1:
        return True
    if any(c.islower() for c in core) and any(c.isupper() for c in core):
        return True
    return False

def title_case_heading_text(text: str) -> str:
    words = text.split()
    if not words:
        return text

    new_words: List[str] = []

    for i, word in enumerate(words):
        # detect prefix/suffix punctuation properly
        leading = len(word) - len(word.lstrip(string.punctuation))
        trailing = len(word) - len(word.rstrip(string.punctuation))

        prefix = word[:leading]
        suffix = word[len(word) - trailing:] if trailing > 0 else ""
        core = word[leading: len(word) - trailing] if trailing > 0 else word[leading:]

        if not core:
            new_words.append(word)
            continue

        if should_preserve_word(core):
            new_words.append(word)
            continue

        lower_core = core.lower()

        if i == 0:
            new_core = core[0].upper() + core[1:].lower()
        else:
            if lower_core in SMALL_WORDS:
                new_core = lower_core
            else:
                new_core = core[0].upper() + core[1:].lower()

        new_words.append(prefix + new_core + suffix)

    return " ".join(new_words)

def remove_trailing_periods(text: str) -> str:
    return text.rstrip(".")  # remove one or more periods

def compute_bump(lines: List[str]) -> int:
    in_code_fence = False
    for line in lines:
        stripped = line.lstrip()
        if stripped.startswith("```"):
            in_code_fence = not in_code_fence
            continue
        if in_code_fence:
            continue
        m = HEADING_RE.match(line)
        if not m:
            continue
        if len(m.group(2)) == 1:
            return 1
    return 0

def fix_headings_in_file(lines: List[str], path: pathlib.Path) -> Tuple[List[str], List[str]]:
    new_lines = list(lines)
    changes: List[str] = []
    bump = compute_bump(lines)

    in_code_fence = False
    prev_effective_level = 0

    for i, line in enumerate(lines):
        stripped = line.lstrip()

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
        new_level = min(orig_level + bump, 6)

        if prev_effective_level and new_level > prev_effective_level + 1:
            new_level = prev_effective_level + 1

        # Capitalize safely
        fixed_title = title_case_heading_text(title)
        # Remove trailing periods
        fixed_title = remove_trailing_periods(fixed_title)

        new_hashes = "#" * new_level
        new_line = f"{indent}{new_hashes}{space}{fixed_title}\n"

        if new_line != line:
            new_lines[i] = new_line
            if new_level != orig_level:
                changes.append(f"{path}: line {i+1}: H{orig_level} -> H{new_level}")
            else:
                changes.append(f"{path}: line {i+1}: capitalization/punctuation adjusted")

        prev_effective_level = new_level

    return new_lines, changes

def find_markdown_files(root: pathlib.Path) -> Iterable[pathlib.Path]:
    for p in root.rglob("*.md"):
        if p.is_file():
            yield p

def main() -> None:
    parser = argparse.ArgumentParser(description="Safely adjust markdown headings in docs/.")
    parser.add_argument("--apply", action="store_true", help="Write changes to files.")
    args = parser.parse_args()

    script_path = pathlib.Path(__file__).resolve()
    repo_root, docs_root = resolve_docs_root(script_path)

    print(f"Scanning markdown files under: {docs_root}")

    if not docs_root.exists():
        print("WARNING: docs/ folder not found. Nothing to scan.")
        return

    total_changes = 0

    for path in find_markdown_files(docs_root):
        if should_ignore(path, repo_root):
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
            print("  (Dry run — rerun with --apply to write changes.)")

if __name__ == "__main__":
    main()
