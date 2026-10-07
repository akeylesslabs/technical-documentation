---
title: Passkey
---
With **Passkey Management** enabled, the extension acts as your WebAuthn authenticator and stores passkeys in your Akeyless vault — so they follow you between machines instead of being locked to one device.

Turn it on in **Settings → Passkey Management**. It is off by default.

## Registering a passkey

When a site offers to create a passkey, the extension intercepts the WebAuthn call and stores the credential in your vault as a **passkey item**.

## Signing in with a passkey

On a return visit, the extension supplies the passkey. Passkeys are matched to the site by its relying-party domain.

## Where passkeys live

<Callout icon="⚠️" theme="warn">
  **Passkeys are stored in the personal folder only** — never in team or corporate vaults.
</Callout>

This means passkeys are invisible if the personal vault is hidden for your session. See [Account Policies Affecting the Extension](https://docs.akeyless.io/docs/web-extension-account-policies).

## Finding your passkeys

Passkeys appear in your item lists with their own icon, and under the ***Passkey*** type in the filter panel.

Opening one shows the relying party, the user handle, the creation date and the Protection Key.

## Security Health

Passkeys are counted in the **Passkeys** metric. The count is reported but does not change your protection score.

## When the toggle is missing

Two policies can remove passkey support:

| Policy | Effect |
|---|---|
| Account **allow passkeys** disabled | Passkey Management is unavailable |
| Organization suppresses passkeys (DBK tenants) | Passkeys are hidden from lists, filters and Settings entirely |

## Related

- [Extension Settings](https://docs.akeyless.io/docs/web-extension-settings)
- [Account Policies Affecting the Extension](https://docs.akeyless.io/docs/web-extension-account-policies)
- [Security Health in the Extension](https://docs.akeyless.io/docs/web-extension-security-health)
