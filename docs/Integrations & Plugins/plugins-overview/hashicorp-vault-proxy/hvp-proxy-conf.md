---
title: Vault Proxy Configuration
excerpt: Configuring Secrets with HashiCorp Vault Proxy
deprecated: false
hidden: false
metadata:
  title: ''
  description: ''
  robots: index
next:
  description: ''
---
## Configuring HashiCorp Vault Proxy

1. Set the `VAULT_ADDR` environment variable to point to your proxy endpoint

   **Custom Endpoint:**

   ```shell Shell
   export VAULT_ADDR=https://your_gw_url:8200
   ```

   **Akeyless SaaS Proxy:**

   ```shell
   export VAULT_ADDR=https://hvp.akeyless.io
   ```

**Note:&#x20;**&#x43;ustom Gateways require port `:8200` for Vault Proxy traffic.

2. Now, you'll need to configure the authentication token that would be used by Vault CLI to fetch secrets from Akeyless.

   Set your Akeyless token in `~/.vault-token`: `Access Id..Access Key`, for example:
   ```shell
   AccessID..AccessKey
   ```
3. Verify `"hvp_route_version"`  is set to `2` on the gateway (Custom Gateway Only):
   ```shell
   akeyless gateway get defaults --gateway-url <your_gateway_url>
   ```

For Custom Gateways, ensure that `hvp_route_version` is set to `2`.

<Callout icon="📘" theme="info">
  ### Legacy Route Version 1:

  If your environment strictly requires `hvp_route_version": 1`, please refer to our [Legacy HVP Configuration Guide](https://docs.akeyless.io/docs/hashicorp-vault-proxy-legacy-configuration).
</Callout>

# Examples

The following section shows the usage of working with the vault CLI to manage resources in your Akeyless account:

## Fetching Secrets:

To retrieve a [Dynamic](https://docs.akeyless.io/docs/how-to-create-dynamic-secret), [Rotated](https://docs.akeyless.io/docs/rotated-secrets) and [Static](https://docs.akeyless.io/docs/static-secrets) using the Vault CLI via HashiCorp Vault Proxy, run:

```shell
vault read /<full_secret_name>
```

### Create or Update a Static Secret

Create a new static secret in Akeyless. If it already exists, it will add a new version of that secret.

#### Usage

`vault kv put secret/{secret-name} {my-key}={my-value}`

### Delete a Static Secret

To delete a secret from Akeyless:

`vault kv delete secret/{secret-name}`

<br />