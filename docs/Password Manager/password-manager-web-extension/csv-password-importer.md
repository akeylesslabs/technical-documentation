---
title: CSV Password Importer
---
Bring your credentials across from another password manager or browser.

Open **Settings → Import Passwords**, choose your source, follow the export instructions shown, then upload the resulting CSV.

## Supported sources

| Source | How to export |
|---|---|
| **1Password** | Desktop export instructions at support.1password.com |
| **LastPass** | lastpass.com/vault → advanced options → export → confirm by email → re-enter your password |
| **Bitwarden** | Export instructions at bitwarden.com/help |
| **Dashlane** | Desktop export instructions at support.dashlane.com |
| **Keeper** | Vault export instructions at docs.keeper.io |
| **Google** | passwords.google.com → gear icon → export |
| **Microsoft Edge** | `edge://settings/passwords` → Saved passwords → ⋯ → Export passwords |
| **Apple** | iPhone and Mac instructions at support.apple.com |
| **KeePass** | File → Export → CSV File… (UTF-8 recommended) |
| **Generic CSV** | Any CSV with the columns below |

## Generic CSV format

Columns: `name`, `url`, `username`, `password`, `description` (or `note` / `notes`).

- **Column order can vary** — headers are detected automatically.
- **Delimiters are detected automatically.**
- **UTF-8 is preferred**, and common Western European (Latin) encodings are also accepted.

## KeePass default columns

A default KeePass export produces: `Account`, `Login Name`, `Password`, `Web Site`, `Comments`. These are recognized without renaming.

## After the import

An **import summary** reports how many rows were imported and what was skipped, so you can check nothing was silently dropped.

<Callout icon="⚠️" theme="warn">
  **Delete the exported CSV afterwards.** It holds every password you just imported, in plain text, in your Downloads folder.
</Callout>

## Related

- [Extension Settings](https://docs.akeyless.io/docs/web-extension-settings)
- [Creating New Password](https://docs.akeyless.io/docs/creating-new-password-1)
