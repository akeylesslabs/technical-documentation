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
- Applies conservative capitalization to all heading text:
    - Title-style capitalization with small-word rules.
    - Preserves acronyms, mixed-case words, CLI flags, placeholders, URLs, and backticked text.
- Does NOT change heading text inside code fences.

Usage (from repo root or anywhere):

    python3 .github/heading-audit/headings-fix.py        # dry run
    python3 .github/heading-audit/headings-fix.py --apply
"""

import argparse
import pathlib
import re
import string
from typing import Iterable, List, Tuple

# Paths relative to repo root
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
    """
    Detect repo root assuming script is under:
        <repo>/.github/heading-audit/headings-fix.py
    """
    parents = list(script_path.parents)
    # parents[0] = .../.github/heading-audit
    # parents[1] = .../.github
    # parents[2] = .../<repo>
    if len(parents) >= 3 and parents[1].name == ".github":
        return parents[2]
    # Fallback: two levels above the script
    return script_path.parent.parent


def resolve_docs_root(script_path: pathlib.Path) -> Tuple[pathlib.Path, pathlib.Path]:
    """
    Return (repo_root, docs_root).
    """
    repo_root = detect_repo_root(script_path)
    docs_root = repo_root / "docs"
    return repo_root, docs_root


def should_ignore(path: pathlib.Path, repo_root: pathlib.Path) -> bool:
    """
    Check if a given file path (absolute) should be ignored,
    using paths relative to the repo root.
    """
    try:
        rel = path.relative_to(repo_root).as_posix()
    except ValueError:
        # Path is not under repo_root for some reason; don't ignore by default.
        return False
    return rel in IGNORE_FILES


def should_preserve_word(word: str) -> bool:
    """Return True if the word should NOT be touched for capitalization."""
    # preserve placeholders <id>, {name}
    if word.startswith("<") and word.endswith(">"):
        return True
    if word.startswith("{") and word.endswith("}"):
        return True
    # preserve code-like arguments
    if word.startswith("--"):
        return True
    # preserve URLs
    if word.startswith("http://") or word.startswith("https://"):
        return True
    # preserve backticks
    if word.startswith("`") and word.endswith("`"):
        return True
    # preserve all caps (API, SSH)
    if word.isupper() and len(word) > 1:
        return True
    # preserve words with mixed case (GitHub, PowerShell)
    if any(c.islower() for c in word) and any(c.isupper() for c in word):
        return True
    return False


def title_case_heading_text(text: str) -> str:
    """
    Apply conservative, safe capitalization to heading text.

    - First word always capitalized (if not preserved).
    - Small words (a, an, the, in, of, ...) are lowercased unless first.
    - Preserves acronyms, mixed case, CLI flags, placeholders, URLs, and backticked text.
    """
    words = text.split()
    if not words:
        return text

    new_words: List[str] = []

    for i, word in enumerate(words):
        # Strip leading/trailing punctuation for decisions,
        # but keep the original punctuation wrapping.
        stripped = word.strip(string.punctuation)

        if not stripped:
            new_words.append(word)
            continue

        if should_preserve_word(stripped):
            new_words.append(word)
            continue

        # First word: always capitalized
        if i == 0:
            new_words.append(word[0:len(word) - len(stripped)] + stripped.capitalize() + word[len(word.rstrip(string.punctuation)):])
            continue

        # Small-word rule
        if stripped.lower() in SMALL_WORDS:
            new_words.append(word[0:len(word) - len(stripped)] + stripped.lower() + word[len(word.rstrip(string.punctuation)):])
            continue

        # Default: Capitalize
        new_words.append(word[0:len(word) - len(stripped)] + stripped.capitalize() + word[len(word.rstrip(string.punctuation)):])

    return " ".join(new_words)


def compute_bump(lines: List[str]) -> int:
    """
    Decide how much to shift heading levels for this file.

    - If we see any H1 (outside code fences), bump = 1
      (H1->H2, H2->H3, etc.).
    - Otherwise bump = 0.
    """
    in_code_fence = False

    for line in lines:
        stripped = line.lstrip()

        # Toggle fenced code block on ``` lines
        if stripped.startswith("```"):
            in_code_fence = not in_code_fence
            continue

        if in_code_fence:
            continue

        m = HEADING_RE.match(line)
        if not m:
            continue

        hashes = m.group(2)
        level = len(hashes)
        if level == 1:
            return 1

    return 0


def fix_headings_in_file(lines: List[str], path: pathlib.Path) -> Tuple[List[str], List[str]]:
    """
    For a single file:

    - If any H1 exists (outside code fences), demote ALL headings by 1:
        H1->H2, H2->H3, ..., capped at H6.
    - Then ensure we never jump upward by more than 1 level (H2->H4 -> H3).
    - Apply safe capitalization to heading text.
    - Ignore headings inside fenced code blocks.
    """
    new_lines = list(lines)
    changes: List[str] = []

    bump = compute_bump(lines)  # 0 or 1

    in_code_fence = False
    prev_level_effective = 0  # after bump + jump-fix

    for i, line in enumerate(lines):
        stripped = line.lstrip()

        # Toggle fenced code block state
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

        # Base new level: apply bump (if any)
        new_level = orig_level + bump
        if new_level > 6:
            new_level = 6  # very defensive

        # Fix big upward jumps: only if we've seen a heading before
        if prev_level_effective > 0 and new_level > prev_level_effective + 1:
            new_level = prev_level_effective + 1
            if new_level > 6:
                new_level = 6

        # Apply capitalization to the title text
        fixed_title = title_case_heading_text(title)

        # Build the new line as it *should* look
        new_hashes = "#" * new_level
        new_line = f"{indent}{new_hashes}{space}{fixed_title}\n"

        # Only record and write if it's actually different
        if new_line != line:
            new_lines[i] = new_line
            if new_level != orig_level:
                changes.append(f"{path}: line {i+1}: H{orig_level} -> H{new_level}")
            else:
                changes.append(f"{path}: line {i+1}: text capitalization adjusted")

        prev_level_effective = new_level

    return new_lines, changes


def find_markdown_files(root: pathlib.Path) -> Iterable[pathlib.Path]:
    """
    Yield all *.md files under the given root directory.
    """
    for p in root.rglob("*.md"):
        if p.is_file():
            yield p


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Safely adjust markdown headings in docs/."
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Write changes to files (default: dry run).",
    )
    args = parser.parse_args()

    script_path = pathlib.Path(__file__).resolve()
    repo_root, docs_root = resolve_docs_root(script_path)

    print(f"Scanning markdown files under: {docs_root}")

    if not docs_root.exists():
        print("WARNING: docs/ directory not found. Nothing to scan.")
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
            print("  (Dry run; run again with --apply to write changes.)")


if __name__ == "__main__":
    main()
