---
title: Adding and Using One-Time Passwords
---
A password item can carry an OTP authenticator, so the extension generates your six-digit codes alongside the password.

## Adding an authenticator

Open the create or edit overlay for a password item and find the **Authenticator (OTP)** section. There are two ways to add one:

| Method | How |
|---|---|
| **Scan from the page** | Select **Scan otpauth QR from the current website tab**. The extension looks for a visible QR code on the page you have open and reads the `otpauth://` URI from it. |
| **Paste the secret** | See [Adding Manual OTP](https://docs.akeyless.io/docs/adding-manual-otp). |

Give the authenticator a label, such as *GitHub*, so you can tell it apart.

### When scanning is unavailable

QR scanning reads the page you currently have open. It does not work on browser-internal pages — `chrome://`, `edge://` or extension pages. Open the site's own two-factor setup page first.

## Using a code

| Where | How |
|---|---|
| **Item preview** | The current code is shown with a copy control |
| **In-page popup** | Select the Akeyless icon in the OTP field and choose the credential — the code is filled for you |
| [Launch](https://docs.akeyless.io/docs/web-extension-launch) | Codes are filled automatically as part of the sign-in flow |

## Security Health

Items carrying an authenticator are counted in the **OTP** metric on the Security Health screen. The count is reported but does not change your protection score.

## Related

- [Adding Manual OTP](https://docs.akeyless.io/docs/adding-manual-otp)
- [Creating New Password](https://docs.akeyless.io/docs/creating-new-password-1)
- [Security Health in the Extension](https://docs.akeyless.io/docs/web-extension-security-health)
