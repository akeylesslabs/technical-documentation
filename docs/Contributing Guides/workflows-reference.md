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
| Akeyless Community Repos Update Jira Tasks | `.github/workflows/akeyless-github-action-update-jira.yml` | Weekly schedule (`0 2 * * 1`) and manual dispatch | Checks the latest upstream version signal for every repository in the `akeyless-community` GitHub organization (49 repos) using a matrix strategy with `fail-fast: false`. Detection first queries `releases/latest`; if no GitHub release exists, it falls back to repository tags and prefers the highest semver-like tag (otherwise the most recent tag in the API response). Repos that have neither releases nor tags are skipped gracefully. For each detected tag, it deduplicates against existing DOCS Jira tasks by querying with the repo-specific summary prefix and tag before creating a new task, so reruns never produce duplicate issues. Labels include `documentation`, `akeyless-community`, a repo slug label, and `scheduled`. It does not inspect technical-documentation repository content. |
| Automated Workflow Fixes | `.github/workflows/automated-workflow-fixes.yml` | Weekly schedule (`0 2 * * 1`) and manual dispatch | Coordinator workflow that calls reusable check workflows for link checking, markdown linting, spell checking, and CLI command path checks. It also runs stateful dependency change collection from `.github/dependency-monitor/registry.json`, compares against persisted last-seen versions, emits findings only for detected version deltas, supports manual dispatch controls (`min_severity`, `force_alert_mode`, `categories`, and `stale_suppression_days`), uploads a dedicated dependency metrics artifact, suppresses stale repeat alerts, applies a source health cool down period for repeated fetch failures, suppresses duplicates in Jira with a stable dedupe label, reopens matching closed issues only when transition target status names exactly match configured values, runs JavaScript actions on Node 24, and aggregates all outputs into one summary artifact without exposing Jira issue keys as job outputs. |
| CLI Command Heading Case | `.github/workflows/cli-command-heading-case.yml` | Pull requests that change CLI reference docs, the checker script, or this workflow; manual dispatch | Validates CLI command heading casing in `docs/Integrations & Plugins/cli-reference/**/*.md`. |
| CLI Command Path Check (Manual) | `.github/workflows/cli-command-path-check.yml` | Manual dispatch | Wrapper workflow that invokes the reusable CLI command path check workflow. |
| Dependabot PR Jira Task | `.github/workflows/dependabot-pr-jira.yml` | Pull request target on open events for Dependabot-authored PRs | Creates one DOCS Jira task for each newly opened Dependabot PR using repo secrets available through `pull_request_target`. Searches Jira by PR-specific summary before create so workflow reruns do not create duplicates. Uses `actions/github-script@v9` for changed-file collection. |
| PR Default Assignee | `.github/workflows/pr-default-assignee.yml` | Pull request target on open events | Assigns the pull request creator when a newly opened pull request has no assignee, leaves later manual assignee changes untouched by running only on creation, and logs non-fatal warnings when assignment is blocked by API policy responses. |
| Link Checker (Manual) | `.github/workflows/link-check.yml` | Manual dispatch | Wrapper workflow that invokes the reusable link check workflow. |
| Markdown Linter (Manual) | `.github/workflows/md-linting.yml` | Manual dispatch | Wrapper workflow that invokes the reusable markdown lint workflow. |
| ReadMe Docs Constraints | `.github/workflows/readme-docs-constraints.yml` | Pull requests that change docs Markdown or constraint checker files; manual dispatch | Validates ReadMe compatibility constraints by blocking duplicate Markdown filenames and excessive docs nesting depth in added or renamed docs files. Maintains a sticky PR comment that updates on both failing and passing runs with the latest report state. Uses `actions/github-script@v9` for file collection and PR comment updates. |
| New Page Announcement Subtask | `.github/workflows/new-page-announcement-subtask.yml` | Pull request closed on `v1.0` when merged | Detects newly added Markdown pages under `docs/`, ignores renames, derives the Jira key from branch name, resolves parent task logic for subtasks, and creates a Jira subtask with a pre-drafted Slack announcement. Jira API reads and writes use bounded retries and timeouts to reduce long-running hangs. |
| Security Alert Jira Task | `.github/workflows/security-alert-jira.yml` | Secret scanning alert events (`created`, `reopened`, `publicly_leaked`) | Creates one DOCS Jira task for each secret scanning alert in the repository. Searches Jira by alert-specific summary before create so workflow reruns do not create duplicates. |
| Spell Checker (Manual) | `.github/workflows/spell-check.yml` | Manual dispatch | Wrapper workflow that invokes the reusable spell check workflow. |
| Reusable Link Check | `.github/workflows/reusable-link-check.yml` | Reusable call, pull request, and manual dispatch | Performs doc link replacement, redirect normalization, and Lychee checks; emits reusable outputs and artifacts for coordinator aggregation. |
| Reusable Markdown Lint | `.github/workflows/reusable-markdownlint.yml` | Reusable call, pull request, and manual dispatch | Runs `markdownlint-cli2 --fix`, emits summary outputs, uploads markdownlint artifacts, and forces JavaScript actions to run on Node 24. |
| Reusable Spell Check | `.github/workflows/reusable-spell-check.yml` | Reusable call, pull request, and manual dispatch | Runs CSpell pre/post checks with conservative autofix, emits findings outputs, uploads CSpell artifacts, and forces JavaScript actions to run on Node 24. |
| Reusable CLI Command Path Check | `.github/workflows/reusable-cli-command-path-check.yml` | Reusable call, pull request, and manual dispatch | Validates command paths for `akeyless`, `aws`, `az`, `certbot`, `curl`, `docker`, `eksctl`, `gcloud`, `helm`, `jq`, `kubectl`, `oci`, `openssl`, `ssh`, and `terraform` in docs, installs and verifies CLI availability before validation, runs checks across a dynamic kubectl matrix (current stable minor and two previous minors) with per-minor fallback to Kubernetes GitHub release tags when `dl.k8s.io` stable-minor files are unavailable, skips unreleased minors when neither source can resolve a patch version, aggregates findings into reusable outputs, and uploads CLI path report artifacts. |

## Dependabot

Dependabot is configured in `.github/dependabot.yml` to run weekly on Mondays. It tracks the `github-actions` ecosystem and raises pull requests when `uses:` action references in `.github/workflows/` have newer versions available. This covers action version pins such as `actions/checkout@v4`, `actions/setup-node@v4`, and similar. Newly opened Dependabot PRs are also routed through `.github/workflows/dependabot-pr-jira.yml`, which creates a DOCS Jira task for triage.

## Workflow Ownership and Maintenance

When a workflow is created, renamed, removed, or behavior changes materially, update this page in the same pull request.

A material workflow change includes any update to:

* Trigger conditions (`on`), including branch filters and path filters.
* Checked file scope (for example, `docs/**/*.md` subsets).
* Generated outputs or artifact locations.
* Jira integration behavior, such as issue creation conditions or issue type.
