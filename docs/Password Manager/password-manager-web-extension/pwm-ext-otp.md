---
title: Adding and Using One-Time Passwords

slug: pwm-ext-otp
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
The extension supports OTP for saved credentials. OTP values can be added from QR content or from manual `otpauth://`-compatible data, and supported sign-in pages can use those values during autofill and injection flows.

## Add an OTP by Scanning QR Content

1. Navigate to the Corporate or Personal area where the password is stored.
2. Click the three-dot menu next to the password entry.
3. Make sure the OTP QR code is visible on the current page.
4. Select "Scan OTP" from the item menu.
5. Confirm that the OTP value is added as a custom field on the selected item.

![Three-dot options menu next to a password entry in the web extension](https://files.readme.io/ba937b7-Screenshot_2024-06-16_at_11.01.45.png)

## View the OTP Value

After the OTP value is saved, click the eye icon next to the custom field to reveal the current code.

## OTP Behavior

The extension supports OTP in these areas:

* OTP values can be stored from QR-based flows and manual OTP entry.
* Supported sign-in pages can use OTP values alongside username and password.
* Better field detection helps distinguish OTP and MFA fields from standard password fields.
* Multi-step sign-in pages can keep the OTP field as the active target during injection.

## Add an OTP Manually

Use manual entry when the OTP secret is provided as a setup key or `otpauth://`-compatible value instead of a QR code.

1. Open the extension.
2. Open the three-dot menu.
3. Select **Manual OTP**.
4. Open the password edit screen for the target item.
5. In the custom-field flow, use the `otpauth` field.
6. Enter the setup key or related OTP value.
7. Save the item.

![OTP setup key and secret input fields in the web extension](https://files.readme.io/8ad8ef4-Screenshot_2024-08-19_at_16.25.10.png)

After saving, the OTP value becomes available as part of the item and can be used in supported OTP-related operations.

![OTP code added as a custom field to a password entry in the web extension](https://files.readme.io/f962648-Screenshot_2024-06-16_at_11.08.08.png)
