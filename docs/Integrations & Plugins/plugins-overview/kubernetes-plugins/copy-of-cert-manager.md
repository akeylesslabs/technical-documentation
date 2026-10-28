---
title: Copy of Cert Manager
deprecated: false
hidden: true
metadata:
  robots: index
---
## Overview

The [Akeyless cert-manager Issuer](https://github.com/akeyless-community/akeyless-cert-manager-issuer) is an [external issuer](https://cert-manager.io/docs/configuration/issuers/) for [cert-manager](https://cert-manager.io/docs/) that signs certificate requests from your Kubernetes (K8s) cluster using an Akeyless [PKI Certificate Issuer](https://docs.akeyless.io/docs/ssh-and-pkitls-certificates).

The issuer adds two Kubernetes resources:

- `AkeylessIssuer` - A namespaced issuer that can sign certificates for `Certificate` resources in its own namespace.
- `AkeylessClusterIssuer` - A cluster-scoped issuer that can sign certificates for `Certificate` resources in any namespace.

The issuance flow works as follows:

1. A `Certificate` resource is created in the cluster, and cert-manager generates a `CertificateRequest` that contains a PKCS#10 CSR.
2. Once the `CertificateRequest` is **approved**, the issuer controller authenticates to the [Akeyless Gateway](https://docs.akeyless.io/docs/gateway-overview) using the `/auth` endpoint.
3. The controller sends the CSR to the `/get-pki-certificate` endpoint, and the certificate is signed by the [PKI Certificate Issuer](https://docs.akeyless.io/docs/ssh-and-pkitls-certificates).
4. cert-manager stores the signed certificate and private key in a Kubernetes `Secret`.

<Callout icon="📘" theme="info">
  ### Info

  This guide covers the dedicated Akeyless external issuer, which calls the Akeyless API directly. Akeyless also supports these cert-manager integrations:

  - **Vault issuer** - Uses the cert-manager built-in [Vault issuer](https://cert-manager.io/docs/configuration/vault/) with the Akeyless Gateway HashiCorp Vault Proxy. See [Cert Manager](https://docs.akeyless.io/docs/kubernetes-cert-manager).
  - **ACME issuer** - Uses the cert-manager built-in [ACME issuer](https://cert-manager.io/docs/configuration/acme/) with External Account Binding, when the [ACME Server](https://docs.akeyless.io/docs/acme-server) is enabled on your PKI Certificate Issuer. See [docs/ACME.md](https://github.com/akeyless-community/akeyless-cert-manager-issuer/blob/main/docs/ACME.md).
</Callout>

## Prerequisites

- A Kubernetes cluster with [cert-manager](https://cert-manager.io/docs/installation/) installed.
- An [Akeyless Gateway](https://docs.akeyless.io/docs/gateway-overview) that is reachable from the issuer controller pods.
- A [PKI Certificate Issuer](https://docs.akeyless.io/docs/ssh-and-pkitls-certificates) that permits the DNS names (Common Name and SANs) you plan to request.
- An [Authentication Method](https://docs.akeyless.io/docs/access-and-authentication-methods), for example an [API Key](https://docs.akeyless.io/docs/auth-with-api-key), associated with an [Access Role](https://docs.akeyless.io/docs/rbac) that has `read` permission on the PKI Certificate Issuer.
- [Docker](https://docs.docker.com/get-docker/) and access to a container registry that your cluster can pull images from.
- `kubectl` configured for your cluster.
- (Optional) [cmctl](https://cert-manager.io/docs/reference/cmctl/), the cert-manager command-line tool, for approving certificate requests.

<Callout icon="🚧" theme="warn">
  ### Note

  The PKI Certificate Issuer must be able to sign the exact names that appear in the CSR. For in-cluster names such as `<service>.<namespace>.svc.cluster.local`, use a private or internal CA. Public CAs reject these names.
</Callout>

## Build and Push the Issuer Image

The repository does not publish a ready-made container image, so you must build the image and push it to a registry that your cluster can pull from.

<Callout icon="🚧" theme="warn">
  ### Note

  The image name in the repository README, `ghcr.io/akeyless-community/akeyless-cert-manager-issuer`, belongs to the repository maintainers' registry, and pushing to it requires write access to the `akeyless-community` GitHub organization. Use a registry that you own instead.
</Callout>

Clone the repository:

```shell Shell
git clone https://github.com/akeyless-community/akeyless-cert-manager-issuer.git
cd akeyless-cert-manager-issuer
```

Log in to your registry:

```shell Shell
docker login <Your_Registry>
```

Build and push the image:

```shell Shell
docker build --platform linux/amd64 \
  -t <Your_Registry>/<Your_Repository>/akeyless-cert-manager-issuer:v0.1.0 \
  --build-arg VERSION=v0.1.0 .

docker push <Your_Registry>/<Your_Repository>/akeyless-cert-manager-issuer:v0.1.0
```

Where:

- `<Your_Registry>/<Your_Repository>` - The registry location your cluster can pull from, for example `docker.io/<Your_DockerHub_User>`, `ghcr.io/<Your_GitHub_User>`, or a cloud registry such as Google Artifact Registry, Amazon ECR, or Azure ACR.
- `--platform linux/amd64` - The repository `Dockerfile` compiles the controller for `amd64`. Setting the platform explicitly is required when building on an ARM machine, such as an Apple Silicon Mac.

<Callout icon="🚧" theme="warn">
  ### Note

  If the image repository is private, make sure the cluster can pull it. Either grant the nodes access to the registry, or create an `imagePullSecret` in the `akeyless-cert-manager-system` namespace and reference it in the Deployment.
</Callout>

## Install the Issuer Controller

Update the image reference in the install manifest to the image you pushed:

```shell Shell
sed -i.bak 's#ghcr.io/akeyless-community/akeyless-cert-manager-issuer:v0.1.0#<Your_Registry>/<Your_Repository>/akeyless-cert-manager-issuer:v0.1.0#' deploy/production/install.yaml

grep -n "image:" deploy/production/install.yaml
```

Install the Custom Resource Definitions (CRDs) and the controller:

```shell Shell
kubectl apply -f deploy/crds/
kubectl apply -f deploy/production/install.yaml
```

The `install.yaml` manifest creates the `akeyless-cert-manager-system` namespace, the required RBAC, a ServiceAccount, a metrics Service, and a Deployment with two replicas and leader election enabled.

Verify the CRDs and the controller pods:

```shell Shell
kubectl get crd akeylessissuers.certmanager.akeyless.io akeylessclusterissuers.certmanager.akeyless.io
kubectl get pods -n akeyless-cert-manager-system
```

The successful output of the command:

```shell Shell
NAME                                            READY   STATUS    RESTARTS   AGE
akeyless-cert-manager-issuer-54bd9495d9-4m874   1/1     Running   0          57s
akeyless-cert-manager-issuer-54bd9495d9-wmcvq   1/1     Running   0          42s
```

## Configure Authentication

Create a dedicated namespace for your issuer and certificates:

```shell Shell
kubectl create namespace akeyless-certs
```

### API Key Auth Method

Create a `Secret` that holds the `Access ID` and `Access Key` of the [API Key](https://docs.akeyless.io/docs/auth-with-api-key) Auth Method:

```shell Shell
kubectl create secret generic akeyless-api-key -n akeyless-certs \
  --from-literal=access-id='<Access_ID>' \
  --from-literal=access-key='<Access_Key>'
```

Where:

- `access-id` - The `Access ID` of the API Key Auth Method.
- `access-key` - The `Access Key` of the API Key Auth Method.

<Callout icon="🚧" theme="warn">
  ### Note

  The Secret keys must be named exactly `access-id` and `access-key`.
</Callout>

### Other Authentication Methods

The issuer supports one authentication configuration per issuer under `spec.auth`:

| Field                         | Akeyless Auth Method                                                             |
| :---------------------------- | :------------------------------------------------------------------------------- |
| `spec.auth.accessKey`         | [API Key](https://docs.akeyless.io/docs/auth-with-api-key)                       |
| `spec.auth.kubernetes`        | [Kubernetes](https://docs.akeyless.io/docs/auth-with-kubernetes)                 |
| `spec.auth.awsIam`            | [AWS IAM](https://docs.akeyless.io/docs/auth-with-aws)                           |
| `spec.auth.azureAd`           | [Azure AD](https://docs.akeyless.io/docs/auth-with-azure)                        |
| `spec.auth.gcp`               | [GCP](https://docs.akeyless.io/docs/auth-with-gcp)                               |
| `spec.auth.universalIdentity` | [Universal Identity](https://docs.akeyless.io/docs/auth-with-universal-identity) |
| `spec.auth.jwt`               | [OAuth 2.0/JWT](https://docs.akeyless.io/docs/auth-with-oauth-jwt)               |

For the required fields and Secrets for each method, see [docs/ENVIRONMENT-RECHECK.md](https://github.com/akeyless-community/akeyless-cert-manager-issuer/blob/main/docs/ENVIRONMENT-RECHECK.md#authentication-methods) in the repository.

## Create an AkeylessIssuer

Edit a configuration file that contains the data of your Akeyless environment, with a reference to the Secret that was created in the previous step:

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

- `apiUrl` - The Akeyless Gateway API v2 base URL, without a trailing slash. The controller appends paths such as `/auth` and `/get-pki-certificate` to this URL.
- `certIssuerName` - The full path of the [PKI Certificate Issuer](https://docs.akeyless.io/docs/ssh-and-pkitls-certificates) in Akeyless, without a trailing slash.
- `auth.accessKey.secretRef.name` - The name of the Secret that holds the API Key credentials.

<Callout icon="📘" theme="info">
  ### Info

  **Gateway in the same cluster** - If the Akeyless Gateway runs in the same Kubernetes cluster, you can use its internal Service address and avoid external network restrictions, for example:

  `http://<Gateway_Service_Name>.<Gateway_Namespace>.svc.cluster.local:8000/api/v2`

  To find the Gateway Service, run `kubectl get svc -A | grep -i akeyless`.
</Callout>

Before creating the issuer, you can verify that the Gateway API is reachable from inside the cluster. Run a temporary pod and call the `/auth` endpoint with only the Access ID:

```shell Shell
kubectl run nettest -n akeyless-certs --rm -it --restart=Never --image=curlimages/curl -- \
  curl -s -m 10 -X POST <apiUrl>/auth \
  -H 'Content-Type: application/json' \
  -d '{"access-type":"access_key","access-id":"<Access_ID>"}'
```

A JSON response, such as `{"error":"invalid request body: access key should not be empty"}`, confirms that the URL reaches the Akeyless API. An HTML response, an HTTP `403`, or a timeout indicates a wrong URL or a network restriction between the cluster and the Gateway.

Create the issuer:

```shell Shell
kubectl apply -f issuer.yaml
```

Ensure the issuer is ready:

```shell Shell
kubectl get akeylessissuer -n akeyless-certs
```

The successful output of the command:

```shell Shell
NAME           READY   REASON    AGE
akeyless-pki   True    Checked   15m
```

`READY True` indicates that the controller successfully authenticated to Akeyless.

### AkeylessClusterIssuer

To use a single issuer for `Certificate` resources in all namespaces, create an `AkeylessClusterIssuer` instead. It uses the same `spec` as `AkeylessIssuer`, but it is cluster-scoped. The Secret it references must be created in the namespace of the controller, `akeyless-cert-manager-system`, which is set by the `--cluster-resource-namespace` flag in `install.yaml`.

```yaml cluster-issuer.yaml
apiVersion: certmanager.akeyless.io/v1alpha1
kind: AkeylessClusterIssuer
metadata:
  name: akeyless-pki
spec:
  apiUrl: "https://<Your_Akeyless_GW_URL>/api/v2"
  certIssuerName: "/path/to/PKI_Cert_Issuer"
  auth:
    accessKey:
      secretRef:
        name: akeyless-api-key
```

When using an `AkeylessClusterIssuer`, set `issuerRef.kind` to `AkeylessClusterIssuer` in your `Certificate` resources.

## Create a Certificate Request

Once the issuer is ready, create a `Certificate` resource. The `Certificate` references the issuer, which calls Akeyless to issue the certificate using the [PKI Certificate Issuer](https://docs.akeyless.io/docs/ssh-and-pkitls-certificates).

Edit a configuration file that contains the data for the certificate request:

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

- `secretName` - The name of the Kubernetes Secret that will store the signed certificate and private key.
- `commonName` and `dnsNames` - The names to include in the certificate. The PKI Certificate Issuer must permit these names.
- `issuerRef.group` - Must be set to `certmanager.akeyless.io` for the Akeyless issuer.
- `issuerRef.kind` - `AkeylessIssuer` or `AkeylessClusterIssuer`.
- `issuerRef.name` - The `metadata.name` of the issuer resource.

Create the certificate request:

```shell Shell
kubectl apply -f certificate.yaml
kubectl get certificaterequest -n akeyless-certs
```

The output shows a new `CertificateRequest` that is waiting for approval:

```shell Shell
NAME         APPROVED   DENIED   READY   ISSUER         REQUESTER                                         AGE
demo-tls-1                               akeyless-pki   system:serviceaccount:cert-manager:cert-manager   14s
```

## Approve the Certificate Request

cert-manager requires every `CertificateRequest` to be [approved](https://cert-manager.io/docs/usage/certificaterequest/#approval) before it is signed. In a default installation, the cert-manager internal approver approves requests only for its built-in issuers, so requests for the Akeyless issuer must be approved explicitly.

### Manual Approval

Approve the request with [cmctl](https://cert-manager.io/docs/reference/cmctl/):

```shell Shell
cmctl approve -n akeyless-certs demo-tls-1
```

Alternatively, approve the request with `kubectl`:

```shell Shell
kubectl patch certificaterequest demo-tls-1 -n akeyless-certs \
  --subresource=status --type=merge \
  -p '{"status":{"conditions":[{"type":"Approved","status":"True","reason":"ManualApproval","message":"Approved manually via kubectl","lastTransitionTime":"'"$(date -u +%Y-%m-%dT%H:%M:%SZ)"'"}]}}'
```

<Callout icon="🚧" theme="warn">
  ### Note

  Each renewal creates a new `CertificateRequest`. With manual approval, every renewal must also be approved, otherwise the certificate is not renewed.
</Callout>

### Automatic Approval

To let the cert-manager internal approver approve Akeyless requests, add the Akeyless signer names to the `approveSignerNames` value of the cert-manager Helm chart (available in cert-manager v1.15.0 and later). Keep the built-in issuers in the list so they continue to be approved:

```yaml approve-values.yaml
approveSignerNames:
  - "issuers.cert-manager.io/*"
  - "clusterissuers.cert-manager.io/*"
  - "akeylessissuers.certmanager.akeyless.io/*"
  - "akeylessclusterissuers.certmanager.akeyless.io/*"
```

```shell Shell
helm upgrade cert-manager jetstack/cert-manager -n cert-manager --reuse-values -f approve-values.yaml
```

For production environments, consider a policy-based approver such as [approver-policy](https://cert-manager.io/docs/policy/approval/approver-policy/), which limits who can request which certificates. For more information, see [Approval Policy](https://cert-manager.io/docs/policy/approval/).

## Verify the Certificate

Ensure the certificate was issued:

```shell Shell
kubectl get certificaterequest -n akeyless-certs
kubectl get certificate -n akeyless-certs
```

The successful output of the command:

```shell Shell
NAME         APPROVED   DENIED   READY   ISSUER         REQUESTER                                         AGE
demo-tls-1   True                True    akeyless-pki   system:serviceaccount:cert-manager:cert-manager   65s

NAME       READY   SECRET     AGE
demo-tls   True    demo-tls   71s
```

Inspect the issued certificate:

```shell Shell
kubectl get secret demo-tls -n akeyless-certs -o jsonpath='{.data.tls\.crt}' | base64 -d | openssl x509 -noout -subject -issuer -dates
```

The `issuer` field shows the CA of your Akeyless PKI Certificate Issuer.

## Troubleshooting

| Symptom                                                                      | Cause                                                                                                                                            | Resolution                                                                                                                                                                                         |
| :--------------------------------------------------------------------------- | :----------------------------------------------------------------------------------------------------------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Controller pods in `ImagePullBackOff` with `401 Unauthorized` from `ghcr.io` | `install.yaml` still references the default image, which is not published.                                                                       | Build and push your own image, and update the image in `install.yaml`, or run `kubectl set image deployment/akeyless-cert-manager-issuer controller=<Your_Image> -n akeyless-cert-manager-system`. |
| Issuer `Pending` with `akeyless auth: undefined response type`               | The `apiUrl` does not point to the Akeyless API, so a non-JSON response is returned.                                                             | Verify the `apiUrl` format, for example `https://<Your_Akeyless_GW_URL>/api/v2`, with no trailing slash and the port attached directly to the host.                                                |
| Issuer `Pending` with `context deadline exceeded`                            | The controller pods cannot reach the Gateway on the configured host and port.                                                                    | Test connectivity from a pod in the cluster. If the Gateway runs in the same cluster, use its internal Service address.                                                                            |
| Issuer `Pending` with `403 Forbidden`                                        | A load balancer, ingress, or firewall in front of the Gateway blocks requests from the cluster, or the Auth Method restricts client IPs.         | Allow the cluster outbound IP, use the internal Gateway Service address, or review the Auth Method's allowed client IPs.                                                                           |
| Issuer status does not update after fixing the configuration                 | The controller is still waiting to retry an earlier failure.                                                                                     | Run `kubectl rollout restart deployment/akeyless-cert-manager-issuer -n akeyless-cert-manager-system`.                                                                                             |
| `CertificateRequest` has no `APPROVED` value                                 | The request has not been approved.                                                                                                               | Approve the request manually or configure automatic approval. See [Approve the Certificate Request](#approve-the-certificate-request).                                                             |
| `CertificateRequest` is `Failed` after approval                              | Akeyless rejected the signing request, for example because of a wrong `certIssuerName` or names that the PKI Certificate Issuer does not permit. | Run `kubectl describe certificaterequest <name> -n akeyless-certs` and check the controller logs. After fixing the configuration, run `cmctl renew <certificate-name> -n akeyless-certs`.          |

To view the controller logs:

```shell Shell
kubectl logs -n akeyless-cert-manager-system -l app.kubernetes.io/name=akeyless-cert-manager-issuer --tail=50
```

## Resources

- [akeyless-cert-manager-issuer repository](https://github.com/akeyless-community/akeyless-cert-manager-issuer)
- [Environment checklist and authentication methods](https://github.com/akeyless-community/akeyless-cert-manager-issuer/blob/main/docs/ENVIRONMENT-RECHECK.md)
- [cert-manager Issuers](https://cert-manager.io/docs/configuration/issuers/)
- [cert-manager CertificateRequest approval](https://cert-manager.io/docs/usage/certificaterequest/#approval)
- [PKI Certificate Issuer](https://docs.akeyless.io/docs/ssh-and-pkitls-certificates)
- [Cert Manager (Vault-compatible issuer)](https://docs.akeyless.io/docs/kubernetes-cert-manager)