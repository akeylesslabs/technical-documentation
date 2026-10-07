---
title: Personal Secrets
---
Your own vault — items only you can see. Nobody else in your organization has access, including
administrators.

![The Personal area](https://files.readme.io/20c3f27945bc91866feb657404a37d887ba1e2e5358062daf19cf82b39f7d05b-personal-secrets-list.png)
*The Personal area*

## What this area contains

| Type | Notes |
|---|---|
| **Password items** | Username, password, Website URLs, OTP, Custom Fields |
| **Secret items** | Free-form values in Text, Key/value or JSON format |
| **File items** | Files, counted against your account's file quota |
| **Passkeys** | **Only** stored here — never in Corporate |
| **Folders** | To organize any of the above |

## What makes it different from Corporate

| | Personal | Corporate |
|---|---|---|
| Who can see it | Only you | Everyone with vault access to the folder |
| Passkeys | Yes | No |
| File items | Yes | No |
| Security Health | Covers this area | Not covered |
| Sharing | By time-limited link | By link, plus vault permissions |

## Header controls

| Control | Does |
|---|---|
| **Search in Personal Secrets** | Searches the whole area, server-side |
| **Filter** (funnel) | Narrows by type and tag |
| **View toggle** | List or grid |
| **+** | New Folder, Secret, Password or File item |
| **Sort By A–Z** | Alphabetical; the arrow reverses |
| **Select** | Multi-select mode |
| **Click to refresh** | Reloads from the vault |

## Dark Mode

![The Personal area in Dark Mode](https://files.readme.io/43f9e2d2e96931fb461ec5af87ac84b43ce11fea948236ae108f9b7553337b09-personal-secrets-dark.png)
*The same area with Dark Mode enabled*

## When the Personal tab is missing

<Callout icon="⚠️" theme="warn">
  The Personal area is hidden when **any** of these apply:

  * Password management is disabled on your account
  * Your account hides the personal folder
  * You signed in with an API-key style credential
  * On DBK tenants, your session's product types do not include `apm`

  These are account policies, not extension settings. See
  [Account Policies Affecting the Extension](https://docs.akeyless.io/docs/web-extension-account-policies).
</Callout>

Hiding the Personal area also hides **Security Health**, which scores personal items only.

## Related

- [Corporate Secrets](https://docs.akeyless.io/docs/web-extension-corporate-area)
- [Security Health in the Extension](https://docs.akeyless.io/docs/web-extension-security-health)
- [Item Types Reference](https://docs.akeyless.io/docs/web-extension-item-types)
