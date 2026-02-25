---
title: Azure DevOps Community Plugin
excerpt: ''
deprecated: false
hidden: true
metadata:
  title: ''
  description: ''
  robots: noindex
next:
  description: ''
---
This page documents the community-maintained Azure DevOps extension published by Lancelot Software.

Choose this option when you need the community extension's single-task workflow for static and dynamic secret retrieval.

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

## Usage

### Authentication setup example (OAuth 2.0/JWT)

Create an OAuth 2.0/JWT auth method:

```shell
akeyless auth-method create oauth2 --name /Dev/AzureAuth \
--jwks-uri https://login.microsoftonline.com/common/discovery/keys \
--unique-identifier appid=<appid-string>
```

Create an access role and associate the auth method with sub-claims:

```shell
akeyless create-role --name /Dev/AzureRole

akeyless assoc-role-am --role-name /Dev/AzureRole \
--am-name /Dev/AzureAuth \
--sub-claims appid=<appid-string>

akeyless set-role-rule --role-name /Dev/AzureRole \
--path /Path/To/your/secret/'*' \
--capability read
```

### Pipeline examples

#### Static secrets

```yaml
steps:
- task: AzureCLI@2
  name: AzureCLI
  displayName: 'Get JWT from Azure'
  inputs:
    azureSubscription: 'service-connection-name'
    scriptType: ps
    scriptLocation: inlineScript
    inlineScript: |
      $JWT=$(az account get-access-token --query accessToken --output tsv)
      echo "##vso[task.setvariable variable=azure_jwt;isoutput=true;issecret=true]$JWT"

- task: akeyless-secrets@1
  name: MyAkeylessTask
  displayName: 'Get Secrets from Akeyless'
  inputs:
    accessid: '<your-access-id>'
    azureJwt: '$(AzureCLI.azure_jwt)'
    staticSecrets: '{"/path/to/first-secret":"first_secret", "/path/to/second-secret":"second_secret" }'
```

#### Dynamic secrets

```yaml
steps:
- task: AzureCLI@2
  name: AzureCLI
  displayName: 'Get JWT from Azure'
  inputs:
    azureSubscription: 'service-connection-name'
    scriptType: ps
    scriptLocation: inlineScript
    inlineScript: |
      $JWT=$(az account get-access-token --query accessToken --output tsv)
      echo "##vso[task.setvariable variable=azure_jwt;isoutput=true;issecret=true]$JWT"

- task: akeyless-secrets@1
  name: MyAkeylessTask
  displayName: 'Get Secrets from Akeyless'
  inputs:
    accessid: '<your-access-id>'
    azureJwt: '$(AzureCLI.azure_jwt)'
    dynamicSecrets: '{"/path/to/dynamic/secret":"my_dynamic_secret"}'
```

Dynamic secret parsing example with `jq`:

```shell
echo '$(MyAkeylessTask.MY_SQL_DYNAMIC_SECRET)' | jq -r 'to_entries|map("SQL_\(.key|ascii_upcase)=\(.value|tostring)")|.[]' >> $SQL

echo $SQL.id
echo $SQL.user
echo $SQL.ttl_in_minutes
echo $SQL.password
```

## Additional options

From the task manifest, this plugin supports:

* `apiUrl` (default `https://api.akeyless.io`)
* `timeout` (request timeout in seconds)
* `autogenerate` (auto-create individual outputs from dynamic secret JSON)

Operational notes:

* `staticSecrets` and `dynamicSecrets` are dictionary-like JSON strings (path-to-output-name mapping).
* For complex dynamic secret JSON, parse outputs with `jq` or `ConvertFrom-Json` in a follow-up script task.
