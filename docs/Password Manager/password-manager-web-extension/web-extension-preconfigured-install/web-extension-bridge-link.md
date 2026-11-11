---
title: Bridge Link Install
---
<Callout icon="ℹ️" theme="info">
  **Audience: account administrators.**
</Callout>

Three link-based ways to deliver your organization's sign-in settings to a user's extension. All three write to `akeyless_installation_preferences` — see [Preconfigured Installs: Overview](https://docs.akeyless.io/docs/web-extension-preconfigured-install).

---

## Path A — localhost bridge

Your portal opens a local bridge page, which writes the settings into page storage and then redirects the user to the browser store. The extension reads them from any `localhost` or `127.0.0.1` page.

### Keys the bridge page sets

```
akeyless_bridge_access_id            (or akeyless_bridge_account_id)
akeyless_bridge_auth_method
akeyless_bridge_timestamp
akeyless_bridge_environment
akeyless_bridge_contact_support_url
akeyless_bridge_privacy_policy_url
akeyless_bridge_passkey_enabled
akeyless_bridge_passkey_verification      (off | on | required — can only make verification stricter)
akeyless_bridge_preconfigured_sign_in_title
akeyless_bridge_preconfigured_sign_in_message
```

### Rules

- **Access ID, auth method and timestamp are all required.** If any is missing, nothing is stored.
- **The data expires after 10 minutes.** Past that, the extension ignores it.
- New values are **merged** into existing preferences.

<Callout icon="ℹ️" theme="info">
  The expiry is the single most common cause of "the link did not work". Tell users to install the extension immediately after opening the link, and re-issue rather than debug.
</Callout>

---

## Path B — cookiebridge redirect URL

The hosted bridge service can carry settings as query parameters. The extension reads `id`, `contact_support_url`, `privacy_policy_url`, `passkey_enabled`, `passkey_verification`, and the sign-in title and message.

---

## Path C — browser store URL parameters

The same parameters can ride on the store page URL. The extension reads them on Chrome Web Store, Edge Add-ons and Firefox Add-ons pages.

```
?access_id=<id>           or  ?account_id=<id>
?auth_method=<method>     or  ?auth=<method>     (also accepted in the URL #hash)
?environment=<region>
?contact_support_url=…   ?privacy_policy_url=…   ?passkey_enabled=…   ?passkey_verification=…
?preconfigured_sign_in_title=…   ?preconfigured_sign_in_message=…
```

### Combined encoding

The Access ID may carry the method in front of it:

```
?access_id=saml:p-xxxxxxxx
```

### When settings are stored

Either **auth method + Access ID**, or **auth = email + a valid environment**. Anything less is ignored.

---

## Validation applied to every path

Because these values arrive from a web page or a URL, they are validated before being stored:

| Value | Rule |
|---|---|
| `auth_method` | Must be one of the seven known methods; anything else is discarded |
| Sign-in title and message | Control characters stripped, length capped |
| Support, privacy and console URLs | Must be safe `https://` URLs |

If a value you set does not appear, check it against this table first.

## Related

- [Preconfigured Installs: Overview](https://docs.akeyless.io/docs/web-extension-preconfigured-install)
- [Preconfigured Package](https://docs.akeyless.io/docs/web-extension-preconfigured-package)
