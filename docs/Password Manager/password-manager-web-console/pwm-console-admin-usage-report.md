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

## Exporting Report Data

The report data can be exported and consumed programmatically in two ways.

### JSON Export

The report header includes an **Export as JSON** option. Selecting it downloads a file named `PasswordManagerReport.json`.

The exported file contains the following top-level fields:

| Field | Description |
| --- | --- |
| `time` | Unix timestamp (milliseconds) of the export |
| `clientsByMonth` | Monthly user counts, keyed by month label |
| `clientsByAuthMethods` | Per auth-method breakdown with `actual` (active) and `total` (including exceeded) counts |
| `secretsByMonth` | Monthly password and secret item counts, keyed by month label |
| `secretByTypes` | Breakdown of item counts by secret type |

Use this export to feed the data into external dashboards, reporting pipelines, or spreadsheet tooling.

### Usage Event Notifications

Admins can configure an automated threshold alert that fires when the Password Manager client count reaches a set value.

To configure it:

1. Open the Usage Report in the Password Manager console.
2. From the options menu in the report header, select **Set Usage Event**.
3. Enter a **Clients Limit** value (the threshold at which the alert fires).
4. Save the setting.

When the account's active client count reaches the configured threshold, Akeyless emits a `usage-report` event through the Event Center. The event message reads:

> Your account has reached _N_ clients in Password Manager.

Route this event to any configured notification target (email, Slack, webhook, and so on) using the Event Center forwarder settings.

![Password Manager usage report showing authentication method breakdown](https://files.readme.io/217ef18-Screenshot_2024-05-13_at_10.30.17.png)
