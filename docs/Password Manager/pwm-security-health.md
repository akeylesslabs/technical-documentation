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
Security Health helps users and administrators review password risk indicators and identify remediation actions across both the Password Manager Web Extension (personal vault view) and the Password Manager Web Console (admin dashboard). Both surfaces provide visibility into password strength, breach exposure, and other signals that indicate elevated account risk to help prioritize password updates and security improvements.

## What Security Health Shows

* Overall security score for password hygiene review.
* Weak-password indicators and remediation suggestions.
* Reused-password detection across your vault.
* Breach-related insights identifying passwords exposed in known data breaches.
* Personal-vault analysis (extension) or account-level analysis (console).

## Typical Review Flow

1. Open the relevant Password Manager surface (Web Extension or Web Console).
2. Navigate to the Security Health view.
3. Review the current score and supporting metrics.
4. Inspect affected items and update weak, reused, or exposed passwords as needed.

## Password Manager Web Extension (User View)

The Web Extension provides a personal-vault view of password hygiene, helping individual users review the security of their stored credentials. The interface includes an overall score view, weak and reused password insights, and breach-related alerts to help users identify passwords that require attention.

Security Health features may vary based on account configuration. When enabled, password-score functionality uses password-related signals to help summarize the current state of your vault.

## Password Manager Web Console (Admin View)

The Web Console provides an admin dashboard for reviewing account-level password security metrics, including aggregated scores across all users and password strength analytics.

### Security Score

The **Overall Security Score** is a 0–100 aggregate value calculated as the average of all individual password scores in the account, reflecting the overall strength of passwords stored in Password Manager. Each password's score is determined by factors such as password length and character variety.

The dashboard gauge shows the current score out of 100. Scores closer to 100 indicate a stronger password portfolio.

> 📘 **Note:**
>
> The password score feature must be enabled in account settings before scores are calculated and displayed. When disabled, the Security Health page is not accessible.

When a password's score is low, the **Suggestion** column in the password list shows a remediation prompt, for example: **Low score**: Strengthen password. Consider length or variety. **Zero score**: Weak password. Use longer password and mix character types.

### Dashboard Layout and Filtering

The Security Health dashboard displays:

1. **Gauges section** — Overall Security Score, Weak passwords count, and Reused passwords count.
2. **Password list section** — Password name, location, Risk Level, Suggestion, and Last updated timestamp.

[Use filters](https://docs.akeyless.io/docs/pwm-ext-use-filters-and-tags) to scope the password list: Weak passwords, Compromised passwords, or Update-required passwords.

### Compromised Password Detection

Security Health checks passwords against the [Have I Been Pwned](https://haveibeenpwned.com/) database, which aggregates publicly disclosed password breaches. This check identifies **Exposure** (whether a password appeared in any known breach), **Reuse-risk indicators** (how many times the same password was exposed across breaches), and **Security score enrichment** (incorporating breach metrics into overall assessment). Passwords flagged appear in the password list with a **Compromised** risk level—use the filter to isolate and prioritize remediation.

### Toggle for Password Score Feature

The account settings page includes a toggle for password scoring located under "Password Management." The feature is disabled by default. When enabled, password scores are calculated and displayed; when disabled, scores are hidden.
