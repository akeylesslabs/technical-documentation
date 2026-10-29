---
title: Akeyless Cert Manager Issuer
deprecated: false
hidden: false
metadata:
  robots: index
---
The [Akeyless cert-manager Issuer](https://github.com/akeyless-community/akeyless-cert-manager-issuer) is an [external issuer](https://cert-manager.io/docs/configuration/issuers/) for [cert-manager](https://cert-manager.io/docs/) that signs certificate requests from your Kubernetes (K8s) cluster using an Akeyless [PKI Certificate Issuer](https://docs.akeyless.io/docs/ssh-and-pkitls-certificates). It calls the Akeyless API directly.

<Callout icon="📘" theme="info">
  ### Info

  To use the cert-manager built-in Vault issuer with the Akeyless Gateway HashiCorp Vault Proxy instead, see [Cert Manager](https://docs.akeyless.io/docs/kubernetes-cert-manager).
</Callout>

## Prerequisites

- A Kubernetes cluster with [cert-manager](https://cert-manager.io/docs/installation/) installed.
- An [Akeyless Gateway](https://docs.akeyless.io/docs/gateway-overview) reachable from the cluster.
- A [PKI Certificate Issuer](https://docs.akeyless.io/docs/ssh-and-pkitls-certificates) that permits the DNS names you plan to request.
- An [Authentication Method](https://docs.akeyless.io/docs/access-and-authentication-methods) associated with an [Access Role](https://docs.akeyless.io/docs/rbac) that has `read` permission on the PKI Certificate Issuer. The issuer supports API Key, Kubernetes, AWS IAM, Azure AD, GCP, Universal Identity, and OAuth 2.0/JWT. This guide uses an [API Key](https://docs.akeyless.io/docs/auth-with-api-key) as an example.
- Docker and a container registry that your cluster can pull images from.

## Build and Push the Issuer Image

The repository does not publish a container image, so build it and push it to a registry that you own:

```shell Shell
git clone https://github.com/akeyless-community/akeyless-cert-manager-issuer.git
cd akeyless-cert-manager-issuer

docker login <Your_Registry>

docker build --platform linux/amd64 \
  -t <Your_Registry>/<Your_Repository>/akeyless-cert-manager-issuer:v0.1.0 \
  --build-arg VERSION=v0.1.0 .

docker push <Your_Registry>/<Your_Repository>/akeyless-cert-manager-issuer:v0.1.0
```

Where:

- `<Your_Registry>/<Your_Repository>` - Your registry location, for example `docker.io/<Your_DockerHub_User>`.
- `--platform linux/amd64` - Required when building on an ARM machine, such as an Apple Silicon Mac.

<Callout icon="🚧" theme="warn">
  ### Note

  Do not use the `ghcr.io/akeyless-community/...` image name from the repository README. Pushing to it requires write access to the `akeyless-community` GitHub organization.
</Callout>

## Install the Issuer Controller

Set your image in the install manifest, and install the CRDs and the controller:

```shell Shell
sed -i.bak 's#ghcr.io/akeyless-community/akeyless-cert-manager-issuer:v0.1.0#<Your_Registry>/<Your_Repository>/akeyless-cert-manager-issuer:v0.1.0#' deploy/production/install.yaml

kubectl apply -f deploy/crds/
kubectl apply -f deploy/production/install.yaml
```

Ensure the controller pods are running:

```shell Shell
kubectl get pods -n akeyless-cert-manager-system
```

## Create an AkeylessIssuer

Create a namespace and a `Secret` with your Auth Method credentials. This example uses an API Key:

```shell Shell
kubectl create namespace akeyless-certs

kubectl create secret generic akeyless-api-key -n akeyless-certs \
  --from-literal=access-id='<Access_ID>' \
  --from-literal=access-key='<Access_Key>'
```

Edit a configuration file for the issuer:

```yaml issuer.yaml
apiVersion: certmanager.akeyless.io/v1alpha1
kind: AkeylessIssuer
metadata:
  name: akeyless-pki
  namespace: akeyless-certs
spec:
  apiUrl: "https://<Your_Akeyless_GW_URL>/api/v2"
  certIssuerName: "/path/to/PKI_Cert_Issuer"
  auth:
    accessKey:
      secretRef:
        name: akeyless-api-key
```

Where:

- `apiUrl` - The Akeyless Gateway API v2 URL, without a trailing slash. If the Gateway runs in the same cluster, you can use its internal Service address, for example `http://<Gateway_Service>.<Gateway_Namespace>.svc.cluster.local:8000/api/v2`.
- `certIssuerName` - The full path of the PKI Certificate Issuer in Akeyless.
- `auth` - The authentication configuration. For other Auth Methods, replace `accessKey` with `kubernetes`, `awsIam`, `azureAd`, `gcp`, `universalIdentity`, or `jwt`. For the required fields of each method, see [Authentication methods](https://github.com/akeyless-community/akeyless-cert-manager-issuer/blob/main/docs/ENVIRONMENT-RECHECK.md#authentication-methods).

<Callout icon="📘" theme="info">
  ### Info

  To use one issuer across all namespaces, create an `AkeylessClusterIssuer` with the same `spec`, and create its Secret in the `akeyless-cert-manager-system` namespace.
</Callout>

Create the issuer and ensure it is ready:

```shell Shell
kubectl apply -f issuer.yaml
kubectl get akeylessissuer -n akeyless-certs
```

The successful output of the command:

```shell Shell
NAME           READY   REASON    AGE
akeyless-pki   True    Checked   15m
```

## Create a Certificate Request

Edit a configuration file for the certificate:

```yaml certificate.yaml
apiVersion: cert-manager.io/v1
kind: Certificate
metadata:
  name: demo-tls
  namespace: akeyless-certs
spec:
  secretName: demo-tls
  duration: 24h
  renewBefore: 8h
  commonName: demo-tls.akeyless-certs.svc.cluster.local
  dnsNames:
    - demo-tls.akeyless-certs.svc.cluster.local
  issuerRef:
    group: certmanager.akeyless.io
    kind: AkeylessIssuer
    name: akeyless-pki
```

Where:

- `secretName` - The Kubernetes Secret that will store the signed certificate.
- `commonName` and `dnsNames` - Must be permitted by the PKI Certificate Issuer.
- `issuerRef.group` - Must be `certmanager.akeyless.io`.

Create the certificate:

```shell Shell
kubectl apply -f certificate.yaml
```

## Approve the Certificate Request

cert-manager signs a `CertificateRequest` only after it is [approved](https://cert-manager.io/docs/usage/certificaterequest/#approval). By default, cert-manager does not auto-approve requests for external issuers.

Approve the request with [cmctl](https://cert-manager.io/docs/reference/cmctl/):

```shell Shell
kubectl get certificaterequest -n akeyless-certs
cmctl approve -n akeyless-certs demo-tls-1
```

<Callout icon="🚧" theme="warn">
  ### Note

  Every renewal creates a new `CertificateRequest` that also requires approval. To approve Akeyless requests automatically, add `akeylessissuers.certmanager.akeyless.io/*` and `akeylessclusterissuers.certmanager.akeyless.io/*` to the cert-manager Helm `approveSignerNames` value, or use [approver-policy](https://cert-manager.io/docs/policy/approval/approver-policy/).
</Callout>

## Verify the Certificate

```shell Shell
kubectl get certificate -n akeyless-certs
```

The successful output of the command:

```shell Shell
NAME       READY   SECRET     AGE
demo-tls   True    demo-tls   71s
```

The signed certificate and private key are stored in the `demo-tls` Secret.

## Troubleshooting

| Symptom                                                              | Resolution                                                                                                                  |
| :------------------------------------------------------------------- | :-------------------------------------------------------------------------------------------------------------------------- |
| Controller pods in `ImagePullBackOff`                                | Make sure `install.yaml` points to the image you pushed, and that the cluster can pull it.                                  |
| Issuer `Pending` with `undefined response type`                      | The `apiUrl` is wrong. Use the format `https://<Your_Akeyless_GW_URL>/api/v2`.                                              |
| Issuer `Pending` with `context deadline exceeded` or `403 Forbidden` | The cluster cannot reach the Gateway. Use the internal Gateway Service address, or allow the cluster in your network rules. |
| Issuer status does not update after a fix                            | Run `kubectl rollout restart deployment/akeyless-cert-manager-issuer -n akeyless-cert-manager-system`.                      |
| `CertificateRequest` failed after approval                           | Check `certIssuerName` and the permitted DNS names, then run `kubectl describe certificaterequest -n akeyless-certs`.       |