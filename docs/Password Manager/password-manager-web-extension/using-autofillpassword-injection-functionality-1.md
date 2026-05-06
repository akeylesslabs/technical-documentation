---
title: Using Autofill/Password Injection Functionality
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

![Illustration for: Password AutoFill is a feature of many web browsers that allows you to automatically fill in your login credentials for websites.](https://files.readme.io/e491682-Screenshot_2024-01-10_at_16.55.04.png)

## Use Autofill

1. Open the target website.
2. Place the cursor in the username, email, or password field.
3. Select the suggested item from the Akeyless prompt when it appears.
4. Confirm the filled values before submitting the sign-in form.

## PWM 2.0 Autofill Improvements

PWM 2.0 improves browser sign-in assistance in these areas:

* Supported pages can use username, password, and OTP values from the same saved item.
* Multi-step login flows can continue targeting the active field when the next step asks for an OTP.
* OTP-style fields are handled more carefully so OTP inputs are less likely to be confused with password-update prompts.
* Save-password flows better avoid treating short MFA values as account passwords.

## Save or Update a Credential

If the extension detects a new or updated credential on a supported page, it can prompt to save the item or update the existing item in the vault.
