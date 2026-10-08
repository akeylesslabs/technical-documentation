---
title: 'Preconfigured Installs: Overview'
---
<Callout icon="ℹ️" theme="info">
  **Audience: account administrators.**
</Callout>

A preconfigured install ships your organization's sign-in settings with the extension, so your users open it to a login screen that is already correct — right method, right Access ID, right region, right branding.

## One destination, four paths

Every path writes to the same place: a browser-storage record named `akeyless_installation_preferences`. The login screen reads it every time it opens.

| Path | Use when | Page |
|---|---|---|
| **Bridge link** | You can send users a link | [Bridge Link Install](https://docs.akeyless.io/docs/web-extension-bridge-link) |
| **Store URL parameters** | You link to the store from a portal | [Bridge Link Install](https://docs.akeyless.io/docs/web-extension-bridge-link) |
| **Cookiebridge URL** | You use the hosted bridge service | [Bridge Link Install](https://docs.akeyless.io/docs/web-extension-bridge-link) |
| **Preconfigured package** | You distribute the extension yourself | [Preconfigured Package](https://docs.akeyless.io/docs/web-extension-preconfigured-package) |

<Callout icon="⚠️" theme="warn">
  Know which path you used before troubleshooting. The bridge link **expires after 10 minutes**; the package applies on **first install only**. The symptoms look identical, the causes are not.
</Callout>

## The preconfigured fields

| Field | Effect |
|---|---|
| `preferredAuthMethod` | Which method the login screen opens on: `alias`, `saml`, `oidc`, `google`, `github`, `access-id`, `email` |
| `allowedAuthMethods` | Restricts the picker to these methods |
| `prefillAccessId` | Pre-fills the Access ID field |
| `prefillAlias` | Pre-fills the field when the method is Alias |
| `environment` | Region for email sign-in: `global`, `us`, `eu`, `wmt`, `dbk`, `cvs` |
| `config_id` | ID of a stored branding bundle |
| `contactSupportUrl` | Destination of **Contact Support** |
| `privacyPolicyUrl` | Destination of **Privacy Policy** |
| `openWebConsoleUrl` | Destination of **Open Web Console** |
| `passkeyEnabled` | Initial state of `Passkey Management` |
| `preconfiguredSignInTitle` | Heading of the login info box. Default *"Ready to Sign In"*. Max 120 characters |
| `preconfiguredSignInMessage` | Body of that box. Blank lines separate paragraphs. Max 2000 characters |
| `installationSource` | Records which path delivered the settings |

Branding fields may accompany them: `sidebarBgColor`, `buttonColor`, `mainBgColor`, `iconColor`, `loadingColor`, `logoUrl`, `brandFolder`. See [Branding & Customization](https://docs.akeyless.io/docs/web-extension-branding).

## What your users will see

| Configuration | Login screen |
|---|---|
| **One allowed method**, not email | No auth picker, no Access ID field. Your title and message, and a single sign-in button. *Powered by Akeyless* at the bottom |
| **One allowed method**, email | Email, password and 2FA only — no auth picker, no region picker |
| **Several allowed methods** | Picker limited to those methods, opened on the preferred one, Access ID pre-filled |

## Defaults

If you set no support or privacy URL, the extension uses:

- `https://www.akeyless.io/contact-support/`
- `https://www.akeyless.com/privacy-policy/`

## Related

- [Bridge Link Install](https://docs.akeyless.io/docs/web-extension-bridge-link)
- [Preconfigured Package](https://docs.akeyless.io/docs/web-extension-preconfigured-package)
- [Branding & Customization](https://docs.akeyless.io/docs/web-extension-branding)
