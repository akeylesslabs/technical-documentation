---
title: SRA Deployment
deprecated: false
hidden: true
metadata:
  robots: index
---
This guide explains how to deploy the **SRA** using the most basic configuration. SRA can be enabled either by using an existing gateway or during the deployment of a new one.

In this guide, we will use an existing Gateway deployed on a K8s cluster. If you don’t have one, please install a Gateway by following [this](https://docs.akeyless.io/docs/gateway-chart#/) guide.

# Prerequisites

* Akeyless Gateway deployed on either [Docker Compose](https://docs.akeyless.io/docs/gateway-compose#/)  or [K8s](https://docs.akeyless.io/docs/gateway-chart#/) .
* Helm Installed.
* Kubernetes Installed.
* [SSH Certificate Issuer](https://docs.akeyless.io/docs/ssh-certificates) for CLI Access.
* Minimum 1 vCPU available with 2 GB RAM per resource. This can be explicitly specified inside the chart for the Zero Trust bastion- `ztbConfig` section and the SSH bastion under `sshConfig`.
* Optional: If **Horizontal Pod Autoscaler (HPA)** usage is desired, you must set requests values.

# Optional Deployment Settings

The settings below are optional and can be applied to further customize your deployment.

## Network

Network configuration ensures proper traffic routing and session management for SRA components. Choose between Ingress controllers or cloud provider load balancers based on your k8s setup.

* **Ingress** - When using an Ingress controller, sticky sessions are essential to maintain user connections to the same pod throughout their session. Make sure to use sticky session annotations, for example, `nginx.ingress.kubernetes.io/affinity: "cookie"`.

* **Cloud Provider Load Balancer** - Configure your Load Balancer to support sticky sessions, for example, in AWS, using [ELB](https://docs.aws.amazon.com/elasticloadbalancing/latest/classic/elb-sticky-sessions.html).

When using SSH sessions behind a load balancer such as ELB, the session can be closed due to an idle connection timeout, so we recommend increasing it to a reasonably high value or even unlimited, for more information, click [here](https://docs.aws.amazon.com/elasticloadbalancing/latest/classic/config-idle-timeout.html?icmpid=docs_elb_console).

## Storage

Persistent storage with `ReadWriteMany` access mode is required when running multiple SSH-bastion pods.

Since a storage class is more environment-specific, you will need to provide one before proceeding. In addition, please provide a **PersistentVolumes** with <code>persistentVolumeReclaimPolicy: retain</code> and reference those PVs in the chart `values.yaml` file:

```yaml
persistence: 
  shareStorageVolume:
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

# Remote Access Configuration

In order to set your gateway with **Remote Access**, add the following to your deployment by editing the `values.yaml` file:

```shell
sra:
  enabled: true

    config:
      CAPublicKey: "<PublicKey>"
```

Where:

* `sra`: set to `enable` in order to deploy the remote access functionality.

* `CAPublicKey`: The public key set on the [SSH Certificate Issuer](https://docs.akeyless.io/docs/ssh-certificates#/configuration).

# Updating the deployment

To update the existing gateway deployment with the SRA configuration, run the following command:

```shell
helm upgrade --install gw akeyless/akeyless-gateway -f values.yaml
```

Once installed, check if the pods are running:

```shell
kubectl get pods
```

In addition to the Gateway pods, two new pods for Remote Access will be created: `web` and `ssh`.

# Working With SRA

In order to get the external IP address of your Gateway, run:

```shell
kubectl get svc
```

You will see the service name as `<release-name>-akeyless-gateway`. The **External-IP** will be used to reach the Gateway from your browser.

To start working with SRA, open your browser and log in using the following URL:

* `https://External-IP:8000/sra/portal`

You will need to log in with [SAML](https://docs.akeyless.io/docs/saml#/), [OIDC](https://docs.akeyless.io/docs/openid#/) or a [Certificate](https://docs.akeyless.io/docs/certificate-based-authentication#/) authentication method.

Once logged in, you will see the [Dynamic Secrets](https://docs.akeyless.io/docs/how-to-create-dynamic-secret#/) with **Secure Remote Access** enabled. From there, you can securely access those resources using Just-In-Time credentials, either through the web interface or via an SSH connection.

<br />
