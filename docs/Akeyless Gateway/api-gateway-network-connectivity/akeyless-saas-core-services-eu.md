---
title: EU SaaS Core Services
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
The following table describes the main functionality of Akeyless microservices in the **EU** environment:

[block:parameters]
{
  "data": {
    "h-0": "**Service**",
    "h-1": "**IP**",
    "h-2": "**Port**",
    "h-3": "**Description**",
    "0-0": "**Console:**  \n  \n<https://console.eu.akeyless.io>",
    "0-1": "13.248.216.215,  \n76.223.80.182",
    "0-2": "443",
    "0-3": "Akeyless SaaS Platform",
    "1-0": "**Vault:**  \n  \n<https://vault.eu.akeyless.io>  \n<https://vault-ro.eu.akeyless.io>",
    "1-1": "3.33.166.129,  \n15.197.166.202",
    "1-2": "443",
    "1-3": "euer Account Management (UAM), managing euer accounts, items, and roles",
    "2-0": "**Auth:**  \n  \n<https://auth.eu.akeyless.io>  \n<https://auth-ro.eu.akeyless.io>",
    "2-1": "3.33.166.129,  \n15.197.166.202,  \n13.248.216.215,  \n76.223.80.182",
    "2-2": "443",
    "2-3": "Akeyless Authentication service",
    "3-0": "**Certificate Auth:**  \n  \n <https://auth-cert.eu.akeyless.io>",
    "3-1": "18.158.96.32,  \n3.68.125.9,  \n52.28.6.110",
    "3-2": "443",
    "3-3": "Relevant only for Certificate Based Auth",
    "4-0": "**Audit:**  \n  \n<https://audit.eu.akeyless.io>  \n<https://audit-ro.eu.akeyless.io>",
    "4-1": "15.197.166.202,  \n3.33.166.129,  \n13.248.216.215,  \n76.223.80.182",
    "4-2": "443",
    "4-3": "Audit log main service, enables log forwarding from GW & Bastion",
    "5-0": "**BIS:**  \n  \n<https://bis.eu.akeyless.io>  \n<https://bis-ro.eu.akeyless.io>",
    "5-1": "15.197.166.202,  \n3.33.166.129",
    "5-2": "443",
    "5-3": "Billing Infrastructure Service (BIS)",
    "6-0": "**Gator:**  \n  \n<https://gator.eu.akeyless.io>  \n<https://gator-ro.eu.akeyless.io>",
    "6-1": "3.33.166.129,  \n15.197.166.202,  \n76.223.80.182,  \n13.248.216.215",
    "6-2": "443",
    "6-3": "Main service to sync gateways instances, and connections with Akeyless SaaS",
    "7-0": "**MQ:**  \n  \namqps://mq.eu.akeyless.io",
    "7-1": "15.197.166.202,  \n3.33.166.129",
    "7-2": "5671",
    "7-3": "Message queue between Akeyless micro-services",
    "8-0": "**KFM:**  \n  \n<https://kfm1.eu.akeyless.io>,  \n<https://kfm1-ro.eu.akeyless.io>,  \n<https://kfm2.eu.akeyless.io>,  \n<https://kfm2-ro.eu.akeyless.io>,  \n<https://kfm3.eu.akeyless.io>,  \n<https://kfm3-ro.eu.akeyless.io>,  \n<https://kfm4.eu.akeyless.io>,  \n<https://kfm4-ro.eu.akeyless.io>",
    "8-1": "3.33.166.129,  \n15.197.166.202,  \n76.223.80.182,  \n13.248.216.215",
    "8-2": "443",
    "8-3": "Key Fragments Services, enabling full DFC encryption",
    "9-0": "**Public Gateway:**  \n  \n<https://rest.eu.akeyless.io>  \n<https://api.eu.akeyless.io>",
    "9-1": "3.33.196.150,  \n15.197.225.215",
    "9-2": "443",
    "9-3": "Optional Public Gateway rest API v1\\\\v2",
    "10-0": "**Public HVP:**  \n  \n<https://hvp.eu.akeyless.io>",
    "10-1": "3.33.196.150,  \n15.197.225.215",
    "10-2": "443",
    "10-3": "Optional Public HVP endpoint",
    "11-0": "**Logs:**  \n  \ntcp://log.eu.akeyless.io:9997 tcp://log.eu.akeyless.io:9443",
    "11-1": "3.124.145.245",
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




> 👍 Note
> 
> When using proxy services, you can use **<https://sqs.eu-central-1.amazonaws.com>** instead of classic MQ services. In case you are not working with proxy serivce, and still want to utilize SQS insted of classic MQ , set your **Gateway**  deployment with the `SQS_NO_PROXY="true"` environment variable.