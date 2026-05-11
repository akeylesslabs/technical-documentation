---
title: Using Autofill and Password Injection Functionality

slug: pwm-ext-autofill-and-password-injection
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
The Akeyless Password Manager Web Extension can detect supported sign-in forms and help fill saved credentials.

![Autofill prompt appearing on a website login form](https://files.readme.io/e491682-Screenshot_2024-01-10_at_16.55.04.png)

## Use Autofill

1. Open the target website.
2. Place the cursor in the username, email, or password field.
3. Select the suggested item from the Akeyless prompt when it appears.
4. Confirm the filled values before submitting the sign-in form.

## Autofill Behavior

The extension supports the following sign-in assistance behaviors:

* Supported pages can use username, password, and OTP values from the same saved item.
* Dynamic and rotated secret items can be resolved through an Akeyless Gateway before injection.
* Gateway selection for dynamic and rotated retrieval uses the item-configured gateway when present, or falls back to the current public gateway from Advanced Options.

## Autofill Setting

The extension settings include an autofill toggle. Depending on account controls, autofill can also be disabled by an administrator.

## Save or Update a Credential

If the extension detects a new or updated credential on a supported page, it can prompt to save the item or update the existing item in the vault.

When the save-suggestion dialog is shown, users can review the detected values and, where needed, add or adjust custom fields before saving.

If a matching item already exists, users can update that item or choose to create a new item from the same dialog flow.
