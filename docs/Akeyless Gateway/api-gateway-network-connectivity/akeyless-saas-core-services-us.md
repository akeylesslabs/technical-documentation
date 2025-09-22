---
title: US SaaS Core Services
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
The following table describes the main functionality of Akeyless microservices in the **US** environment:

[block:parameters]
{
  "data": {
    "h-0": "**Service**",
    "h-1": "**IP**",
    "h-2": "**Port**",
    "h-3": "**Description**",
    "0-0": "**Console:**  \n  \n<https://console.us.akeyless.io>",
    "0-1": "34.49.227.83",
    "0-2": "443",
    "0-3": "Akeyless SaaS Platform",
    "1-0": "**Vault:**  \n  \n<https://vault.us.akeyless.io>  \n<https://vault-ro.us.akeyless.io>",
    "1-1": "34.49.234.6,  \n34.49.227.83",
    "1-2": "443",
    "1-3": "User Account Management (UAM), managing user accounts, items, and roles",
    "2-0": "**Auth:**  \n  \n<https://auth.us.akeyless.io>  \n<https://auth-ro.us.akeyless.io>",
    "2-1": "34.49.234.6, 34.49.227.83",
    "2-2": "443",
    "2-3": "Akeyless Authentication service",
    "3-0": "**Certificate Auth:**  \n  \n <https://auth-cert.us.akeyless.io>",
    "3-1": "104.198.48.39",
    "3-2": "443",
    "3-3": "Relevant only for Certificate Based Auth",
    "4-0": "**Audit:**  \n  \n<https://audit.us.akeyless.io>  \n<https://audit-ro.us.akeyless.io>",
    "4-1": "34.49.234.6, 34.49.227.83",
    "4-2": "443",
    "4-3": "Audit log main service, enables log forwarding from GW & Bastion",
    "5-0": "**BIS:**  \n  \n<https://bis.us.akeyless.io>  \n<https://bis-ro.us.akeyless.io>",
    "5-1": "34.49.234.6, 34.49.227.83",
    "5-2": "443",
    "5-3": "Billing Infrastructure Service (BIS)",
    "6-0": "**Gator:**  \n  \n<https://gator.us.akeyless.io>  \n<https://gator-ro.us.akeyless.io>",
    "6-1": "34.49.234.6, 34.49.227.83",
    "6-2": "443",
    "6-3": "Main service to sync gateways instances, and connections with Akeyless SaaS",
    "7-0": "**MQ:**  \n  \namqps://mq.us.akeyless.io",
    "7-1": "34.132.72.118",
    "7-2": "5671",
    "7-3": "Message queue between Akeyless micro-services",
    "8-0": "**KFM:**  \n  \n<https://kfm1.us.akeyless.io>,  \n<https://kfm1-ro.us.akeyless.io>,  \n<https://kfm2.us.akeyless.io>,  \n<https://kfm2-ro.us.akeyless.io>,  \n<https://kfm3.us.akeyless.io>,  \n<https://kfm3-ro.us.akeyless.io>,  \n<https://kfm4.us.akeyless.io>,  \n<https://kfm4-ro.us.akeyless.io>",
    "8-1": "34.49.234.6,  \n34.49.227.83",
    "8-2": "443",
    "8-3": "Key Fragments Services, enabling full DFC encryption",
    "9-0": "**Public Gateway:**  \n  \n<https://rest.us.akeyless.io>  \n<https://api.us.akeyless.io>",
    "9-1": "34.49.33.88",
    "9-2": "443",
    "9-3": "Optional Public Gateway rest API v1\\\\v2",
    "10-0": "**Public HVP:**  \n  \n<https://hvp.us.akeyless.io>",
    "10-1": "34.49.33.88",
    "10-2": "",
    "10-3": "Optional Public HVP endpoint",
    "11-0": "**Logs:**  \n  \ntcp://log.akeyless.io:9997 tcp://log.akeyless.io:9443",
    "11-1": "N/A",
    "11-2": "9997, 9443",
    "11-3": "GW logs, mainly to be reflected during failure scenarios",
    "12-0": "<https://akeyless-cli.s3.us-east-2.amazonaws.com>",
    "12-1": "N/A",
    "12-2": "443",
    "12-3": "S3 bucket to download & update Akeyless CLI versions",
    "13-0": "<https://akeylessservices.s3.us-east-2.amazonaws.com>",
    "13-1": "N/A",
    "13-2": "443",
    "13-3": "S3 bucket to download & update Akeyless official binaries. e.g. `Gateway`"
  },
  "cols": 4,
  "rows": 14,
  "align": [
    "left",
    "left",
    "left",
    "left"
  ]
}
[/block]