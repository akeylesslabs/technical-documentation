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
Locate the Password: Navigate to the corporate or personal area where the desired password is stored.

Open Options Menu: Tap the three dots button next to the password entry to open the options menu.

![Illustration for: Locate the Password: Navigate to the corporate or personal area where the desired password is stored. Open Options Menu: Tap the three dots button next to the password entry to…](https://files.readme.io/6da4508-Screenshot_2024-06-16_at_11.17.19.png)

Prepare OTP for Scanning: Ensure that the OTP (One-Time Password) code is visible on the screen in a scannable format.

Scan the Code: Use the camera to scan the OTP code.

Select Scan OTP: Choose the "Scan OTP" option from the menu.

Verify Addition: The OTP code will be added as a custom field to the selected password entry.

Access OTP Code: You can view the OTP code by tapping the eye icon next to the custom field.

## Add an OTP Manually

Use the manual workflow when the OTP secret is provided as a setup key or `otpauth://`-compatible value instead of a QR code.

1. Open the Password Manager mobile app and navigate to the saved password.
2. Tap the three-dot menu for the target item.
3. Select **Manual OTP**.
4. Open the password edit screen.
5. Scroll to the **Custom Field** section.
6. Set the field name to `otpauth`.
7. Enter the OTPAuth secret string in the field value.
8. Save the item.

After saving, the OTP value becomes available for supported OTP-related workflows.

![Illustration for: Verify Addition: The OTP code will be added as a custom field to the selected password entry. Access OTP Code: You can view the OTP code by tapping the eye icon next to the…](https://files.readme.io/2d50b9c-Screenshot_2024-06-16_at_11.16.55.png)
