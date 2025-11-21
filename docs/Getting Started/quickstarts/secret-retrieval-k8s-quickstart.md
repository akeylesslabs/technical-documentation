---
title: Getting a Secret within a Kubernetes Cluster Quickstart
excerpt: Under construction. Steps 1 through 7 verified.
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

## Step 1: Create a Namespace and Label

Run these commands to create a namespace and label for our pods:

```shell
kubectl create namespace akeyless
kubectl label namespace akeyless name=akeyless
```

The `kubectl label` commands adds a key-value label to the namespace`akeyless` of `name=akeyless`.

_Sample Output:_

```
namespace/akeyless created
namespace/akeyless labeled
```

## Step 2: Install the Injector

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

_Sample File Section_:

```yaml
env:
  AKEYLESS_URL: "https://vault.akeyless.io"
  AKEYLESS_ACCESS_ID: "p-h8kyauyqvow2am" 
  AKEYLESS_ACCESS_TYPE: "api_key"  # azure_ad/aws_iam/api_key/k8s
  
 # AKEYLESS_API_GW_URL: "https://api-gw-url"
 # AKEYLESS_POD_ACCESS_PATH: "<location-to-access-secrets-per-pod-name>"
 # AKEYLESS_NAMESPACE_ACCESS_PATH: "<location-to-access-secrets-per-namespace>"
 # AKEYLESS_SECRET_DIR_NAME: "<path>"
  AKEYLESS_API_KEY: "GCz5fLEgc0tJftA/7W1WnywbgorEc30V92xQ3dOGNME="
 # AKEYLESS_CRASH_POD_ON_ERROR: "enable"
 # AKEYLESS_K8S_AUTH_CONF_NAME: "K8s_conf_name"
 
 # the gw base64 certificate file e.g: 'cat my-gw.crt | base64'
 # AKEYLESS_GW_CERTIFICATE: 


  AKEYLESS_AGENT_LIMITS_CPU: "500m"
  AKEYLESS_AGENT_REQUESTS_CPU: "250m"
  AKEYLESS_AGENT_LIMITS_MEM: "128Mi"
  AKEYLESS_AGENT_REQUESTS_MEM: "64Mi"
```

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

## Step 3: Verify Pods for the Secret Injector

1. Wait for the Akeyless Kubernetes Secret Injector pods to be ready. This will likely take about one minute.
2. Run the following command to check that the pods are ready:

```shell
kubectl get pods -n akeyless
```

_Sample Output:_

```
NAME                                                          READY   STATUS    RESTARTS   AGE
gw-akeyless-gateway-cache-7bc7c7556b-rdwzx                    1/1     Running   0          155m
secret-injector-akeyless-secrets-injection-8464b9f585-p9r5x   1/1     Running   0          111s
secret-injector-akeyless-secrets-injection-8464b9f585-x882c   1/1     Running   0          111s
unified-gw-akeyless-gateway-695dbb7f67-bflsz                  1/1     Running   0          155m
unified-gw-akeyless-gateway-695dbb7f67-n6kbx                  1/1     Running   0          155m
```

Note that the Akeyless Gateway pods are also included in the sample output.

## Step 4: Verify the Secret

If you have not yet, create a Static Secret named `/QuickSecret` and ensure your API Key's associated Role has access to retrieve its value.

## Step 5: Create a Kubernetes Deployment

1. Create a new manifest file called `akeyless-secret-quickstart.yaml` that define our Deployment:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: akeyless-secret-quickstart
  namespace: akeyless
spec:
  replicas: 1
  selector:
    matchLabels:
      app: akeyless-secret-quickstart
  template:
    metadata:
      labels:
        app: akeyless-secret-quickstart
      annotations:
        akeyless/enabled: "true"
        akeyless/inject_file: "/QuickSecret"
    spec:
      containers:
        - name: quickstart
          image: alpine:3.19
          command:
            - "sh"
            - "-c"
            - "echo $MY_SECRET && echo going to sleep... && sleep 10000"
          env:
            - name: MY_SECRET
              value: akeyless:/QuickSecret
```

2. Apply the manifest file and create the Deployment:

```shell
kubectl apply -f akeyless-secret-quickstart.yaml
```

_Sample Output:_

```
deployment.apps/akeyless-secret-quickstart created
```

## Step 6: Verify the Pod Started

Wait about one minute to verify the Quickstart pod is created:

```shell
kubectl get pods -n akeyless
```

## Step 7: Read the Secret from the Container

```shell
kubectl logs -n akeyless deploy/akeyless-secret-quickstart
```

## Step 8: Clean Up

```bash
kubectl delete -f akeyless-secret-quickstart.yaml
kubectl delete namespace akeyless
```

***

_You have successfully:_

1. _Installed the Akeyless Kubernetes Secrets Injector_
2. _Enabled secret injection with the Akeyless Kubernetes Secrets Injector_
3. _Created a demo deployment using annotation-based secret retrieval_
4. _Retrieved an Akeyless secret directly inside a container_
