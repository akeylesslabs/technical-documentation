---
title: Using Filters & Tags
---
Select the funnel icon in the header to narrow the current list. The panel has two tabs:
**Types** and **Tags**.

![Filtering by item type](https://files.readme.io/f6a021021f48c23a0dbe6b82e58654c1a58dbab0071cee79719cb0fa48fbcdb7-filter-by-type.png)
*Filtering by item type*

## Types

Six types, matching the item kinds the vault stores:

| Type | Covers |
|---|---|
| **PASSWORD** | Password items — username, password, website URLs, OTP, custom fields |
| **FILE** | Files stored in the vault |
| **STATIC SECRET** | Free-form secret values, plain text or key/value |
| **ROTATED SECRET** | Secrets rotated on a schedule by Akeyless |
| **DYNAMIC SECRET** | Credentials generated on demand |
| **PASSKEY** | WebAuthn credentials |

Tick as many as you need — selecting several shows items matching **any** of them.

The counter at the top right of the panel shows how many types exist in this area.

## Tags

The **Tags** tab lists the vault tags present on your items. Tags are applied when you create
or edit an item, under **MetaData** — see
[Creating New Password](https://docs.akeyless.io/docs/creating-new-password-1).

Tags are the way to group items that do not share a type or a folder — for example everything
belonging to one project, one customer, or one environment.

## Combining filters

| Combination | Result |
|---|---|
| Several types | Items matching any selected type |
| Several tags | Items matching the selected tags |
| Types **and** tags | Items matching both conditions |
| Filter **and** search | Search results, narrowed by the filter |

## Clearing

| Control | Effect |
|---|---|
| **Clear Types Selection** | Clears the Types tab only |
| **Clear All Filters** | Clears both tabs |
| **×** | Closes the panel, keeping the filter active |

<Callout icon="⚠️" theme="warn">
  Closing the panel does not clear the filter. If a list looks emptier than you expect, check
  whether a filter is still applied before concluding an item is missing.
</Callout>

## Scope

Filters apply to the area you are in and stay active as you move between folders. They are not
carried across to another area.

## Searching inside the panel

Both tabs have a **Search in types** / search box, useful when an account has many tags.

## Related

- [Searching for Passwords and Secrets](https://docs.akeyless.io/docs/using-search)
- [Item Types Reference](https://docs.akeyless.io/docs/web-extension-item-types)
- [Switching Between Folders & Flat View](https://docs.akeyless.io/docs/password-list-switching-between-folders-flat-view-1)
