---
title: Security Health

slug: pwm-security-health
excerpt: 'Monitor password strength, breach exposure, and account risk across your Password Manager vault.'
deprecated: false
hidden: false
metadata:
  title: ''
  description: ''
  robots: index
next:
  description: ''
---
Security Health helps users and administrators review password risk indicators and identify remediation actions. It provides visibility into password strength, breach exposure, and other signals that indicate elevated account risk.

## Overview

Security Health is available in both the Password Manager Web Extension (personal vault view) and the Password Manager Web Console (admin dashboard). Both surfaces provide signals to help prioritize password updates and security improvements.

### What Security Health Shows

* Overall security score for password hygiene review.
* Weak-password indicators and remediation suggestions.
* Reused-password detection across your vault.
* Breach-related insights identifying passwords exposed in known data breaches.
* Personal-vault analysis (extension) or account-level analysis (console).

### Typical Review Flow

1. Open the relevant Password Manager surface (Web Extension or Web Console).
2. Navigate to the Security Health view.
3. Review the current score and supporting metrics.
4. Inspect affected items and update weak, reused, or exposed passwords as needed.

## Password Manager Web Extension (User View)

The Web Extension provides a personal-vault view of password hygiene, helping individual users review the security of their stored credentials.

### Security Health Features in the Extension

* An overall score view for password hygiene review.
* Weak-password insight.
* Reused-password insight.
* Personal-vault analysis focused on the user's own stored credentials.
* Breach-related insights to help identify passwords that should be updated.

### Password Score Controls

Some account configurations can control whether password-score functionality is shown. When enabled, Security Health uses password-related signals to help summarize the current state of the vault.

### Breach and Exposure Insights

Security Health includes breach-related insights so users can identify passwords that require attention.

Use these insights to prioritize follow-up on:

* Passwords with higher exposure risk.
* Weak or outdated passwords.
* Passwords that should be rotated or replaced.

For detailed steps on accessing Security Health in the Web Extension, see [Accessing Security Health in the Web Extension](https://docs.akeyless.io/docs/pwm-ext-security-health).

## Password Manager Web Console (Admin View)

The Web Console provides an admin dashboard for reviewing account-level password security metrics, including aggregated scores across all users and password strength analytics.

### Security Score

The **Overall Security Score** is a 0–100 aggregate value calculated as the average of all individual password scores in the account. It reflects the overall strength of passwords stored in Password Manager.

Each password in the account has its own score. That score is determined by factors such as password length and character variety. The Overall Security Score rolls up all individual scores into a single account-level indicator.

The dashboard gauge shows the current score out of 100. Scores closer to 100 indicate a stronger password portfolio.

> 📘 **Note:**
>
> The password score feature must be enabled in account settings before scores are calculated and displayed. When disabled, the Security Health page is not accessible.

When a password's score is low, the **Suggestion** column in the password list shows a remediation prompt, for example:

* **Low score**: Strengthen password. Consider length or variety.
* **Zero score**: Weak password. Use longer password and mix character types.

### Dashboard Layout

1. **Gauges section**
   * Overall Security Score gauge: aggregate average score across all passwords, out of 100.
   * Weak gauge: number of weak passwords out of total passwords.
   * Reused gauge: number of reused passwords out of total passwords.
2. **Password list section**
   * Password name.
   * Password location.
   * Risk Level.
   * Suggestion.
   * Last updated timestamp.

### Enhanced Filtering Options

Use filters to scope the password list:

* Weak passwords.
* Compromised passwords.
* Update-required passwords.

### Toggle for Password Score Feature

The account settings page includes a toggle for password scoring:

* **Toggle Button:** Located under "Password Management," the button controls whether the password score is displayed.
* **Default Setting:** The feature is disabled by default.
* **Functionality:** When enabled, password scores are calculated and displayed; when disabled, scores are hidden.

### Compromised Password Check

Security Health checks passwords against known compromised-credential data using the [Have I Been Pwned](https://haveibeenpwned.com/) database, which aggregates publicly disclosed password breaches.

This check provides the following signals:

* **Exposure detection**: Identifies whether a password has appeared in any known data breach, including credentials circulating on the dark web.
* **Reuse-risk indicators**: Measures how many times the same password has been exposed across different breaches, highlighting patterns of weak or reused credentials.
* **Security score enrichment**: Incorporates exposure and reuse metrics into each password's score, producing a more risk-aware Security Health assessment.

Passwords flagged by this check appear in the dashboard password list with a **Compromised** risk level. Use the **Compromised passwords** filter to isolate them and prioritize remediation.

For detailed admin instructions, see [Accessing Security Health in the Web Console](https://docs.akeyless.io/docs/pwm-console-security-health).
