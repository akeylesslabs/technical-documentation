---
title: Hashicorp Vault Proxy Legacy Configuration
deprecated: false
hidden: false
metadata:
  robots: index
---
## Configuring HashiCorp Vault Proxy

1. Set Akeyless HashiCorp Vault Proxy URL in: `VAULT_ADDR` environment variable:

   ```shell
   export VAULT_ADDR=https://hvp.akeyless.io
   ```

2. Now, you'll need to configure the authentication token that would be used by Vault CLI to fetch secrets from Akeyless.

3. Set your Akeyless token in `~/.vault-token`: `Access Id..Access Key`, for example:

   ```shell
   p-XXXXX..AccessKey
   ```

## Get Dynamic Secret With Vault CLI

```shell
vault read {producer-type}/creds/{full/path/to/producer-name}
```

Supported producer types:

```shell
"*"
"db"           
"mysql"
"mssql"
"mongodb"
"rdp"
"rabbitmq"
"chef"
"aws"
"azure"
```

Example:

```shell
vault read */creds/prod/ds-db1
vault read db/creds/prod/ds-db1
vault read mysql/creds/prod/ds-db1

Key                Value
---                -----
lease_id           */creds/prod/ds-db1/vTyDFRr5m01gVaNBYsokIRop
lease_duration     768h
lease_renewable    true
password           of6B6IY/~+i$$Z80
username           tmp.rnnds.hOKbRAqI5j

vault read */creds/my-aws-producer
vault read aws/creds/my-aws-producer

Key                  Value
---                  -----
lease_id             */creds/my-aws-producer/25F5E8gupyoi2dQIynoM9nff
lease_duration       768h
lease_renewable      true
access_key_id        <Access ID>
secret_access_key    <Access Key>
username             tmp.JJRXoSsvDuj1Dp
```

## Working With Static Secrets

### Create or Update Secret

Create a new static secret in Akeyless. If it already exists, it will add a new version of that secret.

#### Usage

`vault kv put secret/{secret-name} {my-key}={my-value}`

### Get Secret

To retrieve the value from Akeyless:

`vault kv get secret/{secret-name}`

<Callout icon="ℹ️" theme="info">
  ### **Info:**

  An optional flag: `-version` to get a specific version of the secret for example:

  `vault kv get -version=3 secret/{secret-name}`

  Default value is the latest version.
</Callout>

### Delete Secret

To delete a secret from Akeyless:

`vault kv delete secret/{secret-name}`

<Callout icon="ℹ️" theme="info">
  ### **Info:**

  An optional flag: `-versions`, a list of specific versions you would like to delete from Akeyless, for example:

  `vault kv delete -versions=2,6,15 secret/{secret-name}`

  If no version is sent all your secret versions will be deleted as well
</Callout>