---
title: Installation and Auth Method of Akeyless Mobile application
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
### Installation on Your Mobile Devices

The Akeyless password manager mobile application offers a streamlined and user-friendly installation process, compatible with both Android and iOS platforms. Here's how you can effortlessly install and begin using Akeyless on your mobile device:

### Akeyless Password Manager Android Installation:

Open Google Play Store: On your Android device, navigate to the Google Play Store. This app is typically found on your device's home screen or app drawer. Tap on its icon to open it.

Search for Akeyless: Once inside the Play Store, locate the search bar at the top of the screen. Here, type in "Akeyless" and press the Enter key on your device's keyboard. This action initiates a search for the app within the Google Play Store.

Locate Akeyless Mobile App: Browse through the search results until you find the official Akeyless password manager mobile application. Look for the app with the recognizable Akeyless logo. Once located, tap on the "Install" button adjacent to the app.

Grant Permissions: A prompt will appear, detailing the permissions required by the Akeyless app to function optimally on your device. Carefully review these permissions. If they seem appropriate and necessary for the app’s functionality, tap on the "Accept" button to begin the installation process.

<Image align="center" width="200px" src="https://files.readme.io/528c51e-Screenshot_20240506_171826_Google_Play_Store2.jpg" />

<br />

### Akeyless Password Manager iOS Installation:

Open Apple App Store: On your iOS device, locate and launch the Apple App Store. This is typically found on your home screen.

Search for Akeyless: At the top of the App Store interface, you'll find a search bar. Tap on it and enter "Akeyless." Proceed by tapping the "Search" button on the keyboard.

Choose Akeyless Mobile App: The search results will display various apps. Navigate to find the official Akeyless password manager mobile application, recognizable by its logo. Once you've found it, tap on the "Get" button next to the app.

Confirm Installation: iOS may prompt you to confirm the installation. This might include reviewing the permissions the app requires and possibly entering your Apple ID password or using Face ID/Touch ID for verification. Follow these steps to finalize the installation.

<Image align="center" width="200px" src="https://files.readme.io/9f41004-File_5.jpg" />

<br />

### Authentication Methods Support

In the context of modern enterprise environments, where security is a top priority, the Akeyless Platform offers a highly secure login flow. This involves using a code ID provided by an IT admin combined with multi-factor authentication (MFA). This method is more secure than traditional master passwords or biometrics, as it introduces multiple verification layers and eliminates potential single points of failure.

### Please Note: Users will need to have a VPN on their phone installed in order to use zero-knowledge keyless functionality:

Zero-knowledge keyless functionality is a security feature that allows users to access and manage their passwords or other sensitive information without revealing their credentials to the service provider. This is achieved through cryptographic techniques that ensure that only the user has knowledge of their credentials, while the service provider can only verify their identity without ever storing or seeing their passwords.

A VPN establishes a secure tunnel between the user's mobile device and the VPN server, encrypting all network traffic and routing it through the VPN provider's secure infrastructure. This encrypted tunnel effectively shields the user's data from prying eyes, ensuring that their sensitive information, including their zero-knowledge keyless credentials, remains protected from interception and unauthorized access.

Therefore, requiring users to have a VPN installed on their phones before using zero-knowledge keyless functionality is a necessary security measure to protect their sensitive information and maintain the integrity of the zero-knowledge authentication process. By routing all network traffic through a secure VPN tunnel, users can confidently use zero-knowledge keyless functionality without compromising their security.

### Authentication Methods Support

Once you've installed the Akeyless browser extension. Simply locate the Akeyless Password Manager mobile app. To securely access your Akeyless account, you can utilize one of the following authentication methods:

* Access-ID & Access-Key: Utilize your unique Access-ID and Access-Key combination for secure login.
* SAML: Leverage your existing SAML (Security Assertion Markup Language) identity provider for streamlined authentication.
* OIDC: Employ your preferred OIDC (OpenID Connect) identity provider for a seamless login experience.
* LDAP: For environments configured with LDAP, you can authenticate using your LDAP credentials for secure access.
  * Configure the [LDAP gateway url](https://docs.akeyless.io/docs/configure-ldap-gateway-url) via advanced settings then login with Email option as a login type.
* Account Alias: Support for using an account alias to simplify identification and enhance user experience.

For more details about Akeyless Authentication Methods please visit this [link](https://docs.akeyless.io/docs/access-and-authentication-methods)