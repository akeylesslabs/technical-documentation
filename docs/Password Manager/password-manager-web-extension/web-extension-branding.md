---
title: Branding & Customization
---
<Callout icon="ℹ️" theme="info">
  **Audience: account administrators.**
</Callout>

The extension can carry your organization's identity.

## What you can change

| Field | Effect | Default |
|---|---|---|
| `logoUrl` | Logo on the login screen and sidebar | Akeyless logo |
| `brandFolder` | Bundled icon set | `akeyless_brand_icons` |
| `sidebarBgColor` | Left rail background | `#eef0f0` |
| `mainBgColor` | Main panel background | `#eef0f0` |
| `buttonColor` | Primary buttons | `#2563eb` |
| `iconColor` | Accent icons, including the in-page field icon | `#6cd7c4` |
| `loadingColor` | Loading animation | `#63d6c1` |
| `poweredByColor` | *Powered by Akeyless* text | — |
| `preconfiguredSignInTitle` | Login info box heading | *Ready to Sign In* |
| `preconfiguredSignInMessage` | Login info box body | — |
| `contactSupportUrl` | **Contact Support** destination | Akeyless support |
| `privacyPolicyUrl` | **Privacy Policy** destination | Akeyless policy |
| `openWebConsoleUrl` | **Open Web Console** destination | Derived from tenant |
| `consentMessage` | Consent copy | — |

## Delivery

Either inline through the bridge link or URL parameters, or by `config_id` — an ID the extension resolves to a stored branding bundle and refreshes on demand.

Use `config_id` when you expect branding to change. Changing the bundle updates every installed extension without re-issuing links.

## Dark mode

<Callout icon="ℹ️" theme="info">
  **When branding is active, dark mode is locked to light and the toggle is hidden**, so your palette renders as intended.
</Callout>

If you want users to keep dark mode, do not set branding colours.

## Logo requirements

`logoUrl` must be `https://` on `*.akeyless.io` or the trusted Google Cloud Storage bucket. Other domains, `data:` URIs and `javascript:` are rejected and the default logo is used instead.

Host your logo on an approved domain, or ask Akeyless to add it to the brand assets bucket.

## Related

- [Preconfigured Installs: Overview](https://docs.akeyless.io/docs/web-extension-preconfigured-install)
- [Account Policies Affecting the Extension](https://docs.akeyless.io/docs/web-extension-account-policies)
