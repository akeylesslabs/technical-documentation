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
[block:callout]
{
  "type": "danger",
  "title": "Note",
  "body": "This chart has been replaced by [Secure Remote Access Bastion](https://docs.akeyless.io/docs/secure-remote-access-bastion)"
}
[/block]
The Akeyless Basic Bastion provides Secure Remote Access to resources using Akeyless Just In Time credentials (dynamic secrets and SSH certificates).

This chart bootstraps an Akeyless Basic Bastion deployment on a Kubernetes cluster using the Helm package manager.

To spin an Akeyless Basic Bastion using docker please refer to the last section on this page. 
[block:api-header]
{
  "title": "Prerequisites"
}
[/block]
* Horizonal Auto-Scaling

* Helm Installed

* K8s Installed

***_Network_***
Currently, when using DB application (mysql, mongodb.mssql) via the Basic Bastion, it'll only work properly when using load balancer with "sticky" session:

* Ingress - Make sure to use sticky session annotation, for example nginx.ingress.kubernetes.io/affinity: "cookie" in Nginx

* Cloud Provider LB - Make sure to config the LB to support sticky session, for example is AWS, using ELB: https://docs.aws.amazon.com/elasticloadbalancing/latest/classic/elb-sticky-sessions.html
[block:callout]
{
  "type": "warning",
  "body": "To enable Secure Remote Access features you will have to get an access-key to Akeyless private repository. Please contact your Account Manager for more details.",
  "title": "Note:"
}
[/block]

[block:api-header]
{
  "title": "Installing the Chart"
}
[/block]
Add Akeyless helm charts repository to your Helm repository list:
[block:code]
{
  "codes": [
    {
      "code": "helm repo add akeyless https://akeylesslabs.github.io/helm-charts\nhelm repo update",
      "language": "shell"
    }
  ]
}
[/block]
The values.yaml file holds default values, copy the file from: 

https://github.com/akeylesslabs/helm-charts/tree/main/charts/akeyless-zero-trust-bastion

Or run the following helm command to generate the values file:

[block:code]
{
  "codes": [
    {
      "code": "helm show values akeyless/akeyless-zero-trust-bastion > values.yaml",
      "language": "shell"
    }
  ]
}
[/block]
And replace the values with the ones from your environment where needed.
 
The following parameters are mandatory: 
[block:parameters]
{
  "data": {
    "h-0": "Parameter",
    "h-1": "Default Value",
    "h-2": "Info",
    "0-0": "dockerRepositoryCreds",
    "0-1": "N\\A",
    "0-2": "Credentials to access Akeyless internal image",
    "1-0": "apiGatewayURL",
    "1-1": "https://rest.akeyless.io",
    "1-2": "A full URL of Akeyless Gateway.",
    "2-0": "privilegedAccess",
    "2-1": "N\\A",
    "2-2": "Optional credentials for zero-trust access: if provided, it is possible for end users to have only \"list\" permissions on Akeyless item.  \nCurrently supported AWS IAM.",
    "3-0": "allowedAccessIDs",
    "3-1": "[ ]",
    "3-2": "Limit access to privileged items only for these end user access ID.\nIf left empty, all access Id are allowed"
  },
  "cols": 3,
  "rows": 4
}
[/block]
Install the chart: 
[block:code]
{
  "codes": [
    {
      "code": "helm install <RELEASE NAME> akeyless/akeyless-zero-trust-bastion -f values.yaml",
      "language": "shell"
    }
  ]
}
[/block]
Verify that the Basic Bastion pod is up and running.
[block:api-header]
{
  "title": "Installing Basic Bastion via Docker"
}
[/block]
Akeyless Basic bastion can be deployed via docker: 
[block:code]
{
  "codes": [
    {
      "code": "docker run -d -p 8888:8888 \\\n    -e AKEYLESS_URL=https://api.akeyless.io \\\n    -e PRIVILEGED_ACCESS_ID=<Access ID>\\\n    -e PRIVILEGED_ACCESS_KEY=<Access Key>\\\n    --name zero_trust_bastion \\\n    akeyless/zero-trust-bastion",
      "language": "shell"
    }
  ]
}
[/block]