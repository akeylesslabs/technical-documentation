---
title: Importing from Another Password Manager
---
Bring your credentials across from another password manager or browser. Ten sources are
supported, each with its own export instructions built into the extension.

Open **Settings → Import Passwords**.

![The import source list](https://files.readme.io/d722ecea95425835e705b6cd8bd779868409dd1fe7028013c8b21d4ae788b481-import-vendor-list.png)
*Choose the password manager you are moving from*

Select a source to see its step-by-step export guide, then upload the CSV it produces.

---

## Supported sources

| Source | How to export |
|---|---|
| **1Password** | Desktop app export; instructions at [1Password Support](https://support.1password.com) |
| **LastPass** | [the LastPass vault](https://lastpass.com/vault) → advanced options → **Export** → confirm by email → re-enter your password |
| **Bitwarden** | Vault → Tools → Export vault; instructions at [Bitwarden Help](https://bitwarden.com/help) |
| **Dashlane** | Desktop app → My Account → Export data; instructions at [Dashlane Support](https://support.dashlane.com) |
| **Keeper** | Vault → Export; instructions at [Keeper Documentation](https://docs.keeper.io) |
| **Google** | `passwords.google.com` → gear icon → **Export** |
| **Microsoft Edge** | `edge://settings/passwords` → Saved passwords → **⋯** → Export passwords |
| **Apple** | iPhone and Mac instructions at [Apple Support](https://support.apple.com) |
| **KeePass** | File → Export → CSV File… (UTF-8 recommended) |
| **Generic CSV** | Any CSV with the columns below |

---

## Generic CSV format

Columns: `name`, `url`, `username`, `password`, `description` (also accepted as `note` or `notes`).

| Behavior | Detail |
|---|---|
| **Column order** | Any — headers are detected automatically |
| **Delimiter** | Detected automatically (comma, semicolon, tab) |
| **Encoding** | UTF-8 preferred; common Western European (Latin) encodings also decode |
| **Extra columns** | Ignored rather than rejected |

### KeePass default columns

A default KeePass export produces `Account`, `Login Name`, `Password`, `Web Site`, `Comments`.
These are recognized without renaming anything.

---

## What happens on import

Each row becomes a **password item**:

| CSV column | Becomes |
|---|---|
| `name` | The item name |
| `username` | The username |
| `password` | The password |
| `url` | A website URL, which drives autofill matching and Launch |
| `description` / `note` | The item description |

Imported items land in the area and folder you choose during the import.

## The import summary

When the upload finishes, a summary reports how many rows were imported and how many were
skipped, so no row is dropped without a record.

Rows are usually skipped because they are missing a required field, or because the file could
not be decoded — see below.

---

## Afterwards

<Callout icon="⚠️" theme="warn">
  **Delete the exported CSV.** It contains every password you just imported, in plain text,
  sitting in your `Downloads` folder. Empty your trash too.
</Callout>

Then:

1. Open [Security Health](https://docs.akeyless.io/docs/web-extension-security-health) and run a scan — an import is the
   most likely moment to discover reused and breached passwords.
2. Check the imported items have **website URLs**, since autofill matches on them.
3. Delete the credentials from the old manager once you have confirmed the import.

---

## Troubleshooting

| Problem | Cause |
|---|---|
| Rows skipped | Missing name or password, or an unreadable encoding — re-export as UTF-8 |
| Accented characters mangled | The export used a non-UTF-8 encoding; re-export choosing UTF-8 |
| Nothing imported | The file is not a CSV, or has no recognizable header row |
| Autofill does not offer imported items | The rows had no `url` column — edit the items to add website URLs |

## Related

- [Creating New Password](https://docs.akeyless.io/docs/creating-new-password-1)
- [Security Health in the Extension](https://docs.akeyless.io/docs/web-extension-security-health)
- [Extension Settings](https://docs.akeyless.io/docs/web-extension-settings)
