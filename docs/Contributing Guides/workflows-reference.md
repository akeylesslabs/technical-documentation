---
title: GitHub Workflows Reference
excerpt: ''
deprecated: false
hidden: true
metadata:
  title: ''
  description: ''
  robots: index
---
## Purpose

This page documents all current GitHub Actions workflows in this repository and the intent of each workflow.

## Current Workflows

| Workflow | File | Trigger | Primary Purpose |
| --- | --- | --- | --- |
| Automated Workflow Fixes | `.github/workflows/automated-workflow-fixes.yml` | Weekly schedule (`0 2 * * 1`) and manual dispatch | Coordinator workflow that calls reusable check workflows for link checking, markdown linting, spell checking, CLI command path checks, and ReadMe docs constraints (duplicate filenames, nesting depth, front matter, and navigation integrity). It also runs the secret-scan job to detect credential leaks, integrating scan summary, leak count, and rule type breakdown into aggregated report and Jira issue descriptions for detailed leak categorization. Jira task descriptions include the automation branch names and commit links when available, and now embed full findings directly from link-check, markdownlint, cspell, CLI command path, ReadMe constraints, and dependency-monitor report artifacts so triage can happen without opening workflow artifacts first. Additionally runs stateful dependency change collection from `.github/dependency-monitor/registry.json`, compares against persisted last-seen versions, emits findings only for detected version deltas, supports manual dispatch controls (`min_severity`, `force_alert_mode`, `categories`, and `stale_suppression_days`), uploads a dedicated dependency metrics artifact, suppresses stale repeat alerts, applies a source health cool down period for repeated fetch failures, suppresses duplicates in Jira with a stable dedupe label, reopens matching closed issues only when transition target status names exactly match configured values, runs JavaScript actions on Node 24, and aggregates all outputs into one summary artifact without exposing Jira issue keys as job outputs. The `notify-on-failure` job runs only on `schedule` triggers when the `aggregate-and-jira` job has failed; it creates a DOCS Jira task (labels: `automation`, `workflow-failure`, `scheduled`) with the workflow name, branch, run ID, and a direct link to the failed run, using `continue-on-error` so a Jira API error does not mask the original failure. Required secrets: `DOCS_JIRA_BASE_URL`, `DOCS_JIRA_EMAIL`, `DOCS_JIRA_API_TOKEN`, `DOCS_JIRA_PROJECT_KEY`. |
| CLI Command Heading Case | `.github/workflows/cli-command-heading-case.yml` | Pull requests that change CLI reference docs, the checker script, or this workflow; manual dispatch | Validates CLI command heading casing in `docs/Integrations & Plugins/cli-reference/**/*.md`. |
| CLI Command Path Check (Manual) | `.github/workflows/cli-command-path-check.yml` | Manual dispatch | Wrapper workflow that invokes the reusable CLI command path check workflow. |
| PR Default Assignee | `.github/workflows/pr-default-assignee.yml` | Pull request target on open events | Assigns the pull request creator when a newly opened pull request has no assignee, leaves later manual assignee changes untouched by running only on creation, and logs non-fatal warnings when assignment is blocked by API policy responses. |
| Link Checker (Manual) | `.github/workflows/link-check.yml` | Manual dispatch | Wrapper workflow that invokes the reusable link check workflow. |
| Markdown Linter (Manual) | `.github/workflows/md-linting.yml` | Manual dispatch | Wrapper workflow that invokes the reusable markdown lint workflow. |
| ReadMe Docs Constraints | `.github/workflows/readme-docs-constraints.yml` | Pull requests that change content under `docs/`, `reference/`, or `recipes/`, or change the constraint checker/workflow files; manual dispatch; reusable call (weekly coordinator) | Validates ReadMe compatibility constraints by blocking duplicate Markdown filenames and excessive docs nesting depth in added or renamed docs files, requiring baseline front matter schema keys, validating impacted `_order.yaml` navigation integrity (required entries and entry targets), disallowing index page entries in `_order.yaml`, enforcing lowercase/no-whitespace naming for nested docs subdirectories below `docs/<first-level>/`, and enforcing that every directory under `docs/`, `reference/`, and `recipes/` contains `_order.yaml`. Maintains a sticky PR comment only when violations are present, includes a plain-English summary of what failed and which file is affected, and deletes the comment automatically when a later commit resolves all issues. Uses `actions/github-script@v9` for file collection and PR comment updates. Exposes `constraints_summary`, `violations_total`, and `failed` outputs for aggregation by the weekly automated workflow coordinator. |
| New Page Announcement Subtask | `.github/workflows/new-page-announcement-subtask.yml` | Pull request closed on `v1.0` when merged | Detects newly added Markdown pages under `docs/`, ignores renames, derives the Jira key from branch name, resolves parent task logic for subtasks, and creates a Jira subtask with a pre-drafted Slack announcement. Jira API reads and writes use bounded retries and timeouts to reduce long-running hangs. |
| Security Alert Jira Task | `.github/workflows/security-alert-jira.yml` | Repository dispatch (`secret_scanning_alert`) and manual dispatch | Creates one DOCS Jira task for each secret scanning alert payload relayed to the repository, with manual dispatch available for validation. Searches Jira by alert-specific summary before create so workflow reruns do not create duplicates. |
| Secret Scan | `.github/workflows/secret-scan.yml` | Pull requests, push to `v1.0`, and manual dispatch | Runs two complementary secret-scanning jobs. **Gitleaks** scans the diff-scoped commit range for committed credentials and sensitive tokens using Gitleaks v8.24.2; emits job outputs: `scan_summary`, `leaks_found`, and `rule_breakdown` (leak categorization by RuleID, for example "generic-api-key: 3, jwt: 2") for integration with automated workflow coordinator reports and Jira issue creation. **CLI Stdout Scan** (`.github/scripts/cli-stdout-scan.sh`) scans changed docs Markdown files for Akeyless CLI commands (`get-secret-value`, `get-dynamic-secret-value`, `auth`, `get-ssh-certificate`) that would print secret or token material to stdout when executed; emits `violations_found` and `scan_summary`; supports per-block suppression via `<!-- secret-stdout-scan:ok -->` annotation; on pull requests, automatically posts (or updates) a comment via `.github/scripts/cli-stdout-pr-comment.py` listing each violation with remediation guidance, and updates the comment to a resolved notice once all violations are fixed. Both jobs must pass for a PR to be mergeable. |
| Spell Checker (Manual) | `.github/workflows/spell-check.yml` | Manual dispatch | Wrapper workflow that invokes the reusable spell check workflow. |
| Reusable Link Check | `.github/workflows/reusable-link-check.yml` | Reusable call and manual dispatch | Performs doc link replacement, enforces absolute `https://docs.akeyless.io/docs/...` link policy for docs links, normalizes redirects, and runs Lychee checks; emits reusable outputs and artifacts for coordinator aggregation. |
| Reusable Markdown Lint | `.github/workflows/reusable-markdownlint.yml` | Reusable call, pull request, and manual dispatch | Runs `markdownlint-cli2 --fix`, emits summary outputs, uploads markdownlint artifacts, and forces JavaScript actions to run on Node 24. |
| Reusable Spell Check | `.github/workflows/reusable-spell-check.yml` | Reusable call, pull request, and manual dispatch | Runs CSpell pre/post checks with conservative autofix, emits findings outputs, uploads CSpell artifacts, and forces JavaScript actions to run on Node 24. |
| Reusable CLI Command Path Check | `.github/workflows/reusable-cli-command-path-check.yml` | Reusable call, pull request, and manual dispatch | Validates command paths for `akeyless`, `aws`, `az`, `certbot`, `curl`, `docker`, `eksctl`, `gcloud`, `helm`, `jq`, `kubectl`, `oci`, `openssl`, `ssh`, and `terraform` in docs. Uses two parallel job tracks: a single `cli-path-check-non-kubectl` job that installs and validates all non-kubectl CLIs, and a concise `cli-path-check-kubectl` matrix job that installs only kubectl and validates kubectl-specific paths across the current stable minor and two previous minors. Helm is installed from the latest upstream release after validating a non-empty release tag, and the downloaded Helm archive is checksum-verified using the original upstream archive filename before extraction so command path validation tracks current Helm major and minor changes safely. Per-minor fallback to Kubernetes GitHub release tags applies when `dl.k8s.io` stable-minor files are unavailable. Guards against non-array GitHub API responses (such as rate-limit errors) in the fallback path, skips unreleased minors when neither source can resolve a patch version, aggregates findings from all tracks into reusable outputs, and uploads CLI path report artifacts. The validator script supports `--only-cli` and `--exclude-cli` flags to scope validation to specific CLI names. |

## Dependabot

Dependabot is configured in `.github/dependabot.yml` to run weekly on Mondays. It tracks the `github-actions` ecosystem and raises pull requests when `uses:` action references in `.github/workflows/` have newer versions available. This covers action version pins such as `actions/checkout@v4`, `actions/setup-node@v4`, and similar.

## CodeRabbit

CodeRabbit review execution is inherited from the organization-level GitHub App installation and does not require a repository-local GitHub Actions workflow in this repository.

Repository-level behavior is configured with `.coderabbit.yaml` at the repository root. Use this file to tune review scope and defaults for documentation-heavy pull requests.

## Workflow Ownership and Maintenance

When a workflow is created, renamed, removed, or behavior changes materially, update this page in the same pull request.

A material workflow change includes any update to:

* Trigger conditions (`on`), including branch filters and path filters.
* Checked file scope (for example, `docs/**/*.md` subsets).
* Generated outputs or artifact locations.
* Jira integration behavior, such as issue creation conditions or issue type.
