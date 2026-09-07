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
      url: https://docs.akeyless.io/docs/how-to-create-dynamic-secret
---
## Vault Token

Many HashiCorp Vault integrations use token-based authentication.

With HashiCorp Vault Proxy, set the Vault token as one of the following values:

* API key format: `<Access ID>..<Access Key>`
* Temporary Akeyless token: `t-...`
* Universal Identity token: `u-...`

Any Akeyless authentication method can be used to obtain a temporary token, then that token can be passed as the Vault token.

Examples:

```shell API Key Token
curl --header "X-Vault-Token: <Access ID>..<Access Key>" \
  https://hvp.akeyless.io/v1/kv/<secret-name>
```
```shell Temporary Token
curl --header "X-Vault-Token: t-XXXXXXXXXXXXXXXX" \
  https://hvp.akeyless.io/v1/kv/<secret-name>
```

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

set the `VAULT_AUTH_ROLE` with your Akeyless [Authentication Method](https://docs.akeyless.io/docs/access-and-authentication-methods) `Access ID` and the `VAULT_AUTH_PATH` with `jwt`. In general, the Vault role should be set with your `Access ID`.

## Kubernetes

HashiCorp Vault Proxy also supports Kubernetes authentication at `auth/kubernetes/login`.

Use `role` as the Base64-encoded value of `<Access ID>..<K8s Auth Config Name>`, and `jwt` as the Kubernetes ServiceAccount JWT.

```shell
vault write auth/kubernetes/login \
  role="<base64(Access ID..K8s Auth Config Name)>" \
  jwt="<kubernetes-serviceaccount-jwt>"
```

For a full implementation example with cert-manager, see [Cert Manager](https://docs.akeyless.io/docs/cert-manager).

> ℹ️ **Note:**
>
> Kubernetes authentication by way of HashiCorp Vault Proxy depends on client support for the Kubernetes auth flow.
