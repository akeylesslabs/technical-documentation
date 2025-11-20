---
title: Akeyless Gateway with Kubernetes Quickstart
excerpt: >-
  Harrison to test this out. Next step to stress test is Step 7. Go back to look
  at step 5a.
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

1. Launch a Terminal or Command Prompt.
2. Run the following command to create a new namespace in the Kubernetes cluster:

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

## Step 3: Fetch `values.yaml`

Run the following command to save the default configuration values of the Akeyless Helm chart to your current directory as a new file called `values.yaml`:

```shell
helm show values akeyless/akeyless-gateway > values.yaml
```

_Sample Output:_

```
level=WARN msg="unable to find exact version; falling back to closest available version" chart=akeyless-gateway requested="" selected=1.13.1
```

## Step 4: Create Secret for Access Key

1. Replace `<Access-Key>` in the command below with the Access Key value of your API Key.
2. Run the command to create a new Secret object in your Kubernetes cluster:

```shell
kubectl create secret generic access-key   --namespace akeyless   --from-literal=gateway-access-key=<Access-Key>
```

## Step 5: Edit values.yaml

1. Using your text editor of choice, edit the `values.yaml` file you created earlier. Below we show the path to and the values that need to be added (`gatewayAccessId`, `gatewayAccessType`, `gatewayCredentialsExistingSecret`, `clusterName`, and `initialClusterDisplayName`).

```yaml
globalConfig:
  gatewayAuth:
    gatewayAccessId: <Access ID of your API Key>
    gatewayAccessType: access_key
    gatewayCredentialsExistingSecret: access-key

  clusterName: quickstart-gateway
  initialClusterDisplayName: Quickstart Gateway
```

2. Save the file.

<Callout icon="📘" theme="info">
  A Helm warning of `level=WARN msg="unable to find exact version; falling back to closest available version" chart=akeyless-gateway requested="" selected=1.13.1` is acceptable when running any Helm commands in a development environment. When a chart version is not specified, Helm defaults to the latest version, but shows this expected warning.
</Callout>

### Step 5a: (Optional) Configure Admin Access

<Callout icon="🚧">
  I'm debating removing this step.
</Callout>

If you want local access to the Gateway's Console, you'll need to also edit the values below. This is not required and users do not need open this interface for normal operations.

```yaml
allowedAccessPermissions:
  - name: Administrators
    access_id: <Admin Access ID>
    permissions:
      - admin
```

## Step 6: Install the Gateway

Run the following command to deploy the Akeyless Gateway Helm chart using the `values.yaml` file that you edited:

```shell
helm install gw akeyless/akeyless-gateway   --namespace akeyless   -f values.yaml
```

_Sample Output:_

```
level=WARN msg="unable to find exact version; falling back to closest available version" chart=akeyless-gateway requested="" selected=1.13.1
NAME: gw
LAST DEPLOYED: Thu Nov 20 13:52:33 2025
NAMESPACE: akeyless
STATUS: deployed
REVISION: 1
DESCRIPTION: Install complete
TEST SUITE: None
```

## Step 7: Verify Pods

```shell
kubectl get pods -n akeyless
```

## Step 8: (Optional) Access Gateway Console

```shell
kubectl get svc -n akeyless
```

Gateway Console:

```
http://<gateway-ip>:8000/console
```

***

_You have now deployed the Akeyless Gateway on Kubernetes using Helm and authenticated it using an API Key._