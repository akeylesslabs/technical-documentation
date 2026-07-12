---
title: Standalone Docker Deployment
slug: gateway-deploy-standalone-docker
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
      slug: gateway-docker-advanced-configuration
      title: Gateway Docker Advanced Configuration
    - type: basic
      slug: gateway-deploy-docker-compose
      title: Docker Compose Deployment
    - type: basic
      slug: gateway-deploy-kubernetes-helm
      title: Kubernetes with Helm Deployment
---
## Prerequisites

* An [Authentication Method](https://docs.akeyless.io/docs/access-and-authentication-methods). For Gateway Console (UI) access, the admin role must include an RBAC Administrative rule scoped to Gateway management, with permission scope set to `scope` or `all`. CLI and API management can still be allowed when the role grants the required permissions.

> ℹ️ **Note:** The following example uses the account default [Authentication Method](https://docs.akeyless.io/docs/access-and-authentication-methods), using the account owner's email and password with superuser privileges on the account.

* A Linux or a Windows machine with [Docker Engine](https://docs.docker.com/get-docker/) installed with a minimum 1 vCPU available with 2 GB RAM.

* Network port `8000` on the cluster must be open **only for internal network access**, allowing access to the following services using the corresponding endpoints:

| Service | Endpoint |
| --- | --- |
| [Gateway Console](https://docs.akeyless.io/docs/configure-gateway) | `/console` |
| [HashiCorp Vault Proxy](https://docs.akeyless.io/docs/hashicorp-vault-proxy) | `/hvp` |
| Akeyless V1 REST API | `/api/v1` |
| Akeyless V2 REST API | `/api/v2` |
| [KMIP Server](https://docs.akeyless.io/docs/kmip-server) | `5696` |

> ⚠️ **Warning:**
>
> Make sure that this server is not globally open to the public network. Akeyless Gateway requires only connections to Akeyless SaaS Core Services.

## Deployment

To deploy a standalone instance of Akeyless Gateway, run the following command:

```shell
docker run -d -p 8000:8000 -p 5696:5696 --name akeyless-gateway akeyless/gateway:latest
```

After executing the above command, a new container named `akeyless-gateway` should run on Docker (use `docker ps` for confirmation). It contains a single instance of Akeyless Gateway.

To upgrade your current Gateway version, simply restart the container using the `docker restart <container name>` command.

> ℹ️ **Note:** In this example, the Gateway was deployed without a default Authentication Method as part of the deployment. Thus, **the first Authentication Method** used to log in becomes the admin user on this Gateway.

For further deployment options, visit the [Gateway Docker Advanced Configuration](https://docs.akeyless.io/docs/gateway-docker-advanced-configuration) page.

### Initial Configuration

To configure your Akeyless Gateway:

1. On your browser, navigate to `http://Your-Akeyless-Gateway-URL:8000/console` and log in.

2. Navigate to **Gateways > Select Your Gateway > Manage Gateway**

## Legacy Deployment

If you are using an older Gateway deployment, see [Gateway Legacy](https://docs.akeyless.io/docs/gateway-legacy).
