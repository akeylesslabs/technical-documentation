---
title: HashiCorp Vault Proxy Authentication Methods
excerpt: ''
deprecated: false
hidden: false
metadata:
  title: ''
  description: ''
  robots: index
next:
  description: ''
  pages:
    - type: link
      title: HashiCorp Vault Proxy Dynamic Secrets
      url: https://docs.akeyless.io/docs/dynamic-secrets
---
## HashiCorp Vault AppRole

Some of Vault’s plugins support only AppRole authentication.

For those types of plugins, you’ll need to specify `role_id` and `secret_id`. When using HashiCorp Vault Proxy, use `Access Id` and `Access key`, replacing `role_id` and `secret_id` correspondingly.

For example, Vault AppRole authentication using HashiCorp Vault Proxy:

```shell
export VAULT_ADDR='https://hvp.akeyless.io'
vault write auth/approle/login role_id="<Access Id>" secret_id="<Access Key>"
```

## JWT

To work with Vault plugins using JWT authentication for example GitLab:

```shell
job:
  variables:
    VAULT_SERVER_URL: 'https://hvp.akeyless.io'
    VAULT_AUTH_PATH: jwt
    VAULT_AUTH_ROLE: <Access ID>
  id_tokens:
    VAULT_ID_TOKEN:
      aud: https://gitlab.com
```

set the `VAULT_AUTH_ROLE` with your Akeyless [Authentication Method](https://docs.akeyless.io/docs/access-and-authentication-methods) `Access ID` and the `VAULT_AUTH_PATH` with `jwt`. In general, the Vault role should be set with your `Aceess ID`.
