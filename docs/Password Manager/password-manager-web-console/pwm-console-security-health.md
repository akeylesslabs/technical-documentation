---
title: Security Health

slug: pwm-console-security-health
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
Use Security Health to review password risk indicators and identify remediation actions.

![Security Health dashboard showing password strength gauges and password list](https://files.readme.io/c51dd3e02752d51b5d79e21377a2cc21270b2bb98962f694dacc5674b4347a87-Screenshot_2024-09-21_at_7.32.19.png)

## Security Score

The **Overall Security Score** is a 0–100 aggregate value calculated as the average of all individual password scores in the account. It reflects the overall strength of passwords stored in Password Manager.

Each password in the account has its own score. That score is determined by factors such as password length and character variety. The Overall Security Score rolls up all individual scores into a single account-level indicator.

The dashboard gauge shows the current score out of 100. Scores closer to 100 indicate a stronger password portfolio.

> 📘 **Note:**
>
> The password score feature must be enabled in account settings before scores are calculated and displayed. When disabled, the Security Health page is not accessible. See [Toggle for Password Score Feature](#toggle-for-password-score-feature).

When a password's score is low, the **Suggestion** column in the password list shows a remediation prompt, for example:

* **Low score**: Strengthen password. Consider length or variety.
* **Zero score**: Weak password. Use longer password and mix character types.

## Dashboard Layout

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

## Enhanced Filtering Options

Use filters to scope the password list:

* Weak passwords.
* Compromised passwords.
* Update-required passwords.

## Toggle for Password Score Feature

The account settings page includes a toggle for password scoring:

* **Toggle Button:** Located under "Password Management," the button controls whether the password score is displayed.
* **Default Setting:** The feature is disabled by default.
* **Functionality:** When enabled, password scores are calculated and displayed; when disabled, scores are hidden.

## Compromised Password Check

Security Health checks passwords against known compromised-credential data using the [Have I Been Pwned](https://haveibeenpwned.com/) database, which aggregates publicly disclosed password breaches.

This check provides the following signals:

* **Exposure detection**: Identifies whether a password has appeared in any known data breach, including credentials circulating on the dark web.
* **Reuse-risk indicators**: Measures how many times the same password has been exposed across different breaches, highlighting patterns of weak or reused credentials.
* **Security score enrichment**: Incorporates exposure and reuse metrics into each password's score, producing a more risk-aware Security Health assessment.

Passwords flagged by this check appear in the dashboard password list with a **Compromised** risk level. Use the **Compromised passwords** filter to isolate them and prioritize remediation.
