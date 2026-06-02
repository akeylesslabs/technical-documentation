---
title: Analytics
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
Akeyless Platform provides rich analytics functionality, allowing the user to analyze the status of his secret posture in various environments with a high-level view.

The main screen tab provides information about items, such as Secrets and Keys where the screen is divided into the following parts:

* A geographic map presenting the IP addresses that consume secrets
* Pie chart that represents the division of the requests by the action type, and below the exact number of operations
* Request volume in the allocated timeframe
* Request time by action type (latency)

The user can change the timeframe for which the data is presented.

Usage Reports include a contract start date indicator for the requested product.

![Illustration for: Request volume in the allocated timeframe](https://files.readme.io/7469f53-Screenshot_at_Nov_23_14-36-38.png)

Navigate to the **Certificates** tab to get an immediate overview of your certificate's status with additional details on future expiration.

![Illustration for: The user can change the timeframe for which the data is presented.](https://files.readme.io/f7946c8-Screenshot_at_Nov_23_15-02-11.png)

On the **Certificate Expiry** graph, click on the **Overview** button in the top right corner to get a detailed overview of all your certificate and their expiration details.

> ℹ️ **Note:** Analytics data is generated asynchronously, so recent activity may take time to appear in the report.

For CLI usage, run the following command:

```shell
akeyless get-analytics-data
```

See the [CLI Reference entry for get-analytics-data](https://docs.akeyless.io/docs/cli-reference#get-analytics-data) for more details.

> ℹ️ **Note:** Data in the Analytics report includes items stored in [Personal Folders](https://docs.akeyless.io/docs/personal-corporate-areas-navigation).

## Tutorial

Check out our tutorial video on [Audit Logs, Analytics, and Usage Reports](https://tutorials.akeyless.io/docs/audit-logs-analytics-and-usage-reports).
