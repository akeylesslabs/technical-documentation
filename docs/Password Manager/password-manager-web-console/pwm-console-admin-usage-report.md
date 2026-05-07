---
title: Password Manager Usage Report for Admins

slug: pwm-console-admin-usage-report
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
Use the Password Manager Usage Report to review adoption and authentication usage trends.

## Overview of the Report

The report includes these core metrics:

1. **Overall user base**
   Total active users.

2. **Total number of passwords**
   Total stored password items.

3. **Users by authentication method**
   Counts users by sign-in type, including SAML, OIDC, LDAP, and Email or Access ID based login.

## How to Interpret the Metrics

Use these patterns during review:

* Growing user base with flat password totals can indicate low vault adoption.
* High reliance on one sign-in method can indicate limited SSO diversification.
* Unexpected sign-in distribution changes can indicate policy or rollout changes.

## Recommended Admin Actions

1. Compare usage report values across review periods.
2. Identify low-adoption teams.
3. Validate configured authentication methods against policy.
4. Coordinate onboarding or policy updates where needed.

![Illustration for: 3. LDAP (Lightweight Directory Access Protocol): For users authenticated by way of traditional directory services. 4. EMAIL: Users who use email-based authentication. Access ID:…](https://files.readme.io/217ef18-Screenshot_2024-05-13_at_10.30.17.png)
