---
title: Azure Serverless
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
This guide describes how to run a Serverless Gateway on **Azure** based on [Function APP](https://learn.microsoft.com/en-us/azure/azure-functions/functions-overview?pivots=programming-language-csharp) using Azure [Bicep](https://learn.microsoft.com/en-us/azure/azure-resource-manager/bicep/overview?tabs=bicep). 

# Prerequisites

- [Azure CLI](https://learn.microsoft.com/en-us/cli/azure/install-azure-cli)

- [Azure Bicep ](https://learn.microsoft.com/en-us/azure/azure-resource-manager/bicep/overview?tabs=bicep)

- Permission to create and manage [Resource Group](https://learn.microsoft.com/en-us/azure/azure-resource-manager/management/manage-resource-groups-portal) in Azure.

- Network port `8000` on the cluster must be open** only for internal network access**, allowing access to the following services using the corresponding endpoints: 

| Service                                              | Endpoint   |
| :--------------------------------------------------- | :--------- |
| [Gateway Console](doc:gateway-configuration-manager) | `/console` |
| [HashiCorp Vault Proxy](doc:hashicorp-vault-proxy)   | `/hvp`     |
| Akeyless V1 REST API                                 | `/api/v1`  |
| Akeyless V2 REST API                                 | `/api/v2`  |
| [KMIP Server](doc:kmip-server)                       | `5696`     |

For example, to get to `/api/v2` endpoint, run: `https://<your_func_url>/api/gw/api/v2/`

> 🚧 Warning
> 
> Make sure that this server is not globally opened to the public network. Akeyless Gateway requires only connections to Akeyless SaaS Core Services.

# Gateway Configuration

Clone the **Serverless Gateway** repository locally: 

```shell Shell
gh repo clone akeyless-community/akeyless-serverless-gateway
```

Edit the `akeyless-serverless-gateway/bicep/Azure/serverless-gateway/params.bicepparam` file according to the sections below.

## Authentication

Set your Gateway with a default [Authentication Method](doc:access-and-authentication-methods) to control the level of access your Gateway will have inside your Akeyless account.

The following Authentication Methods are supported for Azure Serverless:

- [API Key](https://docs.akeyless.io/docs/api-key)
- [Azure AD](https://docs.akeyless.io/docs/azure-ad)

> 👍 Tip
> 
> When working with **Azure AD** authentication method, you can set a [Sub-Claim](https://docs.akeyless.io/docs/sub-claims) containing the **Azure Object ID** on the Access-Role associated to the authentication method.
> 
> When using the **Azure AD** authentication method, you can configure a [Sub-Claim](https://docs.akeyless.io/docs/sub-claims) on the associated [Access Role](https://docs.akeyless.io/docs/rbac) to match the user's **Azure Object ID** which can be found under **Identity** tab, in the **Function App** running the gateway.

<br />

When using [Azure AD](doc:azure-ad) as the `admin_access_id` of the Gateway, make sure to set in addition a list of users that will be able to manage your Gateway configuration using the `allowed_access_permissions` parameter, for example:

```shell Azure_AD
using 'main.bicep'

@description('Initial Display Name')
param initial_display_name = 'Akeyless Serverless'

@description('''This is the url for Akeyless service,
available inputs are https://vault.akeyless.io or  https://vault.eu.akeyless.io''')
param akeyless_url = 'https://vault.akeyless.io'

@description('Cluster Name')
param cluster_name = 'Azure Serverless'

@description('Allowed values are azure_ad or access_key https://docs.akeyless.io/docs/access-and-authentication-method')
param admin_access_id_type = 'azure'

@description('Akeyless Admin Access ID')
param admin_access_id = '<Access ID>'


@description('''Akeyless Allowed Access Permissions
                  The input should be in this json format. See the below example:
                  '[{"name": "", "access_id": "", "permissions": ["admin"]}]'
                  ''')
param allowed_access_permissions = '[{"name": "", "access_id": "", "permissions": ["admin"]}]'

@description('''Akeyless Customer key fragments (Zero Knowledge).
                For more information https://docs.akeyless.io/docs/implement-zero-knowledge
                The input should be in json format. See the below example.
                Use the exact format here inside the {braces} and add it to the `default = ` empty value below.
                {
                  "customer_fragments": [
                      {
                          "id": "<Customer Fragment ID>",
                          "value": "<Customer Fragment Value>",
                          "description": "My Serverless Fragment",
                          "name": "ServerLessFragment"
                      }
                  ]
                }''')
param customer_fragments = '{}'

@description('Then name of the function app')
param functionAppName = 'akeyless-serverless-gateway'

@description('Name of the managed environment')
param managedEnvironmentName = 'serverless-gateway'

@description('docker image')
param docker_img = ''

@description('docker tag')
param docker_tag = 'latest'
```
```shell API Key
using 'main.bicep'

@description('Initial Display Name')
param initial_display_name = 'Akeyless Serverless'

@description('''This is the url for Akeyless service,
available inputs are https://vault.akeyless.io or  https://vault.eu.akeyless.io''')
param akeyless_url = 'https://vault.akeyless.io'

@description('Cluster Name')
param cluster_name = 'Azure Serverless'

@description('Allowed values are azure or access_key https://docs.akeyless.io/docs/access-and-authentication-method')
param admin_access_id_type = 'access_key'

@description('Akeyless Admin Access ID')
param admin_access_id = '<Access ID>'

@description('Akeyless Admin Access Key - not relevant when admin_access_id_type = azure_ad')
param admin_access_key = '<Access Key>'

@description('''Akeyless Allowed Access Permissions
                  The input should be in this json format. See the below example:
                  '[{"name": "", "access_id": "", "permissions": ["admin"]}]'
                  ''')
param allowed_access_permissions = '[{"name": "", "access_id": "", "permissions": ["admin"]}]'

@description('''Akeyless Customer key fragments (Zero Knowledge).
                For more information https://docs.akeyless.io/docs/implement-zero-knowledge
                The input should be in json format. See the below example.
                Use the exact format here inside the {braces} and add it to the `default = ` empty value below.
                {
                  "customer_fragments": [
                      {
                          "id": "cf-xyzxyzxyzxyzxyzxyz",
                          "value": "SomE/CUstOmer/FrAGMenTvALue==",
                          "description": "MyFirstCF"
                      }
                  ]
                }''')
param customer_fragments = '{}'

@description('Then name of the function app')
param functionAppName = 'akeyless-serverless-gateway'

@description('Name of the managed environment')
param managedEnvironmentName = 'serverless-gateway'

@description('docker image')
param docker_img = ''

@description('docker tag')
param docker_tag = 'latest'
```

Where:

- `admin_access_id_type`: The Auth Method type for the Gateway either  `access_key` or  `azure`.

- `admin_access_id`: The **Access ID** of the Gateway default Auth Method.

- `admin_access_key`: The **Access Key** of the `admin_access_id`. **Relevant only ** when `admin_access_id_type` is `access_key`.

- `allowed_access_permissions`:  A list of allowed **Access IDs**, to delegate [permissions](doc:gateway-access-permissions) users will have on your Gateway components. **Required** when `admin_access_id_type` is `azure_ad`. For example, it can be used with [API Key](https://docs.akeyless.io/docs/api-key) or [SAML](doc:saml), etc.

- `functionAppName`: The name for the [Function APP](https://learn.microsoft.com/en-us/azure/azure-functions/functions-overview?pivots=programming-language-csharp) that will be created in Azure.

## Customer Fragment

To work with [Zero-Knowledge ](https://docs.akeyless.io/docs/implement-zero-knowledge) edit the `customer_fragments`  param as follows:

```shell
"customer_fragments": [{"id": "<Customer Fragment ID>","value": "<Customer Fragment Value>","description": "My Serverless Fragment","name": "ServerLessFragment"}]
```

## Storage Account

To associate an existing [Storage Account](https://learn.microsoft.com/en-us/azure/storage/common/storage-account-overview), add the following section to the `main.bicep` file:

```shell main.bicep
param storageAccountName string = '<Storage Account Name>' 

resource stg 'Microsoft.Storage/storageAccounts@2023-04-01' = {
  name: <'storageAccountName'> 
  location: location 
  sku: {
    name: '<Storage SKU>' 
  }
  kind: '<Account kind>' 
  properties: {
    supportsHttpsTrafficOnly: true
  }
}
```

Where:

- `name`: The name of the storage account.

- `location`: The location where the storage account is deployed.

- `sku`: [Stock Keeping Unit](https://learn.microsoft.com/en-us/azure/azure-resource-manager/bicep/file#parameters) - A unique identifier used to specify a particular version or configuration of the storage account. 

- `kind`: Type of storage account.

- `properties`: Settings for the storage account.

- `supportsHttpsTrafficOnly`: Only allows HTTPS traffic.

For more information on the above configuration, refer to the [official Azure documentation](https://learn.microsoft.com/en-us/azure/storage/common/storage-account-overview#recommended-workload-configurations).

# Installation

To install the module, run the following commands from the cloned directory

Create a [Resource Group](https://learn.microsoft.com/en-us/azure/azure-resource-manager/management/manage-resource-groups-portal):

```shell Shell
az group create -l <location> -n <resource_group>
```

Deploy the Gateway using the **Resource Group** that was created:

```shell
az deployment group create -g <resource_group> -f main.bicep -p params.bicepparam --query "properties.outputs.functionAppURL.value"
```

Alternatively, the `/akeyless-serverless-gateway/bicep/Azure/serverless-gateway/Mainfile` file can be configured to create the resource group and to install the serverless Gateway by setting the following: 

```shell
RESOURCE_GROUP = akeless-serverless-gateway
LOCATION = <location>
BICEP_MAIN = main.bicep
BICEP_PARAMS = params.bicepparam
```

Upon successfully installing the **Serverless Gateway**, the Gateway console URL will be printed.

> 📘 Gateway URL
> 
> The default value of the Gateway URL ends with `/console` which will route you to **Akeyless Gateway Console** (Port `18888`).
> 
> To connect to **Akeyless Gateway Configuration Manager** (Port `8000`) use: `/config` instead

# Initial Gateway Configuration

To configure your Akeyless Gateway:

1. On your browser, navigate to the URL in the first output above.
2. Enter your credentials to log in.

# Limitations

**Unavailable services:**

[Kubernetes](https://docs.akeyless.io/docs/kubernetes-auth) / [LDAP](https://docs.akeyless.io/docs/ldap) Authentication, [Caching](https://docs.akeyless.io/docs/configure-the-gateway-cache), [Automatic Migration](https://docs.akeyless.io/docs/automatic-migration), Event on Gateway status change, [TLS Configuration](https://docs.akeyless.io/docs/tls-certificate).