---
title: Deleting Password / Secret
---
Deleting is reversible. Items go to the Recycle Bin rather than being destroyed, and stay
there until you purge them.

## Deleting one item

1. Open the item's **More Options** (⋯) menu, from its row or from the item preview.
2. Choose **Delete**.
3. Confirm with **Move to Recycle Bin**.

The item disappears from the normal lists and appears in the
[Recycle Bin](https://docs.akeyless.io/docs/web-extension-recycle-bin).

## Deleting several

Select **Select** in the header, tick the items, then choose **Delete** — see
[Selecting Multiple Items](https://docs.akeyless.io/docs/web-extension-multi-select).

## Delete protection

<Callout icon="⚠️" theme="warn">
  Items with delete protection **cannot be deleted at all**. They show a lock badge and never
  reach the Recycle Bin.
</Callout>

To delete one:

1. Edit the item.
2. Turn **Delete protection** off.
3. Save.
4. Delete.

Your account may create every new item with delete protection on. See
[Account Policies Affecting the Extension](https://docs.akeyless.io/docs/web-extension-account-policies).

## Folders

Deleting a folder takes everything inside it. Restoring the folder brings its contents back
together with it, in their original structure.

## What deletion affects

| Effect | Detail |
|---|---|
| Lists | The item leaves Personal, Corporate and search results |
| Favorites | The star is removed. Restoring does not re-add it |
| Autofill | The credential stops being offered on websites |
| Security Health | The item drops out of the metrics |
| Shared links | Existing share links stop resolving |

## Permanent deletion

Permanent removal happens only inside the Recycle Bin:

| Control | Effect |
|---|---|
| **Delete Forever** | Removes one item permanently |
| **Empty Recycle Bin** | Removes everything permanently |

<Callout icon="⚠️" theme="warn">
  Permanent deletion cannot be undone, and the extension cannot recover a purged item. If you
  are unsure, leave it in the Recycle Bin — nothing forces you to empty it.
</Callout>

## Permissions

**Delete** appears only on items you have delete permission for. On a Corporate item without
that permission the action is absent — this is a vault permission, not an extension setting.
