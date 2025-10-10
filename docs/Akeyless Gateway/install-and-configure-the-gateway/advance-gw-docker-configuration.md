---
title: Advanced Configuration
excerpt: Standalone Gateway
deprecated: false
hidden: false
metadata:
  title: ''
  description: ''
  robots: index
next:
  description: ''
---
The structure of the Gateway installation command when using environment variables should be the following:

```shell CLI
docker run -d -p 8000:8000  -p 5696:5696 -e ENV_VARIABLE_1="value1" -e ENV_VARIABLE_2="value2" -v /HOST/PATH/TO/FILE:/GATEWAY/PATH/TO/FILE --name akeyless-gw akeyless/base:latest-akeyless
```

> 👍 Note
>
> To update an existing Gateway, use the same **Gateway Access ID**  and **Cluster Name** for the new Gateway in order to retrieve the latest settings and data from the previously removed Docker instance.

# Authentication

To set your Gateway with a default [Authentication Methods](https://docs.akeyless.io/docs/access-and-authentication-methods) to control the level of access your Gateway instance will have inside your Akeyless account.

The following [Authentication Methods](https://docs.akeyless.io/docs/access-and-authentication-methods) are supported for Docker deployments:

* Email\Password

* [API Key](https://docs.akeyless.io/docs/api-key)

* [AWS IAM](https://docs.akeyless.io/docs/aws-iam)

* [GCP](https://docs.akeyless.io/docs/gcp-auth-method)

* [Azure Active Directory](https://docs.akeyless.io/docs/azure-ad)

* [Certificates](https://docs.akeyless.io/docs/certificate-based-authentication)

> 👍 Note
>
> Your Gateway **Authentication Method**  should have permission to create and manage both Items along with Targets items **only**.

While working with Cloud Service Providers [Authentication Methods](https://docs.akeyless.io/docs/access-and-authentication-methods) you can provide a list of allowed users that will be able to log in and manage your Gateway configuration.

## Email Authentication

To set your Gateway default authentication based on your email\password which you used to create your Akeyless account:

```shell CLI
docker run -d -p 8000:8000 -p 5696:5696 -e ADMIN_ACCESS_ID="email" -e ADMIN_PASSWORD="password" --name akeyless-gw akeyless/base:latest-akeyless
```

> 🚧 Warning
>
> Using your default account credentials is not recommended for production environments and can not work with MFA.

## API Key Authentication

To set your Gateway default authentication based on [API Key](https://docs.akeyless.io/docs/api-key) provide the relevant `Access ID` and `Access Key` using those variables:

`GATEWAY_ACCESS_ID="your-access-id"`,  ` GATEWAY_ACCESS_KEY="matching-access-key"`.

```shell CLI
docker run -d -p 8000:8000 -p 5696:5696 -e GATEWAY_ACCESS_ID="p-xxxxxx" -e GATEWAY_ACCESS_KEY="62Hu...xxx....qlg=" --name akeyless-gw akeyless/base:latest-akeyless
```
```shell Legacy
docker run -d -p 8000:8000 -p 5696:5696 -e ADMIN_ACCESS_ID="p-xxxxxx" -e ADMIN_ACCESS_KEY="62Hu...xxx....qlg=" --name akeyless-gw akeyless/base:latest-akeyless
```

## CSP IAM Authentication

While running your Gateway instance inside your cloud environment, you can use [AWS IAM](https://docs.akeyless.io/docs/aws-iam), [GCP](https://docs.akeyless.io/docs/gcp-auth-method), or [Azure Active Directory](https://docs.akeyless.io/docs/azure-ad), using machine-to-machine authentication between Akeyless and your Cloud Service Provider with a list of allowed users that will be able to manage your Gateway configuration.

Set the `GATEWAY_ACCESS_ID` variable with your IAM [Authentication Methods ](https://docs.akeyless.io/docs/access-and-authentication-methods) `Access ID`, where you need to set a list of users that will be able to manage your Gateway configuration using `ALLOWED_ACCESS_PERMISSIONS` variable with any other [Authentication Method](https://docs.akeyless.io/docs/access-and-authentication-methods).

```shell CLI
docker run -d -p 8000:8000 -p 5696:5696 -e GATEWAY_ACCESS_ID="p-xxxxxxx" -e ALLOWED_ACCESS_PERMISSIONS='[ {"name": "Administrators", "access_id": "p-yyyyyy", "permissions": ["admin"]}]' --name akeyless-gw akeyless/base:latest-akeyless
```
```shell Legacy Command
docker run -d -p 8000:8000 -p 5696:5696 -e ADMIN_ACCESS_ID="p-xxxxxxx" -e ALLOWED_ACCESS_PERMISSIONS='[ {"name": "Administrators", "access_id": "p-yyyyyy", "permissions": ["admin"]}]' --name akeyless-gw akeyless/base:latest-akeyless
```

## Universal Identity

To set your Gateway default authentication based on Universal Identity, provide the relevant **UID token** using the `ADMIN_UID_TOKEN`variable:`ADMIN_UID_TOKEN=uid-token`

With a list of users that will be able to manage your Gateway configuration using `ALLOWED_ACCESS_PERMISSIONS` variable with any other [Authentication Method](https://docs.akeyless.io/docs/access-and-authentication-methods) like [SAML](https://docs.akeyless.io/docs/saml) or OIDC or an API Key.

```shell
docker run -d -p 8000:8000  -p 5696:5696 -e ADMIN_UID_TOKEN=<UID Token> -e UID_ROTATE_INTERVAL=5m -e ALLOWED_ACCESS_PERMISSIONS='[{"name": "Administrators", "access_id": "<Access ID>", "permissions": ["admin"]}]' --name akeyless-gateway akeyless/base:latest-akeyless
```

## Certificates Authentication

To set your Gateway default authentication based on [Certificates](https://docs.akeyless.io/docs/certificate-based-authentication)  provide the relevant `Access ID`, `Certificate`, and `Certificate Key` using those variables:

`GATEWAY_ACCESS_ID="your-access-id"`,  `GATEWAY_CERTIFICATE="Certificate base64 encoded"` and `GATEWAY_CERTIFICATE_KEY="Certificate Key base64"`.

With a list of users that will be able to manage your Gateway configuration using `ALLOWED_ACCESS_PERMISSIONS`variable with any other [Authentication Method](https://docs.akeyless.io/docs/access-and-authentication-methods) like [SAML](https://docs.akeyless.io/docs/saml) or [OIDC](https://docs.akeyless.io/docs/openid) or an [API Key](https://docs.akeyless.io/docs/api-key).

```shell CLI
docker run -d -p 8000:8000  -p 5696:5696 -e GATEWAY_ACCESS_ID="p-xxxxxxx" -e GATEWAY_CERTIFICATE="base64-cert" -e GATEWAY_CERTIFICATE_KEY="base64-cert-key" -e ALLOWED_ACCESS_PERMISSIONS='[ {"name": "Administrators", "access_id": "p-yyyyyy", "permissions": ["admin"]}]' --name akeyless-gw akeyless/base:latest-akeyless
```
```shell Legacy Command
docker run -d -p 8000:8000  -p 5696:5696 -e ADMIN_ACCESS_ID="p-xxxxxxx" -e ADMIN_CERTIFICATE="base64-cert" -e ADMIN_CERTIFICATE_KEY="base64-cert-key" -e ALLOWED_ACCESS_PERMISSIONS='[ {"name": "Administrators", "access_id": "p-yyyyyy", "permissions": ["admin"]}]' --name akeyless-gw akeyless/base:latest-akeyless
```

Alternatively, you can mount the certificate and key directly into the docker image:

```shell CLI
docker run -d -p 8000:8000  -p 5696:5696 -e GATEWAY_ACCESS_ID="p-xxxxxxx" -v $PWD/key.pem:/home/akeyless/.akeyless/akeyless-admin-cert.key -v $PWD/cert.crt:/home/akeyless/.akeyless/akeyless-admin-cert.crt -e ALLOWED_ACCESS_PERMISSIONS='[ {"name": "Administrators", "access_id": "p-yyyyyy", "permissions": ["admin"]}]' --name akeyless-gw akeyless/base:latest-akeyless
```
```shell Legacy Command
docker run -d -p 8000:8000  -p 5696:5696 -e ADMIN_ACCESS_ID="p-xxxxxxx" -v $PWD/key.pem:/home/akeyless/.akeyless/akeyless-admin-cert.key -v $PWD/cert.crt:/home/akeyless/.akeyless/akeyless-admin-cert.crt -e ALLOWED_ACCESS_PERMISSIONS='[ {"name": "Administrators", "access_id": "p-yyyyyy", "permissions": ["admin"]}]' --name akeyless-gw akeyless/base:latest-akeyless
```

# Gateway Admins

To support local management of your Gateway configuration, you can set a list of  `Access ID` that will be able to log in and manage your Gateway. This setting can also work with [Sub-Claims](https://docs.akeyless.io/docs/sub-claims) (when a shared authentication method is used), where for each entry you need to define a unique `name` which should describe the **Access Permission** object, with an `access-id`, `sub_claims` when applicable, and a list of `permissions`.

e.g.

```shell CLI
ALLOWED_ACCESS_PERMISSIONS='[ {"name": "Administrators", "access_id": "p-yyyyyy", "sub_claims": {"email": ["test01@testhost.com", "test02@testhost.com"], "group": ["Devops"]}, "permissions": ["admin"]}]'
```
```shell Legacy Command
ALLOWED_ACCESS_PERMISSIONS='[ {"name": "Administrators", "access_id": "p-yyyyyy", "sub_claims": {"email": ["test01@testhost.com", "test02@testhost.com"], "group": ["Devops"]}, "permissions": ["admin"]}]'
```
```powershell Powershell
ALLOWED_ACCESS_PERMISSIONS='[{\"name\": \"Administrators\", \"access_id\": \"Access ID\", \"permissions\": [\"admin\"]}]' --name akeyless-gateway akeyless/base:latest-akeyless
```

Run the following:

```shell Example
docker run -d -p 8000:8000 -p 5696:5696 -e GATEWAY_ACCESS_ID="p-xxxxxxx" -e ALLOWED_ACCESS_PERMISSIONS='[ {"name": "Administrators", "access_id": "p-yyyyyy", "sub_claims": {"email": ["test01@testhost.com", "test02@testhost.com"], "group": ["Devops"]}, "permissions": ["admin"]}]' --name akeyless-gw akeyless/base:latest-akeyless
```
```shell Format
docker run -d -p 8000:8000 -p 8200:8200 -p 5696:5696 -e GATEWAY_ACCESS_ID="your-csp-access-id" -e GATEWAY_AUTHORIZED_ACCESS_ID='[ {"name": "access1", "access_id": "p-xxxxxxx", "sub_claims": {"username": ["username1", "username2"], "group": ["IT"]}, "permissions": ["admin"]},\n  {"name": "access2", "access_id": "p-yyyyyy", "sub_claims": {"username": ["username1"], "group": ["rnd"]}, "permissions": ["targets", "defaults"]},  {"name": "access3", "access_id": "p-zzzzzzz", "sub_claims": {"email": ["xxx@example.com", "zzz@example.com"]}, "permissions": ["admin"]}]'  --name akeyless-gw akeyless/base:latest-akeyless
```

In this case, the above will create an **Access Permission** object named **Administrators**,  associated with an Auth method `p-yyyyyy` which for example is your [SAML](https://docs.akeyless.io/docs/saml) or [OIDC](https://docs.akeyless.io/docs/openid) `Access ID`, where a user that at least matches one [Sub-Claims](https://docs.akeyless.io/docs/sub-claims) attribute, will be authorized to access the Gateway with **Admin** permissions:

In our example, `test01@testhost.com` and `test02@testhost` will be authorized, and any member of `group=Devops` will also be authorized.

In this case, the `Access ID` belongs to the authentication method created for the certain Identity Provider.
**If you don't specify the sub-claims, every user authenticated by this IdP will be able to log in to the Gateway with admin privileges.**

To work with [API Key](https://docs.akeyless.io/docs/api-key) as an `ALLOWED_ACCESS_PERMISSIONS` simply provide your [API Key](https://docs.akeyless.io/docs/api-key) `Access ID` with a `name` for the **Access Permission** object, with a set of permissions.

## Access Permissions

To delegate the exact permissions users will have on your Gateway components you can explicitly grant permissions, for example, to grant permissions to a user to manage only your Gateway [Log Forwarding](https://docs.akeyless.io/docs/log-forwarding) settings:

```shell CLI
ALLOWED_ACCESS_PERMISSIONS='[ {"name": "Administrators", "access_id": "p-yyyyyy", "sub_claims": {"email": ["test01@testhost.com", "test02@testhost.com"], "group": ["Devops"]}, "permissions": ["admin"]},\\n  {"name": "LogForwarding", "access_id": "p-xxxxxx", "sub_claims": {"email": ["test03@testhost.com"]}, "permissions": ["log_forwarding"]}]'
```

In the above example, your Gateway **Admins** are `test01@testhost.com,test01@testhost.com` or any user which is part of your `Devops` group in your **IdP**, where `test03@testhost.com` have permission to manage **only** your Gateway [Log Forwarding](https://docs.akeyless.io/docs/log-forwarding) settings.

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
        `defaults`
      </td>

      <td>
        Management of the defaults settings of your Gateway
        Including `Defualt Encryption Key` & `Defualt AccessID` for login.
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
        Management of [Classic Keys](https://docs.akeyless.io/docs/classic-keys)
      </td>
    </tr>

    <tr>
      <td>
        `automatic_migration`
      </td>

      <td>
        Management of  [Dynamic Secrets](https://docs.akeyless.io/docs/how-to-create-dynamic-secret) settings
      </td>
    </tr>

    <tr>
      <td>
        `dynamic_secret`
      </td>

      <td>
        Management of [Dynamic Secrets](https://docs.akeyless.io/docs/how-to-create-dynamic-secret)
      </td>
    </tr>

    <tr>
      <td>
        `rotated_secret`
      </td>

      <td>
        Management of [Rotated Secrets](https://docs.akeyless.io/docs/rotated-secrets)
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
        `log_forwarding`
      </td>

      <td>
        Management of [Log Forwarding](https://docs.akeyless.io/docs/log-forwarding) settings
      </td>
    </tr>

    <tr>
      <td>
        `zero_knowledge_encryption`
      </td>

      <td>
        Management of [Zero-Knowledge](https://docs.akeyless.io/docs/zero-knowledge)
      </td>
    </tr>

    <tr>
      <td>
        `caching`
      </td>

      <td>
        Management of [Gateway Cache](https://docs.akeyless.io/docs/configure-the-gateway-cache) settings
      </td>
    </tr>

    <tr>
      <td>
        `event_forwarding`
      </td>

      <td>
        Management of [Event](https://docs.akeyless.io/docs/event-center) Forwarding settings
      </td>
    </tr>

    <tr>
      <td>
        `ldap_auth`
      </td>

      <td>
        Management of [LDAP](https://docs.akeyless.io/docs/ldap) Auth Gateway configuration.
      </td>
    </tr>

    <tr>
      <td>
        `k8s_auth`
      </td>

      <td>
        Management of [Kubernetes](https://docs.akeyless.io/docs/kubernetes-auth) Auth Gateway configuration
      </td>
    </tr>

    <tr>
      <td>
        `kmip`
      </td>

      <td>
        Management of [KMIP Servers](https://docs.akeyless.io/docs/kmip-server)
      </td>
    </tr>

    <tr>
      <td>
        `general`
      </td>

      <td>
        Management of Gateway General settings including `GatewayUrl`,`TLS`
      </td>
    </tr>

    <tr>
      <td>
        `admin`
      </td>

      <td>
        Admin permission can manage all Gateway components, including **Access Permissions**
      </td>
    </tr>
  </tbody>
</Table>

> 👍 Note
>
> Only Gateway **Admins** can delegate permissions to additional users. Any pre-provisioned settings will not be editable from the Akeyless Console.

You may also edit this parameter on your console, by going to the Gateways tab and selecting the desired Gateway. On the right of the screen, you will see the Gateway details, including **Access Permissions**.

# Cluster Name & URL

Each Gateway instance is uniquely identified by combining the **Gateway Access ID**  Authentication Method and the **Cluster Name**.

It means that changing the Gateway **Access ID** or the **Cluster Name** of your Gateway instance will create an entirely new Gateway instance, and it will not retrieve the settings and data from the previous Gateway instance.

That’s why we recommend setting up a meaningful Cluster Name for your Gateway instance from the very beginning. By default, your cluster name is _defaultCluster_.

To do that, you can set the <code> CLUSTER_NAME="meaningful-cluster-name"</code> variable. In addition, to set in advance the **Cluster URL**, you can set the `CLUSTER_URL` variable as part of the Gateway Installation command.

```shell CLI
docker run -d -p 8000:8000 -p 5696:5696 -e GATEWAY_ACCESS_ID="your-access-id" -e GATEWAY_ACCESS_KEY="matching-access-key" -e CLUSTER_NAME="meaningful-cluster-name" -e INITIAL_DISPLAY_NAME="display-name" -e CLUSTER_URL="https://<GW_URL>" --name akeyless-gw akeyless/base:latest-akeyless
```
```shell Legacy Command
docker run -d -p 8000:8000 -p 5696:5696 -e ADMIN_ACCESS_ID="your-access-id" -e ADMIN_ACCESS_KEY="matching-access-key" -e CLUSTER_NAME="meaningful-cluster-name" -e INITIAL_DISPLAY_NAME="display-name" -e CLUSTER_URL="https://<GW_URL>" --name akeyless-gw akeyless/base:latest-akeyless
```

You can also provide a custom display name for the Gateway Instance using the <code>INITIAL_DISPLAY_NAME</code> variable, but this is arbitrary. This name can be changed in the Akeyless Console after the Gateway is installed.

# Encryption Key

While the **Secret Encryption** section discusses the secrets created when using the Gateway, this section discusses the encryption of the configuration file.
To choose an [Encryption Key](https://docs.akeyless.io/docs/encryption-keys) to encrypt your Gateway configuration, you can choose an existing key using the following variable <code>CONFIG_PROTECTION_KEY_NAME</code>

```shell CLI
docker run -d -p 8000:8000 -p 5696:5696 -e GATEWAY_ACCESS_ID="p-xxxxxxxxxxxx" -e GATEWAY_ACCESS_KEY="62Hu...xxx....qlg=" -e CONFIG_PROTECTION_KEY_NAME="My-Encryption-Key" --name akeyless-gw akeyless/base:latest-akeyless
```
```shell Legacy Command
docker run -d -p 8000:8000 -p 5696:5696 -e ADMIN_ACCESS_ID="p-xxxxxxxxxxxx" -e ADMIN_ACCESS_KEY="62Hu...xxx....qlg=" -e CONFIG_PROTECTION_KEY_NAME="My-Encryption-Key" --name akeyless-gw akeyless/base:latest-akeyless
```

By default, the Gateway configuration is encrypted with your account's default encryption key.

## Customer Fragment

If your [Encryption Key](https://docs.akeyless.io/docs/encryption-keys) works with [Zero Knowledge](https://docs.akeyless.io/docs/implement-zero-knowledge), provide the full path to a local JSON containing your Customer Fragment:

Note: When adding multiple Customer Fragments to the Gateway, make sure they are in the same JSON file.

```shell CLI
docker run -d -p 8000:8000 -p 5696:5696 -v {full-path-to}/customer_fragments.json:/home/akeyless/.akeyless/customer_fragments.json -e CLUSTER_NAME="test-cluster" -e GATEWAY_ACCESS_ID="p-xxxxxxx" -e GATEWAY_ACCESS_KEY="<YourAccessKey" -e CONFIG_PROTECTION_KEY_NAME="My-Encryption-Key" --name akeyless-gw akeyless/base:latest-akeyless
```
```shell Legacy
docker run -d -p 8000:8000 -p 5696:5696 -v {full-path-to}/customer_fragments.json:/home/akeyless/.akeyless/customer_fragments.json -e CLUSTER_NAME="test-cluster" -e ADMIN_ACCESS_ID="p-xxxxxxx" -e ADMIN_ACCESS_KEY="<YourAccessKey" -e CONFIG_PROTECTION_KEY_NAME="My-Encryption-Key" --name akeyless-gw akeyless/base:latest-akeyless
```

Alternatively, you can use the environment variable to pass the customer fragment value using the `CUSTOMER_FRAGMENTS` variable:

```shell CLI
export CUSTOMER_FRAGMENTS=$(cat customer_fragments.json)
docker run -d -p 8000:8000 -p 5696:5696 -e CUSTOMER_FRAGMENTS="$CUSTOMER_FRAGMENTS"  -e CLUSTER_NAME="test-cluster" -e GATEWAY_ACCESS_ID="p-xxxxxxx" -e GATEWAY_ACCESS_KEY="<YourAccessKey" -e CONFIG_PROTECTION_KEY_NAME="My-Encryption-Key" --name akeyless-gw akeyless/base:latest-akeyless
```
```shell Legacy
export CUSTOMER_FRAGMENTS=$(cat customer_fragments.json)
docker run -d -p 8000:8000 -p 5696:5696 -e CUSTOMER_FRAGMENTS="$CUSTOMER_FRAGMENTS"  -e CLUSTER_NAME="test-cluster" -e ADMIN_ACCESS_ID="p-xxxxxxx" -e ADMIN_ACCESS_KEY="<YourAccessKey" -e CONFIG_PROTECTION_KEY_NAME="My-Encryption-Key" --name akeyless-gw akeyless/base:latest-akeyless
```

# Version Selection

To work with a specific Gateway version use the `VERSION` variable to install a specific version of the Akeyless Gateway.

```shell CLI
docker run -d -p 8000:8000 -p 5696:5696 -e GATEWAY_ACCESS_ID="your-access-id" -e GATEWAY_ACCESS_KEY="matching-access-key" -e VERSION="gw-app-version" --name akeyless-gw akeyless/base:latest-akeyless
```
```shell Legacy
docker run -d -p 8000:8000 -p 5696:5696 -e ADMIN_ACCESS_ID="your-access-id" -e ADMIN_ACCESS_KEY="matching-access-key" -e VERSION="gw-app-version" --name akeyless-gw akeyless/base:latest-akeyless
```

# TLS Configuration

We strongly recommend using Akeyless Gateway with TLS to ensure all traffic is encrypted at transit.
Please note that when you're enabling TLS, you must provide a TLS certificate and a TLS Private Key in PEM format.

```shell
docker run -d -p 8000:8000 -p 5696:5696 -e GATEWAY_ACCESS_ID="your-access-id" -e GATEWAY_ACCESS_KEY="matching-access-key" -e ENABLE_TLS="true" -e ENABLE_TLS_CONFIGURE="true" -e ENABLE_TLS_CURL="true" -e ENABLE_TLS_HVP="true" -e MIN_TLS_VERSION="TLSv1.3" -v $PWD/cert.crt:/home/akeyless/.akeyless/akeyless-api-cert.crt -v $PWD/key.pem:/home/akeyless/.akeyless/akeyless-api-cert.key --name akeyless-gw akeyless/base:latest-akeyless
```
```shell Legacy
docker run -d -p 8000:8000 -p 5696:5696 -e ADMIN_ACCESS_ID="your-access-id" -e ADMIN_ACCESS_KEY="matching-access-key" -e ENABLE_TLS="true" -e ENABLE_TLS_CONFIGURE="true" -e ENABLE_TLS_CURL="true" -e ENABLE_TLS_HVP="true" -e MIN_TLS_VERSION="TLSv1.3" -v $PWD/cert.crt:/home/akeyless/.akeyless/akeyless-api-cert.crt -v $PWD/key.pem:/home/akeyless/.akeyless/akeyless-api-cert.key --name akeyless-gw akeyless/base:latest-akeyless
```
```shell root-image
docker run -d -p 8000:8000 -p 5696:5696 -e GATEWAY_ACCESS_ID="your-access-id" -e GATEWAY_ACCESS_KEY="matching-access-key" -e ENABLE_TLS="true" -e ENABLE_TLS_CONFIGURE="true" -e ENABLE_TLS_CURL="true" -e ENABLE_TLS_HVP="true" -e MIN_TLS_VERSION="TLSv1.3" -v $PWD/cert.crt:/var/akeyless/conf/api-proxy/akeyless-api-cert.crt -v $PWD/private.key:/var/akeyless/conf/api-proxy/akeyless-api-cert.key --name akeyless-gw akeyless/base:latest-akeyless
```

In the example above,

* The <code>ENABLE_TLS</code> variable enables TLS for the Gateway Console.

* The <code>ENABLE_TLS_CONFIGURE</code> variable enables TLS for the Gateway Configuration Manager.

* The <code>ENABLE_TLS_HVP</code> variable enables TLS for the HVP service.

* The <code>ENABLE_TLS_CURL</code> variable enables TLS for the Akeyless API Services.

* The <code> MIN_TLS_VERSION</code>  variable sets the minimum TLS version that will be supported supporting `<TLSv1/TLSv1.1/TLSv1.2/TLSv1.3>`.

In addition to exclude specific cipher suites, use this variable `EXCLUDE_CIPHER_SUITES` with the relevant suites, you wish to exclude comma-separated.

With the following attributes, you can mount the TLS certificate and the TLS Private Key from the Present Working Directory to the Gateway target directory:

* <code>-v $PWD/cert.crt:/home/akeyless/.akeyless/akeyless-api-cert.crt</code>

* <code>-v $PWD/key.pem:/home/akeyless/.akeyless/akeyless-api-cert.key</code>

It is also possible to [Set up TLS](https://docs.akeyless.io/docs/tls-certificate) in the Gateway Configuration Manager after the Gateway is installed.

# Cache Configuration

You can enable **Local In-Memory** caching of secrets and the periodic backup of cached secrets

```shell Example
docker run -d -p 8000:8000 -p 5696:5696 -e GATEWAY_ACCESS_ID="p-xxxxxxxxxxxx" -e GATEWAY_ACCESS_KEY="62Hu...xxx....qlg=" -e CACHE_ENABLE="true" -e PROACTIVE_CACHE_ENABLE="true" -e CACHE_TTL="60" -e PROACTIVE_CACHE_MINIMUM_FETCHING_TIME="5" -e PROACTIVE_CACHE_DUMP_INTERVAL="1" --name akeyless-gw akeyless/base:latest-akeyless
```
```shell Format
docker run -d -p 8000:8000 -p 8200:8200 -p 5696:5696 -e GATEWAY_ACCESS_ID="your-access-id" -e GATEWAY_ACCESS_KEY="matching-access-key" -e CACHE_ENABLE="true" -e PROACTIVE_CACHE_ENABLE="true" -e CACHE_TTL="number-of-minutes" -e PROACTIVE_CACHE_MINIMUM_FETCHING_TIME="number-of-minutes" -e PROACTIVE_CACHE_DUMP_INTERVAL="number-of-minutes" --name akeyless-gw akeyless/base
```

In the example above,

* `CACHE_TTL` variable allows setting the time (in minutes) during which a secret should be kept in the cache.

* `PROACTIVE_CACHE_MINIMUM_FETCHING_TIME` variable instructs the system to update secrets in the cache if they are older than the specified value.

* `PROACTIVE_CACHE_DUMP_INTERVAL`  variable allows setting the time (in minutes) between the two consecutive backups.

It is also possible to <a href="https://docs.akeyless.io/docs/configure-the-gateway-cache" target="_blank">configure caching</a> in the Gateway Configuration Manager after the Gateway is installed.

# Restrict Gateway Access

To restrict access to Gateway services, you can specify exactly which `AccessIDs` will be authorized and will be served by the Gateway. For example, if you want to achieve complete segregation using [Zero-Knowledge Encryption](https://docs.akeyless.io/docs/zero-knowledge) across different teams or applications, you can also set their `AccessIDs` to ensure only they will be able to get service from the Gateway that holds their Fragment. To set the list of users the Gateway services will serve, set the `RESTRICT_SERVICE_TO_ACCESS_IDS` variable with a comma-separated list of `AccessIDs`

```shell CLI
docker run -d -p 8000:8000 -p 5696:5696 -e GATEWAY_ACCESS_ID="aws-iam-access-id" -e RESTRICT_SERVICE_TO_ACCESS_IDS="comma separated list of access-ids" --name akeyless-gw akeyless/base:latest-akeyless
```
```shell Legacy
docker run -d -p 8000:8000 -p 5696:5696 -e ADMIN_ACCESS_ID="aws-iam-access-id" -e RESTRICT_SERVICE_TO_ACCESS_IDS="comma separated list of access-ids" --name akeyless-gw akeyless/base:latest-akeyless
```

In the above example, in addition to your Gateway admin lists, you are limiting the audience of users that your Gateway will serve. Other `AccessIDs` will not be able to get service from your Gateway. Alternatively to block specific `AccessIDs` you can use the `BLOCKLIST_ACCESS_IDS` variable instead.

# Default Secret Encryption

While the **Encryption Key** section discusses the encryption of the configuration file, this section discusses the secrets created when using the Gateway.
To set a default existing key that will be used to encrypt any secret created through the gateway, add the parameter `DEFAULT_ENCRYPTION_KEY` in the following way:

```shell CLI
docker run -d -p 8000:8000 -p 5696:5696 -e DEFAULT_ENCRYPTION_KEY="existing encryption key name"  --name akeyless-gw akeyless/base:latest-akeyless
```
```shell Legacy
docker run -d -p 8000:8000 -p 5696:5696 -e DEFAULT_ENCRYPTION_KEY="existing encryption key name"  --name akeyless-gw akeyless/base:latest-akeyless
```

# Default Secret Location

To set a default location to which any secret created through the gateway will be saved in your Akeyless account, add the parameter `DEFAULT_SECRET_LOCATION` in the following way:

```shell CLI
docker run -d -p 8000:8000 -p 5696:5696 -e DEFAULT_SECRET_LOCATION="path to relevant folder" --name akeyless-gw akeyless/base:latest-akeyless
```
```shell Legacy
docker run -d -p 8000:8000 -p 5696:5696 -e DEFAULT_SECRET_LOCATION="path to relevant folder" --name akeyless-gw akeyless/base:latest-akeyless
```

# Setting a Default Login

When using OIDC or SAML authentication to connect to the Gateway's web UI on endpoint `/console`, a user would usually be asked to supply an access ID, before being transferred to a login screen. This can also be done from the gateway UI as described in [Gateway SAML & OIDC](https://docs.akeyless.io/docs/gateway-authentication).
When configuring your gateway, you may supply a default value for either OIDC, SAML, or both, using the following parameters:

* `-e DEFAULT_SAML_ACCESS_ID=<SAML Access ID>`
* `-e DEFAULT_OIDC_ACCESS_ID=<OIDC Access ID>`
* `-e AKEYLESS_OIDC_GW_AUTH=true` Optional, to authenticate directly against your Gateway. To leverage your Gateway for the callback redirects instead of the Akeyless SaaS (in cases your IDP isn't publicly available), you can add the `AKEYLESS_OIDC_GW_AUTH` variable while making sure the corresponding OIDC App on your IDP has the "**Redirect URI**" set to the Gateway's configuration endpoint (port 8000) with the following URI suffix `/api/oidc-callback`  (e.g., `https://Your-Akeyless-GW-URL:8000/api/oidc-callback`).

In the following way:

```shell CLI
docker run -d -p 8000:8000 -p 5696:5696 -e DEFAULT_SAML_ACCESS_ID="p-xxxxx"  --name akeyless-gw akeyless/base:latest-akeyless
```

To work with [CBA](https://docs.akeyless.io/docs/certificate-based-authentication) flow for users' login, first set your users' DNS records with the cert authentication subdomain  `auth-cert.akeyless.io` to point to your Gateway IP address.

Set your deployment with the following parameters:

* `-e DEFAULT_CERTIFICATE_ACCESS_ID=<Cert Auth Method Access ID>`
* `-e ENABLE_SNI_PROXY="true"`

In the following way:

```shell CLI
docker run -d -p 8000:8000 -p 5696:5696 -e GATEWAY_ACCESS_ID="aws-iam-access-id" -e DEFAULT_CERTIFICATE_ACCESS_ID="access-id" -e ENABLE_SNI_PROXY="true" --name akeyless-gw akeyless/base:latest-akeyless
```
```shell Legacy
docker run -d -p 8000:8000 -p 5696:5696 -e ADMIN_ACCESS_ID="aws-iam-access-id" -e DEFAULT_CERTIFICATE_ACCESS_ID="access-id" -e ENABLE_SNI_PROXY="true" --name akeyless-gw akeyless/base:latest-akeyless
```

<br />

# Fixed Artifact Repository

In some environments where an IP address must be whitelisted, to pull Akeyless official artifacts as part of your Gateway deployment, you can pass the `ARTIFACTS_REPO="artifacts.site2.akeyless.io"` environment variable as part of the docker run command:

```shell CLI
docker run -d -p 8000:8000 -p 5696:5696 -e ARTIFACTS_REPO="artifacts.site2.akeyless.io" --name akeyless-gw akeyless/base:latest-akeyless
```

# Rate Limit

To set a local rate limit on your Gateway instance you can add the `GW_RATE_LIMIT`  environment variable where the value will set the maximum calls per minute. When a client reaches that threshold, this will be logged and any additional requests during that minute will be discarded on the Gateway:

```shell CLI
docker run -d -p 8000:8000 -p 5696:5696 -e GW_RATE_LIMIT=4000 --name akeyless-gw akeyless/base:latest-akeyless
```

# RHEL Image

To work with a [fully compatible image](https://catalog.redhat.com/software/container-stacks/detail/66016090ff08e22201487dd3) based on the RedHat Universal Image base 8 set the repository source at the end of the `docker run` command with `akeyless/base-rhel` for example:

```shell CLI
docker run -d -p 8000:8000 -p 5696:5696 --name akeyless-gateway akeyless/base-rhel:latest-akeyless
```

# gRPC

To enable **gRPC** on your Gateway set the following environment variable ` ENABLE_GRPC=true`, the service will be exposed on port `8085`:

```shell CLI
docker run -d -p 8000:8000 -p 8085:8085 -p 5696:5696 -e ENABLE_GRPC=true  --name akeyless-gw akeyless/base:latest-akeyless
```
