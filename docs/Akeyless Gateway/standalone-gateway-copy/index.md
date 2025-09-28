---
title: Docker Compose
excerpt: Installation
deprecated: false
hidden: true
metadata:
  title: ''
  description: ''
  robots: index
next:
  description: ''
---
Akeyless Gateway can be deployed using [Docker Compose](https://docs.docker.com/compose/), in which, the configuration process takes place before the actual installation.

# Prerequisites

* An [Authentication Method](doc:access-and-authentication-methods). Make sure it has the right [access permission](doc:rbac) to create and manage [Secrets, Keys](doc:manage-your-secrets-overview) & [Targets](doc:targets).
* A Linux or a Windows machine with [Docker engine](https://docs.docker.com/get-docker/) installed with a minimum 1 vCPU available with 2GB RAM.
* [Docker compose installed](https://docs.docker.com/compose/install/)
* Network connection to [Akeyless SaaS Core Services](doc:api-gateway-network-connectivity) from your machine.

> 🚧 Warning
>
> Make sure that this server is not globally opened to the public network. Akeyless Gateway requires only connections to Akeyless SaaS Core Services.

* Network port `8000` on the cluster must be open **only for internal network access**, allowing access to the following services using the corresponding endpoints:

| Service                                                            | Endpoint   |
| :----------------------------------------------------------------- | :--------- |
| [Gateway Configuration Manager](doc:gateway-configuration-manager) | `/console` |
| [HashiCorp Vault Proxy](doc:hashicorp-vault-proxy)                 | `/hvp`     |
| Akeyless V1 REST API                                               | `/api/v1`  |
| Akeyless V2 REST API                                               | `/api/v2`  |
| [KMIP Server](doc:kmip-server)                                     | `:5696`    |

# Configuration

Clone the repository to your environment:

```shell
gh repo clone akeylesslabs/docker-compose
```

Once you have cloned the repository into your environment, you will see the following files:

* `docker-compose.yaml` - defines the Akeyless services and their setup.
* `gateway.env` - stores environment variables for configuring the Gateway.
* `sra.env` - stores environment variables for Secure Remote Access.

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

# Authentication

To set your Gateway with a default [Authentication Methods](doc:access-and-authentication-methods) to control the level of access your Gateway instance will have inside your Akeyless account.

The following [Authentication Methods](doc:access-and-authentication-methods) are supported for Docker deployments:

* [API Key](doc:api-key)

* [AWS IAM](doc:aws-iam)

* [GCP](doc:gcp-auth-method)

* [Azure Active Directory](doc:azure-ad)

* [Certificates](doc:certificate-based-authentication)

> 👍 Note
>
> Your Gateway **Authentication Method**  should have permission to create and manage both Items along with Targets items **only**.

## API Key Authentication

To set your Gateway default authentication based on [API Key](doc:api-key), edit the `gateway.env` file with the relevant `Access ID` and `Access Key` using the environment variables:

```shell gateway.env
GATEWAY_ACCESS_ID=<AccessID>
GATEWAY_ACCESS_KEY=<AccessKey>
GATEWAY_ACCESS_TYPE=access_key
```

## CSP IAM Authentication

While running your Gateway instance inside your cloud environment, you can use [AWS IAM](doc:aws-iam), [GCP GCE](doc:gcp-auth-method), or [Azure Active Directory](doc:azure-ad), using machine-to-machine authentication between Akeyless and your Cloud Service Provider with a list of [allowed users](https://docs.akeyless.io/docs/standalone-gateway-copy#gateway-admins) that will be able to manage your Gateway configuration by adding the `GATEWAY_AUTHORIZED_ACCESS_ID` variable to the `.env` configuration file.

Set the `GATEWAY_ACCESS_ID` variable with your IAM [Authentication Methods ](doc:access-and-authentication-methods) `Access ID`, where you need to set a list of users that will be able to [manage your Gateway](https://docs.akeyless.io/docs/standalone-gateway-copy#gateway-admins) configuration using `GATEWAY_AUTHORIZED_ACCESS_ID` variable with any other [Authentication Method](doc:access-and-authentication-methods) like [SAML](doc:saml) or [OIDC](doc:opened) or an [API Key](doc:api-key).

```shell AWS_IAM
GATEWAY_ACCESS_ID=<AccessID>
GATEWAY_ACCESS_TYPE=aws_iam 
ALLOWED_ACCESS_PERMISSIONS='[{"access_id":"<AccessID>","name":"<Allowed Method Name>", "permissions": ["admin"]}]'
```
```shell GCP_GCE
GATEWAY_ACCESS_ID=<Access ID>
GATEWAY_ACCESS_TYPE=gcp_gce
ALLOWED_ACCESS_PERMISSIONS='[{"access_id":"<Access ID>","name":"<Allowed Method Name>", "permissions": ["admin"]}]'
```
```shell Azure_AD
GATEWAY_ACCESS_ID=<Access ID>
GATEWAY_ACCESS_TYPE=azure_ad 
ALLOWED_ACCESS_PERMISSIONS='[{"access_id":"<Access ID>","name":"<Allowed Method Name>", "permissions": ["admin"]}]'
```

## Certificates Authentication

To set your Gateway default authentication based on [Certificates](doc:certificate-based-authentication)  provide the relevant `Access ID`, `Certificate`, and `Certificate Key`, where you need to set a list of users that will be able to [manage your Gateway](https://docs.akeyless.io/docs/standalone-gateway-copy#gateway-admins) configuration using `GATEWAY_AUTHORIZED_ACCESS_ID`variable with any other [Authentication Method](doc:access-and-authentication-methods) like [SAML](doc:saml) or [OIDC](doc:opened) or an [API Key](doc:api-key).

```shell gateway.env
GATEWAY_ACCESS_ID=<AccessID>
GATEWAY_ACCESS_TYPE=cert
GATEWAY_CERTIFICATE=<certificate.pem base 64>
GATEWAY_CERTIFICATE_KEY=<private key base 64>
ALLOWED_ACCESS_PERMISSIONS='[{"access_id":"<AccessID>","name":"<Allowed Method Name>", "permissions": ["admin"]}]'
```

# Gateway Admins

To support local management of your Gateway configuration, you can set a list of  `Access ID` that will be able to log in and manage your Gateway. This setting can also work with [Sub-Claims](doc:sub-claims) (when a shared authentication method is used), where for each entry you need to define a unique `name` which should describe the **Access Permission** object, with an `access-id`, `sub_claims` when applicable, and a list of `permissions`.

Add the `GATEWAY_AUTHORIZED_ACCESS_ID` environment variable to the `gateway.env` file, specifying a **JSON** list of allowed `Access IDs`:

```yaml gateway.env
ALLOWED_ACCESS_PERMISSIONS='[ {"name": "Administrators", "access_id": "p-yyyyyy", "sub_claims": {"email": ["test01@testhost.com", "test02@testhost.com"], "group": ["Devops"]}, "permissions": ["admin"]}]'
```

Add the environment variable to the `docker-compose.yaml` file:

```shell docker-compose.yaml
ALLOWED_ACCESS_PERMISSIONS: $ALLOWED_ACCESS_PERMISSIONS
```

In this case, the above will create an **Access Permission** object named **Administrators**,  associated with an Auth method `p-yyyyyy` which for example is your [SAML](doc:saml) or [OIDC](doc:openid) `Access ID`, where a user that at least matches one [Sub-Claims](doc:sub-claims) attribute, will be authorized to access the Gateway with **Admin** permissions:

In our example, `test01@testhost.com` and `test02@testhost` will be authorized, and any member of `group=Devops` will also be authorized.

In this case, the `Access ID` belongs to the authentication method created for the certain Identity Provider.
**If you don't specify the sub-claims, every user authenticated by this IdP will be able to log in to the Gateway with admin privileges.**

To work with [API Key](doc:api-key) as an `GATEWAY_AUTHORIZED_ACCESS_ID` simply provide your [API Key](doc:api-key) `Access ID` with a `name` for the **Access Permission** object, with a set of `permissions`.

## Access Permissions

To delegate the exact permissions users will have on your Gateway components you can explicitly grant permissions, for example, to grant permissions to a user to manage only your Gateway [Log Forwarding](doc:log-forwarding) settings:

```shell gateway.env
[{"name": "Administrators", "access_id": "p-yyyyyy", "sub_claims": {"email": ["email=test01@testhost.com", "email=test02@testhost.com"], "group": ["Devops"]}, "permissions": ["admin"]}, {"name": "LogForwarding", "access_id": "p-xxxxxx", "sub_claims": {"email": ["email=test03@testhost.com"]}, "permissions": ["log_forwarding"]}]
```

In the above example, your Gateway **Admins** are `test01@testhost.com,test01@testhost.com` or any user which is part of your `Devops` group in your **IdP**, where `test03@testhost.com` have permission to manage **only** your Gateway [Log Forwarding](doc:log-forwarding) settings.

Full list of available permissions:

<Table align={["left","left"]}>
  <thead>
    <tr>
      <th>
        Permission
      </th>

      <th>
        Description
      </th>
    </tr>
  </thead>

  <tbody>
    <tr>
      <td>
        `admin`
      </td>

      <td>
        Admin permission can manage all Gateway components, including **Access Permissions**
      </td>
    </tr>

    <tr>
      <td>
        `defaults`
      </td>

      <td>
        Management of the defaults settings of your Gateway
        Including  `GatewayUrl`,`TLS`, `Defualt Encryption Key` & `Defualt AccessID` for login.
      </td>
    </tr>

    <tr>
      <td>
        `dynamic_secret`
      </td>

      <td>
        Management of [Dynamic Secrets](doc:how-to-create-dynamic-secret)
      </td>
    </tr>

    <tr>
      <td>
        `rotated_secret`
      </td>

      <td>
        Management of [Rotated Secrets](doc:rotated-secrets)
      </td>
    </tr>

    <tr>
      <td>
        `rotate_secret_value`
      </td>

      <td>
        Grants permission **only** to rotate the secret value, without allowing manual edits. Requires `read` permission on the item
      </td>
    </tr>

    <tr>
      <td>
        `targets`
      </td>

      <td>
        Management of all Targets items that were created using your Gateway
      </td>
    </tr>

    <tr>
      <td>
        `classic_keys`
      </td>

      <td>
        Management of [Classic Keys](doc:classic-keys)
      </td>
    </tr>

    <tr>
      <td>
        `log_forwarding`
      </td>

      <td>
        Management of [Log Forwarding](doc:log-forwarding) settings
      </td>
    </tr>

    <tr>
      <td>
        `zero_knowledge_encryption`
      </td>

      <td>
        Management of [Zero-Knowledge](doc:zero-knowledge)
      </td>
    </tr>

    <tr>
      <td>
        `caching`
      </td>

      <td>
        Management of [Gateway Cache](doc:configure-the-gateway-cache) settings
      </td>
    </tr>

    <tr>
      <td>
        `event_forwarding`
      </td>

      <td>
        Management of [Event](doc:event-center) Forwarding settings
      </td>
    </tr>

    <tr>
      <td>
        `ldap_auth`
      </td>

      <td>
        Management of [LDAP](doc:ldap) Auth Gateway configuration.
      </td>
    </tr>

    <tr>
      <td>
        `k8s_auth`
      </td>

      <td>
        Management of [Kubernetes](doc:kubernetes-auth) Auth Gateway configuration
      </td>
    </tr>

    <tr>
      <td>
        `kmip`
      </td>

      <td>
        Management of [KMIP Servers](doc:kmip-server)
      </td>
    </tr>
  </tbody>
</Table>

> 👍 Note
>
> Only Gateway **Admins** can delegate permissions to additional users. Any pre-provisioned settings will not be editable from the Akeyless Console.

You may also edit this parameter on your console, by going to the Gateways tab and selecting the desired Gateway. On the right of the screen, you will see the Gateway details, including **Access Permissions**.

# Installation

From the directory where the `docker-compose.yaml` and the `.env` file are located, run:

```shell
docker compose up -d
```

Check if the containers are up and running:

```shell
docker ps

CONTAINER ID   IMAGE                                                             COMMAND                  CREATED          STATUS                    PORTS                                                                                        NAMES
c913bebbeed5   docker.registry-2.akeyless.io/base:latest                                            "/bin/bash /akeyless…"   20 minutes ago   Up 20 minutes (healthy)   0.0.0.0:8000->8000/tcp, :::8000->8000/tcp, 0.0.0.0:8080->8080/tcp, :::8080->8080/tcp         akeyless-gateway
```
