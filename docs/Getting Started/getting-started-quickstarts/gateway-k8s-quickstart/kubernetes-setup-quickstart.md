---
title: Setup Kubernetes Quickstart
deprecated: false
hidden: false
metadata:
  robots: index
next:
  pages:
    - slug: gateway-k8s-quickstart
      title: Akeyless Gateway with Kubernetes Quickstart
      type: basic
    - title: Learn More about Docker Desktop
      type: link
      url: https://docs.docker.com/desktop/
    - title: Learn More about Kubernetes
      type: link
      url: https://kubernetes.io/docs/home/
    - title: Learn More about Helm
      type: link
      url: https://helm.sh/docs/
---
This Quickstart helps you prepare a local Kubernetes environment using **Docker Desktop** so that you can deploy the Akeyless Gateway with the [Akeyless Gateway with Kubernetes Quickstart](https://docs.akeyless.io/docs/gateway-deploy-kubernetes-helm).

By the end of this guide, you will have:

- Kubernetes enabled in Docker Desktop
- `kubectl` pointing at the Docker Desktop cluster
- Helm installed and working
- Kubernetes Metrics Server installed
- Basic resource and network checks completed

This environment is intended for **development and testing only**, not production use.

## Prerequisites

You will need:

- Docker Desktop installed ([Windows](https://docs.docker.com/desktop/setup/install/windows-install/), [macOS](https://docs.docker.com/desktop/setup/install/mac-install/), or [Linux](https://docs.docker.com/desktop/setup/install/linux/))
- Permissions to change Docker Desktop settings
- Internet access from your machine

## Step 1: Configure Docker Desktop Resources

Configure Docker Desktop with at least:

- 2 CPUs
- 4 GB RAM

Adjust these in **Settings → Resources**.

## Step 2: Enable Kubernetes in Docker Desktop

1. Open **Docker Desktop**.
2. Open Docker Desktop settings, select the **Kubernetes** options, and **Enable Kubernetes**. This guide was tested with the `Kubeadm` setting.
3. Apply the change and allow Docker Desktop to install or restart Kubernetes if prompted.
4. Wait until Docker Desktop shows that **Kubernetes** is running.

## Step 3: Verify kubectl and Context

1. Launch a Terminal or Command Prompt.

2. Docker Desktop should install the corresponding version of `kubectl` for you. It should match the version of your Kubernetes cluster. Ensure `kubectl` is installed:

   ```shell
   kubectl version --client
   ```

   _Sample Output:_

   ```text
   Client Version: v1.34.1
   Kustomize Version: v5.7.1
   ```

3. A `kubectl` context for Docker Desktop should have been created for you. Verify that your current context points to the Docker Desktop cluster:

   ```shell
   kubectl config get-contexts
   kubectl config use-context docker-desktop
   ```

   _Sample Output:_

   ```text
   CURRENT   NAME             CLUSTER          AUTHINFO         NAMESPACE
   *         docker-desktop   docker-desktop   docker-desktop   
   ```

   Check that the cluster responds:

   ```shell
   kubectl get nodes
   ```

   _Sample Output:_

   ```text
   NAME             STATUS   ROLES           AGE   VERSION
   docker-desktop   Ready    control-plane   51d   v1.34.1
   ```

## Step 4: Install and Verify Helm

1. [Install Helm following official documentation.](https://helm.sh/docs/intro/install/)

2. Verify Helm:

   ```shell
   helm version
   ```

   _Sample Output:_

   ```text
   version.BuildInfo{Version:"v4.0.0", GitCommit:"99cd1964357c793351be481d55abbe21c6b2f4ec", GitTreeState:"clean", GoVersion:"go1.25.4", KubeClientVersion:"v1.34"}
   ```

## Step 5: Verify Network Connectivity to Akeyless

1. Run the following command to create a pod with one container to check network connectivity:

   ```shell
   kubectl run curl-test --image=curlimages/curl --restart=Never --command --   curl -I https://console.akeyless.io
   ```

   _Sample Output:_

   ```text
   pod/curl-test created
   ```

2. Review the container's logs for a valid HTTP response by running the following command:

   ```shell
   kubectl logs curl-test
   ```

   _Sample Output:_

   ```text
   % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                   Dload  Upload   Total   Spent    Left  Speed
   HTTP/2 200 
   0  3321   0     0   0     0     0     0  --:--:-- --:--:-- --:--:--     0
   date: Thu, 20 Nov 2025 19:51:48 GMT
   content-type: text/html
   content-length: 3321
   server: nginx
   last-modified: Sun, 09 Nov 2025 10:08:40 GMT
   etag: "69106828-cf9"
   content-security-policy: frame-ancestors 'none'
   cache-control: no-cache, no-store, must-revalidate, private
   pragma: no-cache
   expires: 0
   strict-transport-security: max-age=31536000; includeSubDomains; preload
   x-content-type-options: nosniff
   x-frame-options: SAMEORIGIN
   accept-ranges: bytes

   ```

   > ℹ️ **Note:**
   >
   > The sample output above shows a valid HTTP response with a 200 response code and several HTTP headers. Any 200 or 300 status codes are fine. Failing outputs could be:
   >
   > - `curl: (6) Could not resolve host: console.akeyless.io`
   > - `curl: (7) Failed to connect to console.akeyless.io port 443: Connection timed out`
   > - `curl: (60) SSL certificate problem`

3. Delete the pod as it is no longer useful:

   ```shell
   kubectl delete pod curl-test
   ```

   _Sample Output_:

   ```text
   pod "curl-test" deleted from default namespace
   ```

## Step 6: Install the Kubernetes Metrics Server

Install the Kubernetes Metrics Server by applying the official manifest file:

```shell
kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml
```

_Sample Output:_

```text
/releases/latest/download/components.yaml
serviceaccount/metrics-server created
clusterrole.rbac.authorization.k8s.io/system:aggregated-metrics-reader created
clusterrole.rbac.authorization.k8s.io/system:metrics-server created
rolebinding.rbac.authorization.k8s.io/metrics-server-auth-reader created
clusterrolebinding.rbac.authorization.k8s.io/metrics-server:system:auth-delegator created
clusterrolebinding.rbac.authorization.k8s.io/system:metrics-server created
service/metrics-server created
deployment.apps/metrics-server created
apiservice.apiregistration.k8s.io/v1beta1.metrics.k8s.io create
```

## Step 7: Verify the Metrics Server

1. Check the Metrics Server deployment object:

   ```shell
   kubectl get deployment metrics-server -n kube-system
   ```

   Wait for the `metrics-server` deployment to show `1/1` ready. This should take about two minutes.

   _Sample Output:_

   ```text
   NAME             READY   UP-TO-DATE   AVAILABLE   AGE
   metrics-server   1/1     1            1           2m
   ```

   Note: `kubectl` supports a built-in watch function with the `-w` flag if you want to avoid entering the command repeatedly.

   > ⚠️ **Warning (If your Metrics Server fails to become ready):**
   >
   > 1. Check the logs for the Metrics Server pod with `kubectl logs -n kube-system $(kubectl get pods -n kube-system -l k8s-app=metrics-server -o jsonpath='{.items[0].metadata.name}')`. This command looks up the pod name and checks its logs.
   > 2. If you see an error similar to `x509: cannot validate certificate for <IP> because it does not contain any IP SANs` in the Metrics Server logs, this is not uncommon. It happens frequently in small-scale development environments. A fast fix is to edit the deployment and add `--kubelet-insecure-tls` to the Metrics Server container arguments. This is acceptable for local development clusters such as Docker Desktop, _but should not be used in production_. This can be done in one line with: `kubectl patch deployment metrics-server -n kube-system --type='json' -p='[{"op":"add","path":"/spec/template/spec/containers/0/args/-","value":"--kubelet-insecure-tls"}]'`.

2. Check some Metrics for your cluster to test functionality. Here is a command to check the Metrics for your cluster's nodes:

   ```shell
   kubectl top nodes
   ```

   _Sample Output:_

   ```text
   NAME             CPU(cores)   CPU(%)   MEMORY(bytes)   MEMORY(%)   
   docker-desktop   130m         0%       1550Mi          20%    
   ```

***

_You have now prepared a Docker Desktop Kubernetes cluster suitable for deploying the Akeyless Gateway._
