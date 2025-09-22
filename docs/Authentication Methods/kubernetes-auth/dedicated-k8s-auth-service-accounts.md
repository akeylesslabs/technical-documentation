---
title: Dedicated K8s Service Accounts
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

* [Akeyless Gateway](doc:api-gw) with network access to the Kubernetes (K8s) cluster.

* `K8s v1.21` or later.

> 📘 Info
>
> **Required Gateway Access Permissions**
>
> To set K8s Authentication method, make sure you have [Access Permissions](https://docs.akeyless.io/docs/gateway-k8s#gateway-admins) on your Gateway to manage the K8s Auth.

# Dedicated ServiceAccount

This flow describes the creation of a dedicated K8s ServiceAccount which will work based on token projection. 

For a Rancher cluster, please create your [Rancher API Key](https://rancher.com/docs/rancher/v2.5/en/user-settings/api-keys/) and refer to [Extract K8s Cluster CA Certificate](doc:kubernetes-auth#extract-k8s-cluster-ca-certificate) to extract your Rancher server CA certificate. 

> 👍 Note
>
> To enable and use token request projection on a self-managed cluster, you must specify each of the following command line arguments to kube-apiserver:\
>  `--service-account-issuer`\
>  `--service-account-key-file`\
>  `--service-account-signing-key-file`\
>  `--api-audiences`
>
> For more details, check out the [minikube configuration example](https://docs.akeyless.io/docs/kubernetes#enable-token-request-projection-on-minikube) at the end of this page.

1. Create a ServiceAccount named `gateway-token-reviewer` with permission to access token review API. This ServiceAccount will be used to validate a K8s `JWT` coming from a pod that will try to authenticate to Akeyless.

```yaml akl_gw_token_reviewer.yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: gateway-token-reviewer
  namespace: default
---
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
- kind: ServiceAccount
  name: gateway-token-reviewer
  namespace: default
```

Apply:

```shell CLI
kubectl apply -f akl_gw_token_reviewer.yaml
```

### Bearer Token Extraction for K8s Server v1.23 or lower

2. Extract the `gateway-token-reviewer` ServiceAccount secret name: 

```shell
GW_SA_NAME=$(kubectl get sa gateway-token-reviewer \
    --output jsonpath="{.secrets[*]['name']}")
```

3. Extract the ServiceAccount `JWT` Bearer Token (K8s Server \<= v1.23):

```shell
SA_JWT_TOKEN=$(kubectl get secret $GW_SA_NAME \
    --output 'go-template={{ .data.token | base64decode }}')
```

### Bearer Token Extraction for K8s Server v1.24 or higher

K8s won’t generate Secrets automatically for ServiceAccounts, to get your ServiceAccount token, run the following commands instead:

2. Create the long-lived ServiceAccount secret called `gateway-token-reviewer-token` (K8s Server >= v1.24):

```yaml akl_gw_token_reviewer_token.yaml
apiVersion: v1
kind: Secret
metadata:
  name: gateway-token-reviewer-token
  namespace: default
  annotations:
    kubernetes.io/service-account.name: gateway-token-reviewer
type: kubernetes.io/service-account-token
```

```shell
kubectl apply -f akl_gw_token_reviewer_token.yaml
```

3. Extract the ServiceAccount `JWT` Bearer Token (K8s Server >= v1.24):

```shell
SA_JWT_TOKEN=$(kubectl get secret gateway-token-reviewer-token \
  --output 'go-template={{.data.token | base64decode}}')
```

### Extract K8s Cluster CA Certificate

To extract the K8s cluster CA cert used to talk to K8s API run the following command:

```shell K8s
CA_CERT=$(kubectl config view --raw --minify --flatten  \
    --output 'jsonpath={.clusters[].cluster.certificate-authority-data}')
```
```shell Rancher
CA_CERT=$(openssl s_client -host <Rancher Server> -port 443 2>&1  | sed -n -e '/-----BEGIN CERTIFICATE-----/,/-----END CERTIFICATE-----/ p' | base64)
```

### Create K8s Auth Method

1. Use the [Akeyless CLI](https://docs.akeyless.io/docs/cli) to create the K8s auth method. The result contains an `access Id` and a `private key` that you will need later for the K8S Auth configuration in your [Akeyless Gateway](https://docs.akeyless.io/docs/api-gw):

```shell Akeyless CLI
akeyless create-auth-method-k8s -n my-k8s-auth-method --json
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
> Save returned private key & AccessID for next steps inside an environment variables  `$PRV_KEY` and `$ACCESS_ID`.

### Create K8s Gateway Auth Config Using Bearer Tokens

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

Use the Akeyless CLI to create the K8S auth config:

```shell Native K8s Cluster
akeyless gateway-create-k8s-auth-config --name k8s-conf \
--gateway-url https://<Your_Akeyless_GW_URL:8000> \
--access-id $ACCESS_ID \
--signing-key $PRV_KEY \
--k8s-host https://<Your_K8s_Cluster_IP:8443> \
--token-reviewer-jwt $SA_JWT_TOKEN \
--k8s-ca-cert $CA_CERT \
--k8s-issuer $K8S_ISSUER
```
```shell Rancher
akeyless gateway-create-k8s-auth-config --name k8s-conf-rancher \
--gateway-url https://<Your_Akeyless_GW_URL:8000> \
--access-id $ACCESS_ID \
--signing-key $PRV_KEY \
--cluster-api-type rancher \
--k8s-host https://<Rancher Host:443> \
--k8s-ca-cert $CA_CERT \
--k8s-issuer $K8S_ISSUER \
--rancher-api-key <API_KEY_bearer_token> \
--rancher-cluster-id <CLUSTER_ID> \
```

Where:

* `name`: The config name (will be used during the authentication process).

* `gateway-url`:  Akeyless Gateway Configuration Manager URL (port `8000`).

* `access-id`: The `Access Id` of the K8s auth method that was created.

* `signing-key`: The private key (base64 encoded) associated with the public key defined in the K8s auth\
  (The private key that was created when the K8s auth method was created previously).

* `k8s-host`: The URL of your **K8s API server** or your **Rancher server**.

* `token-reviewer-jwt`: The ServiceAccount `JWT` used to access the `TokenReview` API\
  (relevant only to `native_k8s` access type).

* `k8s-ca-cert`: The certificate to use to validate the K8s cluster.

* `k8s-issuer`: Optional, the[ Kubernetes JWT issuer name](https://kubernetes.io/docs/tasks/configure-pod-container/configure-service-account/#service-account-issuer-discovery) (default is `kubernetes/serviceaccount`).

When the cluster access type is **Rancher**, add the following parameters:\
(in addition to the relevant parameters above)

* `cluster-api-type`: Cluster access type, we will write `rancher` (default is `native_k8s`).
* `rancher-api-key`: Rancher **Bearer token**, based on the created Rancher [API Key](https://rancher.com/docs/rancher/v2.5/en/user-settings/api-keys/).
* `rancher-cluster-id`: Rancher Cluster ID, i.e., your Rancher API Key Scope.

# Authenticate from a pod in your K8s cluster

1. Create a namespace in your k8s cluster:

```shell CLI
kubectl create namespace my-namespace-a
```

2. In this namespace create a pod:

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

5. Authenticate via your Kubernetes auth method with the following parameters:

```shell Akeyless CLI
./akeyless auth --access-id $ACCESS_ID \
    --access-type k8s \
    --gateway-url https://<Your_Akeyless_GW_URL:8000> \
    --k8s-auth-config-name k8s-conf
```

Where:

* `access-id`: The `Access Id` of the K8s auth method that was created previously.

* `access-type`: The Auth Method access type, `k8s`.

* `gateway-url`:  Akeyless Gateway Configuration Manager URL (port `8000`).

* `k8s-auth-config-name`: The K8s auth config name in your [Gateway](https://docs.akeyless.io/docs/api-gw).

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
"pod_name"  # available only when "token request projection" is enabled on your Kubernetes cluster
"pod_uid"   # available only when "token request projection" is enabled on your Kubernetes cluster
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
> This example uses `api` as the service account issuer name, for your service accounts API audience.

# Tutorial

Check out our tutorial video on [Kubernetes Authentication](https://tutorials.akeyless.io/docs/kubernetes-authentication).
