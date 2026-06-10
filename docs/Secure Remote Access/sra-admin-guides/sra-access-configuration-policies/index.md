---
title: Access Configuration and Policies
slug: sra-access-configuration-and-policies
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
Use this section to configure who can request Secure Remote Access (SRA), how usernames are resolved for target sessions, which redirect endpoints are trusted, and which session security controls are enforced.

These settings combine Gateway runtime configuration, bastion deployment configuration, and authentication method restrictions.

## Start Here by Objective

1. Define who can request SRA and which bastion identity is used: [Allowed Access IDs and SRA Entitlements](https://docs.akeyless.io/docs/sra-allowed-access-ids-and-sra-entitlements)
2. Map identity claims to runtime target usernames: [Username Sub-Claim Mapping](https://docs.akeyless.io/docs/sra-username-sub-claim-mapping)
3. Restrict redirect and callback endpoints to approved destinations: [Redirect and SSH URL Hardening](https://docs.akeyless.io/docs/sra-redirect-and-ssh-url-hardening)
4. Configure session lifetime and SSH/web security controls: [Session TTL and Security Controls](https://docs.akeyless.io/docs/sra-session-ttl-and-security-controls)

## Related Pages

* [SSH Certificates](https://docs.akeyless.io/docs/sra-ssh-certificates)
* [SRA Requirements](https://docs.akeyless.io/docs/sra-requirements)
* [Kubernetes Advanced Configuration](https://docs.akeyless.io/docs/sra-advanced-configuration-k8s)
* [Docker Compose Advanced Configuration](https://docs.akeyless.io/docs/sra-advanced-configuration-docker)
* [Zero Trust Web Access on K8s Advanced Configuration](https://docs.akeyless.io/docs/sra-web-access-on-k8s-adv-config)
