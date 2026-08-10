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

## Prerequisites

- An [Akeyless Gateway](https://docs.akeyless.io/docs/gateway-overview)

- A [GKE Target](https://docs.akeyless.io/docs/kubernetes-targets#gke)

- GKE Service Account

To use a dynamic GKE secret, your GCP administrator needs to create a GCP IAM service account with the desired [Kubernetes Engine role](https://cloud.google.com/iam/docs/understanding-roles#kubernetes-engine-roles) that should be given to users. The service account itself will serve as the user for each individual connection, with access tokens that will last for 60 minutes.

## Create a Dynamic GKE Secret with the CLI

To create a dynamic GKE secret with the CLI using an existing [GKE Target](https://docs.akeyless.io/docs/kubernetes-targets#gke), run the following command:

```shell
akeyless dynamic-secret create gke \
--name <Dynamic Secret Name> \
--target-name <Target Name> \
--gateway-url 'https://<Your-Akeyless-GW-URL>:8000'
```

Where:

- `name`: A unique name of the dynamic secret. The name can include the path to the virtual folder where you want to create the new dynamic secret, using slash `/` separators. If the folder does not exist, it will be created together with the dynamic secret.

- `target-name`: A name of the [GKE Target](https://docs.akeyless.io/docs/kubernetes-targets#gke) that enables connection to the GKE cluster.

- `gateway-url`: Akeyless Gateway URL (port `8000`).

You can find the complete list of parameters for this command in the [CLI Reference - Dynamic Secrets](https://docs.akeyless.io/docs/cli-reference-dynamic-secrets#gke) section.

For guidelines on how to get the GKE service account name and key, see the [API server authentication](https://cloud.google.com/kubernetes-engine/docs/how-to/api-server-authentication#environments-without-gcloud) guide.

If you followed this guide, run:

```shell
# To get the GKE Service Account Name:
cat ~/gsa-key.json | jq -re .client_email

# To get the GKE Service Account Key:
cat ~/gsa-key.json | jq -re .private_key
```

Then copy the values to the dynamic GKE secret settings. You can find the rest of the values for dynamic GKE secret settings in your `kubeconfig` file or in the GCP console.

## Use a Dynamic GKE Secret With the Akeyless CLI Running on the Same Host

If the Akeyless CLI is installed on the same host as the `kubectl`, you can define a `kubeconfig` file to automatically run the `get-dynamic-secret-value` command and fetch new access tokens as required.

You need to either download the `kubeconfig` file directly from the [Akeyless Console](https://console.akeyless.io/) by selecting the **Dynamic Secret** item and copying the file from the **Dynamic Secret Description**, or generate the file manually as follows:

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

## Use a Dynamic GKE Secret With the Akeyless CLI Running on a Different Host

If the Akeyless CLI is installed on a different host as the `kubectl`, you can get a service account token from Akeyless separately, and then manually update the `kubeconfig` file that uses the token.

First, let's generate the **kubeconfig** file manually as described above, with the following change:

```yaml kubeconfig
users:
- name: <some user name>
  user:
    token: < Dynamic Secret Value goes here >
```

To get the dynamic GKE secret value with the CLI, you should run the following command:

```shell
akeyless dynamic-secret get-value --name <Path to the dynamic secret>
```

Then you need to replace under the **kubeconfig** `< Dynamic Secret Value goes here >` with the response token exactly as you received it.

<Callout icon="ℹ️" theme="info">
  ### **Note:**

  To start working with Dynamic Secrets from the Akeyless Console, you need to configure the Gateway URL thus enabling communication between the Akeyless SaaS and the Akeyless Gateway.

  Akeyless supports generation of a single kubeconfig file. For more information see [here](https://docs.akeyless.io/docs/k8s-generic-dynamic-secrets#single-kubeconfig-generation)
</Callout>

<br />
