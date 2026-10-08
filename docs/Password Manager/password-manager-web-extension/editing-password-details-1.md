---
title: Editing, Copying & Moving Items
---
## Editing

Open the **More Options** (⋯) menu on any item row, or on the item preview, and choose **Edit**. The same overlay used to create the item opens, pre-filled.

Every field is editable: `Name`, `Username`, `Password`, `Website URLs`, `Location`, `Description`, `Maximum Versions`, `Protection Key`, `Tags`, `Delete protection`, `Custom Fields` and `Authenticator (OTP)`.

## Copying

Choose **Copy** to duplicate an item. The overlay opens in copy mode — its `Location` section is headed `Copy to` — so you pick a destination for the duplicate.

Use this to base a new credential on an existing one, or to place a copy in a different folder.

## Moving

Items can be moved between folders, and between the Personal and Corporate areas, by editing the item and changing its `Location`.

<Callout icon="ℹ️" theme="info">
  Moving an item between Personal and Corporate changes who can see it. A Corporate item is visible to everyone with vault access to that folder.
</Callout>

## Versions

The vault keeps historical versions of a secret up to the item's `Maximum Versions` value. Lowering the value discards the oldest versions beyond the new limit.

## What you cannot edit

- **Rotated** and **dynamic** secrets are managed by Akeyless — their values are read-only in the extension.
- Items you only have read permission on show no **Edit** action.
- **Delete-protected** items can be edited but not deleted.

## Related

- [Creating New Password](https://docs.akeyless.io/docs/creating-new-password-1)
- [Deleting Password / Secret](https://docs.akeyless.io/docs/deleting-password-1)
- [Viewing an Item](https://docs.akeyless.io/docs/web-extension-viewing-items)
