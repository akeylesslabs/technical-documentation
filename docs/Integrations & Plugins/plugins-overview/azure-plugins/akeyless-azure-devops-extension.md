---
title: Azure DevOps Extension
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
The official Akeyless Azure DevOps extension integrates Azure Pipelines with Akeyless secret retrieval workflows.

Use this extension to authenticate to Akeyless, fetch static secrets, and retrieve dynamic or rotated secrets directly in pipeline jobs.

Any Akeyless API operation performed by this extension is logged with source `Azure-DevOps-Extension` in [Akeyless Audit Logs](https://docs.akeyless.io/docs/audit-logs).

## When this option is the best fit

Use this extension when you want:

* A first-party Akeyless integration for Azure DevOps.
* A dedicated Akeyless service connection type in Azure DevOps.
* Separate tasks for authentication, static secrets, dynamic secrets, and rotated secrets.

The extension contribution manifest and task metadata in the source repo define the following task names:

* `akeyless-auth`
* `akeyless-get-secrets-value-task`
* `akeyless-get-dynamic-secret-value-task`
* `akeyless-get-rotated-secret-value-task`

## Getting started

### Install the extension

Install from Visual Studio Marketplace:

* [Akeyless Secrets Management (Akeyless-Engineering)](https://marketplace.visualstudio.com/items?itemName=Akeyless-Engineering.akeyless-secrets-management)

Then add it to your Azure DevOps organization from **Organization settings > Extensions**.

### Initial configuration

1. Create an Akeyless service connection in **Project settings > Service connections**.
2. Set the service connection URL to your Akeyless endpoint, for example:
   * `https://api.akeyless.io`
   * `https://my.gw/api/v2`
3. Set the service connection Access ID.
4. Add pipeline tasks in this order:
   1. **Akeyless Authenticate**
   2. One of:
      * **Akeyless Get Secrets Value**
      * **Akeyless Get Dynamic Secrets Value**
      * **Akeyless Get Rotated Secret Value**

For authentication setup in Akeyless, see:

* [API Key authentication](https://docs.akeyless.io/docs/auth-with-api-key)
* [OAuth 2.0/JWT authentication](https://docs.akeyless.io/docs/auth-with-oauth-jwt)
* [Azure AD authentication](https://docs.akeyless.io/docs/auth-with-azure)

## Additional options

Use these task inputs when needed:

* **Akeyless Authenticate**:
    * `access-key` (API Key flow)
    * `jwt` (JWT flow)
* **Akeyless Get Secrets Value**:
    * `secretsPaths` (comma-separated `k=v` pairs)
    * `ignoreCache`
    * `accessibility` (`regular`, `personal`, `sharing`)
    * `version`
* **Akeyless Get Dynamic Secrets Value**:
    * `target`
    * `timeout`
    * `args`
    * `host`
* **Akeyless Get Rotated Secret Value**:
    * `ignoreCache`
    * `version`
    * `host`

Known limitation from current extension docs:

* Supported authentication methods are API Key and JWT.

## Related documentation

* [Plugins Overview](https://docs.akeyless.io/docs/plugins-overview)
* [Azure Plugins](https://docs.akeyless.io/docs/azure-plugins)
* [HashiCorp Vault Proxy](https://docs.akeyless.io/docs/hashicorp-vault-proxy)
* [Static secrets](https://docs.akeyless.io/docs/static-secrets)
* [Dynamic secrets](https://docs.akeyless.io/docs/how-to-create-dynamic-secret)
* [Rotated secrets](https://docs.akeyless.io/docs/rotated-secrets)

## TODO for maintainers

* TODO: Validate and document the canonical YAML invocation aliases for each task in Azure Pipelines examples (`...@0` usage differs between historical examples in docs).
