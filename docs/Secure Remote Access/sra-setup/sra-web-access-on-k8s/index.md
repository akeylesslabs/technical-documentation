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
---
Akeyless Zero Trust Web Access Bastion provides Secure Remote Access to internal web applications with session recording.

This deployment can route sessions through an isolated remote browser or directly to the target server, based on secret configuration and policy.

The non-privileged deployment model is supported, so you do not need to add a port `80` binding for the chart to run.

ZTWA session recording captures browser-based web access sessions and supports configurable quality, compression, and encryption for stored recordings.

This chart bootstraps the `Akeyless-Web-Access-Bastion` deployment on Kubernetes with Helm.

## Before you begin

### Requirements

* Helm installed.
* Kubernetes installed.
* Available cluster resources:
    * `webWorker`: minimum `1 vCPU` and `2 GiB` RAM.
    * `dispatcher`: minimum `1 vCPU` and `1 GiB` RAM.

> ⚠️ **Warning:**
>
> To enable Secure Remote Access features, request access to the Akeyless private repository from your account manager.

### Network timeout settings

When an embedded browser session runs behind a load balancer (for example, ELB), idle timeout settings can close active sessions. Set the load balancer idle timeout to a high value or unlimited.

For AWS ELB guidance, see [Configure idle connection timeout](https://docs.aws.amazon.com/elasticloadbalancing/latest/classic/config-idle-timeout.html?icmpid=docs_elb_console).

### Shared storage requirements

To support file downloads to local machines, configure a `StorageClass` with `ReadWriteMany` access mode.

Set a persistent volume reference under `persistence` in `values.yaml`.

```yaml
persistence:
  shareStorageVolume:
    name: share-storage
    storageClassName: "efs-sc"
    accessModes:
      - ReadWriteMany
    persistentVolumeReclaimPolicy: Retain
    annotations: {}
    mountOptions:
      - dir_mode=0650
      - file_mode=0650
    size: 2Gi
```

For Amazon EKS and EFS examples, see [Use Amazon EFS with Amazon EKS](https://docs.aws.amazon.com/eks/latest/userguide/efs-csi.html).

For security, keep persistent volume mount permissions at `0650`.

For current Zero Trust Web Access (ZTWA) versions, configure the shared volume so the root directory is owned by group `10000`.

When using Amazon EFS, mount through an EFS access point configured with the required ownership and permissions.

### Horizontal autoscaling prerequisites

Horizontal autoscaling uses the Kubernetes HorizontalPodAutoscaler.

Install Kubernetes Metrics Server in the cluster before enabling autoscaling. See [Metrics Server](https://github.com/kubernetes-sigs/metrics-server).

## Install the Helm chart

1. Add and update the Akeyless Helm repository.

```shell
helm repo add akeyless https://akeylesslabs.github.io/helm-charts
helm repo update
```

1. Prepare a local `values.yaml` file.

Copy from GitHub: [akeyless-zero-trust-web-access chart values](https://github.com/akeylesslabs/helm-charts/tree/main/charts/akeyless-zero-trust-web-access).

Or generate locally:

```shell
helm show values akeyless/akeyless-zero-trust-web-access > values.yaml
```

1. Install the chart.

```shell
helm install <RELEASE_NAME> akeyless/akeyless-zero-trust-web-access -f values.yaml
```

1. Verify deployments.

```shell
kubectl describe deploy web-worker-deployment -n <NAMESPACE>
kubectl describe deploy web-dispatcher-deployment -n <NAMESPACE>
```

### Baseline resources and non-root runtime

The chart exposes resource requests and limits for workload and init containers.

The chart templates also configure non-root execution for Web Dispatcher and Web Worker containers.

ZTWA session recordings support configurable quality, compression, and encryption for stored sessions.

Do not override default user or group security context values unless directed by Akeyless Support.

Use this baseline for environments with strict Kubernetes admission policies:

```yaml
dispatcher:
  resources:
    requests:
      cpu: 1000m
      memory: 1Gi
    limits:
      memory: 2Gi
  initContainer:
    resources:
      requests:
        cpu: 100m
        memory: 128Mi
      limits:
        memory: 512Mi

webWorker:
  resources:
    requests:
      cpu: 1000m
      memory: 1Gi
    limits:
      memory: 2Gi
  initContainer:
    resources:
      requests:
        cpu: 100m
        memory: 128Mi
      limits:
        memory: 512Mi
```

After installation, verify runtime security context in deployment specs:

```shell
kubectl get deploy web-dispatcher-deployment -n <NAMESPACE> -o yaml
kubectl get deploy web-worker-deployment -n <NAMESPACE> -o yaml
```

### Get the dispatcher service URL

After installation, retrieve the external URL of the dispatcher service. This URL is required for the **Web Application Dispatcher** field in the [SRA Portal](https://docs.akeyless.io/docs/sra-portal).

```shell
kubectl get svc -n <NAMESPACE>
```

Use the `EXTERNAL-IP` or hostname for the dispatcher service in SRA Portal configuration:

* **Web Application Dispatcher** (main sessions): `http://<EXTERNAL_IP>:9000`
* **Web Proxy URL** (secure proxy or HTTP proxy mode): `http://<EXTERNAL_IP>:19414`

> ℹ️ **Note:**
>
> If `EXTERNAL-IP` shows `<pending>`, the cloud load balancer is still provisioning. Wait and run the command again.

If you use Ingress instead of `LoadBalancer`, use the hostname from `dispatcher.ingress.hostname` in `values.yaml`.

## Configure values.yaml

### Private registry credentials

To pull images from the Akeyless private registry, use `imagePullSecrets`.

Before installing the chart, create a Kubernetes Secret of type `kubernetes.io/dockerconfigjson`:

```shell
kubectl create secret docker-registry <SECRET_NAME> \
  --docker-server=<AKEYLESS_REGISTRY_SERVER> \
  --docker-username=<AKEYLESS_REGISTRY_USERNAME> \
  --docker-password=<AKEYLESS_REGISTRY_PASSWORD> \
  --namespace <NAMESPACE>
```

Reference that secret in `values.yaml` for components that pull from the private registry:

```yaml
dispatcher:
  image:
    imagePullSecrets:
      - name: <SECRET_NAME>
  initContainer:
    imagePullSecrets:
      - name: <SECRET_NAME>

webWorker:
  image:
    imagePullSecrets:
      - name: <SECRET_NAME>
  initContainer:
    imagePullSecrets:
      - name: <SECRET_NAME>
```

> ℹ️ **Note:**
>
> `dockerRepositoryCreds` is available as an inline alternative. Prefer `imagePullSecrets` wherever possible.

### Akeyless API endpoints

Set `apiGatewayURL` to the Akeyless Gateway REST API endpoint.

For current ZTWA versions, include the `/api/v2` path.

```yaml
apiGatewayURL: https://rest.akeyless.io/api/v2

# Optional: set the Akeyless SaaS URL for a specific environment.
env:
  - name: AKEYLESS_URL
    value: "https://vault.akeyless.io"
```

### Web access session recording configuration

Use the `sessionRecording` block to configure browser-based session recording for ZTWA.

```yaml
sessionRecording:
  enabled: true
  quality: "360p" # 144p | 240p | 360p | 480p | 720p | 1080p
  upload:
    enabled: true
    s3Bucket: "<S3_BUCKET_NAME>"
    s3Region: "<AWS_REGION>"
    s3Prefix: "<OPTIONAL_PREFIX>"
    s3Endpoint: "<OPTIONAL_S3_COMPATIBLE_ENDPOINT>"
    compress: false
    sse:
      type: "" # "" | sse-s3 | sse-kms
      kmsKeyId: "<OPTIONAL_KMS_KEY_ID_OR_ARN>"
    existingSecretNames:
      s3: "<S3_CREDENTIALS_SECRET_NAME>"
      s3AccessKeyIdKey: "access-key-id"
      s3SecretAccessKeyKey: "secret-access-key"
```

When enabled, the worker captures the browser session and the dispatcher prepares the upload artifact and uploads it to S3 or S3-compatible storage.

#### Recording quality

Set `sessionRecording.quality` to one of:

* `144p`
* `240p`
* `360p`
* `480p`
* `720p`
* `1080p`

#### Upload and encryption options

Use `sessionRecording.upload` to control destination and storage behavior:

* `enabled`: Turn upload on or off.
* `s3Bucket`, `s3Region`, `s3Prefix`: Destination bucket and object path.
* `s3Endpoint`: Optional custom endpoint for S3-compatible platforms.
* `compress`: Gzip-compress before upload.
* `sse.type`: Server-side encryption mode (`sse-s3` or `sse-kms`).
* `sse.kmsKeyId`: KMS key ID or ARN when `sse-kms` is used.

#### Credentials source

Provide S3 credentials by using `sessionRecording.upload.existingSecretNames.s3`.

If the secret is not set, the deployment falls back to the AWS default credential chain.

#### Worker lifecycle watchdog controls

Use `sessionRecording.watchdog` to tune long-running recording behavior:

* `clientConnectTimeoutSeconds`: Timeout for initial browser websocket connection.
* `intervalSeconds`: How often watchdog checks run.
* `maxDurationSeconds`: Maximum wall-clock duration for one recording.

#### Service-specific recording overrides

For advanced setups, service-level `recording` blocks can override part of the top-level `sessionRecording` config:

* `dispatcher.config.recording`: upload-related override fields for the dispatcher.
* `webWorker.config.recording`: capture-related override fields (`enabled`, `quality`) for workers.

Use these only when you need per-service behavior that differs from the shared `sessionRecording` defaults.

### HTTP proxy mode

To enable HTTP proxy mode for remote access, set `WEB_PROXY_TYPE` in dispatcher `env`.

```yaml
env:
  - name: WEB_PROXY_TYPE
    value: http
```

> ⚠️ **Warning:**
>
> HTTP proxy mode currently works with Chrome. For Firefox, skip this setting so the default SOCKS proxy mode is used.

### Privileged access and allowed requesters

Configure a privileged `accessID` with `read` and `list` permissions so the bastion can fetch target secrets for authenticated users.

Use `allowedAccessIDs` to limit which Access IDs can request sessions.

```yaml
privilegedAccess:
  accessID: "<ACCESS_ID>"
  allowedAccessIDs:
    - <ALLOWED_ACCESS_ID>
```

## Configure authentication

Supported authentication methods:

* [API Key](https://docs.akeyless.io/docs/auth-with-api-key)
* [AWS IAM](https://docs.akeyless.io/docs/auth-with-aws)
* [Azure Active Directory](https://docs.akeyless.io/docs/auth-with-azure)

### API key authentication

For [API Key](https://docs.akeyless.io/docs/auth-with-api-key) authentication, configure `accessID`, `accessKey`, and the allowed requester list:

```yaml
privilegedAccess:
  accessID: "<API_KEY_ACCESS_ID>"
  accessKey: "<API_KEY>"
  allowedAccessIDs:
    - <ALLOWED_ACCESS_ID>
```

### AWS IAM authentication

For clusters running in AWS, you can use [AWS IAM](https://docs.akeyless.io/docs/auth-with-aws) machine-to-machine authentication.

For instance profile or node IAM role flows, set the AWS IAM Access ID:

```yaml
privilegedAccess:
  accessID: "<AWS_IAM_ACCESS_ID>"
  allowedAccessIDs:
    - <ALLOWED_ACCESS_ID>
```

If the dispatcher cannot detect AWS through the instance metadata service, set `dispatcher.config.cloudIdentity.type` to `aws_iam` to skip auto-detection and use the configured AWS IAM identity directly. This is useful when the metadata service is unreachable, such as on EKS nodes that use the default IMDSv2 hop limit or in clusters with restrictive network policies.

```yaml
dispatcher:
  config:
    privilegedAccess:
      accessID: "<AWS_IAM_ACCESS_ID>"
      accessKey: ""
      allowedAccessIDs:
        - <ALLOWED_ACCESS_ID>
    cloudIdentity:
      type: "aws_iam"
```

Use this override when auto-detection fails. Leave `accessKey` empty for AWS IAM machine-to-machine authentication.

### Azure Active Directory authentication

For AKS, Azure AD authentication uses OpenID Connect and JWT validation against the configured tenant.

Set the [Azure Active Directory](https://docs.akeyless.io/docs/auth-with-azure) Access ID:

```yaml
privilegedAccess:
  accessID: "<AZURE_AD_ACCESS_ID>"
  allowedAccessIDs:
    - <ALLOWED_ACCESS_ID>
```
