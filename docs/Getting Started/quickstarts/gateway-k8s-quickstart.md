---
title: Akeyless Gateway with Kubernetes Quickstart
deprecated: false
hidden: false
metadata:
  robots: index
---
This Quickstart guides you through deploying the Akeyless Gateway on a Kubernetes cluster using the official Helm chart and configuring it to authenticate to your Akeyless account with an API Key.

By the end, you will have:

- A running Gateway deployment on Kubernetes  
- The Gateway connected to your Akeyless account using API Key authentication 

## Prerequisites

You will need:

- An active Akeyless account
- A Kubernetes cluster (v1.21 or later)
- `kubectl` configured
- Helm installed
- Network connectivity from cluster to Akeyless SaaS
- Kubernetes Metrics Server (required by the chart)
- 1 vCPU and 2 GB RAM free in the cluster
- An Akeyless API Key Authentication Method (Access ID + Access Key)

## Step 1: Create Namespace

```bash
kubectl create namespace akeyless
```

## Step 2: Add Helm Repo

```bash
helm repo add akeyless https://akeylesslabs.github.io/helm-charts
helm repo update
```

## Step 3: Fetch values.yaml

```bash
helm show values akeyless/akeyless-gateway > values.yaml
```

## Step 4: Create Secret for Access Key

```bash
kubectl create secret generic access-key   --namespace akeyless   --from-literal=gateway-access-key=<Access-Key>
```

## Step 5: Edit values.yaml

```yaml
globalConfig:
  gatewayAuth:
    gatewayAccessId: <Access ID>
    gatewayAccessType: access_key
    gatewayCredentialsExistingSecret: access-key

  clusterName: quickstart-gateway
  initialClusterDisplayName: Quickstart Gateway
```

## Step 6: (Optional) Configure Admin Access

```yaml
allowedAccessPermissions:
  - name: Administrators
    access_id: <Admin Access ID>
    permissions:
      - admin
```

## Step 7: Install the Gateway

```bash
helm install gw akeyless/akeyless-gateway   --namespace akeyless   -f values.yaml
```

## Step 8: Verify Pods

```bash
kubectl get pods -n akeyless
```

## Step 9: (Optional) Access Gateway Console

```bash
kubectl get svc -n akeyless
```

Gateway Console:

```
http://<gateway-ip>:8000/console
```

## Summary

You deployed the Akeyless Gateway on Kubernetes using Helm and authenticated it using an API Key.
