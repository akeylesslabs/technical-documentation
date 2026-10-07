---
title: Installation & Supported Browsers
---
Akeyless Password Manager 2.0 puts your Akeyless vault inside the browser — browse, search,
create and fill credentials without leaving the page you are on.

![The extension as a standalone popup window](https://files.readme.io/d0fa7939ef7be595616b44d6b963592018884d0d9b376723d98a150c8ad36142-extension-popup-window.png)
*The extension as a standalone popup window*

## Supported browsers

| Browser | Minimum version | Notes |
|---|---|---|
| **Google Chrome** | 88+ | Full feature set |
| **Microsoft Edge** | 88+ | Full feature set |
| **Mozilla Firefox** | 91.1+ | Sidebar instead of side panel |
| **Safari** | macOS 13.0+ | Distributed through the Mac App Store. Google and GitHub sign-in are not offered |

<Callout icon="ℹ️" theme="info">
  Akeyless Password Manager 2.0 is a **separate listing** from the original Akeyless Password
  Manager, which is still published. Use the links on this page rather than searching the
  store, so you land on the right extension.
</Callout>

---

## Three ways to install

| Method | Who uses it | What the user gets |
|---|---|---|
| **A — Browser store** | Individual users | The full sign-in screen, every authentication method |
| **B — Preconfigured link** | Admins rolling out to a team | A sign-in screen already set to the organization's method and Access ID |
| **C — Preconfigured package (MDM)** | Admins with managed devices | The same, with no link to click and no user action |


<Callout icon="⚠️" theme="warn">
  **Methods B and C are set up by Akeyless.** Preconfigured links and preconfigured package
  files are generated for your organization — they are not something you can create yourself
  from the extension or the console.

  **Contact Akeyless** (your account team, or
  [Akeyless support](https://www.akeyless.io/contact-support/)) to have a preconfigured link
  or an MDM package produced for your tenant. You will be asked for your authentication
  method, your Access ID, your region, and any branding you want applied.
</Callout>

---

## Method A — install from the browser store

### Google Chrome

1. Open [Akeyless Password Manager 2.0 on the Chrome Web Store](https://chromewebstore.google.com/detail/akeyless-password-manager/afmojeipcbpcfkdohnnjfkilfekoobmc).
2. Select **Add to Chrome**.
3. Review the requested permissions and select **Add extension**.
4. Select the puzzle-piece icon in the toolbar, then the pin beside Akeyless, so the icon stays visible.

### Microsoft Edge

1. Open [Akeyless Password Manager 2.0 on Edge Add-ons](https://microsoftedge.microsoft.com/addons/detail/akeyless-password-manager/fppjjcloabbllcakfjefmkdpbaaikeog).
2. Select **Get**, then **Add extension**.
3. Pin it from the toolbar's extensions menu.

### Mozilla Firefox

1. Open [Akeyless Password Manager 2.0 on Firefox Add-ons](https://addons.mozilla.org/en-US/firefox/addon/akeyless-password-manager-2-0/).
2. Select **Add to Firefox**, then **Add**.
3. Pin it to the toolbar.

<Callout icon="⚠️" theme="warn">
  **Firefox — check permissions after installing or updating.**

  1. Firefox menu → **Add-ons and Themes** → **Extensions**.
  2. Under **Enabled**, select the three dots beside Akeyless Password Manager 2.0.
  3. Choose **Manage** and confirm **Access your data for all websites** is switched on.

  Without it, autofill and Launch cannot reach the pages you visit.
</Callout>

### Safari (macOS)

1. Open [Akeyless Password Manager 2.0 on the Mac App Store](https://apps.apple.com/us/app/akeyless-password-manager-2-0/id6760562772).
2. Select **Get**, then install. The app is free, published by Akeyless Security Ltd.
3. Launch the app once — it installs the Safari extension.
4. In Safari: **Settings → Extensions**, tick **Akeyless Password Manager 2.0**.
5. Set its site access to **Allow on Every Website** so autofill and Launch can work.

<Callout icon="ℹ️" theme="info">
  **Safari differences.** Google and GitHub sign-in are not offered in the Safari build
  (macOS App Store guideline 4.8), and the sign-in screen defaults to **Email** rather than
  Alias. Safari also has no side panel or sidebar — the extension opens as a popup only.
</Callout>

---

## Method B — preconfigured link

Your administrator sends a link that carries your organization's sign-in settings. Open it and
the browser store page opens with the settings attached; install as normal and the extension
picks them up.

When you first open the extension, the sign-in screen is already set to your organization's
method, with the Access ID filled in and — if your organization configured one — a short
message of their own.

<Callout icon="⚠️" theme="warn">
  **The link expires after 10 minutes.** Install the extension straight after opening it. If
  you leave it and come back, ask for a new link rather than trying to reuse the old one.
</Callout>

**To obtain a link:** contact Akeyless. The link is generated per tenant and encodes your
organization's sign-in configuration.

Administrators: see [Bridge Link Install](https://docs.akeyless.io/docs/web-extension-bridge-link).

---

## Method C — preconfigured package for MDM

For managed fleets, your administrator distributes a build of the extension with the settings
already inside it, so nothing is clicked and nothing expires.

The package carries a `preconfigured_install.json` file. On **first install only**, if that
file has `"enabled": true`, its contents seed the extension's sign-in configuration.

```json
{
  "enabled": true,
  "prefillAccessId": "p-xxxxxxxxxxxx",
  "preferredAuthMethod": "saml",
  "allowedAuthMethods": ["saml"],
  "environment": "global",
  "config_id": "…",
  "contact_support_url": "https://support.example.com",
  "open_web_console_url": "https://console-pwm.akeyless.io",
  "passkey_enabled": true,
  "preconfigured_sign_in_title": "Ready to Sign In",
  "preconfigured_sign_in_message": "Use your corporate identity.\n\nContact IT if you need help.",
  "installationSource": "bundled_prefill"
}
```

### Deploying it

| Platform | How |
|---|---|
| **Chrome / Edge (Windows, macOS)** | Publish the packaged extension privately and deploy with `ExtensionInstallForcelist` via group policy or your MDM |
| **Firefox** | Deploy the signed XPI through `policies.json` or enterprise policy |
| **Safari (macOS)** | Distribute the container app through Apple Business Manager / your MDM |

<Callout icon="⚠️" theme="warn">
  **First install only.** Updating an extension that is already installed will not apply new
  settings, because the file is read once and never overwrites an existing configuration. For
  a fleet that already has the extension, use a preconfigured link instead.
</Callout>

**To obtain the package:** contact Akeyless. The `preconfigured_install.json` file and the
packaged extension are produced for your tenant and supplied to you for distribution.

Administrators: see [Preconfigured Package](https://docs.akeyless.io/docs/web-extension-preconfigured-package).

---

## Akeyless SA (Secrets Automation)

If your organization uses Akeyless Secrets Automation with Secure Remote Access, install
**Akeyless SA 2.0** instead — a separate extension with proxy and Zero Trust Portal support.

| Browser | Install |
|---|---|
| **Chrome** | [Akeyless SA 2.0](https://chromewebstore.google.com/detail/akeyless-sa-20/cdghndnnjccefelakphihcjngdokccpm) |
| **Edge** | [Akeyless SA 2.0](https://microsoftedge.microsoft.com/addons/detail/akeyless-sa-20/eplnolemlmkfhbmmafdnncdnapoijkgo) |
| **Firefox** | [Akeyless SA 2.0](https://addons.mozilla.org/en-US/firefox/addon/akeyless-sa-2-0/) |

Install one or the other, not both. See
[SA Web Extension (Secrets Automation)](https://docs.akeyless.io/docs/sra-web-extension-sa).

---

## After installing

Select the Akeyless icon in the toolbar to open the extension. To keep it beside the page
while you work, see
[Side Panel & Sidebar](https://docs.akeyless.io/docs/web-extension-side-panel).

Then: [Signing In to the Web Extension](https://docs.akeyless.io/docs/web-extension-sign-in).

## Related

- [Signing In to the Web Extension](https://docs.akeyless.io/docs/web-extension-sign-in)
- [Side Panel & Sidebar](https://docs.akeyless.io/docs/web-extension-side-panel)
- [Preconfigured Installs: Overview](https://docs.akeyless.io/docs/web-extension-preconfigured-install)
