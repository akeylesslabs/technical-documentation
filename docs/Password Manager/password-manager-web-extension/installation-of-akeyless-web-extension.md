---
title: Installation & Supported Browsers
---
Akeyless Password Manager 2.0 lets users browse, search, create, and fill credentials from their Akeyless vault in the browser.

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
  Akeyless Password Manager 2.0 has a **separate listing** from the original Akeyless Password
  Manager, which is still published. The store links on this page lead to the 2.0 extension.
</Callout>

---

## Three ways to install

| Method | Who uses it | What the user gets |
|---|---|---|
| **A — Browser store** | Individual users | The full sign-in screen, every authentication method |
| **B — Preconfigured link** | Admins rolling out to a team | A sign-in screen already set to the organization's method and Access ID |
| **C — Preconfigured package (MDM)** | Admins with managed devices | The same, with no link to click and no user action |


<Callout icon="⚠️" theme="warn">
  **Methods B and C are set up by Akeyless.** Akeyless generates preconfigured links and
  package files for each organization. Neither can be created from the extension or the console.

  An administrator can request a preconfigured link or MDM package from the Akeyless account team
  or [Akeyless support](https://www.akeyless.io/contact-support/). Akeyless requires the
  organization's authentication method, Access ID, region, and any requested branding.
</Callout>

---

## Method A — install from the browser store

### Google Chrome

1. The user opens [Akeyless Password Manager 2.0 on the Chrome Web Store](https://chromewebstore.google.com/detail/akeyless-password-manager/afmojeipcbpcfkdohnnjfkilfekoobmc).
2. The user selects **Add to Chrome**.
3. The user reviews the requested permissions and selects **Add extension**.
4. The user selects the puzzle-piece icon in the toolbar, then the pin beside Akeyless, to keep the icon visible.

### Microsoft Edge

1. The user opens [Akeyless Password Manager 2.0 on Edge Add-ons](https://microsoftedge.microsoft.com/addons/detail/akeyless-password-manager/fppjjcloabbllcakfjefmkdpbaaikeog).
2. The user selects **Get**, then **Add extension**.
3. The user pins the extension from the toolbar's extensions menu.

### Mozilla Firefox

1. The user opens [Akeyless Password Manager 2.0 on Firefox Add-ons](https://addons.mozilla.org/en-US/firefox/addon/akeyless-password-manager-2-0/).
2. The user selects **Add to Firefox**, then **Add**.
3. The user pins the extension to the toolbar.

<Callout icon="⚠️" theme="warn">
  **Firefox permissions after installation or update.**

  1. The user opens the Firefox menu → **Add-ons and Themes** → **Extensions**.
  2. Under **Enabled**, the user selects the three dots beside Akeyless Password Manager 2.0.
  3. The user selects **Manage** and confirms **Access your data for all websites** is switched on.

  Without this permission, autofill and Launch cannot reach visited pages.
</Callout>

### Safari (macOS)

1. The user opens [Akeyless Password Manager 2.0 on the Mac App Store](https://apps.apple.com/us/app/akeyless-password-manager-2-0/id6760562772).
2. The user selects **Get** and installs the app. The app is free and published by Akeyless Security Ltd.
3. The user launches the app once to install the Safari extension.
4. In Safari, the user opens **Settings → Extensions** and enables **Akeyless Password Manager 2.0**.
5. The user sets site access to **Allow on Every Website** so autofill and Launch can work.

<Callout icon="ℹ️" theme="info">
  **Safari differences.** Google and GitHub sign-in are not offered in the Safari build
  (macOS App Store guideline 4.8), and the sign-in screen defaults to **Email** rather than
  Alias. Safari also has no side panel or sidebar — the extension opens as a popup only.
</Callout>

---

## Method B — preconfigured link

An administrator sends users a link containing the organization's sign-in settings. Opening the
link takes a user to the browser store page with those settings attached. The extension picks
up the settings when the user installs it.

On first opening the extension, the user sees the organization's sign-in method and a filled-in
Access ID. The sign-in screen also displays a short message if the organization configured one.

<Callout icon="⚠️" theme="warn">
  **The link expires after 10 minutes.** Users must install the extension immediately after
  opening the link. If it expires, the administrator must request a new link.
</Callout>

An administrator can contact Akeyless to obtain a link. Akeyless generates the link per tenant
with the organization's sign-in configuration.

[Bridge Link Install](https://docs.akeyless.io/docs/web-extension-bridge-link) provides instructions for administrators.

---

## Method C — preconfigured package for MDM

For managed fleets, an administrator distributes a build of the extension with settings already
inside it. Users do not need to open a link, and the configuration does not expire.

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
  "preconfigured_sign_in_message": "Sign in with corporate credentials.\n\nContact IT for help.",
  "installationSource": "bundled_prefill"
}
```

### Deploying it

| Platform | How |
|---|---|
| **Chrome / Edge (Windows, macOS)** | The administrator publishes the packaged extension privately and deploys it with `ExtensionInstallForcelist` via group policy or MDM |
| **Firefox** | The administrator deploys the signed XPI through `policies.json` or enterprise policy |
| **Safari (macOS)** | The administrator distributes the container app through Apple Business Manager or MDM |

<Callout icon="⚠️" theme="warn">
  **First install only.** Updating an extension that is already installed will not apply new
  settings, because the file is read once and never overwrites an existing configuration. For
  a fleet that already has the extension, administrators can use a preconfigured link instead.
</Callout>

An administrator can contact Akeyless to obtain the package. Akeyless produces the
`preconfigured_install.json` file and packaged extension for the tenant and supplies them for distribution.

[Preconfigured Package](https://docs.akeyless.io/docs/web-extension-preconfigured-package) provides instructions for administrators.

---

## Akeyless SA (Secrets Automation)

Organizations using Akeyless Secrets Automation with Secure Remote Access need **Akeyless SA 2.0**
instead. This separate extension supports proxy and Zero Trust Portal features.

| Browser | Install |
|---|---|
| **Chrome** | [Akeyless SA 2.0](https://chromewebstore.google.com/detail/akeyless-sa-20/cdghndnnjccefelakphihcjngdokccpm) |
| **Edge** | [Akeyless SA 2.0](https://microsoftedge.microsoft.com/addons/detail/akeyless-sa-20/eplnolemlmkfhbmmafdnncdnapoijkgo) |
| **Firefox** | [Akeyless SA 2.0](https://addons.mozilla.org/en-US/firefox/addon/akeyless-sa-2-0/) |

Users should install only one of the two extensions. The
[SA Web Extension (Secrets Automation)](https://docs.akeyless.io/docs/sra-web-extension-sa) page provides more information.

---

## After installing

The user selects the Akeyless icon in the toolbar to open the extension. The
[Side Panel & Sidebar](https://docs.akeyless.io/docs/web-extension-side-panel) page explains how to keep the extension beside the current page.

[Signing In to the Web Extension](https://docs.akeyless.io/docs/web-extension-sign-in) covers the next step.

## Related

- [Signing In to the Web Extension](https://docs.akeyless.io/docs/web-extension-sign-in)
- [Side Panel & Sidebar](https://docs.akeyless.io/docs/web-extension-side-panel)
- [Preconfigured Installs: Overview](https://docs.akeyless.io/docs/web-extension-preconfigured-install)