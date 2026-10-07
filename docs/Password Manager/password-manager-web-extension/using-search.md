---
title: Searching for Passwords and Secrets
---
Every area has its own search box at the top of the list:

| Area | Placeholder |
|---|---|
| Personal Secrets | *Search in personal secrets* |
| Corporate Secrets | *Search in corporate secrets* |
| Favorite Secrets | *Search in favorites secrets* |
| Recycle Bin | *Search in recycle bin secrets* |

## How search works

Search in the **Personal** and **Corporate** areas runs against the vault, not just the items
already loaded on screen. That means it finds items anywhere in the area, including in folders
you have never opened.

Your keystrokes are debounced, so the extension waits until you stop typing before querying —
you will not fire one request per character.

Search in **Favorites** and the **Recycle Bin** filters the list already on screen.

## Scope

| Behavior | Detail |
|---|---|
| **Area-scoped** | Results come from the area you are in. Switch areas to search the other vault |
| **Not folder-scoped** | Results span the whole area, not only the folder you have open |
| **Combines with filters** | An active type or tag filter narrows the results — see [Using Filters & Tags](https://docs.akeyless.io/docs/using-filters-tags) |
| **Cached per session** | Repeating a search is instant. The cache holds names and metadata only, never secret values, and is dropped when you sign out |

## Working with results

Result rows behave like any other row — open them, copy from them, launch them, or star them.

A result found by search can be added to Favorites directly; it does not need to be located in
its folder first.

## Clearing

Empty the box to return to the full list. Switching areas keeps your search term where it
still applies, so you can check both vaults for the same credential without retyping.

## If search finds nothing

<Callout icon="ℹ️" theme="info">
  Search matches item names. It does not look inside secret values, and it does not search
  descriptions or custom field contents.
</Callout>

- Check whether a type or tag filter is still active — clear it with **Clear All Filters**.
- Check you are in the right area. Personal and Corporate are separate vaults.
- Items in the Recycle Bin are excluded from the normal areas. Search the Recycle Bin for a
  deleted item — see [Recycle Bin](https://docs.akeyless.io/docs/web-extension-recycle-bin).
