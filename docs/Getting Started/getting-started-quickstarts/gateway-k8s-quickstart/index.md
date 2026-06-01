---
title: Akeyless Gateway with Kubernetes Quickstart
slug: gateway-k8s-quickstart
deprecated: false
hidden: false
metadata:
  robots: index
next:
  pages:
    - slug: secret-retrieval-k8s-quickstart
      title: Getting a Secret with a Kubernetes Container Quickstart
      type: basic
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

<ApiKeyWarning />

> ✅ **Tip:** We have created a [Setup Kubernetes Quickstart](https://docs.akeyless.io/docs/kubernetes-setup-quickstart) to assist you if you're unfamiliar with setting up a Kubernetes cluster.

## Step 1: Create Namespace

1. Launch a Terminal or Command Prompt.
2. Run the following command to create a new Namespace in the Kubernetes cluster:

```shell
kubectl create namespace akeyless
```

_Sample Output:_

```text
namespace/akeyless created
```

## Step 2: Add Helm Repo

Run the following commands to add the official Akeyless Helm repository to your local Helm environment:

```shell
helm repo add akeyless https://akeylesslabs.github.io/helm-charts
helm repo update 
```

_Sample Output:_

```text
"akeyless" has been added to your repositories
Hang tight while we grab the latest from your chart repositories...
...Successfully got an update from the "akeyless" chart repository
Update Complete. ⎈Happy Helming!⎈
```

## Step 3: Fetch `values.yaml`

Run the following command to save the default configuration values of the Akeyless Gateway Helm chart to your current directory as a new file called `values.yaml`:

```shell
helm show values akeyless/akeyless-gateway --version "2.0.9" > values.yaml
```

There should be no command output.

> ℹ️ **Note:**
>
> In the unified Gateway chart, the default deployment image is `gw`.
> If a deployment must use `akeyless/base`, set an explicit image override in `values.yaml` as documented in [Gateway Kubernetes Helm Values Reference](https://docs.akeyless.io/docs/gateway-kubernetes-helm-values-reference#gateway-image-defaults-and-override).

## Step 4: Create Secret for Access Key

1. Replace `<Access-Key>` in the command below with the Access Key value of your API Key.
2. Run the command to create a new Secret object in your Kubernetes cluster:

```shell
kubectl create secret generic access-key --namespace akeyless --from-literal=gateway-access-key=<Access-Key>
```

## Step 5: Edit `values.yaml`

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

## Step 6: Deploy the Gateway

Run the following command to deploy the Akeyless Gateway Helm chart using the `values.yaml` file that you edited:

```shell
helm install gw akeyless/akeyless-gateway --namespace akeyless -f values.yaml --version "2.0.9"
```

_Sample Output:_

```text
NAME: gw
LAST DEPLOYED: Thu Nov 20 13:52:33 2025
NAMESPACE: akeyless
STATUS: deployed
REVISION: 1
DESCRIPTION: Install complete
TEST SUITE: None
```

## Step 7: Verify Pods

1. Wait for the Akeyless Gateway's pods to be ready. This may take up to ten minutes.

2. Run the following command to check that the pods are ready:

    ```shell
    kubectl get pods -n akeyless
    ```

    _Sample Output:_

    ```text
    NAME                                           READY   STATUS    RESTARTS   AGE
    gw-akeyless-gateway-cache-7bc7c7556b-rdwzx     1/1     Running   0          7m44s
    unified-gw-akeyless-gateway-695dbb7f67-bflsz   1/1     Running   0          7m44s
    unified-gw-akeyless-gateway-695dbb7f67-n6kbx   1/1     Running   0          7m44s
    ```

## Step 8: View the Gateway in the Akeyless Console

1. Open the [Akeyless Console](https://console.akeyless.io).

2. Sign in to your existing Akeyless account.

    You will be taken to the Akeyless Console homepage.

3. In the left navigation menu, select **Gateways**.

    You should see `Quickstart Gateway` available with a **Status** of `Healthy`.

> ℹ️ **Note:** We did not configure access to the Akeyless Gateway's local console in the Quickstart and attempts to access it are expected to fail.

***

_You have now deployed the Akeyless Gateway on Kubernetes using Helm and authenticated it using an API Key._
