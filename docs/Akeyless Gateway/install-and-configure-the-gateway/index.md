---
title: Standalone Gateway
excerpt: Installation
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
      slug: advance-gw-docker-configuration
      title: Advanced Configuration
    - type: basic
      slug: gateway-k8s
      title: Gateway on K8s
---
# Prerequisites

* An [Authentication Method](doc:access-and-authentication-methods). Make sure it has the right [access permission](doc:rbac) to create and manage [Secrets, Keys](doc:manage-your-secrets-overview) & [Targets](doc:targets).

<Callout icon="👍" theme="okay">
  _**Note:** The following example uses the account default [Authentication Method](https://docs.akeyless.io/docs/access-and-authentication-methods). Using the account owner's email and password which has superuser privileges on the account._
</Callout>

* A Linux or a Windows machine with [Docker engine](https://docs.docker.com/get-docker/) installed with a minimum 1 vCPU available with 2GB RAM.

* Network port `8000` on the cluster must be open **only for internal network access**, allowing access to the following services using the corresponding endpoints:

| Service                                              | Endpoint   |
| :--------------------------------------------------- | :--------- |
| [Gateway Console](doc:gateway-configuration-manager) | `/console` |
| [HashiCorp Vault Proxy](doc:hashicorp-vault-proxy)   | `/hvp`     |
| Akeyless V1 REST API                                 | `/api/v1`  |
| Akeyless V2 REST API                                 | `/api/v2`  |
| [KMIP Server](doc:kmip-server)                       | `5696`     |

> 🚧 Warning
>
> Make sure that this server is not globally opened to the public network. Akeyless Gateway requires only connections to Akeyless SaaS Core Services.

# Installation

To install a standalone instance of Akeyless Gateway, run the following command:

```shell Shell
docker run -d -p 8000:8000 -p 5696:5696 --name akeyless-gateway akeyless/base:latest-akeyless
```

After executing the above command, a new container named **akeyless-gateway** should run on Docker (use `docker ps` for confirmation). It contains a single instance of Akeyless Gateway.

To upgrade your current Gateway version, simply restart the container using the `docker restart <container name>` command.

> 📘 Info
>
> In this example, the Gateway was installed without a default Authentication Method as part of the installation. Thus, **the first Authentication Method** used to log in will become the admin user on this Gateway.

For further installation options, visit the [Advanced Configuration](advance-gw-docker-configuration) page.

## Initial Configuration

To configure your Akeyless Gateway:

1. On your browser, navigate to [http://Your-Akeyless-Gateway-URL:8000/console](http://Your-Akeyless-Gateway-URL:8000/console) and log in.

2. Navigate to **Gateways > Select Your Gateway > Manage Gateway**

# Tutorial

Check out our tutorial video on [Installing and Configuring the Gateway on Docker](https://tutorials.akeyless.io/docs/installing-and-configuring-akeyless-gateway).
