---
title: Preconfigured Package
---
<Callout icon="ℹ️" theme="info">
  **Audience: account administrators.**
</Callout>

Instead of sending a link, you can distribute a build of the extension with your settings already inside it — for managed deployment through MDM, group policy or an internal portal.

## How it works

The package contains a `preconfigured_install.json` file. **On first install only**, if that file has `"enabled": true`, its contents seed `akeyless_installation_preferences`.

## Guard rails

- A valid `preferredAuthMethod` is required.
- `prefillAccessId` is required unless the method is `email`.
- Nothing is applied if the extension already has an auth method or Access ID configured.

<Callout icon="⚠️" theme="warn">
  **First install only.** Updating an already-installed extension will not apply new settings. For an existing fleet, use a bridge link instead.
</Callout>

## File format

Both snake_case and camelCase keys are accepted.

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

## Building the package

Generate the file into a built extension directory, then package it:

```bash
node scripts/inject-prefill-install.mjs dist/chrome \
  --access-id=p-xxxxx \
  --auth=saml \
  --environment=global
```

```bash
npm run package:chrome
```

The result is `dist/akeyless-chrome-<version>.zip`.

### Available flags

| Flag | Purpose |
|---|---|
| `--access-id=` | Access ID to pre-fill |
| `--auth=` | `alias`, `saml`, `oidc`, `google`, `github`, `access-id`, `email` |
| `--environment=` | Region for email sign-in |
| `--config-id=` | Branding bundle ID |
| `--contact-support-url=` | Custom support destination |
| `--open-web-console-url=` | Custom web console destination |
| `--passkey-enabled=` | `true` or `false` |
| `--preconfigured-sign-in-title=` | Login info box heading |
| `--preconfigured-sign-in-message=` | Login info box body; use `\n\n` for paragraph breaks |

The same values can be supplied through environment variables — `AKEYLESS_PREFILL_ACCESS_ID`, `AKEYLESS_PREFILL_AUTH`, and so on.

## Verifying

Install the package into a clean browser profile and confirm the login screen shows your title, message and prefilled Access ID. A profile that already has the extension will not re-apply the file.

## Related

- [Preconfigured Installs: Overview](https://docs.akeyless.io/docs/web-extension-preconfigured-install)
- [Bridge Link Install](https://docs.akeyless.io/docs/web-extension-bridge-link)
- [Branding & Customization](https://docs.akeyless.io/docs/web-extension-branding)
