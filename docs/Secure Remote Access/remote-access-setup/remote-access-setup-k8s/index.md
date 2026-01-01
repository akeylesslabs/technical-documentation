---
title: Remote Access on K8s
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
Akeyless Secure Remote Access (SRA) is the Akeyless capability that enables controlled, auditable access to private infrastructure and resources without exposing your environments to the public internet or relying on traditional VPN jump-host models. Delivered as part of the Akeyless Gateway deployment, SRA uses the Gateway as a secure access plane inside your target networks (cloud VPC/VNet, data center, Kubernetes, etc.), so users can reach protected resources through a centrally governed policy layer.

In this guide, we will deploy SRA using the most basic configuration on a Kubernetes cluster with an **existing Gateway**. If you do not already have a Gateway, please [deploy](https://docs.akeyless.io/docs/gateway-chart#/) one first.

## Prerequisites

* Akeyless Gateway deployed on [Kubernetes](https://docs.akeyless.io/docs/gateway-chart#/). If deploying the Kubernetes cluster on GKE, Autopilot mode is not supported for SRA.

* [SSH Certificate Issuer](https://docs.akeyless.io/docs/ssh-certificates) for Remote CLI Access.

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

  * **Cloud Provider Load Balancer** - Configure your Load Balancer to support sticky sessions, for example, in AWS, using [ELB](https://docs.aws.amazon.com/elasticloadbalancing/latest/classic/elb-sticky-sessions.html). For **GKE** environment the default service timeout is `30s`. Increase via [BackendConfig](https://docs.cloud.google.com/kubernetes-engine/docs/how-to/ingress-configuration) or [GCPBackendPolicy](https://docs.cloud.google.com/kubernetes-engine/docs/how-to/configure-gateway-resources#configure-backend-selection) using `spec.timeoutSec`. Apply to the Service/Ingress used by SRA. [Read more about the configuration](https://docs.cloud.google.com/kubernetes-engine/docs/how-to/ingress-configuration).

  When using SSH sessions behind a load balancer such as ELB, the session can be closed due to an idle connection timeout, so we recommend increasing it to a reasonably high value or even unlimited. [Read more about configuring Amazon ELBs](https://docs.aws.amazon.com/elasticloadbalancing/latest/classic/config-idle-timeout.html?icmpid=docs_elb_console).

### Horizontal Pod Autoscaler

The **Horizontal Pod Autoscaler (HPA)** automatically adjusts the number of pods in a Kubernetes Deployment based on real-time resource usage (like `CPU` or `memory`) to maintain optimal performance and efficiency.

Horizontal auto-scaling is based on the `HorizontalPodAutoscaler` object. For it to work correctly, the Kubernetes [Metrics Server](https://github.com/kubernetes-sigs/metrics-server) must be installed in the cluster, as well as the above **Storage PV** must be defined for the sshConfig`StatefulSet`(HPA can not support multiple pods without defining a shared persistent storage volume).

> 🚧 Warning
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

2. Enable **Remote Access** on your Gateway values file, and add the public key of your SSH Cert Issuer using the `CAPublicKey` as follow:

```yaml values.yaml
sra:
  enabled: true

sshConfig:
  CAPublicKey: 
```

## Upgrade Gateway

1. To upgrade the existing gateway deployment with the SRA configuration, run the following command:

```shell
helm upgrade --install <deployment name> akeyless/akeyless-gateway -f values.yaml
```

2. Once upgraded, check if the pods are running, In addition to the Gateway pods, two new pods for Remote Access will be created: `web` and `ssh`:

```shell
kubectl get pods

NAME                                          READY   STATUS    RESTARTS   AGE
gw-akeyless-gateway-cache-69f549844-shvs7     1/1     Running   0          5s
ssh-gw-akeyless-gateway-655cd8c975-bg67s      1/1     Running   0          5s
unified-gw-akeyless-gateway-f9697f7dd-8wgc9   1/1     Running   0          5s
web-gw-akeyless-gateway-55c866c9fc-lztl7      1/1     Running   0          5s
```

3. Log in to the Gateway using your browser (`http://Your-Akeyless-Gateway-URL:8000/console`)

## SRA Portal Access

To login to the **Secure Remote Access** portal, open your browser and log in using the following URL: `http://Your-Akeyless-Gateway-URL:8000/sra/portal`, using one of the  [supported authentication methods](https://docs.akeyless.io/docs/access-resources-remotely#prerequisites).

Once logged in, you will see Secrets with **Secure Remote Access** enabled. From there, you can securely access those resources using Just-In-Time credentials, either through the web interface or via CLI.

<br />
