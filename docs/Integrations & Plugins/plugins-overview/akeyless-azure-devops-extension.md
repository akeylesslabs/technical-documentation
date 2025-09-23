---
title: Akeyless Azure DevOps Extension
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
This extension provides seamless integration with [Akeyless REST API,](https://docs.akeyless.io/reference) allowing your Azure DevOps pipelines to securely fetch secrets and inject them as pipeline variables at runtime.

This eliminates the need to hardcode sensitive credentials in your repositories, enhancing your security posture.

**The extension currently includes:**

* Akeyless Service Connection: A custom service connection type to configure your Akeyless Vault access details.
* Akeyless Auth Task: A pipeline task to authenticate with Akeyless.
* Akeyless Fetch Secrets Task: A pipeline task to retrieve one or more secrets from Akeyless Vault and expose them as pipeline variables.
* Akeyless Get Dynamic Secret Value Task: A pipeline task to retrieve a dynamic secret from the Akeyless Gateway and expose it as a pipeline variable.
* Akeyless Get Rotated Secret Value Task: A pipeline task to retrieve a rotated secret from the Akeyless Gateway and expose it as a pipeline variable.

Any Akeyless API operations performed by this extension will be registered as `Source: Azure-DevOps-Extension` in the [Akeyless Audit Logs](https://docs.akeyless.io/docs/audit-logs).

## Installation

To get started, you need to install the Akeyless Azure DevOps Extension from the Visual Studio Marketplace into your Azure DevOps organization.

1. Navigate to your Azure DevOps organization, e.g. [https://dev.azure.com/$YOUR\_ORG](https://dev.azure.com/$YOUR_ORG).
2. Click on the *Organization* settings icon (bottom-left corner).
3. Under *Extensions*, click on *Extensions*.
4. Click on *Browse marketplace*.
5. Search for "Akeyless".
6. Click on the extension and then click *Get it free* or *Install*.
7. Select your organization and complete the installation process.

## Create an Akeyless Service Connection

Before using the task in your pipelines, you need to configure a [Service Connection](https://learn.microsoft.com/en-us/azure/devops/pipelines/library/service-endpoints?view=azure-devops) that allows Azure DevOps to authenticate with your Akeyless Vault.

1. Navigate to your Azure DevOps project.
2. Click on *Project settings* (bottom-left corner).
3. Under *Pipelines*, click on *Service connections*.
4. Click *New service connection*.
5. Search for and select the Akeyless service connection type.
6. Click Next.
7. Configure the service connection parameters:
   1. Server URL (Base Path): Enter the base URL of your Akeyless Gateway or Akeyless SaaS API (e.g., [https://api.akeyless.io](https://api.akeyless.io), [https://my.gw/api/v2](https://my.gw/api/v2)).
   2. Access ID: Your Akeyless Access ID.
   3. Service connection name: Give your connection a descriptive name (e.g., 'my-akeyless-vault,' 'mge\_prod'). This name will be used in your pipeline YAML.
   4. Description: (Optional) Provide a brief description.
   5. Grant access permission to all pipelines: (Recommended for ease of use, or configure specific pipeline permissions later).
8. Click Save to create the service connection.

## Sample Azure Pipelines YAML

### API Key Authentication

This example demonstrates how to authenticate and fetch secrets to retrieve multiple secrets and then use them in a subsequent script, such as initializing an AI agent.

```yaml
# More info in https://aka.ms/yaml

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

- task: akeyless-get-secrets-value@0
  displayName: 'Fetch Akeyless Secrets for AI Agent'
  inputs:
    connectedServiceName: 'mge_prod'
    token: "$(AkeylessAuth.akeylessToken)"
    secretsPaths: 'api_key=/ai/agent/api-key,model_id=/ai/agent/model-id,endpoint_config=/ai/agent/config/endpoint'

- script: |
     echo "--- Initializing Agent ---"
   
     python initialize_ai_agent.py \
       --api-key "$(api_key)" \
       --model-id "$(model_id)" \
       --endpoint "$(endpoint_config)"
   
     echo "Agent initialization complete."
  displayName: 'Initialize agent with Fetched Secrets'
```

#### Key Points:

* The `secretsPaths` input accepts a comma-separated list of key/value pairs where the key is the name of the output Azure DevOps Pipeline variable and the value is secret path.
* Secrets are automatically marked as secret variables in the pipeline, meaning their values will be masked in logs.

### JWT Authentication

The Pipeline below provides an example for using the JWT authentication flow by using the JWT provided by Azure:

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
      
      if [ -z "$JWT_TOKEN" ]; then
        echo "##vso[task.logissue type=error]Failed to retrieve JWT token from Microsoft Entra ID."
        exit 1
      fi

      echo "Microsoft Entra ID JWT token retrieved successfully (masked)."
      echo "##vso[task.setvariable variable=ENTRA_JWT;isSecret=true]$JWT_TOKEN"

- task: akeyless-auth@0
  name: AkeylessAuth
  inputs:
    connectedServiceName: 'mge_prod_jwt'
    jwt: "$(ENTRA_JWT)"

- task: akeyless-get-secrets-value@0
  displayName: 'Fetch Akeyless Secrets for AI Agent'
  inputs:
    connectedServiceName: 'mge_prod'
    token: "$(AkeylessAuth.akeylessToken)"
    secretsPaths: 'api_key=/ai/agent/api-key,model_id=/ai/agent/model-id,endpoint_config=/ai/agent/config/endpoint'
    
- script: |
     echo "--- Initializing Agent ---"
   
     python initialize_ai_agent.py \
       --api-key "$(api_key)" \
       --model-id "$(model_id)" \
       --endpoint "$(endpoint_config)"
   
     echo "Agent initialization complete."
  displayName: 'Initialize agent with Fetched Secrets'
```

* The Akeyless Authentication Method is automatically parsed from the supplied Access ID in the Service Connection.

### Dynamic Secret Example

This example demonstrates how to fetch a dynamic secret, which generates credentials on-demand:

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

- task: akeyless-get-dynamic-secret-value@0
  name: dbDynamicSecret
  displayName: 'Fetch Akeyless Dynamic Secret for PostgreSQL'
  inputs:
    connectedServiceName: 'mge_prod'
    token: "$(AkeylessAuth.akeylessToken)"
    name: '/dynamic/postgres/credentials'
    target: 'postgresql'
    timeout: 30
    args: 'common_name=myapp.example.com'

- script: |
     echo "--- Connecting to PostgreSQL ---"
   
     # Parse the dynamic secret response
     username=$(echo "$(dbDynamicSecret.dynamicSecretValue)" | jq -r '.username')
     password=$(echo "$(dbDynamicSecret.dynamicSecretValue)" | jq -r '.password')
     host=$(echo "$(dbDynamicSecret.dynamicSecretValue)" | jq -r '.host')
     port=$(echo "$(dbDynamicSecret.dynamicSecretValue)" | jq -r '.port')
   
     python connect_postgres.py \
       --username "$username" \
       --password "$password" \
       --host "$host" \
       --port "$port"
   
     echo "PostgreSQL connection established with dynamic credentials."
  displayName: 'Connect to PostgreSQL with Dynamic Credentials'
```

#### Key Points:

* Dynamic secrets generate credentials on-demand and are typically time-limited.
* The `target` parameter specifies the type of dynamic secret (e.g., 'postgresql', 'mysql', 'aws')
* The `args` parameter can pass additional arguments to customize the generated credentials
* The `timeout` parameter controls how long to wait for the dynamic secret generation
* Dynamic secret values are automatically marked as secret variables in the pipeline

### Rotated Secret Example

This example demonstrates how to fetch a single rotated secret, which is automatically rotated by Akeyless:

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

- task: akeyless-get-rotated-secret-value@0
  displayName: 'Fetch Akeyless Rotated Secret for Database'
  name: dbRotatedSecret
  inputs:
    connectedServiceName: 'mge_prod'
    token: "$(AkeylessAuth.akeylessToken)"
    name: '/rotated/mysql/password'

- script: |
     echo "--- Connecting to MySQL ---"
   
     password=$(echo "$(dbRotatedSecret.rotatedSecretValue)" | jq '.password')
     python connect_mysql.py \
       --password "$(password)"
   
          echo "Database connection established."
   displayName: 'Connect to Database with Rotated Credentials'
```

## Known Limitations

* We currently only support API Key and JWT authentication methods.
