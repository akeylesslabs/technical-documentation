---
title: Advanced K8s Configuration
excerpt: ''
deprecated: false
hidden: true
metadata:
  title: ''
  description: ''
  robots: index
next:
  description: ''
  pages:
    - type: basic
      slug: implement-zero-knowledge
      title: Implementing Zero Knowledge
---
# Cluster Name & URL

```yaml values.yaml
env:
- name: CLUSTER_URL
  value: https://<GW-URL>
akeylessUserAuth:
  clusterName:
  initialClusterDisplayName:
```

Each Gateway instance is uniquely identified by combining the **Admin Access ID**  Authentication Method and the **Cluster Name**.

It means that changing the Admin **Access ID** or the **Cluster Name** of your Gateway instance will create an entirely new Gateway instance, and it will not retrieve the settings and data from the previous Gateway instance.

That’s why we recommend setting up a meaningful Cluster Name for your Gateway cluster from the very beginning. By default, your cluster name is **defaultCluster**.

To do that, you can set the `clusterName="meaningful-cluster-name"` field as part of the Gateway deployment.

In addition, to set in advance the **Cluster URL**, you can set the `CLUSTER_URL`  under the `env` section as an environment variable.

You can also provide a custom display name for the Gateway Instance using the `initialClusterDisplayName` variable, which is arbitrary. This name can be changed in the Akeyless Console after the Gateway is installed.

# Encryption Key

To choose an existing [Encryption Key](https://docs.akeyless.io/docs/encryption-keys) to encrypt your Gateway configuration, you can provide the full path to your key using the following setting `configProtectionKeyName`.

By default, the Gateway configuration is encrypted with your account's default encryption key.

> 🚧 Warning
>
> This key can be determined on cluster deployment only, and **cannot** be modified afterward.

## Customer fragment

If your [Encryption Key](https://docs.akeyless.io/docs/encryption-keys) works with [Zero Knowledge](https://docs.akeyless.io/docs/implement-zero-knowledge), provide a JSON containing your Customer Fragment:

```yaml values.yaml
akeylessUserAuth:
  configProtectionKeyName: /KeyName
customerFragments: |
  {
      "customer_fragments": [
          {
              "id": "cf-xyzxyzxyzxyzxyzxyz",
              "value": "xxxxxxxxxxxxxxxxxxxxxx"
          }
      ]
  }
```

# TLS Configuration

You can also [configure TLS settings using the Web interface](https://docs.akeyless.io/docs/tls-certificate) of the Gateway Configuration Manager.

We strongly recommend using Akeyless Gateway with TLS to ensure all traffic is encrypted at transit.\
Please note that when you're enabling TLS, you must provide a TLS certificate and a TLS Private Key.

To set the relevant service to use TLS and the minimum TLS version that will be used by default, set the following:

```yaml values.yaml
TLSConf:
  akeylessWebUI: true
  vaultProxy: true
  akeylessAPIServices: true
  configurationManager: true
  # minimumTlsVersion can be one of the following <TLSv1/TLSv1.1/TLSv1.2/TLSv1.3>
  minimumTlsVersion: "TLSv1.2"
  # excludeCipherSuites: Comma separated list of cipher suites to exclude (e.g. "TLS_ECDHE_ECDSA_WITH_AES_128_CBC_SHA,TLS_ECDHE_RSA_WITH_3DES_EDE_CBC_SHA")
  tlsCertificate: |-
   -----BEGIN CERTIFICATE-----
   -----END CERTIFICATE-----
  tlsPrivateKey: |-
   -----BEGIN RSA PRIVATE KEY-----
   -----END RSA PRIVATE KEY-----
```

# Defaults Gateway Settings

You can also configure the default settings using the [Gateway Configuration Manager](https://docs.akeyless.io/docs/gateway-configuration-manager) UI.

A default [SAML](https://docs.akeyless.io/docs/saml)  or [OIDC](https://docs.akeyless.io/docs/openid)  `Access ID`  can be set for the Gateway (using either `defaultSamlAccessId` or `defaultOidcAccessId` respectively) to automatically select the auth method for end-users logging in to the Gateway Console (port `18888`), upon clicking on the respective auth method.

For OIDC, to leverage your Gateway for the callback redirects instead of the Akeyless SaaS (in cases your IDP isn't publicly available), you can add the `AKEYLESS_OIDC_GW_AUTH` variable (as seen in the `values.yaml` file below) under the `env` section while making sure the corresponding OIDC App on your IDP has the "**Redirect URI**" set to the Gateway's configuration endpoint (port 8000) with the following URI suffix `/api/oidc-callback`  (e.g., `https://Your-Akeyless-GW-URL:8000/api/oidc-callback`).

Set the default [Encryption Key](https://docs.akeyless.io/docs/encryption-keys) that will encrypt all items created on this Gateway using the setting `defaultEncryptionKey` with the full path to your [Encryption Key](https://docs.akeyless.io/docs/encryption-keys) in Akeyless.

Set the default location secrets created by this Gateway will be stored within your Akeyless account using the`defaultSecretLocation` setting with a path to store your secrets. 

> 🚧 Warning
>
> Make sure your Gateway default Authentication Method has `read` permission to access your Encryption key, as well as `create` permission on the desired location to save your secrets.

```yaml values.yaml
env:
  - name: AKEYLESS_OIDC_GW_AUTH
    value: "true"

defaultsConf:
  defaultSamlAccessId: "<SAML Access ID>"
  defaultOidcAccessId: "<OIDC Access ID>"
  defaultEncryptionKey: "</Path/to/Key>"
  defaultSecretLocation: "</Path/To/Save/Secrets>"
```

To work with [CBA](https://docs.akeyless.io/docs/certificate-based-authentication) flow for users login, first set your users' DNS records with the cert authentication subdomain  `auth-cert.akeyless.io` to point to your Gateway IP address.

And set your deployment with the following parameters: 

Under `TLSConf` section, enable the `enableSniProxy` setting, and under the `defaultsConf` section provide your [Certificate](https://docs.akeyless.io/docs/certificate-based-authentication) auth method `accessID`:

```yaml
TLSConf:
  enableSniProxy: true

defaultsConf:
  ## Default Certificate Access ID to be used for initial WebUI login
  defaultCertificateAccessId: "<Access ID>"
```

# Cache Configuration

You can enable caching of secrets and periodic backup of cached secrets, set the `cachingConf` setting and set the `cacheTTL` value in minutes to configure the  TTL for a secret that should be kept in the cache. 

To work with proactive caching set the `proActiveCaching` to true and set the `minimumFetchingTime` to config the Gateway to update secrets in the cache if they are older than the specified value with the `dumpInterval` to set the time in minutes between the two consecutive backups.

To keep your cluster pods always synced via a `clusterCache`  service, you must provide a local K8s secret with an encryption key to encrypt at rest the cached secrets:

```shell
kubectl create secret generic cluster-cache-encryption-key \
--from-literal=cluster-cache-encryption-key="$(openssl rand -base64 64)"
```

To set an internal TLS between the Gateway and `clusterCache` service set the `autoGenerated: true` option, alternatively you can provide the generated TLS secret explicitly.

```yaml
cache:
  tls:
    autoGenerated: true

cachingConf:
  enabled: true
  clusterCache:
    enabled: true
    encryptionKeyExistingSecret: "cluster-cache-encryption-key"
    cacheTTL: 60
  proActiveCaching:
    enabled: true
    minimumFetchingTime: 5
    dumpInterval: 60
```

# Working With K8s Secrets

To provide the settings of your Gateway deployment directly from your local k8s secrets store, you can set the following settings with the corresponding `K8s Secrets names`:

* `admin-access-id`
* `admin-access-key`
* `allowed-access-ids`
* `customer-fragments`
* `akeyless-api-cert.crt` 
* `akeyless-api-cert.key`
* `admin-certificate (base64)`
* `admin-certificate-key (base64)`

> 🚧 Warning
>
> Providing any of those settings using an existing K8s secret,  make sure that the corresponding parameters are left empty in your `values.yaml` file.

```yaml values.yaml
  adminAccessIdExistingSecret:
  adminAccessKeyExistingSecret:
  adminPasswordExistingSecret:
  adminBase64CertificateExistingSecret:
  adminBase64CertificateKeyExistingSecret:
  adminUIDInitTokenExistingSecret:
  allowedAccessIDsExistingSecret:
  allowedAccessPermissionsExistingSecret:
  customerFragmentsExistingSecret:
  customerFragmentsEncodedExistingSecret:
  tlsExistingSecretName: 
  # - akeyless-api-cert.crt (base64)
  # - akeyless-api-cert.key (base64)
```

# Restrict Gateway Access

To restrict access to Gateway services, you can specify exactly which `AccessIDs` will be authorized and will be served by the Gateway. For example, if you want to achieve complete segregation using [Zero-Knowledge Encryption](https://docs.akeyless.io/docs/zero-knowledge) across different teams or applications, you can also set their `AccessIDs` to ensure only they will be able to get service from the Gateway that holds their Fragment. To set the list of users the Gateway services will serve, set the <code>restrictServiceToAccessIds</code> setting with a comma-separated list of `AccessIDs`

```yaml
akeylessUserAuth:
  # adminAccessId is required field, supported types: access_key,password or cloud identity(aws_iam/azure_ad/gcp_gce)
  adminAccessId: 
  # Configure this list to add one or more allowed access to this GW, with the specified permissions and sub-claims.
  allowedAccessPermissions: {}
  restrictServiceToAccessIds:
```

In the above example, in addition to your Gateway admin lists, you are limiting the audience of users that your Gateway will serve. Other `AccessIDs` will not be able to get service from your Gateway.  Alternatively, to block specific `AccessIDs` you can use the `blockedAccessIds` variable instead.

# Fixed Artifact Repository

In some environments where an IP address must be whitelisted, to pull Akeyless official artifacts as part of your Gateway deployment, uncomment the `fixedArtifactRepository: "artifacts.site2.akeyless.io"` setting in your chart:

```yaml
image:
  repository: akeyless/base
  pullPolicy: Always
  tag: latest
fixedArtifactRepository: "artifacts.site2.akeyless.io"
```

# Rate Limit

To set a local rate limit on your Gateway instance you can add the `GW_RATE_LIMIT`  environment variable where the value will set the maximum calls per minute. When a client reaches that threshold, this will be logged and any additional requests during that minute will be discarded on the Gateway:

```yaml YAML
env:
  - name: GW_RATE_LIMIT
    value: 4000
```

# gRPC

To enable **gRPC** on your Gateway set the following, the service will be exposed on port `8085`:

```yaml
grpc:
 enabled: true
```
