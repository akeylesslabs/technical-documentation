---
title: Azure DevOps Plugin
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
2. Set Vault URL to `https://hvp.akeyless.io` or to your Akeyless Gateway Vault Proxy endpoint.
3. Set authentication to **Client Token** and provide an Akeyless token.
4. Set KV path/version for your retrieval model (static-like KV paths or dynamic-like producer paths exposed through Vault-compatible routes).

Compatibility reference:

* [HashiCorp Vault Proxy](https://docs.akeyless.io/docs/hashicorp-vault-proxy)
* [HashiCorp Vault Proxy Authentication Methods](https://docs.akeyless.io/docs/vault-proxy-authentication-methods)

## Additional options

You can authenticate by building a token from API Key material or by obtaining a token from another auth method:

```shell
akeyless auth --access-id <Access ID> --access-type <Auth method type>
```

Related authentication references:

* [Authentication methods overview](https://docs.akeyless.io/docs/access-and-authentication-methods)
* [API Key authentication](https://docs.akeyless.io/docs/auth-with-api-key)

For the Vault Interaction extension itself, review its own task options and caveats (for example recursive discovery and variable prefix behavior) in the Marketplace page.

## Related documentation

* [Plugins Overview](https://docs.akeyless.io/docs/plugins-overview)
* [Azure Plugins](https://docs.akeyless.io/docs/azure-plugins)
* [HashiCorp Vault Proxy](https://docs.akeyless.io/docs/hashicorp-vault-proxy)
* [Static secrets](https://docs.akeyless.io/docs/static-secrets)
* [Dynamic secrets](https://docs.akeyless.io/docs/how-to-create-dynamic-secret)

## TODO for maintainers

* TODO: Validate and document one tested YAML example for KV v1 and one for KV v2 against current Vault Interaction extension version, including exact `VaultReadKV@` major version.
* TODO: Add an explicit gateway endpoint format example that is verified against the current gateway deployment docs (port/path vary by deployment mode).
