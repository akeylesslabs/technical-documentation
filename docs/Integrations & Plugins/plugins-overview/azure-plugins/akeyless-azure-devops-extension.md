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

Install and add the extension to your Azure DevOps organization:

1. Go to your Azure DevOps organization (for example, `https://dev.azure.com/<your-org>`).
2. Select **Organization settings > Extensions**, then select **Browse marketplace**.
3. Open [Akeyless Secrets Management (Akeyless-Engineering)](https://marketplace.visualstudio.com/items?itemName=Akeyless-Engineering.akeyless-secrets-management).
4. Select **Get it free** or **Install**, then select your organization to complete installation.

### Initial configuration

1. Create an Akeyless service connection in **Project settings > Service connections**.
2. Set the service connection URL to your Akeyless endpoint, for example:
   * `https://api.akeyless.io`
   * `https://my.gw/api/v2`
3. Set the service connection Access ID.
4. Add pipeline tasks in this order:
   1. **Akeyless Authenticate**
   2. One or more of:
      * **Akeyless Get Secrets Value**
      * **Akeyless Get Dynamic Secrets Value**
      * **Akeyless Get Rotated Secret Value**

When creating the service connection, configure these fields:

* **Akeyless API Base URL**
* **Access ID**
* **Service connection name** (used in pipeline YAML)
* **Description** (optional)
* **Grant access permission to all pipelines** (optional)

For authentication setup in Akeyless, see:

* [API Key authentication](https://docs.akeyless.io/docs/auth-with-api-key)
* [OAuth 2.0/JWT authentication](https://docs.akeyless.io/docs/auth-with-oauth-jwt)
* [Azure AD authentication](https://docs.akeyless.io/docs/auth-with-azure)

## Usage

### API Key authentication and static secret retrieval

This example authenticates with an API Key, fetches multiple static secrets, and passes them into a downstream script.

```yaml
trigger:
- main

pool:
  vmImage: ubuntu-latest

steps:
- task: akeyless-auth@0
  name: AkeylessAuth
  inputs:
    connectedServiceName: 'mge_prod'
    access-key: "${{ variables.AKEYLESS_ACCESS_KEY }}"

- task: akeyless-get-secrets-value-task@0
  name: Fetch
  displayName: 'Fetch Akeyless Secrets'
  inputs:
    connectedServiceName: 'mge_prod'
    token: "$(AkeylessAuth.akeylessToken)"
    secretsPaths: 'api_key=/ai/agent/api-key,model_id=/ai/agent/model-id,endpoint_config=/ai/agent/config/endpoint'

- script: |
    python initialize_ai_agent.py \
      --api-key "$(Fetch.api_key)" \
      --model-id "$(Fetch.model_id)" \
      --endpoint "$(Fetch.endpoint_config)"
  displayName: 'Initialize Agent'
```

### JWT authentication and static secret retrieval

This example obtains a JWT in the pipeline, authenticates with the JWT flow, and retrieves static secrets.

```yaml
trigger:
- main

pool:
  vmImage: ubuntu-latest

steps:
- task: AzureCLI@2
  inputs:
    azureSubscription: "${{ variables.SUBSCRIPTION_ID }}"
    scriptType: 'bash'
    scriptLocation: 'inlineScript'
    inlineScript: |
      TOKEN_RESPONSE=$(az account get-access-token \
                        --resource "${{ variables.ENTRA_CLIENT_ID }}" \
                        --tenant "${{ variables.ENTRA_TENANT_ID }}" \
                        --query '{accessToken:accessToken}' -o json)

      JWT_TOKEN=$(echo "$TOKEN_RESPONSE" | jq -r '.accessToken')
      echo "##vso[task.setvariable variable=ENTRA_JWT;isSecret=true]$JWT_TOKEN"

- task: akeyless-auth@0
  name: AkeylessAuth
  inputs:
    connectedServiceName: 'mge_prod_jwt'
    jwt: "$(ENTRA_JWT)"

- task: akeyless-get-secrets-value-task@0
  inputs:
    connectedServiceName: 'mge_prod_jwt'
    token: "$(AkeylessAuth.akeylessToken)"
    secretsPaths: 'api_key=/ai/agent/api-key,model_id=/ai/agent/model-id'
```

### Dynamic secret retrieval

This example retrieves a dynamic secret value and parses the returned JSON fields for application use.

```yaml
steps:
- task: akeyless-auth@0
  name: AkeylessAuth
  inputs:
    connectedServiceName: 'mge_prod'
    access-key: "${{ variables.AKEYLESS_ACCESS_KEY }}"

- task: akeyless-get-dynamic-secret-value-task@0
  name: DbDynamicSecret
  inputs:
    connectedServiceName: 'mge_prod'
    token: "$(AkeylessAuth.akeylessToken)"
    name: '/dynamic/postgres/credentials'
    timeout: 30

- script: |
    username=$(echo "$(DbDynamicSecret.dynamicSecretValue)" | jq -r '.secret.displayName')
    password=$(echo "$(DbDynamicSecret.dynamicSecretValue)" | jq -r '.secret.secretText')
    ttl=$(echo "$(DbDynamicSecret.dynamicSecretValue)" | jq -r '.ttl_in_minutes')
    python connect_postgres.py --username "$username" --password "$password" --expiration "$ttl"
  displayName: 'Use Dynamic Secret'
```

### Rotated secret retrieval

This example retrieves a rotated secret and extracts credential values from the returned payload.

```yaml
steps:
- task: akeyless-auth@0
  name: AkeylessAuth
  inputs:
    connectedServiceName: 'mge_prod'
    access-key: "${{ variables.AKEYLESS_ACCESS_KEY }}"

- task: akeyless-get-rotated-secret-value-task@0
  name: DbRotatedSecret
  inputs:
    connectedServiceName: 'mge_prod'
    token: "$(AkeylessAuth.akeylessToken)"
    name: '/rotated/pgsql/password'

- script: |
    username=$(echo "$(DbRotatedSecret.rotatedSecretValue)" | jq -r '.value.username')
    password=$(echo "$(DbRotatedSecret.rotatedSecretValue)" | jq -r '.value.password')
    python connect_postgres.py --username "$username" --password "$password"
  displayName: 'Use Rotated Secret'
```

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

Task aliases used in this page match the task names currently defined in the extension task manifests.
