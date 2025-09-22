---
title: Akeyless SaaS Core Services
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
The Akeyless Gateway is a stateless Docker container, provided as a standalone or as a cluster. To function correctly, it requires public network connectivity to the Akeyless SaaS core services (see the table below).

A basic Gateway deployment requires a server with a Docker engine installed. You may download the latest Docker engine on [Docker website](https://docs.docker.com/get-docker/). You'll need public network access enabled on port 443 to pull a Docker image from the `hub.docker.com`.

> 📘 Tenant Environments
> 
> Accounts that were created on specific environments should modify the services endpoints according to the relevant environments. e.g. for `eu`  `https://vault.eu.akeyless.io`  etc.
> 
> Available explicit tenates are: `us`,`eu` .

The following table describes the main functionality of Akeyless microservices in the global environment:

[block:parameters]
{
  "data": {
    "h-0": "Service ",
    "h-1": "IP",
    "h-2": "Port",
    "h-3": "Description",
    "0-0": "**Console**:  <https://console.akeyless.io>",
    "0-1": "52.223.11.194, 35.71.185.167, 52.223.35.208, 35.71.147.131, 15.197.228.204, 3.33.247.128",
    "0-2": "443",
    "0-3": "Akeyless SaaS platform",
    "1-0": "**Vault** : <https://vault.akeyless.io>  \n<https://vault-ro.akeyless.io>",
    "1-1": "52.223.11.194, 35.71.185.167, 52.223.35.208, 35.71.147.131, 15.197.228.204, 3.33.247.128",
    "1-2": "443",
    "1-3": "User Account Management (UAM), managing user accounts,  items, and roles",
    "2-0": "**Auth** : <https://auth.akeyless.io>  \n<https://auth-ro.akeyless.io>",
    "2-1": "52.223.11.194, 35.71.185.167, 52.223.35.208, 35.71.147.131, 15.197.228.204, 3.33.247.128",
    "2-2": "443",
    "2-3": "Akeyless Authentication service",
    "3-0": "**Certificate Auth** <https://auth-cert.akeyless.io>",
    "3-1": "18.189.176.104",
    "3-2": "443",
    "3-3": "Relevant only for Certificate Based Auth ",
    "4-0": "**Audit** : <https://audit.akeyless.io>  \n<https://audit-ro.akeyless.io>",
    "4-1": "52.223.11.194, 35.71.185.167, 52.223.35.208, 35.71.147.131, 15.197.228.204, 3.33.247.128",
    "4-2": "443",
    "4-3": "Audit log main service, enables log forwarding from GW & Bastion",
    "5-0": "**BIS** : <https://bis.akeyless.io>  \n<https://bis-ro.akeyless.io>",
    "5-1": "52.223.11.194, 35.71.185.167",
    "5-2": "443",
    "5-3": "Billing Infrastructure Service (BIS)",
    "6-0": "**Gator** : <https://gator.akeyless.io>  \n<https://gator-ro.akeyless.io>",
    "6-1": "52.223.11.194, 35.71.185.167, 52.223.35.208, 35.71.147.131, 15.197.228.204, 3.33.247.128",
    "6-2": "443",
    "6-3": "Main service to sync gateways instances, and connections with Akeyless SaaS",
    "7-0": "**MQ** : amqps://mq.akeyless.io",
    "7-1": "52.223.11.194, 35.71.185.167",
    "7-2": "5671",
    "7-3": "Message queue between Akeyless micro-services",
    "8-0": "**KFM**: <https://kfm1.akeyless.io>,  \n<https://kfm1-ro.akeyless.io>,  \n<https://kfm2.akeyless.io>,  \n<https://kfm2-ro.akeyless.io>,  \n<https://kfm3.akeyless.io>,  \n<https://kfm3-ro.akeyless.io>,  \n<https://kfm4.akeyless.io>,  \n<https://kfm4-ro.akeyless.io>",
    "8-1": "52.223.11.194, 35.71.185.167, 52.223.35.208, 35.71.147.131, 15.197.228.204, 3.33.247.128, 34.120.160.242",
    "8-2": "443",
    "8-3": "Key Fragments Services, enabling full DFC encryption",
    "9-0": "**Public Gateway**:  \n<https://rest.akeyless.io>  \n<https://api.akeyless.io>",
    "9-1": "15.197.223.248, 3.33.244.138",
    "9-2": "443",
    "9-3": "**Optional** Public Gateway rest API v1\\\\v2",
    "10-0": "**Public HVP**:  \n<https://hvp.akeyless.io>",
    "10-1": "15.197.223.248, 3.33.244.138",
    "10-2": "443",
    "10-3": "**Optional** Public HVP endpoint",
    "11-0": "**Logs** : tcp://log.akeyless.io:9997 tcp://log.akeyless.io:9443",
    "11-1": "35.192.171.171",
    "11-2": "9997, 9443",
    "11-3": "GW logs, mainly to be reflected during failure scenarios",
    "12-0": "<https://akeyless-cli.s3.us-east-2.amazonaws.com>",
    "12-1": "N\\\\A",
    "12-2": "443",
    "12-3": "S3 bucket to download & update Akeyless CLI versions",
    "13-0": "<https://akeylessservices.s3.us-east-2.amazonaws.com>",
    "13-1": "N\\\\A",
    "13-2": "443",
    "13-3": "S3 bucket to download & update Akeyless official binaries. e.g. `Gateway`",
    "14-0": "<https://artifacts.site2.akeyless.io>",
    "14-1": "34.149.100.205",
    "14-2": "443",
    "14-3": "**Optional** Akeyless official artifacts endpoint. Relevant when working with whitelisted IP range"
  },
  "cols": 4,
  "rows": 15,
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
> When using proxy services, you can use **<https://sqs.us-east-2.amazonaws.com>** instead of classic MQ services. In case you are not working with proxy serivce, and still want to utilize SQS insted of classic MQ , set your **Gateway**  deployment with the `SQS_NO_PROXY="true"` environment variable.

# Working without MQ Connection

If your organization's policies restrict non-web ports, it's important to understand the potential implications of blocking the MQ connection for your Akeyless setup:

- **Cross Gateway Access**: The MQ service enables retrieving Gateways secrets and objects (i.e. Dynamic/Rotated Secrets, Classic Keys, etc.) across different Gateways and the Akeyless SaaS console. If MQ is blocked, you can still retrieve those secrets directly from their own Gateway. However, requests from other Gateways or the SaaS console will not be processed.
- **Operational Adjustments**: Without the MQ service, you will need to ensure you are working directly with the correct Gateway for each relevant item. This may require additional manual oversight and adjustments compared to a setup with MQ enabled.
- **Centralized Management**: The MQ service allows for centralized management, enabling you to perform all operations from the SaaS console. If MQ is blocked, this convenience will not be available, and you will need to interact directly with individual Gateways.
- [Event Forwarding](https://docs.akeyless.io/docs/event-center#event-forwarders) relies on the MQ service for publishing event messages to the Gateway. Blocking the MQ connection will prevent event forwarding from working.