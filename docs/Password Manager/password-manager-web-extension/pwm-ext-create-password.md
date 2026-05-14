---
title: Creating a New Password

slug: pwm-ext-create-password
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
This create-password flow includes improved password generation and password-strength feedback.

Use these steps to create a password item in the Personal or Corporate area.

> 📘 **Password items and secret items**
>
> **Password items** store structured credentials — a URL, username, and password — and integrate with autofill and OTP. **Secret items** store arbitrary text values such as API keys, tokens, or notes, and support custom key-value fields. To create a secret item instead, see [Creating a New Secret](https://docs.akeyless.io/docs/pwm-ext-create-secret).

## Step 1: Launch the Akeyless Web Extension

1. Once installed, the Akeyless Web Extension icon will appear in your browser's toolbar.
2. Click on the Akeyless Web Extension icon to launch the extension.

![Akeyless Web Extension icon in the browser toolbar](https://files.readme.io/33368d1-Screenshot_2023-11-14_at_19.10.15.png)

## Step 2: Access the Password Creation Form

![Password creation form in the web extension](https://files.readme.io/9d80c86-Screenshot_2024-02-22_at_14.22.38.png)

1. Click **New Item**.
2. Enter the password name.
3. Optionally, add a description.
4. Generate a password or enter one manually.

## Step 3: Define Password Name and Location

Choose the target location for the password:

* Personal area
* Corporate area
* A folder within the selected area

> ℹ️ **Note:**
>
> Access to the Personal area depends on account settings. If the Personal area is not available, save the password in the Corporate area.

![Password Location drop-down showing Corporate and Personal options](https://files.readme.io/d75a38d-Screenshot_2024-02-22_at_14.22.54.png)

## Step 4: Enhance Security and Add Context

Optionally, add supporting details such as the related website, service, or application.

If needed, enable delete protection to reduce accidental deletion.

## Step 5: Generate and Save the Password

Generate the password according to the active password policy and generation preferences.

The extension provides stronger generation guidance, including improved password-strength feedback and support for tuning allowed special characters.

When the password is ready, click **Save**.

The extension stores the item in the selected area.

## Step 6: Access Saved Passwords

Open the extension to view saved passwords, review item details, or copy values.

## Password Strength Policy

The Password Strength Policy feature helps ensure that new passwords meet organizational requirements.

![Password Strength Policy settings in the web extension](https://files.readme.io/91fa4a2-Screenshot_2024-04-11_at_14.21.32.png)

Users can customize password settings, but they cannot go below the minimum standards set by the organization.

The password-strength experience includes clearer feedback during password creation.

Password Strength Evaluation Criteria:

### Green: Strong Password

Password length is at the minimum or more of the length defined by the organization

Meets at least 3 of the other 4 criteria (uppercase, lowercase, numbers, special characters)

### Yellow: Medium Password

Password length is lower than the length defined by the organization

Meets at least 2 of the other 4 criteria (uppercase, lowercase, numbers, special characters)

### Red: Weak Password

Fails to meet the criteria for either green or yellow

## Related Tasks

After creating a password, you can:

* Add it to Favorites.
* Use it for autofill.
* Add OTP data if the site requires MFA.
