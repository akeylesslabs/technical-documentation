#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import re
import shlex
import shutil
import subprocess
import traceback
from dataclasses import dataclass
from pathlib import Path


SUPPORTED_COMMANDS = (
    "akeyless",
    "aws",
    "az",
    "certbot",
    "curl",
    "docker",
    "eksctl",
    "gcloud",
    "helm",
    "jq",
    "kubectl",
    "oci",
    "openssl",
    "ssh",
    "terraform",
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


@dataclass(frozen=True)
class CliValidator:
    help_flag: str = "-h"
    invalid_patterns: tuple[str, ...] = ()


DEFAULT_CLI_VALIDATOR = CliValidator()


GENERIC_INVALID_PATTERNS = (
    r"\bcommand not found\b",
    r"\bunknown command\b",
    r"\bis not a command\b",
    r"\bno help topic\b",
    r"\bunknown shorthand flag\b",
)


CLI_VALIDATORS: dict[str, CliValidator] = {
    "aws": CliValidator(
        invalid_patterns=(
            r"\baws:\s+error:\s+argument\s+command:\s+invalid\s+choice\b",
        )
    ),
    "az": CliValidator(
        invalid_patterns=(
            r"\berror:\s+'.+'\s+is\s+misspelled\s+or\s+not\s+recognized\b",
        )
    ),
    "docker": CliValidator(
        invalid_patterns=(
            r"\bdocker:\s+'.+'\s+is\s+not\s+a\s+docker\s+command\b",
        )
    ),
    "gcloud": CliValidator(
        invalid_patterns=(
            r"\berror:\s+\(.+\)\s+invalid\s+choice:\b",
        )
    ),
    "helm": CliValidator(
        invalid_patterns=(
            r"\berror:\s+unknown\s+command\b",
        )
    ),
    "kubectl": CliValidator(
        invalid_patterns=(
            r"\berror:\s+unknown\s+command\b",
        )
    ),
    "terraform": CliValidator(
        invalid_patterns=(
            r"\bterraform\s+has\s+no\s+command\s+named\b",
        )
    ),
}


ENV_ASSIGNMENT_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*=.*$")


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
    parser.add_argument(
        "--only-cli",
        action="append",
        choices=SUPPORTED_COMMANDS,
        default=[],
        help="Validate only these CLI names (repeatable)",
    )
    parser.add_argument(
        "--exclude-cli",
        action="append",
        choices=SUPPORTED_COMMANDS,
        default=[],
        help="Exclude these CLI names from validation (repeatable)",
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


def is_env_assignment(token: str) -> bool:
    return bool(ENV_ASSIGNMENT_RE.match(token))


def strip_wrappers(tokens: list[str]) -> list[str]:
    index = 0
    while index < len(tokens):
        token = tokens[index]

        if token == "sudo":
            index += 1
            while index < len(tokens) and tokens[index].startswith("-"):
                index += 1
            continue

        if token in ("env", "/usr/bin/env"):
            index += 1
            while index < len(tokens):
                current = tokens[index]
                if current == "--":
                    index += 1
                    break
                if current.startswith("-") or is_env_assignment(current):
                    index += 1
                    continue
                break
            continue

        if token == "command":
            index += 1
            while index < len(tokens) and tokens[index].startswith("-"):
                index += 1
            continue

        if is_env_assignment(token):
            index += 1
            continue

        break

    return tokens[index:]


def iter_logical_command_lines(markdown_text: str):
    current_start_line = 0
    current_parts: list[str] = []

    for line_number, raw_line in iter_fenced_code_lines(markdown_text):
        normalized = raw_line.rstrip()
        normalized = re.sub(r"^\s*[$>]\s*", "", normalized)

        if not normalized.strip():
            if current_parts:
                yield current_start_line, " ".join(current_parts).strip()
                current_parts = []
                current_start_line = 0
            continue

        if not current_parts:
            current_start_line = line_number

        if normalized.endswith("\\"):
            current_parts.append(normalized[:-1].strip())
            continue

        current_parts.append(normalized.strip())
        yield current_start_line, " ".join(current_parts).strip()
        current_parts = []
        current_start_line = 0

    if current_parts:
        yield current_start_line, " ".join(current_parts).strip()


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


def collect_commands(md_file: Path, allowed_clis: set[str]) -> list[CommandOccurrence]:
    text = md_file.read_text(encoding="utf-8")
    occurrences: list[CommandOccurrence] = []

    for line_number, normalized in iter_logical_command_lines(text):
        tokens = tokenize_command(normalized)
        tokens = strip_wrappers(tokens)
        if not tokens or tokens[0] not in allowed_clis:
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
    validator = CLI_VALIDATORS.get(cli_name, DEFAULT_CLI_VALIDATOR)
    command = [cli_name, *path_tokens, validator.help_flag]
    proc = subprocess.run(command, capture_output=True, text=True)
    output = (proc.stdout or "") + ("\n" + proc.stderr if proc.stderr else "")
    out_lower = output.lower()
    invalid_patterns = (*GENERIC_INVALID_PATTERNS, *validator.invalid_patterns)

    if proc.returncode == 0:
        return True, output.strip()

    if any(re.search(pattern, out_lower) for pattern in invalid_patterns):
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
    included_clis = set(args.only_cli) if args.only_cli else set(SUPPORTED_COMMANDS)
    excluded_clis = set(args.exclude_cli)
    effective_clis = sorted(included_clis - excluded_clis)

    try:
        if not docs_root.exists():
            raise RuntimeError(f"Docs root does not exist: {docs_root}")

        if not effective_clis:
            raise RuntimeError("No CLI commands selected for validation")

        # Use PATH resolution to verify presence. Some CLIs (for example, aws/ssh)
        # can return non-zero for "-h" even when they are installed and usable.
        missing_clis = [
            cli_name for cli_name in effective_clis if shutil.which(cli_name) is None
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
            occurrences.extend(collect_commands(md_file, set(effective_clis)))

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
