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
## Passkey Management Overview

This page describes how PWM 2.0 handles passkeys in the browser extension, including viewing saved passkeys, using them for sign-in, and creating new passkeys for supported websites.

## Viewing Passkey Details

The Passkey Details section allows users to view information about their saved passkeys.

### Fields Displayed

* Passkey Name: The label or identifier for the passkey.
* Username/Email: The email or username used when the passkey was created.
* Creation Date: The date when the passkey was created.
* Related Website: The website the passkey is linked to for login.
* Option to Delete Passkey: Allows users to remove the passkey from the system.

PWM 2.0 also improves passkey lookup and suggestion behavior for supported sites.

## Using a Passkey for Login

The following steps guide users on how to log in using an existing passkey for a supported website:

### Steps

1. Navigate to a passkey-supported website.
2. Start the sign-in flow.
3. If matching passkeys exist, select the passkey to continue authentication.

PWM 2.0 improves this flow by better matching passkeys to supported sites and login contexts.

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

PWM 2.0 adds support for choosing the account default protection key or a specific protection key when creating supported passkeys.

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

## Reliability Improvements in PWM 2.0

Recent PWM 2.0 updates improve passkey support in these areas:

* Better site matching for supported relying parties.
* Better tab and context selection when the browser has multiple matching pages open.
* Better fallback handling when a page is slow or strict about passkey communication.

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
