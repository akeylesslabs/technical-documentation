---
title: SRA Basic Deployment
deprecated: false
hidden: true
metadata:
  robots: index
---
This guide explains how to deploy the SRA using the most basic configuration. SRA can be deployed either by using an existing gateway or during the deployment of a new one.

In this guide, we will use an existing Gateway deployed on a K8s cluster, note that the SRA utility can also be deployed on Docker using [docker compose](https://docs.akeyless.io/update/docs/remote-access-docker#/).

If you do not have a Gateway, please install one by following [this](https://docs.akeyless.io/update/docs/gateway-chart#/) guide.

# Prerequisites

* Akeyless Gateway deployed on [K8s](https://docs.akeyless.io/docs/gateway-chart#/).

* [SSH Certificate Issuer](https://docs.akeyless.io/docs/ssh-certificates) for CLI Access, with `session_` allowed username.

* Minimum 1 vCPU available with 2 GB RAM per resource. This can be explicitly specified inside the chart for the Zero Trust bastion- `ztbConfig` section and the SSH bastion under `sshConfig`.

* Optional: If **Horizontal Pod Autoscaler (HPA)** usage is desired, you must set requests values.

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

## Horizontal Pod Autoscaler

The **Horizontal Pod Autoscaler (HPA)** automatically adjusts the number of pods in a Kubernetes deployment based on real-time resource usage (like `CPU` or `memory`) to maintain optimal performance and efficiency.

Horizontal auto-scaling is based on the `HorizontalPodAutoscaler` object.
For it to work correctly, the K8s [metrics server](https://github.com/kubernetes-sigs/metrics-server) must be installed in the cluster, as well as the above **Storage PV** must be defined for the sshConfig`Statefulset`(HPA can not support multiple pods without defining a shared persistent storage volume).

> 🚧 Warning
>
> To enable Secure Remote Access features you will have to get an access key to Akeyless private repository. Please contact your Account Manager for more details.

# Basic Configuration

In order to set your gateway with **Remote Access**, add the following to your deployment by editing the `values.yaml` file:

```shell
sra:
  enabled: true

sshConfig:
  CAPublicKey: <"ssh-rsa AAAAB...">
```

Where:

* `sra`: set to `enable` in order to deploy the remote access functionality.

* `CAPublicKey`: The public key set on the [SSH Certificate Issuer](https://docs.akeyless.io/docs/ssh-certificates#/configuration).

# Deployment Update

To update the existing gateway deployment with the SRA configuration, run the following command:

```shell
helm upgrade --install gw akeyless/akeyless-gateway -f values.yaml
```

Once updated, check if the pods are running:

```shell
kubectl get pods
```

In addition to the Gateway pods, two new pods for Remote Access will be created: `web` and `ssh`.

# SRA Access

In order to get the external IP address of your Gateway, run:

```shell
kubectl get svc
```

You will see the service name as `gw-akeyless-gateway`. The **External-IP** will be used to reach the Gateway from your browser.

To start working with SRA, open your browser and log in using the following URL:

* `http://External-IP:8000/sra/portal`

You will need to log in with [SAML](https://docs.akeyless.io/docs/saml#/), [OIDC](https://docs.akeyless.io/docs/openid#/) or a [Certificate](https://docs.akeyless.io/docs/certificate-based-authentication#/) authentication method.

Once logged in, you will see the [Dynamic Secrets](https://docs.akeyless.io/docs/how-to-create-dynamic-secret#/) with **Secure Remote Access** enabled. From there, you can securely access those resources using Just-In-Time credentials, either through the web interface or via an SSH connection.

<br />
