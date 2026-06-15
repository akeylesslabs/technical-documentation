---
title: Kubernetes Cluster Access
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
You can enable Secure Remote Access to a Kubernetes cluster based on the dynamic secret that generates temporary credentials for Kubernetes cluster. Users can then access Kubernetes cluster from the Secure Remote Access Portal, either over the web or using Kubernetes native CLI.

## Prerequisites

* The [Secure Remote Access](https://docs.akeyless.io/docs/sra-setup-overview) deployed.

* A running Kubernetes dynamic Secret [EKS](https://docs.akeyless.io/docs/eks-dynamic-secret-producer), [GKE](https://docs.akeyless.io/docs/gke-dynamic-secret-producer) or [Kubernetes Generic](https://docs.akeyless.io/docs/k8s-generic-dynamic-secrets) .

* [Akeyless Connect](https://docs.akeyless.io/docs/sra-akeyless-connect)

* An [SSH Certificate Issuer](https://docs.akeyless.io/docs/sra-ssh-certificates).

## Set Up Remote Access to a Kubernetes Cluster from the Akeyless CLI

Let's set up remote access to a Kubernetes cluster using the Akeyless CLI. If you’d prefer, see how to do this from the [Akeyless Console](https://docs.akeyless.io/docs/sra-k8s-cluster#set-up-remote-access-to-a-k8s-cluster-from-the-akeyless-console) instead.

Run the relevant command to define the following fields to the secret that specifies the Kubernetes cluster details and access credentials:

```shell
akeyless dynamic-secret update k8s \
--name <Kubernetes dynamic secret name> \
--secure-access-enable true \
--secure-access-certificate-issuer </Path/to/SSH/Cert/Issuer> \
--secure-access-cluster-endpoint <Kubernetes cluster endpoint URL> \
--secure-access-allow-port-forwarding <true/false>
```

Where:

* `secure-access-certificate-issuer`: Required to enable CLI access. The path to the SSH certificate issuer that should be used for certificate authentication..
* `secure-access-cluster-endpoint`: The Kubernetes cluster endpoint URL.
* `secure-access-allow-port-forwarding`: Optional, allows running non-interactive `kubectl` commands, such as `exec` and `port-forward`. It also allows using the `--watch` flag (`-w`).

For [Kubernetes Generic Dynamic Secrets](https://docs.akeyless.io/docs/k8s-generic-dynamic-secrets) you can have Secure Remote Access for your Kubernetes Dashboard URL:

* `secure-access-dashboard-url`: The Kubernetes Dashboard URL available only for Generic Kubernetes.
* `secure-access-web-browsing`: Optional, secure web browsing over isolated web browser **available only for clients with** [Web Access Bastion](https://docs.akeyless.io/docs/sra-web-access-on-k8s).

## Set Up Remote Access to a Kubernetes Cluster from the Akeyless Console

Let's set up remote access to a Kubernetes cluster from the Akeyless Console. If you'd prefer, see how to do this from the [Akeyless CLI](https://docs.akeyless.io/docs/sra-k8s-cluster#set-up-remote-access-to-a-k8s-cluster-from-the-akeyless-cli) instead.

1. Log in to the Akeyless Console and go to **Items**.

2. Select the dynamic secret that specifies the Kubernetes cluster details and access credentials.

3. Click on the **Secure Remote Access** tab, select the pencil icon, and enable **Secure Remote Access**, then fill in the following fields:

For [GKE Dynamic Secrets](https://docs.akeyless.io/docs/gke-dynamic-secret-producer) or [EKS Dynamic Secrets](https://docs.akeyless.io/docs/eks-dynamic-secret-producer):

* `Cluster Endpoint URL`: Required, your Kubernetes cluster URL.
* `certificate-issuer`: Required to enable CLI access. The path to the SSH certificate issuer that should be used for certificate authentication.
* `Allow Port Forwarding`: Optional, allows running non-interactive `kubectl` commands, such as: `exec` / `port-forward` / and so on. Also allows using the `--watch` flag (`-w`), for example.

For [Kubernetes Generic Dynamic Secrets](https://docs.akeyless.io/docs/k8s-generic-dynamic-secrets):

* `Cluster Endpoint URL`: Required, your Kubernetes cluster URL.

For **Web Access**:

* `Dashboard URL`: Required to enable Secure Remote Access to your Kubernetes Dashboard.

* `Secure Web Browsing`: Optional, secure web browsing over isolated web browser **available only for clients with** [Web Access Bastion](https://docs.akeyless.io/docs/sra-web-access-on-k8s).

For **CLI Access**:

* `certificate-issuer`: Required to enable CLI access. The path to the SSH certificate issuer that should be used for certificate authentication.

* `Allow Port Forwarding`: Optional, allows running non-interactive `kubectl` commands, such as: `exec` / `port-forward` / and so on. Also allows using the `--watch` flag (`-w`), for example.

From any terminal which has [Akeyless Connect](https://docs.akeyless.io/docs/sra-akeyless-connect) configured, you can run the following command:

```shell
akeyless connect -t <namespace>@<cluster endpoint without https:// > -n <dynamic-secret-name> -v <sra-bastion-ssh-service-address:port>
```
