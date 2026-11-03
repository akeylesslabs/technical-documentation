---
title: Security and Privacy
---
What the mobile app does to protect your vault on the phone, and what that means for you.

## Your vault stays in Akeyless

Items are stored and encrypted in Akeyless, not on the phone. The app keeps only what it
needs to work — your session and the copy of your logins used by AutoFill — and that is
encrypted on the device:

| | iPhone | Android |
|---|---|---|
| **App data** | Encrypted, with the key in the iOS Keychain, on this device only | Encrypted, with the key in the Android Keystore |
| **AutoFill logins** | iOS Keychain, readable only while the phone is unlocked | Encrypted with an Android Keystore key |
| **Phone backups** | App files are excluded. Keychain items cannot be restored to another device | Not included |

Signing out removes your session and every saved AutoFill login from the phone.

The app collects no analytics and shows no ads, and the leaked-password check in the password
generator and Security Health runs entirely on the phone.

## Screen protection

| | iPhone | Android |
|---|---|---|
| **App switcher** | The app is covered by a shield screen, so your vault is not visible in the app switcher | The app's preview in Recents is blank |
| **Screen recording, mirroring, AirPlay** | The app is covered by a shield screen while any of these is on | Blocked — recordings show a black screen |
| **Screenshots** | Allowed | Blocked |

<Callout icon="ℹ️" theme="info">
  **Need to show the app to someone?** Screen sharing and recordings will not show your vault.
  On iPhone you can still take a screenshot; on Android you cannot.
</Callout>

## Device integrity

The app does not run on devices whose security cannot be trusted:

- jailbroken iPhones and rooted Android phones
- emulators and simulators
- devices running hooking or tampering tools
- modified or re-signed copies of the app
- a debugger attached to the app

If any of these is detected, the app **erases everything it stored on the phone** — your
session, cached data and AutoFill logins — and shows **This device isn't supported**.
AutoFill also stops filling. Your vault itself is untouched in Akeyless; sign in on a
supported device to continue.

The check runs when the app starts and again every few seconds while it is open.

## Sessions

The app signs you out when your Akeyless session expires — including when you return to the
app after it has been in the background. Session length is set by your authentication method;
ask your administrator to change it.

The app has no separate PIN or Face ID lock of its own. Protect it with your phone's lock
screen.

## Policies your organization can set

| Policy | Effect in the app |
|---|---|
| **Hide reveal and copy for corporate secrets** | Copying a corporate value shows **Blocked by policy**. Personal items are not affected |
| **Allowed sign-in methods** | Only those methods appear on the sign-in screen |
| **Block mobile access** | Sign-in fails with your administrator's message |
| **Vault access** | Controls whether the **Personal** and **Corporate** tabs appear |

## Related

- [AutoFill on iPhone and Android](https://docs.akeyless.io/docs/pwm-mobile-autofill)
- [Signing In on Mobile](https://docs.akeyless.io/docs/pwm-mobile-sign-in)
- [Account Policies Affecting the Extension](https://docs.akeyless.io/docs/web-extension-account-policies)
