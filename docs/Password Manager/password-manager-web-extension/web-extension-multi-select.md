---
title: Selecting Multiple Items
---
Multi-select applies a delete or restore action to several items at the same time, instead of opening each
one's menu.

![Multi-select with the bulk action bar](https://files.readme.io/05d09eebebe8c337f5867cb5e16938bb250e14ae1e0532eebd6f61559cae016a-multi-select-bulk-actions.png)
*Ticked items, with **Add** and **Delete** in the floating bar*

## Entering and leaving

| Control | Effect |
|---|---|
| **Select** *(header)* | Enters multi-select mode — a checkbox appears on every row |
| **Cancel** | Leaves multi-select mode and clears the selection |

While you are in multi-select mode, selecting a row ticks it rather than opening it.

## What you can do

| Action | Available in | Effect |
|---|---|---|
| **Add** | Personal, Corporate | Adds everything selected to Favorites |
| **Delete** | Personal, Corporate, Favorites | Moves everything selected to the Recycle Bin |
| **Restore** | Recycle Bin only | Returns the selected items to their original folders |
| **Delete** | Recycle Bin only | Removes the selected items permanently |

## Confirmation

Destructive actions always confirm first, and the button says exactly what will happen:

| Where | Button |
|---|---|
| Personal, Corporate, Favorites | **Move to Recycle Bin** |
| Recycle Bin | **Delete Forever** |

<Callout icon="⚠️" theme="warn">
  **Delete-protected items are skipped.** If your selection includes one, the rest proceed and
  the protected item stays where it is. Clear delete protection on that item first — see
  [Deleting Password / Secret](https://docs.akeyless.io/docs/deleting-password-1).
</Callout>

## Mixed selections

A selection can span folders, and can mix folders with individual items. Deleting a folder
takes its contents with it; restoring the folder brings them back.

Selection does not survive leaving the area. Switching tabs, or selecting **Cancel**, clears it.

## When bulk is the wrong tool

For a handful of items, the row's own **More Options** (⋯) menu is quicker. Multi-select pays
off from roughly five items upward, and for emptying the
[Recycle Bin](https://docs.akeyless.io/docs/web-extension-recycle-bin) — which has its own **Empty Recycle Bin** control
that does not need a selection at all.
