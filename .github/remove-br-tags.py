#!/usr/bin/env python3
"""
Remove literal '<br />' tags from all Markdown files in the repository.

Default behavior: dry run (reports files that would change).
Use --apply to write changes to disk.

Example:
    python3 remove_br_tags.py
    python3 remove_br_tags.py --apply
"""

import argparse
import pathlib

TARGET = "<br />"


def find_markdown_files(root: pathlib.Path):
    return (p for p in root.rglob("*.md") if p.is_file())


def process_file(path: pathlib.Path, apply: bool) -> bool:
    """
    Returns True if the file would be / was modified.
    """
    text = path.read_text(encoding="utf-8")

    if TARGET not in text:
        return False

    new_text = text.replace(TARGET, "")

    if apply:
        path.write_text(new_text, encoding="utf-8")

    return True


def main():
    parser = argparse.ArgumentParser(
        description="Remove <br /> tags from Markdown files."
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Write changes to files (default is dry run).",
    )
    parser.add_argument(
        "--root",
        default=".",
        help="Root directory to scan (default: current directory).",
    )
    args = parser.parse_args()

    root = pathlib.Path(args.root).resolve()
    modified_files = []

    for md_file in find_markdown_files(root):
        if process_file(md_file, apply=args.apply):
            modified_files.append(md_file)

    if not modified_files:
        print("No <br /> tags found in Markdown files.")
        return

    print(f"\nFound <br /> tags in {len(modified_files)} file(s):")
    for f in modified_files:
        print(f"  - {f}")

    if not args.apply:
        print("\n(Dry run only — re-run with --apply to write changes.)")
    else:
        print("\nChanges applied.")


if __name__ == "__main__":
    main()
