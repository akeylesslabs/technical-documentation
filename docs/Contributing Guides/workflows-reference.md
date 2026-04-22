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
| Automated Workflow Fixes | `.github/workflows/automated-workflow-fixes.yml` | Weekly schedule (`0 2 * * 1`) and manual dispatch | Runs consolidated weekly automation for link replacement and checking, markdown linting, spelling checks, CLI command path checks, report generation, branch commits, and Jira issue creation. Captures CLI validator fallback output when JSON is missing and uses bounded retries/timeouts for Jira API writes and attachment uploads to reduce long-running hangs. |
| CLI Command Heading Case | `.github/workflows/cli-command-heading-case.yml` | Pull requests that change CLI reference docs, the checker script, or this workflow; manual dispatch | Validates CLI command heading casing in `docs/Integrations & Plugins/cli-reference/**/*.md`. |
| CLI Command Path Check (Manual) | `.github/workflows/cli-command-path-check.yml` | Manual dispatch | Runs CLI command path validation, writes report artifacts under `.github/cli-command-paths/`, commits report updates, and creates Jira issues when failures are found. Jira API writes and attachment uploads use bounded retries and timeouts to reduce long-running hangs. |
| Dependabot PR Jira Task | `.github/workflows/dependabot-pr-jira.yml` | Pull request target on open events for Dependabot-authored PRs | Creates one DOCS Jira task for each newly opened Dependabot PR using repo secrets available through `pull_request_target`. Searches Jira by PR-specific summary before create so workflow reruns do not create duplicates. Uses `actions/github-script@v9` for changed-file collection. |
| PR Default Assignee | `.github/workflows/pr-default-assignee.yml` | Pull request target on open events | Assigns the pull request creator when a newly opened pull request has no assignee, leaves later manual assignee changes untouched by running only on creation, and logs non-fatal warnings when assignment is blocked by API policy responses. |
| Link Checker (Manual) | `.github/workflows/link-check.yml` | Manual dispatch | Rewrites `doc:` links to absolute docs URLs, runs Lychee discovery and final link checks, normalizes redirected docs links, commits outputs, and creates Jira issues with attached artifacts. Jira API writes and attachment uploads use bounded retries and timeouts to reduce long-running hangs. |
| Markdown Linter (Manual) | `.github/workflows/md-linting.yml` | Manual dispatch | Runs `markdownlint-cli2 --fix` for docs Markdown, commits fixes and reports, and creates Jira issues when fixes or remaining violations are detected. Jira API writes and attachment uploads use bounded retries and timeouts to reduce long-running hangs. |
| ReadMe Docs Constraints | `.github/workflows/readme-docs-constraints.yml` | Pull requests that change docs Markdown or constraint checker files; manual dispatch | Validates ReadMe compatibility constraints by blocking duplicate Markdown filenames and excessive docs nesting depth in added or renamed docs files. Maintains a sticky PR comment that updates on both failing and passing runs with the latest report state. Uses `actions/github-script@v9` for file collection and PR comment updates. |
| New Page Announcement Subtask | `.github/workflows/new-page-announcement-subtask.yml` | Pull request closed on `v1.0` when merged | Detects newly added Markdown pages under `docs/`, ignores renames, derives the Jira key from branch name, resolves parent task logic for subtasks, and creates a Jira subtask with a pre-drafted Slack announcement. Jira API reads and writes use bounded retries and timeouts to reduce long-running hangs. |
| Spell Checker (Manual) | `.github/workflows/spell-check.yml` | Manual dispatch | Runs CSpell pre-fix and post-fix checks for Markdown, applies conservative autofix, commits generated outputs, and creates Jira issues with attached reports when findings exist. Jira API writes and attachment uploads use bounded retries and timeouts to reduce long-running hangs. |

## Dependabot

Dependabot is configured in `.github/dependabot.yml` to run weekly on Mondays. It tracks the `github-actions` ecosystem and raises pull requests when `uses:` action references in `.github/workflows/` have newer versions available. This covers action version pins such as `actions/checkout@v4`, `actions/setup-node@v4`, and similar. Newly opened Dependabot PRs are also routed through `.github/workflows/dependabot-pr-jira.yml`, which creates a DOCS Jira task for triage.

## Workflow Ownership and Maintenance

When a workflow is created, renamed, removed, or behavior changes materially, update this page in the same pull request.

A material workflow change includes any update to:

* Trigger conditions (`on`), including branch filters and path filters.
* Checked file scope (for example, `docs/**/*.md` subsets).
* Generated outputs or artifact locations.
* Jira integration behavior, such as issue creation conditions or issue type.
