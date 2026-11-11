---
title: Importing from Another Password Manager
---
Bring credentials across from another password manager or browser. Ten sources are supported,
each with its own export instructions built into the console.

Select **Import** in the top toolbar.

![Step 1 — choose your source](https://files.readme.io/f38519af5fee1aaa082e07a7c43a987a807a868e2191c00c7179318bdde654ac-import-select-type.webp)
*Ten import sources*

## The import wizard

| Step | What happens |
|---|---|
| **1. Item Type** | Choose **Passwords**, **Secrets** or **Certificates**. This page covers passwords |
| **2. Select Service** | Choose the password manager you are moving from (passwords only) |
| **3. Upload CSV** | Read the export instructions, then upload the file |
| **4. Destination** | Choose Personal or Corporate, the folder, and any tags |
| **5. Results** | Watch it run, then read what succeeded and what did not |

The rail on the left tracks your position, and you can step back without losing what you
entered.

---

## Supported sources

| Source | How to export |
|---|---|
| **1Password** | Desktop app → **Export**; instructions at [1Password Support](https://support.1password.com) |
| **LastPass** | [the LastPass vault](https://lastpass.com/vault) → **Advanced Options** → **Export** → confirm by email → re-enter your password |
| **Bitwarden** | **Vault** → **Tools** → **Export vault**; instructions at [Bitwarden Help](https://bitwarden.com/help) |
| **Dashlane** | Desktop app → **My Account** → **Export data** |
| **Keeper** | **Vault** → **Export**; instructions at [Keeper Documentation](https://docs.keeper.io) |
| **KeePass** | **File** → **Export** → **CSV File…** (UTF-8 recommended) |
| **Google** | `passwords.google.com` → gear icon → **Export** |
| **Microsoft Edge** | `edge://settings/passwords` → **Saved passwords** → **⋯** → **Export passwords** |
| **Apple** | iPhone and Mac instructions at [Apple Support](https://support.apple.com) |
| **Generic CSV** | Any CSV with the columns below |

---

## Generic CSV format

Columns: `name`, `url`, `username`, `password`, `description` (also accepted as `note` or `notes`).

| Behavior | Detail |
|---|---|
| **Column order** | Any — headers are detected automatically |
| **Delimiter** | Detected automatically |
| **Encoding** | UTF-8 preferred; common Western European (Latin) encodings also decode |
| **Extra columns** | Ignored rather than rejected |

### KeePass default columns

A default KeePass export produces `Account`, `Login Name`, `Password`, `Web Site`, `Comments`.
These are recognized without renaming anything.

### Keeper exports

Upload Keeper's CSV export as it is, in **Keeper vault export CSV**. Keeper writes no header row,
so the columns are read in Keeper's order: `Folder`, `Title`, `Login`, `Password`,
`Website Address`, `Notes`, `Shared Folder`, then custom fields as name/value pairs. A file with
a header row works too.

| Keeper data | Becomes |
|---|---|
| `Folder` (sub-folders separated by `\`) | Folders under the destination you choose |
| `Shared Folder` | A folder with that name under the destination. Permission suffixes such as `#edit` are dropped |
| A row with `Notes` and no `Password` | A static secret (Keeper secure note) |
| Custom fields | Custom fields on the password |

**Shared Records Report (optional).** Also upload Keeper's Shared Records Report in
**Shared Records Report CSV (optional)**, with or without a header row. Each item is tagged with
who it was shared with in Keeper. With **Group direct-shared items into folders by who they were
shared with** on, direct-shared items go under
`<destination>/Keeper-Direct-Shares/<you>/<shared with>/`; **Importer identity** sets the `<you>`
part. Keeper sharing permissions are not recreated, so share these folders in Akeyless if others
need access.

**Re-importing.** If an item with the same name already exists, an identical one is skipped and
counted as a duplicate. A different one is saved as a copy under `_Keeper-Conflicts/<you>/` in
the same folder, so nothing is overwritten. The report lists these, with a `keeper-conflicts.csv`
download.

Everything is created inside the destination you choose. Nothing is created at the vault root.
The desktop app imports the same way.

---

## Destination

Choose where everything goes **before** the import runs:

| Choice | Notes |
|---|---|
| **Personal** or **Corporate** | Corporate is offered only where your permissions allow it |
| `Folder path` | Imported items land here rather than at the root |
| `Tags` | Applied to everything imported, which makes the batch easy to find or undo later |

<Callout icon="ℹ️" theme="info">
  **Tag the batch.** Applying a tag like `imported-2026-10` means you can filter to exactly
  what the import created, review it, and bulk-delete it if something went wrong.
</Callout>

## Results

Each row becomes a **password item**:

| CSV column | Becomes |
|---|---|
| `name` | The item name |
| `username` | The username |
| `password` | The password |
| `url` | A website URL, which drives autofill and Launch in the extension |
| `description` / `note` | The item description |

The report lists what succeeded and what failed, with the row number and reason for each
failure, so no row is dropped without a record.

---

## Afterwards

<Callout icon="⚠️" theme="warn">
  **Delete the exported CSV.** It contains every password you just imported, in plain text, in
  your `Downloads` folder. Empty your `Trash` folder too.
</Callout>

1. Run [Security Health](https://docs.akeyless.io/docs/pwm-console-security-health) — an import is the most likely moment
   to discover reused and breached passwords.
2. Check imported items have `Website URLs`, since autofill matches on them.
3. Delete the credentials from the old manager once you have confirmed the import.

## Troubleshooting

| Problem | Cause |
|---|---|
| Rows failed | Missing name or password — the report names the row |
| Accented characters mangled | A non-UTF-8 export; re-export choosing UTF-8 |
| Nothing imported | Not a CSV, or no recognizable header row |
| Keeper: "Could not detect required columns" | Older desktop app (before 0.1.128) needed a header row. Update it, or add `Folder,Title,Login,Password,Website Address,Notes,Shared Folder,Custom Fields` as the first line |
| "unable to get personal folder" | An account setting blocks your personal folder. See [Personal Secrets](https://docs.akeyless.io/docs/pwm-console-personal-area). Import to Corporate meanwhile |
| Autofill ignores imported items | The rows had no `url` column |

## Related

- [Creating Items](https://docs.akeyless.io/docs/pwm-console-creating-items)
- [Security Health](https://docs.akeyless.io/docs/pwm-console-security-health)
