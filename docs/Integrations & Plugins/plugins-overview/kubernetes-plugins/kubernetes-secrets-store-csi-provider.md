---
title: K8s Secrets Store CSI Driver
excerpt: Kubernetes Secrets Store Container Storage Interface (CSI) Driver
deprecated: false
hidden: false
metadata:
  title: ''
  description: ''
  robots: index
next:
  description: ''
---
[Secrets Store CSI Driver ](https://github.com/kubernetes-sigs/secrets-store-csi-driver) for K8s secrets - Integrates secret stores with K8s via a Container Storage Interface (CSI) volume.

The Secrets Store CSI Driver `secrets-store.csi.k8s.io` allows K8s to mount multiple secrets, keys, and certs stored in enterprise-grade external secrets stores into their pods as a volume. Once the volume is attached, the data is mounted into the container's file system.

> 👍 Note
>
> K8s Secrets Store CSI Provider supports Static Secrets, Rotated Secrets and Certificates

[Akeyless provider](https://github.com/akeylesslabs/akeyless-csi-provider) for the Secrets Store CSI driver allows you to fetch existing secrets that are stored in Akeyless and use the Secrets Store CSI driver interface to mount them into K8s pods.

Similar to K8s secrets, upon pod start, the Secrets Store CSI driver communicates with the provider using gRPC to retrieve the secret content from the external Secrets Store specified in the `SecretProviderClass` custom resource.

Then the volume is mounted in the pod as `tmpfs` and the secret value is written to the volume.\
Upon pod deletion, the corresponding volume is cleaned up and deleted.

# Prerequisites

* K8s v1.16 or higher.

* [Secrets store CSI driver](https://secrets-store-csi-driver.sigs.k8s.io/getting-started/installation.html) installed.

* [TokenRequest](https://kubernetes-csi.github.io/docs/token-requests.html) enabled.

# Install Akeyless CSI Provider

Using helm

```shell
helm repo add akeyless https://akeylesslabs.github.io/helm-charts
helm install akeyless-csi akeyless/akeyless-csi-provider
```

Or via local `yaml` file which located under `deployment` folder on this [git](https://github.com/akeylesslabs/akeyless-csi-provider).

```shell
kubectl apply -f deployment/akeyless-csi-provider.yaml
```

# SecretProviderClass

The `SecretProviderClass` is a namespaced resource in Secrets Store CSI Provider that is used to provide configurations and provider-specific parameters to the CSI provider.

Supported [Authentication Methods](doc:access-and-authentication-methods) :

* [API Key](doc:api-key)  
* [Kubernetes (K8s)](doc:kubernetes-auth) 
* [AWS IAM](doc:aws-iam) 
* [Azure AD](doc:azure-ad) 
* [GCP](doc:gcp-auth-method) 

`SecretProviderClass` custom resource should state the `akeylessAccessType`-  which can be one of the supported [Authentication Methods](doc:access-and-authentication-methods) : `access_key`, `aws_iam`, `azure_ad`, `gcp`, `universal_identity`. 

While using `k8s`,`azure_ad`, or `gcp` , the following parameters should be provided accordingly:

`akeylessK8sAuthConfigName`,`akeylessAzureObjectID` or `akeylessGCPAudience`.

Example of a `SecretProviderClass` resource:

```yaml API Key
apiVersion: secrets-store.csi.x-k8s.io/v1
kind: SecretProviderClass
metadata:
  name: akeyless-test
spec:
  provider: akeyless
  parameters:
    akeylessGatewayURL: "https://api.akeyless.io"
    akeylessAccessID: "Access Id"
    akeylessAccessKey: "Access Key"
    akeylessAccessType: "access_key"
    objects:  |
      - secretPath: "/path/to/secret/foo"
        fileName: "foo"
      - secretPath: "/path/to/secret/bar"
        fileName: "bar"
```
```yaml K8s
apiVersion: secrets-store.csi.x-k8s.io/v1
kind: SecretProviderClass
metadata:
  name: akeyless-test
spec:
  provider: akeyless
  parameters:
    akeylessGatewayURL: "https://<Your GW URL>:8081"
    akeylessAccessID: "Access Id"
    akeylessAccessType: "k8s"
    akeylessK8sAuthConfigName: "k8s-conf"
    objects:  |
      - secretPath: "/path/to/secret/foo"
        fileName: "foo"
      - secretPath: "/path/to/secret/bar"
        fileName: "bar"
```
```yaml AWS IAM
apiVersion: secrets-store.csi.x-k8s.io/v1
kind: SecretProviderClass
metadata:
  name: akeyless-test
spec:
  provider: akeyless
  parameters:
    akeylessGatewayURL: "https://api.akeyless.io"
    akeylessAccessID: "Access Id"
    akeylessAccessType: "aws_iam"
    objects:  |
      - secretPath: "/path/to/secret/foo"
        fileName: "foo"
      - secretPath: "/path/to/secret/bar"
        fileName: "bar"
```
```yaml Azure AD
apiVersion: secrets-store.csi.x-k8s.io/v1
kind: SecretProviderClass
metadata:
  name: akeyless-test
spec:
  provider: akeyless
  parameters:
    akeylessGatewayURL: "https://api.akeyless.io"
    akeylessAccessID: "Access Id"
    akeylessAzureObjectID: "<Azure ObjectId>" #When using workload identity and you wish to use the default credentials, leave this field empty
    akeylessAccessType: "azure_ad"
    objects:  |
      - secretPath: "/path/to/secret/foo"
        fileName: "foo"
      - secretPath: "/path/to/secret/bar"
        fileName: "bar"
```
```yaml GCP
apiVersion: secrets-store.csi.x-k8s.io/v1
kind: SecretProviderClass
metadata:
  name: akeyless-test
spec:
  provider: akeyless
  parameters:
    akeylessGatewayURL: "https://api.akeyless.io"
    akeylessAccessID: "<Access Id>"
    akeylessGCPAudience: "akeyless.io"
    akeylessAccessType: "gcp"
    objects:  |
      - secretPath: "/path/to/secret/foo"
        fileName: "foo"
      - secretPath: "/path/to/secret/bar"
        fileName: "bar"
```

> 🚧 Warning
>
> Using Access Key within `YAML` files is not secure. You can provide the `AKEYLESS_ACCESS_KEY` as an environment variable instead.

Reference the `SecretProviderClass` inside the pod deployment volumes when using the CSI driver:

```yaml test-csi-pod.yaml
apiVersion: v1
kind: Pod
metadata:
  name: test-csi
spec:
  containers:
  - image: alpine
    name: alpine
    command:
      - "sh"
      - "-c"
      - "echo going to sleep... && sleep 10000"
    volumeMounts:
    - name: secrets-store-inline
      mountPath: "/akeyless-secrets"
      readOnly: true
  volumes:
    - name: secrets-store-inline
      csi:
        driver: secrets-store.csi.k8s.io
        readOnly: true
        volumeAttributes:
          secretProviderClass: "akeyless-test"
```

> 🚧 Warning
>
> The `SecretProviderClass` needs to be created in the same namespace as the pod.

After the pod is created, the secret can be found inside the pod, under the `mountPath` - within the `fileName`
