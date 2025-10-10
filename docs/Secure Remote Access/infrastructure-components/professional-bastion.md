---
title: Professional Bastion
deprecated: true
hidden: true
link:
  new_tab: false
metadata:
  title: ''
  description: ''
  robots: index
next:
  pages:
    - slug: ssh-remote-access
      title: SSH Remote Access
      type: basic
---
> ❗️ Note
>
> This chart has been replaced by [Secure Remote Access Bastion](https://docs.akeyless.io/docs/secure-remote-access-bastion)

Akeyless Professional Bastion provides SSH connections with short lived signed certificate authentication, together with session recording.

This chart bootstraps a Akeyless-Professional-Bastion deployment on a Kubernetes cluster using the Helm package manager.

To spin Akeyless Professional-Bastion using docker please refer to the last section on this page.

## Prerequisites

* Helm Installed.

* K8s Installed.

* [SSH Certificate](https://docs.akeyless.io/docs/how-to-configure-ssh).

****Storage****

Currently, the helm chart requires a storage class with ReadWriteMany access modes.
Since a storage class is more environment specific, you will need to provide one before proceeding. In addition, please provide 2 PersistentVolumes with <code>persistentVolumeReclaimPolicy: retain</code> and reference those PVs in the values.yaml file

e.g when running on AWS with EKS: [https://docs.aws.amazon.com/eks/latest/userguide/efs-csi.html](https://docs.aws.amazon.com/eks/latest/userguide/efs-csi.html)

****Network****

When using SSH sessions behind load balancer such as ELB, the session can be closed due to idle connection timeout, so its advise to increase it to a reasonable high value, or event unlimited.

e.g when running on AWS with ELB: [https://docs.aws.amazon.com/elasticloadbalancing/latest/classic/config-idle-timeout.html?icmpid=docs_elb_console](https://docs.aws.amazon.com/elasticloadbalancing/latest/classic/config-idle-timeout.html?icmpid=docs_elb_console)

****Horizontal Auto-Scaling****

Horizontal auto-scaling is based on the HorizontalPodAutoscaler object.
For it to work properly, Kubernetes metrics server must be installed in the cluster - [https://github.com/kubernetes-sigs/metrics-server](https://github.com/kubernetes-sigs/metrics-server)

> 🚧 Note:
>
> To enable Secure Remote Access features you will have to get an access-key to Akeyless private repository. Please contact your Account Manager for more details.

## Installing the Chart

Add Akeyless helm charts repository to your Helm repository list:

```shell
helm repo add akeyless https://akeylesslabs.github.io/helm-charts
helm repo update
```

The values.yaml file holds default values, replace the values with the ones from your environment where needed.

[https://github.com/akeylesslabs/helm-charts/tree/main/charts/akeyless-ssh-bastion](https://github.com/akeylesslabs/helm-charts/tree/main/charts/akeyless-ssh-bastion)

If you don't have an SSH certificate ready, please follow this guide on how to create [SSH Cert issuer](https://docs.akeyless.io/docs/how-to-configure-ssh) with Akeyless vault and set your CA Public key in the values.yaml file.

The following parameters are mandatory:

| Parameter             | Defualt                                              | Info                                                                                                                                                                         |
| :-------------------- | :--------------------------------------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| dockerRepositoryCreds | N\A                                                  | Credentials to access Akeyless private image                                                                                                                                 |
| apiGatewayURL         | [https://rest.akeyless.io](https://rest.akeyless.io) | A full URL of Akeyless API GW                                                                                                                                                |
| CAPublicKey           | N\A                                                  | SSH Cert Issuer CA Public key                                                                                                                                                |
| privilegedAccess      | N\A                                                  | Credentials for zero-trust access: If provided, it is possible for end users to have  only "list" permissions on Akeyless items if privileged credentials have "read" access |

> 👍 Tip
>
> Akeyless supports session termination, which can be configured as part of this chart deployment.
> To enable session termination please set your Okta\Keycloak  `apiURL` and `apiToken` under `sessionTermination` section.

Install the chart:

```shell
helm install <RELEASE NAME>  akeyless/akeyless-ssh-proxy -f values.yaml
```

Validate that Akeyless SSH pod is running.

## Installing Akeyless Professional Bastion via Docker

To deploy Akeyless Professional Bastion via Docker, you will have to provide a mount path which should contain the following files:

1. ca.pub - SSH Cert Issuer CA Public key.

```shell ca.pub
ssh-rsa AAAAB3NzaC1yc2EAAAA...
```

2. akeyless_config_file - this file should contain the following information:

```shell akeyless_config_file
https://rest.akeyless.io
cmd=auth&access-id=<access-ID>&<access-key>
```

```shell MacOS
docker run --name ssh_bastion -d -p 0.0.0.0:2222:22 -p 0.0.0.0:9900:9900 \
       -v </path/to/akeyless_config_file/>:/var/akeyless/creds \
       --cap-add=SYS_ADMIN akeyless/ssh-proxy:latest
```
```text Ubuntu
docker run --name ssh_bastion -d -p 0.0.0.0:2222:22 -p 0.0.0.0:9900:9900 \
       -v </path/to/akeyless_config_file/>:/var/akeyless/creds \
       --privileged akeyless/ssh-proxy:latest
```

To add log forwarding capabilities please add those options to the command:

```shell
-v <path/to/logs/folder>:/tmp/ssh_logs \
-v <path/to/log_forwarding.conf>:/var/akeyless/conf/logand.conf
```
