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
---
Akeyless collects detailed audit logs per secret type, operation, user, time, etc. 

Akeyless audit logs take note of just about every change\\action within the Akeyless system, providing a complete track record of your Akeyless system operations. Therefore, Akeyless audit logs are a valuable resource for Akeyless admins and auditors who want to examine suspicious activity on Akeyless or diagnose and troubleshoot issues. 

These audit logs can give an Akeyless administrator invaluable insight into what behavior is normal and what behavior isn’t. A log event, for example, will show what activity was attempted and whether it succeeded. This can be useful when identifying whether a system component is misconfigured or likely to fail.

Akeyless log auditing is important for cybersecurity because it provides records that can serve as evidence. A comprehensive and in-depth log audit can make all the difference in the event of a legal battle and can protect your business from liability.

# Viewing Logs in the Console

When using the console, you will be able to navigate to the **Audit Logs** tab to view logs in the following format:

[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/800a8f4-Screenshot_at_Nov_10_13-44-36.png",
        "Screenshot at Nov 10 13-44-36.png",
        1912
      ],
      "align": "center",
      "caption": "Example of Akeyless Audit log"
    }
  ]
}
[/block]


These logs show you the time of the described action, what it was, whether it was successful or unsuccessful (status in the 400s means error), the client performing it, what IP it was performed from, and additional parameter tags such as access type or product type.

You will be able to filter your logs based on any of these rubricks or tags inside the Akeyless SaaS platform in order to get insights or clarifications.

# Reading the Raw Logs

Another way to view your logs is to forward them in their raw form to tools such as Splunk, Logz.io, etc.  
The logs will show up as a line of text, from which you will be able to read the following information:

| Log Line             | Description                                                                                                                                                                               |
| :------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `Timestamp`          | The log will start with a timestamp string in the format of Date `T` Time Timezone.                                                                                                       |
| `account_id`         | Account ID.                                                                                                                                                                               |
| `access_id`          | Access ID.                                                                                                                                                                                |
| `action`             | The type of action performed, for example, list items, create item, get item, etc. A list of common log items can be found [here](doc:log-actions)                                        |
| `item_type`          | If the action was item specific, like create item, the item type will be listed here.                                                                                                     |
| `status`             | Standard HTTP status code of the following types, Informational responses (100–199), Successful responses (200–299), Redirection messages (300–399), or Client error responses (400–499). |
| `remote_addr`        | The IP address from which the action was performed.                                                                                                                                       |
| `duration`           | The duration of the action in milliseconds.                                                                                                                                               |
| `request_parameters` | More details about the action, for example, the name and details of a dynamic secret if one was fetched.                                                                                  |
| `unique_id`          | Identifier for the specific user id under the account (mostly relevant for human-to-machine auth methods).                                                                                |
| `access_type`        | [Authentication Method](doc:access-and-authentication-methods) type from which the action was performed.                                                                                  |
| `product`            | Which Akeyless product does this log concern. For example, currently this could be **Secrets Management**, **Secure Remote Access**, or **Password Management**.                          |

# Tutorial

Check out our tutorial video on <a href="https://tutorials.akeyless.io/docs/audit-logs-analytics-and-usage-reports" target="_blank" style="color: #00e">Audit Logs, Analytics, and Usage Reports</a>.