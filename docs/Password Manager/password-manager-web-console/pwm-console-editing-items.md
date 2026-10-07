---
title: Editing, Sharing and Deleting Items
---
Every row and card carries a **⋯** actions menu. What it offers depends on your permissions
for that item.

## Opening an item

Select a row or card to open the item view. It shows the value with per-field copy controls,
website URLs, protection key, maximum versions, tags, description, and created and updated
dates.

Dynamic secrets additionally show producer status and TTL.

| Indicator | Meaning |
|---|---|
| **Zero Knowledge Encryption** | The item is wrapped with a customer fragment |
| **Lock** | Delete protection is on |
| **Personal** / **Corporate** | Which vault it lives in |

## Editing

**Edit** reopens the same stepped wizard used to create the item, pre-filled. Everything is
editable: name, username, password, URLs, location, description, maximum versions, protection
key, tags, delete protection, custom fields and the OTP authenticator.

Changing the **Location** between Personal and Corporate moves the item between vaults.

<Callout icon="⚠️" theme="warn">
  Moving an item from Personal to Corporate changes who can see it — everyone with vault access
  to the destination folder. The move is not reversible by undo; you would have to move it back.
</Callout>

### What cannot be edited

| Item | Why |
|---|---|
| **Rotated secrets** | Managed by Akeyless; the value is read-only |
| **Dynamic secrets** | Generated on demand |
| Items without **update** permission | **Edit** does not appear |

## Copying an item

**Copy** duplicates an item to a destination you choose. The wizard's location step is headed
**Copy to**.

Use it to base a new credential on an existing one, or to place a copy in another folder.

## Sharing

**Share** generates a time-limited link.

| Control | Options |
|---|---|
| **Share link validity** | 1 Hour, 1 Day, 7 Days, 14 Days, 30 Days |
| **One time view** | The link stops working after a single view |
| **Share with** | One or more email addresses |

<Callout icon="⚠️" theme="warn">
  **The link is shown once.** Copy it before closing the share screen — you cannot view it
  again. If you lose it, generate a new one.
</Callout>

Your organization may restrict which email domains can receive shares; a disallowed address is
reported as a validation error.

## Deleting

**Delete** moves the item to the [Recycle Bin](https://docs.akeyless.io/docs/pwm-console-recycle-bin). It is not
destroyed, and can be restored.

Delete-protected items cannot be deleted at all — edit the item, turn delete protection off,
save, then delete.

## Versions

The vault keeps historical versions up to the item's `Maximum Versions` limit. Lowering the
limit discards the oldest versions beyond the new value.

## Related

- [Creating Items](https://docs.akeyless.io/docs/pwm-console-creating-items)
- [Recycle Bin](https://docs.akeyless.io/docs/pwm-console-recycle-bin)
