---
title: Web Access on K8s
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
Akeyless Web Access Bastion provides Secure Remote Access to any web application with session recording, including proxy service acting as an entry point to your internal web applications, where only after successful authentication users will get access, either via an isolated remote browser or directly to your target server based on your secret configuration. 

Working with isolated browsers provides a complete zero-knowledge where users do not have any knowledge about the access credentials.  

This chart bootstraps the Akeyless-Web-Access-Bastion deployment on a Kubernetes cluster using the Helm package manager. 

# Prerequisites

* Helm Installed

* K8s Installed

* Minimum 1 vCPU available with 2GB RAM for the `WebWorker` and  1 vCPU available with 1GB RAM for the `WebDispatcher` This can be explicitly specified inside the chart for the `webWorker` and for the `dispatcher` services.

\***\*Network\*\***

When using an Embedded browser session behind a load balancer such as ELB, the session can be closed due to an idle connection timeout, it's advised to increase it to a reasonably high value or even unlimited.

e.g, when running on AWS with ELB: [https://docs.aws.amazon.com/elasticloadbalancing/latest/classic/config-idle-timeout.html?icmpid=docs\_elb\_console](https://docs.aws.amazon.com/elasticloadbalancing/latest/classic/config-idle-timeout.html?icmpid=docs_elb_console)

\***\*Storage\*\***

To be able to download files to your local machine, the chart requires a storage class with `ReadWriteMany` access mode.

Since a storage class is more environment specific, you will need to provide one before proceeding. In addition, please provide a `PersistentVolumes` with reference under the `persistence` section in the `values.yaml` file.

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

e.g, when running on AWS with EKS: [https://docs.aws.amazon.com/eks/latest/userguide/efs-csi.html](https://docs.aws.amazon.com/eks/latest/userguide/efs-csi.html)

For security reasons, please limit the PersistentVolumes`mount permissions to`0650\`.

\***\*Horizontal Auto-Scaling\*\***

Horizontal auto-scaling is based on the HorizontalPodAutoscaler object.\
For it to work correctly, the Kubernetes metrics server must be installed in the cluster - [https://github.com/kubernetes-sigs/metrics-server](https://github.com/kubernetes-sigs/metrics-server).

> 🚧 Warning
>
> To enable Secure Remote Access features you will have to get an access-key to Akeyless private repository. Please contact your Account Manager for more details.

# Installing the Chart

Add Akeyless helm charts repository to your Helm repository list:

```shell
helm repo add akeyless https://akeylesslabs.github.io/helm-charts
helm repo update
```

The values.yaml file holds default values. Copy the file from: 

[https://github.com/akeylesslabs/helm-charts/tree/main/charts/akeyless-zero-trust-web-access](https://github.com/akeylesslabs/helm-charts/tree/main/charts/akeyless-zero-trust-web-access)

Or run the following helm command to generate the values file locally:

```shell
helm show values akeyless/akeyless-zero-trust-web-access > values.yaml
```

# Configuration

To connect to Akeyless private repository, set the `dockerRepositoryCreds` field to access the Akeyless internal image and the relevant `apiGatewayURL` to point your Gateway REST API port `8080`

```yaml
dockerRepositoryCreds:
apiGatewayURL: https://rest.akeyless.io

# Optional, to Work with a specifc enviorement set the relevant URL.
  env:
     - name: AKEYLESS_URL
       value: "https://vault.akeyless.io"
```

To enable **HTTP Proxy** mode for remote access, add the following environment variable to the `env` section under the dispatcher configuration:

```yaml
env:
    - name: WEB_PROXY_TYPE
      value: http
```

> 🚧 Warning
>
> The HTTP-type proxy will only work with Chrome browsers currently. For Firefox, you can skip this environment variable configuration so the default `socks-proxy` protocol will be used for example: `socks://proxy.example.com`

The Web Access Bastion should be set with a **privileged** `AccessID` with **Read** and **list** permissions. To fetch the relevant secret on behalf of your users, set the `privilegedAccess` field with the relevant `AccessID` as described in the Authentication section of this page. 

Users then can have only `list` permissions on their secrets. Upon successful authentication against your IDP, the bastion will fetch the requested secret from Akeyless and will inject them directly for your users transparently. 

To control who will be the relevant users that will be allowed to request access from the Akeyless Bastion, set the `allowedAccessIDs` field with a list of `AccessIDs` that will be authorized to request access. 

```yaml
privilegedAccess:
  accessID: ""
  allowedAccessIDs: []
```

## Authentication

The following [Authentication Methods](https://docs.akeyless.io/docs/access-and-authentication-methods) are supported: 

* [API Key](https://docs.akeyless.io/docs/api-key) 

* [AWS IAM](https://docs.akeyless.io/docs/aws-iam) 

* [Azure Active Directory](https://docs.akeyless.io/docs/azure-ad)

## API Key Authentication

To set your Bastion default authentication based on [API Key](https://docs.akeyless.io/docs/api-key), set the `accessID` and the matching `accessKey`  with a list of `allowedAccessIDs` that will be authorized to request access:

```yaml values.yaml
privilegedAccess:
  accessID: "<API Key Access ID>"
  accessKey: "<Access Key>"
  allowedAccessIDs: 
    - p-xxxxxxx
```

## CSP IAM Authentication

While running your K8s cluster inside your cloud environment, you can use [AWS IAM](https://docs.akeyless.io/docs/aws-iam), or [Azure Active Directory](https://docs.akeyless.io/docs/azure-ad), using machine-to-machine authentication between Akeyless and your Cloud Service Provider with a list of allowed `AccessIDs` that will be authorized to request access.

## AWS IAM

AWS IAM can be used in the following approach: 

* Instance IAM Role 

While working with an IAM Role associated with the instance himself, you can simply provide your [AWS IAM](https://docs.akeyless.io/docs/aws-iam) `Access ID`  as your <code>accessID</code>, with a list of `allowedAccessIDs` that will be authorized to request access:

```yaml values.yaml
privilegedAccess:
  accessID: "<AWS IAM Access ID>"
  allowedAccessIDs: 
    - p-xxxxxxx
```

## Azure Active Directory

Azure AD authentication is provided to AKS clusters with OpenID Connect. OpenID Connect is an identity layer built on top of the OAuth 2.0 protocol. Akeyless treats Azure as a trusted third party and verifies entities based on a JWT signed by the Azure Active Directory for the configured tenant.

Set your [Azure Active Directory](https://docs.akeyless.io/docs/azure-ad) `Access ID` as your <code>accessID</code> with a list of `allowedAccessIDs` that will be authorized to request access:

```yaml values.yaml
privilegedAccess:
  accessID: "Azure AD Access ID"
  allowedAccessIDs: 
    - p-xxxxxxx
```

# Install

```shell
helm install <RELEASE NAME> akeyless/akeyless-zero-trust-web-access -f values.yaml
```

Verify that both pods are up and running: 

<code>web-worker-deployment</code>\ <code>web-dispatcher-deployment</code>
