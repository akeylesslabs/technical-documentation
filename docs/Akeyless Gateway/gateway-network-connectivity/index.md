---
title: gateway-network-connectivity
excerpt: 'Akeyless SaaS Core Services'
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

A basic Gateway deployment requires a server with Docker Engine installed. Download the latest Docker Engine from the [Docker website](https://docs.docker.com/get-docker/).

For deployment instructions, see [Deploy Gateway](https://docs.akeyless.io/docs/deploy-gateway).

> ℹ️ **Note (Tenant Environments):**
>
> Accounts created in a specific tenant environment must use the matching service endpoints. For example, the `eu` tenant uses `https://vault.eu.akeyless.io`.
>
> Available explicit tenants are `us` and `eu`.
>
> * [US SaaS Core Services](https://docs.akeyless.io/docs/akeyless-saas-core-services-us)
> * [EU SaaS Core Services](https://docs.akeyless.io/docs/akeyless-saas-core-services-eu)

The following table describes the main functionality of Akeyless microservices in the global environment:

| Service | Endpoint | IP | Port | Description |
| --- | --- | --- | --- | --- |
| Console | `https://console.akeyless.io` | 52.223.11.194, 35.71.185.167, 52.223.35.208, 35.71.147.131, 15.197.228.204, 3.33.247.128 | 443 | Akeyless SaaS Platform |
| Vault | `https://vault.akeyless.io`, `https://vault-ro.akeyless.io` | 52.223.11.194, 35.71.185.167, 52.223.35.208, 35.71.147.131, 15.197.228.204, 3.33.247.128 | 443 | User Account Management (UAM), managing user accounts, items, and roles |
| Auth | `https://auth.akeyless.io`, `https://auth-ro.akeyless.io` | 52.223.11.194, 35.71.185.167, 52.223.35.208, 35.71.147.131, 15.197.228.204, 3.33.247.128 | 443 | Akeyless Authentication service |
| Certificate Auth | `https://auth-cert.akeyless.io` | 18.189.176.104 | 443 | Relevant only for certificate-based authentication |
| Audit | `https://audit.akeyless.io`, `https://audit-ro.akeyless.io` | 52.223.11.194, 35.71.185.167, 52.223.35.208, 35.71.147.131, 15.197.228.204, 3.33.247.128 | 443 | Audit Log main service, enables log forwarding from Gateway and Bastion |
| BIS | `https://bis.akeyless.io`, `https://bis-ro.akeyless.io` | 52.223.11.194, 35.71.185.167 | 443 | Billing Infrastructure Service (BIS) |
| Gator | `https://gator.akeyless.io`, `https://gator-ro.akeyless.io` | 52.223.11.194, 35.71.185.167, 52.223.35.208, 35.71.147.131, 15.197.228.204, 3.33.247.128 | 443 | Main service to sync gateway instances and connections with Akeyless SaaS |
| MQ | `amqps://mq.akeyless.io` | 52.223.11.194, 35.71.185.167 | 5671 | Message queue (MQ) between Akeyless microservices |
| KFM | `https://kfm1.akeyless.io`, `https://kfm1-ro.akeyless.io`, `https://kfm2.akeyless.io`, `https://kfm2-ro.akeyless.io`, `https://kfm3.akeyless.io`, `https://kfm3-ro.akeyless.io`, `https://kfm4.akeyless.io`, `https://kfm4-ro.akeyless.io` | 52.223.11.194, 35.71.185.167, 52.223.35.208, 35.71.147.131, 15.197.228.204, 3.33.247.128, 34.120.160.242 | 443 | Key Fragments Services, enabling full DFC encryption |
| Public Gateway | `https://rest.akeyless.io`, `https://api.akeyless.io` | 15.197.223.248, 3.33.244.138 | 443 | _Optional:_ Public Gateway REST API v1/v2 |
| Public HashiCorp Vault Proxy | `https://hvp.akeyless.io` | 15.197.223.248, 3.33.244.138 | 443 | _Optional:_ Public HashiCorp Vault Proxy endpoint |
| Logs | `tcp://log.akeyless.io:9443` | 35.192.171.171 | 9443 | Gateway logs over TLS-encrypted Splunk forwarding for global and US environments |
| CLI S3 Bucket | `https://akeyless-cli.s3.us-east-2.amazonaws.com` | N/A | 443 | S3 bucket to download and update Akeyless CLI versions |
| Services S3 Bucket | `https://akeylessservices.s3.us-east-2.amazonaws.com` | N/A | 443 | S3 bucket to download and update Akeyless official binaries (for example, Gateway) |
| Artifacts Endpoint | `https://artifacts.site2.akeyless.io` | 34.149.100.205 | 443 | _Optional:_ Akeyless official artifacts endpoint. Relevant when working with whitelisted IP ranges |

> ℹ️ **Note:**
>
> When using proxy services, you can use `https://sqs.us-east-2.amazonaws.com` instead of classic MQ services. If you are not working with a proxy service and still want to use SQS instead of classic MQ, set your **Gateway** deployment with the `SQS_NO_PROXY="true"` environment variable.
>
> The artifacts endpoint `https://artifacts.site2.akeyless.io` is the documented default repository endpoint in current Gateway chart and CLI references.

## Gateway Inbound Ports

The table below describes common inbound ports on the Gateway service itself.

| Port | Name | Purpose | Required |
| --- | --- | --- | --- |
| 18888 | Web UI | Gateway Web UI | Optional |
| 8000 | Configure App (deprecated) | Redirects to Console app (DOCS-309, Gateway v4.47.0) | Optional |
| 8080 | Legacy API | Akeyless REST API v1 | Optional |
| 8081 | API | Akeyless REST API v2 | Optional |
| 8200 | HashiCorp Vault Proxy | HashiCorp Vault Proxy endpoint | Optional |
| 5696 | KMIP | KMIP service endpoint | Optional |

Use the Akeyless SaaS Console (`https://console.akeyless.io`) or `<gateway-protocol>://<gateway-host>/console` to open the Gateway Console UI entry point. To change Gateway settings, open the **Gateway** tab, select the relevant Gateway, and select **Manage Gateway**. The user must have Gateway-scoped administrative permission (`scope` or `all`) to see the Gateway in the list and manage it. In updated releases, Configure App on port `8000` is deprecated and can redirect to the Console app.

> ℹ️ **Note:**
> The Helm chart values include a `grpc` service port (`8085`). Validate deployment-level listener configuration for your release before exposing this port.

## Proxy Settings and Queue Transport

The Gateway supports outbound proxy settings through the following environment variables:

* `HTTP_PROXY`
* `HTTPS_PROXY`
* `NO_PROXY`

When `HTTP_PROXY` or `HTTPS_PROXY` is set, Gateway queue transport is switched to SQS mode.

If no proxy is configured and you still want to use SQS queue transport, set `SQS_NO_PROXY="true"`.

### Helm Configuration for Queue and Proxy Settings

When deploying with Helm, set `SQS_NO_PROXY` using `env` in your Gateway values file:

```yaml values.yaml
env:
  - name: SQS_NO_PROXY
    value: "true"
```

To configure outbound proxy variables with Helm, set `httpProxySettings` in your values file:

```yaml values.yaml
httpProxySettings:
  http_proxy: "http://proxy.example.internal:3128"
  https_proxy: "http://proxy.example.internal:3128"
  no_proxy: "localhost,127.0.0.1,.svc,.cluster.local"
```

If you set `httpProxySettings.http_proxy` or `httpProxySettings.https_proxy` in Helm values, Gateway queue transport is also switched to SQS mode.

## DNS and Endpoint Resolution

Gateway hosts and pods must be able to resolve all required service hostnames listed on this page.
For Akeyless API host resolution, Gateway routes `GET` requests to `-ro` hostnames and keeps non-`GET` requests on primary hostnames.

If the configured API hostname already includes `-ro`, Gateway does not add the suffix again.

If internal DNS is configured for Akeyless API communication, Gateway skips `-ro` hostname rewriting.

When `AKEYLESS_URL` and `akeyless_url` are not explicitly set, Gateway builds the fallback API URL from the configured protocol and `akeyless_server_dns` (`<protocol>://<akeyless_server_dns>`).

## Working Without MQ Connection

If your organization's policies restrict non-web ports, it's important to understand the potential implications of blocking the MQ connection for your Akeyless setup:

* **Cross Gateway Access**: The MQ service enables retrieving Gateways secrets and objects (that is Dynamic/Rotated Secrets, Classic Keys, and so on) across different Gateways and the Akeyless SaaS console. If MQ is blocked, you can still retrieve those secrets directly from their own Gateway. However, requests from other Gateways or the SaaS console will not be processed.
* **Operational Adjustments**: Without the MQ service, you will need to ensure you are working directly with the correct Gateway for each relevant item. This may require additional manual oversight and adjustments compared to a setup with MQ enabled.
* **Centralized Management**: The MQ service allows for centralized management, enabling you to perform all operations from the SaaS console. If MQ is blocked, this convenience will not be available, and you will need to interact directly with individual Gateways.
* [Event Forwarding](https://docs.akeyless.io/docs/event-center#event-forwarders) relies on the MQ service for publishing event messages to the Gateway. Blocking the MQ connection will prevent event forwarding from working.
