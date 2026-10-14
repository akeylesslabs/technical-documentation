---
title: Exporting Your Passwords
---
Download the passwords in your Personal area as a CSV file, either as a backup or to move them
to another Akeyless account or password manager. The file uses the Generic CSV format, so it
imports straight back through **Import Passwords** without editing.

Open **Settings** → **Export Passwords**.

<Callout icon="⚠️" theme="warn">
  **The file holds your passwords in plain text.** Anyone who can open your `Downloads` folder
  can read every password in it. Delete it as soon as you have imported it or finished with it,
  and empty your `Trash` folder too.
</Callout>

---

## Export your passwords

1. Open **Settings** with the gear icon at the bottom of the left rail.
2. Select **Export Passwords**.
3. Read the confirmation, *Export personal passwords as a CSV file?*, and select **Export**.
4. Wait while the progress bar works through the stages below.
5. **Export Complete** reports how many passwords were exported and shows the file name.
   Select **Close**.

| Stage | What is happening |
|---|---|
| *Listing personal passwords…* | Collecting every password item in your Personal area |
| *Decrypting passwords… (12/40)* | Reading each password from the vault |
| *Saving CSV to Downloads…* | Writing the file |

The panel stays open until the export finishes, and **Cancel** is disabled while it runs. Every
password is read from the vault individually, so large vaults take longer.

---

## Where the file is saved

| Property | Value |
|---|---|
| **Location** | Your browser's `Downloads` folder |
| **File name** | `akeyless-personal-passwords-YYYY-MM-DD.csv`, dated the day of the export |
| **Exporting twice in a day** | The browser adds a number to the new file's name rather than overwriting the earlier one |
| **Encoding** | UTF-8 with a byte-order mark, so spreadsheet apps such as Excel show accented characters correctly |

---

## What the file contains

A header row, then one row per password item:

| Column | Contains |
|---|---|
| `name` | The item's path inside your Personal area, for example `Work/GitHub` |
| `url` | The item's first website URL |
| `username` | The username |
| `password` | The password |
| `description` | The item description |

Fields are comma-separated and quoted wherever they contain commas, quotes or line breaks, so
passwords with special characters come through intact.

### Included

Every **password item** in your Personal area, in every folder.

### Not included

- **Corporate** items. Export covers your Personal area only.
- Secret items, file items, rotated secrets and dynamic secrets
- Passkeys
- One-time password (OTP) keys, custom fields and tags
- Website URLs after the first one on each item

---

## Skipped items

An item is skipped, rather than failing the whole export, when its password is empty or the
vault does not return it in time. The completion message counts skipped items:

> *Exported 38 passwords (2 skipped — could not decrypt). Saved to your Downloads folder.*

The message does not name the skipped items. The usual cause is a password item whose password
field is empty.

---

## Importing the file back into Akeyless

The export is already in Generic CSV format:

1. In the extension, signed in to the account you are moving to, open **Settings** →
   **Import Passwords**.
2. Choose **Generic CSV** and upload the file.
3. Choose the destination area and folder.

Folder paths in the `name` column are recreated under the folder you choose. Importing
`Work/GitHub` into a folder named `Archive` creates `Archive/Work/GitHub`.

<Callout icon="ℹ️" theme="info">
  **Import with version 1.30.131 or later.** Earlier versions can mishandle folder paths and
  passwords that end in a backslash.
</Callout>

To move to a different password manager, use that product's CSV import. Most accept these
columns as they are, or let you match them up during the import.

See [Importing from Another Password Manager](https://docs.akeyless.io/docs/csv-password-importer).

---

## When Export Passwords is unavailable

The option is greyed out, with *Personal vault unavailable* underneath, when your account has no
Personal area. That happens when password management is disabled, the Personal folder is hidden
by policy, or you signed in with an API key. See
[Account Policies Affecting the Extension](https://docs.akeyless.io/docs/web-extension-account-policies).

## Messages

| Message | Meaning |
|---|---|
| *No personal passwords found to export.* | Your Personal area has no password items |
| *Personal vault is not available yet.* | Your Personal area has not been created yet. Save a password to it, then try again |
| *Could not export any passwords (decrypt failed for all items).* | Every item was skipped. See [Skipped items](#skipped-items) |

## The downloads permission

Export saves the file through the browser's downloads permission, which the extension requests
from version 1.30.130. When the extension updates to that version, your browser may ask you to
approve the new permission before turning the extension back on. Extensions that your
organization force-installs through browser policy update without asking.

## Related

- [Importing from Another Password Manager](https://docs.akeyless.io/docs/csv-password-importer)
- [Extension Settings](https://docs.akeyless.io/docs/web-extension-settings)
- [Personal Secrets](https://docs.akeyless.io/docs/web-extension-personal-area)
