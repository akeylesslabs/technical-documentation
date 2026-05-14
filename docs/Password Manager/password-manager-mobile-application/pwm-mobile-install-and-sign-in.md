---
title: Install and Sign In to the Akeyless Mobile App

slug: pwm-mobile-install-and-sign-in
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
The Akeyless Password Manager mobile app is available for Android and iOS.

## Installation on Your Mobile Devices

Use the following steps to install and sign in to the mobile app on Android or iOS.

## Akeyless Password Manager Android Installation

1. Open [Akeyless Password Manager on Google Play](https://play.google.com/store/apps/details?id=com.akeylessmobile).
2. Tap **Install**.
3. Accept required Android prompts.

![Akeyless app permissions prompt on Android](https://files.readme.io/528c51e-Screenshot_20240506_171826_Google_Play_Store2.jpg)

## Akeyless Password Manager iOS Installation

1. Open [Akeyless Password Manager on the App Store](https://apps.apple.com/us/app/akeyless-password-manager/id6455634292).
2. Tap **Get**.
3. Complete iOS confirmation with Apple ID, Face ID, or Touch ID if prompted.

![Akeyless app installation confirmation prompt on iOS](https://files.readme.io/9f41004-File_5.jpg)

## Authentication Methods Support

Use an authentication method allowed by account policy.

## VPN Requirement for Zero-Knowledge Keyless Mode

For environments that require zero-knowledge keyless mode, follow organizational policy for VPN prerequisites before sign-in.

## Authentication Methods Support

After installation, open the mobile app and complete sign-in with one of the supported methods:

* Access-ID and Access-Key: Use your unique Access-ID and Access-Key combination for secure login.
* SAML: Sign in with your configured SAML identity provider.
* OIDC: Sign in with your configured OIDC identity provider.
* LDAP: For environments configured with LDAP, you can authenticate using your LDAP credentials for secure access.
    * Configure the [LDAP gateway URL](https://docs.akeyless.io/docs/configure-ldap-gateway-url) by way of advanced settings then login with Email option as a login type.
* Account Alias: Sign in with account alias when enabled by account policy.

## Post Sign-In Checklist

1. Open the app Home or Secrets view.
2. Confirm Personal or Corporate area selection.
3. Configure autofill on device if required.
4. Validate access to expected folders and items.

For more details about Akeyless Authentication Methods please visit this [link](https://docs.akeyless.io/docs/access-and-authentication-methods)
