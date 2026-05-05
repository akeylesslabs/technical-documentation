#!/usr/bin/env bash
# cli-stdout-scan.sh — Scans Markdown fenced code blocks for Akeyless CLI
# commands that would print secret or token material to stdout.
#
# Usage:
#   cli-stdout-scan.sh [--files <list-file>] [file ...]
#
#   --files <list-file>
#     Read newline-delimited Markdown file paths from <list-file>.
#     Useful in CI when the path list is produced by a prior step and
#     avoids shell expansion limits on large changesets.
#
#   [file ...]
#     Scan the listed Markdown files directly.
#
#   (no arguments)
#     Scan all docs/**/*.md files under the current directory.
#
# Suppress annotation:
#   Place <!-- secret-stdout-scan:ok --> on the line immediately before a
#   fenced code block opening to exempt the entire block from this check.
#
#   Example:
#     <!-- secret-stdout-scan:ok -->
#     ```shell
#     akeyless get-secret-value --name /my/secret   # intentional raw output example
#     ```
#
# Exit codes:
#   0 — no violations found
#   1 — one or more violations found
#   2 — usage or environment error

set -uo pipefail

# ---------------------------------------------------------------------------
# Require bash 4.0+.
# macOS ships bash 3.2; contributors on macOS should: brew install bash
# ---------------------------------------------------------------------------
if (( BASH_VERSINFO[0] < 4 )); then
  echo "Error: bash 4.0 or later is required (found ${BASH_VERSION})." >&2
  echo "On macOS: brew install bash" >&2
  exit 2
fi

# ---------------------------------------------------------------------------
# Flagged patterns (ERE).  Each pattern matches an Akeyless CLI subcommand
# whose unredirected stdout is secret or token material.
#
# Add new subcommands here as the product surface grows.
# ---------------------------------------------------------------------------
readonly -a FLAGGED_PATTERNS=(
  # Static and dynamic secrets
  'akeyless[[:space:]]+(get-secret-value|get-dynamic-secret-value)([[:space:]]|$)'
  # Authentication — akeyless auth prints the access token as plaintext to stdout
  # Note: akeyless configure is intentionally excluded; it writes config to disk
  # and does not echo secret material to stdout.
  'akeyless[[:space:]]+auth([[:space:]]|$)'
  # PKI / SSH credentials
  'akeyless[[:space:]]+get-ssh-certificate([[:space:]]|$)'
)

# ERE that identifies output-safe invocations and suppresses the violation:
#   (a) Output captured in a shell variable:   VAR=$(akeyless ...) or export VAR=$(...)
#       Also handles YAML list-item and key-value prefixes, e.g.:
#         - export VAR=$(...)          (YAML sequence item)
#         command: export VAR=$(...)   (YAML mapping value)
#   (b) Output redirected to a file:           akeyless ... > /tmp/out  or  >> file
#       Note: >&2 (stderr-only redirect) is intentionally NOT treated as safe.
readonly SAFE_OUTPUT_PATTERN='^[[:space:]]*(-[[:space:]]+|[A-Za-z_][A-Za-z_0-9]*:[[:space:]]*)?(export[[:space:]]+)?[A-Za-z_][A-Za-z_0-9]*=[[:space:]]*\$\(|>[[:space:]]*[^&[:space:]][^[:space:]]*'
readonly SUPPRESS_MARKER='<!-- secret-stdout-scan:ok -->'

# ERE for a CommonMark fenced code block opening:
#   0–3 spaces of indentation + 3+ backticks OR 3+ tildes
readonly OPEN_FENCE_RE='^[[:space:]]{0,3}(`{3,}|~{3,})'

# ---------------------------------------------------------------------------
# Argument parsing
# ---------------------------------------------------------------------------
FILES_FROM=""
if [[ "${1:-}" == "--files" ]]; then
  if [[ -z "${2:-}" ]]; then
    echo "Error: --files requires a path argument." >&2
    exit 2
  fi
  FILES_FROM="$2"
  shift 2
fi

declare -a FILES=()
if [[ -n "$FILES_FROM" ]]; then
  [[ -f "$FILES_FROM" ]] || { echo "Error: --files path not found: ${FILES_FROM}" >&2; exit 2; }
  mapfile -t FILES < "$FILES_FROM"
elif [[ "$#" -gt 0 ]]; then
  FILES=("$@")
else
  mapfile -t FILES < <(find docs -name "*.md" -type f | sort)
fi

# ---------------------------------------------------------------------------
# Per-violation data stored in parallel arrays — avoids parsing ambiguity
# when violation content lines contain colons (common with CLI flags/paths).
# ---------------------------------------------------------------------------
declare -a VIO_FILE=()
declare -a VIO_LINE=()
declare -a VIO_CONTENT=()
VIOLATION_COUNT=0

# ---------------------------------------------------------------------------
# Scan each file
# ---------------------------------------------------------------------------
for file in "${FILES[@]}"; do
  [[ -f "$file" ]] || continue

  in_block=false
  suppress_block=false
  fence_char=""
  fence_len=0
  close_re=""
  lineno=0
  prev_content_line=""

  while IFS= read -r line || [[ -n "$line" ]]; do
    lineno=$((lineno + 1))

    if ! $in_block; then
      # ---- Detect fenced code block opening (CommonMark §4.5) ----
      if [[ "$line" =~ $OPEN_FENCE_RE ]]; then
        opening="${BASH_REMATCH[1]}"
        fence_char="${opening:0:1}"
        fence_len="${#opening}"
        # Build the closing-fence regex once per block instead of per line.
        # Same fence character, at least as many characters, trailing spaces only.
        close_re="^[[:space:]]{0,3}([${fence_char}]{${fence_len},})[[:space:]]*$"
        in_block=true
        suppress_block=false
        if [[ "$prev_content_line" == *"$SUPPRESS_MARKER"* ]]; then
          suppress_block=true
        fi
        prev_content_line="$line"
        continue
      fi

      # Track the previous non-blank line for suppress-annotation detection
      if [[ -n "${line// }" ]]; then
        prev_content_line="$line"
      fi

    else
      # ---- Detect closing fence (CommonMark §4.5) ----
      # The regex enforces: same fence character, >= opening length, nothing
      # else on the line.  This correctly rejects longer opening fences (which
      # the old remainder-based check could mishandle).
      if [[ "$line" =~ $close_re ]]; then
        in_block=false
        suppress_block=false
        fence_char=""
        fence_len=0
        close_re=""
        prev_content_line="$line"
        continue
      fi

      # ---- Check for dangerous patterns (unless suppressed) ----
      if ! $suppress_block; then
        # Skip shell/script comment lines — they document usage but never execute it.
        trimmed="${line#"${line%%[! ]*}"}"
        if [[ "$trimmed" == \#* ]]; then
          prev_content_line="$line"
          continue
        fi
        for pattern in "${FLAGGED_PATTERNS[@]}"; do
          # Use bash built-in ERE ([[ =~ ]]) instead of spawning grep per line.
          if [[ "$line" =~ $pattern ]]; then
            # Skip safe invocations: variable capture or file redirect.
            if [[ "$line" =~ $SAFE_OUTPUT_PATTERN ]]; then
              continue
            fi
            VIO_FILE+=("$file")
            VIO_LINE+=("$lineno")
            VIO_CONTENT+=("$line")
            VIOLATION_COUNT=$((VIOLATION_COUNT + 1))
            break  # one violation reported per line is sufficient
          fi
        done
      fi
    fi

  done < "$file"
done

# ---------------------------------------------------------------------------
# Report results
# ---------------------------------------------------------------------------
if [[ "$VIOLATION_COUNT" -gt 0 ]]; then
  echo "CLI stdout scan found ${VIOLATION_COUNT} violation(s) — commands that print secret material to stdout:"
  echo ""
  for (( i = 0; i < VIOLATION_COUNT; i++ )); do
    vf="${VIO_FILE[$i]}"
    vl="${VIO_LINE[$i]}"
    vc="${VIO_CONTENT[$i]}"
    echo "  ${vf}:${vl}: ${vc}"
    # Emit GitHub Actions workflow annotations only when running in CI.
    # Suppressed locally to avoid noisy ::error:: strings in terminal output.
    if [[ -n "${GITHUB_ACTIONS:-}" ]]; then
      echo "::error file=${vf},line=${vl}::CLI command prints secret or token material to stdout. Capture output in a variable, redirect to a file, use a placeholder, or suppress with <!-- secret-stdout-scan:ok --> before the code block. See .github/LEAK_RESPONSE.md for remediation."
    fi
  done
  echo ""
  echo "See .github/LEAK_RESPONSE.md (CLI Output Safety section) for remediation steps."
  exit 1
else
  echo "CLI stdout scan: 0 violations found."
  exit 0
fi
