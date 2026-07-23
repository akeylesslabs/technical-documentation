---
title: Access Configuration and Policies
excerpt: ''
deprecated: false
hidden: false
metadata:
  title: ''
  description: ''
  robots: index
next:
  description: ''
slug: sra-access-configuration-and-policies
---
Use this section to configure the SRA authorization model, who can use Secure Remote Access (SRA) and from which Gateway or, for web application access, which Zero Trust Web Access (ZTWA) deployment, how usernames are resolved for target sessions, which redirect endpoints are trusted, and which session security controls are enforced.

These settings combine RBAC (SRA-specific permissions, separate from Secrets Management RBAC), Gateway runtime configuration, ZTWA deployment configuration, and authentication method restrictions.

## Start Here by Objective

1. **Understand the SRA RBAC model first**: how SRA permissions are evaluated independently of Secrets Management RBAC, and how Approval Authority combines with Request Access: [SRA RBAC Model](https://docs.akeyless.io/docs/sra-rbac-model)
2. Define which identities can establish an SRA sessions from a given Gateway (or ZTWA deployment) — the Gateway-level allow list — and which privileged identity that deployment uses: [Allowed Access IDs and SRA Entitlements](https://docs.akeyless.io/docs/sra-allowed-access-ids-and-sra-entitlements)
3. Map identity claims to runtime target usernames: [Username Sub-Claim Mapping](https://docs.akeyless.io/docs/sra-username-sub-claim-mapping)
4. Restrict redirect and callback endpoints to approved destinations: [Redirect and SSH URL Hardening](https://docs.akeyless.io/docs/sra-redirect-and-ssh-url-hardening)
5. Configure session lifetime and SSH/web security controls: [Session TTL and Security Controls](https://docs.akeyless.io/docs/sra-session-ttl-and-security-controls)
6. Configure centralized desktop app defaults for cert issuer and web URLs: [Desktop App Default Connection Settings](https://docs.akeyless.io/docs/sra-desktop-app-default-connection-settings)

## A Note on Terminology Across Components

SRA covers more than one deployment type - the Gateway (Unified SRA) and Zero Trust Web Access (ZTWA) and the field/variable that restricts _which requester identities may use a given deployment_ is named differently between them. See [Allowed Access IDs and SRA Entitlements](https://docs.akeyless.io/docs/sra-allowed-access-ids-and-sra-entitlements) for the authoritative name-per-deployment-type table (Gateway vs. ZTWA, Helm vs. Docker Compose).

This is also the mechanism behind the advanced setting some teams look for as "restrict who can get service from a specific Gateway" or "create an allow list for this deployment" — it is the same Allowed/Authorized Access ID configuration, not a separate feature.

## Related Pages

- [SRA RBAC Model](https://docs.akeyless.io/docs/sra-rbac-model)
- [RBAC](https://docs.akeyless.io/docs/rbac)
- [SSH Certificates](https://docs.akeyless.io/docs/sra-ssh-certificates)
- [SRA Requirements](https://docs.akeyless.io/docs/sra-requirements)
- [Kubernetes Advanced Configuration](https://docs.akeyless.io/docs/sra-advanced-configuration-k8s)
- [Docker Compose Advanced Configuration](https://docs.akeyless.io/docs/sra-advanced-configuration-docker)
- [Zero Trust Web Access on K8s Advanced Configuration](https://docs.akeyless.io/docs/sra-web-access-on-k8s-adv-config)

<br />
