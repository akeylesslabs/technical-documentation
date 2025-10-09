---
title: Advanced K8s Configuration
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
# Cluster Name & URL

Each Gateway cluster is uniquely identified by combining the **Gateway Access ID**  Authentication Method and the **Cluster Name**.

It means that changing the Gateway **Access ID** or the **Cluster Name** of your Gateway will create an entirely new Gateway cluster, and it will not retrieve the settings and data from the previous Gateway cluster.

That’s why we recommend setting up a meaningful Cluster Name for your Gateway cluster from the very beginning. By default, your cluster name is **defaultCluster**.

To do that, you can set the `clusterName="meaningful-cluster-name"` field as part of the Gateway deployment.

In addition, to set in advance the **Cluster URL**, you can set the `CLUSTER_URL`  under the `env` section as an environment variable.

You can also provide a custom display name for the Gateway Instance using the `initialClusterDisplayName` variable, which is arbitrary. This name can be changed in the Akeyless Console after the Gateway is installed.

```yaml values.yaml
clusterName: <meaningful-cluster-name>
initialClusterDisplayName:

env:
  - name: CLUSTER_URL
    value: 'https://<Your-Akeyless-GW-URL:8000>'
```

# Encryption Key

To choose an existing [Encryption Key](https://docs.akeyless.io/docs/encryption-keys) to encrypt your Gateway configuration, you can provide the full path to your key using the following setting `configProtectionKeyName`.

By default, the Gateway configuration is encrypted with your account's default encryption key.

> 🚧 Warning
>
> This key can be determined on cluster deployment only, and **cannot** be modified afterward.

## Customer fragment

If your [Encryption Key](https://docs.akeyless.io/docs/encryption-keys) works with [Zero Knowledge](https://docs.akeyless.io/docs/implement-zero-knowledge), create a <Anchor label="Kubernetes Secret" target="_blank" href="https://kubernetes.io/docs/concepts/configuration/secret/">Kubernetes Secret</Anchor> with a Base64-encoded JSON that includes your **Customer Fragment**.

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

# TLS Configuration

We strongly recommend using Akeyless Gateway with TLS to ensure all traffic is encrypted at transit.
Please note that when you're enabling TLS, you must provide a `TLS certificate` and a corresponding `TLS Private Key`.

To set the TLS settings, create a [K8s Secret](https://kubernetes.io/docs/concepts/configuration/secret/) includes your **TLS certificate** in `base64 encoded` format where the `key` of the secret has to be `tls-certificate`:

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
```Text shell
kubectl create secret generic tls-certificate \
  --from-file=tlsCertificate=/path/to/certificate.pem \
  --from-file=tlsPrivateKey=/path/to/private-key.pem \
  --namespace=my-namespace
```

Enable TLS:

```yaml values.yaml
TLSConf:
  enabled: true
  minimumTlsVersion: <TLSv1/TLSv1.1/TLSv1.2/TLSv1.3>
  tlsExistingSecretName: tls-certificate 
```

Alternatively, you can also [configure TLS](https://docs.akeyless.io/docs/tls-certificate) settings using the web interface of the Gateway Configuration Manager.

# OIDC Configuration

To leverage your Gateway for the callback redirects instead of the Akeyless SaaS (in cases your IDP isn't publicly available), you can add the `AKEYLESS_OIDC_GW_AUTH` variable (as seen in the `values.yaml` file below) under the `env` section while making sure the corresponding OIDC App on your IDP has the "**Redirect URI**" set to the Gateway's configuration endpoint (`port 8000`) with the following URI suffix `/api/oidc-callback`  (e.g., `https://Your-Akeyless-GW-URL:8000/api/oidc-callback`).

```yaml values.yaml
globalConfig:
  env:
    - name: AKEYLESS_OIDC_GW_AUTH
      value: "true"
```

Once the Gateway is running, you can set the matching AccessID as your OIDC default login using the [Gateway Configuration Manager](https://docs.akeyless.io/docs/gateway-configuration-manager)

# Cache Configuration

To set up your deployment with **Cluster Cache**, the following settings will display the setup of this service from the deployment perspective. Once it's enabled on the deployment level, you should turn on the desired mode of the [Gateway Cache](https://docs.akeyless.io/docs/configure-the-gateway-cache) using the console or directly via **API**.

To set an internal TLS between the Gateway and cache service, set the `enableTls: true` option:

```yaml
  clusterCache:
    enableTls: false
```

To set the cache on your gateway with a default encryption key to support full offline mode, create a [K8s Secret](https://kubernetes.io/docs/concepts/configuration/secret/) that includes your `cluster-cache-encryption-key` base64 encoded :

```shell
kubectl create secret generic cache-configuration \
  --from-literal=cluster-cache-encryption-key=<base64-encoded-cluster-cache-encryption-key>
```

And add to the `values.yaml` file the K8s secret name:

```yaml values.yaml
  clusterCache:
    encryptionKeyExistingSecret: "cache-configuration"
    enableTls: false
```

To control the cache settings, you can [configure the cache](https://docs.akeyless.io/docs/configure-the-gateway-cache) using the Gateway Configuration Manager.

## High Availability Cache

While the **Cache** setup can address many cases for some environments, there is a requirement for a full high availability architecture of the **Cache** service, in such cases when the `cacheHA` is enabled, it will **override** all existing settings of the default cache. The HA mode of the cache **must** be set with a storage class with the `ReadWriteOnce` access mode.

> 📘 Note
>
> This feature is available only from GW version `4.34.0` and higher. To use Cache HA, **existing** GW Helm deployments must be fully uninstalled before proceeding with the Cache HA setup.

To set the default encryption key to support full offline mode, create a [K8s Secret](https://kubernetes.io/docs/concepts/configuration/secret/) that includes your `cluster-cache-encryption-key` base64 encoded :

```yaml
kubectl create secret generic cache-configuration \
  --from-literal=cluster-cache-encryption-key=<base64-encoded-cluster-cache-encryption-key>
```

Set your [storage class](https://kubernetes.io/docs/concepts/storage/storage-classes/) according to your environment, for example:

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

Edit the following section in your `values.yaml` file:

```yaml
cacheHA:
  enabled: true
  nameOverride: "cache-ha"
  encryptionKeyExistingSecret: "cache-configuration"
  tls:
    enabled: true
    authClients: false
    autoGenerated: true

  sentinel:
    enabled: true

  global:
    defaultStorageClass: "akeyless-cache-rwo"
```

Where the **TLS** settings will be applied and generated automatically, make sure to leave the `authClients`set to `false` as `mTLS` between the Gateway and the Cache service is not supported yet, and `sentinel` must be `enabled`.

Additionally, you can add [topology spread constraints]()  settings to control how Pods are spread across your cluster in the event of failures. Ensure that you set the relevant settings in the Gateway section as well, in addition to the `cacheHA` section:

```yaml Cache HA
cacheHA:
  enabled: true
  nameOverride: "cache-ha"
  encryptionKeyExistingSecret: "cache-configuration"
  tls:
    enabled: true
    authClients: false
    autoGenerated: true

  sentinel:
    enabled: true

  global:
  defaultStorageClass: "akeyless-cache-rwo"

  master:
    pdb:
      create: true
      minAvailable: ""
      maxUnavailable: "40%"
    podLabels:
      app.kubernetes.io/component: cache-master
    topologySpreadConstraints:
      - maxSkew: 1
        topologyKey: topology.kubernetes.io/zone
        whenUnsatisfiable: ScheduleAnyway
        labelSelector:
          matchLabels:
            app.kubernetes.io/component: cache-master
  replica:
    pdb:
      create: true
      maxUnavailable: ""
      minAvailable: "40%"
    podLabels:
      app.kubernetes.io/component: cache-replicas
    topologySpreadConstraints:
      - maxSkew: 1
        topologyKey: topology.kubernetes.io/zone
        whenUnsatisfiable: ScheduleAnyway
        labelSelector:
          matchLabels:
            app.kubernetes.io/component: cache-replicas
```

To control the cache settings, you should [configure the cache](https://docs.akeyless.io/docs/configure-the-gateway-cache) using the Gateway Configuration Manager.

# Working With K8s Secrets

To provide the settings of your Gateway deployment directly from your local k8s secrets store, you can set the following settings:

* `gateway-access-key`
* `gateway-uid-init-token`
* `allowed-access-permissions`
* `tlsCertificate`
* `gateway-certificate`
* `gateway-certificate-key`
* `customer-fragments`

> 🚧 Warning
>
> Providing any of those settings using an existing K8s secret,  make sure that the corresponding parameters are left empty in your `values.yaml` file.

```yaml values.yaml
gatewayCredentialsExistingSecret:
allowedAccessPermissionsExistingSecret:
customerFragmentsExistingSecret:
tlsExistingSecretName:
existingSecretName:
encryptionKeyExistingSecret:
```

# Fixed Artifact Repository

In some environments where an IP address must be whitelisted, to pull Akeyless official artifacts as part of your Gateway deployment, uncomment the fixedArtifactRepository: "artifacts.site2.akeyless.io" setting in your chart:

```yaml
image:
  repository: akeyless/base
  pullPolicy: Always
  tag: latest
fixedArtifactRepository: "artifacts.site2.akeyless.io"
```

You can explicitly provide the k8s secret name that contains the credentials for the private registry if needed using the `imagePullSecrets` setting:

```yaml
image:
  repository: akeyless/base
  pullPolicy: Always
  tag: latest
  imagePullSecrets:
    - name: regcred

fixedArtifactRepository: "artifacts.site2.akeyless.io"
```

# Rate Limit

To set a local rate limit on your Gateway instance you can add the `GW_RATE_LIMIT`  environment variable where the value will set the maximum calls per minute. When a client reaches that threshold, this will be logged and any additional requests during that minute will be discarded on the Gateway:

```yaml YAML
env:
  - name: GW_RATE_LIMIT
    value: 4000
```

# Custom CA

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
