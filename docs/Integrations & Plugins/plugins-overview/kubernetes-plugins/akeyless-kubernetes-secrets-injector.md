---
title: Akeyless Kubernetes Secrets Injector
excerpt: ''
deprecated: false
hidden: false
metadata:
  title: ''
  description: ''
  robots: index
next:
  description: ''
  pages:
    - type: basic
      slug: policy-segregation-for-kubernetes
      title: Policy Segregation for Kubernetes
---
## Overview

The Akeyless Kubernetes Secrets Injector plugin enables Kubernetes applications and workloads to use [Static](https://docs.akeyless.io/docs/static-secrets), [Rotated](https://docs.akeyless.io/docs/rotated-secrets), and [Dynamic](https://docs.akeyless.io/docs/how-to-create-dynamic-secret) secrets as well as [Certificates](https://docs.akeyless.io/docs/certificate-storage) and [USC](https://docs.akeyless.io/docs/universal-secrets-connector) sourced from the Akeyless Platform.

This injector leverages the Kubernetes `MutatingAdmissionWebhook` to intercept and augment specifically annotated pod configurations for secrets injection. By doing so, the user benefits as the applications remain ״Akeyless unaware״ as the secrets are stored either as an **environment variable** or as a file at a **filesystem path** in their container.

Before the application starts, the injector deploys an **init** container to fetch and inject secrets at pod start-up, after which the init-container shuts down. To apply an automatic [rollout restart](https://kubernetes.io/docs/reference/kubectl/generated/kubectl_rollout/kubectl_rollout_restart/) to your deployments upon **any** change to your secrets, you can use the Injector with restart-rollout mode, which can track any changes of [Static](https://docs.akeyless.io/docs/static-secrets), [Rotated](https://docs.akeyless.io/docs/rotated-secrets) and [Certificates](https://docs.akeyless.io/docs/certificate-storage).

If the application consumes secrets which regularly change, an annotation can be used to deploy an additional **Sidecar** container which runs alongside the application to monitor changes in secrets. The **Sidecar** tracks and updates secrets within injected files inside the pods, according to specifically annotated pod configurations, and will remain up for the entire application lifecycle. Relevant for cases where the app can watch for live changes in files.

Although authorization in Kubernetes is intentionally high-level, you can configure the injector to support full and flexible isolation using Kubernetes policies together with the Akeyless Platform's [Role-Based Access Control (RBAC)](https://docs.akeyless.io/docs/rbac).  
For details, see [Policy Segregation for Kubernetes](https://docs.akeyless.io/docs/policy-segregation-for-kubernetes).

![Illustration for: Although authorization in Kubernetes is intentionally high level, you can configure the injector to support full and flexible segregation using Kubernetes policies together…](https://files.readme.io/dd531a9-Akeyless_Rebranded_Infographics_1.png)

> ℹ️ **Note:**
>
> The documentation, configuration and examples for the plugin are also applicable to **Red Hat OpenShift** environment.

## Prerequisites

* Helm Installed.

* **Kubernetes Auth** or one of the supported [Authentication Methods for Kubernetes](https://docs.akeyless.io/docs/auth-meth-k8s).

* Kubernetes v1.19 and above.

* For Azure Kubernetes Service (AKS), **managed-identity** is enabled on your AKS cluster.

* For AKS Workload Identity, the AKS OIDC issuer and workload identity features are enabled.

* For Google Kubernetes Engine (GKE) cluster, port **8443** is opened in your Google Cloud Platform (GCP) firewall rules.

## Create a Secret in Akeyless

For example, the following command creates a static secret called **my_k8s_secret** inside **K8s** folder.

```shell
akeyless create-secret --name /K8s/my_k8s_secret --value myPassword
```

Alternatively, a secret can contain `JSON` structured data, for example:

```shell
akeyless create-secret --name /K8s/secret-json --value '{"aws_access_key":"1234","aws_key_id":"abcd"}'
```

> ℹ️ **Note:**
>
> The following example uses a pre-defined [Kubernetes Auth](https://docs.akeyless.io/docs/auth-with-kubernetes) called **K8s_Auth** in **K8s** folder that is `K8s/K8s_Auth`

## Create an Access Role

Create an [Access Role](https://docs.akeyless.io/docs/rbac) associate the role with an **Auth Method** and grant access to the secret.  
For example, the following command creates **K8s_role** role, the role is associated to **K8s_Auth** Auth Method, and grant **read** and **list** access to all the secrets in **K8s** folder

```shell
akeyless create-role --name /K8s/K8s_Role
akeyless assoc-role-am --role-name /K8s/K8s_Role --am-name K8s/K8s_Auth
akeyless set-role-rule --role-name /K8s/K8s_Role --path /K8s/'*' --capability read --capability list
```

## Install the Injector

1. Add the Akeyless Kubernetes Injector Helm repository from [here](https://github.com/akeylesslabs/helm-charts/tree/main/charts/akeyless-k8s-secrets-injection) and update your Helm repositories.

    ```shell
    helm repo add akeyless https://akeylesslabs.github.io/helm-charts
    helm repo update
    ```

2. Fetch the **values.yaml** file locally:

    ```shell
    helm show values akeyless/akeyless-secrets-injection > values.yaml
    ```

    Modify the following values in `values.yaml` as follows:

    * Set `AKEYLESS_ACCESS_ID` to the Access ID of the Auth Method with access to the secret.

    * Set `AKEYLESS_ACCESS_TYPE` to `k8s`. Or with any other supported [Authentication Methods for Kubernetes](https://docs.akeyless.io/docs/auth-meth-k8s).

    * For `AKEYLESS_ACCESS_TYPE` set to `azure_ad`, set `AKEYLESS_AZURE_OBJ_ID` to select a specific user-assigned managed identity. This is required when multiple user-assigned identities are attached.

    * Set `AKEYLESS_K8S_AUTH_CONF_NAME` with your Gateway Kubernetes Auth name. Relevant **only** for Access type of `k8s`.

    * Set `AKEYLESS_API_GW_URL` with the URL of your Gateway API v1 endpoint: `/8000/api/v1` or port `8080`.
      * If `AKEYLESS_API_GW_URL` points to a Gateway that uses a private or internal CA certificate, set the top-level `gatewayCert.tlsCertsSecretName` value to a Kubernetes secret that contains `tls.crt`.

    * Optional `AKEYLESS_CRASH_POD_ON_ERROR` Upon any failure, a pod that tries to fetch a secret and fails will crash. By default this option is disabled. Can be controlled globally or at the deployment level using a dedicated [annotation](https://docs.akeyless.io/docs/akeyless-kubernetes-secrets-injector#annotations-list).

    * Optional `restartRollout`: to apply automatic rollout restart to your deployments upon secret changes. Relevant only for the kinds of: `Deployment`, `DaemonSet` or `StatefulSet`. To control which deployments are not affected by the restart-rollout, you can use a dedicated [annotation](https://docs.akeyless.io/docs/akeyless-kubernetes-secrets-injector#annotations-list) to disable this on the deployment level.

      > ❗ **Important:**
      >
      > When `restartRollout` is enabled, the injector pod must be able to call `list-items` on the Akeyless API to detect secret changes. Ensure the Auth Method configured by `AKEYLESS_ACCESS_ID` grants the injector service account, which runs in the injector namespace, both `list` and `read` permissions on the monitored secret paths. For namespace claim considerations, see [Restart Rollout](https://docs.akeyless.io/docs/akeyless-kubernetes-secrets-injector#restart-rollout).

    * `AKEYLESS_REGISTRY_CREDS`: a reference to an existing secret that holds your container registry credentials. Relevant when working with Environment variables and a **private** container registry, to [override automatically](https://docs.akeyless.io/docs/akeyless-kubernetes-secrets-injector#override-entrypoint-automatically) the Docker entrypoint, can be used at the deployment level using a dedicated [annotation](https://docs.akeyless.io/docs/akeyless-kubernetes-secrets-injector#annotations-list). not required for **public** registry.

    * Optional `AKEYLESS_IGNORE_CACHE`: to allow bypassing the Gateway cache when fetching secrets, ensuring access to the latest data, which is `disabled` by default. can be used at the deployment level using a dedicated [annotation](https://docs.akeyless.io/docs/akeyless-kubernetes-secrets-injector#annotations-list)

    * Optional `INIT_RUN_AS_USER`: To apply a [Security Context](https://kubernetes.io/docs/tasks/configure-pod-container/security-context/) to your init container, set the following environment variable, `INIT_RUN_AS_USER: "id=65534"`.

    ```yaml
    restartRollout:
      enabled: false
      interval: 1m

    gatewayCert:
      tlsCertsSecretName: "gateway-ca-cert"
    
    env:
      AKEYLESS_ACCESS_ID: "<AccessID>"
      AKEYLESS_ACCESS_TYPE: "k8s"
      # For azure_ad authentication (when selecting a user-assigned identity):
      # AKEYLESS_AZURE_OBJ_ID: "<azure-object-id>"
      AKEYLESS_K8S_AUTH_CONF_NAME: "K8s_Auth_Name"
      AKEYLESS_API_GW_URL: "https://Your-Gateway-URL:8000/api/v1"
      # AKEYLESS_CRASH_POD_ON_ERROR: "enable"
      # AKEYLESS_IGNORE_CACHE: "enable"
    ```

    Create the certificate secret before deploying the chart:

    ```shell
    kubectl create secret generic gateway-ca-cert -n akeyless --from-file=tls.crt=<path-to-gateway-ca-certificate>
    ```

    The chart also supports the legacy inline certificate approach with `AKEYLESS_GW_CERTIFICATE`, but using `gatewayCert.tlsCertsSecretName` is the recommended method.

    > 👍 Note
    >
    > 1. When working with Red Hat OpenShift, enable the OpenShift flag in the **values.yaml** chart file: `openshiftEnabled: true`
    >
    > 2. Injecting secrets into the Namespace where the `k8s injector` plugin is installed is unsupported.

3. On your Kubernetes cluster, create and label a Namespace for Akeyless.

    ```shell
    kubectl create namespace akeyless
    kubectl label namespace akeyless name=akeyless
    ```

    Alternatively, for Red Hat OpenShift:

    ```shell
    oc create namespace akeyless
    oc label namespace akeyless name=akeyless
    ```

4. Deploy the Helm chart to the selected Namespace.

    ```shell
    helm install injector akeyless/akeyless-secrets-injection --namespace akeyless -f values.yaml
    ```

5. Validate the deployment state.

    ```shell
    kubectl get all -n akeyless
    ```

    Alternatively, for Red Hat OpenShift:

    ```text CLI
    oc get all -n akeyless
    ```

    The following is an example of the output:

    ```shell
    kubectl get all -n akeyless

    NAME                                                        READY      STATUS         RESTARTS     AGE
    pod/injector-akeyless-secrets-injection-77c857d496-r5xth         1/1        Running        1 (73s ago)  1d
    pod/injector-akeyless-secrets-injection-85c857e421-x6opa         1/1        Running        1 (73s ago)  1d

    NAME                                                        TYPE       CLUSTER-IP     EXTERNAL-IP  PORT(S)   AGE
    service/injector-akeyless-secrets-injection                      ClusterIP  10.97.228.133  <none>       443/TCP   1d

    NAME                                                        READY      UP-TO-DATE     AVAILABLE    AGE
    deployment.apps/injector-akeyless-secrets-injection              2/2        2              2            1d

    NAME                                                        DESIRED    CURRENT        READY        AGE
    replicaset.apps/injector-akeyless-secrets-injection-77c857d496   2          2              2           1d
    ```

### AKS Workload Identity (`azure_ad`) Example

To authenticate the injector with Azure Workload Identity on AKS, configure `AKEYLESS_ACCESS_TYPE: "azure_ad"` and run workloads with a ServiceAccount that is mapped to a federated Azure managed identity.

1. Configure the injector chart values.

    ```yaml values.yaml
    env:
      AKEYLESS_ACCESS_ID: "<Azure-AD-Access-ID>"
      AKEYLESS_ACCESS_TYPE: "azure_ad"
      AKEYLESS_API_GW_URL: "https://<Your-Gateway-URL>:8000/api/v1"
      # Optional. Set only to select a specific user-assigned identity.
      # AKEYLESS_AZURE_OBJ_ID: "<azure-object-id>"
    ```

2. Annotate the Kubernetes ServiceAccount used by the workload.

    ```yaml
    apiVersion: v1
    kind: ServiceAccount
    metadata:
      name: app-wi-sa
      namespace: akeyless
      annotations:
        azure.workload.identity/client-id: "<user-assigned-managed-identity-client-id>"
    ```

3. Label and annotate the workload that consumes Akeyless secrets.

    ```yaml
    apiVersion: apps/v1
    kind: Deployment
    metadata:
      name: wi-demo
      namespace: akeyless
    spec:
      replicas: 1
      selector:
        matchLabels:
          app: wi-demo
      template:
        metadata:
          labels:
            app: wi-demo
            azure.workload.identity/use: "true"
          annotations:
            akeyless/enabled: "true"
        spec:
          serviceAccountName: app-wi-sa
          containers:
            - name: wi-demo
              image: alpine
              command: ["sh", "-c", "echo $MY_SECRET; sleep 3600"]
              env:
                - name: MY_SECRET
                  value: akeyless:/K8s/my_k8s_secret
    ```

4. Validate projected Azure Workload Identity variables in the pod.

    ```shell
    kubectl exec -n akeyless deploy/wi-demo -- printenv | grep AZURE_
    ```

Expected output includes these values:

* `AZURE_CLIENT_ID`
* `AZURE_TENANT_ID`
* `AZURE_FEDERATED_TOKEN_FILE`

> ℹ️ **Note:**
>
> `AKEYLESS_AZURE_OBJ_ID` is not required for the default AKS Workload Identity flow. Set it only when a specific user-assigned identity must be selected.

## Launch an Application

The Akeyless Injector supports the following modes of operations, using **Environment Variables**, **File Injection**, and **SideCar** mode which can work only with File Injection.

### Environment Variable

Set the following annotations in your deployment `YAML` files:

Enable the plugin under the `annotations` section, in your app deployment file:

```yaml
akeyless/enabled: "true"
```

To inject your secret into your pod environment variable during the `init` phase, the value of your `env` should be set with `akeyless:/Path/to/secret`.

The following example demonstrates Akeyless secret injection as an **Environment Variable** into an alpine deployment:

```yaml env.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: test
spec:
  replicas: 1
  selector:
    matchLabels:
      app: hello-secrets
  template:
    metadata:
      labels:
        app: hello-secrets
      annotations:
        akeyless/enabled: "true"
    spec:
      containers:
      - name: alpine
        image: alpine
        command:
          - "sh"
          - "-c"
          - "echo $MY_SECRET && echo going to sleep... && sleep 10000"
        env:
        - name: MY_SECRET
          value: akeyless:/K8s/my_k8s_secret
```

Apply:

```shell
kubectl apply -f env.yaml
```

The following example demonstrates Akeyless secret injection as an **Environment Variable** into MySQL Database and WordPress server deployments:

```yaml MySQLWordPress.yaml
apiVersion: v1
kind: Service
metadata:
  name: wordpress-mysql
  labels:
    app: wordpress
spec:
  ports:
    - port: 3306
  selector:
    app: wordpress
    tier: mysql
  clusterIP: None
---
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: mysql-pv-claim
  labels:
    app: wordpress
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 20Gi
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: wordpress-mysql
  labels:
    app: wordpress
spec:
  selector:
    matchLabels:
      app: wordpress
      tier: mysql
  strategy:
    type: Recreate
  template:
    metadata:
      labels:
        app: wordpress
        tier: mysql
      annotations:
        akeyless/enabled: "true"
    spec:
      containers:
      - image: bitnami/mysql:5.7.33
        name: mysql
        env:
        - name: MYSQL_ROOT_PASSWORD
          value: akeyless:/K8s/my_k8s_secret
        ports:
        - containerPort: 3306
          name: mysql
        volumeMounts:
        - name: mysql-persistent-storage
          mountPath: /var/lib/mysql
      volumes:
      - name: mysql-persistent-storage
        persistentVolumeClaim:
          claimName: mysql-pv-claim
```
```yaml Wordpress.yaml
apiVersion: v1
kind: Service
metadata:
  name: wordpress
  labels:
    app: wordpress
spec:
  ports:
    - port: 80
  selector:
    app: wordpress
    tier: frontend
  type: LoadBalancer
---
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: wp-pv-claim
  labels:
    app: wordpress
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 20Gi
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: wordpress
  labels:
    app: wordpress
spec:
  selector:
    matchLabels:
      app: wordpress
      tier: frontend
  strategy:
    type: Recreate
  template:
    metadata:
      labels:
        app: wordpress
        tier: frontend
      annotations:
        akeyless/enabled: "true"
    spec:
      containers:
      - image: wordpress:4.8-apache
        name: wordpress
        env:
        - name: WORDPRESS_DB_HOST
          value: wordpress-mysql
        - name: WORDPRESS_DB_PASSWORD
          value: akeyless:/K8s/my_k8s_secret
        ports:
        - containerPort: 80
          name: wordpress
        volumeMounts:
        - name: wordpress-persistent-storage
          mountPath: /var/www/html
      volumes:
      - name: wordpress-persistent-storage
        persistentVolumeClaim:
          claimName: wp-pv-claim
```

Apply:

```shell
kubectl apply -f MySQLWordPress.yaml
kubectl apply -f Wordpress.yaml
```

Another example demonstrates fetching secret specific versions for example `version=2` of the secret `my_k8s_secret` in the `K8s` folder, decode in Base64:

```yaml
- name:  MY_SECRET
  value: 'akeyless:/K8s/my_k8s_secret|decode=base64|version=2'
```

Or to extract a specific key from a secret that contains a `JSON` structured data:

```yaml
- name:  MY_JSON_SECRET
  value: 'akeyless:/K8s/secret-json|jq=.json_key'
```

Alternatively, you can parse the entire `JSON` keys automatically into environment variables using:

```yaml
- name:  MY_JSON_SECRET
  value: 'akeyless:/K8s/secret-json|parse_json_secret=true'        
```

This will create an environment variable per **each** key that exists within the `JSON` using the following format:`MY_JSON_SECRET_JSON_KEY_NAME`.

To create the environment variables without the prefix you can use the `parse_json_without_prefix` flag instead.

> ℹ️ **Note:**
>
> The `parse_json_secret` flag is designed to handle flat JSON structures with single string-values (it does not support nested JSONs, nor array values).

#### Inject Secret by way of ConfigMap

For existing environments that currently use ConfigMaps with Kubernetes secrets, you can modify your config maps to fetch the relevant secrets from Akeyless, instead of updating all your deployment manifest files, for example:

```yaml ConfigMap
kind: ConfigMap
apiVersion: v1
metadata:
  name: akeyless-config-map
data:
  MYSQL_ROOT_PASSWORD: "akeyless:/K8s/my_k8s_secret"
```

And the corresponding deployment:

```yaml env.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: test
spec:
  replicas: 1
  selector:
    matchLabels:
      app: hello-secrets
  template:
    metadata:
      labels:
        app: hello-secrets
      annotations:
        akeyless/enabled: "true"
    spec:
      containers:
      - name: alpine
        image: alpine
        command:
          - "sh"
          - "-c"
          - "echo $MY_SECRET && echo going to sleep... && sleep 10000"
        env:
        - name: MY_SECRET
          valueFrom:
            configMapKeyRef:
              name: akeyless-config-map
              key: MYSQL_ROOT_PASSWORD               
```

#### Override Entrypoint Automatically

The injector can be set with credentials of your **private** registry using a secret reference that exists inside Akeyless, this secret should contain a JSON with credentials to your registry, supporting either username and password or a simple token format, for example:

```json Username and Password
{
  "username": "",
  "password": ""
}
```
```json Token
{
  "token": "<value>"
}
```

this secret can be set globally on the deployment using this variable `AKEYLESS_REGISTRY_CREDS = /Path/to/secret` or explicitly on the pod level using this annotation: `akeyless/registry_creds: /Path/to/secret`.

Once this secret is provided the manual command is not required, and the Injector will override the entrypoint automatically.

In AWS and GCP environments the node IAM role on EKS and GKE respectively can be used automatically to fetch private images from AWS ECR and GCP GAR respectively, hence no secret reference is required.

> ℹ️ **Note (Public Container Registry):**
>
> For public container registry no secret is required, the Injector will try to override the entrypoint automatically.

### File Injection

Enable the plugin under the `annotations` section, in your app deployment file:

```yaml
akeyless/enabled: "true"
```

The default location of the Akeyless secrets folder inside your pod file system is **/akeyless/secrets/**.

To explicitly set a different location you can override this by adding `|location=<path>` after your secret name within the annotation.

For example, `/K8s/my_k8s_secret` and `/K8s/my_k8s_secret2` will be saved inside your pod filesystem under the **/tmp/** folder as `secret1` and `secret2` respectively.

```yaml
akeyless/inject_file: "/K8s/my_k8s_secret|location=/tmp/secret1,/K8s/my_k8s_secret2|location=/tmp/secret2"
```

You can specify different destinations for file injection for multiple secrets using the following format: `akeyless/inject_file_*`.

In this example, we will inject different secrets into different locations:

```yaml
akeyless/inject_file_s1: "/K8s/secret-json|jq=.object.first|location=/tmp/secret_json|permission=0777|decode=base64"
akeyless/inject_file_secret2: "/K8s/my_k8s_secret|location=/akeyless/secret2" 
akeyless/inject_file_secret1: "/K8s/my_k8s_secret2"
```

To inject an entire folder of secrets from Akeyless, for example, all secrets under `/K8s/my-secrets-folder` will be injected into the pod `fs` under `/tmp/secrets/K8s/<secrets-full-name>`:

```yaml
akeyless/inject_folder: "/K8s/my-secrets-folder/|location=/tmp/secrets/"
```

To inject only the secrets from the source folder without the full folders structure from Akeyless, for example all secrets under `/K8s/my-secret-folder` use the following pipe command with the annotation:

```yaml
akeyless/inject_folder: "/K8s/my-secrets-folder/|folder_location=/tmp/secrets/"
```

To modify the default target folder location of the Akeyless secrets on your pods' file, you can use this setting on the injector chart `values.yaml` file.

```shell values.yaml
AKEYLESS_SECRET_DIR_NAME: "/My/New/Dir" #Path to save secrets inside pod's file systems
```

The following example demonstrates Akeyless secret injection with file injection into an alpine deployment:

```yaml Injectfile.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: test-file
spec:
  replicas: 1
  selector:
    matchLabels:
      app: hello-secrets-2
  template:
    metadata:
      labels:
        app: hello-secrets-2
      annotations:
        akeyless/enabled: "true"
        akeyless/inject_file: "/K8s/my_k8s_secret"
    spec:
      containers:
      - name: alpine
        image: alpine
        command:
          - "sh"
          - "-c"
          - "cat /akeyless/secrets/K8s/my_k8s_secret && echo going to sleep... && sleep 10000"
```

Apply:

```shell
kubectl apply -f Injectfile.yaml
```

### Sidecar Mode

To keep track of secret changes while reflecting them into your pods during their lifetime, you can use the **Sidecar** mode, for example, while working with **Dynamic** or **Rotated** secrets.

Enable the plugin under the `annotations` section, in your app deployment file and enable the sidecar mode by adding the following annotations:

```yaml
akeyless/enabled: "true"
akeyless/side_car_enabled: "true"
```

Set the desired refresh interval for the sidecar where the units are `Int` and the supported time units are `"s"`, `"m"` or `"h"`:

```yaml
akeyless/side_car_refresh_interval: "30m"
```

To retrieve multiple versions of your secret simultaneously (only for **Static** and **Rotated**):

```yaml
akeyless/side_car_versions_to_retrieve: "2"
```

The following example demonstrates secret injection with sidecar mode into an alpine deployment:

```yaml Akeyless_sidecar.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: test-file-sidecar
spec:
  replicas: 1
  selector:
    matchLabels:
      app: file-secrets
  template:
    metadata:
      labels:
        app: file-secrets
      annotations:
        akeyless/enabled: "true"
        akeyless/inject_file: "/K8s/my_k8s_secret|location=/secrets/secretsVersion.json" 
        akeyless/side_car_enabled: "true"
        akeyless/side_car_refresh_interval: "30m"
        akeyless/side_car_versions_to_retrieve: "2"
    spec:
      containers:
      - name: alpine
        image: alpine
        command:
          - "sh"
          - "-c"
          - "while true; do [ ! -f /secrets/timestamp ] || [ /secrets/secretsVersion.json -nt /secrets/timestamp ] && touch /secrets/timestamp && cat /secrets/secretsVersion.json && echo ''; sleep 15; done"
```

Apply:

```shell
kubectl apply -f Akeyless_sidecar.yaml
```

### Restart Rollout

Restart rollout tracks secret updates and triggers workload rollout restarts so pods reload updated secret values. This feature runs in the injector webhook server pod, not in application pods.

> ❗ **Important (Auth Method Requirements):**
>
> The injector authenticates to Akeyless using credentials configured in its own deployment, such as `AKEYLESS_ACCESS_ID` and `AKEYLESS_ACCESS_TYPE`, and polls for changes through the `list-items` API.
>
> The injector identity must have both `list` and `read` permissions on monitored secret paths. If a Kubernetes Auth Method is scoped with a namespace claim for an application namespace, for example `namespace=my-app-ns`, the injector token can fail to match when the injector runs in a different namespace such as `akeyless`.
>
> In this case, `list-items` can return empty results without errors, and restart rollout does not trigger.

To resolve namespace-scope mismatches:

* Add a second role-auth-method association with a namespace claim for the injector namespace, for example `namespace=akeyless`, and grant `list` and `read` on the required paths.
* Configure a separate Auth Method for the injector that is not restricted by an application namespace claim.

## Annotations List

The following table lists the available annotations:

| Annotation | Options | Description |
| --- | --- | --- |
| `akeyless/enabled: "true"` | `"true"` or `"false"` | Enable the Kubernetes plugin. |
| `akeyless/side_car_enabled: "true"` | `"true"` or `"false"` | Set the Kubernetes plugin to work in sidecar mode. |
| `akeyless/disable_restart_rollout: "true"` | `"true"` or `"false"` | Disable the restart-rollout on a specific deployment. Note that this annotation is presence-based: any value, including `"false"`, disables restart rollout. To re-enable restart rollout, remove the annotation. |
| `akeyless/side_car_refresh_interval: "30m"` | `Int` followed by `"s"`, `"m"`, or `"h"` units | Set the desired refresh time interval for the Akeyless sidecar. Default is `30m`. |
| `akeyless/side_car_versions_to_retrieve: "2"` | `"2"` or higher | Fetch the last X versions of your secret. |
| `akeyless/inject_file: "/mysecret/\|location=/path to save secret name"` | `location=/path to save secret name` | Set the location for your secrets to be saved within your pod file system. **Note:** Available for files only. |
| `akeyless/inject_file: "/mysecret\|permission=0644"` | `permission=0644` | Set the permission of the file that contains your secret value. Default is `0644`. **Note:** Available for files only. |
| `akeyless/inject_file: "/mysecret\|version=1"` | `version={version number}` | Fetch a specific version of your secret. Default is the latest version. **Note:** Available for environment variables as well. |
| `akeyless/inject_file: "/mysecret\|decode=base64"` | `decode=none` or `base64` | Set the decoding for your encoded secret values. Default is `none`. **Note:** Available for environment variables as well. |
| `akeyless/inject_file: "/mysecret\|jq={jq-expression}"` | `jq` expression | Use `jq={jq-expression}` (for example, secret items that contain a JSON structure can be parsed directly). |
| `akeyless/inject_folder: "/prod/my-secrets-folder/\|permission=0644"` | `permission=0644` | Set the permission of the folder that contains your secret value. Default is `0644`. **Note:** Available for files only. |
| `akeyless/inject_folder: "/prod/my-secrets-folder/\|location=/tmp/secrets/\|track-folder-changes=true"` | `track-folder-changes=true` or `false` | Track injected folder changes to sync new secrets. |
| `akeyless/volume: "<Volume Name>"` | Volume name | Work with a custom volume. `MountPath` must also be set in the prefix of the injected secret location. Volume required permissions: `read/write`. |
| `akeyless/post_inject_script: \|` `#!/bin/bash` `echo Hello > /akeyless/secrets/hello.txt` | Script to execute post-fetching the secret | **Note:** Execution occurs in the init container and in the sidecar container (if set). |
| `akeyless:/<usc name>\|usc_remote_secret_name=<remote name>` | USC remote secret name (`string`) | Name of the remote secret to inject. Relevant only when working with Universal Secrets Connector. |
| `akeyless:/<usc name>\|usc_remote_secret_name=<remote name>\|usc_remote_secret_version=1` | USC remote secret version (`int`) | Remote secret version to inject. Relevant only when working with Universal Secrets Connector. |
| `akeyless:/<usc name>\|usc_remote_secret_name=<remote name>\|usc_remote_secret_namespace=default` | USC remote secret namespace (`string`) | Remote secret namespace. Relevant only when working with Universal Secrets Connector. |
| `akeyless/crash_on_error: "true"` | Crash the pod on injection failures | Can be controlled globally for all deployments, or explicitly. |
| `akeyless/ignore_cache: "true"` | Bypass cache to fetch the latest secret value | Can be controlled globally for all deployments, or explicitly. |
| `akeyless/registry_creds` | Path to a secret for Docker registry credentials | Relevant for environment variable mode. Can be used to override the entrypoint automatically. |
| `akeyless/agent_limits_cpu` | `Int` followed by `m` units | Limit of CPU usage (for example, `600m`, where `m` stands for milliCPU). |
| `akeyless/agent_requests_cpu` | `Int` followed by `m` units | CPU request (for example, `250m`, where `m` stands for milliCPU). |
| `akeyless/agent_limits_mem` | `Int` followed by `Mi` units | Limit of memory usage (for example, `64Mi`). |
| `akeyless/agent_requests_mem` | `Int` followed by `Mi` units | Memory request (for example, `64Mi`). |

## Metrics

To enable metrics collection from the injector using [Prometheus Operator](https://prometheus.io/), set the `metrics` setting to `true` in your `values.yaml` file:

At the moment, only the **Sidecar** injection type is supported.

```yaml values.yaml
metrics:
  enabled: true
```

Apply:

```shell
kubectl apply -f values.yaml
```

Verify that `podmonitor` was created:

```shell
kubectl get podmonitor
```

Expected output:

```shell
injector-akeyless-secrets-injection-scrape-pods
```

The `podmonitor` automatically discovers and collects metrics from pods running in a Kubernetes cluster, ensuring seamless integration with Prometheus for dynamic monitoring.

Now, [inject a secret](https://docs.akeyless.io/docs/akeyless-kubernetes-secrets-injector#launch-an-application) into your Kubernetes cluster.

Once done, the following metrics will be shown:

| Metric | Description |
| --- | --- |
| `akeyless_injector_system_http_response_status_code` | Tracks HTTP response status codes for the injectors |
| `akeyless_injector_system_request_count` | Counts the number of requests processed by the injectors |
| `container_cpu_usage_seconds_total` | Total CPU time consumed by a container in seconds. requires Node Exporter |
| `container_memory_usage_bytes` | Current memory usage of a container in bytes. requires Node Exporter |

These metrics are available for any pod matching the name pattern `injector-akeyless-secrets-injection`. If your injector pods have a different name, update the label selector pod=`~"injector-akeyless-secrets-injection.*"` accordingly.

The metrics can be viewed using monitoring tools like [Grafana](https://grafana.com/) or the Prometheus U.

## Scalability guidance for Gateway and Injector

Use the following sizing baselines for production Kubernetes environments that use both Akeyless Gateway and Akeyless Kubernetes Secrets Injector. The planning table assumes a single Kubernetes auth configuration unless noted, adequately sized worker nodes, and a healthy Injector webhook. Start with these values and adjust based on metrics such as request latency and Gateway response time.

### Gateway TokenReview environment variables

`K8S_TOKEN_REVIEW_QPS` and `K8S_TOKEN_REVIEW_BURST` are optional Gateway runtime environment variables (Gateway 4.53.0+). They control TokenReview client rate limits for `native_k8s` auth. They are **not** required for normal deployments.

Set them only when Kubernetes client-side TokenReview throttling appears in Gateway logs during large concurrent injection bursts. A typical log line looks like:

```text
Waited for <duration> due to client-side throttling, not priority and fairness, request: POST:.../apis/authentication.k8s.io/v1/tokenreviews
```

When that throttling is observed, raise the limits using the `K8S_TOKEN_REVIEW_QPS` and `K8S_TOKEN_REVIEW_BURST` values from the planning table for your peak concurrent inject scale. Add them as environment variables on the Gateway container (Helm values `env` / deployment `env`), not as Kubernetes Auth Method create/update flags:

```yaml
env:
  - name: K8S_TOKEN_REVIEW_QPS
    value: "<qps-from-planning-table>"
  - name: K8S_TOKEN_REVIEW_BURST
    value: "<burst-from-planning-table>"
```

* If unset, Gateway uses the Kubernetes client-go defaults: `QPS=5` and `Burst=10`.
* Prefer raising `K8S_TOKEN_REVIEW_QPS` for capacity and latency. Raising Burst alone (for example `100` QPS with `200` Burst versus `100`/`100`) has little effect at high concurrency.
* For configuration details, see [TokenReview Rate Limit Configuration](https://docs.akeyless.io/docs/cli-reference-k8s-auth-method#tokenreview-rate-limit-configuration-gateway-4530).

One Gateway replica can handle on the order of **1000–2500** concurrent inject pods when queue drain time and injection latency stay below both the Kubernetes mutating webhook timeout (`30` seconds) and the Injector HTTP timeout (typically about `55` seconds). The Injector timeout does not extend the API server’s admission window — keep latency under the `30`-second webhook limit. A second Gateway replica further reduces latency and is recommended above 1000 pods for headroom/HA. Injector replica count has little effect on inject latency once TokenReview limits match the table; run at least two injectors for availability.

Use this planning table for Gateway replicas, Injector replicas, and TokenReview environment variable values:

| Peak concurrent pods | Min Gateway replicas | Recommended Gateway replicas | Recommended Injector replicas | `K8S_TOKEN_REVIEW_QPS` | `K8S_TOKEN_REVIEW_BURST` |
| --- | --- | --- | --- | --- | --- |
| <= 50 | 1 | 1 | 1 - 2 | unset (defaults `5`) | unset (defaults `10`) |
| 51 - 150 | 1 | 1 | 2 | 50 | 100 |
| 151 - 300 | 1 | 1 - 2 | 2 | 50 | 100 |
| 301 - 500 | 1 | 1 - 2 | 2 | 100 | 100 |
| 501 - 750 | 1 | 1 - 2 | 2 | 100 | 100 |
| 751 - 1000 | 1 | 1 - 2 | 2 | 100 | 100 |
| 1001 - 2500 | 1 | 2 | 2 | 100 | 100 |
| Over 2500 | 2 | `2 + ceil((p - 2500) / 1500)` (for example, 2501–4000 → 3) | 2 | 100 | 100 |

### Advanced sizing formulas

Use these variables:

* `p`: peak concurrent pods that request secrets injection.
* `r`: required Gateway replica count.
* `i`: required Injector replica count.
* `k`: number of Kubernetes auth configurations used by Gateway.

For Gateway with one Kubernetes auth configuration (`k=1`):

* For `p <= 2500`: minimum starting point `r = 1`; recommended `r = 1`–`2` (prefer `2` when `p > 1000` for latency headroom/HA)
* For `p > 2500`: minimum starting point `r = 2`; recommended `r = 2 + ceil((p - 2500) / 1500)` — add **1** Gateway replica per additional **1500** concurrent inject pods (for example, **2501–4000** → **3** Gateway replicas; **4001–5500** → **4**)

For Gateway with multiple Kubernetes auth configurations:

* Effective per-replica throughput scales by `k`.
* Apply the same bands as above, then reduce replica count by roughly a factor of `k` (at least `1`, or `2` when `p > 2500`).

Relying on a single Kubernetes auth configuration for bursts above about **5000–6000** concurrent injections can lead to HTTP **429** rate limiting. Each injected pod issues **3** Gateway requests (`auth`, `describe-item`, and `get-secret-value`). If you approach that scale, split Injector Kubernetes auth across multiple auth configurations.

For Injector:

* Recommended starting point: `i = 2` for availability and webhook headroom (do not scale injectors primarily to reduce inject latency once TokenReview limits match the planning table).

### Webhook timeout guidance

* Set the mutating webhook timeout to `30` seconds when sizing for large concurrent bursts.
* Keep Gateway queue drain time and injection latency below both the mutating webhook timeout (`30` seconds) and the Injector HTTP timeout (typically about `55` seconds). The Injector timeout cannot extend the API server’s `30`-second admission limit.
* If queue drain time approaches the timeout, confirm TokenReview QPS/Burst environment variables match the planning table when throttling is observed, then increase Gateway replicas; tune Injector replicas mainly for availability.

### Deployment optimization for injector latency

Define both `command` and `args` in workload manifests when possible. This reduces injector processing time during pod mutation.

* If `command` and `args` are not set, the injector resolves startup behavior from image metadata.
* If `command` is set, it overrides the container image `ENTRYPOINT`.
* If `args` is set, it overrides the container image `CMD`.

Example:

```yaml
containers:
  - name: app
    image: my-app:latest
    command: ["/bin/myapp"]
    args: ["--debug"]
```

For operational metrics and alerting baselines, monitor Injector metrics in [Metrics](https://docs.akeyless.io/docs/akeyless-kubernetes-secrets-injector#metrics) together with Gateway metrics in [Gateway telemetry and metrics](https://docs.akeyless.io/docs/gateway-telemetry-and-metrics).

## Pod scheduling for high availability

The `akeyless-k8s-secrets-injection` chart exposes pod scheduling controls under the `deployment` key (`nodeSelector`, `tolerations`, `affinity`, `topologySpreadConstraints`). For conceptual guidance and examples, see [Pod scheduling for high availability](https://docs.akeyless.io/docs/gateway-best-practices#pod-scheduling-for-high-availability-kubernetes).

When applying those examples to the Injector chart, note the following schema differences from the Gateway chart:

* `tolerations` and `topologySpreadConstraints` each use `enabled`/`data` sub-keys instead of a flat list. To enable `tolerations`, set `deployment.tolerations.enabled: true` and add entries under `deployment.tolerations.data`. Apply the same pattern for `deployment.topologySpreadConstraints`.
* `topologySpreadConstraints` is rendered independently — it does not require `affinity.enabled: true` (unlike the Gateway chart).
* Injector pods carry an `app` label computed from the Helm release name (typically `<release-name>-akeyless-k8s-secrets-injection`). Verify this label against a running pod before using it in affinity or spread rule label selectors.

The following example shows the `enabled`/`data` schema for `tolerations` and `topologySpreadConstraints` in the Injector chart. Replace `<release-name>` with your Helm release name:

```yaml values.yaml
deployment:
  tolerations:
    enabled: true
    data:
      - key: "dedicated"
        operator: "Equal"
        value: "injector"
        effect: "NoSchedule"
  topologySpreadConstraints:
    enabled: true
    data:
      - maxSkew: 1
        topologyKey: topology.kubernetes.io/zone
        whenUnsatisfiable: ScheduleAnyway
        labelSelector:
          matchLabels:
            app: <release-name>-akeyless-k8s-secrets-injection
      - maxSkew: 1
        topologyKey: kubernetes.io/hostname
        whenUnsatisfiable: ScheduleAnyway
        labelSelector:
          matchLabels:
            app: <release-name>-akeyless-k8s-secrets-injection
```

## Troubleshooting

When you are working with a GKE cluster, make sure that port **8443** is opened in your firewall rules, This port is needed by the Akeyless Secret Injection mutating webhook. Update your firewall rule as follows:

1. Review the firewall rule for access:

    ```shell
    gcloud compute firewall-rules list
    ```

2. Replace the existing rule and allow access:

    ```shell
    gcloud compute firewall-rules update <firewall-rule-name> --allow tcp:10250,tcp:443,tcp:8443
    ```

### Restart rollout does not trigger

If restart rollout is enabled but workloads do not restart after secret changes, use the following checks:

1. Check injector pod logs for `restart-rollout` or `list items change` messages. If restart-related logs are missing, the restart manager might not have started.
2. Verify that `RESTART_ROLLOUT` is set to `enable` in the injector deployment environment variables.
3. Ensure `akeyless/disable_restart_rollout` is not present on the target workload. Presence of this annotation with any value disables restart rollout.
4. Confirm the injector Auth Method grants `list` and `read` from the injector namespace, not only from the application namespace.
5. Verify leader election:

    ```shell
    kubectl get lease -n <injector-ns> akeyless.injector -o yaml
    ```

    The `holderIdentity` value should match a running injector pod.
6. Confirm the target workload type is `Deployment`, `DaemonSet`, or `StatefulSet`. OpenShift `DeploymentConfig` is not supported.

## Tutorial

Check out our tutorial video on [Injecting Secrets into a Kubernetes Cluster](https://tutorials.akeyless.io/docs/injecting-secrets-into-a-kubernetes-cluster).
