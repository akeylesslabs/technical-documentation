---
title: Using Autofill and Password Injection Functionality

slug: pwm-mobile-autofill-and-password-injection
excerpt: ''
deprecated: false
hidden: false
metadata:
  title: ''
  description: ''
  robots: index
next:
  description: ''
---
Enable autofill in the Password Manager app to fill saved credentials in supported websites and apps.

## When Users Are Prompted to Enable Autofill

Users can be prompted to enable autofill in two common situations:

* During installation, immediately after a successful sign-in.
* Later, from the app after installation is complete.

## Use Autofill in an App or Website

1. Open the target app or website.
2. Tap the username or password field.
3. Select the suggested credential from Akeyless Password Manager.
4. Complete any required biometric or device-authentication prompt.

## Enable Autofill

### On iOS

1. Open **Settings** on the iOS device.
2. Open **Passwords** or **Passwords & Accounts**, depending on the iOS version.
3. Open **Autofill Passwords**.
4. Turn on the autofill option.
5. Under **Allow Filling From**, select **Akeyless Password Manager**.

When you open a login screen in Safari or an app, iOS can offer saved credentials from Akeyless Password Manager above the keyboard or inside the sign-in field.

![Autofill settings enabled in the Akeyless mobile app](https://files.readme.io/c309879-File_3.jpg)

### On Android

1. Open **Settings** on the Android device.
2. Open **System** and then **Languages & Input**. On some devices, these labels can vary.
3. Open **Autofill service**.
4. Select **Akeyless Password Manager** as the autofill service.
5. If needed, open the Akeyless Password Manager app and enable autofill from its settings flow.

When autofill is enabled, supported apps and browsers can prompt for saved credentials when users tap a sign-in field.

![Akeyless autofill popup suggesting credentials on a login screen](https://files.readme.io/229e403-Screenshot_20240221-112137_Firefox.jpg)

## Browser Support Notes

The following Android browsers are documented as providing strong autofill support:

* Firefox
* Firefox Focus
* Microsoft Edge
* DuckDuckGo
* Brave

Chrome supports Android autofill, but prompt behavior can differ by page. In Chrome, users might need to tap the credential suggestion above the keyboard or reopen the focused field to trigger the Akeyless suggestion.
