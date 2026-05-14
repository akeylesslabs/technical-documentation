---
title: Helm Values Reference
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
Use this page to find Helm settings by deployment goal:

| Goal | Section |
| --- | --- |
| Set cluster identity and login behavior | [Identity and Access Settings](#identity-and-access-settings) |
| Configure transport security and trust | [Security Settings](#security-settings) |
| Configure cache behavior and high availability | [Cache Settings](#cache-settings) |
| Configure deployment runtime options | [Operational Settings](#operational-settings) |

## Identity and Access Settings

### Cluster Name & URL

Each Gateway cluster is uniquely identified by combining the **Gateway Access ID** Authentication Method and the **Cluster Name**.

It means that changing the Gateway **Access ID** or the **Cluster Name** of your Gateway will create an entirely new Gateway cluster, and it will not retrieve the settings and data from the previous Gateway cluster.

That’s why we recommend setting up a meaningful Cluster Name for your Gateway cluster from the very beginning. By default, your cluster name is **defaultCluster**.

To do that, you can set the `clusterName="meaningful-cluster-name"` field as part of the Gateway deployment.

In addition, to set in advance the **Cluster URL**, you can set the `CLUSTER_URL` under the `env` section as an environment variable.

You can also provide a custom display name for the Gateway Instance using the `initialClusterDisplayName` variable, which is arbitrary. This name can be changed in the Akeyless Console after the Gateway is deployed.

```yaml values.yaml
clusterName: <meaningful-cluster-name>
initialClusterDisplayName:

env:
  - name: CLUSTER_URL
    value: 'https://<Your-Akeyless-GW-URL>:8000'
```

### Encryption Key

To choose an existing [Encryption Key](https://docs.akeyless.io/docs/encryption-keys) to encrypt your Gateway configuration, you can provide the full path to your key using the following setting `configProtectionKeyName`.

By default, the Gateway configuration is encrypted with your account's default encryption key.

> ⚠️ **Warning:**
>
> This key can be determined on cluster deployment only, and **cannot** be modified afterward.

#### Customer Fragment

If your [Encryption Key](https://docs.akeyless.io/docs/encryption-keys) works with [Zero Knowledge](https://docs.akeyless.io/docs/gateway-zero-knowledge), create a [Kubernetes Secret](https://kubernetes.io/docs/concepts/configuration/secret/) with a Base64-encoded JSON that includes your **Customer Fragment**.

```shell values.yaml
kubectl create secret generic customer-fragment \
  --from-literal=customer-fragments=<customer-fragment>
  
kubectl create secret generic customer-fragment \
  --from-file=customer-fragments=<customer-fragment-json-path>
```

Add the secret to the `values.yaml` file:

```yaml values.yaml
customerFragmentsExistingSecret: customer-fragment
```

## Security Settings

### TLS Configuration

We strongly recommend using Akeyless Gateway with TLS to ensure all traffic is encrypted in transit.
Note that when you enable TLS, you must provide a TLS certificate and a corresponding TLS private key.

To configure the TLS settings, create a [Kubernetes Secret](https://kubernetes.io/docs/concepts/configuration/secret/) that includes your **TLS Certificate** in a Base64-encoded format where the `key` of the secret has to be `tls-certificate`:

```shell kubectl
kubectl create secret generic tls-certificate \
  --from-file=tlsCertificate=/path/to/certificate.pem \
  --from-file=tlsPrivateKey=/path/to/private-key.pem \
  --namespace=my-namespace
```
```yaml secret.yaml
apiVersion: v1
kind: Secret
metadata:
  name: tls-certificate
type: Opaque
data: 
  tlsCertificate: <base64-encoded-tls-certificate.pem>
  tlsPrivateKey: <base64-encoded-tls-certificate-key.pem>
```

Enable TLS on the Akeyless Gateway by modifying the `TLSConf` key in the `values.yaml` file of the Gateway:

```yaml values.yaml
TLSConf:
  enabled: true
  minimumTlsVersion: <TLSv1/TLSv1.1/TLSv1.2/TLSv1.3>
  tlsExistingSecret: tls-certificate

  #Optionally override the following default values if needed when migrating to the Akeyless Unified Gateway
  tlsCertificateSecretKeyName: tlsCertificate
  tlsPrivateKeySecretKeyName:  tlsPrivateKey
```

Alternatively, you can also [configure TLS](https://docs.akeyless.io/docs/gateway-tls-settings) using the web interface of the Gateway Configuration Manager.

### TLS 1.3 and PQC on Any Cloud Platform

The same TLS and PQC settings apply across all cloud platforms where Akeyless Gateway runs on Kubernetes, including managed and self-managed clusters.

To enable hybrid post-quantum key exchange on the Gateway pod, set TLS 1.3 in `TLSConf`:

```yaml values.yaml
TLSConf:
  enabled: true
  minimumTlsVersion: TLSv1.3
```

Apply the updated chart values and restart/upgrade the Gateway release.

To verify PQC support, open the Gateway endpoint over HTTPS in Chrome, check the connection security details, and confirm the negotiated key exchange includes `X25519MLKEM768`.

`X25519MLKEM768` confirms a hybrid key exchange:

* `X25519` (classical elliptic-curve cryptography)
* ML-KEM 768 (post-quantum cryptography)

### OIDC Configuration

To leverage your Gateway for the callback redirects instead of the Akeyless SaaS (if your IdP isn't publicly available), you can add the `AKEYLESS_OIDC_GW_AUTH` variable (as seen in the `values.yaml` file below) under the `env` section while making sure the corresponding OIDC App on your IdP has the "**Redirect URI**" set to the Gateway's configuration endpoint (`port 8000`) with the following URI suffix `/api/oidc-callback` (for example, `https://Your-Akeyless-GW-URL:8000/api/oidc-callback`).

```yaml values.yaml
globalConfig:
  env:
    - name: AKEYLESS_OIDC_GW_AUTH
      value: "true"
```

Once the Gateway is running, you can set the matching AccessID as your OIDC default login using the [Gateway Configuration Manager](https://docs.akeyless.io/docs/configure-gateway)

## Cache Settings

This section covers Helm cache deployment options. For cache behavior, terminology, outage semantics, and request flow details, see [Gateway Caching](https://docs.akeyless.io/docs/gateway-caching).

### Cluster Cache (Standalone)

Use standalone cluster cache when Gateway pods need a shared Redis cache service.

```yaml values.yaml
globalConfig:
  clusterCache:
    enabled: true
    enableTls: false
```

To enable durable storage for standalone cluster cache, configure persistence:

```yaml values.yaml
globalConfig:
  clusterCache:
    enabled: true
    persistence:
      enabled: true
      existingClaim: ""
      accessMode: "ReadWriteOnce"
      storageClass: ""
      size: 10Gi
```

If `globalConfig.clusterCache.persistence.enabled` is `false`, the standalone cache does not mount a PersistentVolumeClaim at `/data`.

Optional Redis runtime flags can be passed through `globalConfig.clusterCache.extraArgs`. This key is a direct pass-through to the `redis-server` command arguments for the standalone cluster cache pod.

* Supported options are Redis server command-line flags, documented by Redis:
    * [Redis configuration](https://redis.io/docs/latest/operate/oss_and_stack/management/config/)
    * [Redis persistence](https://redis.io/docs/latest/operate/oss_and_stack/management/persistence/)
* There are no Akeyless-specific `extraArgs` keys. Akeyless does not parse custom keys under this field.

Example (`values.yaml`):

```yaml values.yaml
globalConfig:
  clusterCache:
    extraArgs:
      - --save
      - ""
      - --appendonly
      - "no"
```

In this example, Redis snapshotting and AOF persistence are disabled by explicit Redis flags.

### Cluster Cache HA (`cacheHA`)

Enable `cacheHA` for a high-availability [Redis Sentinel](https://redis.io/docs/latest/operate/oss_and_stack/management/sentinel/) topology. When `cacheHA.enabled=true`, this mode replaces the default standalone cache service.

```yaml values.yaml
cacheHA:
  enabled: true
  nameOverride: cluster-cache-ha
  replicas: 3
  auth: true
  authKey: redis-password
  existingSecret: "{{ .Release.Name }}-cluster-cache-ha"
```

Cache HA persistence is controlled separately:

```yaml values.yaml
cacheHA:
  persistentVolume:
    enabled: true
    storageClass: ~
    accessModes:
      - ReadWriteOnce
    size: 10Gi
```

Set the appropriate [StorageClass](https://kubernetes.io/docs/concepts/storage/storage-classes/) according to the environment, for example:

```yaml AWS
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: akeyless-cache-rwo
provisioner: ebs.csi.aws.com
volumeBindingMode: WaitForFirstConsumer
allowVolumeExpansion: true
parameters:
  type: gp3
  encrypted: "true"
```
```yaml Azure
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: akeyless-cache-rwo
provisioner: disk.csi.azure.com
volumeBindingMode: WaitForFirstConsumer
allowVolumeExpansion: true
parameters:
  skuName: Premium_LRS
  cachingMode: ReadOnly
```
```yaml GCP
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: akeyless-cache-rwo
provisioner: pd.csi.storage.gke.io
volumeBindingMode: WaitForFirstConsumer
allowVolumeExpansion: true
parameters:
  type: pd-balanced
```
```yaml Ceph
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: akeyless-cache-rwo
provisioner: rbd.csi.ceph.com
volumeBindingMode: WaitForFirstConsumer
allowVolumeExpansion: true
parameters:
  pool: <your-ceph-pool-name> 
  clusterID: <your-ceph-cluster-id> 
  csi.storage.k8s.io/provisioner-secret-name: <your-provisioner-secret-name> 
  csi.storage.k8s.io/provisioner-secret-namespace: <your-secret-namespace> 
  csi.storage.k8s.io/node-stage-secret-name: <your-node-stage-secret-name>
  csi.storage.k8s.io/node-stage-secret-namespace: <your-secret-namespace> 
  encrypted: "true"
```

If you enable `cacheHA`, set or review the following keys to configure authentication and pod placement behavior:

```yaml values.yaml
cacheHA:
  enabled: true
  auth: true
  authKey: redis-password
  existingSecret: "{{ .Release.Name }}-cluster-cache-ha"
  hardAntiAffinity: false
```

To configure cache authentication, set `auth: true` and store the password in a [Kubernetes Secret](https://kubernetes.io/docs/concepts/configuration/secret/) referenced by `existingSecret` and `authKey`.

When **TLS** is enabled, the Gateway deployment automatically generates a Kubernetes Secret containing the TLS certificate and key.

For production environments, set `hardAntiAffinity` to schedule cache HA pods on different nodes.

Additionally, you can add topology spread constraint settings to control how pods are spread across your cluster in the event of failures. The full configuration settings can be found in this [link](https://github.com/DandyDeveloper/charts/blob/master/charts/redis-ha/values.yaml).

For cache runtime behavior, terminology, `ignore-cache`, and outage semantics, see [Gateway Caching](https://docs.akeyless.io/docs/gateway-caching).

#### Cluster Cache Encryption Key and Offline Scale-Out

Kubernetes Secret–based encryption keys for Cluster Cache are used **only when offline scale-out mode is enabled**.

```yaml values.yaml
globalConfig:
  clusterCache:
    enableScaleOutOnDisconnectedMode: false  # default
```

Accepted Values:

* `false` (default): The Gateway does not read or generate a Kubernetes Secret for the cluster cache encryption key. The Kubernetes Secret–based encryption key flow is disabled, even if cache is enabled.
* `true`: The Gateway will read or generate a Kubernetes Secret to support offline scale-out.
    * If encryptionKeyExistingSecret is set, the Gateway uses that Secret.
    * If not set, the Helm chart generates a new encryption key and stores it in a Kubernetes Secret.
    * **RBAC Requirement:** When `enableScaleOutOnDisconnectedMode: true`, the Gateway ServiceAccount must have permission to get Kubernetes Secrets in the namespace. Missing permissions will cause Gateway startup to fail with a forbidden: cannot get resource "secrets" error.

## Operational Settings

### Pod Scheduling

Use the following values to control pod placement, distribution, and scheduling constraints for the Gateway deployment. These settings all live under `gateway.deployment` in the chart.

#### Node selector

Schedule pods only on nodes that match a label selector. Replace the example label with a real node label from your cluster.

```yaml values.yaml
gateway:
  deployment:
    nodeSelector:
      kubernetes.io/os: linux
```

#### Tolerations

Allow pods to be scheduled on tainted nodes. This is required when your Gateway node pool uses taints for isolation.

```yaml values.yaml
gateway:
  deployment:
    tolerations:
      - key: "dedicated"
        operator: "Equal"
        value: "gateway"
        effect: "NoSchedule"
```

#### Affinity

Use pod affinity or anti-affinity to control co-location of pods. The example below uses soft pod anti-affinity to prefer spreading pods across nodes. Replace `<release-name>` with your Helm release name.

```yaml values.yaml
gateway:
  deployment:
    affinity:
      enabled: true
      data:
        podAntiAffinity:
          preferredDuringSchedulingIgnoredDuringExecution:
            - weight: 100
              podAffinityTerm:
                labelSelector:
                  matchLabels:
                    app.kubernetes.io/name: akeyless-gateway
                    app.kubernetes.io/instance: <release-name>
                topologyKey: kubernetes.io/hostname
```

For required (hard) scheduling rules, use `requiredDuringSchedulingIgnoredDuringExecution` instead. See the [Kubernetes affinity documentation](https://kubernetes.io/docs/concepts/scheduling-eviction/assign-pod-node/#affinity-and-anti-affinity) for full reference.

#### Topology spread constraints

Spread pods across zones or nodes to improve availability. Akeyless recommends configuring topology spread constraints in any multi-pod production deployment.

Because `topologySpreadConstraints` is rendered inside the `affinity` block in this chart, `affinity.enabled` must be `true`. Replace `<release-name>` with your Helm release name.

```yaml values.yaml
gateway:
  deployment:
    affinity:
      enabled: true
      data: {}

    topologySpreadConstraints:
      - maxSkew: 1
        topologyKey: topology.kubernetes.io/zone
        whenUnsatisfiable: ScheduleAnyway
        labelSelector:
          matchLabels:
            app.kubernetes.io/name: akeyless-gateway
            app.kubernetes.io/instance: <release-name>
      - maxSkew: 1
        topologyKey: kubernetes.io/hostname
        whenUnsatisfiable: ScheduleAnyway
        labelSelector:
          matchLabels:
            app.kubernetes.io/name: akeyless-gateway
            app.kubernetes.io/instance: <release-name>
```

Use `DoNotSchedule` instead of `ScheduleAnyway` for stricter placement enforcement. For full details, see the [Kubernetes topology spread constraints documentation](https://kubernetes.io/docs/concepts/scheduling-eviction/topology-spread-constraints/).

For a broader discussion of pod scheduling and HA best practices for Gateway, see [Pod scheduling for high availability](https://docs.akeyless.io/docs/gateway-best-practices#pod-scheduling-for-high-availability-kubernetes).

### Working with Kubernetes Secrets

To provide the settings of your Gateway deployment directly from your local Kubernetes secrets store, you can set the following settings

> ⚠️ **Warning:**
>
> Providing any of those settings using an existing Kubernetes Secret, make sure that the corresponding parameters are left empty in your `values.yaml` file.

```yaml values.yaml
gatewayCredentialsExistingSecret:
allowedAccessPermissionsExistingSecret:
customerFragmentsExistingSecret:
tlsExistingSecret:
metricsExistingSecret:
encryptionKeyExistingSecret:
```

When using `allowedAccessPermissions`, wildcard access IDs are supported with `access_id: "*"`.

More options for using K8s Secrets can be found directly within the chart values file.

### Gateway Image Defaults and Override

In the unified Gateway chart, the default Gateway deployment image is `gw`.

To override the default and use the `base` image, set the Gateway image repository and tag explicitly:

```yaml values.yaml
gateway:
  deployment:
    image:
      repository: akeyless/base
      tag: latest # use latest-akeyless for non-root
```

When working with white-label environments, prefer Docker Hub repositories over `docker.registry-2.akeyless.io`.

### Fixed Artifact Repository

In some environments where an IP address must be whitelisted, to pull Akeyless official artifacts as part of your Gateway deployment, uncomment the `fixedArtifactRepository: "artifacts.site2.akeyless.io"` setting in your chart:

```yaml values.yaml
gateway:
  deployment:
    image:
      repository: akeyless/gw
      pullPolicy: Always
      tag: latest
fixedArtifactRepository: "artifacts.site2.akeyless.io"
```

> ℹ️ **Note:**
>
> In Unified Gateway Helm deployments, setting `repository: akeyless/base` with `tag: latest` resolves to `akeyless/base:latest-akeyless` at runtime (non-root image path).
>
> Legacy API Gateway deployments use `akeyless/base:latest`.

```yaml
# Example rendered container image for Unified Gateway
image: akeyless/base:latest-akeyless
```

To verify the resolved image in your cluster:

```shell
kubectl get pod <gateway-pod> -n <namespace> -o jsonpath="{.spec.containers[*].image}"
```

You can explicitly provide the Kubernetes Secret name that contains the credentials for the private registry if needed using the `imagePullSecrets` setting:

```yaml values.yaml
gateway:
  deployment:
    image:
      repository: akeyless/gw
      pullPolicy: Always
      tag: latest
      imagePullSecrets:
        - name: regcred

fixedArtifactRepository: "artifacts.site2.akeyless.io"
```

### Rate Limit

To set a local rate limit on your Gateway instance you can add the `GW_RATE_LIMIT` environment variable where the value will set the maximum calls per minute. When a client reaches that threshold, this will be logged and any additional requests during that minute will be discarded on the Gateway:

```yaml
env:
  - name: GW_RATE_LIMIT
    value: 4000
```

### Custom CA

The Gateway application supports uploading Self-Signed and Private Certificates to establish trust between Akeyless and the relevant endpoint. However, for some cases, a custom Certificate Authority for closed environments might be required to ensure the related service is trusted **before** the Gateway application starts, for example, a proxy server in front of the public Internet.

To support those cases, you'll have to provide and maintain your own CA bundle file using a persistence volume, for example:

```yaml customCA
  customCA:
    enabled: false
    volumeName: "ca-certificates"
    volumeType: "configMap" 
    volumeSourceName: <VolumeSourceName> 
```

where the supported `volumeType` are either `configMap` or `secret` the `volumeSourceName` **must** include a key named `ca-certificates.crt`
