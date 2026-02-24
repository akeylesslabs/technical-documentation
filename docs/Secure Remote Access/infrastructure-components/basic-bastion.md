---
title: Basic Bastion
excerpt: ''
deprecated: true
hidden: true
metadata:
  title: ''
  description: ''
  robots: index
next:
  description: ''
  pages:
    - type: basic
      slug: database-secure-remote-access
      title: Database Secure Remote Access
    - type: basic
      slug: remote-desktop-secure-access
      title: Remote Desktop Secure Access
    - type: basic
      slug: aws-console-secure-remote-access
      title: AWS Console Secure Remote Access
---
> ❗️ Note
>
> This chart has been replaced by [Secure Remote Access Bastion](https://docs.akeyless.io/docs/secure-remote-access-bastion) and is no longer available.

The Akeyless Basic Bastion provides Secure Remote Access to resources using Akeyless Just In Time credentials (Dynamic Secrets and SSH certificates).

This chart bootstraps an Akeyless Basic Bastion deployment on a Kubernetes cluster using the Helm package manager.

To spin an Akeyless Basic Bastion using Docker please refer to the last section on this page.

## Prerequisites

* Horizontal Auto-Scaling

* Helm Installed

* Kubernetes Installed

### Network

Currently, when using DB application (MySQL, MongoDB) by way of the Basic Bastion, it'll only work properly when using load balancer with "sticky" session:

* Ingress - Make sure to use sticky session annotation, for example, `nginx.ingress.kubernetes.io/affinity: "cookie"` in NGINX

* Cloud Provider LB - Make sure to config the LB to support sticky session, for example is AWS, using ELB: [https://docs.aws.amazon.com/elasticloadbalancing/latest/classic/elb-sticky-sessions.html](https://docs.aws.amazon.com/elasticloadbalancing/latest/classic/elb-sticky-sessions.html).

> **Note:**
>
> To enable Secure Remote Access features you will have to get an access-key to Akeyless private repository. Please contact your Account Manager for more details.

## Installing the Chart

Add Akeyless Helm charts repository to your Helm repository list:

```shell
helm repo add akeyless https://akeylesslabs.github.io/helm-charts
helm repo update
```

The `values.yaml` file holds default values, copy the file from: `https://github.com/akeylesslabs/helm-charts/tree/main/charts/akeyless-zero-trust-bastion`

Or run the following Helm command to generate the values file:

```shell
helm show values akeyless/akeyless-zero-trust-bastion > values.yaml
```

And replace the values with the ones from your environment where needed. The following parameters are mandatory:

| Parameter               | Default Value              | Info                                                                                                                                                                     |
| `dockerRepositoryCreds` | N/A                        | Credentials to access Akeyless internal image                                                                                                                            |
| `apiGatewayURL`         | `https://rest.akeyless.io` | A full URL of Akeyless Gateway.                                                                                                                                          |
| `privilegedAccess`      | N/A                        | Optional credentials for zero-trust access: if provided, it is possible for end users to have only "list" permissions on an Akeyless item. Currently supported: AWS IAM. |
| `allowedAccessIDs`      | `[bl`                      | Limit access to privileged items only for these end user access IDs. If left empty, all access IDs are allowed.                                                          |

Install the chart:

```shell
helm install <RELEASE NAME> akeyless/akeyless-zero-trust-bastion -f values.yaml
```

Verify that the Basic Bastion pod is up and running.

## Installing Basic Bastion by way of Docker

Akeyless Basic bastion can be deployed by way of Docker:

```shell
docker run -d -p 8888:8888 \
    -e AKEYLESS_URL=https://api.akeyless.io \
    -e PRIVILEGED_ACCESS_ID=<Access ID>\
    -e PRIVILEGED_ACCESS_KEY=<Access Key>\
    --name zero_trust_bastion \
    akeyless/zero-trust-bastion
```
