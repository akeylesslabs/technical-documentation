---
title: Adding Manual OTP
slug: pwm-ext-add-manual-otp
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
Use this workflow when the OTP secret is provided as a setup key or `otpauth://`-compatible value instead of a QR code.

## Accessing the Feature

1. Open the extension.
2. Open the three-dot menu.
3. Select **Manual OTP**.

## Entering OTPAuth Secret

1. Open the password edit screen for the target item.
2. In the custom-field flow, use the `otpauth` field.
3. Enter the setup key or related OTP value.
4. Save the item.

![Illustration for: Setup Key Option: There is an option to enter the setup key associated with the OTPAuth secret. Input Secret: Enter the OTPAuth secret into the designated field.](https://files.readme.io/8ad8ef4-Screenshot_2024-08-19_at_16.25.10.png)

![Illustration for: Setup Key Option: There is an option to enter the setup key associated with the OTPAuth secret. Input Secret: Enter the OTPAuth secret into the designated field.](https://files.readme.io/2a2137f-Screenshot_2024-08-19_at_14.43.54.png)

## Result

After saving, the OTP value becomes available as part of the item and can be used in supported OTP-related workflows.
