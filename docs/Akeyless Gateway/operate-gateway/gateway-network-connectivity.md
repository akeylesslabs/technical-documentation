---
title: Gateway Network Connectivity
deprecated: false
hidden: false
link:
  new_tab: false
metadata:
  title: ''
  description: ''
  robots: index
---
The Akeyless Gateway is a stateless Docker container, provided as a standalone or as a cluster. To function correctly, it requires public network connectivity to the Akeyless SaaS core services (see the table below).

A basic Gateway deployment requires a server with a Docker Engine installed. You may download the latest Docker Engine on [Docker website](https://docs.docker.com/get-docker/). You'll need public network access enabled on port 443 to pull a Docker image from the `hub.docker.com`.

> ℹ️ **Note (Tenant Environments):**
>
> Accounts that were created on specific environments should modify the services endpoints according to the relevant environments, for example, `eu` would use `https://vault.eu.akeyless.io`.
>
> Available explicit tenants are: `us`, `eu`.

The following table describes the main functionality of Akeyless microservices in the global environment:

| Service | Endpoints | IP | Port | Description |
| --- | --- | --- | --- | --- |
| Console | `https://console.akeyless.io` | 52.223.11.194, 35.71.185.167, 52.223.35.208, 35.71.147.131, 15.197.228.204, 3.33.247.128 | 443 | Akeyless SaaS platform |
| Vault | `https://vault.akeyless.io`, `https://vault-ro.akeyless.io` | 52.223.11.194, 35.71.185.167, 52.223.35.208, 35.71.147.131, 15.197.228.204, 3.33.247.128 | 443 | User Account Management (UAM), managing user accounts, items, and roles |
| Auth | `https://auth.akeyless.io`, `https://auth-ro.akeyless.io` | 52.223.11.194, 35.71.185.167, 52.223.35.208, 35.71.147.131, 15.197.228.204, 3.33.247.128 | 443 | Akeyless Authentication service |
| Certificate Auth | `https://auth-cert.akeyless.io` | 18.189.176.104 | 443 | Relevant only for certificate-based authentication |
| Audit | `https://audit.akeyless.io`, `https://audit-ro.akeyless.io` | 52.223.11.194, 35.71.185.167, 52.223.35.208, 35.71.147.131, 15.197.228.204, 3.33.247.128 | 443 | Audit log main service, enables log forwarding from GW and Bastion |
| BIS | `https://bis.akeyless.io`, `https://bis-ro.akeyless.io` | 52.223.11.194, 35.71.185.167 | 443 | Billing Infrastructure Service (BIS) |
| Gator | `https://gator.akeyless.io`, `https://gator-ro.akeyless.io` | 52.223.11.194, 35.71.185.167, 52.223.35.208, 35.71.147.131, 15.197.228.204, 3.33.247.128 | 443 | Main service to sync gateway instances and connections with Akeyless SaaS |
| MQ | `amqps://mq.akeyless.io` | 52.223.11.194, 35.71.185.167 | 5671 | Message queue between Akeyless microservices |
| KFM | `https://kfm1.akeyless.io`, `https://kfm1-ro.akeyless.io`, `https://kfm2.akeyless.io`, `https://kfm2-ro.akeyless.io`, `https://kfm3.akeyless.io`, `https://kfm3-ro.akeyless.io`, `https://kfm4.akeyless.io`, `https://kfm4-ro.akeyless.io` | 52.223.11.194, 35.71.185.167, 52.223.35.208, 35.71.147.131, 15.197.228.204, 3.33.247.128, 34.120.160.242 | 443 | Key Fragments Services, enabling full DFC encryption |
| Public Gateway | `https://rest.akeyless.io`, `https://api.akeyless.io` | 15.197.223.248, 3.33.244.138 | 443 | _Optional:_ Public Gateway REST API v1/v2 |
| Public HashiCorp Vault Proxy | `https://hvp.akeyless.io` | 15.197.223.248, 3.33.244.138 | 443 | _Optional:_ Public HashiCorp Vault Proxy endpoint |
| Logs | `tcp://log.akeyless.io:9997`, `tcp://log.akeyless.io:9443` | 35.192.171.171 | 9997, 9443 | GW logs, mainly used during failure scenarios |
| CLI S3 Bucket | `https://akeyless-cli.s3.us-east-2.amazonaws.com` | N/A | 443 | S3 bucket to download and update Akeyless CLI versions |
| Services S3 Bucket | `https://akeylessservices.s3.us-east-2.amazonaws.com` | N/A | 443 | S3 bucket to download and update Akeyless official binaries (for example, Gateway) |
| Artifacts Endpoint | `https://artifacts.site2.akeyless.io` | 34.149.100.205 | 443 | _Optional:_ Akeyless official artifacts endpoint. Relevant when working with whitelisted IP ranges |

> ℹ️ **Note:**
>
> When using proxy services, you can use `sqs.us-east-2.amazonaws.com` instead of classic MQ services. If you are not working with a proxy service and still want to use SQS instead of classic MQ, set your **Gateway** deployment with the `SQS_NO_PROXY="true"` environment variable.

## Working Without MQ Connection

If your organization's policies restrict non-web ports, it's important to understand the potential implications of blocking the MQ connection for your Akeyless setup:

* **Cross Gateway Access**: The MQ service enables retrieving Gateways secrets and objects (that is Dynamic/Rotated Secrets, Classic Keys, and so on) across different Gateways and the Akeyless SaaS console. If MQ is blocked, you can still retrieve those secrets directly from their own Gateway. However, requests from other Gateways or the SaaS console will not be processed.
* **Operational Adjustments**: Without the MQ service, you will need to ensure you are working directly with the correct Gateway for each relevant item. This may require additional manual oversight and adjustments compared to a setup with MQ enabled.
* **Centralized Management**: The MQ service allows for centralized management, enabling you to perform all operations from the SaaS console. If MQ is blocked, this convenience will not be available, and you will need to interact directly with individual Gateways.
* [Event Forwarding](https://docs.akeyless.io/docs/event-center#event-forwarders) relies on the MQ service for publishing event messages to the Gateway. Blocking the MQ connection will prevent event forwarding from working.
