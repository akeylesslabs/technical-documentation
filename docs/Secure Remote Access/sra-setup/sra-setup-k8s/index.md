---
title: SRA on Kubernetes
excerpt: ''
deprecated: false
hidden: false
metadata:
  title: ''
  description: ''
  robots: index
next:
  description: ''
slug: sra-setup-k8s
---
Use this page to deploy Akeyless Gateway with Secure Remote Access (SRA) components on Kubernetes by using Helm.

If you do not already have a Gateway deployment, start with [Deploying Gateway on Kubernetes](https://docs.akeyless.io/docs/gateway-deploy-kubernetes-helm).

## Prerequisites

* Akeyless Gateway deployed on [Kubernetes](https://docs.akeyless.io/docs/gateway-deploy-kubernetes-helm#/). If deploying the Kubernetes cluster on GKE, Autopilot mode is not supported for SRA.

* [SSH Certificate Issuer](https://docs.akeyless.io/docs/sra-ssh-certificates) for remote CLI access.

* Minimum 1 vCPU and 2 GiB memory per SRA component.

* SSH bastion service must be exposed with `type: LoadBalancer`.

* SSH bastion container must run as privileged.

* Network connection to [Akeyless SaaS Core Services](https://docs.akeyless.io/docs/gateway-network-connectivity) from your cluster.

* Network port `8000` on the cluster must be open **only for internal network access**, allowing access to the following services:

| Service | Endpoint |
| --- | --- |
| Remote Access Portal | `<gateway-url>:8000/sra/portal` |
| Remote Access Web Client | `<gateway-url>:8000/sra/web-client` |
| Remote Access SSH Config | `<gateway-url>:8000/sra/ssh-config` |

For a full list of ports and outbound dependencies, see [Requirements](https://docs.akeyless.io/docs/sra-requirements).

### Network Settings

Configure sticky sessions and timeout settings based on your ingress or load balancer implementation.

* **Ingress**: Keep a session pinned to a backend pod. For NGINX ingress, for example, set `nginx.ingress.kubernetes.io/affinity: "cookie"`.

* **Cloud load balancer**: Ensure idle/response timeout values align with your expected SRA session duration.

### Horizontal Pod Autoscaler

The **Horizontal Pod Autoscaler (HPA)** automatically adjusts the number of pods in a Kubernetes Deployment based on real-time resource usage (like `CPU` or `memory`) to maintain optimal performance and efficiency.

Horizontal auto-scaling is based on the `HorizontalPodAutoscaler` object. For it to work correctly, install the Kubernetes [Metrics Server](https://github.com/kubernetes-sigs/metrics-server).

> ⚠️ **Warning:**
>
> To enable Secure Remote Access features you will have to get an access key to Akeyless private repository. Please contact your Account Manager for more details.

## Helm Chart Configuration

1. Add the following repository to the Helm repository list:

    ```shell
    helm repo add akeyless https://akeylesslabs.github.io/helm-charts
    helm repo update
    ```

2. Fetch the `values.yaml` file from the Akeyless repository:

    ```shell
    helm show values akeyless/akeyless-gateway > values.yaml
    ```

3. Set the relevant parameters in the `values.yaml` file with a text editor or IDE.

### SRA Configuration

1. Get your SSH Cert Issuer Signer public key using the **CLI** command:

    ```shell SSH CA Public Key
    akeyless get-rsa-public --name /path/to/SSHSignerKey --json --jq-expression='.ssh' 
    ```

2. Enable **Remote Access** on your Gateway values file, and add the public key of your SSH Cert Issuer using `CAPublicKey` as follows. You can provide one or more CA public keys:

    ```yaml values.yaml
        sra:
            enabled: true
            sshConfig:
                CAPublicKey: |
                    ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDAPzDVmeABzsGd0lEl9m2fdgmCzOLVmEGcLxNkn...
                    ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDz0v4zyj4d1m7K9w7j2qQ5B1v8bH0ArK...
    ```

## Upgrade Gateway

1. To upgrade the existing gateway deployment with the SRA configuration, run the following command:

    ```shell
    helm upgrade --install <deployment name> akeyless/akeyless-gateway -f values.yaml
    ```

2. Once upgraded, check if the pods are running. In addition to the Gateway pods, two new pods for Remote Access are created: `web` and `ssh`.

    ```shell
    kubectl get pods

    NAME                                          READY   STATUS    RESTARTS   AGE
    gw-akeyless-gateway-cache-69f549844-shvs7     1/1     Running   0          5s
    ssh-gw-akeyless-gateway-655cd8c975-bg67s      1/1     Running   0          5s
    unified-gw-akeyless-gateway-f9697f7dd-8wgc9   1/1     Running   0          5s
    web-gw-akeyless-gateway-55c866c9fc-lztl7      1/1     Running   0          5s
    ```

3. Log in to the Gateway using your browser (`http://Your-Akeyless-Gateway-URL:8000/console`).

## SRA Portal Access

To log in to the **Secure Remote Access** portal, open your browser and use the following URL: `http://Your-Akeyless-Gateway-URL:8000/sra/portal`, with one of the [supported authentication methods](https://docs.akeyless.io/docs/sra-portal).

Once logged in, you will see Secrets with **Secure Remote Access** enabled.

## Advanced Configuration

For keyboard layouts, session log forwarding, RDP recording configuration, SSH fingerprint behavior, and `CONFIG_MAX_STARTUPS`, see [Advanced Configuration on Kubernetes](https://docs.akeyless.io/docs/sra-advanced-configuration-k8s).

If web application isolation is required, continue with [Zero Trust Web Access Topology](https://docs.akeyless.io/docs/sra-web-access-topology).