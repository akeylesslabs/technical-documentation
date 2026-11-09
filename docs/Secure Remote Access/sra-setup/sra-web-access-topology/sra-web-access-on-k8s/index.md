---
title: Zero Trust Web Access on K8s
excerpt: ''
deprecated: false
hidden: false
metadata:
  title: ''
  description: ''
  robots: index
next:
  description: ''
slug: sra-web-access-on-k8s
---
Akeyless Zero Trust Web Access (ZTWA) gives users secure access to internal web applications through an isolated Chromium browser, with optional session recording. Users never see the target's credentials.

This chart deploys ZTWA on Kubernetes with Helm. For how the components fit together, see [Zero Trust Web Access](https://docs.akeyless.io/docs/sra-web-access-topology).

<Callout icon="far fa-circle-info" theme="info">
  ### Using an earlier version

  This page describes ZTWA Helm chart 4.0.0 (app version 3.0.0). For earlier versions, see [Zero Trust Web Access on K8s (earlier versions)](https://docs.akeyless.io/docs/zero-trust-web-access-on-k8s-legacy-1).
</Callout>

## Before you begin

### Requirements

* Helm installed.
* Kubernetes installed.
* Cluster resources (chart defaults):

| Component         | Kind                              | CPU request | Memory request / limit |
| ----------------- | --------------------------------- | ----------- | ---------------------- |
| Dispatcher        | Deployment                        | 1 vCPU      | 1 GiB / 2 GiB          |
| Web worker (each) | Deployment, 5 replicas by default | 1 vCPU      | 1 GiB / 2 GiB          |
| Web proxy         | Deployment                        | 0.5 vCPU    | 512 MiB / 1 GiB        |
| Media server      | DaemonSet, one per node           | 0.1 vCPU    | 128 MiB / 1 GiB        |

> ⚠️ **Warning:**
>
> To enable Secure Remote Access features, request access to the Akeyless private repository from your account manager.

### Network

* **UDP `8189` on every node** must be reachable from users' browsers. The live view of each session uses it.
* If users can't reach the nodes' IPs, set a reachable address, for example a public IP, in `mediamtx.additionalHosts`.

### Network timeout settings

When an embedded browser session runs behind a load balancer (for example, ELB), idle timeout settings can close active sessions. Set the load balancer idle timeout to a high value or unlimited.

For AWS ELB guidance, see [Configure idle connection timeout](https://docs.aws.amazon.com/elasticloadbalancing/latest/classic/config-idle-timeout.html?icmpid=docs_elb_console).

### Shared storage

File downloads and session recording need a shared volume, mounted at `/etc/shared` on the dispatcher, the web workers and the media server. The chart fails to install if recording is enabled without it.

* **Single-node clusters** (k3s, Minikube, kind) can use a node-scoped provisioner such as `local-path`.
* **Clusters with more than one node** need a `ReadWriteMany` storage class, for example AWS EFS, Azure Files, GCP Filestore or NFS.

```yaml values.yaml
persistence:
  shareStorageVolume:
    name: share-storage
    storageClassName: "efs-sc"
    accessModes:
      - ReadWriteMany
    size: 2Gi
```

Limit the mount permissions to `0650`, and make the root directory owned by group `10000`. On Amazon EFS, use an access point with that ownership. See [Use Amazon EFS with Amazon EKS](https://docs.aws.amazon.com/eks/latest/userguide/efs-csi.html).

## Configure values.yaml

Add the Akeyless Helm repository and get the default values file:

```shell
helm repo add akeyless https://akeylesslabs.github.io/helm-charts
helm repo update
helm show values akeyless/akeyless-zero-trust-web-access > values.yaml
```

Then set the values below. At minimum, set [ZTWA authentication](https://docs.akeyless.io/docs/sra-web-access-on-k8s#ztwa-authentication), since ZTWA accepts no users without it.

### Private registry credentials

Create a pull secret for the Akeyless private registry:

```shell
kubectl create secret docker-registry <SECRET_NAME> \
  --docker-server=<AKEYLESS_REGISTRY_SERVER> \
  --docker-username=<AKEYLESS_REGISTRY_USERNAME> \
  --docker-password=<AKEYLESS_REGISTRY_PASSWORD> \
  --namespace <NAMESPACE>
```

Reference it once in `values.yaml`. It applies to every pod:

```yaml values.yaml
image:
  imagePullSecrets:
    - name: <SECRET_NAME>
```

### Akeyless API URL

Keep the default for the Akeyless SaaS, or set the API URL of your Akeyless Gateway:

```yaml values.yaml
config:
  gatewayURL: https://api.akeyless.io
```

If your Gateway's certificate isn't signed by a public CA, create a Secret with the CA certificate under the key `tls.crt` and set:

```yaml values.yaml
config:
  gatewayCert:
    tlsExistingSecret: <SECRET_NAME>
```

### ZTWA authentication

ZTWA reads the secrets of the web targets with its own auth method, the **ZTWA Access ID**. It needs **Read** and **List** permissions on those secrets. Users only need **List**.

`authorizedAccessIDs` lists the auth methods allowed to open sessions, for example your SAML auth method.

> ⚠️ **Warning:**
>
> `authorizedAccessIDs` is required. If it's empty, the dispatcher and the web proxy accept no users.

Supported auth method types: [API Key](https://docs.akeyless.io/docs/auth-with-api-key), [AWS IAM](https://docs.akeyless.io/docs/auth-with-aws), [Azure AD](https://docs.akeyless.io/docs/auth-with-azure) and [GCP](https://docs.akeyless.io/docs/auth-with-gcp).

#### API key

Create a Secret with the access key under the key `ztwa-access-key`:

```shell
kubectl create secret generic ztwa-access \
  --from-literal=ztwa-access-key=<ACCESS_KEY> \
  --namespace <NAMESPACE>
```

```yaml values.yaml
config:
  ztwaAuth:
    ztwaAccessID: "<API_KEY_ACCESS_ID>"
    ztwaAccessType: access_key
    ztwaExistingSecret: ztwa-access
    authorizedAccessIDs:
      - "<ALLOWED_ACCESS_ID>"
```

#### Cloud identity (AWS IAM, Azure AD, GCP)

Set the cloud auth method's Access ID. No access key is needed:

```yaml values.yaml
config:
  ztwaAuth:
    ztwaAccessID: "<CLOUD_ACCESS_ID>"
    ztwaAccessType: ""   # empty = detect the cloud automatically
    authorizedAccessIDs:
      - "<ALLOWED_ACCESS_ID>"
```

ZTWA detects the cloud through the instance metadata service at `169.254.169.254`. If the pods can't reach it, for example on EKS with an IMDSv2 hop limit of 1, set `ztwaAccessType` to `aws_iam`, `azure_ad` or `gcp`.

### Proxy mode

The web proxy uses HTTP by default. For SOCKS5, set:

```yaml values.yaml
webProxy:
  env:
    - name: WEB_PROXY_TYPE
      value: SOCKS
```

### Session recording

The media server records each session to the shared volume, and the dispatcher uploads it to S3 or S3-compatible storage. Recording needs [shared storage](https://docs.akeyless.io/docs/sra-web-access-on-k8s#shared-storage).

```yaml values.yaml
recording:
  enabled: true
  s3:
    enabled: true
    bucket: "<S3_BUCKET_NAME>"
    region: "<AWS_REGION>"
    prefix: "<OPTIONAL_PREFIX>"
    endpoint: "<OPTIONAL_S3_COMPATIBLE_ENDPOINT>"
    existingSecretName: "<S3_CREDENTIALS_SECRET_NAME>"
    accessKeyIdKey: "access-key-id"
    secretAccessKeyKey: "secret-access-key"
    compress: false
    sse:
      type: "" # "" | sse-s3 | sse-kms
      kmsKeyId: "<OPTIONAL_KMS_KEY_ID_OR_ARN>"
```

* `enabled`: Record sessions. Upload also needs `s3.enabled`.
* `s3.bucket`, `s3.region`, `s3.prefix`: Destination bucket and object path. `bucket` and `region` are required for upload.
* `s3.endpoint`: Endpoint of an S3-compatible service, for example MinIO. Leave empty for AWS S3.
* `s3.existingSecretName`: Secret with the S3 credentials, under the keys set in `accessKeyIdKey` and `secretAccessKeyKey`. When empty, the dispatcher uses the AWS default credential chain, for example IRSA or an instance profile.
* `s3.compress`: Gzip the recordings before upload.
* `s3.sse.type`, `s3.sse.kmsKeyId`: Server-side encryption (`sse-s3` or `sse-kms`). An empty `kmsKeyId` uses the default KMS key.

#### Session visibility prerequisites

Recordings, Session Overview entries and Audit Log events share the same session ID. If sessions work but don't appear in Session Overview or the Audit Log, check that:

* `config.clusterName` exactly matches the cluster name of the connected Akeyless Gateway.
* ZTWA authenticates with the same Access ID that the Gateway is registered with.
* If the Gateway certificate is private or self-signed, it's set in `config.gatewayCert.tlsExistingSecret`.
* The Gateway is running and registered in the same Akeyless account.

### Autoscaling

The chart can scale the web workers by the share of busy workers. Autoscaling needs `metrics.enabled`, and `webProxy.replicaCount` must be set:

```yaml values.yaml
metrics:
  enabled: true
HPA:
  enabled: true
  webWorker:
    busyWorkersPercentage: 50
    minReplicas: 3
    maxReplicas: 14
webProxy:
  replicaCount: 1
```

A worker pod gets `webWorker.terminationGracePeriodSeconds` (default `3600`) to finish its live session before a scale-down or an upgrade stops it.

## Install the Helm chart

1. Install the chart with your `values.yaml`:

   ```shell
   helm install <RELEASE_NAME> akeyless/akeyless-zero-trust-web-access -f values.yaml --namespace <NAMESPACE>
   ```

2. Check that the components are running:

   ```shell
   kubectl get deploy web-dispatcher-deployment web-worker-deployment web-proxy-deployment --namespace <NAMESPACE>
   kubectl get daemonset <RELEASE_NAME>-mediamtx --namespace <NAMESPACE>
   ```

> ⚠️ **Warning:**
>
> The dispatcher, the web workers and the web proxy run as non-root users. The media server (`mediamtx` DaemonSet) doesn't set a non-root user, so if your cluster enforces a policy such as the Kubernetes `restricted` Pod Security Standard, allow an exception for it.

### Set the external URLs

1. Get the external addresses of the dispatcher (the Service ending in `-dispatcher`, port `9000`) and the web proxy (the Service ending in `-proxy`, port `19414`):

   ```shell
   kubectl get svc --namespace <NAMESPACE>
   ```

   If `EXTERNAL-IP` shows `<pending>`, the load balancer is still being created. Wait and run the command again.

2. Add them to `values.yaml`, then run `helm upgrade` with the same values file. The SRA Portal redirects users only to these URLs:

   ```yaml values.yaml
   config:
     allowedBastionUrls:
       - "https://<DISPATCHER_ADDRESS>:9000"
     allowedProxyUrls:
       - "https://<WEB_PROXY_ADDRESS>:19414"
   ```

   ```shell
   helm upgrade <RELEASE_NAME> akeyless/akeyless-zero-trust-web-access -f values.yaml --namespace <NAMESPACE>
   ```

3. In the [SRA Portal](https://docs.akeyless.io/docs/sra-portal), use the same URLs:
   * **Web Application Dispatcher**: the dispatcher URL
   * **Web Proxy URL**: the web proxy URL, for proxy-mode sessions

If you use an ingress for the dispatcher (`dispatcher.ingress.enabled: true`), use `dispatcher.ingress.hostname` instead. With an ingress, the chart sets the dispatcher Service to `NodePort`.

## Upgrade from an earlier chart

The values structure changed. The chart stops with an error that names each old key it finds, so update your `values.yaml` first:

| Earlier chart | Current chart |
| --- | --- |
| `dispatcher.config.apiGatewayURL` | `config.gatewayURL` |
| `dispatcher.config.apiGatewayCert.tlsCertsSecretName` | `config.gatewayCert.tlsExistingSecret` |
| `dispatcher.config.clusterName` | `config.clusterName` |
| `dispatcher.config.privilegedAccess.accessID` | `config.ztwaAuth.ztwaAccessID` |
| `dispatcher.config.privilegedAccess.accessKey` | Removed. Use a Secret in `config.ztwaAuth.ztwaExistingSecret` |
| `dispatcher.config.privilegedAccess.allowedAccessIDs` | `config.ztwaAuth.authorizedAccessIDs` (now required) |
| `dispatcher.config.cloudIdentity.type` | `config.ztwaAuth.ztwaAccessType` |
| `dispatcher.config.allowedBastionUrls`, `allowedProxyUrls` | `config.allowedBastionUrls`, `config.allowedProxyUrls` |
| `dispatcher.config.disableSecureCookie`, `allowedInternalAuth` | `config.disableSecureCookie`, `config.allowedInternalAuth` |
| `dispatcher.service.proxyPort` | `webProxy.service.port` (separate Service) |
| `sessionRecording.*` | `recording.*` |
| `webWorker.config.policies` (Firefox) | `webWorker.config.policies` (Chromium, Chrome Enterprise JSON) |
| `listOnlyCredentials`, `logForward`, `dlp`, recording `quality` and `watchdog` | Removed |