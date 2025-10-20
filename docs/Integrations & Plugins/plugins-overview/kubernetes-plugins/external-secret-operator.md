---
title: External Secret Operator
excerpt: External Secrets Operator (ESO)
deprecated: false
hidden: false
metadata:
  title: ''
  description: ''
  robots: index
next:
  description: ''
---
[External Secrets Operator (ESO)](https://external-secrets.io/latest/provider/akeyless/) is a Kubernetes (K8s) operator that integrates with external secret management systems like Akeyless. The operator reads information from Akeyless APIs and automatically injects the values into a [Kubernetes Secret](https://kubernetes.io/docs/concepts/configuration/secret/).

The goal of the ESO is to synchronize secrets from Akeyless into Kubernetes. ESO is a collection of custom API resources - `ExternalSecret`, `SecretStore`, and `ClusterSecretStore` that provides a user-friendly abstraction for the external API that stores and manages the lifecycle of the secrets for you.

The ESO runs within your Kubernetes cluster as a `deployment` resource. It utilizes `CustomResourceDefinitions` to configure access to secret providers through `SecretStore` resources and manages Kubernetes secret resources with `ExternalSecret` resources.

You can use two types of resources to fetch secrets from Akeyless:

* [SecretStore](https://external-secrets.io/v0.5.5/api-secretstore/): Defines how to access secrets from Akeyless within a specific namespace.

* [ClusterSecretStore](http://external-secrets.io/v0.5.5/api-clustersecretstore/): Defines how to access secrets from Akeyless across the entire Kubernetes cluster.

In addition to retrieving secrets from Akeyless to your Kubernetes cluster, you can use the `PushSecret` resource to push a local Kubernetes secret from your cluster to Akeyless.

# Prerequisites

* [Helm ](https://helm.sh/) installed
* `K8s v1.16` or higher

# Installing with Helm

Add External Secrets [official repository](https://github.com/external-secrets/external-secrets) to your helm and install:

```shell CLI
helm repo add external-secrets https://charts.external-secrets.io
helm install external-secrets external-secrets/external-secrets
```

# Authentication

Akeyless official [provider](https://external-secrets.io/main/provider/akeyless/) support the following Auth Methods:

* [API Key](https://docs.akeyless.io/docs/api-key)
* [AWS IAM](https://docs.akeyless.io/docs/aws-iam)
* [Azure AD](https://docs.akeyless.io/docs/azure-ad)
* [GCP](https://docs.akeyless.io/docs/gcp-auth-method)
* [K8s](https://docs.akeyless.io/docs/kubernetes-auth)

> 👍 Note
>
> This guide demonstrates authentication using API Key and K8s Auth Methods. However, for security purposes, it’s highly recommended to avoid using API Keys in production.

To set an auth method for the external secret operator, first create a [K8s Secret](https://kubernetes.io/docs/concepts/configuration/secret/) with the relevant settings, for example:

```yaml API Auth
apiVersion: v1
kind: Secret
metadata:
  name: akeyless-secret-creds
type: Opaque
stringData:
  accessId: <Access ID>
  accessType: api_key
  accessTypeParam: <Access Key>
```
```yaml K8s Auth
apiVersion: v1
kind: Secret
metadata:
  name: akeyless-secret-creds
type: Opaque
stringData:
  accessId: <Access ID>
  accessType: k8s
  accessTypeParam: <k8s-conf-name>
```

Where:

* `name`: A name for the Kubernetes secret to store the Authentication details.

* `accessId`: The Auth Method `Access ID`.

* `accessType`: The Auth method type.

* `accessTypeParam`:  `Access Key` for **API Key** or `k8s-conf-name` for **K8s**. For more options, check the official [provider ](https://external-secrets.io/v0.5.9/provider-akeyless/#authentication) docs.

Apply the configuration:

```shell CLI
kubectl apply -f akeylesscreds.yaml
```

# SecretStore

The [SecretStore](https://external-secrets.io/v0.4.2/api-secretstore/) resource is namespaced and defines how to authenticate to Akeyless. In the following example, a reference to the `akeyless-secret-creds` that was created earlier is used.

Set the **SecretStore** resource:

```yaml secretstore.yaml
apiVersion: external-secrets.io/v1
kind: SecretStore
metadata:
  name: akeyless-secret-store
spec:
  provider:
    akeyless:
      akeylessGWApiURL: "https://api.akeyless.io"
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

Where:

* `akeylessGWApiURL`: The URL of your Gateway API v2 endpoint: `https://Your-Gateway-URL:8000/api/v2`. (or using your gateway url at port `8081`)

* `authSecretRef`: References a Kubernetes Secret `akeyless-secret-creds` containing authentication credentials.

* `secretRef`: Refers to a Kubernetes Secret named `akeyless-secret-creds`, which contains values for `accessID`, `accessType`, and `accessTypeParam`.

Apply the configuration:

```shell shell
kubectl apply -f secretstore.yaml
```

## Explicit Secret Store

Authentication with Akeyless can be done using credentials stored in the `akeyless-secret-creds` Kubernetes secret through the [SecretStore](https://docs.akeyless.io/docs/external-secret-operator-copy#secretstore). Alternatively, you can authenticate directly using your Kubernetes Auth settings.

Using an explicit secret store provides key benefits for access control and security. By segregating secrets based on service accounts, you can ensure that each service account only has access to the secrets it needs.

```yaml secretstore.yaml
apiVersion: external-secrets.io/v1
kind: SecretStore
metadata:
  name: akeyless-secret-store
spec:
  provider:
    akeyless:
      akeylessGWApiURL: "https://api.akeyless.io"
      authSecretRef:
        kubernetesAuth:
          accessID: <AccessID>
          k8sConfName: <K8s Conf Name>
          serviceAccountRef:
            name: <ServiceAccount Name>
```

Where:

* `accessId`: The Kubernetes Auth Method `Access ID`.

* `k8sConfName`: The name of the **K8s Conf** on the Gateway.

* `serviceAccountRef`: The name of the Kubernetes service account used to fetch secrets from Akeyless. Only secrets defined in a role associated with that service account under claim `service_account_name` can be accessed.

# ExternalSecret

To retrieve a secret from Akeyless and store it as a [Kubernetes secret](https://kubernetes.io/docs/concepts/configuration/secret/) in your cluster, create an [ExternalSecret](https://external-secrets.io/latest/api/externalsecret/) resource that specifies which secret to fetch:

```yaml externalsecret.yaml
apiVersion: external-secrets.io/v1
kind: ExternalSecret
metadata:
  name: akeyless-external-secret-example
spec:
  refreshInterval: 1h

  secretStoreRef:
    kind: SecretStore 
    name: akeyless-secret-store 

  target:
    name: akeyless-secret-to-create 
    creationPolicy: Owner

  data:
    - secretKey: secretKey 
      remoteRef:
        key: /path/to/your/secret 
```

Where:

* `refreshInterval`: The amount of time before the values are read again

* `secretStoreRef`: Reference to the `SecretStore`  that was created earlier, in case of `ClusterSecretStore`  set the `Kind`  to `ClusterSecretStore`

* `target`: Name of the Kubernetes secret to create.

* `secretKey`: The key of the secret that will be created locally in the Kubernetes cluster.

* `key`: Full path to the secret in Akeyless

Apply the configuration:

```text CLI
kubectl apply -f externalsecret.yaml
```

Getting the Kubernetes secret:

```shell CLI
kubectl get secret akeyless-secret-to-create -o jsonpath='{.data.secretKey}' | base64 -d
```

# Using DataFrom

DataFrom can be used to get a secret as a `JSON` string and attempt to parse it, where each key will be used as the secret key in the [Kubernetes Secret](https://kubernetes.io/docs/concepts/configuration/secret/):

```yaml datafrom.yaml
apiVersion: external-secrets.io/v1
kind: ExternalSecret
metadata:
  name: akeyless-external-secret-example-json
spec:
  refreshInterval: 1h

  secretStoreRef:
    kind: SecretStore 
    name: akeyless-secret-store 

  target:
    name: akeyless-secret-to-create-json 
    creationPolicy: Owner

  dataFrom:
  - extract:
      key: /path/to/your/secret/keyname 
```

Where:

* `refreshInterval`: The amount of time before the values are read again

* `secretStoreRef`: Reference to the `SecretStore`.

* `target`: Name of the Kubernetes secret to create.

* `key`: Full path to the secret in Akeyless

Getting the Kubernetes secret:

```yaml shell
kubectl get secret akeyless-secret-to-create-json -o jsonpath='{.data}'
```

## Working with Certificates

Another example is when working with Akeyless [Certificate](https://docs.akeyless.io/docs/certificate-storage), the certificate item contains two separate `PEM` blocks, the actual `Certificate` and the `Private Key`, to split them into different keys you can configure the resource accordingly:

```yaml externalsecret.yaml
apiVersion: external-secrets.io/v1
kind: ExternalSecret
metadata:
  name: akeyless-external-secret-example
spec:
  refreshInterval: 1h

  secretStoreRef:
    kind: SecretStore 
    name: akeyless-secret-store 

  target:
    name: akeyless-secret-to-create 
    creationPolicy: Owner

  data:
    - secretKey: tls.crt
      remoteRef:
        key: /path/to/your/secret 
        property: certificate_pem

    - secretKey: tls.key
      remoteRef:
        key: /path/to/your/secret 
        property: private_key_pem
```

Where:

* `refreshInterval`: The amount of time before the values are read again

* `secretStoreRef`: Reference to the `SecretStore`.

* `target`: Name of the Kubernetes secret to create.

* `secretKey`: The Secret keys that will be created.

* `key`: Full path to the secret in Akeyless

* `Property`: The existing keys of the secret as stored in Akeyless.

Apply the configuration:

```shell CLI
kubectl apply -f externalsecret.yaml
```

Getting the Kubernetes secret:

```shell Certificate
kubectl get secret akeyless-secret-to-create -o jsonpath='{.data.tls\.crt}' | base64 -d 
```
```shell Private Key
kubectl get secret akeyless-secret-to-create -o jsonpath='{.data.tls\.key}' | base64 -d 
```

# ClusterSecretStore

The [ClusterSecretStore](https://external-secrets.io/v0.4.2/api-clustersecretstore/) is cluster-wide and can be accessed by `ExternalSecrets` from any namespace, offering centralized secret management:

> 👍 Note
>
> The **namespace** value is required in the `secretRef` section.

Set the **ClusterSecretStore** resource:

```yaml clustersecretstore.yaml
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
            namespace: <namespace>
          accessType:
            name: akeyless-secret-creds
            key: accessType
            namespace: <namespace>
          accessTypeParam:
            name: akeyless-secret-creds
            key: accessTypeParam
            namespace: <namespace>
```

Where:

* `akeylessGWApiURL`: The URL of your Gateway API v2 endpoint: `https://Your-Gateway-URL:8000/api/v2`  (or using your gateway url at port `8081`).

* `authSecretRef`: Reference to the  [Kubernetes Secret](https://kubernetes.io/docs/concepts/configuration/secret/) that holds the authentication details, in our example  `akeyless-secret-creds`.

Run the following command to create the **ClusterSecretStore** resource:

```shell
kubectl apply -f clustersecretstore.yaml
```

# Push Secret

The [PushSecret](https://external-secrets.io/latest/api/pushsecret/) resource is namespaced and is used to push secrets from your Kubernetes Cluster to Akeyless.

Let's create a local Kubernetes secret in the cluster, which will then be pushed to Akeyless:

```shell
kubectl create secret generic --from-literal=cache-pass=mypassword k8s-created-secret
```

Upon successful secret creation, a Kubernetes secret named `k8s-created-secret` will be created in your cluster.

Next, we will create the `PushSecret` resource, which will be used to push the `k8s-created-secret` Kubernetes Secret, to Akeyless:

```yaml pushsecret.yaml
apiVersion: external-secrets.io/v1alpha1
kind: PushSecret
metadata:
  name: push-secret
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

Where:

* `refreshInterval`: The amount of time before the values are read again

* `secretStoreRef`: Reference to the `SecretStore`

* `updatePolicy`: Policy to overwrite existing secrets in the provider on sync

* `deletePolicy`: The provider secret will be deleted if the `PushSecret` is deleted

* `remoteKey` The location within the provider where the secret will be stored

Apply the configuration:

```shell
kubectl apply -f pushsecret.yaml
```

Upon successful execution, a secret named `k8s-created-secret` will be created in Akeyless, with the value of `cache-pass=mypassword`

# Tutorial

Check out our tutorial video on [Sync Secrets to Kubernetes with External Secrets Operator (ESO)](https://tutorials.akeyless.io/docs/sync-secrets-to-k8s-with-external-secrets-operator).
