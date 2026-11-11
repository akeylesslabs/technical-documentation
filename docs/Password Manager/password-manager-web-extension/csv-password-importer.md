---
title: Importing from Another Password Manager
---
Bring your credentials across from another password manager or browser. Ten sources are
supported, each with its own export instructions built into the extension.

Open **Settings** → **Import Passwords**.

![The import source list](https://files.readme.io/d722ecea95425835e705b6cd8bd779868409dd1fe7028013c8b21d4ae788b481-import-vendor-list.png)
*Choose the password manager you are moving from*

Select a source to see its step-by-step export guide, then upload the CSV it produces.

---

## Supported sources

| Source | How to export |
|---|---|
| **1Password** | Desktop app → **Export**; instructions at [1Password Support](https://support.1password.com) |
| **LastPass** | [the LastPass vault](https://lastpass.com/vault) → **Advanced Options** → **Export** → confirm by email → re-enter your password |
| **Bitwarden** | **Vault** → **Tools** → **Export vault**; instructions at [Bitwarden Help](https://bitwarden.com/help) |
| **Dashlane** | Desktop app → **My Account** → **Export data**; instructions at [Dashlane Support](https://support.dashlane.com) |
| **Keeper** | **Vault** → **Export**; instructions at [Keeper Documentation](https://docs.keeper.io) |
| **Google** | `passwords.google.com` → gear icon → **Export** |
| **Microsoft Edge** | `edge://settings/passwords` → **Saved passwords** → **⋯** → **Export passwords** |
| **Apple** | iPhone and Mac instructions at [Apple Support](https://support.apple.com) |
| **KeePass** | **File** → **Export** → **CSV File…** (UTF-8 recommended) |
| **Generic CSV** | Any CSV with the columns below |

---

## Generic CSV format

Columns: `name`, `url`, `username`, `password`, `description` (also accepted as `note` or `notes`).

Optional:

| Column | Becomes |
|---|---|
| `otp` / `otpauth` / `totp` / `mfa_secret` (and similar) | Password OTP (`otpauth` custom field). Cell may be an `otpauth://` URI or a Base32 TOTP secret. |
| **Any other header** | A custom field with that header as the label (toggle which columns to import after upload) |

| Behavior | Detail |
|---|---|
| **Column order** | Any — headers are detected automatically |
| **Delimiter** | Detected automatically (comma, semicolon, tab) |
| **Encoding** | UTF-8 preferred; common Western European (Latin) encodings also decode |
| **Extra columns** | Imported as custom fields (Generic CSV); you can deselect columns before import |

The extension's own **Export Passwords** writes the core five-column format, so a file exported from one Akeyless
account imports into another unchanged. See [Exporting Your Passwords](https://docs.akeyless.io/docs/web-extension-export-passwords).

### KeePass default columns

A default KeePass export produces `Account`, `Login Name`, `Password`, `Web Site`, `Comments`.
These are recognized without renaming anything.

### Keeper exports

Upload Keeper's CSV export as it is. Keeper writes no header row, so when **Keeper** is the
selected source the columns are read in Keeper's order: `Folder`, `Title`, `Login`, `Password`,
`Website Address`, `Notes`, `Shared Folder`, then custom fields as name/value pairs. A file with a
header row works too.

| Keeper data | Becomes |
|---|---|
| `Folder` (sub-folders separated by `\`) | Folders under the destination you choose |
| `Shared Folder` | A folder with that name under the destination. Permission suffixes such as `#edit` are dropped |
| A row with `Notes` and no `Password` | A secret (Keeper secure note) |
| Custom fields | Custom fields on the password |

You can also upload Keeper's **Shared Records Report** CSV, with or without a header row. Each
item is then tagged with who it was shared with in Keeper, and direct-shared items can be grouped
under `<destination>/Keeper-Direct-Shares/<you>/<shared with>/`. Keeper sharing permissions are not
recreated; share these folders in Akeyless if others need access.

**Re-importing.** If an item with the same name already exists, an identical one is skipped and
counted as a duplicate. A different one is saved as a copy under `_Keeper-Conflicts/<you>/` in
the same folder, so nothing is overwritten. The import summary lists these.

Everything is created inside the destination you choose. Nothing is created at the vault root.

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
| `otp` (etc.) | Authenticator / OTP on the password item |
| other columns | Custom fields (Generic CSV only) |

Imported items land in the area and folder you choose during the import. A folder path in the
`name` column, such as `Work/GitHub`, is recreated under the folder you choose.

## The import summary

When the upload finishes, a summary reports how many rows were imported and how many were
skipped, so no row is dropped without a record.

Rows are usually skipped because they are missing a required field, or because the file could
not be decoded — see below.

---

## Afterwards

<Callout icon="⚠️" theme="warn">
  **Delete the exported CSV.** It contains every password you just imported, in plain text,
  sitting in your `Downloads` folder. Empty your `Trash` folder too.
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
| Keeper: "Could not detect required columns" | Extension older than 1.30.161, which needed a header row. Update the extension, or add `Folder,Title,Login,Password,Website Address,Notes,Shared Folder,Custom Fields` as the first line |
| "unable to get personal folder" | An account setting blocks your personal folder — see [Troubleshooting](https://docs.akeyless.io/docs/web-extension-troubleshooting). Import to Corporate meanwhile |
| Autofill does not offer imported items | The rows had no `url` column — edit the items to add website URLs |

## Related

- [Exporting Your Passwords](https://docs.akeyless.io/docs/web-extension-export-passwords)
- [Creating New Password](https://docs.akeyless.io/docs/creating-new-password-1)
- [Security Health in the Extension](https://docs.akeyless.io/docs/web-extension-security-health)
- [Extension Settings](https://docs.akeyless.io/docs/web-extension-settings)
