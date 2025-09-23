---
title: Cert Manager
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
# Overview

[Cert-Manager](https://cert-manager.io/docs/) generates certificate requests from the Kubernetes (K8s) cluster to Akeyless and simplifies the process of obtaining, renewing, and using those certificates.

The process of generating a certificate request from a K8s cluster to Akeyless is divided into three steps:

* Generating **Authentication Token** either using an [API Key](doc:api-key) or using [Kubernetes](doc:kubernetes-auth) ServiceAccount token  -  This token will be used for authenticating to Akeyless. 
* Configuring an **Issuer** - A K8s resource that represents the Certificate Authority (CA).
* Configuring the **Certificate Signing Request (CSR)** - A file that contains the data for the certificate

Once all of the above are set, **CSR** will be generated to Akeyless from the K8s Cluster, then, the certificate will be issued by the [PKI Issuer](https://docs.akeyless.io/docs/ssh-and-pkitls-certificates).

# Prerequisites

* [Cert-Manager](https://cert-manager.io/docs/installation/) installed
* A [Kubernetes](https://docs.akeyless.io/docs/kubernetes-auth) or an [API Key](https://docs.akeyless.io/docs/api-key) Auth Method attached to a role with `read` permission for **Items**
* [PKI Issuer](https://docs.akeyless.io/docs/ssh-and-pkitls-certificates)

Create a namespace called `akeyless-cert-manager`:

```shell
kubectl create ns akeyless-cert-manager
```

## K8s Auth Method

**Cert-Manager** authenticates to Akeyless using a K8s **ServiceAccount token**, which is being generated using [Secretless Authentication with a Service Account](https://cert-manager.io/docs/configuration/vault/#secretless-authentication-with-a-service-account) - **Available in Cert-Manager >= v1.12.0**

> 📘 Info
>
> **Authentication with a Static ServiceAccount Token** - For **Cert-Manager** with a lower version than v1.12.0, you can use "[Authentication with a Static ServiceAccount Token](https://cert-manager.io/docs/configuration/vault/#static-service-account-token)" for authentication.

Using **Secretless Authentication** with a ServiceAccount, a temporary ServiceAccount token is created, **Cert-Manager** uses this ServiceAccount token to authenticate.

In order to create the ServiceAccount token, edit a configuration file that will contain a  **ServiceAccount** with a **Role** and **Role Binding** allowing K8s token creation:

```yaml k8s_sa.yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: akeyless-issuer
  namespace: akeyless-cert-manager
  
---
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: akeyless-issuer
  namespace: akeyless-cert-manager
rules:
  - apiGroups: ['']
    resources: ['serviceaccounts/token']
    resourceNames: ['akeyless-issuer']
    verbs: ['create']

---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: akeyless-issuer
  namespace: akeyless-cert-manager
subjects:
  - kind: ServiceAccount
    name: cert-manager
    namespace: cert-manager
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: Role
  name: akeyless-issuer
```

Create the  **ServiceAccount** :

```shell
kubectl apply -f k8s_sa.yaml
```

Once the ServiceAccount is created, an **Issuer** needs to be created as well. An **Issuer** is a K8s resource that represents the CA, in our case, **Akeyless**.

> 👍 Note
>
> With an **Issuer** resource, you can only refer to a ServiceAccount located in the same namespace as the Issuer, for more information refer to [this](https://cert-manager.io/docs/configuration/vault/#:~:text=Issuer%20vs.%20ClusterIssuer%3A) link.

In order to create the `Issuer` resource, edit a configuration file that will contain the data of your Akeyless environment with a reference to the `ServiceAccount` which we created in the previous step:

```yaml issuer.yaml
apiVersion: cert-manager.io/v1
kind: Issuer
metadata:
  name: akeyless-issuer
  namespace: akeyless-cert-manager
spec:
  vault:
    path: /pki/sign/dev/Pki_Cert_Issuer 
    server: <https://Your_Akeyless_GW_URL:8000/hvp> # Or using port 8200
    auth:
      kubernetes:
        role: <"base64 encoding of access_id..k8s_auth_config_name">
        mountPath: /v1/auth/kubernetes
        serviceAccountRef:
          name: akeyless-issuer # The ServiceAccount that was created earlier
```

Where:

* `path` - The path to the [PKI Certificate Issuer](https://docs.akeyless.io/docs/ssh-and-pkitls-certificates) in Akeyless, where `/pki/sign/` is a **mandatory** prefix. In our example, the PKI Issuer name is  `Pki_Cert_Issuer` which is  located under `/dev/` folder 
* `server` - The URL of the [Akeyless Gateway](https://docs.akeyless.io/docs/api-gw) HVP endpoint `https://Your_Akeyless_GW_URL:8000/hvp` (or using your gateway url at port 8200)
* `role` - `<Access-ID..K8s Auth Config Name>` in base64 encoded format. Note the K8s Auth config name can be found in the Gateway config-manager (port 8000), under the "Kubernetes Auth" menu.

> 📘 Info
>
> **Base64 encoding** - The following command can be used for base64 conversion: `echo -n '<Access-ID..K8s Auth Config Name>' | base64`.

Create the Issuer:

```shell
kubectl apply -f issuer.yaml
```

At this stage, all the configuration for K8s authentication is set and it is possible to proceed to the next step to  [create the certificate request](https://docs.akeyless.io/docs/kubernetes-cert-manager#create-a-certificate-request).

## API Key Auth Method

In order to use an [API Key](https://docs.akeyless.io/docs/api-key) Auth Method for generating certificate requests from the K8s cluster to Akeyless, An **Authentication Token** is required.

The **Authentication Token** will be created using a `Secret` resource which will hold the `Access-Key` of the API Key Auth Method.

Edit a configuration file that will contain the data for the **Authentication Token**:

```yaml secret_token.yaml
apiVersion: v1
kind: Secret
type: Opaque
metadata:
  name: cert-manager-api-key
  namespace: akeyless-cert-manager
data:
  secretId: <Access Key base64 encoded> 
```

Where: 

* `secretId` - The `Access-Key` of the **API Key** Auth Method base64 encoded format

Create the **Authentication Token**:

```shell
kubectl apply -f secret_token.yaml
```

Once the **Authentication Token** is created, an Issuer needs to be created as well. An Issuer is a K8s resource that represents the CA, in our case, **Akeyless**.

In order to create the Issuer, edit a configuration file that will contain the data of your Akeyless environment with a reference to the `secret`:

```yaml issuer.yaml
apiVersion: cert-manager.io/v1
kind: Issuer
metadata:
  name: akeyless-issuer
  namespace: akeyless-cert-manager
spec:
  vault:
    path: /pki/sign/dev/Pki_Cert_Issuer 
    server: <http://<Your_Akeyless_GW_URL:8200> # HVP address
    auth:
      appRole:
        path: approle
        roleId: <"Access ID">
        secretRef:
          name: cert-manager-api-key
          key: secretId
```

Where:

* `path` - The path to the [PKI Certificate Issuer](https://docs.akeyless.io/docs/ssh-and-pkitls-certificates) in Akeyless, where `/pki/sign/` is a **mandatory** prefix, in our example, the PKI Issuer name is  `Pki_Cert_Issuer` which is  located under `/dev/` folder
* `server` - The URL of the Akeyless Gateway on port `8200`
* `roleId` - `Access-ID`  of the **API Key** Auth Method

Create the Issuer:

```shell
kubectl apply -f issuer.yaml
```

# Create a certificate request

Ensure the Issuer is successfully created:

```shell
kubectl get issuer akeyless-issuer -n akeyless-cert-manager
```

The successful output of the command:

```shell
NAME              READY    AGE
akeyless-issuer   True    4d21h
```

Once the issuer is running, a certificate request can be generated. In order to do this, a `Certificate` resource needs to be created. 

Within the `certificate` resource file, information about the certificate itself will be defined, it will also be referenced to the `issuer` resource file that was created, which will call Akeyless to issue the certificate using the [PKI Issuer](https://docs.akeyless.io/docs/ssh-and-pkitls-certificates).

Edit a configuration file that will contain the data for the certificate request:

```yaml certificate.yaml
apiVersion: cert-manager.io/v1
kind: Certificate
metadata:
  name: demo-certificate
  namespace: akeyless-cert-manager
spec:
  secretName: demo-certificate
  commonName: <my.domain.com>
  # DNS SAN
  dnsNames:
    - example.domain.com
  # Duration of the certificate
  duration: 24h
  renewBefore: 8h
  issuerRef:
    kind: Issuer
    name: akeyless-issuer
```

Where:

* `secretName` - The secret name in **K8s** to store the signed certificate
* `commonName` - The **Common Name** that will be attached to the certificate

Create the certificate request:

```shell
kubectl apply -f certificate.yaml
```

To make sure the certificate was successfully created, run the following command:

```shell
kubectl describe certificate -n akeyless-cert-manager
```

The successful output of the command:

```shell
 Normal  Reused     3m4s (x2 over 2d22h)   cert-manager-certificates-key-manager      Reusing private key stored in existing Secret resource "demo-certificate"
 Normal  Issuing    3m4s                   cert-manager-certificates-trigger          Fields on existing CertificateRequest resource not up to date: [spec.duration]
 Normal  Requested  3m4s                   cert-manager-certificates-request-manager  Created new CertificateRequest resource "demo-certificate-sx7vf"
 Normal  Issuing    2m59s (x2 over 2d22h)  cert-manager-certificates-issuing          The certificate has been successfully issued
```

The certificate will be created under the directory that was defined in the **Storage Folder Location** field of the **PKI Issuer**
