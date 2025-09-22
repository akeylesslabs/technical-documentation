---
title: GKE Dynamic Secrets
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
You can create a dynamic Google Kubernetes Engine (GKE) secret to allow users receive dynamically access tokens to a GKE cluster.

# Prerequisites

* An [Akeyless Gateway](doc:api-gw).

* GKE Service Account.

To use a dynamic GKE secret, your GCP administrator needs to create a GCP IAM service account with the desired [Kubernetes Engine role](https://cloud.google.com/iam/docs/understanding-roles#kubernetes-engine-roles) that should be given to users. The service account itself will serve as the user for each individual connection, with access tokens that will last for 60 minutes.

# Create a Dynamic GKE Secret from the CLI

> 👍 Note
>
> We recommend using dynamic secrets with [Targets](doc:kubernetes-targets#gke). While it saves time for multiple secret-level configurations by not requiring you to provide an [inline connection string](https://docs.akeyless.io/docs/gke-dynamic-secret-producer#inline-connection-strings) each time, it is also important for security streamlining. Using a target allows you to rotate credentials without breaking the credential chain for the objects connected to the server used, using inline will force you to go and change the credentials in each individual item instead of just the target.

To create a dynamic GKE secret from the CLI using an existing [GKE Target](doc:kubernetes-targets#gke), run the following command: 

```shell
akeyless dynamic-secret create gke \
--name <Dynamic Secret Name> \
--target-name <Target Name> \
--gateway-url 'https://<Your-Akeyless-GW-URL:8000>'
```

 Or using an inline connection string:

```shell
akeyless dynamic-secret create akeyless dynamic-secret get-valuegke \
--name <Dynamic Secret Name> \
--gateway-url 'https://<Your-Akeyless-GW-URL:8000>' \
--gke-account-email <GKE service account email> \
--gke-account-key <GKE service account Key>
--gke-cluster-endpoint <GKE cluster endpoint URL> \
--gke-cluster-ca-cert <Base64-encoded GKE cluster CA certificate> \
--gke-cluster-name <GKE cluster name>
```

Where:

* `name`: A unique name of the dynamic secret. The name can include the path to the virtual folder where you want to create the new dynamic secret, using slash `/` separators. If the folder does not exist, it will be created together with the dynamic secret.

* `target-name`: A name of the [GKE Target](doc:kubernetes-targets#gke) that enables connection to the GKE cluster. 

* `gateway-url`: Akeyless Gateway Configuration Manager URL (port `8000`).

### Inline connection strings

If you don't have a [GKE Target](doc:kubernetes-targets#gke) yet, you can use the command with your GKE connection string:

* `gke-cluster-name`: The name of the GKE cluster you want to connect to.

* `gke-cluster-ca-cert`: Base64-encoded GKE cluster CA certificate.

* `gke-cluster-endpoint`: GKE Cluster endpoint URL.

* `gke-account-email`: GKE service account email.

* `gke-account-key`: GKE service account key.

You can find the complete list of parameters for this command in the [CLI Reference - Dynamic Secrets](https://docs.akeyless.io/docs/cli-reference-dynamic-secrets#p-stylecolorbluegkep) section.

For guidelines on how to get the GKE service account name and key, see the [API server authentication](https://cloud.google.com/kubernetes-engine/docs/how-to/api-server-authentication#environments-without-gcloud) guide. 

If you followed this guide, run:

```shell
# To get the GKE Service Account Name:
cat ~/gsa-key.json | jq -re .client_email

# To get the GKE Service Account Key:
cat ~/gsa-key.json | jq -re .private_key
```

Then copy the values to the dynamic GKE secret settings. You can find the rest of the values for dynamic GKE secret settings in your <code>kubeconfig</code> file or in the GCP console.

# Use a Dynamic GKE Secret with the Akeyless CLI running on the same host

If the Akeyless CLI is installed on the same host as the `kubectl`, you can define a `kubeconfig` file to automatically run the `get-dynamic-secret-value` command and fetch new access tokens as required. 

You need to either download the <code>kubeconfig</code> file directly from the [Akeyless Console](https://console.akeyless.io/) by selecting the **Dynamic Secret** item and copying the file from the **Dynamic Secret Description**, or generate the file manually as follows:

```yaml kubeconfig
apiVersion: v1
clusters:
- cluster:
    certificate-authority-data: <base 64 encoding of the cluster's certificate>
    server: <cluster DNS/IP address>
  name: <cluster name>
contexts:
- context:
    cluster: <cluster name>
    user: <some user name>
  name: <cluster context name>
current-context: <cluster context name>
kind: Config
preferences: {}
users:
- name: <some user name>
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

For every new GKE cluster, you must update the `kubeconfig` file accordingly.

When you run `kubectl`, the Akeyless `get-dynamic-secret-value` command will fetch a new access token for you.

For more information regarding `kubectl` and the `kubeconfig` file, see the [kubectl installation manual](https://kubernetes.io/docs/tasks/tools/install-kubectl/).

# Use a Dynamic GKE Secret with the Akeyless CLI running on a different host

If the Akeyless CLI is installed on a different host as the `kubectl`, you can get a service account token from Akeyless separately, and then manually update the `kubeconfig` file that uses the token.

First, let's generate the **kubeconfig** file manually as described above, with the following change:

```yaml kubeconfig
users:
- name: <some user name>
  user:
    token: < Dynamic Secret Value goes here >
```

To get the dynamic GKE secret value from the CLI, you should run the following command:

```shell
akeyless dynamic-secret get-value --name <Path to the dynamic secret>
```

Then you need to replace under the **kubeconfig** `< Dynamic Secret Value goes here >` with the response token exactly as you received it.

> 👍 Note
>
> To start working with dynamic secrets from the Akeyless Console, you need to configure the Gateway URL thus enabling communication between the Akeyless SaaS and the Akeyless Gateway.

> 📘 Single Kubeconfig Generation
>
> Akeyless supports generation of a single kubeconfig file. For more information see [here](https://docs.akeyless.io/docs/k8s-generic-dynamic-secrets#single-kubeconfig-generation)
