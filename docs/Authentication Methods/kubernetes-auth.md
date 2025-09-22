---
title: Kubernetes
excerpt: Kubernetes (K8s)
deprecated: false
hidden: false
metadata:
  title: Kubernetes
  description: ''
  robots: index
next:
  description: ''
---
The Kubernetes (K8s) Auth Method uses K8s JWTs in order to authenticate the K8s application (e.g. a pod). Throughout the process, this K8s JWT is never shared with Akeyless or any other third party, but only with the [Akeyless Gateway](https://docs.akeyless.io/docs/api-gw) that is controlled and operated in the customer environment. It is therefore considered a trusted machine.

<Image align="center" src="https://files.readme.io/ecfb4eb-Akeyless_Rebranded_Infographics.png" />

# Prerequisites

* [Akeyless Gateway](doc:api-gw) with network access to the K8s cluster.

* `K8s v1.21` or later.

> 📘 Info
>
> **Required Gateway Access Permissions**
>
> To set K8s Authentication method, make sure you have [Access Permissions](https://docs.akeyless.io/docs/gateway-k8s#gateway-admins) on your Gateway to manage the K8s Auth

# Authentication Strategies

Akeyless supports several authentication strategies to interact with the K8s cluster. Each of the below links describes the entire flow of creating the Akeyless K8s Auth Method. Choose the one that works for you and follow the entire flow:

* The Akeyless Gateway ServiceAccount
* A [dedicated ServiceAccount ](https://docs.akeyless.io/docs/dedicated-k8s-auth-service-accounts)
* A [client certificate ](https://docs.akeyless.io/docs/k8s-auth-client-certificate)

> 📘 Info
>
> ServiceAccount approaches work based on K8s bearer tokens, whereas Certificate-based Authentication works based on a certificate and private key

# Using Akeyless Gateway ServiceAccount

In order to work with your Gateway Service Account the following K8s role should be assigned to the Service Account that runs your Gateway, Please make sure to adjust the `ServiceAccount:name` and `namespace` fields according to your environment: 

```yaml Gateway SA K8s Role
cat << EOF > akl_gw_sa_token_reviewer.yaml 
apiVersion: v1
kind: ServiceAccount
metadata:
  name: <Gateway SA Name>
  namespace: default
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: role-tokenreview-binding
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: system:auth-delegator
subjects:
- kind: ServiceAccount
  name: <Gateway SA Name>
  namespace: default 
EOF
```

Apply the changes: 

```shell
kubectl apply -f akl_gw_sa_token_reviewer.yaml
```

### Create K8s Auth Method

Use the [Akeyless CLI](https://docs.akeyless.io/docs/cli) to create the Kubernetes auth method, The result contains an `Access Id` and a `private key` that you will need later for the K8S Auth configuration in your [Gateway](https://docs.akeyless.io/docs/api-gw):

```shell Akeyless CLI
akeyless auth-method create k8s -n my-k8s-auth-method --json
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
> Save returned private key & AccessID for next steps inside an environment variables  `$PRV_KEY` and `$ACCESS_ID`

### Create K8s Gateway Auth Config Using Gateway ServiceAccount

Use the Akeyless CLI to create the K8S auth config:

```shell
akeyless gateway-create-k8s-auth-config  --name k8s-conf \
--gateway-url <https://Your-Akeyless-GW-URL>:8000 \
--access-id $ACCESS_ID \
--signing-key $PRV_KEY \
--use-gw-service-account
```

Where:

* `name`: The config name (will be used during the authentication process).

* `gateway-url`:  Akeyless Gateway Configuration Manager URL (port `8000`).

* `access-id`: The `Access Id` of the Kubernetes auth method that was created.

* `signing-key`: The private key (The key that was created when the Kubernetes auth method was created).

* `use-gw-service-account`: Extract all the relevant information using the Gateway Service Account.

# Authenticate from a pod in your K8s cluster

1. Create a namespace in your k8s cluster:

```shell
kubectl create namespace my-namespace-a
```

2. In this namespace, create a pod:

```shell
kubectl run mypod1 --image=nginx -n my-namespace-a
```

3. Start an interactive shell session on the pod and perform the following commands in the pod:

```shell
kubectl exec --stdin=true --namespace my-namespace-a  --tty=true mypod1 -- /bin/sh
```

4. Install Akeyless CLI inside your pod:

```shell
curl -o akeyless https://akeyless-cli.s3.us-east-2.amazonaws.com/cli/latest/production/cli-linux-amd64
chmod +x akeyless
./akeyless --init
```

5. Authenticate via your Kubernetes auth method as follows:

```shell
./akeyless auth --access-id $ACCESS_ID \
    --access-type k8s \
    --gateway-url https://<Your-GW-URL>:8000 \
    --k8s-auth-config-name k8s-conf
```

Where:

* `access-id`: The `Access Id` of the Kubernetes auth method that was created.

* `access-type`: the access type - `k8s`

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

The following list of claims can be configured within Akeyless [Access Roles (RBAC)](doc:rbac) to control and segregate the relevant policy for K8s. 

```yaml
"service_account_name"
"service_account_uid"
"service_account_secret_name"
"namespace"
"aud"
"pod_name"   # available only when "token request projection" is enabled on your Kubernetes cluster
"pod_uid"    # available only when "token request projection" is enabled on your Kubernetes cluster
"config_name" # The name of the k8s auth config used for kubernetes authentication appended to the JWT
```

Each claim can be enforced as part of your role association to enforce the right policy for your items.

# Enable token request projection on Minikube

To enable token request projection on a managed K8s cluster you can follow [this](https://kubernetes.io/docs/tasks/configure-pod-container/configure-service-account/#serviceaccount-token-volume-projection) guide. 

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

> 👍 Note
>
> This example uses `api` as the service account issuer name, for your service accounts API audience.

# Tutorial

Check out our tutorial video on [Kubernetes Authentication](https://tutorials.akeyless.io/docs/kubernetes-authentication).
