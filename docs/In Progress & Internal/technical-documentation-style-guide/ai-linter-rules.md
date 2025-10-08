---
title: AI Linter Rules
deprecated: false
hidden: true
metadata:
  robots: index
---
# Errors

* There must be no technical inaccuracies.
* There must be no conflicts between the information on a page or between pages.
* There must be no errors in CLI commands or sample code.
* There must be no misspellings.
* There must be no custom HTML styling within pages. All styling must come from project-wide CSS. The following elements are excepted:
  * Alignment attributes of images.
  * Border attributes of images.
* There must be no errors in Markdown syntax.
* All file names, CLI commands, configuration keys, and code should be formatted as such with backticks or fenced code blocks.
* There should be no underlined text.
* When referencing non-Akeyless products and features, consistently apply the capitalization and punctuation of the owning organization of the product referenced. Some examples are:
  * GitLab (instead of Gitlab)
  * GitHub (instead of Github)
  * Docker Hub (instead of dockerhub)
  * HashiCorp Vault (instead of Hashi-Vault)
  * SAP HANA database (instead of HANA DB)
  * MySQL (instead of mysql)
  * MSSQL (instead of mssql)
  * Amazon Redshift (instead of Redshift)
  * Amazon EKS (instead of EKS or AWS EKS)
  * `kubectl` (instead of Kubectl)'
* When referring to CLI commands use the proper terminology. Referring to this example: `akeyless target create godaddy -n "name-value" -p "password"`
  * `akeyless` is the command.
  * `target`, `create`, and `godaddy` are subcommands.
  * `-n` and `-p` are flags (also known as options).
  * `"name-value"` and `"password"` are flag values (or option values).
* Provide alt-text for all images.
* There must be no idioms, slang, or cultural references.
* Use commas as separators for large numbers (1,000).

# Warnings

* There should be no inconsistent styling within the same page.
* There should be no grammar issues.
* There should be no incorrect capitalization or styling of Akeyless and external product/feature names.
* There should only be third-person viewpoints. There should be no first-person or second-person language.
* Language should be simple and direct.
* Language should use the active voice.
* Use the same terminology for features, functions, and components throughout.
* Avoid unnecessary words, filler phrases, or redundant explanations.
* Assume readers have basic technical knowledge but may not be experts.
* Keep punctuation simple and avoid chained clauses.
* The tone should be professional, yet approachable. It should also be neutral and instructional.
* Avoid slang, jargon, or overly casual language.
* All language should be inclusive.
* Paragraphs should be short (3-5 sentences).
* Use lists and table to break down complex information.
* When sample code, sample commands, or examples are shown across multiple languages or formats, tabs should be used to prevent multiple fenced code blocks.
* Bold text should be used for UI element, important notes, or emphasis.
* Italics should be used for new terms or lighter emphasis.'
* Capitalize proper nouns and feature names (e.g., Akeyless MCP Server).
* When using abbreviations, unless they are widely known (e.g., "API," "URL"), always define them on first use.
* Always use the product’s official names.
* Wherever possible, examples of codes and command should be used.
* Show expected output whenever possible with sample commands and code.
* Use realistic values wherever possible, not placeholders, unless security-sensitive.
* When formatting inputs and output pairs, precede the input with a ">" and the output following on the next line.
* CLI References should document only one command or subcommand. Each CLI reference page should describe the command (or subcommand), provide a usage example, provide a description of all available flags, and can optionally have an additional notes section. Consequently, CLI Reference pages will feature a large amount of redundancy. To ease authoring, use ReadMe's Reusable Content feature.
* Due to the nature of CLI help pages, their documentation uses many shortened words, abbreviations, and unclear descriptions. These issues should be resolved on a CLI Reference, rather than duplicated.
* Dates should adhere to the YYYY-MM-DD format.
* Times should use the UTC format when relevant.
* Numbers: Use numerals for all numbers over ten (e.g., "12 files," not "twelve files"). Use words for numbers under ten (e.g., "three files," not "3 files").
* Use a space between the value and unit (e.g., "10 GB", "12 ms")
* File paths: Use `/` for paths (e.g., `/usr/local/bin`).
* Data Structures: When representing child elements outside of a full object notation file, use a period to represent child elements in relation to their parents. For example, represent `--access-type` from the below example as `args.--access-type`.
* Use descriptive link text instead of "click here."
* Avoid sentence fragments wherever reasonable.
* If using variables like `{username}` or `{path}`, describe their expected format so translation can adjust grammar as needed.
* Do not overload with unnecessary detail.
* Do not use bolded text, when a heading is appropriate.
