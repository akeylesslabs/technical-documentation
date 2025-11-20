---
title: Getting a Secret within a Kubernetes Cluster Quickstart
excerpt: Under construction.
deprecated: false
hidden: false
metadata:
  robots: index
---
This Quickstart shows how to inject a secret from Akeyless into a Kubernetes container using the **Akeyless Kubernetes Secrets Injector**. Your application will read the secret from a file inside the container’s filesystem; the injector handles authentication and secret retrieval.

## Prerequisites

You will need:

* A running Kubernetes cluster (v1.21 or later recommended)
* `kubectl` configured
* An Akeyless Gateway reachable from the cluster
* An Akeyless API Key (Access ID + Access Key) with an appropriate Role associated
* A Static Secret in Akeyless

## Step 1: Install the Injector

Before injecting secrets into containers, you must install and configure the **Akeyless Kubernetes Secrets Injector**. This component authenticates workloads to Akeyless and writes secrets into the container filesystem.

1. Run the following commands to update the Helm repositories in your local Helm environment:

```shell
helm repo update
```

You previously should have already added the official Akeyless Helm chart repository in order to install the Akeyless Gateway.

_Sample Output:_

```
Hang tight while we grab the latest from your chart repositories...
...Successfully got an update from the "akeyless" chart repository
Update Complete. ⎈Happy Helming!⎈
```

2. Run the following command to save the default configuration values of the Akeyless Kubernetes Secrets Injector Helm chart to your current directory as a new file called `values.yaml`:

```shell
helm show values akeyless/akeyless-secrets-injection --version 1.17.5 > values.yaml
```

There should be no command output.

3. Using your text editor of choice, edit the `values.yaml` file.
   1. Under the `env` key:
      1. Set `AKEYLESS_ACCESS_ID` to the Access ID of your API Key.
      2. Set `AKEYLESS_ACCESS_TYPE` to `api_key`.
      3. Uncomment `AKEYLESS_API_KEY` (by removing the `#`) and replace `<api-key` with the value to the Access Key of your API Key.

In all of these instances, you should leave the quotation marks in place (`"`).

3. Save the file.
4. Run the following command to install the Akeyless Kubernetes Secrets Injector Helm chart using the `values.yaml` file that you edited:

```shell
helm install secret-injector akeyless/akeyless-secrets-injection --version 1.17.5 --namespace akeyless -f values.yaml
```

_Sample Output:_

```
NAME: secret-injector
LAST DEPLOYED: Thu Nov 20 13:52:33 2025
NAMESPACE: akeyless
STATUS: deployed
REVISION: 1
DESCRIPTION: Install complete
TEST SUITE: None
```

## Step 7: Verify Pods

1. Wait for the Akeyless Gateway's pods to start. This may take up to ten minutes.
2. Run the following command to check that the pods are ready:

```shell
kubectl get pods -n akeyless
```

_Sample Output:_

```
NAME                                           READY   STATUS    RESTARTS   AGE
gw-akeyless-gateway-cache-7bc7c7556b-rdwzx     1/1     Running   0          7m44s
unified-gw-akeyless-gateway-695dbb7f67-bflsz   1/1     Running   0          7m44s
unified-gw-akeyless-gateway-695dbb7f67-n6kbx   1/1     Running   0          7m44s
```

##

### Step A1: Create a Kubernetes Auth Method in Akeyless

1. Open the Akeyless Console:  
   <Anchor label="[[https://console.akeyless.io](https://console.akeyless.io)](https://console.akeyless.io)" target="_blank" href="https://console.akeyless.io"><Anchor label="[https://console.akeyless.io](https://console.akeyless.io)" target="_blank" href="https://console.akeyless.io">[https://console.akeyless.io](https://console.akeyless.io)</Anchor></Anchor>
2. Sign in to your existing Akeyless account.

You will be taken to the Akeyless Console homepage.

3. In the left navigation menu, select **Users & Auth Methods**.
4. Select **+ New** and choose **Kubernetes**.
5. Select **Next →**.
6. Give it the name `K8s-Injector-Auth` and select **Next →** again.
7. <br />

Retrieve the cluster CA for the Auth Method:

```bash
kubectl config view --raw -o jsonpath='{.clusters[0].cluster.certificate-authority-data}'   | base64 --decode > k8s-ca.crt
```

Upload `k8s-ca.crt` when creating the Kubernetes Auth Method.

Record the **Access ID** for later use.

### Step A2: Create a Role That Grants Access to Your Secret

1. In the Akeyless Console, navigate to **Access Management → Roles**.
2. Create a new Role named **K8sInjectorRole**.
3. Add permissions for the secret path you want to allow, for example:

```
Path: /QuickStart/QuickSecret
Actions: read, list
```

4. Assign the Role to the Kubernetes Auth Method created in Step A1.

This gives the Injector permission to retrieve secrets on behalf of your pods.

### Step A3: Install the Akeyless Kubernetes Secrets Injector via Helm

Add the Akeyless Helm repository:

```bash
helm repo add akeyless https://akeylesslabs.github.io/helm-charts
helm repo update
```

Fetch default values:

```bash
helm show values akeyless/k8s-secrets-injection > injector-values.yaml
```

Edit `injector-values.yaml`:

```yaml
authMethodAccessId: "<YOUR-K8S-AUTH-METHOD-ACCESS-ID>"
gatewayAddress: "<YOUR-GATEWAY-URL>"

namespaceSelector:
  matchLabels:
    name: akeyless
```

Install the injector:

```bash
helm install akeyless-injector akeyless/k8s-secrets-injection   --namespace akeyless   --create-namespace   -f injector-values.yaml
```

### Step A4: Confirm the Injector Is Running

```bash
kubectl get pods -n akeyless
```

Expected output:

```text
akeyless-injector-7cd9d4b78f-zxs2p   1/1   Running   0   ...
```

If not running:

```bash
kubectl logs -n akeyless deploy/akeyless-injector
```

### Step A5: Label Namespaces That Should Receive Secrets

Label your target namespace so the injector processes its pods:

```bash
kubectl label namespace akeyless-demo name=akeyless
```

## Part B: Retrieve a Secret within a Container

### Step B1: Create a Namespace for the Demo

```bash
kubectl create namespace akeyless-demo
kubectl label namespace akeyless-demo name=akeyless
```

### Step B2: Verify the Secret Exists in Akeyless

Ensure a static secret exists at `/QuickStart/QuickSecret`.

### Step B3: Create a Demo Deployment

Create `akeyless-secret-demo.yaml`:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: akeyless-secret-demo
  namespace: akeyless-demo
spec:
  replicas: 1
  selector:
    matchLabels:
      app: akeyless-secret-demo
  template:
    metadata:
      labels:
        app: akeyless-secret-demo
      annotations:
        akeyless/enabled: "true"
        akeyless/inject_file: "/QuickStart/QuickSecret"
    spec:
      containers:
      - name: demo
        image: alpine:3.19
        command:
          - "sh"
          - "-c"
          - |
            echo "Reading secret from file..."
            cat /akeyless/secrets/QuickStart/QuickSecret || echo "Secret file not found"
            sleep 3600
```

Apply it:

```bash
kubectl apply -f akeyless-secret-demo.yaml
```

### Step B4: Verify the Pod Started

```bash
kubectl get pods -n akeyless-demo
```

If issues arise:

```bash
kubectl describe pod -n akeyless-demo <pod-name>
kubectl logs -n akeyless-demo <pod-name> -c akeyless-init
```

### Step B5: Read the Secret from the Container

```bash
kubectl logs -n akeyless-demo deploy/akeyless-secret-demo
```

Or exec:

```bash
POD_NAME=$(kubectl get pods -n akeyless-demo -l app=akeyless-secret-demo -o jsonpath='{.items[0].metadata.name}')
kubectl exec -it -n akeyless-demo "$POD_NAME" -- sh
cat /akeyless/secrets/QuickStart/QuickSecret
```

### Step B6: Clean Up

```bash
kubectl delete -f akeyless-secret-demo.yaml
kubectl delete namespace akeyless-demo
```

***

_You have successfully:_

1. _Installed the Akeyless Kubernetes Secrets Injector_
2. _Enabled secret injection with the Akeyless Kubernetes Secrets Injector_
3. _Created a demo deployment using annotation-based secret retrieval_
4. _Retrieved an Akeyless secret directly inside a container_
