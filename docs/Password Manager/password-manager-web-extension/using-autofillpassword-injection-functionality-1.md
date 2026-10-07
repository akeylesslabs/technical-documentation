---
title: Using Autofill / Password Injection
---
With **Autofill** enabled in Settings, the extension offers your vault credentials directly on the pages where you need them.

## The suggestion popup

Select a username, email, password or OTP field and a small Akeyless icon appears inside it. Select the icon to open a popup listing the vault credentials whose **Website URLs** match the current domain.

Choose one and the extension fills the form.

## What the popup can do

| Action | Where it appears |
|---|---|
| **Fill a credential** | Any matching login form |
| **Generate a strong password** | Signup and password-change forms |
| **Fill a one-time code** | When the item has an OTP authenticator configured |
| Launch | Opens the site and signs in — see [Launch](https://docs.akeyless.io/docs/web-extension-launch) |

## Matching

Credentials are matched to the page by domain, using the **Website URLs** on the item. If a credential does not appear, confirm the item has a URL for that site.

## Decoy fields

Some sites plant hidden fields to catch automated form fillers. The extension detects and skips them, so your credentials are not written into a trap field.

## Turning it off

Autofill follows your account's default on first sign-in. Changing the toggle in **Settings** overrides the account default from then on, on that browser.

## Related

- [Launch: Open a Site Already Signed In](https://docs.akeyless.io/docs/web-extension-launch)
- [Prompt to save password](https://docs.akeyless.io/docs/web-extension-save-prompt)
- [Extension Settings](https://docs.akeyless.io/docs/web-extension-settings)
