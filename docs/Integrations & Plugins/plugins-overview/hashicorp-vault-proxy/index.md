---
title: HashiCorp Vault Proxy
excerpt: HashiCorp Vault Proxy
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
      title: Vault Proxy Dynamic Secrets
      url: https://docs.akeyless.io/docs/how-to-create-dynamic-secret
slug: hashicorp-vault-proxy
---
Akeyless developed API compatibility with HashiCorp Vault OSS, enabling the use of Vault OSS community plugins for both Static, Rotated and Dynamic Secrets.

Benefits:

- Extending the variety of platform plugins
- Side-by-side scenarios with vault repositories
- Easing migrations from existing solutions
- Supporting **KV** and Dynamic Secrets.

Interaction with the Akeyless vault proxy can be done against our public endpoint: `https://hvp.akeyless.io`

Or directly through your [Gateway](https://docs.akeyless.io/docs/gateway-overview) on port `8200`.

## Related Pages

Use the following pages for HashiCorp Vault Proxy integrations and configuration details:

- [GitHub Actions by way of HashiCorp Vault Proxy](https://docs.akeyless.io/docs/github-actions-hvp)
- [HashiCorp Vault Proxy Authentication Methods](https://docs.akeyless.io/docs/vault-proxy-authentication-methods)
- [Vault Proxy Dynamic Secrets](https://docs.akeyless.io/docs/how-to-create-dynamic-secret)
- [Jenkins Plugin by way of HashiCorp Vault Proxy](https://docs.akeyless.io/docs/jenkins-plugin-via-hvp)
- [TeamCity Plugin by way of HashiCorp Vault Proxy](https://docs.akeyless.io/docs/teamcity-hcv-plugin)

## Usage

HashiCorp Vault `V1` secret engine proxy will be available using this prefix: `v1/kv`

```shell Vault Proxy V1
curl --header "X-Vault-Token: XXXXX" https://hvp.akeyless.io/v1/kv/{secret-name}
```

HashiCorp Vault `V2` secret engine will be available using this prefix: `v1/secret/data`

```shell Vault Proxy V2
curl --header "X-Vault-Token: XXXX" https://hvp.akeyless.io/v1/secret/data/{secret-name}
```

If the secret value itself is a JSON-structured object, the **Path** must be in the following format:

`secret/<Full Secret Name>`, without the `data/` prefix, you can use the internal JSON keys as the **Key Names**

### Custom Engine Name

Custom engine names can also be used for accessing secrets by replacing the default engine name with the custom engine name in the URL:

```shell
curl --header "X-Vault-Token: XXXXX" https://hvp.akeyless.io/v1/{custom-engine-name}/{secret-name}
```

<br />
