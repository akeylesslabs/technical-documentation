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
* Follow source priority in this order:

    * Marketing/brand guidelines (if explicitly applicable)
    * Technical documentation style guide
    * Existing local conventions in adjacent files

## Repository conventions for documentation edits

* Keep edits minimal and scoped to the requested task; do not rewrite unaffected sections.
* Preserve front matter and metadata unless the task explicitly requires changes.
* Do not rename, move, or delete files/folders unless explicitly requested.
* Preserve navigation structures and ordering files (for example, `_order.yaml`) when adding or updating pages.
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
* When any Markdown file is edited, run markdownlint CLI against the edited file before finalizing:

    * `npx markdownlint-cli2 --fix --config .github/markdownlint/.markdownlint-cli2.yaml "<edited-file>.md"`
    * Then verify with: `npx markdownlint-cli2 --config .github/markdownlint/.markdownlint-cli2.yaml "<edited-file>.md"`

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
* Markdownlint is run for every edited Markdown file, and reported issues are addressed where feasible.

## AI assistant operating defaults

* When requirements are ambiguous, choose the simplest interpretation that matches the style guide.
* Prefer consistency with existing documentation patterns over introducing new formats.
* When users propose broad conventions (for example, all-file changes or repository-wide automation), suggest updating both this file and `docs/Contributing Guides/technical-documentation-style-guide/index.md` where relevant.
* Flag potential factual uncertainty instead of guessing product behavior.
