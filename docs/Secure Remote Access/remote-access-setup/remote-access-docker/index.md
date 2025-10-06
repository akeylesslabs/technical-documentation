---
title: Remote Access on Docker Compose
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
Akeyless Remote Access provides secure remote access to resources using just-in-time credentials (dynamic secrets, rotated secrets, and SSH certificates).

This guide provides instructions on deploying Akeyless Secure Remote Access (SRA) using Docker Compose. The deployment includes the [Akeyless Gateway](https://docs.akeyless.io/docs/install-and-configure-the-gateway#/), SRA Web UI, SRA SSH Proxy, and a Redis cache for performance optimization

# Prerequisites

> ⚠️ Intended use & production guidance
>
> The purpose of the Docker Compose is mainly for
>
> * Evaluation of Akeyless Gateway and SRA quickly on a single host
> * Demo/POC workflows (API, Web SRA, SSH proxy)
> * Small pilots with limited users/targets where downtime is acceptable
>
> For more information please refer to [Readme.md](https://github.com/akeylesslabs/docker-compose/blob/main/README.md) file

* Docker Installed (version 20.10 or later)
* Docker Compose (version 1.29 or later)
* [Gateway](https://docs.akeyless.io/docs/gateway-compose#/) deployed and Unified value is set to TRUE
  * Make sure to set the UNIFIED_GATEWAY=true in both Gateway & SRA env files.
* Environment variables configured in .env files
* [SSH Certificate Issuer](https://dash.readme.com/project/akeyless/v1.0/docs/ssh-certificates) for CLI Access.
* At least 1 vCPU available with 1GB RAM per Docker container.

<Callout icon="🌐" theme="default">
  ### Network Configuration

  * Ensure _sticky sessions_ are enabled.
  * Cloud Provider Load Balancer: Configure the load balancer to support sticky sessions. For example, in AWS, you can use Elastic Load Balancer (ELB). Refer to the AWS ELB Sticky Sessions Documentation for guidance.
</Callout>

* When SSH sessions are routed through a load balancer, such as ELB, they may be disconnected due to idle connection timeouts. To avoid this, we recommend increasing the idle timeout to a higher value or setting it to unlimited.
* For AWS ELB, you can adjust the idle timeout settings as outlined in the AWS ELB Idle Timeout Documentation.

# Deployment Overview

The Docker Compose file defines the following services:

| Service                                                             | Description                                       | Ports                       |
| :------------------------------------------------------------------ | :------------------------------------------------ | :-------------------------- |
| [Akeyless Gateway](https://docs.akeyless.io/docs/gateway-compose#/) | Central access control and authentication gateway | 8000 (API), 8080 (Health)   |
| SRA Web                                                             | Web-based Zero Trust portal for remote access     | As specified in YAML        |
| SRA SSH Proxy                                                       | Secure SSH-based remote access                    | 2222 (SSH), 9900 (Internal) |

Each service runs within an isolated Docker bridge network (internal-net), ensuring secure internal communication.

# Configuration

The deployment uses number of environment files for configuration:

* `gateway.env` - Defines environment variables for Akeyless Gateway. For more information on deployment of Gateway via Docker Compose, please refer to [Gateway documentation](https://docs.akeyless.io/docs/gateway-compose#/).
* `sra.env` - Defines environment variables for Secure Remote Access services.

## Example Configuration

`sra.env`

```shell
#############################################
# Akeyless Gateway + SRA (.env)
# Notes:
# - Keep URLs reachable only within your network/cluster.
# - Keep service names aligned with your Compose/K8s services.
#############################################

## ── Modes & Feature Toggles ───────────────────────────────────────────────────
# UNIFIED_GATEWAY: Enables unified Akeyless Gateway mode
UNIFIED_GATEWAY="true"

# USE_CLUSTER_CACHE: use Redis caching for the Akeyless Gateway
# Best practice: set to "true" when Redis is available
USE_CLUSTER_CACHE="true"

# REMOTE_ACCESS_TYPE: Choose the SRA integration flow (e.g., "ssh-proxy" for Web-SSH)
REMOTE_ACCESS_TYPE="ssh-proxy"


## ── Gateway Endpoints ─────────────────────────────────────────────────────────
# Public/cluster URL for clients reaching the Gateway (port 8000 by default)
GATEWAY_URL=http://akeyless-gateway:8000

# Internal API endpoint (port 8080) used for Gateway health checks or internal calls
INTERNAL_GATEWAY_API=http://akeyless-gateway:8080


## ── SRA Web-SSH (Default) ─────────────────────────────────────────────────────
# Internal URL for the SRA service (SSH proxy) used by the Gateway to route SSH traffic
# Default port for the Web-SSH service: 9900
REMOTE_ACCESS_SSH_SERVICE_INTERNAL_URL=http://akeyless-ssh:9900

# Actual SSH endpoint (container name and port 22 by default)
REMOTE_ACCESS_SSH_ENDPOINT=akeyless-ssh:22


## ── SSH Security ──────────────────────────────────────────────────────────────
# SSH_HOST_KEYS_PATH: Path to persistent host keys (recommended to persist!)
# See: https://docs.akeyless.io/docs/remote-access-advanced-configuration-docker#ssh-fingerprint
# Leave empty to use container defaults; set a volume path to persist across restarts.
SSH_HOST_KEYS_PATH=""
```

> 🚧 Restricting User Access
>
> To enable only specific users to use Secure Remote Access, make sure to add the relevant `GATEWAY_AUTHORIZED_ACCESS_ID` in the `sra.env `file.
>
> A comma-separated list can be used for multiple IDs. While this is not mandatory, it is a good security practice to limit user access. If not configured, a Warning message will appear.

In order to provide just-in-time native CLI access for your users using SSH Certificates, you should mount your `ca.pub` file to `/var/akeyless/creds/` inside of the `akeyless-ssh` component. To do this, provide a local directory which contains your `ca.pub` file which you created as part of your [SSH Certificate Issuer](https://docs.akeyless.io/docs/ssh-certificates) creation.

> 📘 Creating a public key
>
> If you don't have an SSH certificate ready, please follow this guide on creating [SSH Cert issuer](https://docs.akeyless.io/docs/ssh-certificates) with Akeyless and set your `ca.pub`.

# Running the Deployment

1. Ensure you have the `docker-compose.yml` and`.env`files are in your working directory.
2. Start the Services

### Deploying as Secure Remote Access (SRA)

To deploy only the SRA components, run:

```shell
docker-compose --profile sra up -d
```

The above command will deploy SRA (if Gateway is not deployed, it will deploy this as well).

> 📘 Verify Deployment
>
> Check that the deployed containers are running with `docker ps `

To stop and remove all services, run:

```shell
docker-compose down
```

# Getting Started

Once Gateway & SRA are deployed, you can open SRA Web at `http://localhost:8000/sra/portal` and use your credentials to login to the local SRA portal.
