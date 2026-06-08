---
title: Kubernetes Auth Client Certificate
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
## Prerequisites

* [Akeyless Gateway](https://docs.akeyless.io/docs/gateway-overview) with network access to the Kubernetes (K8s) cluster.

* Kubernetes v1.21 or later.

> ℹ️ **Info:**
>
> To set Kubernetes Authentication method, make sure you have [Access Permissions](https://docs.akeyless.io/docs/gateway-authentication-and-access) on your Gateway to manage the Kubernetes Auth.
>
> Notice: Kubernetes Client certificate authentication is **not supported by EKS**.

## Client Certificate Authentication

Client certificate-based authentication using a dedicated Kubernetes user, instead of the bearer token flow, enables receiving notifications in advance of certificate expiration. This approach also follows Kubernetes best practices for auth strategies since no token is being exchanged as part of the flow directly with your cluster.

### Kubernetes Client Creation

Create a client key using a Certificate Signing Request (CSR):

```shell
export USER_NAME="AkeylessK8sAuth";
export GROUP="AkeylessAuth";
export GATEWAY_URL="https://<Your_Akeyless_GW_URL>:8000";
K8S_CSR=$(akeyless generate-csr -n /k8s/Clustername/csr/$USER_NAME --generate-key --alg RSA2048 --common-name $USER_NAME --gateway-url $GATEWAY_URL --org $GROUP --json --jq-expression ".data"| base64 | tr -d "\n")
USER_KEY=$(akeyless export-classic-key -n /k8s/Clustername/csr/$USER_NAME --jq-expression ".key" | base64)
```

Make sure to set the relevant `user_name` and `group` according to your convention.

Issue a client certificate from your Kubernetes cluster:

```yaml
cat <<EOF | kubectl apply -f -
apiVersion: certificates.k8s.io/v1
kind: CertificateSigningRequest
metadata:
  name: ${USER_NAME}
spec:
  groups:
  - system:authenticated
  request: ${K8S_CSR}
  signerName: kubernetes.io/kube-apiserver-client
  usages:
  - client auth
EOF
```

Approve the issued certificate, and upload it into Akeyless for future notifications about expiration:

```shell
kubectl certificate approve $USER_NAME
USER_CERT=$(kubectl get csr $USER_NAME -o jsonpath='{.status.certificate}')  
akeyless create-certificate --name /k8s/Clustername/certificates/$USER_NAME --certificate-data $USER_CERT --key-data $USER_KEY --expiration-event-in 30
```

### Kubernetes RoleBinding

Create the **Cluster RoleBinding** named `role-tokenreview-binding` for the user to review tokens:

```yaml akl_gw_token_reviewer.yaml
cat <<EOF | kubectl apply -f -
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: role-tokenreview-binding
  namespace: default
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: system:auth-delegator
subjects:
- kind: User
  name: ${USER_NAME}
  namespace: default
EOF
```

#### Extract Kubernetes Cluster CA Certificate

To extract the Kubernetes cluster CA cert. used to talk to the Kubernetes API, run the following command:

```shell kubectl
CA_CERT=$(kubectl config view --raw --minify --flatten \
    --output 'jsonpath={.clusters[].cluster.certificate-authority-data}')
```
```shell Rancher
CA_CERT=$(openssl s_client -host <Rancher Server> -port 443 2>&1  | sed -n -e '/-----BEGIN CERTIFICATE-----/,/-----END CERTIFICATE-----/ p' | base64)
```

#### Create Kubernetes Auth Method

Use the [Akeyless CLI](https://docs.akeyless.io/docs/cli) to create the Kubernetes Auth Method. The result will output an `Access ID` and `private key` that you will need later for the Kubernetes auth configuration in your [Gateway](https://docs.akeyless.io/docs/gateway-overview):

```shell
akeyless auth-method create k8s -n my-k8s-auth-method --json
```

Upon successful creation, the response:

```shell
{
  "access_id": "p-abcdefg1234",
  "prv_key": "LS0tLS1CRUdJTiBSUlNDUUxt.....QVRFIEtFWS0tLS0tCg=="
}
```

> ℹ️ **Note:**
>
> Save the returned `AccessID` and private key for next steps inside environment variables `$PRV_KEY` and `$ACCESS_ID`.
>
> If the private key is lost, generate a new key pair on the same Kubernetes Auth Method:
>
> ```shell
> akeyless auth-method update k8s --name my-k8s-auth-method --gen-key true --json
> ```
>
> Update each Kubernetes Auth config that uses this Auth Method with the new private key before authenticating.

#### Create Kubernetes Gateway Auth Config Using Certificates

To [discover your Kubernetes ServiceAccount issuer](https://kubernetes.io/docs/tasks/configure-pod-container/configure-service-account/#service-account-issuer-discovery) run the following command:

> ℹ️ **Note:**
>
> The Kubernetes Issuer parameter is no longer used by default, as the issuer validation is done by the API server, if you still wish to work with local issuer validation open a new tab to run this command as it starts a server. Then, go back to your original tab to extract the issuer.

Forwarding the Kubernetes API:

```shell Issuer Discovery
kubectl proxy --api-prefix=/k8s-api
```

Extract the issuer:

```shell Issuer Discovery
K8S_ISSUER=$(curl -s http://localhost:8001/k8s-api/.well-known/openid-configuration | jq -r .issuer)
```

Or extract the issuer directly from your pod token:

```shell Issuer Discovery
K8S_ISSUER=$(jq -R 'split(".") | .[1] | @base64d | fromjson |.iss' <<< $(cat /var/run/secrets/kubernetes.io/serviceaccount/token) -r)
```

Use the Akeyless CLI to create the Kubernetes auth config using the Client Certificate.

```shell Native Kubernetes
akeyless gateway-create-k8s-auth-config 
--name k8s-conf \
--gateway-url https://<Your_Akeyless_GW_URL>:8000 \
--access-id $ACCESS_ID \
--signing-key $PRV_KEY \
--k8s-auth-type certificate \
--k8s-host https://<Your_Kubernetes_Cluster_IP>:8443 \
--k8s-client-certificate $USER_CERT \
--k8s-client-key $USER_KEY \
--k8s-ca-cert $CA_CERT \
--k8s-issuer $K8S_ISSUER
```

Where:

* `name`: The config name (will be used during the authentication process).

* `gateway-url`: Akeyless Gateway URL (port `8000`).

* `access-id`: The `Access ID` of the Kubernetes Auth Method that was created.

* `signing-key`: The private key (Base64-encoded) associated with the public key defined in the Kubernetes auth (The private key that was created when the Kubernetes Auth Method was created previously).

* `k8s-auth-type`: Kubernetes auth type, use `certificate`.

* `k8s-host`: The URL of your **Kubernetes Cluster**.

* `k8s-client-certificate`: The client's certificate in `PEM` format and `base64` encoding.

* `k8s-client-key`: The client's private key in `PEM` format and `base64` encoding.

* `k8s-ca-cert`: The certificate to validate the Kubernetes cluster.

* `k8s-issuer`: Optional, the [Kubernetes JWT issuer name](https://kubernetes.io/docs/tasks/configure-pod-container/configure-service-account/#service-account-issuer-discovery) (default is `kubernetes/serviceaccount`).

Upon successful creation, the response:

```shell
K8S Auth config k8s-conf successfully created. ID=[UqeOAkg4UDo...bpv52Iq]
```

## Authenticate from a Pod in Your Kubernetes Cluster

1. Create a Namespace in your Kubernetes cluster:

    ```shell
    kubectl create namespace my-namespace-a
    ```

2. In this Namespace, create a pod:

    ```shell
    kubectl run mypod1 --image=nginx -n my-namespace-a
    ```

3. Start an interactive shell session on the pod and perform the following commands in the pod:

    ```shell
    kubectl exec --stdin=true --namespace my-namespace-a --tty=true mypod1 -- /bin/sh
    ```

4. Install Akeyless CLI inside your pod:

    ```shell
    curl -o akeyless https://akeyless-cli.s3.us-east-2.amazonaws.com/cli/latest/production/cli-linux-amd64
    chmod +x akeyless
    ./akeyless configure
    ```

5. Authenticate by way of your Kubernetes Auth Method:

    ```shell
    ./akeyless auth --access-id $ACCESS_ID \
        --access-type k8s \
        --gateway-url https://<Your_Akeyless_GW_URL>:8000 \
        --k8s-auth-config-name k8s-conf
    ```

Where:

* `access-id`: The `Access ID` of the Kubernetes Auth Method that was created.

* `access-type`: The Auth Method access type: `k8s`.

* `gateway-url`: Akeyless Gateway URL (port `8000`).

* `k8s-auth-config-name`: The Kubernetes auth config name in your [Gateway](https://docs.akeyless.io/docs/gateway-overview).

Upon successful authentication, the response will be:

```shell
Authentication succeeded.
Token: t-bb7b...3564a7c9
```

> ℹ️ **Note:**
>
> Delete the private key and Access ID that you stored in environment variables `$PRV_KEY` and `$ACCESS_ID`.

## Available Claims for Kubernetes Auth

The following list of claims can be configured within Akeyless [Role-Based Access Control (RBAC)](https://docs.akeyless.io/docs/rbac) to control and segregate the relevant policy for Kubernetes.

```yaml
"service_account_name"
"service_account_uid"
"service_account_secret_name"
"namespace"
"aud"
"pod_name" # available only when "token request projection" is enabled on your Kubernetes cluster
"pod_uid" # available only when "token request projection" is enabled on your Kubernetes cluster
```

Each claim can be enforced as part of your role association to enforce the right policy for your items.

## Enable Token Request Projection on Minikube

To enable token request projection on a managed Kubernetes cluster you can follow [this](https://kubernetes.io/docs/tasks/configure-pod-container/configure-service-account/#serviceaccount-token-volume-projection) guide.

To get this to work with Minikube you can start your cluster with the following configuration.

```shell
minikube start \
    --vm-driver=none \
    --extra-config=apiserver.service-account-signing-key-file=/var/lib/minikube/certs/sa.key \
    --extra-config=apiserver.service-account-key-file=/var/lib/minikube/certs/sa.pub \
    --extra-config=apiserver.service-account-issuer=api \
    --extra-config=apiserver.service-account-api-audiences=api,spire-server \
    --extra-config=apiserver.authorization-mode=Node,RBAC \
    --extra-config=kubelet.authentication-token-webhook=true
```

> ℹ️ **Note:**
>
> This example uses `api` as the ServiceAccount issuer name, for your ServiceAccounts API audience.
