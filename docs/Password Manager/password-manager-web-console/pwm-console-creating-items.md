---
title: Creating Items
---
Select **+ Create** in the top toolbar and choose what to make.

![The Create menu](https://files.readme.io/398de878efe79b3922418d11898bf82ec4b5f1dee858235e7a91aafff44c4ca8-create-menu.webp)
*New Folder, New Secret Item, New Password Item, New File Item*

<Callout icon="ℹ️" theme="info">
  **New File Item appears in Personal only.** Files are personal-vault items; the Corporate
  create menu offers three options rather than four.
</Callout>

Creation flows are **stepped wizards** with a progress rail on the left, so a long form is
broken into stages you can move back and forth through. The step you are on is named in the
subtitle.

---

## New Password

Three steps.

![New Password, step 1](https://files.readme.io/29ed18eaa634289805f0b47182f7f08cbbc0035b220ad82c0a6a98ad706b403c-new-password.webp)
*Step 1 — name, username, password*

### Step 1 — Name, username, password

| Field | Notes |
|---|---|
| **Item name** | Required |
| **Username** | Required |
| **Password** | Required. **Random** or **Passphrase** generator, a refresh control, and a reveal eye |

**Password Strength (guidance)** rates what is in the field:

> This meter reflects length and real-world guessability. It does not add points for symbols
> or uppercase. Generation Settings below are separate.

**Details** expands the reasoning behind the rating.

**Generation Settings** control the generator, not the meter:

| Setting | Controls |
|---|---|
| **At least N characters** | Minimum length, set with the slider |
| **A-Z**, **a-z**, **0-9**, **!@#** | Which character classes to include |
| **Allowed special characters** | Exactly which symbols may be used, with **Reset to default** |

Each requirement shows a tick or cross against the current value.

<Callout icon="ℹ️" theme="info">
  **The meter and the settings are independent.** Ticking every box does not make a weak
  password strong — `Password1!` satisfies all of them and still rates **Very Weak**, because
  it is among the first an attacker tries.
</Callout>

### Step 2 — Location, Protection Key, tags & details

Destination vault (**Personal** or **Corporate**), folder path, Protection Key, tags,
description, Delete protection and Maximum Versions.

When editing an existing item this step is headed **Copy to**.

### Step 3 — OTP (optional)

Add an authenticator so the console and extension generate your six-digit codes. Skippable.

---

## New Secret

Two steps.

![New Secret, step 1](https://files.readme.io/95f839241c445e2810fe1305b7d9328ce88fefb9fd7ffd1c2abb0d2e3b19f8c9-new-secret.webp)
*Step 1 — name, type, value, and folder location*

### Step 1 — Name, type, value, and folder location

| Field | Notes |
|---|---|
| **Secret name** | Required |
| **Type** | **Generic** by default; **Select** to choose a specific type |
| **Maximum Versions** | Shows your account default and the allowed range, e.g. *Account default: 100 (allowed 1–300)* |
| **Format** | **Text**, **Key/value** or **JSON** |
| **Value** | Required, with a reveal eye |
| **Location** | **Personal** or **Corporate**, then the folder path |

### The three formats

| Format | Use when |
|---|---|
| **Text** | One value consumed whole — an API key, a connection string, a certificate body |
| **Key/value** | Several named values consumed separately — host, port, username, password |
| **JSON** | Nested structure, or a shape something downstream depends on |

Key/value and JSON reveal the value field by default, since structured content cannot be
edited blind. JSON is validated before saving.

### Step 2 — Description, Protection Key, and tags

---

## New File

A single step.

![New File](https://files.readme.io/62b7be807355cacfe9d3d91f9a8f5d4ad587ca78afe0ce2aaacf855218c86c2f-new-file.webp)
*Upload an encrypted file to your personal vault*

| Field | Notes |
|---|---|
| **Name** | e.g. *Certificates* |
| **File** | Drag and drop, or click to browse. **Maximum 10 MB** |
| **Description** | Optional |
| **Personal vault location** | Folder path. Marked **Personal only** |
| **Metadata** | Delete protection, tags |

<Callout icon="⚠️" theme="warn">
  Files are capped at **10 MB each** and count against your account's File storage quota, which
  is shared across the account. Check it in [Settings](https://docs.akeyless.io/docs/pwm-console-settings) before a large
  upload.
</Callout>

---

## New Folder

A single step.

![New Folder](https://files.readme.io/cbf7c5863d5f6d6a72c039187ef99fad61f8452084ea96289e79ddf3a32d598c-new-folder.webp)
*Name, description, parent folder and metadata*

| Field | Notes |
|---|---|
| **Folder name** | Required |
| **Description** | Optional |
| **Parent folder** | **Personal** or **Corporate**, then the path |
| **Delete protection** | Prevents the folder and its contents being deleted |
| **Tags** | Applied to the folder |

---

## Common to every flow

| Element | Behavior |
|---|---|
| **Step rail** | Shows where you are; completed steps carry a tick |
| **Cancel** | Abandons the flow and returns you to the area you came from |
| **Next** / **Save** | Disabled until the current step validates |
| **Location switch** | Personal and Corporate side by side; Corporate is hidden where your permissions do not allow it |

## Related

- [Editing, Sharing and Deleting Items](https://docs.akeyless.io/docs/pwm-console-editing-items)
- [Importing from Another Password Manager](https://docs.akeyless.io/docs/pwm-console-import)
- [Settings](https://docs.akeyless.io/docs/pwm-console-settings)
