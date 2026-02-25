---
title: Azure DevOps Community Plugin
excerpt: ''
deprecated: false
hidden: true
metadata:
  title: ''
  description: ''
  robots: index
next:
  description: ''
---
This page documents the community-maintained Azure DevOps extension published by Lancelot Software.

Use this option when you explicitly prefer the community extension and its single-task model.

## When this option is the best fit

Use the community plugin when you want:

* One task (`akeyless-secrets`) to retrieve static and dynamic secrets.
* Community-maintained behavior and release cadence.
* Dynamic-secret output auto-generation controls (`autogenerate`).

If you want the official Akeyless-maintained extension, use:

* [Azure DevOps Extension](https://docs.akeyless.io/docs/akeyless-azure-devops-extension)

## Getting started

### Install the extension

Install from Visual Studio Marketplace:

* [AKeyless Extensions (LancelotSoftware)](https://marketplace.visualstudio.com/items?itemName=LancelotSoftware.akeyless-extensions)

Or search for `akeyless secrets` in Azure DevOps task selection.

### Initial configuration

1. Configure an Azure service connection that can issue a JWT with `AzureCLI@2`.
2. Configure Akeyless authentication and authorization:
   * [OAuth 2.0/JWT authentication method](https://docs.akeyless.io/docs/auth-with-oauth-jwt)
   * [Access roles (RBAC)](https://docs.akeyless.io/docs/rbac)
   * [Sub-claims](https://docs.akeyless.io/docs/sub-claims)
3. Add the `akeyless-secrets@1` task to your pipeline.
4. Pass:
   * `accessid`
   * `azureJwt`
   * `staticSecrets` and/or `dynamicSecrets`

Reference setup from the upstream project:

* [Community plugin repo](https://github.com/LanceMcCarthy/akeyless-extension-azdo/)
* [Getting started guide](https://github.com/LanceMcCarthy/akeyless-extension-azdo/blob/main/docs/getting-started.md)
* [Examples](https://github.com/LanceMcCarthy/akeyless-extension-azdo/blob/main/docs/examples.md)

## Additional options

From the task manifest, this plugin supports:

* `apiUrl` (default `https://api.akeyless.io`)
* `timeout` (request timeout in seconds)
* `autogenerate` (auto-create individual outputs from dynamic secret JSON)

Operational notes:

* `staticSecrets` and `dynamicSecrets` are dictionary-like JSON strings (path-to-output-name mapping).
* For complex dynamic secret JSON, parse outputs with `jq` or `ConvertFrom-Json` in a follow-up script task.

## Related documentation

* [Plugins Overview](https://docs.akeyless.io/docs/plugins-overview)
* [Azure Plugins](https://docs.akeyless.io/docs/azure-plugins)
* [Static secrets](https://docs.akeyless.io/docs/static-secrets)
* [Dynamic secrets](https://docs.akeyless.io/docs/how-to-create-dynamic-secret)
* [OAuth 2.0/JWT authentication](https://docs.akeyless.io/docs/auth-with-oauth-jwt)

## TODO for maintainers

* TODO: Confirm whether this page should remain `hidden: true` now that it is grouped under Azure plugins and intended as a reusable template example.
