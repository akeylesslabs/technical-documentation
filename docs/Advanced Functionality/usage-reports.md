---
title: Usage Reports
excerpt: ''
deprecated: false
hidden: false
metadata:
  title: ''
  description: ''
  robots: index
---

Akeyless Usage Reports help administrators monitor secrets, keys, and password manager activity across their organization.
These reports track requests, actions, and usage trends for secrets and keys, password manager interactions, and billing across users, applications, and service accounts. For details on password manager reporting, see the [Password Manager Usage Report for Admins](https://docs.akeyless.io/docs/password-manager-usage-report-for-admins).
To enable organization-wide views, contact your Account Manager.

## Data scope and retention

### What is included

* All actions and requests involving secrets, keys, and password manager items (creation, access, update, deletion, authentication events)
* Usage by users, applications, and service accounts
* Data from all accounts linked to your organization (if enabled)
* Items in [Personal Folders](https://docs.akeyless.io/docs/personal-corporate-areas-navigation) and shared/corporate areas

### Timeframes

* Reports can be generated for custom date ranges (for example, last 7 days, month-to-date, or a custom period)
* Default views show the last 30 days

### Retention

* Usage data is retained for 12 months (Enterprise tier; may vary by plan)
* Exported reports are not deleted automatically

### Exclusions

* Deleted items are not shown in current usage reports, but historical actions on deleted items remain visible for the retention period
* Some system/service actions may be excluded from user-facing reports for security reasons

## How to access usage reports

### Web console

1. Log in to the Akeyless Web Console.
2. Go to **Usage Report** from the main navigation menu.
3. Select the desired date range and filters (for example, by user, secret, or action).
4. Review the dashboard for key metrics (total requests, top users, and most-accessed secrets).
5. To export, open the report action menu and select **Export as JSON**.
