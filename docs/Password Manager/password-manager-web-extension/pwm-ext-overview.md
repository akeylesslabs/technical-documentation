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

This page separates currently documented-and-verified capabilities from items that still require validation.

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

### Enterprise deployment

PWM 2.0 documentation now includes a first-pass enterprise deployment pattern for preconfigured authentication in managed browser deployments.

## Current Documentation Gaps

The following PWM 2.0 areas still need additional validation or assets before the documentation can be considered complete:

* Firefox-specific enterprise deployment validation.
* Confirmed supported values for preconfigured authentication fields.
* Updated screenshots for Security Health, passkey workflows, and multi-step OTP injection.
* Source-verified setup details for browser-admin deployment patterns beyond the current Chromium example.

## Pending Validation Items

The following claims should remain provisional until validation artifacts are added:

* Detailed behavior for multi-step sign-in flows that split username, password, and OTP across multiple screens.
* Exact behavior for masked OTP and MFA-style fields across target websites.
* Passkey matching behavior details across relying-party edge cases.

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
