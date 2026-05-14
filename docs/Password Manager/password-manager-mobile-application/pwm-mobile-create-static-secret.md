---
title: Creating a New Secret

slug: pwm-mobile-create-static-secret
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
Static secrets let you securely store arbitrary text values, such as API keys, tokens, or notes, alongside your passwords in the Akeyless mobile app. Use the steps below to create one.

> 📘 **Secret items and password items**
>
> **Secret items** store arbitrary text values such as API keys, tokens, or notes, and support custom key-value fields. **Password items** store structured credentials — a URL, username, and password — and integrate with autofill and OTP. To create a password item instead, see [Creating a New Password](https://docs.akeyless.io/docs/pwm-mobile-create-password).

## Step 1: Launch the Akeyless Password Manager Mobile App

Once installed, tap on the Akeyless Password Manager app icon on your mobile device to open it.

![Akeyless Password Manager app icon on a mobile device home screen](https://files.readme.io/eef7865-IMG_0054.png)

## Step 2: Start Creating a Static Secret

1. Tap the orange **+** button. This opens an action sheet with item type options.
2. Select **Static Secret** from the action sheet.
3. Enter a unique and recognizable name in the **Secret Name** field.
4. Optionally, enter a description for the secret.

## Step 3: Define the Secret Details

In the **Value** field, enter the sensitive data that you want to store. The field accepts both plain-text and JSON values: use plain text for straightforward data such as a token, note, or API key; use JSON when the secret should store structured key-value data in a single item.

![Value field in the static secret creation form showing plain-text and JSON options](https://files.readme.io/4bb02a9-IMG_0055.png)

Optionally, specify the location for the secret by using the drop-down menu to choose the target folder or area. If the required folder does not exist yet, create it inline from the location picker.

You can also add a description and enable delete protection to reduce the risk of accidental deletion.

## Step 4: Save the Secret

Review the secret details and then tap **Save** to create the static secret in Akeyless Password Manager.
