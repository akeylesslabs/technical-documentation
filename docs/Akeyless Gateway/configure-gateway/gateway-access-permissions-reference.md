---
title: Gateway Access Permissions Reference
excerpt: ''
deprecated: false
hidden: false
metadata:
  title: ''
  description: ''
  robots: index
---

<GatewayConfigManagementNote />
Use this page as the single reference for Gateway access permissions used in `allowedAccessPermissions`.

## Permission Catalog

> ℹ️ **Note:**
>
> In current Gateway behavior, `general` and `defaults` are treated as a compatible pair for effective access. If one is configured, the other is included in effective permission evaluation.

| Permission | Typical use |
| --- | --- |
| `defaults` | Manage default login and default encryption settings. |
| `acme` | Manage Gateway ACME configuration and workflows. |
| `admin` | Full Gateway administration, including access permission management. |
| `automatic_migration` | Manage [Dynamic Secrets](https://docs.akeyless.io/docs/how-to-create-dynamic-secret) settings used by automatic migration workflows. |
| `caching` | Manage cache and offline behavior settings. |
| `classic_keys` | Manage [Classic Keys](https://docs.akeyless.io/docs/classic-keys) through the Gateway. |
| `dynamic_secret` | Manage dynamic secret configuration. |
| `event_forwarding` | Manage [Event Forwarding](https://docs.akeyless.io/docs/event-center) settings. |
| `general` | Manage general Gateway settings, including URL and TLS behavior. |
| `hsm` | Manage Gateway HSM integration settings. |
| `k8s_auth` | Manage [Kubernetes](https://docs.akeyless.io/docs/auth-with-kubernetes) authentication configuration for the Gateway. |
| `kerberos_auth` | Manage Kerberos authentication configuration for the Gateway. |
| `kmip` | Manage KMIP service configuration. |
| `ldap_auth` | Manage [LDAP](https://docs.akeyless.io/docs/auth-with-ldap) authentication configuration for the Gateway. |
| `log_forwarding` | Manage log forwarding settings. |
| `rotate_secret_value` | Rotate secret values through the Gateway without enabling broader manual secret editing. |
| `rotated_secret` | Manage rotated secret configuration. |
| `sdr` | Manage Gateway SDR scanner configuration and operations. |
| `sra_config` | Manage Secure Remote Access (SRA) Gateway configuration. |
| `targets` | Manage target-related operations through the Gateway. |
| `zero_knowledge_encryption` | Manage [Zero-Knowledge](https://docs.akeyless.io/docs/zero-knowledge) Gateway settings. |

## Permission Scope Behavior

Administrative operations for Gateway allowed access management require `admin` permission.

For item-related operations (`targets`, `classic_keys`, `dynamic_secret`, `rotated_secret`, and `rotate_secret_value`), access is evaluated in two scopes:

1. Gateway allowed access permission for the relevant component.
2. RBAC path permission for the specific item path.

Both scopes must allow the operation.

## Related Pages

* [Authentication and Access](https://docs.akeyless.io/docs/gateway-authentication-and-access)
* [Kubernetes with Helm Deployment](https://docs.akeyless.io/docs/gateway-deploy-kubernetes-helm)
* [Gateway Docker Advanced Configuration](https://docs.akeyless.io/docs/gateway-docker-advanced-configuration)
* [Deploy with Docker Compose](https://docs.akeyless.io/docs/gateway-deploy-docker-compose)
* [Kubernetes Legacy Deployment](https://docs.akeyless.io/docs/gateway-kubernetes-legacy-deployment)
