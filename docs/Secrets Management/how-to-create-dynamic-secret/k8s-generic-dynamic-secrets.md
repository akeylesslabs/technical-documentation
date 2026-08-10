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
## Introduction

Akeyless allows you to create a wide variety of resources in Kubernetes to use Dynamic Secrets, from tokens for existing Kubernetes [Service Accounts](https://kubernetes.io/docs/reference/access-authn-authz/service-accounts-admin/) that are used for authentication to completely new Service Accounts complete with Roles and RoleBindings.

To know what resources to generate with and supply to Akeyless, you will first need to choose which of the following Service Account modes is best for your purposes:

### Fixed Service Account

Fixed Service Accounts are existing Kubernetes Service Accounts that Akeyless generates JIT tokens or keys for, and manages them. To work in **Fixed Mode**, you must point Akeyless to the exact Service Account you want to generate tokens for.

### Dynamic Service Account

When working in **Dynamic Mode**, you may use a predefined role and only generate and bind the Service Account. Alternatively, you may use a YAML file that contains both new Role and RoleBinding information for the new Service Account to be generated.

In addition, you must supply a list of Allowed Namespaces to exist within, to control where the Service Account will be created. If you select a pre-existing role (and not a cluster role) - it also must exist in the mentioned namespaces. It’s also possible to define the wildcard character `*` as the list of Allowed Namespaces to allow any Namespace.

## Prerequisites

- An [Akeyless Gateway](https://docs.akeyless.io/docs/gateway-overview)

- A [Generic Kubernetes Target](https://docs.akeyless.io/docs/kubernetes-targets#k8s-generic) or the equivalent inline credentials

- **Fixed Mode:** A pre-defined privileged service account or a Kubernetes user, with permission to run the Kubernetes API `RequestToken` command to generate JWT tokens for other service accounts. In our example, it will be called `token-request-sa` or `token-request-user` respectively. This entity would be used as a privileged user to generate the temporary tokens for other service accounts. In our example, it will be called `example-service-account`.

- **Dynamic Mode:** A pre-defined privileged service account or a Kubernetes user with permission to create and manage `Service Accounts`, `RoleBinding` and `Roles` as well as `get` permissions to `namespaces`. In our example, it will be called `akeyless-jit`. This entity will be used as a privileged user to dynamically generate and manage temporary service accounts.

## Authentication Strategies

Akeyless supports several authentication strategies to interact with the Kubernetes cluster using:

- **The Akeyless Gateway Service Account**
- **A dedicated Service Account's Bearer Token**
- **A Kubernetes User based on a Client Certificate**

### Authenticate Using a Service Account

For both Service Account approaches (either the Gateway SA, or the dedicated SA), the following `yaml` files describe the relevant permissions required for the Service Account to produce Just-in-Time Access (per the desired type of Dynamic Secret you wish to implement: Fixed / Dynamic Mode). If you are using your Gateway Service Account, make sure to adjust the Service Account name in the file below, and discard the creation section of a dedicated Service Account:

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

If you haven't done so already, you can now create a [Generic Kubernetes Target](https://docs.akeyless.io/docs/kubernetes-targets#k8s-generic) using either the GW Service Account or the dedicated Service Account (if it's a dedicated Service Account, be sure to extract its Bearer Token).

<Callout icon="ℹ️" theme="info">
  ### **Info (Kubernetes v1.24 and above):**

  Starting from Kubernetes v1.24 and above, note that Service Accounts are created without tokens by default. To provide the privileged Service Account a Bearer Token for creating the [Kubernetes Generic Target](https://docs.akeyless.io/docs/kubernetes-targets#k8s-generic), create the token manually.
</Callout>

When using `kubeadm`, please make sure to enable the following API flags in the `kubeadm-config.yaml` file.

```yaml kubeadm-config.yaml
apiServer:
  extraArgs:
    service-account-signing-key-file: /etc/kubernetes/pki/sa.key
    service-account-key-file: /etc/kubernetes/pki/sa.pub
    service-account-issuer: api
    service-account-api-audiences: api,vault,factors
```

### Authenticate Using Client Certificate

Create a client key using a Certificate Signing Request (CSR):

```shell
export USER_NAME="token-request-user";
export GROUP="Akeyless-dynamic-secret";
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

The following `yaml` files describe the relevant permissions required for the Kubernetes client according to the type of Dynamic Secret mode you wish to implement - **either Fixed or Dynamic mode**:

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

## Dynamic Generic Kubernetes Secrets with the CLI

### Create a Dynamic Generic Kubernetes Secret

**Fixed Mode:** To create a dynamic generic Kubernetes Secret with the CLI using an existing [Kubernetes Target](https://docs.akeyless.io/docs/kubernetes-targets#create-a-generic-kubernetes-target-from-the-cli) in **Fixed Mode**, use the following command:

```shell Fixed Mode
akeyless dynamic-secret create k8s \
--name <secret name> \
--target-name <Target Name> \
--gateway-url 'https://<Your-Akeyless-GW-URL>:8000' \
--k8s-service-account-type fixed \
--k8s-service-account <example-service-account> \
--k8s-namespace <namespace>
```

Where:

- `name`: A unique name of the dynamic secret. The name can include the path to the virtual folder where you want to create the new dynamic secret, using slash `/` separators. If the folder does not exist, it will be created together with the dynamic secret.

- `target-name`: A name of the target that enables connection to the Kubernetes cluster. The name can include the path to the virtual folder where this target resides.

- `gateway-url`: Akeyless Gateway URL (port `8000`).

- `k8s-service-account-type`: This is the parameter that will define if you are working with a Fixed SA or a Dynamic SA. The default is `fixed`.

- `k8s-service-account`: The Kubernetes ServiceAccount to generate tokens for (Relevant for **Fixed Mode** only).

- `k8s-namespace`: The name of the Kubernetes Namespace where the example Kubernetes ServiceAccount exists.

**Dynamic Mode:** To create a dynamic generic Kubernetes Secret with the CLI using an existing [Kubernetes Target](https://docs.akeyless.io/docs/kubernetes-targets#create-a-generic-kubernetes-target-from-the-cli) in **Dynamic Mode**, use the following command (note that parameters will change if you choose to create a Service Account using an existing Role, or if you choose to generate everything from scratch):

```shell Existing Role
akeyless dynamic-secret create k8s \
--name <secret name> \
--target-name <Target Name> \
--gateway-url 'https://<Your_Akeyless_GW_URL>:8000' \
--k8s-service-account-type dynamic \
--k8s-predefined-role-type <Role|ClusterRole> \
--k8s-predefined-role-name <Role or ClusterRole name> \
--k8s-allowed-namespaces <namespace1, namespace2>
```
```shell Generated Role
akeyless dynamic-secret create k8s \
--name <secret name> \
--target-name <Target Name> \
--gateway-url 'https://<Your_Akeyless_GW_URL>:8000' \
--k8s-service-account-type dynamic \
--k8s-rolebinding-yaml-def <path/to/rolebinding/yml> \
--k8s-allowed-namespaces <namespace1, namespace2>
```

Where:

- `k8s-predefined-role-type`: The type of the pre-existing Kubernetes Role \[`Role`/`ClusterRole`] (For dynamic mode only).

- `k8s-predefined-role-name`: The pre-existing Role or ClusterRole name to bind the generated ServiceAccount to (For dynamic mode only).

- `k8s-allowed-namespaces`: Comma-separated list of allowed Kubernetes Namespaces for the generated ServiceAccount (For dynamic mode only).

- `k8s-rolebinding-yaml-def`: This can be an alternative for specifying other dynamic mode parameters by supplying a YAML file with all of the relevant data in the following format:

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

<Callout icon="⚠️" theme="warn">
  ### **Warning:**

  While working with RoleBinding using a `yml` file, the `namespace` subjects are ignored and managed only by way of the `Allowed Namespaces` list.
</Callout>

If you don't have a configured [Kubernetes Targets](https://docs.akeyless.io/docs/kubernetes-targets) yet, you can use the command with your Kubernetes Cluster connection strings inline:

- `k8s-cluster-endpoint`: The URL of the cluster.

- `k8s-cluster-ca-cert`: The base-64 encoded CA cluster certificate.

- `k8s-cluster-token`: A JWT authentication token authorized to manage Service Accounts, Roles, and RoleBinding depending on the working mode.

You can find the complete list of parameters for this command in the [CLI Reference - Dynamic Secrets](https://docs.akeyless.io/docs/cli-reference-dynamic-secrets#k8s) section.

### Using Dynamic Generic Kubernetes Secrets

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

1. Create the following `kubeconfig` file:

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

To get the dynamic generic Kubernetes Secret value with the CLI, you should run the following command:

{/* secret-stdout-scan:ok */}

```shell Fixed
akeyless get-dynamic-secret-value --name <Path to the dynamic secret>
```
```shell Dynamic
akeyless get-dynamic-secret-value --name <Path to the dynamic secret> --args=namespace=<namespace>
```

Then you need to replace `< Dynamic Secret Value goes here >` with the response token exactly as you received it.

<Callout icon="ℹ️" theme="info">
  ### **Note:**

  To start working with Dynamic Secrets from the Akeyless Console, you need to configure the Gateway URL thus enabling communication between the Akeyless SaaS and the Akeyless Gateway.
</Callout>

## Dynamic Generic Kubernetes Secrets in the Console

### Create a Dynamic Generic Kubernetes Secret

1. Log in to the Akeyless Console, and go to **Items > New > Dynamic Secret**.

2. Select the required dynamic secret type and click **Next**.

3. Define a **Name** of the dynamic secret, and specify the **Location** as a path to the virtual folder where you want to create the new dynamic secret, using slash `/` separators. If the folder does not exist, it will be created together with the dynamic secret.

4. Define the remaining parameters as follows:

   - **Description:** A brief description of the item.

   - **Tags:** Tags you would like to attach to the item.

   - **Delete Protection:** When enabled, it protects the secret from accidental deletion.

   - **Target:** Select an existing [Kubernetes Target](https://docs.akeyless.io/docs/kubernetes-targets).

5. Select your Service Account mode, **Fixed** or **Dynamic**, and fill in the following parameters:

   _For Fixed Mode:_

   - **Service Account:** The name of the Kubernetes Service Account to generate tokens for.

   - **Namespace:** The Namespace of the Kubernetes Service Account.

   _For Dynamic Mode:_

   - **RoleBindings:** A YAML file describing the Role and RoleBinding parameters.

   - **Role Type:** Select if the role is a Kubernetes Role or a Cluster Role.

   - **Allowed Namespaces:** A list of namespaces the secret is allowed to exist within. If the role type is a Kubernetes Role, it must also exist within these namespaces. You can input the wildcard character `*` to allow any Namespace.

   - **Custom Username Template:** Set a [custom username template](https://docs.akeyless.io/docs/dynamic-secrets-user-templating) for the generated user.

6. Fill in the remaining parameters for either type of service account:

   - **User TTL:** Provide a time-to-live value for a dynamic secret. When TTL expires, temporary users and roles will be removed.

   - **Time Unit:** Select the time unit (`seconds`, `minutes`, `hours`) for the TTL value.

   - **Gateway:** Select the Gateway through which the dynamic secret will create users.

   - **Protection key**: To enable zero-Knowledge, select a key with a Customer Fragment. For more information, [read here](https://docs.akeyless.io/docs/gateway-zero-knowledge).

   Select **Finish**.

### Using Dynamic Generic Kubernetes Secrets

1. Log in to the Akeyless Console, and go to **Items**.

2. Browse to the folder where you created a dynamic secret.

3. Select the secret and click the **Get Dynamic Secret** button.

## Example: Kubernetes Dashboard

Let's see an example of how you could use dynamic generic Kubernetes secrets to get a token for the [Kubernetes Dashboard](https://kubernetes.io/docs/tasks/access-application-cluster/web-ui-dashboard/).

In this example, the **token-request-sa** service account will have permission to create tokens for the existing service account **Kubernetes-dashboard** on the **Kubernetes-dashboard** Namespace.

<Callout icon="ℹ️" theme="info">
  ### **Note:**

  Make sure you have the `kubernetes-dashboard` created on your cluster in advance, and confirm the service account has some roles bound to it (in this example, we use the ServiceAccount `kubernetes-dashboard`, which might not have any roles by default, so feel free to change it).
</Callout>

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

1. Extract the `token-request-sa` service account token by running:

```shell
ACCESS_TOKEN=$(kubectl -n kubernetes-dashboard create token token-request-sa)
```

This command uses the Kubernetes TokenRequest flow, which works on current Kubernetes versions and does not depend on auto-generated service account token secrets.

1. Create a Kubernetes generic dynamic secret called **K8s-dashboard-producer** by running:

   ```shell
   akeyless dynamic-secret create k8s -n k8s-dashboard-producer \
   --gateway-url 'http://YourGWURL:8000' \
   --k8s-cluster-endpoint <cluster DNS/IP address> \
   --k8s-cluster-ca-cert <base 64 encoding of the cluster certificate> \
   --k8s-namespace kubernetes-dashboard \
   --k8s-service-account kubernetes-dashboard \
   --k8s-cluster-token ${ACCESS_TOKEN}
   ```

2. Get the **K8s-dashboard-producer** dynamic secret value by running:

   ```shell
   akeyless get-dynamic-secret-value -n k8s-dashboard-producer | jq .
   ```

   The output is:

   ```shell
   {
   "apiVersion": "client.authentication.k8s.io/v1beta1",
   "clusterCACertificate": "LS0tLS1CRUdJTiBDRVJUSUZJQ0FURS0tLS0tCk1JSUJkekNDQVIyZ0F3SUJBZ0lCQURBS0JnZ3Foa2pPUFFRREFqQWpNU0V3SHdZRFZRUUREQmhyTTNNdGMyVnkKZG1WeUxXTmhRREUyTWpNek1UZzBPRFV3SGhjTk1qRXdOakV3TURrME9EQTFXaGNOTXpFd05qQTRNRGswT0RBMQpXakFqTVNFd0h3WURWUVFEREJock0zTXRjMlZ5ZG1WeUxXTmhRREUyTWpNek1UZzBPRFV3V1RBVEJnY3Foa2pPClBRSUJCZ2dxaGtqT1BRTUJCd05DQUFUTEZqVXZIRFg0YmhzMm9TS0Vkb1Y1R2dsQVRPUkpYVDBzYmhCVSs2VzEKUm52dEFwWVZlVDlQa1crUnJXL0VKcS9lZEpNYUFzZGFIcEtxM2FHZTFNbGJvMEl3UURBT0JnTlZIUThCQWY4RQpCQU1DQXFRd0R3WURWUjBUQVFIL0JBVXdBd0VCL3pBZEJnTlZIUTRFRmdRVWhXTGwzU1N5UGVHVlRRVlh6UkszClV5RnF4S0l3Q2dZSUtvWkl6ajBFQXdJRFNBQXdSUUloQUkwd2MwcUUwck9YZVN2VzN5d1RFc1BHWVUrVHZkVTIKbVFEYUtIN3BvSGJVQWlCbWtoQTNZejZhQkpmTmU0c09Eb1RKK2lGTElwSndvb3FPZjhGZWYvdnJSdz09Ci0tLS0tRU5EIENFUlRJRklDQVRFLS0tLS0K",
   "clusterEndpoint": "https://0.0.0.0:56155",
   "clusterName": "k8s-native-cluster",
   "clusterUsername": "k8s-native-cluster",
   "kind": "ExecCredential",
   "status": {
     "token": "<K8S_SERVICE_ACCOUNT_JWT_TOKEN>"
   }
   }
   ```

3. Copy the **token** value, and use it for the Kubernetes Dashboard.

## Single `Kubeconfig` Generation

Generate a single `kubeconfig` file that aggregates all of your allowed Kubernetes Dynamic Secrets (across one or more clusters).

The CLI command is `akeyless kubeconfig-generate`

### Options

- `n, --name` - List of Dynamic Secret names (repeatable)
- `t, --tag` - A single tag attached to Dynamic Secrets
- `o, --out[=kubeconfig.json]` - Output path for the generated `kubeconfig` file
- `-profile, --token` - Use a saved profile (`$HOME/.akeyless/profiles`) or a temporary access token
- `-uid-token` - Universal Identity token (required only with the `universal_identity` Authentication Method)
- `-json[=false]` - Return tool output in JSON
- `-jq-expression` - jq filter for JSON output
- `-no-creds-cleanup[=false]` -  Do not clean local temporary expired credentials

Remember to provide at least one selector:  `--name` (one or more secret names) or `--tag` (a single tag). When both are provided, the first provided selector is used.

### Conflict Handling (Duplicate Cluster/context Names)

When duplicate context names are detected during merge:

- **Default behavior:** It keeps the **first** occurrence and **logs a warning** about the conflict.
- **Resolution message:** the CLI prints a clear notice in the terminal describing which context was kept and which was skipped or renamed.
- **Auditable:** the same message is written to the log for later review.

<Callout icon="ℹ️" theme="info">
  ### **Note (Example terminal notice):**

  `WARNING: Context "prod-us1" already exists. Keeping the first occurrence; skipped merging duplicate from secret "ds-kube-prod-us1".`

  Ensure the user or automation has permission to retrieve the selected Dynamic Secrets.
</Callout>

<br />
