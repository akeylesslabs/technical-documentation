---
title: Basic Bastion
excerpt: ''
deprecated: false
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

The Akeyless Basic Bastion provides Secure Remote Access to resources using Akeyless Just In Time credentials (dynamic secrets and SSH certificates).

This chart bootstraps an Akeyless Basic Bastion deployment on a Kubernetes cluster using the Helm package manager.

To spin an Akeyless Basic Bastion using docker please refer to the last section on this page. 

## Prerequisites

* Horizonal Auto-Scaling

* Helm Installed

* K8s Installed

****Network****\
Currently, when using DB application (mysql, mongodb.mssql) via the Basic Bastion, it'll only work properly when using load balancer with "sticky" session:

* Ingress - Make sure to use sticky session annotation, for example nginx.ingress.kubernetes.io/affinity: "cookie" in Nginx

* Cloud Provider LB - Make sure to config the LB to support sticky session, for example is AWS, using ELB: [https://docs.aws.amazon.com/elasticloadbalancing/latest/classic/elb-sticky-sessions.html](https://docs.aws.amazon.com/elasticloadbalancing/latest/classic/elb-sticky-sessions.html)

> 🚧 Note:
>
> To enable Secure Remote Access features you will have to get an access-key to Akeyless private repository. Please contact your Account Manager for more details.

## Installing the Chart

Add Akeyless helm charts repository to your Helm repository list:

```shell
helm repo add akeyless https://akeylesslabs.github.io/helm-charts
helm repo update
```

The values.yaml file holds default values, copy the file from: (not available).

Or run the following helm command to generate the values file:

```shell
helm show values akeyless/akeyless-zero-trust-bastion > values.yaml
```

And replace the values with the ones from your environment where needed.

The following parameters are mandatory: 

<Table align={["left","left","left"]}>
  <thead>
    <tr>
      <th>
        Parameter
      </th>

      <th>
        Default Value
      </th>

      <th>
        Info
      </th>
    </tr>
  </thead>

  <tbody>
    <tr>
      <td>
        dockerRepositoryCreds
      </td>

      <td>
        N\A
      </td>

      <td>
        Credentials to access Akeyless internal image
      </td>
    </tr>

    <tr>
      <td>
        apiGatewayURL
      </td>

      <td>
        [https://rest.akeyless.io](https://rest.akeyless.io)
      </td>

      <td>
        A full URL of Akeyless Gateway.
      </td>
    </tr>

    <tr>
      <td>
        privilegedAccess
      </td>

      <td>
        N\A
      </td>

      <td>
        Optional credentials for zero-trust access: if provided, it is possible for end users to have only "list" permissions on Akeyless item.\
        Currently supported AWS IAM.
      </td>
    </tr>

    <tr>
      <td>
        allowedAccessIDs
      </td>

      <td>
        [bl
      </td>

      <td>
        Limit access to privileged items only for these end user access ID.\
        If left empty, all access Id are allowed
      </td>
    </tr>
  </tbody>
</Table>

Install the chart: 

```shell
helm install <RELEASE NAME> akeyless/akeyless-zero-trust-bastion -f values.yaml
```

Verify that the Basic Bastion pod is up and running.

## Installing Basic Bastion via Docker

Akeyless Basic bastion can be deployed via docker: 

```shell
docker run -d -p 8888:8888 \
    -e AKEYLESS_URL=https://api.akeyless.io \
    -e PRIVILEGED_ACCESS_ID=<Access ID>\
    -e PRIVILEGED_ACCESS_KEY=<Access Key>\
    --name zero_trust_bastion \
    akeyless/zero-trust-bastion
```
