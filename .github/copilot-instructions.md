---
title: Copilot Instructions for technical-documentation
---

## Copilot Instructions for `technical-documentation`

Use this style guide as permanent context for all documentation work in this repository:

* `docs/Contributing Guides/technical-documentation-style-guide/index.md`

## Required behavior

* Always follow the conventions in the style guide when creating or editing documentation.
* If there is a conflict between other patterns and the style guide, prefer the style guide.
* Keep terminology, tone, structure, and formatting aligned with the style guide.
* For ambiguous writing decisions, choose the option most consistent with the style guide.

## Priority and scope

* Apply these instructions to all content under `docs/`, `reference/`, `recipes/`, and reusable content under `custom_blocks/`.
* Limit all modifications to this repository (`technical-documentation`) only.
* Do not create, edit, rename, move, or delete files in any sibling repository in the workspace.
* Follow source priority in this order:

    * Marketing/brand guidelines (if explicitly applicable)
    * Technical documentation style guide
    * Existing local conventions in adjacent files

## Repository conventions for documentation edits

* Keep edits minimal and scoped to the requested task; do not rewrite unaffected sections.
* When creating a branch for this repository, always use a branch name prefixed with `v1.0_`.
* Never merge a pull request without the user's explicit approval.
* Preserve front matter and metadata unless the task explicitly requires changes.
* **Sensitive examples and placeholders**: All credential-like values (API keys, passwords, tokens, cloud account IDs) in documentation examples **must use semantic placeholders**. See the style guide's "Sensitive Examples and Placeholders" section for conventions and examples. Never commit real or real-looking credentials, and verify with `pre-commit run gitleaks` before pushing.
* For ReadMe.com pages, ensure front matter is present and complete. Use this baseline unless a nearby file requires an exception:

    ```yaml
    ---
    title: <Page Title>
    excerpt: ''
    deprecated: false
    hidden: false
    metadata:
        title: ''
        description: ''
        robots: index
    ---
    ```

    * Keep existing keys and ordering consistent with adjacent files.
    * If `next:` is already used in nearby pages, preserve that structure as-is.
* Do not rename, move, or delete files/folders unless explicitly requested.
* Never rename Markdown files without explicit user permission. Filename changes usually require redirect updates, and redirects must be planned and validated as part of the same change.
* Preserve navigation structures and ordering files (for example, `_order.yaml`) when adding or updating pages.
* `_order.yaml` controls the visible navigation order for pages and folders in its directory. When adding, removing, or renaming pages, update the corresponding `_order.yaml` entry set to keep navigation deterministic and complete.
* When any file under `.github/workflows/` is added, removed, renamed, or materially changed, update `docs/Contributing Guides/workflows-reference.md` in the same change to keep the workflow inventory accurate.
* Use descriptive headings and maintain proper heading hierarchy (`##`, `###`, and deeper levels).
* Use absolute URLs for documentation links; do not use relative links.

    * Example: use `https://docs.akeyless.io/docs/mcp-server` instead of `/docs/mcp-server`.
* Favor ReadMe.com code tabbing for equivalent examples across languages/platforms.

    * Keep adjacent fenced code blocks contiguous (no blank line between them), for example:

      ```shell
      Code 1.
      ```
      ```shell
      Code 2.
      ```
* Run validation only against edited Markdown pages, not the full repository, unless explicitly requested.
* Default to pre-commit validation for edited files:

    * `pre-commit run --files "<edited-file>.md"`
    * Use `pre-commit run --all-files` only when full-repository validation is explicitly requested.
* For local validation in VS Code, use workspace tasks in `.vscode/tasks.json` as the default path instead of running validator commands/scripts directly:

    * `Docs: Validate Edited File (full)` to run markdownlint (`--fix` and verify), cspell, and lychee for one file.
    * `Docs: Link Check (token-aware)` or `Docs: Link Check (token-aware, file)` for token-aware lychee checks that reduce GitHub rate-limit noise.
* Use direct CLI commands only as a fallback when pre-commit or tasks cannot be run. When needed, run markdownlint against each edited file before finalizing:

    * `npx markdownlint-cli2 --fix --config .github/markdownlint/.markdownlint-cli2.yaml "<edited-file>.md"`
    * Then verify with: `npx markdownlint-cli2 --config .github/markdownlint/.markdownlint-cli2.yaml "<edited-file>.md"`
* Run cspell only on edited Markdown files before finalizing:

    * `npx cspell --config cspell.config.yaml --no-progress "<edited-file>.md"`
* Run link checking only on edited Markdown files before finalizing. Use lychee arguments aligned with repository workflow settings:

    * `lychee --verbose --no-progress --exclude-file ".github/lychee/.lycheeignore" --exclude-path ".github" --exclude-link-local --exclude-loopback --include-mail "<edited-file>.md"`
    * Exception: if the edited Markdown file is under `.github/`, omit `--exclude-path ".github"` for that invocation so the edited file is included in the check.

## Akeyless terminology guardrails

* Refer to Akeyless as an "identity security platform" unless the source context explicitly requires older wording.
* Use official product and feature names exactly, with consistent capitalization.
* Define non-obvious acronyms on first use.

## Content quality checklist

Before finalizing documentation changes, ensure:

* Language is clear, concise, active-voice, and neutral in tone.
* Terminology is consistent with the style guide and nearby docs.
* Examples and commands are realistic and internally consistent.
* Links, paths, commands, and code fences are correctly formatted.
* Accessibility and localization basics are respected (descriptive links, simple sentence structure, no idioms).
* Markdownlint, cspell, and link checks are run for every edited Markdown file, and reported issues are addressed where feasible.

## AI assistant operating defaults

* When requirements are ambiguous, choose the simplest interpretation that matches the style guide.
* Prefer consistency with existing documentation patterns over introducing new formats.
* When users propose broad conventions (for example, all-file changes or repository-wide automation), suggest updating both this file and `docs/Contributing Guides/technical-documentation-style-guide/index.md` where relevant.
* Flag potential factual uncertainty instead of guessing product behavior.

## Local Personal Overlay

Personal prompt packs and user-specific workflows should be stored in a local-only file:

* `.github/copilot-instructions.local.md`

Keep this file untracked for personal use. Do not commit personal workflow content to this repository's tracked instructions.
