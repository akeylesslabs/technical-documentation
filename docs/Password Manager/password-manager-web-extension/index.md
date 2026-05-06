---
title: Password Manager Web Extension

slug: pwm-overview
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

The Akeyless Password Manager Web Extension provides browser-based access to passwords, secrets, one-time passwords (OTPs), and passkeys. PWM 2.0 expands this experience with improved password generation, stronger autofill support for multi-step sign-in flows, passkey enhancements, Security Health insights, and enterprise deployment options.

## Recommended Reading Order

Use this section as the starting point for PWM 2.0 workflows:

1. Install the extension and sign in.
2. Configure Advanced Options, tenant, LDAP, or enterprise deployment settings if needed.
3. Create or import passwords.
4. Use autofill, OTP, and passkey features during sign-in.
5. Review Security Health in the personal vault.

## PWM 2.0 Capabilities

### Password creation and import

PWM 2.0 includes the following updates for password management workflows:

* Strong password generation with improved feedback.
* Tuning for allowed special characters when generating passwords.
* Import behavior that uses current account settings when a new import session starts.
* Support for account-level controls that can limit access to the personal vault area.

### Sign-in assistance

PWM 2.0 improves sign-in support for browser workflows:

* Username and password autofill for supported pages.
* OTP support for scanned and manually added `otpauth://` values.
* Better handling for pages that split username, password, and OTP across multiple steps.
* Better handling for masked OTP and other MFA-style fields.

### Passkeys

PWM 2.0 expands passkey support with:

* Passkey creation and sign-in flows from the extension.
* A passkey toggle in advanced settings.
* Reliability improvements for site matching and passkey suggestions on supported relying parties.

### Security Health

PWM 2.0 adds Security Health for personal-vault review, including:

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

## Suggested Entry Points

Use these pages for common tasks:

* Installation and sign-in.
* Advanced Options and environment configuration.
* Password and secret creation.
* CSV import.
* Autofill, OTP, and passkeys.
* Security Health.

## Tutorial

Check out the tutorial video on [Using the Akeyless Password Manager Web Extension](https://tutorials.akeyless.io/docs/akeyless-password-manager-web-extension).
