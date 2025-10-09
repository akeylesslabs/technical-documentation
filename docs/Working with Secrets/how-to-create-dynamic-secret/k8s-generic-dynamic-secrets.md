---
title: Kubernetes Generic Dynamic Secrets
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
# Introduction

Akeyless allows you to create a wide variety of resources in Kubernetes to utilize dynamic secrets, from tokens for existing Kubernetes [Service Accounts](https://kubernetes.io/docs/reference/access-authn-authz/service-accounts-admin/) that are used for authentication to completely new Service Accounts complete with roles and role bindings.

To know what resources to generate with and supply to Akeyless, you will first need to choose which of the following Service Account modes is best for your purposes:

### **Fixed Service Account**

Fixed Service Accounts are existing Kubernetes Service Accounts that Akeyless generates JIT tokens or keys for, and manages them. To work in **Fixed Mode**, you must point Akeyless to the exact Service Account you want to generate tokens for.

### **Dynamic Service Account**

When working in **Dynamic Mode**, you may use a predefined role and only generate and bind the Service Account. Alternatively, you may use a YAML file that contains both new Role and Role Binding information for the new Service Account to be generated.

In addition, you must supply a list of Allowed Namespaces to exist within, to control where the Service Account will be created. If you select a pre-existing role (and not a cluster role) - it also must exist in the mentioned namespaces. It’s also possible to define the wildcard character `*` as the list of Allowed Namespaces to allow any namespace.

> 👍 Note
>
> We recommend using dynamic secrets with [Targets](https://docs.akeyless.io/docs/targets). While it saves time for multiple secret-level configurations by not requiring you to provide an inline connection string each time, it is also important for security streamlining. Using a target allows you to rotate credentials without breaking the credential chain for the objects connected to the server used, using inline will force you to go and change the credentials in each individual item instead of just the target.

# Prerequisites

* An [Akeyless Gateway](https://docs.akeyless.io/docs/api-gw)

* A [Generic Kubernetes Target](https://docs.akeyless.io/docs/kubernetes-targets#k8s-generic) or the equivalent inline credentials

* **Fixed Mode:** A pre-defined privileged service account or a K8s user, with permission to run the Kubernetes API `RequestToken` command to generate JWT tokens for other service accounts. In our example, it will be called `token-request-sa` or `token-request-user` respectively. This entity would be used as a privileged user to generate the temporary tokens for other service accounts. In our example, it will be called `example-service-account`.

* **Dynamic Mode:** A pre-defined privileged service account or a k8s user with permission to create and manage `Service Accounts`, `Role Binding` and `Roles` as well as `get` permissions to `namespaces`. In our example, it will be called `akeyless-jit`. This entity will be used as a privileged user to dynamically generate and manage temporary service accounts.

# Authentication Strategies

Akeyless supports several authentication strategies to interact with the K8s cluster using:

* **The Akeyless Gateway Service Account**
* **A dedicated Service Account's Bearer Token**
* **A K8s User based on a Client Certificate**

## Authenticate using a Service Account

For both Service Account approaches (either the Gateway SA, or the dedicated SA), the following `yaml` files describe the relevant permissions required for the Service Account to produce just-in-time access (per the desired type of Dynamic Secret you wish to implement: Fixed / Dynamic Mode). If you are using your Gateway Service Account, make sure to adjust the Service Account name in the file below, and discard the creation section of a dedicated Service Account:

```yaml Fixed Mode
apiVersion: v1
kind: ServiceAccount
metadata:
  name: token-request-sa
  namespace: <Namespace>
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: tokenrequest
rules:
- apiGroups: [""]
  resources:
  - "serviceaccounts/token"
  - "serviceaccounts"
  verbs:
  - "create"
  - "get"
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: tokenrequest
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: tokenrequest
subjects:
- kind: ServiceAccount
  name: token-request-sa
  namespace: <Namespace>
```
```yaml Dynamic Mode
apiVersion: v1
kind: ServiceAccount
metadata:
  name: akeyless-jit
  namespace: <Namespace>
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: sa-request
rules:
- apiGroups: [""]
  resources: ["namespaces"]
  verbs: ["get"]
- apiGroups: [""]
  resources: ["serviceaccounts", "serviceaccounts/token"]
  verbs: ["get", "create", "update", "delete"]
- apiGroups: ["rbac.authorization.k8s.io"]
  resources: ["rolebindings", "clusterrolebindings"]
  verbs: ["get", "create", "update", "delete"]
- apiGroups: ["rbac.authorization.k8s.io"]
  resources: ["roles", "clusterroles"]
  verbs: ["get", "bind", "escalate", "create", "update", "delete"]
- apiGroups: [""]
  resources: ["pods"]
  verbs: ["list"]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: sa-request
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: sa-request
subjects:
- kind: ServiceAccount
  name: akeyless-jit
  namespace: <Namespace>
```

If you haven't done so already, you can now create a [Generic Kubernetes Target](https://docs.akeyless.io/docs/kubernetes-targets#k8s-generic) using either the GW Service Account, or the dedicated Service Account (if its a dedicated Service Account, be sure to extract its Bearer Token).

> 📘 Info
>
> **K8s v1.24 and above**
>
> Starting from K8s v1.24 and above, note that Service Accounts are created without tokens by default. In order to provide the privileged Service Account a Bearer Token for the creation of the [K8s Generic Target](https://docs.akeyless.io/docs/kubernetes-targets#k8s-generic), please create the token manually.

When using `kubeadm`, please make sure to enable the following API flags in the <code>kubeadm-config.yaml</code> file.

```yaml kubeadm-config.yaml
apiServer:
  extraArgs:
    service-account-signing-key-file: /etc/kubernetes/pki/sa.key
    service-account-key-file: /etc/kubernetes/pki/sa.pub
    service-account-issuer: api
    service-account-api-audiences: api,vault,factors
```

## Authenticate using Client Certificate

Create a client key using a Certificate Signing Request (CSR):

```shell
ֿexport USER_NAME="token-request-user" ;
export GROUP="Akeyless-dynamic-secret";
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

The following `yaml` files describe the relevant permissions required for the K8s client according to the type of Dynamic Secret mode you wish to implement - **either Fixed or Dynamic mode**:

```yaml Fixed Mode
cat <<EOF | kubectl apply -f -
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: tokenrequest
rules:
- apiGroups: [""]
  resources:
  - "serviceaccounts/token"
  - "serviceaccounts"
  verbs:
  - "create"
  - "get"
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: tokenrequest
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: tokenrequest
subjects:
- kind: User
  name: $USER_NAME
  apiGroup: rbac.authorization.k8s.io
EOF
```
```yaml Dynamic Mode
cat <<EOF | kubectl apply -f -
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: sa-request
rules:
- apiGroups: [""]
  resources: ["namespaces"]
  verbs: ["get"]
- apiGroups: [""]
  resources: ["serviceaccounts", "serviceaccounts/token"]
  verbs: ["get", "create", "update", "delete"]
- apiGroups: ["rbac.authorization.k8s.io"]
  resources: ["rolebindings", "clusterrolebindings"]
  verbs: ["get", "create", "update", "delete"]
- apiGroups: ["rbac.authorization.k8s.io"]
  resources: ["roles", "clusterroles"]
  verbs: ["get", "bind", "escalate", "create", "update", "delete"]
- apiGroups: [""]
  resources: ["pods"]
  verbs: ["list"]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: sa-request
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: sa-request
subjects:
- kind: User
  name: $USER_NAME
  apiGroup: rbac.authorization.k8s.io
EOF
```

If you haven't done so already, you can now create a [Generic Kubernetes Target](https://docs.akeyless.io/docs/kubernetes-targets#k8s-generic) using the Client Certificate generated above.

# Dynamic Generic Kubernetes Secrets in the CLI

## Create a Dynamic Generic Kubernetes Secret

**Fixed Mode:** To create a dynamic generic Kubernetes secret from the CLI using an existing [Kubernetes Target](https://docs.akeyless.io/docs/kubernetes-targets#create-a-generic-kubernetes-target-from-the-cli) in **Fixed Mode**, use the following command:

```shell Fixed Mode
akeyless dynamic-secret create k8s \ 
--name <secret name> \
--target-name <Target Name> \
--gateway-url 'https://<Your-Akeyless-GW-URL:8000>' \
--k8s-service-account-type fixed \
--k8s-service-account <example-service-account> \
--k8s-namespace <namespace>
```

Where:

* `name`: A unique name of the dynamic secret. The name can include the path to the virtual folder where you want to create the new dynamic secret, using slash `/` separators. If the folder does not exist, it will be created together with the dynamic secret.

* `target-name`: A name of the target that enables connection to the Kubernetes cluster. The name can include the path to the virtual folder where this target resides.

* `gateway-url`: Akeyless Gateway Configuration Manager URL (port `8000`).

* `k8s-service-account-type`: This is the parameter that will define if you are working with a Fixed SA or a Dynamic SA. The default is `fixed`.

* `k8s-service-account`: The Kubernetes Service Account to generate tokens for (Relevant for **Fixed Mode** only).

* `k8s-namespace`: The name of the K8S Namespace where the example Service Account exists.

**Dynamic Mode:** To create a dynamic generic Kubernetes secret from the CLI using an existing [Kubernetes Target](https://docs.akeyless.io/docs/kubernetes-targets#create-a-generic-kubernetes-target-from-the-cli) in **Dynamic Mode**, use the following command (note parameters will change if you choose to create a ServiceAccount using an existing Role, or if you choose to generate everything from scratch):

```shell Existing Role
akeyless dynamic-secret create k8s \ 
--name <secret name> \
--target-name <Target Name> \
--gateway-url 'https://<Your_Akeyless_GW_URL:8000>' \
--k8s-service-account-type dynamic \
--k8s-predefined-role-type <Role|ClusterRole> \
--k8s-predefined-role-name <Role or ClusterRole name> \
--k8s-allowed-namespaces <namespace1, namespace2>
```
```shell Generated Role
akeyless dynamic-secret create k8s \ 
--name <secret name> \
--target-name <Target Name> \
--gateway-url 'https://<Your_Akeyless_GW_URL:8000>' \
--k8s-service-account-type dynamic \
--k8s-rolebinding-yaml-def <path/to/rolebinding/yml>
--k8s-allowed-namespaces <namespace1, namespcae2>
```

Where:

* `k8s-predefined-role-type`: The type of the pre-existing K8S role [`Role`/`ClusterRole`] (For dynamic mode only).

* `k8s-predefined-role-name`: The pre-existing Role or ClusterRole name to bind the generated ServiceAccount to (For dynamic mode only).

* `k8s-allowed-namespaces`: Comma-separated list of allowed K8S namespaces for the generated ServiceAccount (For dynamic mode only).

* `k8s-rolebinding-yaml-def`: This can be an alternative for specifying other dynamic mode parameters by supplying a YAML file with all of the relevant data in the following format:

```yaml RoleBinding.yml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: example-role
rules:
- apiGroups: [""]
  resources: ["pods"]
  verbs: ["list"]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: example-role
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: Role
  name: example-role
```

> 🚧 Warning
>
> While working with Role Binding using `yml` file, the `namespace` subjects are ignored and managed only via the `Allowed Namespaces` list

If you don't have a configured [Kubernetes Targets](https://docs.akeyless.io/docs/kubernetes-targets) yet, you can use the command with your K8s Cluster connection strings inline:

* `k8s-cluster-endpoint`: The URL of the cluster.

* `k8s-cluster-ca-cert`: The base-64 encoded CA cluster certificate.

* `k8s-cluster-token`: A JWT authentication token authorized to manage Service Accounts, Roles, and Role Binding depending on the working mode.

You can find the complete list of parameters for this command in the [CLI Reference - Dynamic Secrets](https://docs.akeyless.io/docs/cli-reference-dynamic-secrets#p-stylecolorbluek8sp) section.

## Using Dynamic Generic Kubernetes Secrets

If the Akeyless CLI is installed on the same host as the `kubectl`, you can define a `kubeconfig` file to automatically run the `get-dynamic-secret-value` command and fetch new access tokens as required.

Create the following `kubeconfig` file to run the `get-dynamic-secret-value` command and fetch new access tokens:

```yaml
apiVersion: v1
clusters:
- cluster:
    certificate-authority-data: <base 64 encoding of the cluster certificate>
    server: <cluster DNS/IP address>
  name: <cluster name>
contexts:
- context:
    cluster: <cluster name>
    user: <user name>
  name: <cluster context name>
current-context: <cluster context name>
kind: Config
preferences: {}
users:
- name: <user name>
  user:
    exec:
      apiVersion: client.authentication.k8s.io/v1beta1
      args:
        - get-dynamic-secret-value
        - --name
        - <dynamic secret item name>
        - --profile
        - <some profile> 
      command: /usr/local/bin/akeyless
      interactiveMode: IfAvailable
```

If the Akeyless CLI is installed on a different host as the `kubectl`, you can get a service account token from Akeyless separately, and then manually update the `kubeconfig` file that uses the token.

1. Create the following kubeconfig file:

```yaml
apiVersion: v1
clusters:
- cluster:
    certificate-authority-data: <base 64 encoding of the cluster certificate>
    server: <cluster DNS/IP address>
  name: <cluster name>
contexts:
- context:
    cluster: <cluster name>
    user: <user name>
  name: <cluster context name>
current-context: <cluster context name>
kind: Config
preferences: {}
users:
- name: <some user name>
  user:
    token: < Dynamic Secret Value goes here >
```

To get the dynamic generic Kubernetes secret value from the CLI, you should run the following command:

```shell Fixed
akeyless get-dynamic-secret-value --name <Path to the dynamic secret>
```
```shell Dynamic
akeyless get-dynamic-secret-value --name <Path to the dynamic secret> --args=namespace=<namespace>"
```

Then you need to replace `< Dynamic Secret Value goes here >` with the response token exactly as you received it.

> 👍 Note
>
> To start working with dynamic secrets from the Akeyless Console, you need to configure the Gateway URL thus enabling communication between the Akeyless SaaS and the Akeyless Gateway.

# Dynamic Generic Kubernetes Secrets in the Console

## Create a Dynamic Generic Kubernetes Secret

1. Log in to the Akeyless Console, and go to **Items > New > Dynamic Secret**.

2. Select the required database type and click **Next**.

3. Define a **Name** of the dynamic secret, and specify the **Location** as a path to the virtual folder where you want to create the new dynamic secret, using slash `/` separators. If the folder does not exist, it will be created together with the dynamic secret.

4. Define the remaining parameters as follows:

* **Description:** A brief description of the item.

* **Tags:** Tags you would like to attach to the item.

* **Delete Protection:** When enabled, it protects the secret from accidental deletion.

* **Target mode:** In this section, you can either select an existing [Kubernetes Target](https://docs.akeyless.io/docs/kubernetes-targets) or specify details of the endpoint specifically in the next section explicitly.

5. Select your Service Account mode, **Fixed** or **Dynamic**, and fill in the following parameters:

**For Fixed Mode**

* **Service Account:** The name of the Kubernetes Service Account to generate the tokens for.

* **Namespace:** The namespace of the Kubernetes Service Account.

**For Dynamic Mode**

* **Role Bindings:** A YAML file describing the Role, and Role Binding parameters.

* **Role Type:** Select if the role is a K8s Role or a Cluster Role.

* **Allowed Namespaces:** A list of namespaces the secret is allowed to exist within. If the role type is a K8s Role, it must also exist within these namespaces. You can input the wildcard character `*` to allow any namespace.

* **Custom Username Template:** Set a [custom username template](https://docs.akeyless.io/docs/dynamic-secrets-user-templating) for the generated user.

6. Fill in the remaining parameters for either type of service account:

* **User TTL:** Provide a time-to-live value for a dynamic secret. When TTL expires, temporary users and roles will be removed.

* **Time Unit:** Select the time unit (`seconds`, `minutes`,`hours`) for the TTL value.

* **Gateway:** Select the Gateway through which the dynamic secret will create users.

* **Protection key**: To enable zero-Knowledge, select a key with a Customer Fragment. For more information, [read here](https://docs.akeyless.io/docs/implement-zero-knowledge).

If you selected the **Explicitly specify target properties** mode, click **Next**. Otherwise, select **Finish**.

7. Fill in the parameters required:

   1. **Bearer Token**

      * **Bearer Token:** Provide a JWT authentication token authorized to manage Service Account tokens, Roles, and Role Binding, depending on the working mode.

      * **Cluster CA Certificate:**Provide the k8s cluster CA certificate (PEM format)

      * **Cluster Endpoint URL:** Specify the URL of the cluster.
   2. **GW Service Account** to extract the connection settings from a  **Gateway** that runs on a **K8s** cluster, with a Service Account with permissions as described in the [prerequisits](https://docs.akeyless.io/docs/k8s-generic-dynamic-secrets#prerequisites) section of this page.
   3. **Client Certificate**
      * **Client Certificate:**Provide the k8s client certificate (PEM format).
      * **Client Private Key :** Provide the K8s client private key (PEM format).
      * **Cluster CA Certificate:** Provide the k8s cluster CA certificate (PEM format).
      * **Cluster Endpoint URL:** Specify the URL of the cluster.
8. Select **Finish**.

## Using Dynamic Generic Kubernetes Secrets

1. Log in to the Akeyless Console, and go to **Items**.

2. Browse to the folder where you created a dynamic secret.

3. Select the secret and click **Get Dynamic Secret** button.

# Example: Kubernetes Dashboard

Let's see an example of how you could use dynamic generic Kubernetes secrets to get a token for the [Kubernetes Dashboard](https://kubernetes.io/docs/tasks/access-application-cluster/web-ui-dashboard/).

In this example, the **token-request-sa** service account will have permission to create tokens for the existing service account **kubernetes-dashboard** on the **kubernetes-dashboard** namespace.

> 👍 Note
>
> Make sure you have the `kubernetes-dashboard` created on your cluster in advance, and confirm the service account has some roles bound to it (in this example, we use the ServiceAccount `kubernetes-dashboard`, which might not have any roles by default, so feel free to change it).

```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: token-request-sa
  namespace: kubernetes-dashboard
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: tokenrequest-dash
rules:
- apiGroups: [""]
  resources:
  - "serviceaccounts/token"
  - "serviceaccounts"
  verbs:
  - "create"
  - "get"
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: tokenrequest-dash
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: tokenrequest-dash
subjects:
- kind: ServiceAccount
  name: token-request-sa
  namespace: kubernetes-dashboard
```

1. Extract the service account token (secret) name by running:

```shell Shell
TOKENNAME=`kubectl -n kubernetes-dashboard get serviceaccount/token-request-sa -o jsonpath='{.secrets[0].name}'`
```

2. Extract the service account token by running:

```shell Shell
TOKEN=`kubectl -n kubernetes-dashboard get secret $TOKENNAME -o jsonpath='{.data.token}'| base64 --decode`
```

3. Create a Kubernetes generic dynamic secret called **k8s-dashboard-producer** by running:

```shell Shell
akeyless dynamic-secret create k8s -n k8s-dashboard-producer \
--gateway-url <http://YourGWURL:8000> \
--k8s-cluster-endpoint <cluster DNS/IP address> \
--k8s-cluster-ca-cert <base 64 encoding of the cluster certificate> \
--k8s-namespace kubernetes-dashboard \
--k8s-service-account kubernetes-dashboard \
--k8s-cluster-token ${TOKEN}
```

3. Get the **k8s-dashboard-producer** dynamic secret value by running:

```shell Akeyless CLI
akeyless get-dynamic-secret-value -n k8s-dashboard-producer | jq .
```

The output is:

```shell Akeyless CLI
{
  "apiVersion": "client.authentication.k8s.io/v1beta1",
  "clusterCACertificate": "LS0tLS1CRUdJTiBDRVJUSUZJQ0FURS0tLS0tCk1JSUJkekNDQVIyZ0F3SUJBZ0lCQURBS0JnZ3Foa2pPUFFRREFqQWpNU0V3SHdZRFZRUUREQmhyTTNNdGMyVnkKZG1WeUxXTmhRREUyTWpNek1UZzBPRFV3SGhjTk1qRXdOakV3TURrME9EQTFXaGNOTXpFd05qQTRNRGswT0RBMQpXakFqTVNFd0h3WURWUVFEREJock0zTXRjMlZ5ZG1WeUxXTmhRREUyTWpNek1UZzBPRFV3V1RBVEJnY3Foa2pPClBRSUJCZ2dxaGtqT1BRTUJCd05DQUFUTEZqVXZIRFg0YmhzMm9TS0Vkb1Y1R2dsQVRPUkpYVDBzYmhCVSs2VzEKUm52dEFwWVZlVDlQa1crUnJXL0VKcS9lZEpNYUFzZGFIcEtxM2FHZTFNbGJvMEl3UURBT0JnTlZIUThCQWY4RQpCQU1DQXFRd0R3WURWUjBUQVFIL0JBVXdBd0VCL3pBZEJnTlZIUTRFRmdRVWhXTGwzU1N5UGVHVlRRVlh6UkszClV5RnF4S0l3Q2dZSUtvWkl6ajBFQXdJRFNBQXdSUUloQUkwd2MwcUUwck9YZVN2VzN5d1RFc1BHWVUrVHZkVTIKbVFEYUtIN3BvSGJVQWlCbWtoQTNZejZhQkpmTmU0c09Eb1RKK2lGTElwSndvb3FPZjhGZWYvdnJSdz09Ci0tLS0tRU5EIENFUlRJRklDQVRFLS0tLS0K",
  "clusterEndpoint": "https://0.0.0.0:56155",
  "clusterName": "k8s-native-cluster",
  "clusterUsername": "k8s-native-cluster",
  "kind": "ExecCredential",
  "status": {
    "token": "eyJhbGciOiJSUzI1NiIsImtpZCI6InNmMmZhbXgyRC1KT1pzUTBSVll0RFMzQjk1dGJXV19sRnd0b3FhYnBBRTgifQ.eyJhdWQiOlsiaHR0cHM6Ly9rdWJlcm5ldGVzLmRlZmF1bHQuc3ZjLmNsdXN0ZXIubG9jYWwiLCJrM3MiXSwiZXhwIjoxNjI0MTg4MTY5LCJpYXQiOjE2MjQxODQ1NjksImlzcyI6Imh0dHBzOi8va3ViZXJuZXRlcy5kZWZhdWx0LnN2Yy5jbHVzdGVyLmxvY2FsIiwia3ViZXJuZXRlcy5pbyI6eyJuYW1lc3BhY2UiOiJrdWJlcm5ldGVzLWRhc2hib2FyZCIsInNlcnZpY2VhY2NvdW50Ijp7Im5hbWUiOiJrdWJlcm5ldGVzLWRhc2hib2FyZCIsInVpZCI6IjI5MGU4M2IwLTc1MTItNDZiOC1hYWIxLWViN2IxOTIxNmY2NyJ9fSwibmJmIjoxNjI0MTg0NTY5LCJzdWIiOiJzeXN0ZW06c2VydmljZWFjY291bnQ6a3ViZXJuZXRlcy1kYXNoYm9hcmQ6a3ViZXJuZXRlcy1kYXNoYm9hcmQifQ.oflUcXwzFF2Kcyi45_SNrdGmAk_2abqAz0nE7AyUU_-W2-l7ZxPovtM2pfcfHm_dmW9wCDxM3zK4Zh39ruWnvjqIB_uxWQGAtQnU3TBlHSY2knQdZ7lNop-ylvQMdh4rTNf07BM_zKoKVh1w1__nE-esghwOe6mtRuKIy3Xj5Ijk2aamx3DFbFcyizHyZVst_PSbm1fdxdSLFzBy0vXmI8-Lx-KbJsUM5yO2MGmEk-oX28YCG0hgF0NkPbyjyEtIPBrRKbbdyo8lM_dGQ5Hk7D1P5Vo56f14oKUHRJDdzyd-jFSH_dtxD0FxazuNPlmuE9lRdJzeSgvuGp6S-MsksQ"
  }
}
```

4. Copy the **token** value, and use it for the Kubernetes Dashboard.

# Single `kubeconfig` Generation

Generate a single `kubeconfig` file that aggregates all of your allowed Kubernetes Dynamic Secrets (across one or more clusters).

The CLI command is `akeyless kubeconfig-generate`

**Options**

* `n, --name` - List of Dynamic Secret names (repeatable)
* `t, --tag` - A single tag attached to Dynamic Secrets
* `o, --out[=kubeconfig.json]` - Output path for the generated `kubeconfig` file
* `-profile, --token` - Use a saved profile (`$HOME/.akeyless/profiles`) or a temporary access token
* `-uid-token` - Universal Identity token (required only with the`universal_identity` Authentication Method)
* `-json[=false]` - Return tool output in JSON
* `-jq-expression` - JQ filter for JSON output
* `-no-creds-cleanup[=false]` -  Do not clean local temporary expired credentials

Remember to provide at least one selector:  `--name` (one or more secret names) or `--tag` (a single tag). When both are provided, the first provided selector is used.

## Conflict handling (duplicate cluster/context names)

When duplicate context names are detected during merge:

* **Default behavior:** It keeps the **first** occurrence and **log a warning** about the conflict.
* **Resolution message:** the CLI prints a clear notice in the terminal describing which context was kept and which was skipped or renamed.
* **Auditable:** the same message is written to the log for later review.

> Example terminal notice:
>
> `WARNING: Context "prod-us1" already exists. Keeping the first occurrence; skipped merging duplicate from secret "ds-kube-prod-us1".`

> 👍 Note
>
> * Ensure the user or automation has permission to retrieve the selected Dynamic Secrets
