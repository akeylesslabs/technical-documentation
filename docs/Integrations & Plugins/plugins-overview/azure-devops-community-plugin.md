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
# Overview

Azure DevOps is a set of tools and services that help DevOps teams provision and manage the lifecycle of production environments.

With [this](https://github.com/LanceMcCarthy/akeyless-extension-azdo/) **community** plugin, you can fetch secrets directly from the Akeyless Platform into your workflows.

This guide will demonstrate the use of an [ OAuth 2.0 / JWT](https://docs.akeyless.io/docs/oauth20jwt) **Authentication Method** to fetch both [Static ](https://docs.akeyless.io/docs/static-secrets)and [Dynamic](https://docs.akeyless.io/docs/how-to-create-dynamic-secret) secrets from Akeyless.

# Prerequisites

1. An Azure Service Connection (see [here](https://github.com/LanceMcCarthy/akeyless-extension-azdo/blob/main/docs/getting-started.md#azure-setup) for setup if you don't have)
2. A [JWT Authentication Method](https://docs.akeyless.io/docs/oauth20jwt) that points to the Service Connection with `Read` access to secrets
3. The Akeyless extension added to your Azure DevOps pipeline. You can do this in one of two ways:
   1. Search for 'akeyless secrets' when adding a new task
   2. Go to [Akeyless Extensions - Visual Studio Marketplace](https://marketplace.visualstudio.com/items?itemName=LancelotSoftware.akeyless-extensions)

> 📘 Step-by-Step
> 
> If this is your first time using the extension, see the documentation here to make sure you have the required prerequisites prepared: [Setup Akeyless and Azure service principal](https://github.com/LanceMcCarthy/akeyless-extension-azdo/blob/main/docs/getting-started.md).

# Authentication

The following Authentication Methods can be used for authentication:

## OAuth 2.0 / JWT

Create a new [OAuth 2.0 / JWT](https://docs.akeyless.io/docs/oauth20jwt) **Authentication Method** using the CLI:

```shell
akeyless create-auth-method-oauth2 --name /Dev/AzureAuth  \
--jwks-uri https://login.microsoftonline.com/common/discovery/keys \
--unique-identifier appid=<appid-string> \
--force-sub-claims
```

Where:

- `--jwks-uri` - The URL to the `JWKS` that contains the public keys that would be used for JWT verification.

- `--unique identifier` - For the unique identifier, you can use the Azure service principal's `tenantid`, or `appid`. Whenever a user logs in with a token, these authentication types issue [Sub-Claims](doc:sub-claims)  that contains details uniquely identifying that user. This sub-claim includes a key containing the ID value you configured and is used to distinguish between users from within the same organization. You can find your `appid` in your Azure DevOps account in "Project settings" -> "Service connections" -> Click on your connection -> "Manage App registration".

- `--force-sub-claims` -  Enforce role association to include sub-claims.

Create an **[Access Role](https://docs.akeyless.io/docs/rbac)**:

```shell
akeyless create-role --name /Dev/AzureRole
```

> 🚧 Warning
> 
> ** It is required ** to add appropriate [Sub-Claims](https://docs.akeyless.io/docs/sub-claims) based on the [claims available in the JWT](https://docs.github.com/en/actions/deployment/security-hardening-your-deployments/about-security-hardening-with-openid-connect#understanding-the-oidc-token) to prevent access by unauthorized users.
> 
> Sub-Claim configuration allows Akeyless to grant access to specific workflows, based on the claims that Azure DevOps provides in the JWT.

Attach your `OAuth 2.0 / JWT` **Authentication Method** to the **Access Role** that was created and add an appropriate **Sub-Claim**, for example: `appid=<appid-string>`.

```shell
akeyless assoc-role-am --role-name /Dev/AzureRole \
--am-name /Dev/AzureAuth  \
--sub-claims appid=<appid-string>
```

Set `Read` permissions for **Items **for the **Access Role**:     

```shell
akeyless set-role-rule --role-name /Dev/AzureRole \
--path /Path/To/your/secret/'*' \
--capability read
```

# Usage

The following examples will demonstrate how to fetch [Static](https://docs.akeyless.io/docs/static-secrets) and [Dynamic](https://docs.akeyless.io/docs/how-to-create-dynamic-secret) secrets from Akeyless.

> 📘 Classic Pipelines
> 
> If you are using classic pipelines, you will find the `Reference Name` under the `Output Variables` section. This will be the `name` of your task in the YAML file.

## Fetching Static Secrets

For static secrets, you will get an individual secret output variable for each secret. For example:

```yaml
steps:
- task: AzureCLI@2
  name: 'AzureCLI'
  displayName: 'Get JWT from Azure'
  inputs:
    azureSubscription: 'service-connection-name'
    scriptType: ps
    scriptLocation: inlineScript
    inlineScript: |
     $JWT=$(az account get-access-token --query accessToken --output tsv)
     echo "##vso[task.setvariable variable=azure_jwt;isoutput=true;issecret=true]$JWT"

- task: akeyless-secrets@1
  name: 'MyAkeylessTask'
  displayName: 'Get Secrets from Akeyless'
  inputs:
    accessid: '<your-access-id>'
    azureJwt: '$(AzureCLI.azure_jwt)'
    staticSecrets: '{"/path/to/first-secret":"first_secret", "/path/to/second-secret":"second_secret" }'
```

> 📘 JWT Usage
> 
> Note that we are using the `azure_jwt` output from the `AzureCLI` task to hold the JWT, then use it in the `akeyless-secret` task with `$(AzureCLI.azure_jwt)`.

You will also have `$(MyAkeylessTask.first_secret)` and  `$(MyAkeylessTask.second_secret)` available in subsequent tasks of that job if needed.

## Fetching Dynamic Secrets

For dynamic secrets, the output variable that holds all of that dynamic secret's output. For example:

```yaml
steps:
- task: AzureCLI@2
  name: 'AzureCLI'
  displayName: 'Get JWT from Azure'
  inputs:
    azureSubscription: 'service-connection-name'
    scriptType: ps
    scriptLocation: inlineScript
    inlineScript: |
     $JWT=$(az account get-access-token --query accessToken --output tsv)
     echo "##vso[task.setvariable variable=azure_jwt;isoutput=true;issecret=true]$FRESH_JWT"

- task: akeyless-secrets@1
  name: 'MyAkeylessTask'
  displayName: 'Get Secrets from Akeyless'
  inputs:
    accessid: '<your-access-id>'
    azureJwt: '$(AzureCLI.azure_jwt)'
    dynamicSecrets: '{"/path/to/dynamic/secret":"my_dynamic_secret"}'
```

You will also have `$(MyAkeylessTask.my_dynamic_secret)` available in subsequent tasks of that job if needed.

### Using jq to Parse Credentials

Dynamic secrets are more complex objects and you will likely need to further process the temporary credentials to get each value individually.

For example, with a MySQL dynamic secret, you can use `jq` to get each separate value:

```shell
echo '$(MyAkeylessTask.MY_SQL_DYNAMIC_SECRET)' | jq -r 'to_entries|map("SQL_\(.key|ascii_upcase)=\(.value|tostring)")|.[]' >> $SQL

echo $SQL.id
echo $SQL.user
echo $SQL.ttl_in_minutes
echo $SQL.password
```

For additional information use this [link](https://github.com/LanceMcCarthy/akeyless-extension-azdo/).

For a Complete walkthrough demo, go to this link: [Example (Tutorial)](https://github.com/LanceMcCarthy/akeyless-extension-azdo/blob/main/docs/examples.md):