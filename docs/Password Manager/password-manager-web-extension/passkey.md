---
title: Passkey
---
With `Passkey Management` enabled, the extension acts as your WebAuthn authenticator and stores passkeys in your Akeyless vault — so they are available on every machine where you sign in, not stored on one device only.

Turn it on in **Settings** → `Passkey Management`. It is off by default.

## Registering a passkey

When a site offers to create a passkey, the extension intercepts the WebAuthn call and stores the credential in your vault as a **passkey item**.

## Signing in with a passkey

On a return visit, the extension supplies the passkey. Passkeys are matched to the site by its relying-party domain.

## Verifying it's you

With **Verify it's me before using passkeys** on (Settings, under `Passkey Management`), the extension asks you to confirm it's you before it creates or uses a passkey. A small Akeyless window opens and your computer shows its own prompt.

| Method | What you use |
|---|---|
| **This computer's verification** (recommended) | Touch ID, Windows Hello face or fingerprint, or your computer password or PIN |
| **Akeyless PIN** (backup) | A 6–12 digit PIN you create once, for computers without built-in verification |

- **First use:** you choose the method once per computer and browser.
- **Every time:** you verify each time a passkey is created or used, the same as Apple Passwords and Google Password Manager.
- **Wrong PIN:** after 5 wrong attempts the PIN is locked for 5 minutes.
- **The site is told the truth:** the passkey's "user verified" (UV) flag is set only after a real check. Sites that require verification (for example Microsoft Entra) accept the passkey only when this is on.
- **Sites that don't want verification** (`userVerification: "discouraged"`) are never prompted.
- **Your administrator** can turn it on, or require it, through the configuration file or the bridge link (`passkeyVerification` / `passkey_verification`: `off`, `on` or `required`). When it's required, the toggle is locked on.
- **Reset** next to the toggle clears the saved method; you choose again on next use.
- **Chrome and Edge:** while your computer's prompt is shown, the site's request is paused and then sent again automatically, so the site just sees the passkey. If a site reports "aborted" right after you install or update the extension, reload that page once.

## Passkey provider ID (AAGUID)

From version 1.30.155, passkeys the extension creates identify Akeyless as their provider with
the AAGUID `e5d70961-485b-4877-9428-f381d298e958`. Sites and identity providers that list or
restrict passkey providers by AAGUID, such as Microsoft Entra, show these passkeys as coming from
Akeyless, and administrators can allow this AAGUID. Passkeys created earlier carry an empty
AAGUID ("Not available yet" in Entra) but keep working.

## Where passkeys live

<Callout icon="⚠️" theme="warn">
  **Passkeys are stored in the personal folder only** — never in team or corporate vaults.
</Callout>

This means passkeys are invisible if the personal vault is hidden for your session. See [Account Policies Affecting the Extension](https://docs.akeyless.io/docs/web-extension-account-policies).

## Finding your passkeys

Passkeys appear in your item lists with their own icon, and under the ***Passkey*** type in the filter panel.

Opening one shows the relying party, the user handle, the creation date and the protection key.

## Security Health

Passkeys are counted in the **Passkeys** metric. The count is reported but does not change your protection score.

## When the toggle is missing

Two policies can remove passkey support:

| Policy | Effect |
|---|---|
| Account setting `allow_passkeys` disabled | Passkey management is unavailable |
| Organization suppresses passkeys (DBK tenants) | Passkeys are hidden from lists, filters and Settings entirely |

## Related

- [Extension Settings](https://docs.akeyless.io/docs/web-extension-settings)
- [Account Policies Affecting the Extension](https://docs.akeyless.io/docs/web-extension-account-policies)
- [Security Health in the Extension](https://docs.akeyless.io/docs/web-extension-security-health)
