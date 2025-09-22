---
title: K8s Auth Client Certificate
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
# Prerequisites

- [Akeyless Gateway](doc:api-gw) with network access to the Kubernetes (K8s) cluster.

- `K8s v1.21` or later.

> 📘 Info
> 
> To set K8s Authentication method, make sure you have [Access Permissions](https://docs.akeyless.io/docs/gateway-k8s#gateway-admins) on your Gateway to manage the K8s Auth. 
> 
> Notice: K8s Client certificate authentication is **not supported by EKS**.

# Client Certificate Authentication

Client certificate-based authentication using a dedicated K8s user, instead of the bearer token flow, enables receiving notifications in advance of certificate expiration. This approach also follows K8s best practices for auth strategies since no token is being exchanged as part of the flow directly with your cluster. 

## K8s Client Creation

Create a client key using a Certificate Signing Request (CSR): 

```shell
export USER_NAME="AkeylessK8sAuth";
export GROUP="AkeylessAuth";
export GATEWAY_URL="https://<Your_Akeyless_GW_URL:8000>";
K8S_CSR=$(akeyless generate-csr -n /k8s/Clustername/csr/$USER_NAME --generate-key --alg RSA2048 --common-name $USER_NAME --gateway-url $GATEWAY_URL --org $GROUP --json --jq-expression ".data"| base64 | tr -d "\n")
USER_KEY=$(akeyless export-classic-key -n /k8s/Clustername/csr/$USER_NAME --jq-expression ".key" | base64)
```

Make sure to set the relevant `user_name` and `group` according to your convention.

Issue a client certificate from your K8s cluster:

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

## K8s Role Binding

Create the **Cluster Role Binding** named `role-tokenreview-binding` for the user to review tokens:

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

### Extract K8s Cluster CA Certificate

To extract the K8s cluster CA cert. used to talk to the K8s API, run the following command:

```shell K8s
CA_CERT=$(kubectl config view --raw --minify --flatten  \
    --output 'jsonpath={.clusters[].cluster.certificate-authority-data}')
```
```shell Rancher
CA_CERT=$(openssl s_client -host <Rancher Server> -port 443 2>&1  | sed -n -e '/-----BEGIN CERTIFICATE-----/,/-----END CERTIFICATE-----/ p' | base64)
```

### Create K8s Auth Method

1. Use the [Akeyless CLI](https://docs.akeyless.io/docs/cli) to create the K8s auth method. The result will output an `Access ID` and `private key` that you will need later for the K8s auth configuration in your [Gateway](https://docs.akeyless.io/docs/api-gw):

```shell Akeyless CLI
akeyless auth-method create k8s -n my-k8s-auth-method  --json
```

Upon successful creation, the response:

```shell
{
  "access_id": "p-abcdefg1234",
  "prv_key": "LS0tLS1CRUdJTiBSUlNDUUxt.....QVRFIEtFWS0tLS0tCg=="
}
```

> 👍 Note
> 
> Save the returned Access ID & private key for next steps inside environment variables `$PRV_KEY` and `$ACCESS_ID`.

### Create K8s Gateway Auth Config Using Certificates

To [discover your K8s service account issuer](https://kubernetes.io/docs/tasks/configure-pod-container/configure-service-account/#service-account-issuer-discovery) run the following command:

> 👍 Note
> 
> The K8s Issuer parameter is no longer used by default, as the issuer validation is done by the API server, if you still wish to work with local issuer validation open a new tab to run this command as it starts a server. Then, go back to your original tab to extract the issuer.

Forwarding the K8s API:

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

Use the Akeyless CLI to create the K8s auth config using the Client Certificate. 

```shell Native K8s
akeyless gateway-create-k8s-auth-config 
--name k8s-conf \
--gateway-url https://<Your_Akeyless_GW_URL:8000> \
--access-id $ACCESS_ID \
--signing-key $PRV_KEY \
--k8s-auth-type certificate \
--k8s-host https://<Your_K8s_Cluster_IP:8443> \
--k8s-client-certificate $USER_CERT \
--k8s-client-key $USER_KEY \
--k8s-ca-cert $CA_CERT \
--k8s-issuer $K8S_ISSUER
```

Where:

- `name`: The config name (will be used during the authentication process).

- `gateway-url`:  Akeyless Gateway Configuration Manager URL (port `8000`).

- `access-id`: The `Access ID` of the K8s auth method that was created.

- `signing-key`: The private key (base64 encoded) associated with the public key defined in the K8s auth  
  (The private key that was created when the K8s auth method was created previously).

- `k8s-auth-type`: K8S auth type, use `certificate`.

- `k8s-host`: The URL of your **K8s Cluster**.

- `k8s-client-certificate`: The client's certificate in `PEM` format and `base64` encoding. 

- `k8s-client-key`: The client's private key in `PEM` format and `base64` encoding.

- `k8s-ca-cert`: The certificate to validate the K8s cluster.

- `k8s-issuer`: Optional ,the[ Kubernetes JWT issuer name](https://kubernetes.io/docs/tasks/configure-pod-container/configure-service-account/#service-account-issuer-discovery) (default is `kubernetes/serviceaccount`).

Upon successful creation, the response: 

```shell
K8S Auth config k8s-conf successfully created. ID=[UqeOAkg4UDo...bpv52Iq]
```

# Authenticate from a pod in your K8s cluster

1. Create a namespace in your k8s cluster:

```shell CLI
kubectl create namespace my-namespace-a
```

2. In this namespace, create a pod:

```shell CLI
kubectl run mypod1 --image=nginx -n my-namespace-a
```

3. Start an interactive shell session on the pod and perform the following commands in the pod:

```shell CLI
kubectl exec --stdin=true --namespace my-namespace-a  --tty=true mypod1 -- /bin/sh
```

4. Install Akeyless CLI inside your pod:

```shell CLI
curl -o akeyless https://akeyless-cli.s3.us-east-2.amazonaws.com/cli/latest/production/cli-linux-amd64
chmod +x akeyless
./akeyless --init
```

5. Authenticate via your K8s auth method :

```shell Akeyless CLI
./akeyless auth --access-id $ACCESS_ID \
    --access-type k8s \
    --gateway-url https://<Your_Akeyless_GW_URL:8000> \
    --k8s-auth-config-name k8s-conf
```

Where:

- `access-id`: The `Access Id` of the Kubernetes auth method that was created.

- `access-type`: The Auth Method access type, i.e. `k8s`.

- `gateway-url`:  Akeyless Gateway Configuration Manager URL (port `8000`).

- `k8s-auth-config-name`: The K8s auth config name in your [Gateway](https://docs.akeyless.io/docs/api-gw).

Upon successful authentication, the response will be:

```shell
Authentication succeeded.
Token: t-bb7b...3564a7c9
```

> 👍 Note
> 
> Delete the private key and Access ID which you stored as an environment variables `$PRV_KEY` and `$ACCESS_ID`

# Available claims for K8s Auth

The following list of claims can be configured within Akeyless [Role-based Access Control (RBAC)](doc:rbac) to control and segregate the relevant policy for K8s. 

```yaml
"service_account_name"
"service_account_uid"
"service_account_secret_name"
"namespace"
"aud"
"pod_name"  # available only when "token request projection" is enabled on your K8s cluster
"pod_uid"   # available only when "token request projection" is enabled on your K8s cluster
```

Each claim can be enforced as part of your role association to enforce the right policy for your items.

# Enable token request projection on Minikube

To enable token request projection on a managed K8s cluster you can follow [this](https://kubernetes.io/docs/tasks/configure-pod-container/configure-service-account/#serviceaccount-token-volume-projection) guide. 

To get this to work with Minikube you can start your cluster with the following configuration. 

```shell CLI
minikube start \
    --vm-driver=none \
    --extra-config=apiserver.service-account-signing-key-file=/var/lib/minikube/certs/sa.key \
    --extra-config=apiserver.service-account-key-file=/var/lib/minikube/certs/sa.pub \
    --extra-config=apiserver.service-account-issuer=api \
    --extra-config=apiserver.service-account-api-audiences=api,spire-server \
    --extra-config=apiserver.authorization-mode=Node,RBAC \
    --extra-config=kubelet.authentication-token-webhook=true
```

> 👍 Note
> 
> This example uses `api` as the ServiceAccount issuer name, for your ServiceAccounts API audience.