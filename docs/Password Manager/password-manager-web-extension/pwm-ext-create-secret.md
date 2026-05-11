---
title: Creating a New Secret

slug: pwm-ext-create-secret
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
Use these steps to create a static secret item in the extension.

> 📘 **Secret items and password items**
>
> **Secret items** store arbitrary text values such as API keys, tokens, or notes, and support custom key-value fields. **Password items** store structured credentials — a URL, username, and password — and integrate with autofill and OTP. To create a password item instead, see [Creating a New Password](https://docs.akeyless.io/docs/pwm-ext-create-password).

## Step 1: Launch the Akeyless Web Extension

1. Once installed (see [Install and Sign In to the Akeyless Web Extension](https://docs.akeyless.io/docs/pwm-ext-install-and-sign-in)), the Akeyless Web Extension icon will appear in your browser's toolbar.
2. Click on the Akeyless Web Extension icon to launch the extension.

![Akeyless Web Extension icon in the browser toolbar](https://files.readme.io/8a3048e-Screenshot_2024-02-22_at_14.23.10.png)

## Step 2: Access the Password Creation Form

1. Click **New Item**.
2. Open the **Static Secret** tab.
3. Enter the secret name.
4. Optionally, add a description.

## Step 3: Add Custom Fields (Optional)

You can add custom fields to store additional key-value data on the secret item.

1. Select **Add Field**.
2. Enter field name and value.
3. Save the field.

Field names must be unique per item.

For OTP-specific custom field setup, see [OTP setup and usage](https://docs.akeyless.io/docs/pwm-ext-otp).

## Step 4: Define Value and Location

Enter the secret value in the **Value** field.

![Value and Location fields in the secret creation form](https://files.readme.io/774a6f9-Screenshot_2024-02-22_at_14.23.19.png)

Then choose the target location:

* Personal area
* Corporate area
* A folder within the selected area

## Save the Secret

After entering the value and location, click **Save**.

## Secret Value Types

The secret value field supports both plain text and JSON values.

Use plain text for single-value items such as tokens, notes, or one-value credentials.

Use JSON when the secret needs structured key-value data in one item.

![Value field containing JSON data in the secret creation form](https://files.readme.io/55cdb8e-Screenshot_2024-03-21_at_13.50.43.png)
