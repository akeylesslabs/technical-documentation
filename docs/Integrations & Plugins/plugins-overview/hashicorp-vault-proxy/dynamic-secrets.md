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

1. Set Akeyless HashiCorp Vault Proxy URL in: `VAULT_ADDR` environment variable:

   ```shell
   export VAULT_ADDR=https://hvp.akeyless.io
   ```

2. Now, you'll need to configure the authentication token that would be used by Vault CLI to fetch secrets from Akeyless.

3. Set your Akeyless token in `~/.vault-token`: `Access Id..Access Key`, for example:

   ```shell
   AccessID..AccessKey
   ```

4. Verify `"hvp_route_version"`  is set to `2` on the gateway:
   ```shell
   akeyless gateway get defaults --gateway-url <your_gateway_url>
   ```

You will see `hvp_route_version`  in the output, if it is set to `1` , update it to `2` .

<Callout icon="📘" theme="info">
  ### Note

  This guide refers to `"hvp_route_version": 2`.

  If your gateway is configured with `"hvp_route_version": 1` , please refer to the legacy configuration [here](https://docs.akeyless.io/docs/hashicorp-vault-proxy-legacy-configuration).&#x20;
</Callout>

# Examples

The following section shows the usage of working with the vault CLI to manage resources in your Akeyless account:

## Get Secret:

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
