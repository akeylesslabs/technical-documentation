---
title: PWM 2.0 Release Notes
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

This page summarizes notable updates for Akeyless Password Manager (PWM) 2.0.

For the full release stream, refer to the official changelog:

* [https://akeylesspwm20.featurebase.app/changelog](https://akeylesspwm20.featurebase.app/changelog)

## Recent Highlights

### 2026-05-02 (1.26.24 to 1.30.1)

* Added a NIST-aligned password-strength experience with improved scoring and feedback.
* Added local breach-checking with an offline Bloom filter.
* Expanded Security Health with known-leak indicators and related metrics.

### 2026-04-19 (1.26.3 to 1.26.5)

* Improved OTP autofill detection and handling across MFA form patterns.
* Improved launch and inject flows for pages that require username, password, and OTP in multi-step authentication.
* Improved OTP-focused save and edit behavior for pages that reuse masked input patterns.

### 2026-04-11 (1.25.14 to 1.25.15)

* Added the Security Health tab for personal-vault analysis.
* Added a protection score and graph view for password hygiene signals.
* Improved scan orchestration and progress reporting for large personal-vault datasets.

### 2026-04-05 (1.25.3)

* Improved passkey sign-in reliability across relying-party and tab-selection scenarios.
* Improved fallback behavior for strict pages by retrying and injecting passkey bridge logic.

## Notes

* The version ranges above reflect grouped release notes from the PWM 2.0 changelog.
* This page is a concise summary. Use the official changelog for complete per-version details and patch-level context.
