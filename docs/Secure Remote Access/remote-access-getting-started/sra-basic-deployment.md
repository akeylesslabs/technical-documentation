---
title: SRA On K8s
deprecated: false
hidden: true
metadata:
  robots: index
---
Akeyless Secure Remote Access (SRA) is the Akeyless capability that enables controlled, auditable access to private infrastructure and resources  without exposing your environments to the public internet or relying on traditional VPN jump-host models. Delivered as part of the Akeyless Gateway deployment, SRA uses the Gateway as a secure access plane inside your target networks (cloud VPC/VNet, data center, Kubernetes, etc.), so users can reach protected resources through a centrally governed policy layer.

In this guide, we will deploy SRA using the most basic configuration on a K8s cluster with an **existing Gateway**. If you do not already have a Gateway, please [deploy](https://docs.akeyless.io/docs/gateway-chart#/) one first.

## Prerequisites

* Akeyless Gateway deployed on [K8s](https://docs.akeyless.io/docs/gateway-chart#/).

* [SSH Certificate Issuer](https://docs.akeyless.io/docs/ssh-certificates) for CLI Access with `session_`  username .

* Minimum 1 vCPU available with 2 GB RAM per resource. This can be explicitly specified inside the chart for the Zero Trust bastion `ztbConfig` section and the SSH bastion under `sshConfig`.

* Network connection to [Akeyless SaaS Core Services](https://docs.akeyless.io/docs/api-gateway-network-connectivity) from your cluster.

* Network port `8000` on the cluster must be open **only for internal network access**, allowing access to the following services using the corresponding endpoints:

| Service                  | Endpoint                            |
| :----------------------- | :---------------------------------- |
| Remote Access Portal     | `<gateway-url>:8000/sra/portal`     |
| Remote Access Web Client | `<gateway-url>:8000/sra/web-client` |
| Remote Access SSH Config | `<gateway-url>:8000/sra/ssh-config` |

* Network Settings:

  Proper network configuration is required to ensure correct traffic routing and session management for SRA components. Configure networking depending on whether you use an Ingress controller or a cloud load balancer.

  * **Ingress** - When using an Ingress controller, sticky sessions are essential to maintain user connections to the same pod throughout their session. Make sure to use sticky session annotations, for example, `nginx.ingress.kubernetes.io/affinity: "cookie"`.

  * **Cloud Provider Load Balancer** - Configure your Load Balancer to support sticky sessions, for example, in AWS, using [ELB](https://docs.aws.amazon.com/elasticloadbalancing/latest/classic/elb-sticky-sessions.html).

  When using SSH sessions behind a load balancer such as ELB, the session can be closed due to an idle connection timeout, so we recommend increasing it to a reasonably high value or even unlimited, for more information, click [here](https://docs.aws.amazon.com/elasticloadbalancing/latest/classic/config-idle-timeout.html?icmpid=docs_elb_console).

* Storage Settings:

  Persistent storage with `ReadWriteMany` access mode is required when running multiple SSH-bastion pods.

  Since a storage class is more environment-specific, you will need to provide one before proceeding. In addition, please provide a **PersistentVolumes** with `persistentVolumeReclaimPolicy: retain` and reference those PVs in the chart `values.yaml` file:

```yaml
persistence: 
  volumes:
    name: share-storage
    storageClassName: "efs-sc"
    accessModes:
      - ReadWriteMany
    persistentVolumeReclaimPolicy: Retain
    annotations: {}
    mountOptions:
      - dir_mode=0650
      - file_mode=0650
    size: 2Gi
```

### Horizontal Pod Autoscaler

The **Horizontal Pod Autoscaler (HPA)** automatically adjusts the number of pods in a Kubernetes deployment based on real-time resource usage (like `CPU` or `memory`) to maintain optimal performance and efficiency.

Horizontal auto-scaling is based on the `HorizontalPodAutoscaler` object.
For it to work correctly, the K8s [metrics server](https://github.com/kubernetes-sigs/metrics-server) must be installed in the cluster, as well as the above **Storage PV** must be defined for the sshConfig`Statefulset`(HPA can not support multiple pods without defining a shared persistent storage volume).

> 🚧 Warning
>
> To enable Secure Remote Access features you will have to get an access key to Akeyless private repository. Please contact your Account Manager for more details.

## Basic Configuration

You can get the `values.yaml` file that will be used on this guide by running the following commands:

Add the following repository to the Helm repository list:

```shell
helm repo add akeyless https://akeylesslabs.github.io/helm-charts
helm repo update
```

Fetch the `values.yaml` file from the Akeyless repository:

```shell
helm show values akeyless/akeyless-gateway > values.yaml
```

In order to set your gateway with **Remote Access**, set the `sra` section to `true` and add the public key which is set on the SSH certificate Issuer as follows:

```shell
sra:
  enabled: true

sshConfig:
  CAPublicKey: <"ssh-rsa AAAAB...">
```

## Run The Deployment

To upgrade the existing gateway deployment with the SRA configuration, run the following command:

```shell
helm upgrade --install gw akeyless/akeyless-gateway -f values.yaml
```

Once upgraded, check if the pods are running:

```shell
kubectl get pods
```

In addition to the Gateway pods, two new pods for Remote Access will be created: `web` and `ssh`.

## SRA Access

In order to get the external IP address of your Gateway, run:

```shell
kubectl get svc
```

You will see the service name as `gw-akeyless-gateway`. The **External-IP** will be used to reach the Gateway from your browser.

To start working with SRA, open your browser and log in using the following URL:

* `http://<External-IP>:8000/sra/portal`

You will need to log in with [SAML](https://docs.akeyless.io/docs/saml#/), [OIDC](https://docs.akeyless.io/docs/openid#/) or a [Certificate](https://docs.akeyless.io/docs/certificate-based-authentication#/) authentication method.

Once logged in, you will see the [Dynamic Secrets](https://docs.akeyless.io/docs/how-to-create-dynamic-secret#/) with **Secure Remote Access** enabled. From there, you can securely access those resources using Just-In-Time credentials, either through the web interface or via an SSH connection.
