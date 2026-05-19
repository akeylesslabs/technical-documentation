---
title: Docker Compose Deployment
excerpt: Installation
deprecated: false
hidden: false
metadata:
  title: ''
  description: ''
  robots: index
next:
  description: ''
---
Akeyless Gateway can be deployed using [Docker Compose](https://docs.docker.com/compose/), in which, the configuration process takes place before the actual installation.

## Prerequisites

* An [Authentication Method](https://docs.akeyless.io/docs/access-and-authentication-methods). Make sure it has the right [access permission](https://docs.akeyless.io/docs/rbac) to create and manage [Secrets, Keys](https://docs.akeyless.io/docs/manage-your-secrets-overview) and [Targets](https://docs.akeyless.io/docs/targets).
* A Linux or a Windows machine with [Docker Engine](https://docs.docker.com/get-docker/) installed with a minimum 1 vCPU available with 2 GB RAM.
* [Docker Compose installed](https://docs.docker.com/compose/install/)
* Network connection to [Akeyless SaaS Core Services](https://docs.akeyless.io/docs/gateway-network-connectivity) from your machine.

> ⚠️ **Warning:**
>
> Make sure that this server is not globally opened to the public network. Akeyless Gateway requires only connections to Akeyless SaaS Core Services.

* Network port `8000` on the cluster must be open **only for internal network access**, allowing access to the following services using the corresponding endpoints:

| Service | Endpoint |
| --- | --- |
| [Gateway Configuration Manager](https://docs.akeyless.io/docs/configure-gateway) | `/console` |
| [HashiCorp Vault Proxy](https://docs.akeyless.io/docs/hashicorp-vault-proxy) | `/hvp` |
| Akeyless V1 REST API | `/api/v1` |
| Akeyless V2 REST API | `/api/v2` |
| [KMIP Server](https://docs.akeyless.io/docs/kmip-server) | `:5696` |

## Configuration

Clone the [repository](https://github.com/akeylesslabs/docker-compose) to your environment:

```shell
gh repo clone akeylesslabs/docker-compose
```

Once you have cloned the repository into your environment, you will see the following files:

* `docker-compose.yaml` - defines the Akeyless services and their setup.
* `gateway.env` - stores environment variables for configuring the Gateway.
* `sra.env` - stores environment variables for Secure Remote Access.
* `cache.env` - stores Redis password (required when cache is enabled)

## Authentication

To set your Gateway with a default [Authentication Methods](https://docs.akeyless.io/docs/access-and-authentication-methods) to control the level of access your Gateway instance will have inside your Akeyless account.

The following [Authentication Methods](https://docs.akeyless.io/docs/access-and-authentication-methods) are supported for Docker deployments:

* [API Key](https://docs.akeyless.io/docs/auth-with-api-key)

* [AWS IAM](https://docs.akeyless.io/docs/auth-with-aws)

* [GCP](https://docs.akeyless.io/docs/auth-with-gcp)

* [Azure Active Directory](https://docs.akeyless.io/docs/auth-with-azure)

* [Universal Identity](https://docs.akeyless.io/docs/auth-with-universal-identity)

* [Certificates](https://docs.akeyless.io/docs/auth-with-certificate)

> ℹ️ **Note:**
>
> Your Gateway **Authentication Method** should have permission to create and manage both Items along with Targets items **only**.

### API Key Authentication

To set your Gateway default authentication based on [API Key](https://docs.akeyless.io/docs/auth-with-api-key), edit the `gateway.env` file with the relevant `Access ID` and `Access Key` using the environment variables:

```shell gateway.env
GATEWAY_ACCESS_ID=<AccessID>
GATEWAY_ACCESS_KEY=<AccessKey>
GATEWAY_ACCESS_TYPE=access_key
```

### CSP IAM Authentication

While running your Gateway instance inside your cloud environment, you can use [AWS IAM](https://docs.akeyless.io/docs/auth-with-aws), [GCP GCE](https://docs.akeyless.io/docs/auth-with-gcp), or [Azure Active Directory](https://docs.akeyless.io/docs/auth-with-azure) for authentication. Using machine-to-machine authentication between Akeyless and your Cloud Service Provider, they can supply a list of users allowed to to manage your Akeyless Gateway configuration by adding the `ALLOWED_ACCESS_PERMISSIONS` variable to the `.env` configuration file.

Set the `GATEWAY_ACCESS_ID` variable with your IAM [Authentication Methods](https://docs.akeyless.io/docs/access-and-authentication-methods) `Access ID`, where you need to set a list of users who can [manage your Gateway](https://docs.akeyless.io/docs/gateway-docker-advanced-configuration#gateway-admins) configuration using the `ALLOWED_ACCESS_PERMISSIONS` variable with any other [Authentication Method](https://docs.akeyless.io/docs/access-and-authentication-methods), like [SAML](https://docs.akeyless.io/docs/auth-with-saml), [OIDC](https://docs.akeyless.io/docs/auth-with-oidc), or an [API Key](https://docs.akeyless.io/docs/auth-with-api-key).

```shell AWS IAM
GATEWAY_ACCESS_ID=<AccessID>
GATEWAY_ACCESS_TYPE=aws_iam 
ALLOWED_ACCESS_PERMISSIONS='[{"access_id":"<AccessID>","name":"<Allowed Method Name>", "permissions": ["admin"]}]'
```
```shell GCP_GCE
GATEWAY_ACCESS_ID=<Access ID>
GATEWAY_ACCESS_TYPE=gcp_gce
ALLOWED_ACCESS_PERMISSIONS='[{"access_id":"<Access ID>","name":"<Allowed Method Name>", "permissions": ["admin"]}]'
```
```shell Azure AD
GATEWAY_ACCESS_ID=<Access ID>
GATEWAY_ACCESS_TYPE=azure_ad 
ALLOWED_ACCESS_PERMISSIONS='[{"access_id":"<Access ID>","name":"<Allowed Method Name>", "permissions": ["admin"]}]'
```

### Universal Identity Authentication

To set your Gateway default authentication based on [Universal Identity](https://docs.akeyless.io/docs/auth-with-universal-identity), provide a UID token using `ADMIN_UID_TOKEN` and optionally set `UID_ROTATE_INTERVAL` for automatic token rotation.

Set a list of users who can [manage your Gateway](https://docs.akeyless.io/docs/gateway-docker-advanced-configuration#gateway-admins) by using `ALLOWED_ACCESS_PERMISSIONS` with another [Authentication Method](https://docs.akeyless.io/docs/access-and-authentication-methods), such as [SAML](https://docs.akeyless.io/docs/auth-with-saml), [OIDC](https://docs.akeyless.io/docs/auth-with-oidc), or an [API Key](https://docs.akeyless.io/docs/auth-with-api-key).

```shell gateway.env
ADMIN_UID_TOKEN=<UID Token>
UID_ROTATE_INTERVAL=5m
ALLOWED_ACCESS_PERMISSIONS='[{"access_id":"<Access ID>","name":"<Allowed Method Name>", "permissions": ["admin"]}]'
```

### Certificates Authentication

To set your Gateway default authentication based on [Certificates](https://docs.akeyless.io/docs/auth-with-certificate), provide the relevant `Access ID`, `Certificate`, and `Certificate Key`, and set a list of users who can [manage your Gateway](https://docs.akeyless.io/docs/gateway-docker-advanced-configuration#gateway-admins) configuration using the `ALLOWED_ACCESS_PERMISSIONS` variable with any other [Authentication Method](https://docs.akeyless.io/docs/access-and-authentication-methods) like [SAML](https://docs.akeyless.io/docs/auth-with-saml), [OIDC](https://docs.akeyless.io/docs/auth-with-oidc), or an [API Key](https://docs.akeyless.io/docs/auth-with-api-key).

```shell gateway.env
GATEWAY_ACCESS_ID=<AccessID>
GATEWAY_ACCESS_TYPE=cert
GATEWAY_CERTIFICATE=<certificate.pem base 64>
GATEWAY_CERTIFICATE_KEY=<private key base 64>
ALLOWED_ACCESS_PERMISSIONS='[{"access_id":"<AccessID>","name":"<Allowed Method Name>", "permissions": ["admin"]}]'
```

## Gateway Admins

To support local management of your Gateway configuration, you can set a list of `Access ID` values that can log in and manage your Gateway. This setting can also work with [Sub-Claims](https://docs.akeyless.io/docs/sub-claims) (when a shared authentication method is used), where for each entry you need to define a unique `name` which should describe the **Access Permission** object, with an `access-id`, `sub_claims` when applicable, and a list of `permissions`.

Add the `ALLOWED_ACCESS_PERMISSIONS` environment variable to the `gateway.env` file, specifying a **JSON** list of allowed `Access IDs`:

```yaml gateway.env
ALLOWED_ACCESS_PERMISSIONS='[ {"name": "Administrators", "access_id": "p-yyyyyy", "sub_claims": {"email": ["test01@testhost.com", "test02@testhost.com"], "group": ["Devops"]}, "permissions": ["admin"]}]'
```

Add the environment variable to the `docker-compose.yaml` file:

```shell docker-compose.yml
ALLOWED_ACCESS_PERMISSIONS: $ALLOWED_ACCESS_PERMISSIONS
```

In this case, the above will create an **Access Permission** object named **Administrators**, associated with an Auth Method `p-yyyyyy` which for example is your [SAML](https://docs.akeyless.io/docs/auth-with-saml) or [OIDC](https://docs.akeyless.io/docs/auth-with-oidc) `Access ID`, where a user that at least matches one [Sub-Claims](https://docs.akeyless.io/docs/sub-claims) attribute, will be authorized to access the Gateway with **Admin** permissions:

In our example, `test01@testhost.com` and `test02@testhost` will be authorized, and any member of `group=Devops` will also be authorized.

In this case, the `Access ID` belongs to the authentication method created for the certain Identity Provider.
_If you don't specify the sub-claims, every user authenticated by this IdP can log in to the Gateway with admin privileges._

To work with [API Key](https://docs.akeyless.io/docs/auth-with-api-key) as an `ALLOWED_ACCESS_PERMISSIONS` simply provide your [API Key](https://docs.akeyless.io/docs/auth-with-api-key) `Access ID` with a `name` for the **Access Permission** object, with a set of `permissions`.

### Access Permissions

To delegate the exact permissions users will have on your Gateway components you can explicitly grant permissions, for example, to grant permissions to a user to manage only your Gateway [Log Forwarding](https://docs.akeyless.io/docs/gateway-log-forwarding) settings:

```shell gateway.env
[{"name": "Administrators", "access_id": "p-yyyyyy", "sub_claims": {"email": ["email=test01@testhost.com", "email=test02@testhost.com"], "group": ["Devops"]}, "permissions": ["admin"]}, {"name": "LogForwarding", "access_id": "p-xxxxxx", "sub_claims": {"email": ["email=test03@testhost.com"]}, "permissions": ["log_forwarding"]}]
```

In the above example, your Gateway **Admins** are `test01@testhost.com,test01@testhost.com` or any user which is part of your `Devops` group in your **IdP**, where `test03@testhost.com` have permission to manage **only** your Gateway [Log Forwarding](https://docs.akeyless.io/docs/gateway-log-forwarding) settings.

Full list of available permissions:

| Permission | Description |
| --- | --- |
| `admin` | Admin permission can manage all Gateway components, including **Access Permissions** |
| `defaults` | Management of the defaults settings of your Gateway, including `GatewayUrl`, `TLS`, `Default Encryption Key` and `Default AccessID` for login. |
| `dynamic_secret` | Management of [Dynamic Secrets](https://docs.akeyless.io/docs/how-to-create-dynamic-secret) |
| `rotated_secret` | Management of [Rotated Secrets](https://docs.akeyless.io/docs/rotated-secrets) |
| `rotate_secret_value` | Grants permission **only** to rotate the secret value, without allowing manual edits. Requires `read` permission on the item |
| `targets` | Management of all Targets items that were created using your Gateway |
| `classic_keys` | Management of [Classic Keys](https://docs.akeyless.io/docs/classic-keys) |
| `log_forwarding` | Management of [Log Forwarding](https://docs.akeyless.io/docs/gateway-log-forwarding) settings |
| `zero_knowledge_encryption` | Management of [Zero-Knowledge](https://docs.akeyless.io/docs/zero-knowledge) |
| `caching` | Management of [Gateway Caching](https://docs.akeyless.io/docs/gateway-caching) settings |
| `event_forwarding` | Management of [Event](https://docs.akeyless.io/docs/event-center) Forwarding settings |
| `ldap_auth` | Management of [LDAP](https://docs.akeyless.io/docs/auth-with-ldap) Auth Gateway configuration. |
| `k8s_auth` | Management of [Kubernetes](https://docs.akeyless.io/docs/auth-with-kubernetes) Auth Gateway configuration |
| `kmip` | Management of [KMIP Servers](https://docs.akeyless.io/docs/kmip-server) |

> ℹ️ **Note:**
>
> Only Gateway **Admins** can delegate permissions to additional users. Any pre-provisioned settings will not be editable from the Akeyless Console.

You may also edit this parameter on your console, by going to the Gateways tab and selecting the desired Gateway. On the right of the screen, you will see the Gateway details, including **Access Permissions**.

## Profiles

Profiles let you choose which services to start when running the configuration. The available profiles are:

* **Gateway** - runs the Gateway service.
* **SRA** - runs the Secure Remote Access services (both SSH and Web).
* **Metrics** - runs monitoring services (**Prometheus** and **Grafana**).

Example:

```shell
sudo docker compose --profile gateway up -d
```

The above command will deploy a Gateway.

## Installation

From the directory where the `docker-compose.yaml` and the `.env` file are located, run:

```shell
docker compose --profile <profile> up -d
```

Check if the containers are up and running `docker ps`.
