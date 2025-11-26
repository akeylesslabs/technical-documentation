---
title: SRA Deployment
deprecated: false
hidden: true
metadata:
  robots: index
---
This guide explains how to deploy the **SRA** using the most basic configuration. SRA can be enabled either by using an existing gateway or by deploying a new one.

In this guide, we will deploy the gateway using a K8s cluster.

# Prerequisites

* Helm Installed

* Kubernetes Installed

* [SSH Certificate Issuer](https://docs.akeyless.io/docs/ssh-certificates) for CLI Access.

* Minimum 1 vCPU available with 2 GB RAM per resource. This can be explicitly specified inside the chart for the Zero Trust bastion- `ztbConfig` section and the SSH bastion under `sshConfig`.

* Optional: If Horizontal Pod Autoscaler (HPA) usage is desired, you must set requests values.

## Network

* **Ingress** - Make sure to use sticky session annotation, for example, nginx.ingress.kubernetes.io/affinity: "cookie" in Nginx

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

_**Horizontal Auto-Scaling**_

Horizontal auto-scaling is based on the HorizontalPodAutoscaler object.
For it to work correctly, the Kubernetes metrics server must be installed in the cluster - [https://github.com/kubernetes-sigs/metrics-server](https://github.com/kubernetes-sigs/metrics-server), as well as the above Storage PV must be defined for the `sshConfig` Statefulset (HPA can not support multiple pods without defining a shared persistent storage volume).

> 🚧 Warning
>
> To enable Secure Remote Access features you will have to get an access key to Akeyless private repository. Please contact your Account Manager for more details.

# Deployment

The following steps include the Gateway deployment. If you already have a running gateway, you can proceed to the [Remote Access](https://docs.akeyless.io/docs/copy-of-quick-start#/remote-access-configuration) section.

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

## Gateway Configuration

Set the Authentication Method (in this example, we will use an [API Key](https://docs.akeyless.io/docs/api-key#/)):

```shell
akeylessGatewayAuth:
  gatewayAccessId: <AccessID>
  gatewayAccessType: access_key
  gatewayCredentialsExistingSecret: access-key
```

Where

* `gatewayAccessId`: The `AccessID` of the API Key.

* `gatewayAccessType`: The `AccessType` of the API Key.

* `gatewayCredentialsExistingSecret`: [K8s secret](https://kubernetes.io/docs/concepts/configuration/secret/) that stores sensitive information (in our case, the `AccessKey`).

```shell
kubectl create secret generic access-key \
  --from-literal=gateway-access-key=<plaintext-Access-Key>
```

## Remote Access Configuration

In order to set your gateway with **Remote Access**, add the following to your deployment:

```shell
sra:
  enabled: true

    config:
      CAPublicKey: "<PublicKey>"
```

Where:

* `sra`: set to `enable` in order to deploy the remote access functionality.

* `CAPublicKey`: The public key set on the [SSH Certificate Issuer](https://docs.akeyless.io/docs/ssh-certificates#/configuration).

# Installation

To install the Gateway, run the following command:

```shell
helm install gw akeyless/akeyless-gateway -f values.yaml
```

Once installed, check if the pods are running:

```shell
kubectl get pods
```

Upon successful installation, you will see the Gateway pods as well as the Remote Access pods, which include the `web` and `ssh` components.

In order to get the external IP address of your Gateway, run:

```shell
kubectl get svc
```

You will see the service name as `gw-akeyless-gateway`. The **External-IP** will be used to reach the Gateway from your browser.

Log in to the Gateway using your browser at `https://<External-IP>:8000` with your Gateway admin credentials.

If you see the login page, you have successfully deployed the Gateway.

# Working With SRA

To start working with SRA, open your browser and log in using the following URL:

* `https://External-IP:8000/sra/portal`

You will need to log in with [SAML](https://docs.akeyless.io/docs/saml#/), [OIDC](https://docs.akeyless.io/docs/openid#/) or a [Certificate](https://docs.akeyless.io/docs/certificate-based-authentication#/) authentication method.

Once logged in, you will see the [Dynamic Secrets](https://docs.akeyless.io/docs/how-to-create-dynamic-secret#/) with **Secure Remote Access** enabled. From there, you can securely access those resources using Just-In-Time credentials, either through the web interface or via an SSH connection.

<br />
