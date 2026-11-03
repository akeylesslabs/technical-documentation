---
title: Viewing, Copying and Managing Items
---
On a phone there is no mouse to hover, so item actions live in three places: **tap** a row to
open it, **swipe** a row to reveal quick actions, and tap **More** for everything else.

## Opening an item

Tap any item to open it. From the item view you can reveal the password with the eye icon,
copy any field, open the website, and see the current one-time password code if the item has
one. Certificates show the certificate and its private key.

See [Viewing an Item](https://docs.akeyless.io/docs/web-extension-viewing-items) for every
field the view shows.

## Swipe actions

| Swipe | Reveals | What it does |
|---|---|---|
| **Right** (finger moves to the right) | **Select** | Starts selecting several items, with this one already selected |
| **Left** (finger moves to the left) | **Favorite** / **Unfavorite** | Stars or un-stars the item |
| | **Delete** | Moves the item to the Recycle Bin, after you confirm |
| | **More** | Opens the **More options** sheet |

A short message at the bottom of the screen confirms each action, such as **Added to
favorites**. Only one row stays open at a time; swiping another row or tapping elsewhere
closes it.

Folders swipe the same way: **Select** on the right, **Favorite** and **Delete** on the left.

## The More options sheet

| Action | What it does |
|---|---|
| **Launch website** | Opens the item's website inside the app |
| **Copy username** | Copies the username of a password item |
| **Copy password** / **Copy secret** | Copies the value without opening the item |
| **Edit** | Opens the item's edit form — see [Editing, Copying & Moving Items](https://docs.akeyless.io/docs/editing-password-details-1) |
| **Copy** | Creates a copy of the item, for example in another folder or in the other area |
| **Share** | Creates a time-limited share link you can send to someone — see [Sharing Password / Secret](https://docs.akeyless.io/docs/sharing-password-1) |
| **Restore** | In the Recycle Bin only — puts the item back where it was |

<Callout icon="ℹ️" theme="info">
  **Missing an action?** The app only shows what your access role allows for that item. If you
  can read an item but not update it, **Edit** does not appear. Certificates cannot be edited
  or copied from the app.
</Callout>

If your organization does not allow revealing or copying corporate secrets, copying shows
**Blocked by policy**. Personal items are never blocked.

## Selecting several items

1. Swipe an item to the right and tap **Select**.
2. Tap more items to add them. Tap **Select All** to select everything in view, or **Clear**
   to start over.
3. Choose an action from the bar at the bottom:

| Action | What it does |
|---|---|
| **Favorite** / **Unstar** | Adds or removes all selected items from Favorites |
| **Delete** | Moves the selected items to the Recycle Bin. Delete-protected items are skipped |
| **Restore** | In the Recycle Bin only — restores the selected items |
| **Delete Forever** | In the Recycle Bin only — permanently deletes the selected items |

Tap **Done** or **Cancel** to leave selection mode.

See [Selecting Multiple Items](https://docs.akeyless.io/docs/web-extension-multi-select) for
how selection works across folders.

## Deleting and restoring

Deleting moves an item to the **Recycle Bin** (**More** → **Recycle Bin**). Items marked
**Delete protection** cannot be deleted until the protection is turned off.

In the Recycle Bin:

- Swipe an item left and tap **Delete Forever** to remove it for good.
- Swipe left, tap **More**, then **Restore** to put it back.
- Tap the trash icon in the header to empty the whole bin.

<Callout icon="⚠️" theme="warn">
  **Delete Forever** and emptying the bin cannot be undone.
</Callout>

See [Recycle Bin](https://docs.akeyless.io/docs/web-extension-recycle-bin) and
[Deleting Password / Secret](https://docs.akeyless.io/docs/deleting-password-1).

## Related

- [Creating Items and Generating Passwords](https://docs.akeyless.io/docs/pwm-mobile-creating-items)
- [Item Types Reference](https://docs.akeyless.io/docs/web-extension-item-types)
- [Adding Items To Favorites](https://docs.akeyless.io/docs/adding-password-to-favorites-1)
