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

### CLI

Retrieve analytics and usage data:

```shell
akeyless get-analytics-data
```

Sample output:

```json
{
  "date_updated": 1716172800,
  "usage_reports": {
    "sm": {
      "product": "sm",
      "total_clients": 17,
      "clients_by_auth_method_types": {
        "saml2": 10,
        "oidc": 5,
        "ldap": 2
      },
      "total_secrets": 530,
      "secrets_by_types": {
        "static_secret": 320,
        "classic_key": 210
      }
    }
  }
}
```

To automate or parse results:

```shell
akeyless get-analytics-data --json | jq '.usage_reports.sm.secrets_by_types | to_entries[] | select(.value > 100)'
```

For command flags and usage details, see [CLI reference: get-analytics-data](https://docs.akeyless.io/docs/cli#get-analytics-data). For operation-level schema details, see [Get analytics data](https://docs.akeyless.io/reference/getanalyticsdata). For usage report access configuration, see [CLI reference for access roles](https://docs.akeyless.io/docs/cli-reference-access-roles).

### Downloading and exporting reports

#### Web console

1. In the Usage Reports dashboard, apply any filters needed.
2. Open the report action menu.
3. Select **Export as JSON**.

#### CLI

1. Run the command and redirect the output to a file:

```shell
akeyless get-analytics-data --json > usage-reports.json
```

1. Open `usage-reports.json` for reporting, sharing, or automation.

## Key metrics and filtering

* Use filters to narrow results by user, secret, action type, or time period.
* Hover over chart elements for detailed tooltips.
* Common metrics:
    * **Total Requests**: Number of API/console actions
    * **Unique Users**: Distinct users who accessed secrets/keys
    * **Top Secrets/Keys**: Most frequently accessed items
    * **Authentication Methods**: SAML, OIDC, LDAP, and more

### CLI filtering examples

The `get-analytics-data` output includes aggregated usage metrics under `usage_reports` and detailed client usage under `clients_usage_reports`.

Get total clients and total secrets for Secret Management:

```shell
akeyless get-analytics-data --json | jq '.usage_reports.sm | {total_clients, total_secrets}'
```

List authentication method usage counts for Secret Management:

```shell
akeyless get-analytics-data --json | jq '.usage_reports.sm.clients_by_auth_method_types'
```

Show the top secret types by count:

```shell
akeyless get-analytics-data --json | jq '.usage_reports.sm.secrets_by_types | to_entries | sort_by(-.value) | .[:5]'
```

Find clients that exceeded limits:

```shell
akeyless get-analytics-data --json | jq '.clients_usage_reports.sm.clients[] | select(.exceeded_clients > 0)'
```

## Configuration and notifications

### Permissions and RBAC

Access to Usage Reports is controlled by role-based access control (RBAC). To grant a role access, use the following CLI flag:

```shell
akeyless create-role --name <Role Name> --usage-reports-access all
```

Supported values: `none`, `all`.
For more on RBAC, see [Access Roles](https://docs.akeyless.io/docs/rbac).

### Event Center integration

Usage Reports can trigger events and notifications when thresholds are reached. Configure these in the [Event Center](https://docs.akeyless.io/docs/event-center):

* `usage-report`: Notifies when client usage exceeds defined limits.

Event Forwarders can be set up to deliver notifications via email, Slack, ServiceNow, and webhooks.

## Specialized usage reports

### Organizational usage and billing

Selected users can be added to an organization view for usage and billing. To aggregate usage across multiple accounts, contact your Account Manager.

### Password manager usage report

Admins can access a dedicated report for password management activity, including:

* Total users and authentication methods
* Number of stored passwords
* Usage by authentication type (SAML, OIDC, LDAP, Email)

See [Password Manager Usage Report for Admins](https://docs.akeyless.io/docs/password-manager-usage-report-for-admins) for details.

## Troubleshooting

### Missing data

* Ensure you have the correct RBAC permissions (`--usage-reports-access all`)
* Check that the selected date range includes the period of interest
* Data may be delayed by a few minutes for recent actions

### Permission errors

* Contact your administrator to verify your role includes usage reports access
* If using the CLI/API, ensure your API key or token is valid and has the required scope

### Export issues

* Try a different browser or clear cache if export/download fails
* If export fails, retry the JSON export action from the report action menu

## Related features

* [Audit Logs](https://docs.akeyless.io/docs/audit-logs): For detailed event-level tracking and compliance
* [Analytics](https://docs.akeyless.io/docs/analytics): For advanced dashboards and trend analysis
* [Billing](https://docs.akeyless.io/docs/billing): For usage-based billing and cost management

## Tutorials and further reading

* [Audit Logs, Analytics, and Usage Reports Tutorial](https://tutorials.akeyless.io/docs/audit-logs-analytics-and-usage-reports)
* [Analytics](https://docs.akeyless.io/docs/analytics)
* [Audit Logs](https://docs.akeyless.io/docs/audit-logs)
* [Event Center](https://docs.akeyless.io/docs/event-center)

> ℹ️ **Note:** Data in usage reports includes items stored in [Personal Folders](https://docs.akeyless.io/docs/personal-corporate-areas-navigation).
