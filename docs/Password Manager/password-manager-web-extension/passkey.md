---
title: Passkey
excerpt: Web Extension
deprecated: false
hidden: false
metadata:
  title: ''
  description: ''
  robots: index
next:
  description: ''
---
### Passkey Management Overview

This documentation provides an overview of the Passkey management system, including how to view passkey details, use a passkey for login, and create a new passkey. The instructions below describe the key functionalities and flow for managing passkeys.

<br />

### Viewing Passkey Details

The Passkey Details section allows users to view information about their saved passkeys.

**Fields Displayed:**

* Passkey Name: The label or identifier for the passkey.
* Username/Email: The email or username used when the passkey was created.
* Creation Date: The date when the passkey was created.
* Related Website: The website the passkey is linked to for login.
* Option to Delete Passkey: Allows users to remove the passkey from the system.

<br />

### Using a Passkey for Login

The following steps guide users on how to log in using an existing passkey for a supported website:

**Steps:**

* Navigate to a Passkey-supported website:
  * Example: Adobe Account Security
* Attempt to Sign In:
  * Try logging in to the website.
* If a passkey exists for the website:
  * A list of available passkeys will be shown.
  * Users can select the relevant passkey to sign in.

**Example Flow:**

* Go to the website → Try to sign in → If passkey exists → Show available passkeys.

<br />

### Creating a New Passkey

Users can create a new passkey for a supported website. Follow the steps below to generate and save a passkey within the system.

**Steps:**

* Navigate to the Passkey creation page on a supported website:
  * Example: Adobe Account Security
* Click on "Add Passkey".
* Authenticate:
  * If logged in to the website (e.g., Adobe), proceed with passkey creation.
  * If not logged in, authenticate first.
* Passkey Status:
  * If the passkey already exists for the website, the user will be given the option to update or create a new passkey.
  * If no passkey exists, a new passkey will be created.
* Save the Passkey:
  * If saving the passkey is successful, a Success Message will be shown.
  * If there is an error during the process, an Error Message will be displayed.

**Example Flow:**

* Navigate to the website → Click on "Add Passkey" → Authenticate (if needed) → Check passkey existence → Create or update passkey → Save passkey → Success/Error message.

## Error and Success Messages

* Error Message: Shown when the passkey creation or update process fails.
* Success Message: Displayed when the passkey is successfully created or updated.

## Toggling Passkey Authentication in the Web Extension

Users can enable or disable Passkey Authentication directly through the web extension. This allows them to control when the extension uses passkeys for login.

Steps:

1. Open the web extension.
2. Click on the three-dot menu in the upper-right corner of the extension.
3. Locate the Passkey Authentication Toggle option.
4. Use the toggle button to enable or disable Passkey Authentication:
5. When enabled, the extension will use passkeys for supported logins.
6. When disabled, passkey functionality will be turned off.

* Note: Disabling Passkey Authentication does not delete saved passkeys but prevents them from being used until re-enabled.
