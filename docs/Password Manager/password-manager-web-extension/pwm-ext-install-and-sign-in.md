---
title: Password Manager Web Extension

slug: pwm-ext-install-and-sign-in
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
Use the following steps to install and sign in to the Akeyless Password Manager Web Extension in your browser.

## Installation Across Browsers

The Akeyless Password Manager Web Extension is available for:

* [Firefox](#akeyless-password-manager-firefox-installation)
* [Google Chrome](#akeyless-password-manager-google-chrome-installation)
* [Microsoft Edge](#akeyless-password-manager-microsoft-edge-installation)

> ℹ️ **Note (Installing Akeyless Extensions with SRA Support):**
>
> Search for **Akeyless Password Manager** in the relevant browser extension store.

## Akeyless Password Manager Firefox Installation

Supported Firefox: desktop version 91.1.0 or later.

1. Open Firefox and go to the Firefox Add-ons listing for Akeyless Password Manager: [link](https://addons.mozilla.org/en-US/firefox/addon/akeyless-sra/).
2. Click **Add to Firefox**.
3. Review the requested permissions, and confirm the installation.
4. Pin the extension so it remains visible in the browser toolbar.

> ℹ️ **Note:**
>
> After installing or updating the extension on Firefox, verify that the extension can access website data:
>
> 1. Open the Extensions Manager: Go to the Firefox menu, select Add-ons and Themes > Extensions.
> 2. Locate the Akeyless Password Manager Extension: Under the Enabled section, click the three dots (...) next to the extension.
> 3. Verify Permissions: Select Manage and ensure the "Access your data for all websites" permission is enabled.
> 4. Confirm Settings: The toggle switch should be turned on for this permission.

## Akeyless Password Manager Google Chrome Installation

![Akeyless Password Manager in the Chrome Web Store](https://files.readme.io/3d3d29c-Screenshot_2024-05-07_at_16.02.38.png)

Supported Google Chrome: Version 88+

1. Open the Chrome Web Store search results for Akeyless: [link](https://chromewebstore.google.com/search/akeyless?hl=en-US).
2. Select the Akeyless Password Manager extension.
3. Click **Add to Chrome**.
4. Review the requested permissions, and confirm the installation.
5. Pin the extension so it remains visible in the browser toolbar.

## Akeyless Password Manager Microsoft Edge Installation

Supported Microsoft Edge: Version 88+

1. Open the Microsoft Edge Add-ons listing for Akeyless Password Manager: [link](https://microsoftedge.microsoft.com/addons/detail/akeyless-password-manager/bjgnnbhhfenmggpgnlbiilnoadoblmgo).
2. Click **Get**.
3. Review the requested permissions, and confirm the installation.
4. Pin the extension so it remains visible in the browser toolbar.

## Next Step

After installation, sign in with the required authentication method. For environment-specific options, see the Advanced Options, tenant URL, LDAP, and enterprise deployment pages in this section.

## Authentication Methods Support

After installation, click the Akeyless icon in the browser toolbar and start the sign-in flow. The extension supports these authentication methods:

* Email and Password: Enter your registered email address and password to gain access.
* Access-ID and Access-Key: Use your unique Access-ID and Access-Key combination for secure login.
* SAML: Sign in with your configured SAML identity provider.
* OIDC: Sign in with your configured OIDC identity provider.
* GitHub: Sign in with GitHub when enabled by account policy.
* Google: Sign in with Google when enabled by account policy.
* Code-ID: Enter the unique code ID provided by your IT administrator. This code serves as your primary identifier and ensures that only authorized individuals can initiate the login process.
* LDAP: For environments configured with LDAP, you can authenticate using LDAP credentials.
  Configure the [LDAP gateway URL](https://docs.akeyless.io/docs/pwm-ext-configure-ldap-gateway-url) in Advanced Options, and then sign in with the Email option.
* Account Alias: Sign in with account alias when enabled by account policy.

## Sign-In Policy Notes

Available authentication methods depend on account configuration and administrator policy.

If a configured method is not shown in the extension sign-in screen, verify account-level authentication settings before troubleshooting the client.

For more details, see [Access and Authentication Methods](https://docs.akeyless.io/docs/access-and-authentication-methods).
