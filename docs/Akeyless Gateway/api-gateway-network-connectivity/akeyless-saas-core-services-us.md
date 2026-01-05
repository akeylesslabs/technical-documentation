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

| Service | Endpoint | IP | Port | Description |
|---|---|---|---|---|
| Console | `https://console.us.akeyless.io` | 4.242.224.82 | 443 | Akeyless SaaS Platform |
| Vault | `https://vault.us.akeyless.io`, `https://vault-ro.us.akeyless.io` | 68.154.26.48, 4.242.224.82 | 443 | User Account Management (UAM), managing user accounts, items, and roles |
| Auth | `https://auth.us.akeyless.io`, `https://auth-ro.us.akeyless.io` | 68.154.26.48, 4.242.224.82 | 443 | Akeyless Authentication service |
| Certificate Auth | `https://auth-cert.us.akeyless.io` | 172.206.81.32 | 443 | Relevant only for certificate-based authentication |
| Audit | `https://audit.us.akeyless.io`, `https://audit-ro.us.akeyless.io` | 68.154.26.48, 4.242.224.82 | 443 | Audit log main service, enables log forwarding from GW and Bastion |
| BIS | `https://bis.us.akeyless.io`, `https://bis-ro.us.akeyless.io` | 68.154.26.48, 4.242.224.82 | 443 | Billing Infrastructure Service (BIS) |
| Gator | `https://gator.us.akeyless.io`, `https://gator-ro.us.akeyless.io` | 68.154.26.48, 4.242.224.82 | 443 | Main service to sync gateway instances and connections with Akeyless SaaS |
| MQ | `amqps://mq.us.akeyless.io` | 172.177.144.122 | 5671 | Message queue between Akeyless microservices |
| KFM | `https://kfm1.us.akeyless.io`, `https://kfm1-ro.us.akeyless.io`, `https://kfm2.us.akeyless.io`, `https://kfm2-ro.us.akeyless.io`, `https://kfm3.us.akeyless.io`, `https://kfm3-ro.us.akeyless.io`, `https://kfm4.us.akeyless.io`, `https://kfm4-ro.us.akeyless.io` | 68.154.26.48, 4.242.224.82 | 443 | Key Fragments Services, enabling full DFC encryption |
| Public Gateway | `https://rest.us.akeyless.io`, `https://api.us.akeyless.io` | 68.154.26.48, 4.242.224.82 | 443 | Optional Public Gateway REST API v1/v2 |
| Public HashiCorp Vault Proxy | `https://hvp.us.akeyless.io` | 68.154.26.48 | (none) | Optional Public HashiCorp Vault Proxy endpoint |
| Logs | `tcp://log.akeyless.io:9997`, `tcp://log.akeyless.io:9443` | N/A | 9997, 9443 | GW logs, mainly to be reflected during failure scenarios |
| Akeyless CLI | `https://akeyless-cli.s3.us-east-2.amazonaws.com` | N/A | 443 | S3 bucket to download and update Akeyless CLI versions |
| Akeyless Binaries | `https://akeylessservices.s3.us-east-2.amazonaws.com` | N/A | 443 | S3 bucket to download and update Akeyless official binaries (for example, `Gateway`) |
