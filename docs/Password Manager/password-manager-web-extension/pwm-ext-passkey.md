---
title: Passkey

slug: pwm-ext-passkey
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
Use the following steps to view, create, and use passkeys with the Akeyless Password Manager Web Extension.

## Passkey Management Overview

The extension supports passkey operations, including viewing saved passkeys, using them for sign-in, and creating new passkeys for supported websites.

## Viewing Passkey Details

The Passkey Details section allows users to view information about their saved passkeys.

### Fields Displayed

* Passkey Name: The label or identifier for the passkey.
* Username/Email: The email or username used when the passkey was created.
* Creation Date: The date when the passkey was created.
* Related Website: The website the passkey is linked to for login.
* Option to Delete Passkey: Allows users to remove the passkey from the system.

The extension improves passkey lookup and suggestion behavior for supported sites.

## Using a Passkey for Login

The following steps guide users on how to log in using an existing passkey for a supported website:

### Steps

1. Navigate to a passkey-supported website.
2. Start the sign-in flow.
3. If matching passkeys exist, select the passkey to continue authentication.

This flow includes matching passkeys to supported sites and login contexts.

### Example Flow

* Go to the website → Try to sign in → If passkey exists → Show available passkeys.

## Creating a New Passkey

Users can create a new passkey for a supported website. Follow the steps below to generate and save a passkey within the system.

### Steps

1. Navigate to passkey creation on a supported website.
2. Select the website option to add a passkey.
3. Complete website authentication if required.
4. Complete the extension prompt to create or update the passkey.
5. Confirm success message.

The extension supports choosing the account default protection key or a specific protection key when creating supported passkeys.

#### Example Flow

* Navigate to the website → Click on "Add Passkey" → Authenticate (if needed) → Check passkey existence → Create or update passkey → Save passkey → Success/Error message.

## Error and Success Messages

* Error Message: Shown when the passkey creation or update process fails.
* Success Message: Displayed when the passkey is successfully created or updated.

## Transport and Authenticator Behavior

When a passkey is created, the extension processes browser-provided WebAuthn data, including authenticator transport metadata.

Transport values can include:

* `hybrid`
* `internal`
* `usb`

These values come from the authenticator and browser flow. They are used by the extension during passkey handling and are not configured as manual user inputs in Password Manager pages.

## WebAuthn Metadata Handling

During passkey create and assert flows, the extension normalizes WebAuthn request metadata from the browser before processing.

Normalized metadata includes values such as:

* Challenge and RP context.
* Origin and client data payload.
* User verification and resident-key requirements.
* Credential include or exclude descriptors.
* Supported public-key algorithm selection.

These values are handled internally by the extension flow and are not directly edited by end users in Password Manager screens.

## Toggling Passkey Authentication in the Web Extension

Users can enable or disable Passkey Authentication directly through the web extension. This allows them to control when the extension uses passkeys for login.

Steps:

1. Open the web extension.
2. Click on the three-dot menu in the upper-right corner of the extension.
3. Locate the Passkey Authentication toggle in settings.
4. Turn the setting on or off.
5. When enabled, the extension can provide passkey-based login suggestions on supported pages.
6. When disabled, passkey functionality is not used for sign-in suggestions.

* Note: Disabling Passkey Authentication does not delete saved passkeys but prevents them from being used until re-enabled.
