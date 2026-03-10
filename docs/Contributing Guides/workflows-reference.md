---
title: GitHub Workflows Reference
excerpt: ''
deprecated: false
hidden: false
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
| Automated Workflow Fixes | `.github/workflows/automated-workflow-fixes.yml` | Weekly schedule (`0 2 * * 1`) and manual dispatch | Runs consolidated weekly automation for link replacement and checking, markdown linting, spelling checks, CLI command path checks, report generation, branch commits, and Jira issue creation. |
| CLI Command Heading Case | `.github/workflows/cli-command-heading-case.yml` | Pull requests that change CLI reference docs, the checker script, or this workflow; manual dispatch | Validates CLI command heading casing in `docs/Integrations & Plugins/cli-reference/**/*.md`. |
| CLI Command Path Check (Manual) | `.github/workflows/cli-command-path-check.yml` | Manual dispatch | Runs CLI command path validation, writes report artifacts under `.github/cli-command-paths/`, commits report updates, and creates Jira issues when failures are found. |
| Link Checker (Manual) | `.github/workflows/link-check.yml` | Manual dispatch | Rewrites `doc:` links to absolute docs URLs, runs Lychee discovery and final link checks, normalizes redirected docs links, commits outputs, and creates Jira issues with attached artifacts. |
| Markdown Linter (Manual) | `.github/workflows/md-linting.yml` | Manual dispatch | Runs `markdownlint-cli2 --fix` for docs Markdown, commits fixes and reports, and creates Jira issues when fixes or remaining violations are detected. |
| New Page Announcement Subtask | `.github/workflows/new-page-announcement-subtask.yml` | Pull request closed on `v1.0` when merged | Detects newly added Markdown pages under `docs/`, ignores renames, derives the Jira key from branch name, resolves parent task logic for subtasks, and creates a Jira subtask with a pre-drafted Slack announcement. |
| Spell Checker (Manual) | `.github/workflows/spell-check.yml` | Manual dispatch | Runs CSpell pre-fix and post-fix checks for Markdown, applies conservative autofix, commits generated outputs, and creates Jira issues with attached reports when findings exist. |

## Workflow Ownership and Maintenance

When a workflow is created, renamed, removed, or behavior changes materially, update this page in the same pull request.

A material workflow change includes any update to:

* Trigger conditions (`on`), including branch filters and path filters.
* Checked file scope (for example, `docs/**/*.md` subsets).
* Generated outputs or artifact locations.
* Jira integration behavior, such as issue creation conditions or issue type.
