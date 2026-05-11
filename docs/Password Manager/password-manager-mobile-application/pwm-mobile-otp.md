---
title: Adding and Using OTP

slug: pwm-mobile-otp
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
The mobile app supports OTP for saved passwords. You can add OTP values by scanning a QR code or entering the secret manually.

## Add an OTP by Scanning a QR Code

1. Navigate to the corporate or personal area where the password is stored.
2. Tap the three-dot menu next to the password entry.
3. Make sure the OTP QR code is visible on the screen in a scannable format.
4. Select **Scan OTP** from the menu.
5. Use the camera to scan the QR code.

![Three-dot options menu next to a password entry in the mobile app](https://files.readme.io/6da4508-Screenshot_2024-06-16_at_11.17.19.png)

The OTP value is added as a custom field to the selected password entry. Tap the eye icon next to the custom field to view the current code.

## Add an OTP Manually

Use manual entry when the OTP secret is provided as a setup key or `otpauth://`-compatible value instead of a QR code.

1. Open the Password Manager mobile app and navigate to the saved password.
2. Tap the three-dot menu for the target item.
3. Select **Manual OTP**.
4. Open the password edit screen.
5. Scroll to the **Custom Field** section.
6. Set the field name to `otpauth`.
7. Enter the OTPAuth secret string in the field value.
8. Save the item.

After saving, the OTP value becomes available for supported OTP-related operations.

![OTP code added as a custom field to a password entry in the mobile app](https://files.readme.io/2d50b9c-Screenshot_2024-06-16_at_11.16.55.png)
