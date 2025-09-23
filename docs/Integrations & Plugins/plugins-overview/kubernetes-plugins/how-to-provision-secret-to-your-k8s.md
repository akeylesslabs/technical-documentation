---
title: Akeyless K8s Secrets Injector
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
# Overview

The Akeyless K8s Secrets Injector plugin enables K8s applications and workloads to use [Static](doc:static-secrets), [Rotated](https://docs.akeyless.io/docs/rotated-secrets), and [Dynamic](doc:how-to-create-dynamic-secret) secrets as well as [Certificates](doc:certificate-storage)  and [USC](doc:universal-secrets-connector) sourced from the Akeyless Platform.

This injector leverages the K8s `MutatingAdmissionWebhook` to intercept and augment specifically annotated pod configurations for secrets injection. By doing so, the user benefits as the applications remain ״Akeyless unaware״ as the secrets are stored either as an **environment variable** or as a file at a **filesystem path** in their container.

Before the application starts, the injector deploys an **init** container to fetch and inject secrets at pod start-up, after which the init-container shuts down. To apply an automatic [rollout restart](https://kubernetes.io/docs/reference/kubectl/generated/kubectl_rollout/kubectl_rollout_restart/) to your deployments upon **any** change to your secrets, you can use the Injector with restart-rollout mode, which can track any changes of [Static](doc:static-secrets), [Rotated](https://docs.akeyless.io/docs/rotated-secrets) and  [Certificates](doc:certificate-storage).

If the application consumes secrets which regularly change, an annotation can be used to deploy an additional **Sidecar** container which runs alongside the application to monitor changes in secrets. The **Sidecar** tracks and updates secrets within injected files inside the pods, according to specifically annotated pod configurations, and will remain up for the entire application lifecycle. Relevant for cases where the app can watch for live changes in files.

Although authorization in K8s is intentionally high level, you can configure the injector to support full and flexible segregation using K8s policies together with the Akeyless Platform's [Role-based Access Control (RBAC)](doc:rbac).\
For details, see [Policy Segregation for Kubernetes](doc:policy-segregation-for-kubernetes).

<Image align="center" src="https://files.readme.io/dd531a9-Akeyless_Rebranded_Infographics_1.png" />

> 👍 Note
>
> The documentation, configuration and examples for the plugin are also applicable to **Red Hat OpenShift** environment.

# Prerequisites

* Helm Installed.

* **K8s Auth** or one of the supported [Authentication Methods for Kubernetes](https://docs.akeyless.io/docs/auth-meth-k8s).

* `K8s v1.19` and above.

* For Azure Kubernetes Service (AKS), **managed-identity** is enabled on your AKS cluster.

* For Google Kubernetes Engine (GKE) cluster, port **8443** is opened in your Google Cloud Platform (GCP) firewall rules.

## Create a Secret in Akeyless

For example, the following command creates a static secret called **my\_k8s\_secret** inside  **K8s** folder.

```shell Akeyless CLI
akeyless create-secret --name /K8s/my_k8s_secret --value myPassword
```

Alternatively, a secret can contain `JSON` structured data, for example: 

```shell Akeyless CLI
akeyless create-secret --name /K8s/secret-json --value '{"aws_access_key":"1234","aws_key_id":"abcd"}'
```

> 👍 Note
>
> The following example uses a pre-defined [K8s Auth](doc:kubernetes-auth) called **K8s\_Auth** in **K8s** folder i.e. `K8s/K8s_Auth`

## Create an Access Role

Create an [Access Role](doc:rbac) associate the role with an **Auth Method** and grant access to the secret.\
For example, the following command creates **K8s\_role** role, the role is associated to **K8s\_Auth** Auth Method, and grant **read** and **list** access to all the secrets in **K8s** folder

```shell Akeyless CLI
akeyless create-role --name /K8s/K8s_Role
akeyless assoc-role-am --role-name /K8s/K8s_Role --am-name K8s/K8s_Auth
akeyless set-role-rule --role-name /K8s/K8s_Role --path /K8s/'*' --capability read --capability list
```

# Install the Injector

1. Add the Akelyess K8s Injector Helm repository from [here](https://github.com/akeylesslabs/helm-charts/tree/main/charts/akeyless-k8s-secrets-injection) and update your Helm repositories.

```shell CLI
helm repo add akeyless https://akeylesslabs.github.io/helm-charts
helm repo update
```

2. Fetch the **values.yaml** file locally:

```shell CLI
helm show values akeyless/akeyless-secrets-injection > values.yaml
```

Modify the following values under the `env` section as follows:

* Set `AKEYLESS_ACCESS_ID` to the Access ID of the Auth Method with access to the secret.

* Set `AKEYLESS_ACCESS_TYPE` to `k8s`. Or with any other supported [Authentication Methods for Kubernetes](doc:auth-meth-k8s).

* Set `AKEYLESS_K8S_AUTH_CONF_NAME` with your Gateway Kubernetes Auth name. Relevant **only** for Access type of `k8s`.

* Set `AKEYLESS_API_GW_URL` with the URL of your Gateway API v1 endpoint: `/8000/api/v1` or port `8080`.

* Optional  `AKEYLESS_CRASH_POD_ON_ERROR` Upon any failure, a pod that tries to fetch a secret and fails will crash. By default this option is disabled. Can be controlled globally or at the deployment level using a dedicated [annotation](https://docs.akeyless.io/docs/how-to-provision-secret-to-your-k8s#annotations-list).

* Optional `restartRollout`: to apply automatic rollout restart to your deployments upon secret changes. Relevant only for the kinds of: `Deployment`, `DaemonSet` or `StatefulSet`.  To control which deployments are not effected by the restart-rollout, you can use a dedicated [annotation](https://docs.akeyless.io/docs/how-to-provision-secret-to-your-k8s#annotations-list) to disable this on the deployment level. 

* `AKEYLESS_REGISTRY_CREDS`: a reference to an existing secret that holds your container registry credentials. Relevant when working with Environment variables and a **private** container registry, to [override automatically ](https://docs.akeyless.io/docs/how-to-provision-secret-to-your-k8s#override-entrypoint-automatically)the docker entrypoint, can be utilized at the deployment level using a dedicated [annotation](https://docs.akeyless.io/docs/how-to-provision-secret-to-your-k8s#annotations-list). not required for **public**  registry.  

* Optional `AKEYLESS_IGNORE_CACHE`:  to allow bypassing the Gateway cache when fetching secrets, ensuring access to the latest data, which is `disabled` by default. can be utilized at the deployment level using a dedicated [annotation](https://docs.akeyless.io/docs/how-to-provision-secret-to-your-k8s#annotations-list)  

* Optional `INIT_RUN_AS_USER`: To apply a [Security Context](https://kubernetes.io/docs/tasks/configure-pod-container/security-context/) to your init container, set the following environment variable,  `INIT_RUN_AS_USER: "id=65534"`.

```yaml
 restartRollout:
  enabled: false
  interval: 1m
  
env:
  AKEYLESS_ACCESS_ID: "<AccessID>"
  AKEYLESS_ACCESS_TYPE: "k8s"
  AKEYLESS_K8S_AUTH_CONF_NAME: "K8s_Auth_Name"
  AKEYLESS_API_GW_URL: "https://Your-Gateway-URL:8000/api/v1" 
 # AKEYLESS_CRASH_POD_ON_ERROR: "enable"
 # AKEYLESS_IGNORE_CACHE: "enable"
```

> 👍 Note
>
> 1. When working with Red Hat OpenShift, enable the OpenShift flag in the **values.yaml** chart file: `openshiftEnabled: true`
>
> 2. Injecting secrets into the namespace where the `k8s injector` plugin is installed is unsupported.

3. On your K8s cluster, create and label a namespace for Akeyless.

```shell CLI
kubectl create namespace akeyless
kubectl label namespace akeyless name=akeyless
```

Alternatively, for Red Hat OpenShift:

```shell CLI
oc create namespace akeyless
oc label namespace akeyless name=akeyless
```

4. Deploy the Helm chart to the selected namespace.

```shell CLI
helm install injector akeyless/akeyless-secrets-injection --namespace akeyless -f values.yaml
```

5. Validate the deployment state.

```shell CLI
kubectl get all -n akeyless
```

Alternatively, for Red Hat OpenShift:

```text CLI
oc get all -n akeyless
```

The following is an example of the output:

```shell CLI
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

# Launch an Application

The Akeyless Injector supports the following modes of operations, using **Environment Variables**, **File Injection**, and **SideCar** mode which can work only with File Injection. 

## Environment Variable

Set the following annotations in your deployment `YAML` files: 

Enable the plugin under the `annotations` section, in your app deployment file:

```yaml
akeyless/enabled: "true"
```

To inject your secret into your pod environment variable during the `init` phase, the value of your `env` should be set with  `akeyless:/Path/to/secret`.

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

Another example demonstrates fetching secret specific versions for example `version=2` of the secret `my_k8s_secret` in the `K8s` folder,  decode in base64:

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

This will create an environment variable per **each** key that exists within the `JSON`  using the following format:`MY_JSON_SECRET_JSON_KEY_NAME`.

To create the environment variables without the prefix you can use the `parse_json_without_prefix` flag instead.

> 📘 Note
>
> The `parse_json_secret` flag is designed to handle flat JSON structures with single string-values (it does not support nested JSONs, nor array values).

### Inject Secret via ConfigMap

For existing environments that currently use ConfigMaps with K8s secrets, you can modify your config maps to fetch the relevant secrets from Akeyless, instead of updating all your deployment manifest files, for example:

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

### Override Entrypoint Automatically

The injector can be set with credentials of your **private** registry using a secret reference that exists inside Akeyless, this secret should contain a JSON with creds to your registry, supporting either username & password or a simple token format, for example:

```json Username & Password
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

In AWS and GCP environments the node IAM role on EKS and GKE respectively can be utilized automatically to fetch private images from AWS ECR and GCP GAR respectively, hence no secret reference is required.

> 👍 Public Container Registry
>
> For public container registry no secret is required, the Injector will try to override the entrypoint automatically.

## File Injection

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

```yaml YAML
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

## Sidecar Mode

To keep track of secret changes while reflecting them into your pods during their lifetime, you can use the **Sidecar** mode, for example, while working with **Dynamic** or **Rotated** secrets. 

Enable the plugin under the `annotations` section, in your app deployment file and enable the sidecar mode  by adding the following annotations:

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

# Annotations List

The following table lists the available annotations:  

<Table align={["left","left","left"]}>
  <thead>
    <tr>
      <th>
        Annotation
      </th>

      <th>
        Options
      </th>

      <th>
        Description
      </th>
    </tr>
  </thead>

  <tbody>
    <tr>
      <td>
        `akeyless/enabled: "true"`
      </td>

      <td>
        `"true"` or `"false"`
      </td>

      <td>
        Enable the K8s plugin
      </td>
    </tr>

    <tr>
      <td>
        `akeyless/side_car_enabled: "true"`
      </td>

      <td>
        `"true"` or `"false"`
      </td>

      <td>
        Set the K8s plugin to work in sidecar mode
      </td>
    </tr>

    <tr>
      <td>
        `akeyless/disable_restart_rollout: "true"`
      </td>

      <td>
        `"true"` or `"false"`
      </td>

      <td>
        To disable the restart-rollout on a specific deployment
      </td>
    </tr>

    <tr>
      <td>
        `akeyless/side_car_refresh_interval: "30m"`
      </td>

      <td>
        `Int` followed by\
         `"s"`, `"m"`or `"h"` units
      </td>

      <td>
        Set the desired refresh time interval for the Akeyless sidecar, by default set to `30m`
      </td>
    </tr>

    <tr>
      <td>
        `akeyless/side_car_versions_to_retrieve: "2"`
      </td>

      <td>
        `"2"` or higher
      </td>

      <td>
        Fetch the last X versions of your secret
      </td>
    </tr>

    <tr>
      <td>
        `akeyless/inject_file: "/mysecret/\|location=/path to save secret name"`
      </td>

      <td>
        `location= /path to save secret name`
      </td>

      <td>
        Set the location for your secrets to be saved within your pod file system.  

        Note: Available for files only
      </td>
    </tr>

    <tr>
      <td>
        `akeyless/inject_file: "/mysecret\|permission=0644"`
      </td>

      <td>
        `permission= 0644`
      </td>

      <td>
        Set the permission of the file that contains your secret value  

        Default is `0644`  

        Note: Available for files only
      </td>
    </tr>

    <tr>
      <td>
        `akeyless/inject_file: "/mysecret\|version=1"`
      </td>

      <td>
        `version= {version number}`
      </td>

      <td>
        Fetch a specific version of your secret  

        The default value is set to the latest version  

        Note: Available for Environment variables as well
      </td>
    </tr>

    <tr>
      <td>
        `akeyless/inject_file: "/mysecret\|decode=base64"`
      </td>

      <td>
        `decode= none` or `base64`
      </td>

      <td>
        Set the decoding for your encoded secret values  

        Default is `none`  

        Note: Available for Environment variables as well
      </td>
    </tr>

    <tr>
      <td>
        `akeyless/inject_file: "/mysecret\|jq={jq-expresion}"`
      </td>

      <td>
        `jq` expression to work with conventional JSON data form
      </td>

      <td>
        jq=\{jq-expresion} e.g. secret items that contain JSON structure, can be parsed directly
      </td>
    </tr>

    <tr>
      <td>
        `akeyless/inject_folder: "/prod/my-secrets-folder/\|permission=0644"`
      </td>

      <td>
        `permission=0644`
      </td>

      <td>
        Set the permission of the folder that contains your secret value  

        Default is `0644`  

        Note: Available for files only
      </td>
    </tr>

    <tr>
      <td>
        `akeyless/inject_folder: "/prod/my-secrets-folder/\|location=/tmp/secrets/\|track-folder-changes=true"`
      </td>

      <td>
        `track-folder-changes=` `true` or `false`
      </td>

      <td>
        Track injected folder changes to sync new secrets
      </td>
    </tr>

    <tr>
      <td>
        `akeyless/volume: "<Volume Name>"`
      </td>

      <td>
        Volume name 
      </td>

      <td>
        To work with a custom volume. `MountPath` should also be set in the prefix of the injected secret location. Volume required permissions: `read/write` 
      </td>
    </tr>

    <tr>
      <td>
        `akeyless/post_inject_script: \|`\
          `#!/bin/bash`\
             `echo Hello > /akeyless/secrets/hello.txt`
      </td>

      <td>
        script to execute post-fetching the secret
      </td>

      <td>
        Note:\
        the execution occurs in the init container and at the sidecar container if set.
      </td>
    </tr>

    <tr>
      <td>
        `akeyless:/<usc name>\|usc_remote_secret_name=<remote name>`
      </td>

      <td>
        The USC remote secret name `string`
      </td>

      <td>
        The name of the remote secret to inject. Relevant only when working with Universal Secret Connector
      </td>
    </tr>

    <tr>
      <td>
        `akeyless:/<usc name>\|usc_remote_secret_name=<remote name>\|usc_remote_secret_version=1`
      </td>

      <td>
        The USC remote secret version `int`
      </td>

      <td>
        The remote secret version to inject. Relevant only when working with Universal Secret Connector
      </td>
    </tr>

    <tr>
      <td>
        `akeyless:/<usc name>\|usc_remote_secret_name=<remote name>\|usc_remote_secret_namespace=default`
      </td>

      <td>
        The USC remote secret namespace `string`
      </td>

      <td>
        The remote secret namespace. Relevant only when working with Universal Secret Connector
      </td>
    </tr>

    <tr>
      <td>
        `akeyless/crash_on_error: "true"`
      </td>

      <td>
        Crash the pod on injection failures
      </td>

      <td>
        Can be controlled globally for all deployments, or explicitly. 
      </td>
    </tr>

    <tr>
      <td>
        `akeyless/ignore_cache: "true"`
      </td>

      <td>
        Bypass cache, to fetch the secret latest value
      </td>

      <td>
        Can be controlled globally for all deployments, or explicitly.
      </td>
    </tr>

    <tr>
      <td>
        `akeyless/registry_creds`
      </td>

      <td>
        Path to a secret for Docker registry creds, relevant for environment variable mode 
      </td>

      <td>
        Can be used to override the entrypoint automatically 
      </td>
    </tr>

    <tr>
      <td>
        `akeyless/agent_limits_cpu`
      </td>

      <td>
        `Int` followed by `m` units
      </td>

      <td>
        Limit of CPU usage\
        e.g. `600m`\
        where the unit suffix `m` stands for core thousandth (miliCPU)
      </td>
    </tr>

    <tr>
      <td>
        `akeyless/agent_requests_cpu`
      </td>

      <td>
        `Int` followed by `m` units
      </td>

      <td>
        Limit of CPU request\
         e.g. `250m`\
        where the unit suffix `m` stands for core thousandth (miliCPU)
      </td>
    </tr>

    <tr>
      <td>
        `akeyless/agent_limits_mem`
      </td>

      <td>
        `Int` followed by `Mi` units
      </td>

      <td>
        Limit of Memory usage, e.g. `64Mi`
      </td>
    </tr>

    <tr>
      <td>
        `akeyless/agent_requests_mem`
      </td>

      <td>
        `Int` followed by `Mi`units
      </td>

      <td>
        Limit of Memory request usage, e.g. `64Mi`
      </td>
    </tr>
  </tbody>
</Table>

# Metrics

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

Now, [inject a secret](https://docs.akeyless.io/docs/how-to-provision-secret-to-your-k8s#launch-an-application) into your k8s cluster.

Once done, the following metrics will be shown:

| Metric                                               | Description                                                               |
| :--------------------------------------------------- | :------------------------------------------------------------------------ |
| `akeyless_injector_system_http_response_status_code` | Tracks HTTP response status codes for the injectors                       |
| `akeyless_injector_system_request_count`             | Counts the number of requests processed by the injectors                  |
| `container_cpu_usage_seconds_total`                  | Total CPU time consumed by a container in seconds. requires Node Exporter |
| `container_memory_usage_bytes`                       | Current memory usage of a container in bytes. requires Node Exporter      |

These metrics are available for any pod matching the name pattern `injector-akeyless-secrets-injection`. If your injector pods have a different name, update the label selector pod=`~"injector-akeyless-secrets-injection.*"` accordingly.

The metrics can be viewed using monitoring tools like [Grafana](https://grafana.com/) or the Prometheus U.

# Troubleshooting

When you are working with a GKE cluster, make sure that port **8443** is opened in your firewall rules, This port is needed by the Akeyless Secret Injection mutating webhook. Update your firewall rule as follows:

1. Review the firewall rule for access:

```shell CLI
gcloud compute firewall-rules list
```

2. Replace the existing rule and allow access:

```shell CLI
gcloud compute firewall-rules update <firewall-rule-name> --allow tcp:10250,tcp:443,tcp:8443
```

# Tutorial

Check out our tutorial video on [Injecting Secrets into a Kubernetes Cluster](https://tutorials.akeyless.io/docs/injecting-secrets-into-a-kubernetes-cluster).
