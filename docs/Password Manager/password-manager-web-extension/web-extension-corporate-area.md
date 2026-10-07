---
title: Corporate Secrets
---
Items shared across your organization. What you can see and do here is governed by your vault
permissions, not by extension settings.

![The Corporate area](https://files.readme.io/5e257857e726fe4673f5059d30608a1506818e249049bbd7c6d36d395e62ffb6-corporate-secrets-list.png)
*The Corporate area*

## What this area contains

| Type | Notes |
|---|---|
| **Password items** | Shared logins |
| **Secret items** | API keys, connection strings, certificates |
| **Rotated secrets** | Rotated on a schedule by Akeyless; read-only |
| **Dynamic secrets** | Generated on demand, with producer status and TTL |
| **Folders** | Mirroring your team or environment structure |

Passkeys and file items are personal-only and do not appear here.

## Creating in Corporate

![The create menu in the Corporate area](https://files.readme.io/71524d6baca1ca29089f21534f798294c773d64b6f1d3b81bd151f2268989dc6-create-menu-corporate.png)
*Corporate offers folders, secret items and password items*

<Callout icon="ℹ️" theme="info">
  The Corporate create menu has **three** options — New Folder, New Secret Item and New
  Password Item. **New File Item is personal-only** and does not appear here.
</Callout>

## Permissions

Each item lists the operations permitted for the current user. The extension hides what you cannot
do rather than failing after the fact:

| Permission | Effect |
|---|---|
| `read` | You can open the item and copy its value |
| `list` | The item appears in lists and search |
| `update` | **Edit** appears in the ⋯ menu |
| `delete` | **Delete** appears in the ⋯ menu |

A **lock** badge marks delete-protected items, which cannot be deleted by anyone until the
protection is cleared.

## Shared items can change between refreshes

<Callout icon="ℹ️" theme="info">
  Lists are cached so the extension opens instantly. A colleague's edit will not appear until
  you select **Click to refresh**. The **Last refreshed** indicator tells you how stale the
  list is.
</Callout>

## When the Corporate tab is missing

The tab is hidden when your vault access summary does not permit listing secrets. That is a
vault permission set by your administrator — see
[Account Policies Affecting the Extension](https://docs.akeyless.io/docs/web-extension-account-policies).

## Related

- [Personal Secrets](https://docs.akeyless.io/docs/web-extension-personal-area)
- [Item Types Reference](https://docs.akeyless.io/docs/web-extension-item-types)
- [Sharing Password / Secret](https://docs.akeyless.io/docs/sharing-password-1)
