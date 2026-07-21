---
title: Copy of SRA Setup
deprecated: false
hidden: true
metadata:
  robots: index
---
Akeyless Secure Remote Access (SRA) runs as part of a unified Gateway deployment. The same deployment pattern can host:

* Gateway core services
* SRA web and SSH bastion components
* Zero Trust Web Access (ZTWA) components when needed

## Deployment Models

Choose one deployment model for Gateway + SRA:

1. [Kubernetes (Gateway + SRA)](https://docs.akeyless.io/docs/sra-setup-k8s)
2. [Docker Compose (Gateway + SRA)](https://docs.akeyless.io/docs/sra-docker)

If you also need isolated browser access for web applications, follow [Zero Trust Web Access Topology](https://docs.akeyless.io/docs/sra-web-access-topology).

If Gateway is already deployed, continue with the Kubernetes or Docker setup page to enable SRA components on that deployment.

## Before You Deploy

Review [Requirements](https://docs.akeyless.io/docs/sra-requirements) first for port inventory, outbound connectivity, Redis dependency, minimum resources, and platform-specific constraints.

## Related Features

* [Session Management](https://docs.akeyless.io/docs/sra-session-management)
* [Akeyless Connect](https://docs.akeyless.io/docs/sra-akeyless-connect)
* [Akeyless SCP](https://docs.akeyless.io/docs/sra-akeyless-scp)
* [SSH Certificates](https://docs.akeyless.io/docs/sra-ssh-certificates)