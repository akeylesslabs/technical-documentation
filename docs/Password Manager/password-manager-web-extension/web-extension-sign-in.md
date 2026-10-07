---
title: Signing In to the Web Extension
---
The extension supports seven authentication methods. Which ones you see depends on what your
organization allows.

![Choosing an authentication method](images/login-auth-method-picker.png)
*Choosing an authentication method*

---

## Authentication methods

| Method | What you enter |
|---|---|
| **Login with Alias** | Your alias, typically containing a `/` such as `team/you`. Default on Chrome, Edge and Firefox. |
| **Login with SAML** | Your **Access ID**. Your identity provider opens in a new tab. |
| **Login with OIDC** | Your **Access ID**. Your OIDC provider opens in a new tab. |
| **Login with Gmail** | Nothing — Google OAuth starts immediately. *Not available on Safari.* |
| **Login with GitHub** | Nothing — GitHub OAuth starts immediately. *Not available on Safari.* |
| **Login with Access ID** | **Access ID** and **Access Key**. |
| **Login with Email** | Email address and password, with optional account selection and 2FA. Default on Safari. |

![SAML sign-in with the Access ID filled](images/login-saml-access-id.png)
*SAML sign-in with the Access ID filled*

<Callout icon="ℹ️" theme="info">
  **Where do I find my Access ID?**
  Contact your account administrator. If your organization used a bridge link or a
  preconfigured package, it is filled in for you.
</Callout>

---

## Email sign-in

1. **Email** — enter your address and select **Continue**.
2. **Account** — if your address belongs to more than one Akeyless account, choose the
   account ID and select **Continue**.
3. **Password** — enter your password and select **Sign In**.
4. **Two-factor** — if your account requires MFA, enter the code emailed to you. A resend
   option appears after a short cooldown.

### Regions

Email sign-in needs the right region: **global**, **us**, **eu**, **wmt**, **dbk** or **cvs**.
Choose it next to the email field. If your install was preconfigured with a region, the picker
is hidden and that region is used.

For Alias, SAML, OIDC and Access ID sign-in the region is derived from the Access ID itself —
there is nothing to choose.

---

## Sign-in conveniences

- **Access ID history** — select the Access ID field to pick from your 10 most recently used
  IDs for that method.
- **Last used method** — the extension reopens on the method you used last.
- **Show password** — the eye icon. Hidden when your account enforces secure-paste mode.
- **Open Web Console** — opens the Akeyless web console for your tenant.
- Dark mode survives sign-out.

---

## DBK tenants

On DBK tenants a one-time machine-to-machine disclaimer appears before your first sign-in.
Acknowledge it once and it is remembered.

---

## Session expiry

The extension signs you out when your session token expires. Token lifetime is set by your
account's authentication method — contact your administrator to change it.

## Related

- [Installation & Supported Browsers](https://docs.akeyless.io/docs/installation-of-akeyless-web-extension)
- [Preconfigured Installs: Overview](https://docs.akeyless.io/docs/web-extension-preconfigured-install)
- [Troubleshooting](https://docs.akeyless.io/docs/web-extension-troubleshooting)
