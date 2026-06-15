---
title: Audit Logs
excerpt: ''
deprecated: false
hidden: false
metadata:
  title: ''
  description: ''
  robots: index
next:
  description: ''
  pages:
    - type: basic
      slug: log-forwarding
      title: Log Forwarding
slug: audit-logs
---
Akeyless collects detailed Audit Logs per secret type, operation, user, time, and so on.

Akeyless Audit Logs take note of just about every change/action within the Akeyless system, providing a complete track record of your Akeyless system operations. Therefore, Akeyless Audit Logs are a valuable resource for Akeyless admins and auditors who want to examine suspicious activity on Akeyless or diagnose and troubleshoot issues.

These Audit Logs can give an Akeyless administrator invaluable insight into what behavior is normal and what behavior isn’t. A log event, for example, will show what activity was attempted and whether it succeeded. This can be useful when identifying whether a system component is misconfigured or likely to fail.

Akeyless log auditing is important for cybersecurity because it provides records that can serve as evidence. A comprehensive and in-depth log audit can make all the difference in the event of a legal battle and can protect your business from liability.

## Viewing Logs in the Console

When using the console, you can navigate to the **Audit Logs** tab to view logs in the following format:

![Audit Logs view in the Akeyless Console.](https://files.readme.io/7ec054a7174c4de9426983fab4b975d5eeee76db3c232f68c249ee7beea90113-Screenshot_2026-06-11_at_12.21.37.png)

These logs show you the time of the described action, what it was, whether it was successful or unsuccessful (status codes in the four hundreds means error), the client performing it, what IP it was performed from, and additional parameter tags such as access type or product type.

You can filter your logs based on any of these rubrics or tags inside the Akeyless SaaS platform to get insights or clarifications.

## Reading the Raw Logs

Another way to view your logs is to forward them in their raw form to tools such as Splunk, Logz.io, and so on.
The logs will show up as a line of text, from which you can read the following information:

| Log Line | Description |
| --- | --- |
| `Timestamp` | The log starts with a timestamp string in Date `T` Time Timezone format. |
| `account_id` | Account ID. |
| `access_id` | Access ID. |
| `action` | Type of action performed, such as list items, create item, or get item. For common actions, see [Log Actions](https://docs.akeyless.io/docs/log-actions). |
| `item_type` | If the action is item-specific (for example, create item), the item type is listed. |
| `status` | Standard HTTP status code: informational (`100`-`199`), success (`200`-`299`), redirection (`300`-`399`), or client error (`400`-`499`). |
| `remote_addr` | IP address from which the action was performed. |
| `duration` | Duration of the action in milliseconds. |
| `request_parameters` | Additional action details, such as dynamic secret details when a value is fetched. |
| `unique_id` | Identifier for the specific user under the account (mostly relevant for human-to-machine auth methods). |
| `client_sub_claims` | Sub-claims captured for the authenticated client when configured on the authentication method (for example, `email`, `username`, and `uid_comment` for UID token flows). |
| `access_type` | [Authentication Method](https://docs.akeyless.io/docs/access-and-authentication-methods) type used for the action. |
| `product` | Akeyless product associated with the log, such as **Secrets Management**, **Secure Remote Access**, or **Password Management**. |

To enrich Audit Logs with additional token parameters, configure **Audit Log Sub-Claims** on the relevant authentication method. For UID tokens, `uid_comment` is available as a sub-claim key.

## Tutorial

Check out our tutorial video on [Audit Logs, Analytics, and Usage Reports](https://tutorials.akeyless.io/docs/audit-logs-analytics-and-usage-reports).
