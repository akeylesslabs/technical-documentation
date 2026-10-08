---
title: Adding Manual OTP
---
Use this when you cannot scan a QR code — the site shows the secret as text, you set up two-factor on another device, or you are working from a recovery sheet.

## Steps

1. Open the password item for editing.
2. Find the **Authenticator (OTP)** section.
3. Select the paste option — *Paste Base32 secret only*.
4. Paste the secret into **Paste your secret**.
5. Enter a label, such as *GitHub*.
6. Save.

## What to paste

Paste **only the Base32 secret** — the block of letters and digits the site shows beside or beneath the QR code, often labelled "setup key", "manual entry key" or "secret key".

Do not paste the whole `otpauth://` URI into this field, and do not include spaces the site may have added for readability.

## Verifying

After saving, open the item and compare the code shown against the one the site expects. If they do not match:

- confirm you copied the full secret
- confirm you pasted the secret rather than a recovery code
- confirm your computer's clock is correct — TOTP codes are time-based, and a clock more than a minute out produces wrong codes

## Related

- [Adding and Using One-Time Passwords](https://docs.akeyless.io/docs/adding-and-using-otp-1)
- [Creating New Password](https://docs.akeyless.io/docs/creating-new-password-1)
