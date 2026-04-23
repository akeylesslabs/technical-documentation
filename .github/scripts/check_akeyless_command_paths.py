#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import re
import shlex
import subprocess
import traceback
from dataclasses import dataclass
from pathlib import Path


SUPPORTED_COMMANDS = (
    "akeyless",
    "kubectl",
)


ALLOWED_FENCE_LANGS = {
    "",
    "bash",
    "console",
    "curl",
    "cmd",
    "powershell",
    "ps",
    "ps1",
    "shell",
    "sh",
    "text",
    "zsh",
}


@dataclass
class CommandOccurrence:
    file_path: str
    line_number: int
    command_line: str
    cli_name: str
    path_tokens: tuple[str, ...]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Validate supported CLI command paths in markdown code blocks against "
            "`<command> <path> -h`."
        )
    )
    parser.add_argument(
        "--docs-root",
        default="docs",
        help="Root folder to scan for markdown files (default: docs)",
    )
    parser.add_argument(
        "--out-json",
        default=".github/cli-command-paths/command-path-check.json",
        help="Path to JSON report",
    )
    parser.add_argument(
        "--out-md",
        default=".github/cli-command-paths/command-path-check.md",
        help="Path to markdown report",
    )
    return parser.parse_args()


def iter_fenced_code_lines(markdown_text: str):
    in_fence = False
    fence_lang = ""
    for index, raw_line in enumerate(markdown_text.splitlines(), start=1):
        stripped = raw_line.strip()
        fence_match = re.match(r"^```\s*([A-Za-z0-9_-]*)\s*$", stripped)
        if fence_match:
            if not in_fence:
                in_fence = True
                fence_lang = (fence_match.group(1) or "").lower()
            else:
                in_fence = False
                fence_lang = ""
            continue

        if in_fence and fence_lang in ALLOWED_FENCE_LANGS:
            yield index, raw_line


def tokenize_command(line: str) -> list[str]:
    try:
        return shlex.split(line, posix=True)
    except Exception:
        return line.split()


def extract_path_tokens(tokens: list[str]) -> tuple[str, ...]:
    path: list[str] = []
    for token in tokens[1:]:
        if token.startswith("-"):
            break
        if any(mark in token for mark in ("<", ">", "{{", "}}", "$", "(", ")", "=")):
            break
        if not re.match(r"^[a-z][a-z0-9-]*$", token):
            break
        path.append(token)
    return tuple(path)


def collect_commands(md_file: Path) -> list[CommandOccurrence]:
    text = md_file.read_text(encoding="utf-8")
    occurrences: list[CommandOccurrence] = []

    for line_number, raw_line in iter_fenced_code_lines(text):
        normalized = raw_line.strip()
        normalized = re.sub(r"^\s*[$>]\s*", "", normalized)
        tokens = tokenize_command(normalized)
        if not tokens or tokens[0] not in SUPPORTED_COMMANDS:
            continue

        cli_name = tokens[0]
        path_tokens = extract_path_tokens(tokens)
        if not path_tokens:
            continue

        occurrences.append(
            CommandOccurrence(
                file_path=md_file.as_posix(),
                line_number=line_number,
                command_line=normalized,
                cli_name=cli_name,
                path_tokens=path_tokens,
            )
        )

    return occurrences


def run_help(cli_name: str, path_tokens: tuple[str, ...]) -> tuple[bool, str]:
    command = [cli_name, *path_tokens, "-h"]
    proc = subprocess.run(command, capture_output=True, text=True)
    output = (proc.stdout or "") + ("\n" + proc.stderr if proc.stderr else "")
    out_lower = output.lower()

    invalid_markers = (
        "command not found",
        "unknown command",
        "is not a command",
        "unknown shorthand flag",
        "accepts",
    )

    if proc.returncode == 0:
        return True, output.strip()

    if any(marker in out_lower for marker in invalid_markers):
        return False, output.strip()

    return True, output.strip()


def write_reports(
    out_json: Path,
    out_md: Path,
    files_scanned: int,
    checked_paths: int,
    failures: list[dict],
    runtime_error: str | None = None,
) -> None:
    out_json.parent.mkdir(parents=True, exist_ok=True)

    report = {
        "files_scanned": files_scanned,
        "checked_command_paths": checked_paths,
        "failures": failures,
        "failure_count": len(failures),
        "runtime_error": runtime_error,
    }
    out_json.write_text(json.dumps(report, indent=2), encoding="utf-8")

    lines = [
        "# CLI command-path check",
        "",
        f"- Files scanned: {files_scanned}",
        f"- Command paths checked: {checked_paths}",
        f"- Failures: {len(failures)}",
        "",
    ]

    if runtime_error:
        lines.append("## Runtime error")
        lines.append("")
        lines.append("```")
        lines.append(runtime_error)
        lines.append("```")
        lines.append("")

    if failures:
        lines.append("## Invalid command paths")
        lines.append("")
        for failure in failures:
            lines.append(f"- `{failure['path']}` in `{failure['file']}:{failure['line']}`")
            lines.append(f"  - Command: `{failure['command']}`")
            snippet = (failure.get("cli_output") or "").strip().replace("\n", " ")
            if snippet:
                lines.append(f"  - CLI output: `{snippet[:300]}`")
        lines.append("")
    else:
        lines.append("No invalid command paths found.")
        lines.append("")

    out_md.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    args = parse_args()
    docs_root = Path(args.docs_root)
    out_json = Path(args.out_json)
    out_md = Path(args.out_md)
    files_scanned = 0
    checked_paths = 0
    failures: list[dict] = []

    try:
        if not docs_root.exists():
            raise RuntimeError(f"Docs root does not exist: {docs_root}")

        missing_clis = [
            cli_name
            for cli_name in SUPPORTED_COMMANDS
            if subprocess.run([cli_name, "-h"], capture_output=True).returncode != 0
        ]
        if missing_clis:
            raise RuntimeError(
                "Required CLI command(s) are not available in PATH: "
                + ", ".join(missing_clis)
            )

        md_files = sorted(docs_root.rglob("*.md"))
        files_scanned = len(md_files)

        occurrences: list[CommandOccurrence] = []
        for md_file in md_files:
            occurrences.extend(collect_commands(md_file))

        unique_paths = sorted({(occ.cli_name, occ.path_tokens) for occ in occurrences})
        checked_paths = len(unique_paths)

        validation_cache: dict[tuple[str, tuple[str, ...]], tuple[bool, str]] = {}
        for cli_name, path_tokens in unique_paths:
            validation_cache[(cli_name, path_tokens)] = run_help(cli_name, path_tokens)

        for occ in occurrences:
            is_valid, cli_output = validation_cache[(occ.cli_name, occ.path_tokens)]
            if is_valid:
                continue
            failures.append(
                {
                    "file": occ.file_path,
                    "line": occ.line_number,
                    "command": occ.command_line,
                    "path": f"{occ.cli_name} {' '.join(occ.path_tokens)}",
                    "cli_output": cli_output,
                }
            )

        write_reports(
            out_json=out_json,
            out_md=out_md,
            files_scanned=files_scanned,
            checked_paths=checked_paths,
            failures=failures,
            runtime_error=None,
        )

        print(
            f"files_scanned={files_scanned} checked_command_paths={checked_paths} failures={len(failures)}"
        )

        return 1 if failures else 0
    except Exception as exc:
        runtime_error = "".join(traceback.format_exception(exc)).strip()
        write_reports(
            out_json=out_json,
            out_md=out_md,
            files_scanned=files_scanned,
            checked_paths=checked_paths,
            failures=failures,
            runtime_error=runtime_error,
        )
        print(f"runtime_error={exc}")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
