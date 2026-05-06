#!/usr/bin/env python3
"""Build and post (or update/resolve) the PR comment for cli-stdout-scan results.

Usage:
    python3 cli-stdout-pr-comment.py \\
        --repo <owner/repo> \\
        --pr <number> \\
        --json-results <path>   \\
        --violations-found <N>  \\
        --token <github-token>

The script looks for an existing comment marked with COMMENT_MARKER.  When
violations_found > 0 it posts/updates with the full violation table and
remediation guidance.  When violations_found == 0 it updates any existing
failure comment to a "resolved" notice (and does nothing if none exists).
"""

import argparse
import json
import os
import sys
import urllib.error
import urllib.request

COMMENT_MARKER = "<!-- cli-stdout-scan-comment -->"


def gh_api(method: str, path: str, token: str, body: dict | None = None):
    url = f"https://api.github.com/{path}"
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(
        url,
        data=data,
        method=method,
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            "Content-Type": "application/json",
        },
    )
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as exc:
        body_text = exc.read().decode(errors="replace")
        print(f"GitHub API error {exc.code} {method} {url}: {body_text}", file=sys.stderr)
        raise


def find_existing_comment(repo: str, pr: int, token: str) -> int | None:
    """Return the comment ID of the existing scan comment, or None."""
    page = 1
    while True:
        comments = gh_api(
            "GET",
            f"repos/{repo}/issues/{pr}/comments?per_page=100&page={page}",
            token,
        )
        if not comments:
            return None
        for c in comments:
            if COMMENT_MARKER in c.get("body", ""):
                return c["id"]
        if len(comments) < 100:
            return None
        page += 1


def build_violation_table(violations: list[dict]) -> str:
    rows = []
    for v in violations:
        loc = f"`{v['file']}:{v['line']}`"
        cmd = "`" + v["content"].strip().replace("`", "'") + "`"
        rows.append(f"| {loc} | {cmd} |")
    return "\n".join(rows)


def build_failure_body(violation_count: int, violations: list[dict], repo: str) -> str:
    table = build_violation_table(violations)
    return f"""{COMMENT_MARKER}
## :warning: CLI stdout scan: {violation_count} violation(s) found

One or more CLI commands in this pull request print secret or token material directly to stdout inside a fenced code block. This must be resolved before merging.

### Violations

| Location | Command |
|----------|---------|
{table}

### How to fix

For each flagged command, choose one of the following options:

1. **Capture output in a variable** (preferred for script examples):
   ```bash
   SECRET=$(akeyless get-secret-value --name /path/to/secret)
   ```
2. **Redirect output to a file**:
   ```bash
   akeyless get-secret-value --name /path/to/secret > /tmp/secret.txt
   ```
3. **Use a placeholder comment** to show expected output without running the command:
   ```bash
   akeyless get-secret-value --name /path/to/secret
   # Output: <YOUR_SECRET_VALUE>
   ```
4. **Suppress with an annotation** for intentional illustrative examples — place `<!-- secret-stdout-scan:ok -->` on the line immediately before the fenced code block opening:
   ````markdown
   <!-- secret-stdout-scan:ok -->
   ```shell
   akeyless get-secret-value --name /path/to/secret
   ```
   ````

See [LEAK\_RESPONSE.md — CLI Output Safety](https://github.com/{repo}/blob/v1.0/.github/LEAK_RESPONSE.md#cli-output-safety) for full remediation guidance.
"""


def build_resolved_body() -> str:
    return f"""{COMMENT_MARKER}
## :white_check_mark: CLI stdout scan: all findings resolved

All previously flagged CLI commands that printed secret or token material to stdout have been addressed. No violations remain in this pull request.
"""


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", required=True)
    parser.add_argument("--pr", required=True, type=int)
    parser.add_argument("--json-results", required=True)
    parser.add_argument("--violations-found", required=True, type=int)
    parser.add_argument("--token", default=os.environ.get("GH_TOKEN", ""))
    args = parser.parse_args()

    if not args.token:
        print("Error: GitHub token required via --token or GH_TOKEN env var.", file=sys.stderr)
        return 1

    existing_id = find_existing_comment(args.repo, args.pr, args.token)

    if args.violations_found == 0:
        if existing_id is not None:
            # Update the existing failure comment to show it's resolved.
            gh_api(
                "PATCH",
                f"repos/{args.repo}/issues/comments/{existing_id}",
                args.token,
                {"body": build_resolved_body()},
            )
            print(f"Updated existing comment {existing_id} to resolved state.")
        else:
            print("No violations and no existing comment — nothing to do.")
        return 0

    # Load violations from JSON.
    with open(args.json_results) as f:
        data = json.load(f)

    body = build_failure_body(args.violations_found, data.get("violations", []), args.repo)

    if existing_id is not None:
        gh_api(
            "PATCH",
            f"repos/{args.repo}/issues/comments/{existing_id}",
            args.token,
            {"body": body},
        )
        print(f"Updated existing comment {existing_id}.")
    else:
        result = gh_api(
            "POST",
            f"repos/{args.repo}/issues/{args.pr}/comments",
            args.token,
            {"body": body},
        )
        print(f"Posted new comment {result['id']}.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
