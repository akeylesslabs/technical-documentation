#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Tuple


DEFAULT_CORRECTIONS_PATH = ".cspell/corrections.json"


@dataclass(frozen=True)
class Issue:
    path: Path
    offset: int
    length: int
    text: str
    suggestions: List[str]


def _safe_int(v: Any, default: int = -1) -> int:
    try:
        return int(v)
    except Exception:
        return default


def _load_corrections(path: Path) -> Dict[str, str]:
    """
    Load a JSON object mapping misspelling -> correction.
    Example:
      { "relevalt": "relevant" }

    Returns empty dict if file missing.
    Raises ValueError on invalid structure (intentional; fail fast).
    """
    if not path.exists():
        return {}

    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"Corrections file must be a JSON object mapping strings to strings: {path}")

    out: Dict[str, str] = {}
    for k, v in data.items():
        if not isinstance(k, str) or not isinstance(v, str):
            raise ValueError(f"Corrections keys/values must be strings. Bad entry: {k!r}: {v!r}")
        kk = k.strip()
        vv = v.strip()
        if not kk or not vv:
            raise ValueError(f"Corrections keys/values must be non-empty strings. Bad entry: {k!r}: {v!r}")
        out[kk] = vv

    return out


def _extract_issues(report: Dict[str, Any], repo_root: Path) -> List[Issue]:
    """
    Resilient to minor schema differences from the JSON reporter.
    We keep suggestions list intact, and decide fix strategy later.
    """
    issues_raw = report.get("issues") or []
    out: List[Issue] = []

    for it in issues_raw:
        uri = it.get("uri") or it.get("file") or it.get("filename")
        if not uri:
            continue

        if isinstance(uri, str) and uri.startswith("file://"):
            uri = uri.replace("file://", "", 1)

        file_path = Path(str(uri))
        if not file_path.is_absolute():
            file_path = (repo_root / file_path).resolve()

        offset = _safe_int(it.get("offset"), -1)
        length = _safe_int(it.get("length"), -1)
        text = it.get("text")

        if offset < 0 or length <= 0 or not isinstance(text, str):
            continue

        suggestions_raw = it.get("suggestions") or it.get("suggestion") or []
        if not isinstance(suggestions_raw, list):
            suggestions_raw = []

        suggestions: List[str] = []
        for s in suggestions_raw:
            if isinstance(s, str):
                suggestions.append(s)
            elif isinstance(s, dict):
                w = s.get("word") or s.get("text")
                if isinstance(w, str):
                    suggestions.append(w)

        suggestions = [s.strip() for s in suggestions if isinstance(s, str) and s.strip()]
        out.append(Issue(path=file_path, offset=offset, length=length, text=text, suggestions=suggestions))

    return out


def _choose_replacement(word: str, suggestions: List[str], corrections: Dict[str, str]) -> str | None:
    """
    Priority:
      1) corrections.json mapping (exact match on token)
      2) conservative cspell: exactly one suggestion
    """
    if word in corrections:
        repl = corrections[word]
        return repl if repl != word else None

    if len(suggestions) == 1:
        repl = suggestions[0]
        return repl if repl != word else None

    return None


def _apply_fixes(issues: List[Issue], corrections: Dict[str, str]) -> Tuple[int, int]:
    """
    Applies fixes by offset (from end of file backward).
    Returns: (files_changed, total_replacements)
    """
    by_file: Dict[Path, List[Tuple[int, int, str, str]]] = {}

    for iss in issues:
        repl = _choose_replacement(iss.text, iss.suggestions, corrections)
        if not repl:
            continue
        by_file.setdefault(iss.path, []).append((iss.offset, iss.length, iss.text, repl))

    files_changed = 0
    replacements = 0

    for fpath, fixes in by_file.items():
        if not fpath.exists() or not fpath.is_file():
            continue

        data = fpath.read_text(encoding="utf-8")

        # Apply from end to start so offsets remain valid
        fixes.sort(key=lambda x: x[0], reverse=True)

        changed = False
        for offset, length, expected, repl in fixes:
            start = offset
            end = offset + length
            if start < 0 or end > len(data) or start >= end:
                continue

            current = data[start:end]
            if current != expected:
                # Offsets drifted; skip safely.
                continue

            data = data[:start] + repl + data[end:]
            replacements += 1
            changed = True

        if changed:
            fpath.write_text(data, encoding="utf-8")
            files_changed += 1

    return files_changed, replacements


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--report", required=True, help="Path to cspell JSON report")
    ap.add_argument("--repo-root", default=".", help="Repository root (default: .)")
    ap.add_argument(
        "--corrections",
        default=DEFAULT_CORRECTIONS_PATH,
        help=f"JSON mapping misspelling->correction (default: {DEFAULT_CORRECTIONS_PATH})",
    )
    args = ap.parse_args()

    report_path = Path(args.report).resolve()
    repo_root = Path(args.repo_root).resolve()
    corrections_path = Path(args.corrections).resolve()

    if not report_path.exists():
        print(f"[cspell_autofix] Report not found: {report_path}")
        return 2

    try:
        report = json.loads(report_path.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"[cspell_autofix] Failed to parse JSON report: {e}")
        return 3

    try:
        corrections = _load_corrections(corrections_path)
    except Exception as e:
        print(f"[cspell_autofix] Invalid corrections file: {e}")
        return 4

    issues = _extract_issues(report, repo_root=repo_root)
    files_changed, replacements = _apply_fixes(issues, corrections)

    print(
        f"[cspell_autofix] Issues seen: {len(issues)} | "
        f"Corrections loaded: {len(corrections)} | "
        f"Files changed: {files_changed} | Replacements: {replacements}"
    )

    github_output = os.environ.get("GITHUB_OUTPUT")
    if github_output:
        with open(github_output, "a", encoding="utf-8") as f:
            f.write(f"files_changed={files_changed}\n")
            f.write(f"replacements={replacements}\n")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
