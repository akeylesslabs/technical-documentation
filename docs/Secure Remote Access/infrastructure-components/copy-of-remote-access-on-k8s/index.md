---
title: Copy of Remote Access on K8s
deprecated: false
hidden: true
metadata:
  robots: index
---
Akeyless Secure Remote Access offers robust security for accessing your resources by leveraging a range of just-in-time credentials, including Dynamic Secrets, Rotated Secrets, and SSH certificates.

> 📘 New Chart
>
> This guide describe the flow using the **latest** chart of the Akeyless Secure Remote Access.
>
> [Review the documentation for the legacy chart](https://docs.akeyless.io/docs/secure-remote-access-bastion).

Remote Access is enabled through the [Akeyless Gateway](https://docs.akeyless.io/docs/gateway-chart) Helm chart deployment. Usually this is added after the Gateway is deployed, but it can be deployed as part of the Gateway deployment. This document will show how to upgrade your deployment to add Remote Access capabilities.

The Remote Access deployment spins up two pods in your cluster: `ssh-sra` and `web-sra`.

## Prerequisites

* An [Akeyless Gateway](https://docs.akeyless.io/docs/gateway-chart)

* Helm Installed

* A Kubernetes Cluster

* [SSH Certificate Issuer](https://docs.akeyless.io/docs/ssh-certificates) for CLI access

* Minimum 1 vCPU available with 2 GB RAM per resource. This can be explicitly specified inside the chart. It can be found under `sraConfig` for the Web service and `sshConfig` for the SSH service.

* Optional: If Horizontal Pod Autoscaler (HPA) usage is desired, you must set `requests` values in the `resources` section. For the HPA to function correctly, the Kubernetes Metrics Server must be installed in your cluster. [Review the Metrics Server setup guide](https://github.com/kubernetes-sigs/metrics-server).

### Network Configuration

<Callout icon="🌐" theme="default">
  #### Network Configuration

* When using **Ingress**, ensure _sticky sessions_ are enabled by using the appropriate annotation. For example, in NGINX, you can use: `nginx.ingress.kubernetes.io/affinity: "cookie"`.
* Configure your load balancer to support sticky sessions. For example, in AWS with Elastic Load Balancer (ELB), refer to AWS ELB Sticky Sessions documentation for more details.
</Callout>

* When using SSH sessions behind a load balancer, such as ELB, sessions may be closed due to idle connection timeouts. We recommend increasing the idle timeout to a higher value or setting it to unlimited.
* For AWS ELB, adjust the idle timeout settings as per AWS ELB Idle Timeout documentation.

## Deploying Remote Access

The `values.yaml` file used to deploy the [Gateway](https://docs.akeyless.io/docs/gateway-chart) holds the Remote Access default values.

## Configuration

Remote Access can only be used with the following Authentication Methods:

[SAML](https://docs.akeyless.io/docs/auth-with-saml)

[OIDC](https://docs.akeyless.io/docs/auth-with-oidc)

[Certificates](https://docs.akeyless.io/docs/auth-with-certificate)

[LDAP](https://docs.akeyless.io/docs/auth-with-ldap)

To enable only specific users to use Remote Access, make sure to add the relevant `authorizedAccessIDs` in the `Global` section. A comma-separated list can be used for multiple IDs. While this is not mandatory, it is a good security practice to limit user access. If not configured, a Warning message will appear.

```yaml
############
## Global ##
############

authorizedAccessIDs: <AccessID>
```

Remote Access uses the same Authentication as the Gateway which is found in the `akeylessGatewayAuth` section of the chart. To start configuring Remote Access, find the `sra` section and set it to `enabled: true`.

```yaml
######################################################
## Default values for akeyless-secure-remote-access ##
######################################################
sra:
  # Enable secure-remote-access. Valid values: true/false.
  enabled: true
```

### Web Config

This section describes the web deployment. You can add `annotations` and `labels` as well as the number of replicas for the service.

```yaml
  webConfig:
    deployment:
      annotations: {}
      labels: {}
    replicaCount: 1
```

_**Storage**_

**NOTE**: Persistence is only relevant for the SRA-Web pod.

The purpose of the `PersistentVolume` is to ensure that data can be shared and accessed by all pods in the cluster. When RDP is configured to [save recordings locally](https://docs.akeyless.io/docs/remote-access-rdp-recordings#local), the PersistentVolume is used to store these recordings. The Helm chart defines a persistent storage configuration using the `ReadWriteMany` access mode, which enables all pods to read from, and write to, the same storage volume. This is necessary to ensure that any changes or updates made by one pod are available to all other pods, maintaining consistency across the services.

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

Here’s how it works:

**Persistent Storage**: A storage resource is allocated that can be accessed by multiple pods.

**ReadWriteMany** Access Mode: This allows multiple pods to both read from and write to the same storage volume at the same time, ensuring that data remains consistent across the cluster.

**Environment-Specific StorageClass**: The [StorageClass, like Amazon EFS](https://docs.aws.amazon.com/eks/latest/userguide/efs-csi.html) (`efs-sc`), defines the backend storage type. You will need to choose or create a StorageClass suited to your cloud provider or infrastructure.

**Persistent Volume Reclaim Policy**: Setting this policy to `Retain` ensures that the data in the `PersistentVolume` remains intact even if the pods using it are deleted. This can be important for recovery or deployment updates.

### SSH Config

To provide just-in-time native CLI access for your users using [SSH Certificates](https://docs.akeyless.io/docs/ssh-certificates), set the `CAPublicKey` field with the matching public key of the key you used to create the [SSH Certificate Issuer](https://docs.akeyless.io/docs/ssh-certificates).

```yaml
sshConfig:
    replicaCount: 1

    config:
      CAPublicKey: "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDAP.."
      # CAPublicKey: |
```

> 📘 Info
>
> If you don't have an SSH certificate yet, please follow this guide on creating an SSH Cert issuer with Akeyless and set your `CAPublicKey` in the `values` file.
>
> You will also need to enable Secure Remote Access on the SSH Cert Issuer either in the UI or by adding the `--secure-access-enable true` flag to your CLI command.

## Install

```shell
helm install <RELEASE NAME> akeyless/akeyless-gateway -f values.yaml
```

Verify that both `ssh-` and `web-` pods are up and running.

## Upgrade Remote Access

To upgrade Remote Access to the latest version, run the following:

```shell
helm repo update  
helm upgrade <RELEASE NAME> akeyless/akeyless-gateway -f values.yaml
```

Check that the new pods are starting.

## Recommended Security Configuration Options

### Allowed Redirect URL(s)

The Allowed Redirect URL(s) option ensures that only specific redirects (usually Remote Access are accepted. This configuration, allows administrators to define a list of authorized URLs that will be considered valid for redirection from the Web Portal back to the remote access server. This setup enhances security by ensuring that users are only redirected to trusted URLs.

Run the following command from the Terminal:

```shell
akeyless gateway update remote-access --allowed-urls <redirect-urls>
```

This can also be done by way of the console by going to **Gateways** -> **Your-Gateway** -> **Manage Gateway** -> **Remote Access**.
