---
title: SRA Deployment
deprecated: false
hidden: true
metadata:
  robots: index
---
This guide explains how to deploy the **SRA** using the most basic configuration. SRA can be enabled either by using an existing gateway or by deploying a new one.

In this guide, we will use an existing Gateway deployed on a K8s cluster. If you don’t have one, please install a Gateway by following [this](https://docs.akeyless.io/docs/gateway-chart#/) guide.

# Prerequisites

* Helm Installed

* Kubernetes Installed

* [SSH Certificate Issuer](https://docs.akeyless.io/docs/ssh-certificates) for CLI Access.

* Minimum 1 vCPU available with 2 GB RAM per resource. This can be explicitly specified inside the chart for the Zero Trust bastion- `ztbConfig` section and the SSH bastion under `sshConfig`.

* Optional: If **Horizontal Pod Autoscaler (HPA)** usage is desired, you must set requests values.

# Additional Configuration

The settings below are optional and can be applied to further customize your deployment.

## Network

* **Ingress** - Make sure to use sticky session annotation, for example, nginx.ingress.kubernetes.io/affinity: "cookie" in **Nginx**.

* **Cloud Provider Load Balancer** - Make sure to config the Load Balancer to support sticky sessions, for example, in AWS, using ELB: [https://docs.aws.amazon.com/elasticloadbalancing/latest/classic/elb-sticky-sessions.html](https://docs.aws.amazon.com/elasticloadbalancing/latest/classic/elb-sticky-sessions.html)

When using SSH sessions behind a load balancer such as ELB, the session can be closed due to an idle connection timeout, so we recommend increasing it to a reasonably high value or even unlimited.

e.g., when running on AWS with ELB: [https://docs.aws.amazon.com/elasticloadbalancing/latest/classic/config-idle-timeout.html?icmpid=docs_elb_console](https://docs.aws.amazon.com/elasticloadbalancing/latest/classic/config-idle-timeout.html?icmpid=docs_elb_console)

## Storage

To be able to make more than 1 SSH-bastion pod work, the chart requires a persistent storage, with the `ReadWriteMany` access mode.

Since a storage class is more environment-specific, you will need to provide one before proceeding. In addition, please provide a **PersistentVolumes** with <code>persistentVolumeReclaimPolicy: retain</code> and reference those PVs in the chart `values` file

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

e.g., when running on AWS with EKS: [https://docs.aws.amazon.com/eks/latest/userguide/efs-csi.html](https://docs.aws.amazon.com/eks/latest/userguide/efs-csi.html)

## Horizontal Auto-Scaling

Horizontal auto-scaling is based on the `HorizontalPodAutoscaler` object.
For it to work correctly, the Kubernetes metrics server must be installed in the cluster - [https://github.com/kubernetes-sigs/metrics-server](https://github.com/kubernetes-sigs/metrics-server), as well as the above Storage PV must be defined for the sshConfig`Statefulset`(HPA can not support multiple pods without defining a shared persistent storage volume).

> 🚧 Warning
>
> To enable Secure Remote Access features you will have to get an access key to Akeyless private repository. Please contact your Account Manager for more details.

## Remote Access Configuration

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
