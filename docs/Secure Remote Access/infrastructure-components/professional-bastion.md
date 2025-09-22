---
title: Professional Bastion
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
      slug: ssh-remote-access
      title: SSH Remote Access
---
[block:callout]
{
  "type": "danger",
  "body": "This chart has been replaced by [Secure Remote Access Bastion](https://docs.akeyless.io/docs/secure-remote-access-bastion)",
  "title": "Note"
}
[/block]
Akeyless Professional Bastion provides SSH connections with short lived signed certificate authentication, together with session recording.

This chart bootstraps a Akeyless-Professional-Bastion deployment on a Kubernetes cluster using the Helm package manager. 

To spin Akeyless Professional-Bastion using docker please refer to the last section on this page. 
[block:api-header]
{
  "title": "Prerequisites"
}
[/block]

* Helm Installed.

* K8s Installed.

* [SSH Certificate](https://docs.akeyless.io/docs/how-to-configure-ssh).

***_Storage_***

Currently, the helm chart requires a storage class with ReadWriteMany access modes.
Since a storage class is more environment specific, you will need to provide one before proceeding. In addition, please provide 2 PersistentVolumes with <code>persistentVolumeReclaimPolicy: retain</code> and reference those PVs in the values.yaml file

e.g when running on AWS with EKS: https://docs.aws.amazon.com/eks/latest/userguide/efs-csi.html

***_Network_***

When using SSH sessions behind load balancer such as ELB, the session can be closed due to idle connection timeout, so its advise to increase it to a reasonable high value, or event unlimited.

e.g when running on AWS with ELB: https://docs.aws.amazon.com/elasticloadbalancing/latest/classic/config-idle-timeout.html?icmpid=docs_elb_console

***_Horizontal Auto-Scaling_***

Horizontal auto-scaling is based on the HorizontalPodAutoscaler object.
For it to work properly, Kubernetes metrics server must be installed in the cluster - https://github.com/kubernetes-sigs/metrics-server

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
The values.yaml file holds default values, replace the values with the ones from your environment where needed.

https://github.com/akeylesslabs/helm-charts/tree/main/charts/akeyless-ssh-bastion

If you don't have an SSH certificate ready, please follow this guide on how to create [SSH Cert issuer](https://docs.akeyless.io/docs/how-to-configure-ssh) with Akeyless vault and set your CA Public key in the values.yaml file. 

The following parameters are mandatory:
[block:parameters]
{
  "data": {
    "0-0": "dockerRepositoryCreds",
    "0-1": "N\\A",
    "0-2": "Credentials to access Akeyless private image",
    "1-0": "apiGatewayURL",
    "1-1": "https://rest.akeyless.io",
    "h-0": "Parameter",
    "h-1": "Defualt",
    "h-2": "Info",
    "1-2": "A full URL of Akeyless API GW",
    "2-0": "CAPublicKey",
    "2-1": "N\\A",
    "2-2": "SSH Cert Issuer CA Public key",
    "3-0": "privilegedAccess",
    "3-1": "N\\A",
    "3-2": "Credentials for zero-trust access: If provided, it is possible for end users to have  only \"list\" permissions on Akeyless items if privileged credentials have \"read\" access"
  },
  "cols": 3,
  "rows": 4
}
[/block]

[block:callout]
{
  "type": "success",
  "title": "Tip",
  "body": "Akeyless supports session termination, which can be configured as part of this chart deployment. \nTo enable session termination please set your Okta\\Keycloak  `apiURL` and `apiToken` under `sessionTermination` section."
}
[/block]
Install the chart:
[block:code]
{
  "codes": [
    {
      "code": "helm install <RELEASE NAME>  akeyless/akeyless-ssh-proxy -f values.yaml",
      "language": "shell"
    }
  ]
}
[/block]
Validate that Akeyless SSH pod is running.
[block:api-header]
{
  "title": "Installing Akeyless Professional Bastion via Docker"
}
[/block]
To deploy Akeyless Professional Bastion via Docker, you will have to provide a mount path which should contain the following files: 

1. ca.pub - SSH Cert Issuer CA Public key. 
[block:code]
{
  "codes": [
    {
      "code": "ssh-rsa AAAAB3NzaC1yc2EAAAA...",
      "language": "shell",
      "name": "ca.pub"
    }
  ]
}
[/block]
2. akeyless_config_file - this file should contain the following information: 

[block:code]
{
  "codes": [
    {
      "code": "https://rest.akeyless.io\ncmd=auth&access-id=<access-ID>&<access-key> ",
      "language": "shell",
      "name": "akeyless_config_file"
    }
  ]
}
[/block]

[block:code]
{
  "codes": [
    {
      "code": "docker run --name ssh_bastion -d -p 0.0.0.0:2222:22 -p 0.0.0.0:9900:9900 \\\n       -v </path/to/akeyless_config_file/>:/var/akeyless/creds \\\n       --cap-add=SYS_ADMIN akeyless/ssh-proxy:latest",
      "language": "shell",
      "name": "MacOS"
    },
    {
      "code": "docker run --name ssh_bastion -d -p 0.0.0.0:2222:22 -p 0.0.0.0:9900:9900 \\\n       -v </path/to/akeyless_config_file/>:/var/akeyless/creds \\\n       --privileged akeyless/ssh-proxy:latest",
      "language": "text",
      "name": "Ubuntu"
    }
  ]
}
[/block]
To add log forwarding capabilities please add those options to the command: 
[block:code]
{
  "codes": [
    {
      "code": "-v <path/to/logs/folder>:/tmp/ssh_logs \\\n-v <path/to/log_forwarding.conf>:/var/akeyless/conf/logand.conf ",
      "language": "shell"
    }
  ]
}
[/block]