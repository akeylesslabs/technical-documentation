---
title: Install and Sign In to the Akeyless mobile app

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
## Installation on Your Mobile Devices

Use the following steps to install and sign in to the mobile app on Android or iOS.

## Akeyless Password Manager Android Installation

1. Open Google Play.
2. Search for **Akeyless Password Manager**.
3. Select the official app listing.
4. Tap **Install**.
5. Accept required Android prompts.

![Illustration for: Grant Permissions: A prompt will appear, detailing the permissions required by the Akeyless app to function optimally on your device. Carefully review these permissions. If…](https://files.readme.io/528c51e-Screenshot_20240506_171826_Google_Play_Store2.jpg)

## Akeyless Password Manager iOS Installation

1. Open the Apple App Store.
2. Search for **Akeyless Password Manager**.
3. Select the official app listing.
4. Tap **Get**.
5. Complete iOS confirmation with Apple ID, Face ID, or Touch ID if prompted.

![Illustration for: Confirm Installation: iOS may prompt you to confirm the installation. This might include reviewing the permissions the app requires and possibly entering your Apple ID password…](https://files.readme.io/9f41004-File_5.jpg)

## Authentication Methods Support

Use an authentication method allowed by account policy.

## VPN Requirement for Zero-Knowledge Keyless Mode

Zero-knowledge keyless functionality is a security feature that allows users to access and manage their passwords or other sensitive information without revealing their credentials to the Service Provider. This is achieved through cryptographic techniques that ensure that only the user has knowledge of their credentials, while the Service Provider can only verify their identity without ever storing or seeing their passwords.

A VPN establishes a secure tunnel between the user's mobile device and the VPN server, encrypting all network traffic and routing it through the VPN provider's secure infrastructure. This encrypted tunnel effectively shields the user's data from prying eyes, ensuring that their sensitive information, including their zero-knowledge keyless credentials, remains protected from interception and unauthorized access.

Therefore, requiring users to have a VPN installed on their phones before using zero-knowledge keyless functionality is a necessary security measure to protect their sensitive information and maintain the integrity of the zero-knowledge authentication process. By routing all network traffic through a secure VPN tunnel, users can confidently use zero-knowledge keyless functionality without compromising their security.

## Authentication Methods Support

After installation, open the mobile app and complete sign-in with one of the supported methods:

* Access-ID and Access-Key: Use your unique Access-ID and Access-Key combination for secure login.
* SAML: Leverage your existing SAML (Security Assertion Markup Language) identity provider for streamlined authentication.
* OIDC: Employ your preferred OIDC (OpenID Connect) identity provider for a seamless login experience.
* LDAP: For environments configured with LDAP, you can authenticate using your LDAP credentials for secure access.
    * Configure the [LDAP gateway URL](https://docs.akeyless.io/docs/configure-ldap-gateway-url) by way of advanced settings then login with Email option as a login type.
* Account Alias: Support for using an account alias to simplify identification and enhance user experience.

## Post Sign-In Checklist

1. Open the app Home or Secrets view.
2. Confirm Personal or Corporate area selection.
3. Configure autofill on device if required.
4. Validate access to expected folders and items.

For more details about Akeyless Authentication Methods please visit this [link](https://docs.akeyless.io/docs/access-and-authentication-methods)
