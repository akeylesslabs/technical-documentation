---
title: External Secrets Operator
deprecated: false
hidden: false
metadata:
  robots: index
next:
  pages:
    - title: ESO API Specification
      type: link
      url: >-
        https://external-secrets.io/latest/api/spec/#external-secrets.io/v1.AkeylessAuthSecretRef
---
This guide shows how to integrate the **Akeyless Platform** with the **[External Secrets Operator (ESO)](https://external-secrets.io/latest/provider/akeyless/)** to synchronize secrets between Akeyless and Kubernetes.

It covers:

* Installing ESO with Helm
* Configuring authentication from Kubernetes to Akeyless (API Key, Kubernetes Auth, Azure AD, and other cloud identities)
* Using [SecretStore](https://external-secrets.io/latest/api/secretstore/), [ClusterSecretStore](https://external-secrets.io/latest/api/clustersecretstore/), and [ExternalSecret](https://external-secrets.io/latest/api/externalsecret/) to fetch secrets
* Using [PushSecret](https://external-secrets.io/latest/api/pushsecret/) to push Kubernetes secrets back to Akeyless
* Example usage

## Supported Secret Types

The Akeyless ESO provider supports all Akeyless secret types:

* [Static Secrets](https://docs.akeyless.io/docs/static-secrets)
* [Dynamic Secrets](https://docs.akeyless.io/docs/how-to-create-dynamic-secret)
* [Rotated Secrets](https://docs.akeyless.io/docs/rotated-secrets)
* [Certificates](https://docs.akeyless.io/docs/certificate-storage)

You can fetch and push these secret types between Akeyless and Kubernetes using ESO's `ExternalSecret` and `PushSecret` resources.

## How ESO Works With Akeyless

The **External Secrets Operator** is a Kubernetes operator that reads secrets from external systems (such as Akeyless) and creates or updates [standard Kubernetes Secret objects](https://kubernetes.io/docs/concepts/configuration/secret/) in a Kubernetes cluster.

For Akeyless, ESO uses the following custom resources:

* **`SecretStore`**: namespaced definition of how to connect and authenticate to Akeyless.
* **`ClusterSecretStore`**: cluster-wide variant of `SecretStore`.
* **`ExternalSecret`**: defines which Akeyless items to sync into which Kubernetes Secret object.
* **`PushSecret`**: pushes a Kubernetes Secret from the cluster into Akeyless.

At a high level:

1. ESO authenticates to Akeyless using the method specified in `SecretStore` or `ClusterSecretStore`.
2. ESO fetches secrets from Akeyless.
3. ESO writes those values into Kubernetes Secrets (or pushes them back to Akeyless in the case of `PushSecret`).
4. ESO periodically refreshes secrets according to the `refreshInterval` on each `ExternalSecret` or `PushSecret`.

![Illustration for: 3. ESO writes those values into Kubernetes Secrets (or pushes them back to Akeyless in the case of PushSecret). 4. ESO periodically refreshes secrets according to the…](https://files.readme.io/143d329a383df21e1e4481289a4d1be018652093b525d21d77e2b6d758efa807-External_Secrets_Operator_1.jpg)

***

## Architecture & Resources

### In-Cluster Components

* The ESO controller runs as a Kubernetes **Deployment**.
* It watches custom resources: `ExternalSecret`, `SecretStore`, `ClusterSecretStore`, and `PushSecret`.
* It reconciles the desired state by calling Akeyless APIs to create and update Kubernetes Secret objects.

### Akeyless Side

* Akeyless **Authentication Methods** define how Kubernetes workloads authenticate (For example, API Key, Kubernetes Auth, Azure AD, AWS IAM, GCP).
* **Access Roles** control which Akeyless items (paths) a given authentication identity may access.
* ESO uses an **Access ID** (and additional auth parameters) to obtain a token and read or write secrets.

***

## Prerequisites

* A running Kubernetes cluster, **v1.19+** (ESO requirement).
* **Helm** installed locally.
* An Akeyless tenant with:
    * At least one **Authentication Method** (API Key, Kubernetes Auth, Azure AD, AWS IAM, or GCP).
    * An **Access Role** that grants read or write permissions to the relevant secrets.
* For Kubernetes Auth, private deployments, or hybrid deployments:
    * An **Akeyless Gateway** with network access to the Kubernetes API server.

***

## Installing External Secrets Operator With Helm

1. Add the official ESO Helm repository:

    ```shell
    helm repo add external-secrets https://charts.external-secrets.io
    helm repo update
    ```

2. Install ESO (default configuration):

    ```shell
    helm install external-secrets external-secrets/external-secrets --namespace external-secrets --create-namespace
    ```

The ESO controller pods running in the `external-secrets` Namespace should now be running.

***

## Authentication With Akeyless

ESO’s Akeyless provider supports the following **access types**:

* `api_key`
* `k8s`
* `azure_ad`
* `aws_iam`
* `gcp`

> ℹ️ **Note:** For AKS Workload Identity, use the Azure AD Authentication Method (`accessType: azure_ad`).
> When using `accessType: azure_ad`, ESO relies on the identity of the Kubernetes `ServiceAccount` that runs the `ExternalSecret`. Identity is not selected through the `SecretStore`. For full guidance, see [ESO and AKS Workload Identity](https://docs.akeyless.io/docs/eso-and-aks-workload-identity).
>
> ⚠️ **Warning:** OIDC is not supported as an **access type** at this time.

Each Authentication Method in Akeyless exposes an **Access ID**, and for some methods, an additional parameter (`accessTypeParam`) such as:

* **API Key** → `accessTypeParam`: Akeyless Access Key
* **Kubernetes Auth** → `accessTypeParam`: Kubernetes Auth config name
* **Azure AD** → `accessTypeParam`: Azure Object ID (optional)
    * See [ESO and AKS Workload Identity](https://docs.akeyless.io/docs/eso-and-aks-workload-identity) for more information.
* **GCP** → `accessTypeParam`: GCP audience
* **AWS IAM** → `accessTypeParam`: not required

ESO can authenticate in one of two ways:

1. Using a **credentials Secret** (generic pattern, works for all supported access types).
2. Using **Kubernetes Auth-specific fields** (directly referencing a Kubernetes ServiceAccount and/or JWT).

### Creating a Credentials Secret

Store the Akeyless credentials that ESO should use within a Kubernetes Secret:

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: akeyless-secret-creds
  namespace: akeyless-demo
type: Opaque
stringData:
  accessId: "p-XXXX"                 # Access ID of the Akeyless Auth Method
  accessType: "api_key"              # api_key / k8s / azure_ad / aws_iam / gcp
  accessTypeParam: "<access-key>"
```

#### API Key Example (NOT Recommended for Production)

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: akeyless-api-creds
  namespace: akeyless-demo
type: Opaque
stringData:
  accessId: "<p-xxxxxxxxxxxxxxxx>"
  accessType: "api_key"
  accessTypeParam: "<YOUR-ACCESS-KEY-HERE>"
```

<ApiKeyWarning />

#### Kubernetes Auth Example

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: akeyless-k8s-creds
  namespace: akeyless-demo
type: Opaque
stringData:
  accessId: "<p-k8saccessid>"
  accessType: "k8s"
  accessTypeParam: "<my-k8s-auth-config-name>"
```

* `accessId`: Access ID for the **Kubernetes Auth** method.
* `accessTypeParam`: Name of the Kubernetes Auth config for the cluster.

#### Azure AD Example (Managed Identity or Service Principal)

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: akeyless-azure-creds
  namespace: akeyless-demo
type: Opaque
stringData:
  accessId: "<p-xxxxx>"
  accessType: "azure_ad"
  accessTypeParam: ""              # Optional: Azure Object ID; can be left empty if using sub-claims such as xms_mirid
```

This Secret is suitable when using Azure AD Managed Identity with sub-claim enforcement.

> ℹ️ **Note:** ESO does not implement Azure Workload Identity flows internally. When `accessType: azure_ad` is used, ESO relies entirely on the Azure AD token available in the pod’s environment. This is typically projected by way of AKS Workload Identity. Therefore, the identity ESO uses depends on the `ServiceAccount` the `ExternalSecret` runs under, not on the `SecretStore`.

### `SecretStore`: Namespaced Secret Provider

#### `SecretStore` (Using a Credentials Secret)

Create a `SecretStore` resource which defines how ESO connects to Akeyless within a single Namespace.

```yaml
apiVersion: external-secrets.io/v1
kind: SecretStore
metadata:
  name: akeyless-secret-store
  namespace: akeyless-demo
spec:
  provider:
    akeyless:
      # Public SaaS API
      akeylessGWApiURL: "https://api.akeyless.io"
      # ignoreCache: true  # bypass Gateway cache when using an Akeyless Gateway URL
      authSecretRef:
        secretRef:
          accessID:
            name: akeyless-secret-creds
            key: accessId
          accessType:
            name: akeyless-secret-creds
            key: accessType
          accessTypeParam:
            name: akeyless-secret-creds
            key: accessTypeParam
```

If using a **private Akeyless Gateway** (for example in a zero-knowledge or hybrid deployment), set:

```yaml
      akeylessGWApiURL: "https://<the.akeyless.gw>:8000/api/v2"
```

Custom CAs can be configured by way of `caBundle` or `caProvider` if the Akeyless Gateway uses a private CA.

#### `SecretStore` (Direct Kubernetes Auth)

Alternatively, Kubernetes Auth can be configured directly in the `SecretStore` without a generic credentials Secret.

```yaml
apiVersion: external-secrets.io/v1
kind: SecretStore
metadata:
  name: akeyless-k8s-secret-store
  namespace: akeyless-demo
spec:
  provider:
    akeyless:
      akeylessGWApiURL: "https://api.akeyless.io"
      authSecretRef:
        kubernetesAuth:
          accessID: "p-k8saccessid"
          k8sConfName: "my-k8s-auth-config-name"
          serviceAccountRef:
            name: "akeyless-demo-sa"
          # Optional: Use a specific Secret containing a ServiceAccount JWT
          secretRef:
            name: "akeyless-demo-sa-token"
            key: "token"
```

##### Key Fields

* `accessID`: Access ID of the Kubernetes Auth Method.
* `k8sConfName`: Kubernetes Auth config name attached to the cluster.
* `serviceAccountRef`: `ServiceAccount` that ESO uses to request and project tokens.
* `secretRef`: Optional; explicit Secret containing a SA token ESO should use.

### `ClusterSecretStore`: Cluster-Wide Secret Provider

A `ClusterSecretStore` is a cluster-scoped provider configuration that can be used by `ExternalSecret` resources in any Namespace.

```yaml
apiVersion: external-secrets.io/v1
kind: ClusterSecretStore
metadata:
  name: akeyless-cluster-secret-store
spec:
  provider:
    akeyless:
      akeylessGWApiURL: "https://api.akeyless.io"
      authSecretRef:
        secretRef:
          accessID:
            name: akeyless-secret-creds
            key: accessId
            namespace: akeyless-demo
          accessType:
            name: akeyless-secret-creds
            key: accessType
            namespace: akeyless-demo
          accessTypeParam:
            name: akeyless-secret-creds
            key: accessTypeParam
            namespace: akeyless-demo
```

For a `ClusterSecretStore` object, the Namespace fields are required for `secretRef.accessID`, `secretRef.accessType`, and `secretRef.accessTypeParam` (and for any `serviceAccountRef` or `secretRef` when using the Kubernetes authentication method).

When using `ClusterSecretStore`, the referencing `ExternalSecret` must set `secretStoreRef` to use the `ClusterSecretStore` as opposed to a `SecretStore`:

```yaml
secretStoreRef:
  kind: ClusterSecretStore
  name: akeyless-cluster-secret-store
```

Remember that any Namespace using this `ClusterSecretStore` must be authorized in the Akeyless Platform with appropriate roles and claims.

***

## `ExternalSecret`: Syncing Akeyless Secrets Into Kubernetes

To fetch an Akeyless secret and store it as a Kubernetes Secret, define an `ExternalSecret` resource.

### Basic `ExternalSecret` (Single Values)

```yaml
apiVersion: external-secrets.io/v1
kind: ExternalSecret
metadata:
  name: akeyless-external-secret
  namespace: akeyless-demo
spec:
  refreshInterval: 1h

  secretStoreRef:
    kind: SecretStore
    name: akeyless-secret-store

  target:
    name: app-config-secret
    creationPolicy: Owner

  data:
    - secretKey: api-key
      remoteRef:
        key: /path/to/the/secret/api-key
    - secretKey: db-password
      remoteRef:
        key: /path/to/the/secret/db-password
```

* `refreshInterval`: How often ESO refreshes values from Akeyless.
* `secretStoreRef`: Which `SecretStore` or `ClusterSecretStore` to use.
* `target.name`: Name of the Kubernetes Secret created.
* `data[*].secretKey`: Key name inside the Kubernetes Secret.
* `data[*].remoteRef.key`: Full path of the item in Akeyless.
* `ignoreCache`: Fetch the secret directly from SaaS without cache involved.

Retrieve values:

```shell
kubectl get secret app-config-secret -n akeyless-demo -o jsonpath='{.data.api-key}' | base64 -d
```

### Using `dataFrom` to Extract JSON

If an Akeyless secret contains JSON, `dataFrom.extract` can be used to split that JSON into multiple keys in the Kubernetes Secret.

```yaml
apiVersion: external-secrets.io/v1
kind: ExternalSecret
metadata:
  name: akeyless-external-secret-json
  namespace: akeyless-demo
spec:
  refreshInterval: 1h

  secretStoreRef:
    kind: SecretStore
    name: akeyless-secret-store

  target:
    name: app-config-json
    creationPolicy: Owner

  dataFrom:
    - extract:
        key: /path/to/the/json-secret
```

If the JSON value in Akeyless is:

```json
{
  "username": "demo",
  "password": "s3cr3t"
}
```

Then the resulting Kubernetes Secret `app-config-json` will contain two keys: `username` and `password`.

To inspect all keys:

```shell
kubectl get secret app-config-json -o jsonpath='{.data}'
```

### Certificates: Splitting Certificate and Private Key

Akeyless certificate items typically contain separate PEM blocks for the certificate and private key. They can be mapped to `tls.crt` and `tls.key` in a Kubernetes TLS Secret.

```yaml
apiVersion: external-secrets.io/v1
kind: ExternalSecret
metadata:
  name: akeyless-tls-secret
  namespace: akeyless-demo
spec:
  refreshInterval: 1h

  secretStoreRef:
    kind: SecretStore
    name: akeyless-secret-store

  target:
    name: my-tls-secret
    creationPolicy: Owner
    template:
      type: kubernetes.io/tls

  data:
    - secretKey: tls.crt
      remoteRef:
        key: /path/to/the/certificate-item
        property: certificate_pem

    - secretKey: tls.key
      remoteRef:
        key: /path/to/the/certificate-item
        property: private_key_pem
```

Now `my-tls-secret` can be used with a Kubernetes `Ingress` or other resource expecting a TLS Secret.

***

## `PushSecret`: Push Kubernetes Secrets Into Akeyless

`PushSecret` is used to **push** local Kubernetes Secrets into Akeyless, enabling a GitOps-friendly workflow where Kubernetes becomes the source of truth for some secrets.

### Create a Local Kubernetes Secret

```shell
kubectl create secret generic --from-literal=cache-pass=mypassword k8s-created-secret -n akeyless-demo
```

### Define the `PushSecret` Resource

```yaml
apiVersion: external-secrets.io/v1alpha1
kind: PushSecret
metadata:
  name: push-secret
  namespace: akeyless-demo
spec:
  refreshInterval: 5s
  updatePolicy: Replace
  deletionPolicy: Delete

  secretStoreRefs:
    - name: akeyless-secret-store
      kind: SecretStore

  selector:
    secret:
      name: k8s-created-secret

  data:
    - match:
        remoteRef:
          remoteKey: eso-created/my-secret
```

#### Key Fields

* `refreshInterval`: How often ESO checks for changes in the Kubernetes Secret.
* `updatePolicy`: Whether to replace or merge when updating the provider secret.
* `deletionPolicy`: Whether to delete the provider secret when the `PushSecret` resource is deleted.
* `remoteKey`: Path where the secret will be stored in Akeyless.

Applying this manifest will create an Akeyless secret named `eso-created/my-secret` whose value is derived from `k8s-created-secret` (for example `{"cache-pass":"mypassword"}`).

***

## Azure AD Managed Identity: Sub-Claim Example

This section illustrates how to use **Azure AD Managed Identity** on AKS in combination with an Akeyless **Azure AD Authentication Method** that enforces **sub-claims**, such as `xms_mirid` (Managed Identity resource ID) and `oid` (user/object ID).

### Example: Akeyless Azure AD Auth Method With Sub-Claims

Below is a truncated example of an Azure AD Auth Method with **role associations** and **sub-claims** that bind the role to specific identities:

```json
{
  "name": "devops/azure/akeyless-azure-ad-auth",
  "auth_method_access_id": "p-xxxxx",
  "access_info": {
    "rules_type": "azure_ad",
    "force_sub_claims": true,
    "azure_ad_access_rules": {
      "issuer": "https://sts.windows.net/<tenant-id>/",
      "jwks_uri": "https://login.microsoftonline.com/common/discovery/keys",
      "bound_tenant_id": "<tenant-id>"
    }
  },
  "auth_method_roles_assoc": [
    {
      "role_name": "devops/devops-api-role",
      "auth_method_sub_claims": {
        "xms_mirid": [
          "/subscriptions/.../resourcegroups/.../providers/Microsoft.ManagedIdentity/userAssignedIdentities/identities"
        ]
      }
    },
    {
      "role_name": "devops/devops-api-role",
      "auth_method_sub_claims": {
        "oid": [
          "11108008-9999-abcd-1234-ab123456abc1"
        ]
      }
    },
    {
      "role_name": "devops/devops-api-role",
      "auth_method_sub_claims": {
        "xms_mirid": [
          "/subscriptions/.../userAssignedIdentities/UserAkeylessGWManagedID",
          "/subscriptions/.../userAssignedIdentities/identities"
        ]
      }
    }
  ]
}
```

In this configuration:

* `force_sub_claims: true` requires that **at least one sub-claim match** for access to be granted.
* `auth_method_sub_claims.xms_mirid` binds access to specific **user-assigned Managed Identities**.
* `auth_method_sub_claims.oid` can bind access to specific Azure AD identities (for example, human users or service principals).

The associated role `devops/devops-api-role` typically grants `read`, `list`, `create`, `update`, and `delete` capabilities on paths such as `/devops/` and `/SPIRE/`.

### Kubernetes Manifests for ESO Using Azure AD Auth

The following manifests show how to use the above Auth Method from an AKS cluster with ESO.

#### Credentials Secret (Azure AD)

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: akeyless-azure-creds
  namespace: app-test
type: Opaque
stringData:
  accessId: "p-xxxxx"
  accessType: "azure_ad" # Use Azure AD Auth Method
  accessTypeParam: ""      # Required field; can be empty when binding by way of sub-claims
```

#### SecretStore Referencing the Azure AD Credentials

```yaml
apiVersion: external-secrets.io/v1
kind: SecretStore
metadata:
  name: akeyless-store
  namespace: app-test
spec:
  provider:
    akeyless:
      akeylessGWApiURL: "https://api.akeyless.io"
      # Optional: use a specific ServiceAccount for ESO controller in this namespace
      serviceAccountRef:
        name: app-test
      authSecretRef:
        secretRef:
          accessID:
            name: akeyless-azure-creds
            key: accessId
          accessType:
            name: akeyless-azure-creds
            key: accessType
          accessTypeParam:
            name: akeyless-azure-creds
            key: accessTypeParam
```

#### ExternalSecret Consuming a Secret by way of the SecretStore

```yaml
apiVersion: external-secrets.io/v1
kind: ExternalSecret
metadata:
  name: app-api-secret
  namespace: app-test
spec:
  refreshInterval: 1h
  secretStoreRef:
    name: akeyless-store
    kind: SecretStore
  target:
    name: app-api-secret
    creationPolicy: Owner
  data:
    - secretKey: api-key
      remoteRef:
        key: /devops/static_secret_1
```

#### Retrieving the Synced Secret

```shell
kubectl -n app-test get secret app-api-secret -o jsonpath="{.data.api-key}" | base64 -d
```

This pattern ties together:

* AKS nodes or workloads using **Managed Identity**,
* An Akeyless **Azure AD Auth Method** with sub-claim constraints, and
* ESO as the consumer that syncs secrets into Kubernetes.

***

## Tutorial

For a hands-on walkthrough, check out our tutorial video on [Sync Secrets to Kubernetes with External Secrets Operator (ESO)](https://tutorials.akeyless.io/docs/sync-secrets-to-k8s-with-external-secrets-operator).
