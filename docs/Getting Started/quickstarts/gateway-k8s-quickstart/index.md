---
title: Akeyless Gateway with Kubernetes Quickstart
excerpt: Harrison to test this out.
deprecated: false
hidden: false
metadata:
  robots: index
---
This Quickstart guides you through deploying the Akeyless Gateway on a Kubernetes cluster using the official Helm chart and configuring it to authenticate to your Akeyless account with an API Key.

By the end, you will have:

* A running Gateway deployment on Kubernetes
* The Gateway connected to your Akeyless account using API Key authentication

## Prerequisites

You will need:

* An active Akeyless account
* A Kubernetes cluster (v1.21 or later)
* `kubectl` installed and configured
* Helm installed
* Network connectivity from the Kubernetes cluster to Akeyless
* Kubernetes Metrics Server installed and working
* 1 vCPU and 2 GB RAM free in the cluster
* An Akeyless API Key (Access ID + Access Key) with an appropriate Role associated

## Step 1: Create Namespace

Run the following command to create a new namespace in the Kubernetes cluster:

```shell
kubectl create namespace akeyless
```

_Sample Output:_

```
namespace/akeyless created
```

## Step 2: Add Helm Repo

Run the following commands to add the official Akeyless Helm repository to your local Helm environment:

```shell
helm repo add akeyless https://akeylesslabs.github.io/helm-charts
helm repo update 
```

_Sample Output:_

```
"akeyless" has been added to your repositories
Hang tight while we grab the latest from your chart repositories...
...Successfully got an update from the "akeyless" chart repository
Update Complete. ⎈Happy Helming!⎈
```

## Step 3: Fetch values.yaml

Run the following command to save 

```shell
helm show values akeyless/akeyless-gateway > values.yaml
```

_Sample Output:_

```
level=WARN msg="unable to find exact version; falling back to closest available version" chart=akeyless-gateway requested="" selected=1.13.1
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

***

_You have now deployed the Akeyless Gateway on Kubernetes using Helm and authenticated it using an API Key._
