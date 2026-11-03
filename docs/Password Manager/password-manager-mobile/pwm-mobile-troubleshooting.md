---
title: Troubleshooting
---
## Signing in

| Problem | What to do |
|---|---|
| **Sign-in failed. Check your details and try again.** | The app shows this for every rejected sign-in, so check each detail: the method, the email or Access ID, the password, and — for email — the environment. See [Signing In on Mobile](https://docs.akeyless.io/docs/pwm-mobile-sign-in) |
| **Too many sign-in attempts** | Wait a few minutes before trying again |
| **Akeyless could not complete sign-in right now** | A temporary service problem. Try again shortly |
| No **Login with Gmail** or **Login with GitHub** | These are not offered in the mobile app. Use another method your account supports |
| The SAML or OIDC page does not return to the app | Close the provider window, check your network connection, and start again. If it keeps failing, ask your administrator to confirm your Access ID |
| Sent back to the sign-in screen | Your session expired. Sign in again. Session length is set by your administrator |

## Finding items

| Problem | What to do |
|---|---|
| The **Personal** or **Health** tab is missing | Your account has no personal vault, or you signed in with **Access ID**, which never shows one. Sign in with another method, or ask your administrator |
| The **Corporate** tab is missing | Your access role does not include the corporate vault. Ask your administrator |
| An item is missing | Pull down on the list to refresh. Check that no filter is on — a dot on the **Filter** icon means one is. Search looks in the current area only, so try the other area |
| **Edit**, **Delete** or **Share** is missing | Your access role does not allow it for that item |
| Copying shows **Blocked by policy** | Your organization does not allow copying corporate secrets |
| Swiping a row does nothing | You are in selection mode. Tap **Done** or **Cancel** first |

## AutoFill

| Problem | What to do |
|---|---|
| Akeyless is not offered at all | Check that Akeyless is turned on as your AutoFill provider, and on Android that Chrome is set to **Autofill using another service**. See [AutoFill on iPhone and Android](https://docs.akeyless.io/docs/pwm-mobile-autofill) |
| A login is not suggested for a site | The item needs the site's address under **Website URLs**. On Android, save the shortest address the site uses — `example.com` matches `login.example.com`, not the other way round |
| A login is not suggested inside an Android app | Add the website URL `androidapp://<package name>` to the item |
| A login added on another device does not appear | Open the Akeyless app, or pull down to refresh, so the phone picks it up |
| AutoFill stopped working after signing out | Expected — signing out removes your logins from the phone. Sign in again |
| No AutoFill on an older Android phone | AutoFill needs Android 8.0 or later |

## The app

| Problem | What to do |
|---|---|
| **This device isn't supported** | The app detected a jailbroken or rooted phone, an emulator, or a modified copy of the app, and erased its local data. Use a supported, unmodified device with the app installed from the App Store or Google Play. See [Security and Privacy](https://docs.akeyless.io/docs/pwm-mobile-security#device-integrity) |
| Screen recordings or screen sharing show a blank or shield screen | Expected — the app hides your vault while the screen is being captured |
| Android screenshots are black | Expected — Android screenshots of the app are blocked |
| **Scan QR code** does not open the camera | Allow camera access in your phone's settings |

## Contacting support

Tap **More** → **Settings** → **Contact Support**. Include the **Version** shown at the bottom
of the Settings screen, your phone model and its iOS or Android version.

## Related

- [Signing In on Mobile](https://docs.akeyless.io/docs/pwm-mobile-sign-in)
- [AutoFill on iPhone and Android](https://docs.akeyless.io/docs/pwm-mobile-autofill)
- [Troubleshooting (web extension)](https://docs.akeyless.io/docs/web-extension-troubleshooting)
