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

Use this page as the single reference for Gateway access permissions used in `allowedAccessPermissions`.

## Permission Catalog

> ℹ️ **Note:**
>
> In current Gateway behavior, `general` and `defaults` are treated as a compatible pair for effective access. If one is configured, the other is included in effective permission evaluation.

| Permission key | Console label | Typical use |
| --- | --- | --- |
| `defaults` | Defaults | Manage default login and default encryption settings. |
| `general` | General | Manage general Gateway settings, including URL and TLS behavior. |
| `acme` | ACME | Manage Gateway ACME configuration and workflows. |
| `admin` | Admin | Full Gateway administration, including access permission management. |
| `automatic_migration` | Automatic Migration | Manage [Dynamic Secrets](https://docs.akeyless.io/docs/how-to-create-dynamic-secret) settings used by automatic migration workflows. |
| `caching` | Caching | Manage cache and offline behavior settings. |
| `classic_keys` | Classic Keys | Manage [Classic Keys](https://docs.akeyless.io/docs/classic-keys) through the Gateway. |
| `dynamic_secret` | Dynamic Secret | Manage dynamic secret configuration. |
| `event_forwarding` | Event Forwarding | Manage [Event Forwarding](https://docs.akeyless.io/docs/event-center) settings. |
| `hsm` | N/A in current Console Gateway access permission list | Manage Gateway HSM integration settings. |
| `k8s_auth` | Kubernetes Auth | Manage [Kubernetes](https://docs.akeyless.io/docs/auth-with-kubernetes) authentication configuration for the Gateway. |
| `kerberos_auth` | Kerberos Auth | Manage Kerberos authentication configuration for the Gateway. |
| `kmip` | KMIP | Manage KMIP service configuration. |
| `ldap_auth` | LDAP Auth | Manage [LDAP](https://docs.akeyless.io/docs/auth-with-ldap) authentication configuration for the Gateway. |
| `log_forwarding` | Log Forwarding | Manage log forwarding settings. |
| `rotate_secret_value` | Rotate Secret Value | Rotate secret values through the Gateway without enabling broader manual secret editing. |
| `rotated_secret` | Rotated Secret | Manage rotated secret configuration. |
| `sdr` | N/A in current Console Gateway access permission list | Manage Gateway SDR scanner configuration and operations. |
| `sra_config` | Remote Access Configuration (`sra` in Console API enum) | Manage Secure Remote Access (SRA) Gateway configuration. |
| `targets` | Targets | Manage target-related operations through the Gateway. |
| `zero_knowledge_encryption` | Zero Knowledge Encryption | Manage [Zero-Knowledge](https://docs.akeyless.io/docs/zero-knowledge) Gateway settings. |

Console behavior note: in the current custom permission multi-select UI, `admin` and `general` are intentionally excluded for backward compatibility.

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
