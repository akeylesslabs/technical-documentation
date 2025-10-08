---
title: Gateway on Azure Container App
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
This page describes how to run [Akeyless Gateway](https://docs.akeyless.io/docs/api-gw) on [Azure Container Apps](https://azure.microsoft.com/en-us/products/container-apps). The latest Docker image can be found at the [Akeyless Docker Hub](https://hub.docker.com/r/akeyless/gateway/tags) using the following image tag: `akeyless/gateway:latest-container-app`.

# Prerequisites

* Azure [Resource Group](https://learn.microsoft.com/en-us/azure/azure-resource-manager/management/manage-resource-groups-portal#what-is-a-resource-group)
* Azure [Container Apps environment](https://learn.microsoft.com/en-us/azure/container-apps/environment)
* Azure [Container Registry](https://azure.microsoft.com/en-us/products/container-registry)

The steps below demonstrate how to configure an Azure Container Apps environment to deploy the Gateway.

Log in to your Azure Account:

```shell
az login
```

Install the Azure Container Apps extension (if not installed):

```shell
az extension add --name containerapp --upgrade
```

Create a [Resource Group](https://learn.microsoft.com/en-us/azure/azure-resource-manager/management/manage-resource-groups-portal#what-is-a-resource-group) using the following command:

```shell
az group create --name akeyless-gw-rg --location eastus
```

Create a [Container Registry](https://azure.microsoft.com/en-us/products/container-registry) using the following command:

```shell
az acr create --resource-group akeyless-gw-rg \
--name akeylessgwacr \
--sku Standard
```

Create a [Container Apps Environment](https://learn.microsoft.com/en-us/azure/container-apps/environment) using the following command:

```shell
az containerapp env create \
  --name akeyless-gw-env \
  --resource-group akeyless-gw-rg \
  --location eastus
```

With the configuration complete, we can now proceed to install the Gateway.

# Container App Creation

If the **Azure Container Registry (ACR)** is private and requires authentication, run the following command while Docker is running on your host:

```shell
az acr login --name akeylessgwacr
```

Import the Image into ACR:

```shell
az acr import \
  --name akeylessgwacr \
  --source docker.registry-2.akeyless.io/gateway:latest-container-app \
  --image gateway:latest-container-app
```

To verify that the image was imported to the ACR, run the following command:

```shell
az acr repository list -n akeylessgwacr
```

# Installation

Create the Container App using the following command:

```shell System-Assigned Identity
az containerapp create \
  --name akeyless-gw-app \
  --resource-group akeyless-gw-rg	 \
  --environment akeyless-gw-env	 \
  --image akeylessgwacr.azurecr.io/gateway:latest-container-app \
  --registry-server akeylessgwacr.azurecr.io \
  --cpu 4.0 \
  --memory 8.0Gi \
  --ingress external \
  --target-port 8000 \
  --env-vars \
    GATEWAY_ACCESS_ID=<AccessID> \
    GATEWAY_ACCESS_TYPE='azure' \
    ALLOWED_ACCESS_PERMISSIONS='[{"access_id":"<AccessID>","name":"Administrators"}]' \
    AKEYLESS_URL='https://vault.akeyless.io' \
    CLUSTER_NAME='Akeyless-GW-Container-APP' \
    CUSTOMER_FRAGMENTS='{"customer_fragments":[{"id":"CF-ID","value":"CF-Value","name":"CF-Name","fragment_type":"CF-Type"}]}'
```
```shell User-Assigned Identity
az containerapp create \
  --name akeyless-gw-app \
  --resource-group akeyless-gw-rg	 \
  --environment akeyless-gw-env	 \
  --image akeylessgwacr.azurecr.io/gateway:latest-container-app \
  --registry-server akeylessgwacr.azurecr.io \
  --user-assigned '<user-identity-resource-id>'
  --registry-identity '<registry-identity-resource-id>'
  --cpu 4.0 \
  --memory 8.0Gi \
  --ingress external \
  --target-port 8000 \
  --env-vars \
    GATEWAY_ACCESS_ID=<AccessID> \
    GATEWAY_ACCESS_TYPE='azure' \
    ALLOWED_ACCESS_PERMISSIONS='[{"access_id":"<AccessID>","name":"Administrators"}]' \
    AKEYLESS_URL='https://vault.akeyless.io' \
    CLUSTER_NAME='Akeyless-GW-Container-APP' \
    AZURE_CLIENT_ID='<User-Identity-Client-ID>'
    CUSTOMER_FRAGMENTS='{"customer_fragments":[{"id":"CF-ID","value":"CF-Value","name":"CF-Name","fragment_type":"CF-Type"}]}'
```

Where:

* `name` - The name of the Container App.

* `resource-group` - The resource group used for this Container App.

* `environment` - Your Container App environment.

* `image` - The container image to run.

* `registry-server` - The container registry where the image is stored.

* `cpu` - Assigns 4 `vCPUs` to the container.

* `memory` - Allocates 8 `GiB RAM` to the container.

* `ingress` - Either **External** or **Internal**:

  * **External**: Accepts traffic from both the public internet and your container app's internal environment.

  * **Internal**: Allows only internal access from within your container app's environment.

* `target-port` - The app inside the container listens on port `8000` for incoming traffic.

* `gateway_access_id` - Your [Azure](https://docs.akeyless.io/docs/azure-ad) Authentication Method Access ID.

* `gateway_access_type` - The Auth Method type for the Gateway (In our case - `azure`).

* `allowed_access_permissions` - A list of allowed **Access IDs**, to delegate [permissions](https://docs.akeyless.io/docs/gateway-access-permissions) users will have on your Gateway components.
  **Required** when `admin_access_id_type` is `azure`. For example, it can be used with [API Key](https://docs.akeyless.io/docs/api-key) or [SAML](https://docs.akeyless.io/docs/saml), etc.

* `akeyless_url` - `https://vault.akeyless.io`.

* `cluster_name` - The name of the cluster.

* `customer-fragment` - Optional, Add a customer fragment in `JSON` format to the `CUSTOMER_FRAGMENTS` parameter to work with [Zero-Knowledge encryption](https://docs.akeyless.io/docs/zero-knowledge).

* `user-assigned` - Optional, The **User Assigned Managed Identity** your container app will use at runtime to access Azure resources (only relevant when using a **User-Assigned Identity**).

* `registry-identity` - Optional, The **User Assigned Managed Identity** used by the container app to authenticate to **Azure Container Registry** when pulling images (only relevant when using a **User-Assigned Identity**).

* `AZURE_CLIENT_ID` - Optional, The Client ID of your Managed Identity (only relevant when using a **User-Assigned Identity**)

* `AZURE_TENANT_ID` - Optional, the Azure Tenant ID of your Managed Identity (only relevant when using a **User-Assigned Identity**)

Upon successful deployment, A new [Container APP](https://azure.microsoft.com/en-us/products/container-apps) will be created, which will hold the Gateway application.

The Gateway is configured using environment variables. For additional available variables, refer to the [Advanced Configuration](https://docs.akeyless.io/docs/advance-gw-docker-configuration)  guide.

# Mount a Volume in Your Container App

After your Container App is created, follow these steps to add a volume:

Use the following command to export your app's configuration to a `YAML` file:

```shell
az containerapp show \
  --name akeyless-gw-app \
  --resource-group akeyless-gw-rg	 \
  --out yaml > akeyless-gw-app_deployment.yaml
```

In the `akeyless-gw-app_deployment.yaml`, add the `volumeMounts` section under the container definition:

```shell
volumeMounts:
  - volumeName: akeyless-var-log
    mountPath: /var/log/akeyless
```

In the same file, define the `akeyless-var-log` volume in the volumes section of the template:

```shell
volumes: 
  - name: akeyless-var-log
    storageType: EmptyDir
```

Save the file and update the **Container APP** with the new configuration using the following command:

```shell
az containerapp update --name akeyless-gw-app --resource-group akeyless-gw-rg --yaml akeyless-gw-app_deployment.yaml --output table
```

The Gateway URL will be available in the **Container App** resource in the **Overview** tab, and in the output of the `az containerapp create` command in the `fqdn` parameter.
