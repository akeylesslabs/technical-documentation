---
title: Personal, Corporate & Favorites Navigation
---
The left rail switches between areas. Hovering an icon names it.

![Tooltip on a sidebar icon](https://files.readme.io/0fb2aa173deb536d0f3cbc01314eef65cabedc66c4ed1f716c31b0a55d47e9eb-sidebar-tooltip.png)
*Each rail icon names its area on hover and on keyboard focus*

## The areas

| Icon | Area | What it holds |
|---|---|---|
| Person | **[Personal Secrets](https://docs.akeyless.io/docs/web-extension-personal-area)** | Items only you can see, including passkeys and files |
| Building | **[Corporate Secrets](https://docs.akeyless.io/docs/web-extension-corporate-area)** | Items shared across your organization |
| Star | **[Favorite Secrets](https://docs.akeyless.io/docs/adding-password-to-favorites-1)** | Shortcuts to items and folders from either vault |
| Trash | **[Recycle Bin](https://docs.akeyless.io/docs/web-extension-recycle-bin)** | Deleted items, restorable |
| Heart | **[Security Health](https://docs.akeyless.io/docs/web-extension-security-health)** | A score for your personal credentials |

At the bottom of the rail:

| Icon | Does |
|---|---|
| Pin | [Dock the extension](https://docs.akeyless.io/docs/web-extension-side-panel) beside the page |
| External link | Opens the Akeyless web console for your tenant |
| Gear | [Extension Settings](https://docs.akeyless.io/docs/web-extension-settings) |

## Tabs that are not there

Areas are hidden when they do not apply to your account rather than shown and failing:

| Missing | Why |
|---|---|
| **Personal** | Password management disabled, personal folder hidden, or an API-key sign-in |
| **Security Health** | Follows Personal — it scores personal items only |
| **Corporate** | Your vault permissions do not allow listing secrets |

See [Account Policies Affecting the Extension](https://docs.akeyless.io/docs/web-extension-account-policies).

## Shared controls

Every area has the same header: search, filter, view toggle, sort, **Select** for multi-select,
and **Click to refresh** with a **Last refreshed** indicator.

The create **+** appears in Personal and Corporate only.

## Related

- [Personal Secrets](https://docs.akeyless.io/docs/web-extension-personal-area)
- [Corporate Secrets](https://docs.akeyless.io/docs/web-extension-corporate-area)
- [Searching for Passwords and Secrets](https://docs.akeyless.io/docs/using-search)
