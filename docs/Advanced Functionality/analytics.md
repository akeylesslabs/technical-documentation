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
Akeyless Platform provides rich analytics functionality, allowing the user to analyze the status of his secret posture in various environments from a bird's eye view.

The main screen tab provides information mostly for **Secret & Keys** where the screen is divided into the following parts:

* A geographic map presenting the IP addresses that consume secrets
* Pie chart that represents the division of the requests by the action type, and below the exact number of operations
* Request volume in the allocated timeframe
* Request time by action type (latency)

The user can change the timeframe for which the data is presented.

<Image align="center" src="https://files.readme.io/7469f53-Screenshot_at_Nov_23_14-36-38.png" />

<br />

Navigate to the **Certificates** tab to get an immediate overview of your certificate's status with additional details on future expiration.

<Image align="center" src="https://files.readme.io/f7946c8-Screenshot_at_Nov_23_15-02-11.png" />

On the **Certificate Expiry** graph, click on the **Overview** button in the top right corner to get a detailed overview of all your certificate and their expiration details.

To get the Analytic data using a CLI command run the following command:

```shell CLI
akeyless get-analytics-data
```

# Tutorial

Check out our tutorial video on <a href="https://tutorials.akeyless.io/docs/audit-logs-analytics-and-usage-reports" target="_blank" style={{ color: "#00e" }}>Audit Logs, Analytics, and Usage Reports</a>.