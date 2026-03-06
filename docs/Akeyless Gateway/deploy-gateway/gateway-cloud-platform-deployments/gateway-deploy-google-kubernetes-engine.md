---
title: Google Kubernetes Engine Deployment
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
> ℹ️ **Note (Gateway New Chart):**
>
> The Gateway new chart docs is now available [here](https://docs.akeyless.io/docs/gateway-chart).

This page includes only Google Kubernetes Engine (GKE)-specific delta steps.

Review the [Kubernetes Helm deployment page](https://docs.akeyless.io/docs/gateway-chart) first, then apply the GKE changes in this guide.

## Scope

This guide assumes that the baseline Helm deployment flow is complete, including:

* Helm chart setup
* base `values.yaml` preparation
* installation and upgrade flow
* Gateway admin and permission model

This page focuses on GKE workload identity and GKE-specific `values.yaml` changes.

## Prerequisites

Complete all baseline prerequisites from the main Helm deployment page, and add:

* A [GCP authentication method](https://docs.akeyless.io/docs/auth-with-gcp) in Akeyless.
* GKE workload identity setup as documented in the [GKE workload identity guide](https://cloud.google.com/kubernetes-engine/docs/how-to/workload-identity#authenticating_to).
* A Kubernetes ServiceAccount mapped to the target Google service account.

## GKE Identity Delta

Set the Gateway auth type to `gcp` and provide your GCP Access ID:

```yaml values.yaml
globalConfig:
  gatewayAuth:
    gatewayAccessId: <GCP Access ID>
    gatewayAccessType: gcp
  allowedAccessPermissions: {}
```

Set ServiceAccount annotations for workload identity:

```yaml values.yaml
serviceAccount:
  create: false
  serviceAccountName: <GKE ServiceAccount Name>
  annotations:
    iam.gke.io/gcp-service-account: <GCP Service Account>

nodeSelector:
  iam.gke.io/gke-metadata-server-enabled: "true"
```

> ℹ️ **Info:**
>
> For Autopilot clusters, omit `nodeSelector`. Autopilot rejects this selector because all nodes already use workload identity.

## Validation Delta

After deployment, validate GKE workload identity integration:

1. Confirm pod health:

    ```shell
    kubectl get pods -n <namespace>
    ```

2. Confirm ServiceAccount annotations:

    ```shell
    kubectl get sa <GKE ServiceAccount Name> -n <namespace> -o yaml
    ```

3. Validate Gateway login and management endpoint connectivity.

## Related Tasks

* For shared Helm install and upgrade commands, use the main Kubernetes Helm deployment page.
* For advanced chart settings, use [Advanced Kubernetes Configuration](https://docs.akeyless.io/docs/advanced-k8s-gateway-configuration).
* For TLS configuration, use [Configuring TLS](https://docs.akeyless.io/docs/configuring-tls).
