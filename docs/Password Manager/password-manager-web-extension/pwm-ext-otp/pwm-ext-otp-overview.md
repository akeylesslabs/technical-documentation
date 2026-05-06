---
title: Adding and Using One-Time Passwords
slug: pwm-ext-otp-overview
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
## Overview

PWM 2.0 supports OTP workflows for saved credentials in the browser extension. OTP values can be added from QR content or from manual `otpauth://`-compatible data, and supported sign-in pages can use those values during autofill and injection flows.

## Add an OTP by Scanning QR Content

1. Navigate to the Corporate or Personal area where the password is stored.
2. Click the three-dot menu next to the password entry.
3. Make sure the OTP QR code is visible on the current page.
4. Select "Scan OTP" from the item menu.
5. Confirm that the OTP value is added as a custom field on the selected item.

![Illustration for: Locate the Password: Navigate to the corporate or personal area where the desired password is stored. Open Options Menu: Click the three dots button next to the password entry…](https://files.readme.io/ba937b7-Screenshot_2024-06-16_at_11.01.45.png)

## View the OTP Value

After the OTP value is saved, click the eye icon next to the custom field to reveal the current code.

## OTP Behavior in PWM 2.0

PWM 2.0 expands OTP support in these areas:

* OTP values can be stored from QR-based flows and manual OTP entry.
* Supported sign-in pages can use OTP values alongside username and password.
* Better field detection helps distinguish OTP and MFA fields from standard password fields.
* Multi-step sign-in pages can keep the OTP field as the active target during injection.

## Related Topic

If the OTP secret is provided as a setup string instead of a QR code, use the manual OTP workflow.

![Illustration for: Verify Addition: The OTP code will be added as a custom field to the selected password entry. Access OTP Code: You can view the OTP code by clicking the eye icon next to the…](https://files.readme.io/f962648-Screenshot_2024-06-16_at_11.08.08.png)
