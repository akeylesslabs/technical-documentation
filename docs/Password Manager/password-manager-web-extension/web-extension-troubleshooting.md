---
title: Troubleshooting
---
## The login screen shows the wrong organization, or no preconfigured settings

Bridge-link data **expires 10 minutes** after it is generated. Ask your administrator for a fresh link and install the extension promptly.

Preconfigured package settings apply on **first install only** and never overwrite an existing configuration. On a browser profile that already had the extension, use a bridge link instead.

## Autofill offers nothing on a site

- Confirm `Autofill` is on in **Settings**.
- Confirm you are signed in.
- Confirm the item has a `Website URL` matching the site — matching is by domain.

## Launch opens the site but does not sign in

- Confirm the item has **both** a username and a password.
- Confirm the URL points at the actual login page, not a landing page.
- Multi-step forms need the page to settle between steps.
- Launch runs only on allowed domains.

## Passkeys do not appear

- `Passkey Management` must be on in **Settings**.
- Your account must allow passkeys.
- Passkeys are stored in the **personal folder only** — they are invisible if the personal vault is hidden for your session.

## A share link was lost

Share links are shown **once**. Generate a new one.

## Security Health shows nothing

It covers **personal items only**. Save passwords or passkeys to your personal folder to populate the metrics.

## A tab is missing

Almost always account policy or vault permissions rather than a fault. See [Account Policies Affecting the Extension](https://docs.akeyless.io/docs/web-extension-account-policies).

## The session keeps expiring

Token lifetime is set by your account's authentication method. Contact your account administrator.

## An import dropped rows

Check the **import summary** shown after upload — it reports what was skipped. Common causes: a non-UTF-8 encoding the importer could not decode, and missing required columns. See [CSV Password Importer](https://docs.akeyless.io/docs/csv-password-importer).

## Export Passwords is greyed out, or skipped items

Greyed out means your account has no Personal area, which is set by account policy. See [Account Policies Affecting the Extension](https://docs.akeyless.io/docs/web-extension-account-policies). Skipped items usually have an empty password field. See [Exporting Your Passwords](https://docs.akeyless.io/docs/web-extension-export-passwords).

## The extension turned off after an update

Version 1.30.130 added the browser's downloads permission, used by **Export Passwords**. Chrome and Edge turn an extension off until you approve a newly requested permission. Open the browser's extensions page and approve it to turn the extension back on. Firefox instead holds the update and asks from its menu, and the previous version keeps working until you accept.

## Still stuck

Use **Settings** → **Contact Support**, which points at your organization's support channel when configured.

## Related

- [Account Policies Affecting the Extension](https://docs.akeyless.io/docs/web-extension-account-policies)
- [Installation & Supported Browsers](https://docs.akeyless.io/docs/installation-of-akeyless-web-extension)
- [Signing In to the Web Extension](https://docs.akeyless.io/docs/web-extension-sign-in)
