---
title: Gateway Docker Advanced Configuration
excerpt: Advanced environment-variable configuration for standalone Docker deployments.
deprecated: false
hidden: false
metadata:
  title: ''
  description: ''
  robots: index
next:
  description: ''
---
The structure of the Gateway deployment command when using environment variables should be as follows:

```shell
docker run -d -p 8000:8000  -p 5696:5696 -e ENV_VARIABLE_1="value1" -e ENV_VARIABLE_2="value2" -v /HOST/PATH/TO/FILE:/GATEWAY/PATH/TO/FILE --name akeyless-gw akeyless/gateway:latest
```

> ℹ️ **Note:**
>
> To update an existing Gateway, use the same **Gateway Access ID** and **Cluster Name** for the new Gateway to retrieve the latest settings and data from the previously removed Docker instance.

Use this page to organize settings by deployment goal:

| Goal | Section |
| --- | --- |
| Configure login and admin access | [Authentication and Access Control](#authentication-and-access-control) |
| Define cluster identity and encryption behavior | [Cluster Identity and Encryption](#cluster-identity-and-encryption) |
| Configure TLS, caching, and runtime options | [Runtime and Security Settings](#runtime-and-security-settings) |
| Restrict access scope and define defaults | [Access Scope and Defaults](#access-scope-and-defaults) |
| Configure platform and networking extras | [Operational Options](#operational-options) |

## Authentication and Access Control

### Authentication

Set your Gateway with a default [Authentication Method](https://docs.akeyless.io/docs/access-and-authentication-methods) to control the level of access your Gateway instance will have in your Akeyless account.

The following [Authentication Methods](https://docs.akeyless.io/docs/access-and-authentication-methods) are supported for Docker deployments:

* Email/password

* [API Key](https://docs.akeyless.io/docs/auth-with-api-key)

* [AWS IAM](https://docs.akeyless.io/docs/auth-with-aws)

* [GCP](https://docs.akeyless.io/docs/auth-with-gcp)

* [Azure Active Directory](https://docs.akeyless.io/docs/auth-with-azure)

* [Certificates](https://docs.akeyless.io/docs/auth-with-certificate)

> ℹ️ **Note:**
>
> Your Gateway **Authentication Method** should have permission to create and manage both Items and Target items **only**.

While working with Cloud Service Providers [Authentication Methods](https://docs.akeyless.io/docs/access-and-authentication-methods), you can provide a list of allowed users who can log in and manage your Gateway configuration.

### Email Authentication

To set your Gateway default authentication based on your email/password used to create your Akeyless account:

```shell
docker run -d -p 8000:8000 -p 5696:5696 -e ADMIN_ACCESS_ID="email" -e ADMIN_PASSWORD="password" --name akeyless-gw akeyless/gateway:latest
```

> ⚠️ **Warning:**
>
> Using your default account credentials is not recommended for production environments and cannot work with MFA.

### API Key Authentication

To set your Gateway default authentication based on [API Key](https://docs.akeyless.io/docs/auth-with-api-key), provide the relevant `Access ID` and `Access Key` using these variables:

`GATEWAY_ACCESS_ID="your-access-id"`, `GATEWAY_ACCESS_KEY="matching-access-key"`.

```shell
docker run -d -p 8000:8000 -p 5696:5696 -e GATEWAY_ACCESS_ID="p-xxxxxx" -e GATEWAY_ACCESS_KEY="62Hu...xxx....qlg=" --name akeyless-gw akeyless/gateway:latest
```

### CSP IAM Authentication

While running your Gateway instance inside your cloud environment, you can use [AWS IAM](https://docs.akeyless.io/docs/auth-with-aws), [GCP](https://docs.akeyless.io/docs/auth-with-gcp), or [Azure Active Directory](https://docs.akeyless.io/docs/auth-with-azure), using machine-to-machine authentication between Akeyless and your Cloud Service Provider with a list of allowed users who can manage your Gateway configuration.

Set the `GATEWAY_ACCESS_ID` variable with your IAM [Authentication Methods](https://docs.akeyless.io/docs/access-and-authentication-methods) `Access ID`, where you need to set a list of users who can manage your Gateway configuration using the `ALLOWED_ACCESS_PERMISSIONS` variable with any other [Authentication Method](https://docs.akeyless.io/docs/access-and-authentication-methods).

```shell
docker run -d -p 8000:8000 -p 5696:5696 -e GATEWAY_ACCESS_ID="p-xxxxxxx" -e ALLOWED_ACCESS_PERMISSIONS='[ {"name": "Administrators", "access_id": "p-yyyyyy", "permissions": ["admin"]}]' --name akeyless-gw akeyless/gateway:latest
```

### Universal Identity

To set your Gateway default authentication based on Universal Identity, provide the relevant **UID token** using the `ADMIN_UID_TOKEN` variable: `ADMIN_UID_TOKEN=uid-token`

With a list of users who can manage your Gateway configuration using the `ALLOWED_ACCESS_PERMISSIONS` variable with any other [Authentication Method](https://docs.akeyless.io/docs/access-and-authentication-methods), like [SAML](https://docs.akeyless.io/docs/auth-with-saml), OIDC, or an API Key.

```shell
docker run -d -p 8000:8000  -p 5696:5696 -e ADMIN_UID_TOKEN=<UID Token> -e UID_ROTATE_INTERVAL=5m -e ALLOWED_ACCESS_PERMISSIONS='[{"name": "Administrators", "access_id": "<Access ID>", "permissions": ["admin"]}]' --name akeyless-gateway akeyless/gateway:latest
```

### Certificates Authentication

To set your Gateway default authentication based on [Certificates](https://docs.akeyless.io/docs/auth-with-certificate), provide the relevant `Access ID`, `Certificate`, and `Certificate Key` using these variables:

`GATEWAY_ACCESS_ID="your-access-id"`, `GATEWAY_CERTIFICATE="Certificate base64-encoded"` and `GATEWAY_CERTIFICATE_KEY="Certificate Key base64"`.

With a list of users who can manage your Gateway configuration using the `ALLOWED_ACCESS_PERMISSIONS` variable, with any other [Authentication Method](https://docs.akeyless.io/docs/access-and-authentication-methods) like [SAML](https://docs.akeyless.io/docs/auth-with-saml), [OIDC](https://docs.akeyless.io/docs/auth-with-oidc), or an [API Key](https://docs.akeyless.io/docs/auth-with-api-key).

```shell
docker run -d -p 8000:8000  -p 5696:5696 -e GATEWAY_ACCESS_ID="p-xxxxxxx" -e GATEWAY_CERTIFICATE="base64-cert" -e GATEWAY_CERTIFICATE_KEY="base64-cert-key" -e ALLOWED_ACCESS_PERMISSIONS='[ {"name": "Administrators", "access_id": "p-yyyyyy", "permissions": ["admin"]}]' --name akeyless-gw akeyless/gateway:latest
```

Alternatively, you can mount the certificate and key directly into the Docker image:

```shell
docker run -d -p 8000:8000  -p 5696:5696 -e GATEWAY_ACCESS_ID="p-xxxxxxx" -v $PWD/key.pem:/home/akeyless/.akeyless/akeyless-admin-cert.key -v $PWD/cert.crt:/home/akeyless/.akeyless/akeyless-admin-cert.crt -e ALLOWED_ACCESS_PERMISSIONS='[ {"name": "Administrators", "access_id": "p-yyyyyy", "permissions": ["admin"]}]' --name akeyless-gw akeyless/gateway:latest
```

### Gateway Admins

To support local management of your Gateway configuration, you can set a list of `Access ID` values that can log in and manage your Gateway. This setting can also work with [Sub-Claims](https://docs.akeyless.io/docs/sub-claims) (when a shared authentication method is used), where for each entry you need to define a unique `name` which should describe the **Access Permission** object, with an `access-id`, `sub_claims` when applicable, and a list of `permissions`.

> ℹ️ **Note:**
>
> Older deployments may use `ALLOWED_ACCESS_IDS`, which accepts a comma-separated list of access IDs but does not support per-entry permissions or sub-claims. `ALLOWED_ACCESS_PERMISSIONS` is the current variable and supersedes `ALLOWED_ACCESS_IDS`.

For example:

```shell
ALLOWED_ACCESS_PERMISSIONS='[ {"name": "Administrators", "access_id": "p-yyyyyy", "sub_claims": {"email": ["test01@testhost.com", "test02@testhost.com"], "group": ["Devops"]}, "permissions": ["admin"]}]'
```
```powershell
ALLOWED_ACCESS_PERMISSIONS='[{"name": "Administrators", "access_id": "Access ID", "permissions": ["admin"]}]'
```

Run the following:

```shell
docker run -d -p 8000:8000 -p 5696:5696 -e GATEWAY_ACCESS_ID="p-xxxxxxx" -e ALLOWED_ACCESS_PERMISSIONS='[ {"name": "Administrators", "access_id": "p-yyyyyy", "sub_claims": {"email": ["test01@testhost.com", "test02@testhost.com"], "group": ["Devops"]}, "permissions": ["admin"]}]' --name akeyless-gw akeyless/gateway:latest
```
```shell
docker run -d -p 8000:8000 -p 8200:8200 -p 5696:5696 -e GATEWAY_ACCESS_ID="your-csp-access-id" -e ALLOWED_ACCESS_PERMISSIONS='[ {"name": "access1", "access_id": "p-xxxxxxx", "sub_claims": {"username": ["username1", "username2"], "group": ["IT"]}, "permissions": ["admin"]},\n {"name": "access2", "access_id": "p-yyyyyy", "sub_claims": {"username": ["username1"], "group": ["rnd"]}, "permissions": ["targets", "defaults"]}, {"name": "access3", "access_id": "p-zzzzzzz", "sub_claims": {"email": ["xxx@example.com", "zzz@example.com"]}, "permissions": ["admin"]}]' --name akeyless-gw akeyless/gateway:latest
```

In this case, the above creates an **Access Permission** object named **Administrators**, associated with an Auth Method `p-yyyyyy`, which is, for example, your [SAML](https://docs.akeyless.io/docs/auth-with-saml) or [OIDC](https://docs.akeyless.io/docs/auth-with-oidc) `Access ID`. A user that matches at least one [Sub-Claims](https://docs.akeyless.io/docs/sub-claims) attribute is authorized to access the Gateway with **Admin** permissions:

In our example, `test01@testhost.com` and `test02@testhost.com` are authorized, and any member of `group=Devops` is also authorized.

In this case, the `Access ID` belongs to the authentication method created for a certain Identity Provider. **If you don't specify the sub-claims, every user authenticated by this IdP can log in to the Gateway with admin privileges.**

To work with [API Key](https://docs.akeyless.io/docs/auth-with-api-key) as an `ALLOWED_ACCESS_PERMISSIONS` simply provide your [API Key](https://docs.akeyless.io/docs/auth-with-api-key) `Access ID` with a `name` for the **Access Permission** object, with a set of permissions.

#### Access Permissions

To delegate the exact permissions users will have on your Gateway components you can explicitly grant permissions, for example, to grant permissions to a user to manage only your Gateway [Log Forwarding](https://docs.akeyless.io/docs/gateway-log-forwarding) settings:

```json
ALLOWED_ACCESS_PERMISSIONS='[ {"name": "Administrators", "access_id": "p-yyyyyy", "sub_claims": {"email": ["test01@testhost.com", "test02@testhost.com"], "group": ["Devops"]}, "permissions": ["admin"]},\\n {"name": "LogForwarding", "access_id": "p-xxxxxx", "sub_claims": {"email": ["test03@testhost.com"]}, "permissions": ["log_forwarding"]}]'
```

In the above example, your Gateway **Admins** are `test01@testhost.com`, `test02@testhost.com`, or any user who is part of your `Devops` group in your **IdP**, where `test03@testhost.com` has permission to manage **only** your Gateway [Log Forwarding](https://docs.akeyless.io/docs/gateway-log-forwarding) settings.

For the complete and current list, see [Gateway Access Permissions Reference](https://docs.akeyless.io/docs/gateway-access-permissions-reference).

> ℹ️ **Note:**
>
> Only Gateway **Admins** can delegate permissions to additional users. Any pre-provisioned settings will not be editable from the Akeyless Console.

You may also edit this parameter on your console, by going to the Gateways tab and selecting the desired Gateway. On the right of the screen, you will see the Gateway details, including **Access Permissions**.

### Restrict Gateway Callers by Access ID

Use `GATEWAY_AUTHORIZED_ACCESS_ID` to restrict which access IDs can call the Gateway API at all. This is a transport-layer allowlist enforced before any permission check: if the variable is set, the Gateway rejects requests from any access ID not on the list (the Gateway's own `GATEWAY_ACCESS_ID` is always implicitly allowed).

#### Warning: Access Control Variable Comparison

Use the table below to avoid mixing variables that serve different control planes:

| Variable | Control plane | Purpose | Format | Legacy predecessor |
| --- | --- | --- | --- | --- |
| `ALLOWED_ACCESS_PERMISSIONS` | Gateway authorization (Gateway access permissions) | Grants component-level permissions (for example, `admin`, `targets`, `log_forwarding`) to identities that can manage Gateway settings | JSON array of objects (`name`, `access_id`, optional `sub_claims`, `permissions`) | `ALLOWED_ACCESS_IDS` |
| `GATEWAY_AUTHORIZED_ACCESS_ID` | Gateway ingress allowlist (transport layer) | Restricts which access IDs can call the Gateway API at all, before permission evaluation | Comma-separated list of access IDs | `RESTRICT_SERVICE_TO_ACCESS_IDS` |

Set the value to a comma-separated list of access IDs:

```shell
docker run -d -p 8000:8000 -p 5696:5696 \
  -e GATEWAY_ACCESS_ID="p-xxxxxxx" \
  -e GATEWAY_ACCESS_KEY="matching-access-key" \
  -e GATEWAY_AUTHORIZED_ACCESS_ID="p-aaaaaa,p-bbbbbb" \
  --name akeyless-gw akeyless/gateway:latest
```

> ℹ️ **Note:**
>
> `GATEWAY_AUTHORIZED_ACCESS_ID` replaces the legacy `RESTRICT_SERVICE_TO_ACCESS_IDS`. Both names are accepted, but `GATEWAY_AUTHORIZED_ACCESS_ID` is preferred for current deployments.

`GATEWAY_AUTHORIZED_ACCESS_ID` and `ALLOWED_ACCESS_PERMISSIONS` serve different purposes and can be used together. `GATEWAY_AUTHORIZED_ACCESS_ID` controls **who can reach the Gateway**, while `ALLOWED_ACCESS_PERMISSIONS` controls **what those callers are permitted to do inside the Gateway**.

## Cluster Identity and Encryption

### Cluster Name & URL

Each Gateway instance is uniquely identified by combining the **Gateway Access ID** Authentication Method and the **Cluster Name**.

It means that changing the Gateway **Access ID** or the **Cluster Name** of your Gateway instance will create an entirely new Gateway instance, and it will not retrieve the settings and data from the previous Gateway instance.

That is why we recommend setting up a meaningful Cluster Name for your Gateway instance from the very beginning. By default, your cluster name is _defaultCluster_.

To do that, you can set the `CLUSTER_NAME="meaningful-cluster-name"` variable. In addition, to set in advance the **Cluster URL**, you can set the `CLUSTER_URL` variable as part of the Gateway deployment command.

```shell
docker run -d -p 8000:8000 -p 5696:5696 -e GATEWAY_ACCESS_ID="your-access-id" -e GATEWAY_ACCESS_KEY="matching-access-key" -e CLUSTER_NAME="meaningful-cluster-name" -e INITIAL_DISPLAY_NAME="display-name" -e CLUSTER_URL="https://<GW_URL>" --name akeyless-gw akeyless/gateway:latest
```

You can also provide a custom display name for the Gateway Instance using the `INITIAL_DISPLAY_NAME` variable, but this is arbitrary. This name can be changed in the Akeyless Console after the Gateway is deployed.

### Encryption Key

While the **Secret Encryption** section discusses the secrets created when using the Gateway, this section discusses the encryption of the configuration file.
To choose an [Encryption Key](https://docs.akeyless.io/docs/encryption-keys) to encrypt your Gateway configuration, you can choose an existing key using the following variable `CONFIG_PROTECTION_KEY_NAME`

```shell
docker run -d -p 8000:8000 -p 5696:5696 -e GATEWAY_ACCESS_ID="p-xxxxxxxxxxxx" -e GATEWAY_ACCESS_KEY="62Hu...xxx....qlg=" -e CONFIG_PROTECTION_KEY_NAME="My-Encryption-Key" --name akeyless-gw akeyless/gateway:latest
```

By default, the Gateway configuration is encrypted with your account's default encryption key.

#### Customer Fragment

If your [Encryption Key](https://docs.akeyless.io/docs/encryption-keys) works with [Zero Knowledge](https://docs.akeyless.io/docs/gateway-zero-knowledge), provide the full path to a local JSON containing your Customer Fragment:

Generate the Customer Fragment before deployment by using the documented CLI flow in [Gateway Zero Knowledge](https://docs.akeyless.io/docs/gateway-zero-knowledge#step-1-generate-a-customer-fragment-cli).

Note: When adding multiple Customer Fragments to the Gateway, make sure they are in the same JSON file.

```shell
docker run -d -p 8000:8000 -p 5696:5696 -v {full-path-to}/customer_fragments.json:/home/akeyless/.akeyless/customer_fragments.json -e CLUSTER_NAME="test-cluster" -e GATEWAY_ACCESS_ID="p-xxxxxxx" -e GATEWAY_ACCESS_KEY="<YourAccessKey" -e CONFIG_PROTECTION_KEY_NAME="My-Encryption-Key" --name akeyless-gw akeyless/gateway:latest
```

Alternatively, you can use the environment variable to pass the customer fragment value using the `CUSTOMER_FRAGMENTS` variable:

```shell
export CUSTOMER_FRAGMENTS=$(cat customer_fragments.json)
docker run -d -p 8000:8000 -p 5696:5696 -e CUSTOMER_FRAGMENTS="$CUSTOMER_FRAGMENTS" -e CLUSTER_NAME="test-cluster" -e GATEWAY_ACCESS_ID="p-xxxxxxx" -e GATEWAY_ACCESS_KEY="<YourAccessKey" -e CONFIG_PROTECTION_KEY_NAME="My-Encryption-Key" --name akeyless-gw akeyless/gateway:latest
```

## Runtime and Security Settings

### Version Selection

To work with a specific Gateway version, use the `VERSION` variable to deploy a specific version of the Akeyless Gateway.

```shell
docker run -d -p 8000:8000 -p 5696:5696 -e GATEWAY_ACCESS_ID="your-access-id" -e GATEWAY_ACCESS_KEY="matching-access-key" -e VERSION="gw-app-version" --name akeyless-gw akeyless/gateway:latest
```

### TLS Configuration

We strongly recommend using Akeyless Gateway over TLS to ensure all traffic is encrypted in transit.
Note that when you enable TLS, you must provide a TLS certificate and a TLS private key in PEM format.

```shell
docker run -d -p 8000:8000 -p 5696:5696 -e GATEWAY_ACCESS_ID="your-access-id" -e GATEWAY_ACCESS_KEY="matching-access-key" -e ENABLE_TLS="true" -e ENABLE_TLS_CONFIGURE="true" -e ENABLE_TLS_CURL="true" -e ENABLE_TLS_HVP="true" -e MIN_TLS_VERSION="TLSv1.3" -v $PWD/cert.crt:/home/akeyless/.akeyless/akeyless-api-cert.crt -v $PWD/key.pem:/home/akeyless/.akeyless/akeyless-api-cert.key --name akeyless-gw akeyless/gateway:latest
```
```shell root-image
docker run -d -p 8000:8000 -p 5696:5696 -e GATEWAY_ACCESS_ID="your-access-id" -e GATEWAY_ACCESS_KEY="matching-access-key" -e ENABLE_TLS="true" -e ENABLE_TLS_CONFIGURE="true" -e ENABLE_TLS_CURL="true" -e ENABLE_TLS_HVP="true" -e MIN_TLS_VERSION="TLSv1.3" -v $PWD/cert.crt:/var/akeyless/conf/api-proxy/akeyless-api-cert.crt -v $PWD/private.key:/var/akeyless/conf/api-proxy/akeyless-api-cert.key --name akeyless-gw akeyless/gateway:latest
```

In the example above,

* The `ENABLE_TLS` variable enables TLS for the Gateway Console.

* The `ENABLE_TLS_CONFIGURE` variable enables TLS for the Gateway Configuration Manager.

* The `ENABLE_TLS_HVP` variable enables TLS for the HashiCorp Vault Proxy service.

* The `ENABLE_TLS_CURL` variable enables TLS for the Akeyless API Services.

* The `MIN_TLS_VERSION` variable sets the minimum supported TLS version (`TLSv1`, `TLSv1.1`, `TLSv1.2`, or `TLSv1.3`).

To exclude specific cipher suites, use the `EXCLUDE_CIPHER_SUITES` variable with a comma-separated list of suites.

With the following parameters, you can mount the TLS certificate and the TLS private key from the present working directory to the Gateway target directory:

> ⚠️ **Warning:**
>
> Use mounted TLS certificate and key files only for initial bootstrap when required. For ongoing Gateway configuration updates, use the [Gateway Configuration Manager](https://docs.akeyless.io/docs/configure-gateway) or the [Akeyless CLI](https://docs.akeyless.io/docs/cli-reference-gateway) to reduce configuration drift and avoid TLS misconfiguration.

* `-v $PWD/cert.crt:/home/akeyless/.akeyless/akeyless-api-cert.crt`

* `-v $PWD/key.pem:/home/akeyless/.akeyless/akeyless-api-cert.key`

It is also possible to [set up TLS](https://docs.akeyless.io/docs/gateway-tls-settings) in the Gateway Configuration Manager after the Gateway is deployed.

### TLS and PQC Verification on Gateway

#### Gateway Configuration Requirements

In the Gateway Console, navigate to **Gateway > General** and configure the following fields:

* **TLS Certificate**
* **TLS Private Key**

After saving these values, the Gateway applies TLS for the selected services.

#### Where to Verify PQC Support

After TLS is configured and the Gateway is available over HTTPS, validate the negotiated key exchange in your browser:

1. Open your Gateway URL (for example, `https://localhost:8000/console`) in Chrome.
2. Open Developer Tools.
3. Navigate to the security/connection details for the current page.
4. Verify the key exchange value includes `X25519MLKEM768`.

#### PQC Verification

`X25519MLKEM768` confirms a hybrid key exchange:

* `X25519` (classical elliptic-curve cryptography)
* ML-KEM 768 (post-quantum cryptography)

This confirms the connection is using **TLS 1.3 with hybrid post-quantum key exchange**.

#### Gateway Restart Requirement

To enable hybrid PQC support on the Gateway endpoint, restart the Gateway with the required environment variable:

```shell
docker run -d \
-p 8000:8000 \
-p 5696:5696 \
-e MIN_TLS_VERSION=TLSv1.3 \
--name akeyless-gateway \
akeyless/gateway:latest
```

Setting `MIN_TLS_VERSION=TLSv1.3` enables hybrid PQC support (X25519 + ML-KEM 768) on the Gateway container.

> ℹ️ **Info:**
>
> Akeyless SaaS connections already use hybrid PQC encryption by default over TLS 1.3. The environment variables in this section are required for the Gateway endpoint configuration.

### Cache Configuration

Use the following environment variables to enable runtime and proactive cache features for Docker deployments.

For the full variable reference and behavior details, see [Runtime Caching](https://docs.akeyless.io/docs/runtime-caching), [Proactive Caching](https://docs.akeyless.io/docs/proactive-caching), and [Cluster Cache (Standalone)](https://docs.akeyless.io/docs/cluster-cache-standalone).

```shell
docker run -d -p 8000:8000 -p 5696:5696 -e GATEWAY_ACCESS_ID="p-xxxxxxxxxxxx" -e GATEWAY_ACCESS_KEY="62Hu...xxx....qlg=" -e CACHE_ENABLE="true" -e PROACTIVE_CACHE_ENABLE="true" -e NEW_PROACTIVE_CACHE_ENABLE="true" -e CACHE_TTL="60" -e PROACTIVE_CACHE_MINIMUM_FETCHING_TIME="5" -e PROACTIVE_CACHE_WORKERS="3" --name akeyless-gw akeyless/gateway:latest
```
```shell
docker run -d -p 8000:8000 -p 8200:8200 -p 5696:5696 -e GATEWAY_ACCESS_ID="your-access-id" -e GATEWAY_ACCESS_KEY="matching-access-key" -e CACHE_ENABLE="true" -e PROACTIVE_CACHE_ENABLE="true" -e NEW_PROACTIVE_CACHE_ENABLE="true" -e CACHE_TTL="number-of-minutes" -e PROACTIVE_CACHE_MINIMUM_FETCHING_TIME="number-of-minutes" -e PROACTIVE_CACHE_WORKERS="number-of-workers" --name akeyless-gw akeyless/gateway:latest
```

It is also possible to configure runtime and proactive caching in the Gateway Console after the Gateway is deployed.

## Access Scope and Defaults

### Restrict Gateway Access

To restrict access to Gateway services, set `GATEWAY_AUTHORIZED_ACCESS_ID` to a comma-separated list of `AccessIDs`. This is the current variable for limiting which callers the Gateway will serve. For the variable comparison, format details, and a current example, see [Restrict Gateway Callers by Access ID](https://docs.akeyless.io/docs/gateway-docker-advanced-configuration#restrict-gateway-callers-by-access-id).

```shell
docker run -d -p 8000:8000 -p 5696:5696 -e GATEWAY_ACCESS_ID="aws-iam-access-id" -e GATEWAY_AUTHORIZED_ACCESS_ID="comma-separated list of access-ids" --name akeyless-gw akeyless/gateway:latest
```

`RESTRICT_SERVICE_TO_ACCESS_IDS` is the legacy predecessor to `GATEWAY_AUTHORIZED_ACCESS_ID`. Existing deployments can continue to use it, but new deployments should use `GATEWAY_AUTHORIZED_ACCESS_ID`.

In the above example, in addition to your Gateway admin lists, you are limiting the audience of users that your Gateway will serve. Other `AccessIDs` will not be able to get service from your Gateway. Alternatively, to block specific `AccessIDs`, you can use the `BLOCKLIST_ACCESS_IDS` variable.

### Default Secret Encryption

While the **Encryption Key** section discusses the encryption of the configuration file, this section discusses the secrets created when using the Gateway.
To set a default existing key that will be used to encrypt any secret created through the gateway, add the parameter `DEFAULT_ENCRYPTION_KEY` in the following way:

```shell
docker run -d -p 8000:8000 -p 5696:5696 -e DEFAULT_ENCRYPTION_KEY="existing encryption key name" --name akeyless-gw akeyless/gateway:latest
```

### Default Secret Location

To set a default location to which any secret created through the Gateway will be saved in your Akeyless account, add the parameter `DEFAULT_SECRET_LOCATION` in the following way:

```shell
docker run -d -p 8000:8000 -p 5696:5696 -e DEFAULT_SECRET_LOCATION="path to relevant folder" --name akeyless-gw akeyless/gateway:latest
```

### Setting a Default Login

When using OIDC or SAML authentication to connect to the Gateway web UI on endpoint `/console`, a user is usually asked to supply an access ID before being transferred to a login screen. This can also be done from the Gateway UI as described in [Gateway SAML and OIDC](https://docs.akeyless.io/docs/gateway-authentication-and-access).
When configuring your Gateway, you may supply a default value for either OIDC, SAML, or both, using the following parameters:

* `-e DEFAULT_SAML_ACCESS_ID=<SAML Access ID>`
* `-e DEFAULT_OIDC_ACCESS_ID=<OIDC Access ID>`
* `-e AKEYLESS_OIDC_GW_AUTH=true` Optional, to authenticate directly against your Gateway. To leverage your Gateway for the callback redirects instead of the Akeyless SaaS (if your IdP isn't publicly available), you can add the `AKEYLESS_OIDC_GW_AUTH` variable while making sure the corresponding OIDC App on your IdP has the "**Redirect URI**" set to the Gateway's configuration endpoint (port 8000) with the following URI suffix `/api/oidc-callback` (for example, `https://Your-Akeyless-GW-URL:8000/api/oidc-callback`).

In the following way:

```shell
docker run -d -p 8000:8000 -p 5696:5696 -e DEFAULT_SAML_ACCESS_ID="p-xxxxx" --name akeyless-gw akeyless/gateway:latest
```

To work with [CBA](https://docs.akeyless.io/docs/auth-with-certificate) flow for users' login, first set your users' DNS records with the cert authentication subdomain `auth-cert.akeyless.io` to point to your Gateway IP address.

Set your deployment with the following parameters:

* `-e DEFAULT_CERTIFICATE_ACCESS_ID=<Cert Auth Method Access ID>`
* `-e ENABLE_SNI_PROXY="true"`

In the following way:

```shell
docker run -d -p 8000:8000 -p 5696:5696 -e GATEWAY_ACCESS_ID="aws-iam-access-id" -e DEFAULT_CERTIFICATE_ACCESS_ID="access-id" -e ENABLE_SNI_PROXY="true" --name akeyless-gw akeyless/gateway:latest
```

## Operational Options

### Fixed Artifact Repository

In some environments where an IP address must be whitelisted, to pull Akeyless official artifacts as part of your Gateway deployment, you can pass the `ARTIFACTS_REPO="artifacts.site2.akeyless.io"` environment variable as part of the `docker run` command:

```shell
docker run -d -p 8000:8000 -p 5696:5696 -e ARTIFACTS_REPO="artifacts.site2.akeyless.io" --name akeyless-gw akeyless/gateway:latest
```

### Rate Limit

To set a local rate limit on your Gateway instance, add the `GW_RATE_LIMIT` environment variable, where the value sets the maximum calls per minute. When a client reaches that threshold, this is logged and any additional requests during that minute are discarded on the Gateway:

```shell
docker run -d -p 8000:8000 -p 5696:5696 -e GW_RATE_LIMIT=4000 --name akeyless-gw akeyless/gateway:latest
```

### RHEL Image

To work with a [fully compatible image](https://catalog.redhat.com/software/container-stacks/detail/66016090ff08e22201487dd3) based on Red Hat Universal Base Image 8, set the repository source at the end of the `docker run` command to `akeyless/base-rhel`, for example:

```shell
docker run -d -p 8000:8000 -p 5696:5696 --name akeyless-gateway akeyless/base-rhel:latest-akeyless
```

### gRPC

To enable **gRPC** on your Gateway set the following environment variable `ENABLE_GRPC=true`, the service will be exposed on port `8085`:

```shell
docker run -d -p 8000:8000 -p 8085:8085 -p 5696:5696 -e ENABLE_GRPC=true --name akeyless-gw akeyless/gateway:latest
```

## Legacy Deployment Reference

If you are using an older Gateway deployment that uses `ADMIN_ACCESS_ID` and the `akeyless/base:latest-akeyless` image, see [Gateway Legacy](https://docs.akeyless.io/docs/gateway-legacy) for guidance. The legacy image and `ADMIN_*` environment variables have been superseded by `akeyless/gateway:latest` and the `GATEWAY_*` variable naming convention used throughout this page.
