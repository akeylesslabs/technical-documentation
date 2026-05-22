---
title: Azure DevOps with Vault Proxy Plugin
excerpt: ''
deprecated: false
hidden: false
metadata:
  title: ''
  description: ''
  robots: index
next:
  description: ''
---
This page covers the Vault Interaction-based integration path for Azure DevOps.

This option uses Akeyless HashiCorp Vault Proxy compatibility and a third-party Vault task in Azure DevOps.

## When this option is the best fit

Use this plugin path when you want:

* To keep existing Vault-oriented pipeline patterns.
* To consume Akeyless through HashiCorp Vault-compatible endpoints.
* A migration bridge from HashiCorp Vault OSS plugins to Akeyless.

For direct, first-party Akeyless Azure DevOps tasks, use:

* [Azure DevOps Extension](https://docs.akeyless.io/docs/akeyless-azure-devops-extension)

## Getting started

### Install the extension

Install the Vault Interaction extension from Visual Studio Marketplace:

* [Vault Interaction (Fizcko)](https://marketplace.visualstudio.com/items?itemName=Fizcko.azure-devops-vault-interaction)

### Initial configuration

1. Add the **Vault - Read KV secrets** task (`VaultReadKV`) to your pipeline.
2. Set Vault URL to one of these endpoints:

    * `https://hvp.akeyless.io` (Akeyless public Vault Proxy endpoint)
    * `https://<your-gateway-host>:8200` (Akeyless Gateway Vault Proxy endpoint)

3. Set authentication to **Client Token** and provide an Akeyless token.
4. Set KV path/version for your retrieval model (static-like KV paths or dynamic-like producer paths exposed through Vault-compatible routes).

For API Key authentication, the token can be provided in this format:

* `<Access ID>..<Access Key>`

Store token values in secure variables.

## Usage

### KV v1 static secret retrieval with `VaultReadKV@5`

```yaml
- task: VaultReadKV@5
  inputs:
    strUrl: 'https://hvp.akeyless.io'
    ignoreCertificateChecks: true
    strAuthType: 'clientToken'
    strToken: '$(AKEYLESS_TOKEN)'
    strKVEnginePath: 'kv'
    kvVersion: 'v1'
    strSecretPath: 'my-static-secret'
    strPrefixType: 'custom'
    strVariablePrefix: 'APP'
    replaceCR: false
```

### KV v2 static secret retrieval with `VaultReadKV@5`

```yaml
- task: VaultReadKV@5
  inputs:
    strUrl: 'https://hvp.akeyless.io'
    ignoreCertificateChecks: false
    strAuthType: 'clientToken'
    strToken: '$(AKEYLESS_TOKEN)'
    strKVEnginePath: 'secret'
    kvVersion: 'v2'
    strSecretPath: 'my-app/prod'
    strPrefixType: 'custom'
    strVariablePrefix: 'APP'
    replaceCR: false
```

### Dynamic-style retrieval with `VaultReadKV@5`

```yaml
- task: VaultReadKV@5
  inputs:
    strUrl: 'https://hvp.akeyless.io'
    ignoreCertificateChecks: false
    strAuthType: 'clientToken'
    strToken: '$(AKEYLESS_TOKEN)'
    strKVEnginePath: 'mysql/creds'
    kvVersion: 'v1'
    strSecretPath: 'readonly'
    strPrefixType: 'custom'
    strVariablePrefix: 'DB'
    replaceCR: false
```

Example script usage after retrieval:

```yaml
- script: |
    mysql --host XXXXX --port 3306 --user=$(DB_username) --password='$(DB_password)' -e 'show databases;'
  displayName: 'Show Databases in DB'
```

Compatibility reference:

* [HashiCorp Vault Proxy](https://docs.akeyless.io/docs/hashicorp-vault-proxy)
* [HashiCorp Vault Proxy Authentication Methods](https://docs.akeyless.io/docs/vault-proxy-authentication-methods)

## Additional options

For an API Key auth method, generate a token with:

```shell
akeyless auth --access-type access_key --access-id <Access ID> --access-key <Access Key>
```

Related authentication references:

* [Authentication methods overview](https://docs.akeyless.io/docs/access-and-authentication-methods)
* [API Key authentication](https://docs.akeyless.io/docs/auth-with-api-key)

For the Vault Interaction extension itself, review its task options and caveats (for example, recursive discovery and variable prefix behavior) in the [Vault Interaction Marketplace page](https://marketplace.visualstudio.com/items?itemName=Fizcko.azure-devops-vault-interaction).

Current examples use `VaultReadKV@5`, aligned with the Vault Interaction Marketplace examples and current extension major version documentation.

## Restored Visuals

![Restored visual: Capture222](https://files.readme.io/c775c07-Capture222.JPG)

![Restored visual: pasted image 0 3](https://files.readme.io/cbd4b8b-pasted_image_0_3.png)
