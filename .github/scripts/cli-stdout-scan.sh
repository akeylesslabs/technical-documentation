#!/usr/bin/env bash
# cli-stdout-scan.sh — Scans Markdown fenced code blocks for Akeyless CLI
# commands that would print secret or token material to stdout.
#
# Usage:
#   cli-stdout-scan.sh [file ...]
#     Scan the listed Markdown files.
#
#   cli-stdout-scan.sh
#     Scan all docs/**/*.md files.
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

set -uo pipefail

# ---------------------------------------------------------------------------
# Patterns (ERE) that match Akeyless CLI commands whose unredirected output
# is secret or token material.
# ---------------------------------------------------------------------------
PATTERNS=(
  'akeyless[[:space:]]+(get-secret-value|get-dynamic-secret-value)([[:space:]]|$)'
)

SUPPRESS_MARKER='<!-- secret-stdout-scan:ok -->'
VIOLATION_COUNT=0
declare -a VIOLATIONS=()

# ---------------------------------------------------------------------------
# Resolve the list of files to scan
# ---------------------------------------------------------------------------
if [ "$#" -gt 0 ]; then
  FILES=("$@")
else
  mapfile -t FILES < <(find docs -name "*.md" -type f | sort)
fi

# ---------------------------------------------------------------------------
# Scan each file
# ---------------------------------------------------------------------------
for file in "${FILES[@]}"; do
  [[ -f "$file" ]] || continue

  in_block=false
  suppress_block=false
  fence=""
  lineno=0
  prev_content_line=""

  while IFS= read -r line || [[ -n "$line" ]]; do
    ((lineno++))

    if ! $in_block; then
      # Detect fenced code block opening (``` or ~~~, optionally with language tag)
      if [[ "$line" =~ ^([[:space:]]*)(\`\`\`+|~~~+) ]]; then
        fence="${BASH_REMATCH[2]}"
        in_block=true
        # Suppress if the immediately preceding non-blank content line was a marker
        if [[ "$prev_content_line" == *"$SUPPRESS_MARKER"* ]]; then
          suppress_block=true
        else
          suppress_block=false
        fi
        continue
      fi

      # Track the previous non-blank line for suppress detection
      if [[ -n "${line// }" ]]; then
        prev_content_line="$line"
      fi

    else
      # Detect closing fence: same or longer fence sequence at start of line
      if [[ "$line" =~ ^[[:space:]]*${fence} ]]; then
        # Make sure it is actually closing (not a longer opening inside)
        remainder="${line#*${fence}}"
        if [[ ! "$remainder" =~ [^[:space:]] ]] || [[ "$remainder" =~ ^[[:space:]]*$ ]]; then
          in_block=false
          suppress_block=false
          fence=""
          continue
        fi
      fi

      # Inside a code block: check for dangerous patterns (unless suppressed)
      if ! $suppress_block; then
        for pattern in "${PATTERNS[@]}"; do
          if echo "$line" | grep -qE "$pattern"; then
            # Allow if the command output is captured into a shell variable:
            #   VAR=$(akeyless ...) or export VAR=$(akeyless ...)
            if echo "$line" | grep -qE '(^\s*(export\s+)?[A-Za-z_][A-Za-z_0-9]*=\$\()'; then
              continue
            fi
            VIOLATIONS+=("${file}:${lineno}:${line}")
            ((VIOLATION_COUNT++)) || true
          fi
        done
      fi
    fi

  done < "$file"
done

# ---------------------------------------------------------------------------
# Report results
# ---------------------------------------------------------------------------
if [ "${VIOLATION_COUNT}" -gt 0 ]; then
  echo "CLI stdout scan found ${VIOLATION_COUNT} violation(s) — commands that print secret material to stdout:"
  echo ""
  for v in "${VIOLATIONS[@]}"; do
    # Parse file:line:content (content may itself contain colons)
    file_part="${v%%:*}"
    rest="${v#*:}"
    line_num="${rest%%:*}"
    matched="${rest#*:}"
    echo "  ${file_part}:${line_num}: ${matched}"
    echo "::error file=${file_part},line=${line_num}::CLI command prints secret or token material to stdout. Redirect output, capture in a variable, use a placeholder, or suppress with <!-- secret-stdout-scan:ok --> before the code block."
  done
  echo ""
  echo "See .github/LEAK_RESPONSE.md for remediation steps (CLI Output Safety section)."
  exit 1
else
  echo "CLI stdout scan: 0 violations found."
  exit 0
fi
