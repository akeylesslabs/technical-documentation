---
title: SA Web Extension (Secrets Automation)
---
**Akeyless SA 2.0** is a separate extension built from the same codebase as Akeyless Password Manager 2.0, adding Secure Remote Access capabilities.

## Download

| Browser | Install |
|---|---|
| **Google Chrome** | [Add to Chrome](https://chromewebstore.google.com/detail/akeyless-sa-20/cdghndnnjccefelakphihcjngdokccpm) |
| **Microsoft Edge** | [Get from Edge Add-ons](https://microsoftedge.microsoft.com/addons/detail/akeyless-sa-20/eplnolemlmkfhbmmafdnncdnapoijkgo) |
| **Mozilla Firefox** | [Add to Firefox](https://addons.mozilla.org/en-US/firefox/addon/akeyless-sa-2-0/) |
| **Safari** | Coming soon |

<Callout icon="ℹ️" theme="info">
  This is a **different extension** from Akeyless Password Manager 2.0. Install the one your organization uses — not both.
</Callout>

## What it adds

### Zero Trust Portal (ZTP) launch

Opens a target application through the Akeyless proxy, resolving credentials from the vault and filling them on arrival. Supports private and incognito windows, and proxy-based routing.

### SRA clipboard

Clipboard support for remote-access sessions, driven by a server-sent-event channel from the SRA worker.

### Flow audit log and support diagnostics

A structured record of each launch — inject, authentication, secret resolution — that can be copied and sent to support, with an option to upload diagnostics directly.

### Verbose logging

On by default in SA builds, giving operators visibility into the launch pipeline.

## Permissions

SA builds request additional browser permissions beyond the Password Manager build — proxy, webRequest, clipboardRead, webNavigation and management — and broader host access, because they route traffic through the Akeyless proxy.

## Shared features

Everything in the Password Manager documentation applies: vault browsing, item creation, autofill, sharing, import, passkeys and settings. See **Password Manager → Password Manager Web Extension**.

## Related

- [Installation & Supported Browsers](https://docs.akeyless.io/docs/installation-of-akeyless-web-extension)
- [Launch: Open a Site Already Signed In](https://docs.akeyless.io/docs/web-extension-launch)
