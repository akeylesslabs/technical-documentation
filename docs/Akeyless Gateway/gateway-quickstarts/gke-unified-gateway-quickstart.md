---
title: GKE Unified Gateway Quickstart
excerpt: ''
deprecated: false
hidden: false
metadata:
  title: ''
  description: ''
  robots: index
---
This quickstart deploys the Akeyless Unified Gateway on Google Kubernetes Engine (GKE), using GKE Workload Identity for authentication and GKE ingress with a Google-managed certificate.

## Prerequisites

* Google Kubernetes Engine cluster with Workload Identity enabled.
* `gcloud`, `kubectl`, and Helm 3 installed.
* A Google service account (GSA) for the Gateway workload.
* Akeyless Authentication Method configured for GCP.

## Step 1: Add the Akeyless Helm Repository

```shell
helm repo add akeyless https://akeylesslabs.github.io/helm-charts
helm repo update
helm show values akeyless/akeyless-gateway > values.yaml
```

## Step 2: Bind GKE Service Account to GSA

```shell
gcloud iam service-accounts add-iam-policy-binding \
  <gsa-name>@<project-id>.iam.gserviceaccount.com \
  --member="serviceAccount:<project-id>.svc.id.goog[akeyless/akeyless-gateway-sa]" \
  --role="roles/iam.workloadIdentityUser"
```

## Step 3: Configure Gateway Authentication

```yaml values.yaml
globalConfig:
  gatewayAuth:
    gatewayAccessType: gcp
    gatewayAccessId: <gcp-auth-method-access-id>
  allowedAccessPermissions:
    - name: Administrators
      access_id: <admin-access-id>
      permissions:
        - admin

serviceAccount:
  create: true
  serviceAccountName: akeyless-gateway-sa
  annotations:
    iam.gke.io/gcp-service-account: <gsa-name>@<project-id>.iam.gserviceaccount.com
```

## Step 4: Configure Managed Certificate and Ingress

Create a managed certificate resource:

```yaml
apiVersion: networking.gke.io/v1
kind: ManagedCertificate
metadata:
  name: akeyless-gateway-cert
spec:
  domains:
    - gateway.yourdomain.com
```

Apply it:

```shell
kubectl apply -f managed-certificate.yaml
```

Configure ingress in `values.yaml`:

```yaml values.yaml
ingress:
  enabled: true
  ingressClassName: "gce"
  annotations:
    kubernetes.io/ingress.class: "gce"
    networking.gke.io/managed-certificates: "akeyless-gateway-cert"
  rules:
    - hostname: "gateway.yourdomain.com"
      servicePort: gateway
      path: "/*"
      pathType: ImplementationSpecific
  tls: false
```

## Step 5: Install the Gateway

```shell
helm install gateway akeyless/akeyless-gateway -f values.yaml -n akeyless
```

## Step 6: Configure DNS and Validate

```shell
kubectl get ingress -n akeyless
kubectl describe managedcertificate akeyless-gateway-cert
curl -vk https://gateway.yourdomain.com/console
```

Expected result: the managed certificate becomes active and the Gateway endpoint is reachable over HTTPS.

## Related Reference Pages

* [Gateway on Kubernetes](https://docs.akeyless.io/docs/gateway-chart)
* [Advanced Chart Configuration](https://docs.akeyless.io/docs/advanced-chart-configuration)
