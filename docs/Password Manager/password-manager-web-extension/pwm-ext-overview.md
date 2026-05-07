---
title: Password Manager Web Extension

slug: pwm-ext-overview
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

The Akeyless Password Manager Web Extension provides browser-based access to passwords, secrets, one-time passwords (OTPs), and passkeys.

This page summarizes documented extension capabilities and links to task-focused pages.

## Recommended Reading Order

Use this section as the starting point for PWM 2.0 workflows:

1. Install the extension and sign in.
2. Configure Advanced Options, tenant, LDAP, or enterprise deployment settings if needed.
3. Create or import passwords.
4. Use autofill, OTP, and passkey features during sign-in.
5. Review Security Health in the personal vault.

## Verified Capabilities

### Password creation and import

The extension documentation currently supports the following password-management workflows:

* Strong password generation with improved feedback.
* Tuning for allowed special characters when generating passwords.
* Import behavior that uses current account settings when a new import session starts.
* Support for account-level controls that can limit access to the personal vault area.

### Sign-in assistance

The extension supports these sign-in workflows:

* Username and password autofill for supported pages.
* OTP support for scanned and manually added `otpauth://` values.

### Passkeys

The extension supports passkey workflows including:

* Passkey creation and sign-in flows from the extension.
* A passkey toggle in advanced settings.
* Site-matching and suggestion behavior on supported relying parties.

### Security Health

Security Health support for personal-vault review includes:

* A protection score view.
* Visual breakdowns of password hygiene metrics.
* Breach-related insights and actionable follow-up.

### Secret value retrieval behavior

The extension supports value retrieval for these secret types:

* Static secrets.
* Dynamic secrets.
* Rotated secrets.

When a dynamic or rotated item is opened for value retrieval, the extension uses the gateway defined on the item when available. If the item does not define a gateway, the extension falls back to the currently configured public gateway in Advanced Options.

### Enterprise deployment

PWM 2.0 documentation now includes a first-pass enterprise deployment pattern for preconfigured authentication in managed browser deployments.

## Suggested Entry Points

Use these pages for common tasks:

* Installation and sign-in.
* Advanced Options and environment configuration.
* Password and secret creation.
* CSV import.
* Autofill, OTP, and passkeys.
* Security Health.

## Task-Based Cross-Platform Navigation

Use these links when a workflow exists in both extension and mobile docs:

* Create a password: [https://docs.akeyless.io/docs/pwm-ext-create-password](https://docs.akeyless.io/docs/pwm-ext-create-password) and [https://docs.akeyless.io/docs/pwm-mobile-create-password](https://docs.akeyless.io/docs/pwm-mobile-create-password)
* Create a static secret: [https://docs.akeyless.io/docs/pwm-ext-create-secret](https://docs.akeyless.io/docs/pwm-ext-create-secret) and [https://docs.akeyless.io/docs/pwm-mobile-create-static-secret](https://docs.akeyless.io/docs/pwm-mobile-create-static-secret)
* Autofill and injection: [https://docs.akeyless.io/docs/pwm-ext-autofill-and-password-injection](https://docs.akeyless.io/docs/pwm-ext-autofill-and-password-injection) and [https://docs.akeyless.io/docs/pwm-mobile-autofill-and-password-injection](https://docs.akeyless.io/docs/pwm-mobile-autofill-and-password-injection)
* OTP workflows: [https://docs.akeyless.io/docs/pwm-ext-otp](https://docs.akeyless.io/docs/pwm-ext-otp) and [https://docs.akeyless.io/docs/pwm-mobile-otp](https://docs.akeyless.io/docs/pwm-mobile-otp)
* Password policy settings: [https://docs.akeyless.io/docs/pwm-ext-setting-password-policy-on-account-level](https://docs.akeyless.io/docs/pwm-ext-setting-password-policy-on-account-level) and [https://docs.akeyless.io/docs/pwm-mobile-setting-password-policy-on-account-level](https://docs.akeyless.io/docs/pwm-mobile-setting-password-policy-on-account-level)

## Tutorial

Check out the tutorial video on [Using the Akeyless Password Manager Web Extension](https://tutorials.akeyless.io/docs/akeyless-password-manager-web-extension).
