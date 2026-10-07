---
title: Account Policies Affecting the Extension
---
<Callout icon="ℹ️" theme="info">
  **Audience: account administrators and support.**
</Callout>

Account settings and vault permissions change what users see without notification. **Most "a tab is missing" reports resolve here**, not in the extension.

## Visibility

| Policy | Effect when set |
|---|---|
| `passwordManagement` disabled | Personal vault and File storage hidden |
| `hidePersonalFolder` | Personal tab and Security Health hidden |
| Vault `secrets_allowed` denied | Corporate tab hidden |
| Sign-in with an API key (access type `api_key`) | Personal vault hidden |
| `product_types` without `apm` *(DBK tenants)* | Password manager features unavailable |

## Behavior

| Policy | Effect |
|---|---|
| `allowAutoFill` | Server default for the `Autofill` toggle. A user's manual change overrides it from then on |
| `hide_secret_reveal_copy` | Secure paste mode — no reveal, no copy of secret values anywhere |
| `allow_passkeys` disabled | Passkey management unavailable |
| Organization passkey suppression *(DBK)* | Passkeys hidden from lists, filters and Settings entirely |
| `protect_items_by_default` | New items created with delete protection on |
| `account_default_key_name` | Preselects the protection key; when exclusive, the picker is locked |
| Static secret max-versions settings | Default value and allowed range for `Maximum Versions` |

## Diagnosing a missing feature

1. **Which tab is missing?** Personal → check `passwordManagement`, `hidePersonalFolder` and the sign-in method. Corporate → check vault `secrets_allowed`.
2. **Reveal and copy gone?** `hide_secret_reveal_copy` is on. This is an account setting with no user toggle.
3. **No `Passkey Management` in Settings?** `allow_passkeys` is off, or the organization suppresses passkeys.
4. **Dark mode toggle gone?** Branding is active — see [Branding & Customization](https://docs.akeyless.io/docs/web-extension-branding).
5. **Protection key locked?** `account_default_key_name` is configured as exclusive.

## Where these are set

In the Akeyless console under account general settings and access roles, not in the extension. Users cannot override them.

## Related

- [Troubleshooting](https://docs.akeyless.io/docs/web-extension-troubleshooting)
- [Preconfigured Installs: Overview](https://docs.akeyless.io/docs/web-extension-preconfigured-install)
- [Extension Settings](https://docs.akeyless.io/docs/web-extension-settings)
