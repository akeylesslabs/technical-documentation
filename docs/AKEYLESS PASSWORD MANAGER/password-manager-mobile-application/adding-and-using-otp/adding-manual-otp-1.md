---
title: Adding Manual OTP
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
Users often receive OTP Auth secrets as strings instead of complete QR codes or full OTP Auth links. This feature allows users to manually input these secrets into the PM mobile app, where they will be decoded and integrated as functional OTP authentication methods.

## Accessing the Feature

Navigate to the Secrets Section: Open the PM mobile app and navigate to the 'Secrets' section, where your passwords are stored.

Open the Menu: Tap on the three-dot icon next to the desired account, such as GitLab, to open the options menu.

Select "Manual OTP": From the menu, select the "Manual OTP" option to manually input an OTP secret. (Visible in the second screenshot.)

## Entering OTPAuth Secret

Password Edit Screen: After selecting "Manual OTP," you’ll be redirected to the password edit screen, as shown in the first screenshot.

Custom Field Creation: Scroll down to the "Custom Field" section where a new custom field can be added.

Field Name: The field name should be labeled "otpauth" for OTP-based secrets.

Input Secret: Enter the OTPAuth secret string into the "Field Name Value" box (as shown in the first screenshot). Once entered, it will be stored and ready to use for authentication.

<br />

[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/31a69fb27196aa64ab36b2f9023c35cd3ed646c1c88e90f01b21c371a3274e49-Screenshot_2024-10-07_at_11.55.12.png",
        null,
        null
      ],
      "align": "center",
      "sizing": "1px"
    }
  ]
}
[/block]


[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/482c2db0fdfdf2a6dbed1c834403f289e5412806f56bcaf335ba380a8390c6b6-Screenshot_2024-10-07_at_11.55.12.png",
        null,
        null
      ],
      "align": "left",
      "sizing": "200px"
    }
  ]
}
[/block]


[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/668b604f63d6a4ef43ccc0effbffd40583bfc5268b50e2c6d96c2e4970f6eaef-Screenshot_2024-10-07_at_11.55.19.png",
        null,
        null
      ],
      "align": "right",
      "sizing": "200px"
    }
  ]
}
[/block]