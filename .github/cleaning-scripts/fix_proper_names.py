#!/usr/bin/env python3
"""
fix_proper_names.py

Auto-fix proper-name capitalization issues (AKY013-like) in Markdown files.

Key behaviors (aligned with common markdownlint custom-rule expectations):
- Reads canonical proper-name list from a YAML file:
    * Either a standalone YAML containing:  names: [...]
    * Or a markdownlint-cli2 config YAML containing: config: AKY013: names: [...]
- Skips fenced code blocks (``` or ~~~) and indented code blocks.
- Skips inline code spans: `like this`
- Skips text inside raw URLs (http(s)://... and www....)
- Skips text inside HTML anchor tags: <a ...> ... </a>
- For Markdown link/image syntax: [text](url) and ![alt](url)
    * Fixes only the visible text/alt portion; never touches the URL destination.

Usage:
  python3 .github/cleaning-scripts/fix_proper_names.py \
  --names-file .github/markdownlint/.markdownlint-cli2.yaml \
  --glob "docs/**/*.md" --write

Dry-run (default, excluding --write) prints a summary and diffs per file are not shown to keep output manageable.
"""

from __future__ import annotations

import argparse
import dataclasses
import fnmatch
import os
import re
import sys
from pathlib import Path
from typing import Dict, Iterable, List, Tuple, Optional, Any

try:
    import yaml # PyYAML
except Exception as e:
    print("ERROR: PyYAML is required. Install with: pip install pyyaml", file=sys.stderr)
    raise


# ----------------------------
# YAML loading
# ----------------------------

def _extract_names_from_yaml_obj(obj: Any) -> List[str]:
    """
    Accepts either:
      - {"names": [...]}
      - {"AKY013": {"names": [...]} }
      - {"config": {"AKY013": {"names": [...]}}}
    """
    if not isinstance(obj, dict):
        return []

    # Standalone {names: [...]}
    if isinstance(obj.get("names"), list):
        return [str(x) for x in obj["names"] if str(x).strip()]

    # {AKY013: {names: [...]}}
    aky = obj.get("AKY013")
    if isinstance(aky, dict) and isinstance(aky.get("names"), list):
        return [str(x) for x in aky["names"] if str(x).strip()]

    # markdownlint-cli2 config shape: {config: {AKY013: {names: [...]}}}
    cfg = obj.get("config")
    if isinstance(cfg, dict):
        aky = cfg.get("AKY013")
        if isinstance(aky, dict) and isinstance(aky.get("names"), list):
            return [str(x) for x in aky["names"] if str(x).strip()]

    return []


def load_names(names_file: Path) -> List[str]:
    data = yaml.safe_load(names_file.read_text(encoding="utf-8"))
    names = _extract_names_from_yaml_obj(data)
    # Deduplicate while preserving order
    seen = set()
    out = []
    for n in names:
        n2 = n.strip()
        if not n2:
            continue
        key = n2.lower()
        if key in seen:
            continue
        seen.add(key)
        out.append(n2)
    return out


# ----------------------------
# Markdown parsing helpers
# ----------------------------

URL_RE = re.compile(r"\bhttps?://[^\s)>'\"]+|\bwww\.[^\s)>'\"]+", re.IGNORECASE)

# Markdown link pattern that tolerates nested brackets poorly (intentionally simple, resilient).
# Captures: segments preceding, visible text (or alt), url part.
MD_LINK_RE = re.compile(
    r"""(!?\[)([^\]]*?)(\]\()([^\s)]+?)(\))""",
    re.VERBOSE,
)

INLINE_CODE_RE = re.compile(r"`[^`]*`")

A_TAG_OPEN_RE = re.compile(r"<a(\s|>)", re.IGNORECASE)
A_TAG_CLOSE_RE = re.compile(r"</a\s*>", re.IGNORECASE)

FENCE_RE = re.compile(r"^\s*(```+|~~~+)")
INDENTED_CODE_RE = re.compile(r"^(?:\t| {4,})")


def split_protected_inline_code(s: str) -> List[Tuple[bool, str]]:
    """
    Splits a string into [(is_protected, segment)] where protected segments are inline code spans.
    """
    parts: List[Tuple[bool, str]] = []
    last = 0
    for m in INLINE_CODE_RE.finditer(s):
        if m.start() > last:
            parts.append((False, s[last:m.start()]))
        parts.append((True, m.group(0)))
        last = m.end()
    if last < len(s):
        parts.append((False, s[last:]))
    return parts


def split_protected_urls(s: str) -> List[Tuple[bool, str]]:
    """
    Protect raw URLs from replacement.
    """
    parts: List[Tuple[bool, str]] = []
    last = 0
    for m in URL_RE.finditer(s):
        if m.start() > last:
            parts.append((False, s[last:m.start()]))
        parts.append((True, m.group(0)))
        last = m.end()
    if last < len(s):
        parts.append((False, s[last:]))
    return parts


def split_html_a_regions(s: str) -> List[Tuple[bool, str]]:
    """
    Protect text between <a ...> and </a> (inline HTML anchors).
    Very lightweight; does not fully parse HTML, but works for typical docs usage.
    """
    out: List[Tuple[bool, str]] = []
    i = 0
    protected = False
    while i < len(s):
        if not protected:
            m = A_TAG_OPEN_RE.search(s, i)
            if not m:
                out.append((False, s[i:]))
                break
            if m.start() > i:
                out.append((False, s[i:m.start()]))
            # include the opening tag itself as protected
            # advance to end of tag
            tag_end = s.find(">", m.start())
            if tag_end == -1:
                # malformed; protect rest
                out.append((True, s[m.start():]))
                break
            out.append((True, s[m.start():tag_end+1]))
            i = tag_end + 1
            protected = True
        else:
            m = A_TAG_CLOSE_RE.search(s, i)
            if not m:
                out.append((True, s[i:]))
                break
            if m.start() > i:
                out.append((True, s[i:m.start()]))
            out.append((True, m.group(0)))
            i = m.end()
            protected = False
    return out


def protect_markdown_link_urls(s: str) -> List[Tuple[bool, str]]:
    """
    Splits a string so that only visible link text is editable.
    For patterns like [text](url) and ![alt](url),
    it returns segments where url parts are protected.
    """
    parts: List[Tuple[bool, str]] = []
    last = 0
    for m in MD_LINK_RE.finditer(s):
        if m.start() > last:
            parts.append((False, s[last:m.start()]))

        open_br, vis, mid, url, close_paren = m.groups()
        # opening marker is editable (safe), visible text editable, but URL protected
        parts.append((False, open_br))
        parts.append((False, vis))
        parts.append((False, mid))
        parts.append((True, url))
        parts.append((False, close_paren))
        last = m.end()
    if last < len(s):
        parts.append((False, s[last:]))
    return parts


# ----------------------------
# Replacement engine
# ----------------------------

def build_term_regex(names: List[str]) -> Tuple[re.Pattern, Dict[str, str]]:
    """
    Build a single regex that matches any term (case-insensitive) and a map lower->canonical.
    Use custom boundaries to avoid matching inside words.
    """
    canonical_by_lower: Dict[str, str] = {n.lower(): n for n in names}

    # Sort by length descending so longer terms win when regex alternation overlaps.
    escaped = sorted((re.escape(n) for n in names if n.strip()), key=len, reverse=True)
    if not escaped:
        raise ValueError("No names found.")

    alternation = "|".join(escaped)

    # Custom boundary: avoid matching as substring of alphanumeric/underscore
    # (keeps terms like "API" from matching inside "myAPIThing").
    pat = re.compile(rf"(?<![A-Za-z0-9_])(?:{alternation})(?![A-Za-z0-9_])", re.IGNORECASE)
    return pat, canonical_by_lower


def apply_replacements_to_editable_segment(seg: str, term_re: re.Pattern, canon: Dict[str, str]) -> Tuple[str, int]:
    """
    Replace any case-insensitive match with canonical casing. Returns (new, replacements_count).
    """
    count = 0

    def repl(m: re.Match) -> str:
        nonlocal count
        found = m.group(0)
        canonical = canon.get(found.lower())
        if canonical and found != canonical:
            count += 1
            return canonical
        return found

    new = term_re.sub(repl, seg)
    return new, count


def process_line(line: str, term_re: re.Pattern, canon: Dict[str, str]) -> Tuple[str, int]:
    """
    Process one non-code line.
    Protect (in order):
      - HTML <a> regions
      - Markdown link URLs (only edit visible)
      - raw URLs
      - inline code spans
    Then apply term replacements to editable segments only.
    """
    total = 0

    # 1) split by <a>...</a> regions
    a_parts = split_html_a_regions(line)
    new_line_parts: List[str] = []
    for a_prot, a_seg in a_parts:
        if a_prot:
            new_line_parts.append(a_seg)
            continue

        # 2) protect markdown link destinations
        link_parts = protect_markdown_link_urls(a_seg)
        link_out: List[str] = []
        for l_prot, l_seg in link_parts:
            if l_prot:
                link_out.append(l_seg)
                continue

            # 3) protect raw URLs
            url_parts = split_protected_urls(l_seg)
            url_out: List[str] = []
            for u_prot, u_seg in url_parts:
                if u_prot:
                    url_out.append(u_seg)
                    continue

                # 4) protect inline code
                code_parts = split_protected_inline_code(u_seg)
                code_out: List[str] = []
                for c_prot, c_seg in code_parts:
                    if c_prot:
                        code_out.append(c_seg)
                        continue
                    replaced, n = apply_replacements_to_editable_segment(c_seg, term_re, canon)
                    total += n
                    code_out.append(replaced)
                url_out.append("".join(code_out))
            link_out.append("".join(url_out))
        new_line_parts.append("".join(link_out))

    return "".join(new_line_parts), total


def process_markdown(text: str, term_re: re.Pattern, canon: Dict[str, str]) -> Tuple[str, int]:
    """
    Process a full markdown document with code-block skipping.
    """
    out_lines: List[str] = []
    total = 0

    in_fence = False
    fence_marker = ""

    lines = text.splitlines(keepends=True)
    for raw in lines:
        line = raw.rstrip("\n")
        newline = "\n" if raw.endswith("\n") else ""

        # Fence toggling
        m = FENCE_RE.match(line)
        if m:
            marker = m.group(1)
            if not in_fence:
                in_fence = True
                fence_marker = marker[:3]
            else:
                # Close only when marker matches type/backticks vs tildes
                if marker.startswith(fence_marker):
                    in_fence = False
                    fence_marker = ""
            out_lines.append(line + newline)
            continue

        if in_fence:
            out_lines.append(line + newline)
            continue

        # Indented code blocks
        if INDENTED_CODE_RE.match(line):
            out_lines.append(line + newline)
            continue

        new_line, n = process_line(line, term_re, canon)
        total += n
        out_lines.append(new_line + newline)

    return "".join(out_lines), total


# ----------------------------
# File scanning / CLI
# ----------------------------

def iter_files(root: Path, patterns: List[str]) -> Iterable[Path]:
    for dirpath, _, filenames in os.walk(root):
        for fn in filenames:
            rel = str(Path(dirpath, fn).relative_to(root))
            if any(fnmatch.fnmatch(rel, p) for p in patterns):
                yield Path(dirpath, fn)


@dataclasses.dataclass
class FileResult:
    path: Path
    replacements: int
    changed: bool


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--names-file", required=True, help="YAML file containing AKY013 names list (standalone or full config).")
    ap.add_argument("--root", default=".", help="Root directory to scan (default: .).")
    ap.add_argument("--glob", action="append", dest="globs", default=[], help="Glob patterns relative to root (e.g., docs/**/*.md). Can be specified multiple times.")
    ap.add_argument("--write", action="store_true", help="Write changes in-place. If omitted, runs in dry-run mode.")
    ap.add_argument("--encoding", default="utf-8", help="File encoding (default: utf-8).")
    args = ap.parse_args()

    root = Path(args.root).resolve()
    names_path = Path(args.names_file).resolve()

    if not names_path.exists():
        print(f"ERROR: names file not found: {names_path}", file=sys.stderr)
        return 2

    patterns = args.globs or ["**/*.md"]
    names = load_names(names_path)
    if not names:
        print(f"ERROR: Could not find any names in {names_path}. Expected 'names:' or 'config: AKY013: names:'", file=sys.stderr)
        return 2

    term_re, canon = build_term_regex(names)

    results: List[FileResult] = []
    files = list(iter_files(root, patterns))
    if not files:
        print("No files matched.", file=sys.stderr)
        return 0

    for p in files:
        try:
            original = p.read_text(encoding=args.encoding)
        except UnicodeDecodeError:
            print(f"SKIP (encoding): {p}", file=sys.stderr)
            continue

        updated, n = process_markdown(original, term_re, canon)
        changed = updated != original

        results.append(FileResult(path=p, replacements=n, changed=changed))

        if changed and args.write:
            p.write_text(updated, encoding=args.encoding)

    changed_files = [r for r in results if r.changed]
    total_repl = sum(r.replacements for r in results)

    print(f"Scanned: {len(results)} file(s)")
    print(f"Changed: {len(changed_files)} file(s)")
    print(f"Replacements: {total_repl}")

    if changed_files:
        print("\nTop changed files:")
        for r in sorted(changed_files, key=lambda x: x.replacements, reverse=True)[:25]:
            rel = r.path.relative_to(root)
            print(f"  {rel}  ({r.replacements} replacement(s))")

    # Exit non-zero in dry-run if changes would be made (useful for CI).
    if (not args.write) and changed_files:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
