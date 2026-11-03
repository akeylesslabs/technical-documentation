---
title: 'One-Time Passwords: Scanning a QR Code'
---
A password item can hold an authenticator, so the app shows your six-digit two-factor codes
right next to the password. On your phone you add one by pointing the camera at the QR code a
website shows when you turn on two-factor authentication.

## Adding an authenticator with the camera

1. On your computer, open the website's two-factor setup page so the QR code is on screen.
2. In the app, create a password item for that site, or open an existing one and choose
   **Edit**.
3. Find the **Authenticator (OTP)** section and tap **Scan QR code**.
4. The first time, allow camera access when your phone asks.
5. Point the camera at the QR code. The app reads it and adds the authenticator to the item.
6. Tap **Save**.

The scanner screen is titled **Scan authenticator QR**. Tap **Cancel** to leave without
adding anything.

### Scanning from a screenshot

If the QR code is already on your phone — for example in a screenshot — tap **Choose image**
on the scanner screen and pick the picture instead.

| Message | What to do |
|---|---|
| **No otpauth QR found in that image. Try another photo or use the camera.** | The picture has no authenticator QR code in it. Crop closer, or scan the screen directly |
| **Could not read a QR from that image. Try again.** | The image could not be read. Try a sharper picture |

<Callout icon="ℹ️" theme="info">
  The app only accepts authenticator QR codes — the kind whose content starts with
  `otpauth://`. Other QR codes, such as a link to a web page, are ignored.
</Callout>

## Adding an authenticator by hand

If the site shows a setup key instead of, or as well as, a QR code:

1. In the **Authenticator (OTP)** section, tap **Add OTP from secret (manual)**.
2. Paste the setup key into the secret field.
3. Optionally enter the **Issuer**, such as *GitHub*, so you can tell authenticators apart.
4. Tap **Save**.

See [Adding Manual OTP](https://docs.akeyless.io/docs/adding-manual-otp) for the details.

## Using a code

Open the item. The current code is shown with a copy control — copy it and paste it into the
site's two-factor prompt.

<Callout icon="ℹ️" theme="info">
  AutoFill fills the username and password only. One-time codes are not filled
  automatically on iPhone or Android — copy the code from the app.
</Callout>

## Camera permission

The app asks for the camera only to scan authenticator QR codes. If you declined and want to
scan later, turn camera access back on:

| Phone | Where |
|---|---|
| **iPhone** | **Settings** → **Akeyless Password Manager** → **Camera** |
| **Android** | **Settings** → **Apps** → **Akeyless Password Manager** → **Permissions** → **Camera** |

Menu names vary slightly between Android manufacturers.

## Related

- [Adding and Using One-Time Passwords](https://docs.akeyless.io/docs/adding-and-using-otp-1)
- [Creating Items and Generating Passwords](https://docs.akeyless.io/docs/pwm-mobile-creating-items)
