---
title: Azure Kubernetes Service Deployment
excerpt: ''
deprecated: false
hidden: false
metadata:
  title: ''
  description: ''
  robots: index
next:
  description: ''
  pages:
    - type: basic
      slug: advanced-k8s-gateway-configuration
      title: Advanced Kubernetes Configuration
    - type: basic
      slug: configuring-tls
      title: Configuring TLS
---
<Callout icon="ℹ️" theme="info">
  ### **Gateway New Chart:**

  The Gateway new chart docs is now available [here](https://docs.akeyless.io/docs/gateway-deploy-kubernetes-helm).
</Callout>

This page includes only Azure Kubernetes Service (AKS)-specific delta steps.

Review the [Kubernetes Helm deployment page](https://docs.akeyless.io/docs/gateway-deploy-kubernetes-helm) first, then apply the AKS changes in this guide.

## Scope

This guide assumes that the baseline Helm deployment flow is complete, including:

- Helm chart setup
- base `values.yaml` preparation
- installation and upgrade flow
- Gateway admin and permission model

This page focuses on AKS workload identity and AKS-specific `values.yaml` changes.

## Prerequisites

Complete all baseline prerequisites from the main Helm deployment page, and add:

- An [Azure Active Directory authentication method](https://docs.akeyless.io/docs/auth-with-azure) in Akeyless.
- AKS cluster workload identity configured as documented in the [AKS workload identity guide](https://learn.microsoft.com/en-us/azure/aks/workload-identity-deploy-cluster).
- A user-assigned managed identity client ID for ServiceAccount annotation.

## AKS Identity Delta

Set the Gateway auth type to `azure_ad` and provide your Azure Access ID:

```yaml values.yaml
globalConfig:
  gatewayAuth:
    gatewayAccessId: <Azure Access ID>
    gatewayAccessType: azure_ad
  allowedAccessPermissions: {}
```

Enable workload identity labels and ServiceAccount annotations:

```yaml values.yaml
deployment:
  annotations: {}
  labels:
    azure.workload.identity/use: "true"

serviceAccount:
    create: false
    serviceAccountName: <AKS ServiceAccount Name>
    annotations:
      azure.workload.identity/client-id: <User Assigned Managed Identity Client ID>
```

## Validation Delta

After deployment, validate Azure workload identity integration:

1. Confirm pod health:

   ```shell
   kubectl get pods -n <namespace>
   ```

2. Confirm ServiceAccount annotations:

   ```shell
   kubectl get sa <AKS ServiceAccount Name> -n <namespace> -o yaml
   ```

3. Validate Gateway login and management endpoint connectivity.

## Related Tasks

- For shared Helm install and upgrade commands, use the main Kubernetes Helm deployment page.
- For advanced chart settings, use [Advanced Kubernetes Configuration](https://docs.akeyless.io/docs/gateway-kubernetes-helm-values-reference).
- For TLS configuration, use [Configuring TLS](https://docs.akeyless.io/docs/gateway-tls-settings).

<br />
