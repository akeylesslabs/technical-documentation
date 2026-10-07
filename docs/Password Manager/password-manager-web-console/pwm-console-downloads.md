---
title: 'Downloads: Extension and Desktop App'
---
The console hosts a downloads page for the Akeyless browser extension and the desktop
application, with the full release history for each.

## Where it is

| Item | Address |
|---|---|
| **Downloads page** | [https://console-pwm.akeyless.io/artifacts](https://console-pwm.akeyless.io/artifacts) |
| **The console itself** | [https://console-pwm.akeyless.io](https://console-pwm.akeyless.io) — sign in here |
| **On a dedicated tenant** | `/artifacts` on your own console address |
| **From the sign-in screen** | There is a link to it, so you can get builds before you have an account |
| **Back** | **← Back to sign in** returns you to the console |

<Callout icon="ℹ️" theme="info">
  **No sign-in required.** The downloads page is reachable without an account, so you can send
  the link to someone who is setting up for the first time, or to IT for a managed rollout.
</Callout>

Two tabs: **Web Extension** and **Desktop app**.

---

## Web Extension

![The Web Extension downloads tab](https://files.readme.io/e85e0ca49fe376395dc99bdf80c7c6dc4e4674518933a46867fa9ff465658a33-downloads-web-extension.webp)
*Release history on the left, downloads for the selected release on the right*

Expand a version on the left to preview it; its downloads appear on the right.

Each release shows the date, the version, a one-line summary, and a **What changed** list.

### Per browser

| Browser | Builds offered |
|---|---|
| **Chrome** | Password Manager, Secure Access |
| **Microsoft Edge** | Password Manager, Secure Access |
| **Mozilla Firefox** | Password Manager, Secure Access |
| **Safari** | Password Manager |

<Callout icon="ℹ️" theme="info">
  **Password Manager** and **Secure Access** are different products built from the same
  codebase. Secure Access adds proxy routing and Zero Trust Portal launch. Install the one
  your organization uses — not both, or two extensions compete to fill the same login forms.
</Callout>

---

## Desktop app

![The desktop app downloads tab](https://files.readme.io/351972db63d9eaf40c959a966353abaa7390611a697baa0a7d097c02f93414a2-downloads-desktop-app.webp)
*Desktop builds, with macOS and Windows downloads*

| Platform | Build |
|---|---|
| **macOS** | Apple Silicon |
| **Windows** | x64 |

The release list works the same way: expand a version to see its changes and download links.

### Or install from an app store

| Platform | Store |
|---|---|
| **macOS** | [Akeyless PWM Desktop App](https://apps.apple.com/us/app/akeyless-pwm-desktop-app/id6766774323?mt=12) |
| **Windows** | [Akeyless PWM Desktop App](https://apps.microsoft.com/detail/9pbghb5vx6bm) |

Store installs update themselves. Use this page instead when you need a specific version.

<Callout icon="⚠️" theme="warn">
  Akeyless also publishes an **SRA Desktop App** for Secure Remote Access — a different
  product. Check the listing says **PWM**.
</Callout>

---

## Why older versions are listed

The history is kept so you can:

- **Pin a known-good version** while a regression is investigated
- **Roll back** if a release causes a problem in your environment
- **Check what changed** between the version your users are on and the current one

The newest release carries a **LATEST** badge.

## Which version am I running?

[Settings](https://docs.akeyless.io/docs/pwm-console-settings) shows the extension's `Installed version` when the
console can detect it, alongside the console's own version in the footer.

## Related

- [Settings](https://docs.akeyless.io/docs/pwm-console-settings)
- [Password Manager Web Extension](https://docs.akeyless.io/docs/password-manager-web-extension)
