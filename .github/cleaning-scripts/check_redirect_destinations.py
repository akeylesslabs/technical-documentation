#!/usr/bin/env python3
"""
check_redirect_destinations.py

Validates that redirect DESTINATION URLs (RHS of "A -> B") on docs.akeyless.io
are not dead.

Input format:
    /some/path -> /some/other/path
or (optionally) lines beginning with '#' or blank lines are ignored.

Example:
    /docs/opened -> /docs/openid

Usage:
    python .github/cleaning-scripts/check_redirect_destinations.py .other/redirects-backup.txt
    python .github/cleaning-scripts/check_redirect_destinations.py .other/redirects-backup.txt --base https://docs.akeyless.io --workers 20

Outputs:
    redirect_check_report.csv
    redirect_check_report.json

Exit codes:
    0 = all destinations OK
    1 = some destinations failed
"""

import argparse
import csv
import json
import re
import sys
import time
from dataclasses import asdict, dataclass
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Optional, Tuple

import requests


# -----------------------------
# Data model
# -----------------------------
@dataclass
class RedirectCheckResult:
    source: str
    destination: str
    requested_url: str
    final_url: Optional[str]
    status_code: Optional[int]
    ok: bool
    failure_reason: Optional[str]
    elapsed_ms: int


# -----------------------------
# Parsing
# -----------------------------
REDIRECT_LINE_RE = re.compile(r"^\s*(/[^ ]*)\s*->\s*(/[^ ]*)\s*$")

def parse_redirect_lines(lines: List[str]) -> List[Tuple[str, str]]:
    redirects = []
    for i, line in enumerate(lines, start=1):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        m = REDIRECT_LINE_RE.match(line)
        if not m:
            print(f"[WARN] Skipping invalid line {i}: {line}", file=sys.stderr)
            continue
        redirects.append((m.group(1), m.group(2)))
    return redirects


# -----------------------------
# HTTP check
# -----------------------------
DEFAULT_HEADERS = {
    "User-Agent": "Akeyless-Redirect-Validator/1.0 (+https://docs.akeyless.io)"
}

NOT_FOUND_HINTS = [
    "page not found",
    "not found",
    "404",
    "doesn't exist",
    "does not exist",
    "cannot be found",
]

def looks_like_not_found(html_text: str) -> bool:
    if not html_text:
        return False
    text = html_text.lower()
    return any(hint in text for hint in NOT_FOUND_HINTS)

def normalize_join(base: str, path: str) -> str:
    base = base.rstrip("/")
    path = path.strip()
    if not path.startswith("/"):
        path = "/" + path
    return base + path

def check_destination(
    source: str,
    destination: str,
    base_url: str,
    timeout: float,
    verify_tls: bool,
    detect_soft_404: bool,
    session: requests.Session,
) -> RedirectCheckResult:
    url = normalize_join(base_url, destination)
    start = time.time()

    try:
        resp = session.get(
            url,
            headers=DEFAULT_HEADERS,
            timeout=timeout,
            allow_redirects=True,
            verify=verify_tls,
        )
        elapsed_ms = int((time.time() - start) * 1000)

        final_url = resp.url
        status_code = resp.status_code

        # Hard failures by status code
        if status_code >= 500:
            return RedirectCheckResult(
                source, destination, url, final_url, status_code,
                ok=False,
                failure_reason=f"Server error ({status_code})",
                elapsed_ms=elapsed_ms
            )
        if status_code == 404:
            return RedirectCheckResult(
                source, destination, url, final_url, status_code,
                ok=False,
                failure_reason="404 Not Found",
                elapsed_ms=elapsed_ms
            )
        if status_code >= 400:
            return RedirectCheckResult(
                source, destination, url, final_url, status_code,
                ok=False,
                failure_reason=f"Client error ({status_code})",
                elapsed_ms=elapsed_ms
            )

        # Soft 404 detection (status 200 but content indicates not found)
        if detect_soft_404:
            content_type = (resp.headers.get("Content-Type") or "").lower()
            if "text/html" in content_type:
                if looks_like_not_found(resp.text):
                    return RedirectCheckResult(
                        source, destination, url, final_url, status_code,
                        ok=False,
                        failure_reason="Soft 404 (content suggests not found)",
                        elapsed_ms=elapsed_ms
                    )

        # Looks OK
        return RedirectCheckResult(
            source, destination, url, final_url, status_code,
            ok=True,
            failure_reason=None,
            elapsed_ms=elapsed_ms
        )

    except requests.exceptions.Timeout:
        elapsed_ms = int((time.time() - start) * 1000)
        return RedirectCheckResult(
            source, destination, url, None, None,
            ok=False,
            failure_reason="Timeout",
            elapsed_ms=elapsed_ms
        )
    except requests.exceptions.RequestException as e:
        elapsed_ms = int((time.time() - start) * 1000)
        return RedirectCheckResult(
            source, destination, url, None, None,
            ok=False,
            failure_reason=f"Request error: {e.__class__.__name__}",
            elapsed_ms=elapsed_ms
        )


# -----------------------------
# Main runner
# -----------------------------
def run_checks(
    redirects: List[Tuple[str, str]],
    base_url: str,
    workers: int,
    timeout: float,
    verify_tls: bool,
    detect_soft_404: bool,
) -> List[RedirectCheckResult]:

    results: List[RedirectCheckResult] = []

    # Use a single session per worker to reuse connections
    def worker_task(pair):
        src, dst = pair
        with requests.Session() as session:
            return check_destination(
                source=src,
                destination=dst,
                base_url=base_url,
                timeout=timeout,
                verify_tls=verify_tls,
                detect_soft_404=detect_soft_404,
                session=session
            )

    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = {executor.submit(worker_task, pair): pair for pair in redirects}
        for fut in as_completed(futures):
            res = fut.result()
            results.append(res)

    # keep stable output order matching input
    idx = {pair: i for i, pair in enumerate(redirects)}
    results.sort(key=lambda r: idx.get((r.source, r.destination), 10**9))
    return results


def write_csv(results: List[RedirectCheckResult], out_path: str) -> None:
    fieldnames = list(asdict(results[0]).keys()) if results else [
        "source", "destination", "requested_url", "final_url",
        "status_code", "ok", "failure_reason", "elapsed_ms"
    ]
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for r in results:
            w.writerow(asdict(r))

def write_json(results: List[RedirectCheckResult], out_path: str) -> None:
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump([asdict(r) for r in results], f, indent=2)

def print_summary(results: List[RedirectCheckResult]) -> int:
    total = len(results)
    ok_count = sum(1 for r in results if r.ok)
    fail_count = total - ok_count

    print("\n=== Redirect Destination Validation Summary ===")
    print(f"Total destinations checked: {total}")
    print(f"OK: {ok_count}")
    print(f"FAIL: {fail_count}")

    if fail_count:
        print("\nFailures:")
        for r in results:
            if not r.ok:
                print(f"- {r.destination}  ({r.failure_reason})  [{r.status_code}]  final={r.final_url}")
    return 0 if fail_count == 0 else 1


def main():
    ap = argparse.ArgumentParser(description="Validate redirect destinations are not dead.")
    ap.add_argument("input_file", help="Text file containing lines like '/a -> /b'")
    ap.add_argument("--base", default="https://docs.akeyless.io", help="Base URL (default: https://docs.akeyless.io)")
    ap.add_argument("--workers", type=int, default=20, help="Parallel workers (default: 20)")
    ap.add_argument("--timeout", type=float, default=15.0, help="Request timeout in seconds (default: 15)")
    ap.add_argument("--no-verify-tls", action="store_true", help="Disable TLS certificate verification")
    ap.add_argument("--no-soft-404", action="store_true", help="Disable soft-404 detection for HTML pages")
    ap.add_argument("--csv", default="redirect_check_report.csv", help="CSV output path")
    ap.add_argument("--json", default="redirect_check_report.json", help="JSON output path")

    args = ap.parse_args()

    with open(args.input_file, "r", encoding="utf-8") as f:
        lines = f.readlines()

    redirects = parse_redirect_lines(lines)
    if not redirects:
        print("[ERROR] No valid redirect rules found.", file=sys.stderr)
        sys.exit(2)

    print(f"Loaded {len(redirects)} redirect rules.")
    print(f"Checking destinations at base: {args.base}")
    print(f"Workers: {args.workers}  Timeout: {args.timeout}s  Soft404: {not args.no_soft_404}")

    results = run_checks(
        redirects=redirects,
        base_url=args.base,
        workers=args.workers,
        timeout=args.timeout,
        verify_tls=not args.no_verify_tls,
        detect_soft_404=not args.no_soft_404,
    )

    write_csv(results, args.csv)
    write_json(results, args.json)

    print(f"\nReports written:")
    print(f"- CSV : {args.csv}")
    print(f"- JSON: {args.json}")

    exit_code = print_summary(results)
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
