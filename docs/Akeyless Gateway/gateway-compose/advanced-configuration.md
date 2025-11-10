---
title: Advanced Configuration
excerpt: Docker Compose Gateway
deprecated: false
hidden: false
metadata:
  title: ''
  description: ''
  robots: index
next:
  description: ''
---
In this guide, we will configure settings in the `gateway.env` file. This file has to be located in the same directory the `docker-compose.yaml` file is located.

# Cluster Name & URL

Each Gateway instance is uniquely identified by combining the **Gateway Access ID**  Authentication Method and the **Cluster Name**.

It means that changing the Gateway **Access ID** or the **Cluster Name** of your Gateway instance will create an entirely new Gateway instance, and it will not retrieve the settings and data from the previous Gateway instance.

That’s why we recommend setting up a meaningful Cluster Name for your Gateway instance from the very beginning. By default, your cluster name is `defaultcluster`.

To do that, edit the `gateway.env` file:

```yaml gateway.env
 CLUSTER_NAME: <meaningful-cluster-name>
```

You can also provide a custom display name for the Gateway Instance using the `INITIAL_DISPLAY_NAME`  variable, but this is arbitrary. This name can be changed in the Akeyless Console after the Gateway is installed.

# Customer Fragment

If your [Encryption Key](https://docs.akeyless.io/docs/encryption-keys) works with [Zero Knowledge](https://docs.akeyless.io/docs/implement-zero-knowledge), add the `CUSTOMER_FRAGMENT` as a `JSON` file in your `gateway.env`:

```yaml gateway.env
CUSTOMER_FRAGMENTS: <Customer Fragment>
```

Note: When adding multiple Customer Fragments to the Gateway, make sure they are in the same JSON file.

# Version Selection

To work with a specific Gateway version use the `VERSION` setting in your `gateway.env` file:

```yaml gateway.env
VERSION: x.y.z
```

# TLS Configuration

We strongly recommend using Akeyless Gateway with TLS to ensure all traffic is encrypted at transit.\
Please note that when you're enabling TLS, you must provide a `TLS certificate` and a `TLS Private Key` in `PEM` format.

Add the following to the `gateway.env` file to use TLS Certificate:

```yaml docker-compose.yaml
ENABLE_TLS="true"		# enables TLS for the Gateway Console.
ENABLE_TLS_CONFIGURE="true"	# enables TLS for the Gateway Configuration Manager.
ENABLE_TLS_HVP="true"		# enables TLS for the HVP service.
ENABLE_TLS_CURL="true"		# enables TLS for the Akeyless API Services
ENABLE_TLS_CONFIGURE=true
volumes:
- ./PWD/cert.crt:/home/akeyless/.akeyless/akeyless-api-cert.crt
- ./PWD/key.pem:/home/akeyless/.akeyless/akeyless-api-cert.key
```

In the example above,

* The `ENABLE_TLS` variable enables TLS for the Gateway Console.

* The `ENABLE_TLS_CONFIGURE` variable enables TLS for the Gateway Configuration Manager.

* The `ENABLE_TLS_HVP` variable enables TLS for the HVP service.

* The `ENABLE_TLS_CURL` variable enables TLS for the Akeyless API Services.

* The `MIN_TLS_VERSION` variable sets the minimum TLS version that will be supported supporting `<TLSv1/TLSv1.1/TLSv1.2/TLSv1.3>`.

In addition to exclude specific cipher suites use this variable `EXCLUDE_CIPHER_SUITES` with the relevant suites, you wish to exclude comma-separated.

Once the settings are set in the `gateway.env` file, mount the **TLS certificate** and the **TLS Private Key** from the Present Working Directory to the Gateway target directory. (This should be done using the `docker-compose.yaml`) file:

```yaml docker-compose.yaml
volumes:
      - ./<Path-To-Cert>:/home/akeyless/.akeyless/akeyless-api-cert.crt    
      - ./<Path-To-Key>:/home/akeyless/.akeyless/akeyless-api-cert.key
```

It is also possible to [Set up TLS](https://docs.akeyless.io/docs/tls-certificate) in the Gateway Configuration Manager after the Gateway is installed.

# Cache Configuration

You can enable caching of secrets and periodic backup of cached secrets using the `gateway.env` file:

```yaml gateway.env
CACHE_ENABLE="true"
PROACTIVE_CACHE_ENABLE="true"
USE_CLUSTER_CACHE="true"
GATEWAY_CLUSTER_CACHE="enable"
```
It is also possible to [configure cache](https://docs.akeyless.io/docs/configure-the-gateway-cache)  in the Gateway Configuration Manager after the Gateway is installed.

NOTE: If you enable the Gateway cluster cache, you must define a Redis password. Edit the cache.env file in this folder and set: REDIS_PASS='your-REDIS-password'
The password is stored in the Cache.env file and is referenced by both the redis-cache service and the Gateway (gateway.env). Replace the example value with your own and keep this file out of source control.

# Restrict Gateway Access

To restrict access to Gateway services, you can specify exactly which `AccessIDs` will be authorized and will be served by the Gateway. For example, if you want to achieve complete segregation using [Zero-Knowledge Encryption](https://docs.akeyless.io/docs/zero-knowledge) across different teams or applications, you can also set their `AccessIDs` to ensure only they will be able to get service from the Gateway that holds their Fragment. To set the list of users the Gateway services will serve, set the `RESTRICT_SERVICE_TO_ACCESS_IDS` variable with a comma-separated list of `AccessIDs`

```yaml docker-compose.yaml
RESTRICT_SERVICE_TO_ACCESS_IDS: <"comma separated list of access-ids">
```

In the above example, in addition to your Gateway admin lists, you are limiting the audience of users that your Gateway will serve. Other `AccessIDs` will not be able to get service from your Gateway. Alternatively to block specific `AccessIDs` you can use the `BLOCKLIST_ACCESS_IDS` variable instead. 

# Default Secret Encryption

While the **Encryption Key** section discusses the encryption of the configuration file, this section discusses the secrets created when using the Gateway.\
To set a default existing key that will be used to encrypt any secret created through the gateway, add the parameter `DEFAULT_ENCRYPTION_KEY` in the following way:

```yaml docker-compose.yaml
DEFAULT_ENCRYPTION_KEY: <"existing encryption key name">
```

# Setting a Default Login

When using OIDC or SAML authentication to connect to the Gateway's web UI on endpoint `/console` , a user would usually be asked to supply an access ID, before being transferred to a login screen. This can also be done from the gateway UI as described in [Gateway SAML & OIDC](https://docs.akeyless.io/docs/gateway-authentication).\
When configuring your gateway, you may supply a default value for either OIDC, SAML, or both, using the following parameters:

* `DEFAULT_SAML_ACCESS_ID=<SAML Access ID>`
* `DEFAULT_OIDC_ACCESS_ID=<OIDC Access ID>`
* `AKEYLESS_OIDC_GW_AUTH=true` Optional, to authenticate directly against your Gateway. 

Add the following to the `gateway,env` file:

```yaml gateway.env
DEFAULT_SAML_ACCESS_ID: <Access ID>
```
