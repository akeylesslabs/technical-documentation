---
title: AKS Unified Gateway Quickstart
excerpt: ''
deprecated: false
hidden: false
metadata:
  title: ''
  description: ''
  robots: index
---
This quickstart deploys the Akeyless Unified Gateway on Azure Kubernetes Service (AKS), using Azure Workload Identity and Azure Application Gateway Ingress Controller for HTTPS ingress.

## Prerequisites

* Azure Kubernetes Service cluster with OIDC issuer and Workload Identity enabled.
* Azure Application Gateway configured and connected to the cluster by Azure Application Gateway Ingress Controller.
* Azure CLI, `kubectl`, and Helm 3 installed.
* User-assigned managed identity for the Gateway workload.
* Akeyless Authentication Method configured for Azure AD.

## Step 1: Add the Akeyless Helm Repository

```shell
helm repo add akeyless https://akeylesslabs.github.io/helm-charts
helm repo update
helm show values akeyless/akeyless-gateway > values.yaml
```

## Step 2: Configure Azure Workload Identity

Configure `values.yaml` to use the Kubernetes ServiceAccount bound to the managed identity:

```yaml values.yaml
globalConfig:
  gatewayAuth:
    gatewayAccessType: azure_ad
    gatewayAccessId: <azure-ad-auth-method-access-id>
  allowedAccessPermissions:
    - name: Administrators
      access_id: <admin-access-id>
      permissions:
        - admin
  serviceAccount:
    create: true
    serviceAccountName: akeyless-gateway-sa
    annotations:
      azure.workload.identity/client-id: <managed-identity-client-id>

gateway:
  deployment:
    labels:
      azure.workload.identity/use: "true"
```

## Step 3: Configure Ingress for Application Gateway

```yaml values.yaml
gateway:
  ingress:
    enabled: true
    annotations:
      kubernetes.io/ingress.class: "azure/application-gateway"
      appgw.ingress.kubernetes.io/backend-protocol: "http"
      appgw.ingress.kubernetes.io/request-timeout: "300"
      appgw.ingress.kubernetes.io/appgw-ssl-certificate: akeyless-gw-cert
      appgw.ingress.kubernetes.io/ssl-redirect: "true"
    rules:
      - hostname: "gateway.yourdomain.com"
        servicePort: gateway
    path: "/*"
    pathType: ImplementationSpecific
    tls: false
```

  For Application Gateway Ingress Controller, include `kubernetes.io/ingress.class: "azure/application-gateway"` in ingress annotations.

## Step 4: Install the Gateway

```shell
helm install gateway akeyless/akeyless-gateway -f values.yaml -n akeyless --create-namespace
```

## Step 5: Configure DNS and Validate

```shell
kubectl get ingress -n akeyless
curl -vk https://gateway.yourdomain.com/console
```

Expected result: ingress is provisioned through Application Gateway and the Gateway endpoint is reachable over HTTPS.

## Related Reference Pages

* [Gateway on Kubernetes](https://docs.akeyless.io/docs/gateway-chart)
* [Advanced Chart Configuration](https://docs.akeyless.io/docs/advanced-chart-configuration)
* [ESO and AKS Workload Identity](https://docs.akeyless.io/docs/eso-and-aks-workload-identity)
