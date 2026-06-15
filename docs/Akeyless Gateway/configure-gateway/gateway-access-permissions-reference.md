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

### How to Use This Table

When an administrator manages Gateway access permissions:

* Use **Console label** to find and select the permission in the Gateway access permissions UI.
* Use **Permission key** when configuring permissions in API/CLI payloads, including `allowedAccessPermissions`.
* Use **Description** to understand what each permission enables and to decide the minimum required access.

If a permission has no current Console label, it is not currently selectable in the Console permission list and should be managed by permission key in API/CLI workflows.

| Console label | Permission key | Description |
| --- | --- | --- |
| Defaults | `defaults` | Manage default login and default encryption settings. |
| General | `general` | Manage general Gateway settings, including URL and TLS behavior. |
| ACME | `acme` | Manage Gateway ACME configuration and workflows. |
| Admin | `admin` | Full Gateway administration, including access permission management. |
| Automatic Migration | `automatic_migration` | Manage [Dynamic Secrets](https://docs.akeyless.io/docs/how-to-create-dynamic-secret) settings used by automatic migration workflows. |
| Caching | `caching` | Manage cache and offline behavior settings. |
| Classic Keys | `classic_keys` | Manage [Classic Keys](https://docs.akeyless.io/docs/classic-keys) through the Gateway. |
| Dynamic Secret | `dynamic_secret` | Manage dynamic secret configuration. |
| Event Forwarding | `event_forwarding` | Manage [Event Forwarding](https://docs.akeyless.io/docs/event-center) settings. |
| N/A in current Console Gateway access permission list | `hsm` | Manage Gateway HSM integration settings. |
| Kubernetes Auth | `k8s_auth` | Manage [Kubernetes](https://docs.akeyless.io/docs/auth-with-kubernetes) authentication configuration for the Gateway. |
| Kerberos Auth | `kerberos_auth` | Manage Kerberos authentication configuration for the Gateway. |
| KMIP | `kmip` | Manage KMIP service configuration. |
| LDAP Auth | `ldap_auth` | Manage [LDAP](https://docs.akeyless.io/docs/auth-with-ldap) authentication configuration for the Gateway. |
| Log Forwarding | `log_forwarding` | Manage log forwarding settings. |
| Rotate Secret Value | `rotate_secret_value` | Rotate secret values through the Gateway without enabling broader manual secret editing. |
| Rotated Secret | `rotated_secret` | Manage rotated secret configuration. |
| N/A in current Console Gateway access permission list | `sdr` | Manage Gateway SDR scanner configuration and operations. |
| Remote Access Configuration (`sra` in Console API enum) | `sra_config` | Manage Secure Remote Access (SRA) Gateway configuration. |
| Targets | `targets` | Manage target-related operations through the Gateway. |
| Zero Knowledge Encryption | `zero_knowledge_encryption` | Manage [Zero-Knowledge](https://docs.akeyless.io/docs/zero-knowledge) Gateway settings. |

Console behavior note: in the current custom permission multi-select UI, `admin` and `general` are intentionally excluded for backward compatibility.

## Permission Scope Behavior

Administrative operations for Gateway allowed access management require `admin` permission.

Gateway visibility in the Console is permission-scoped. Users with Gateway access permissions can view the Gateway in the Console only when their role includes Gateway administrative scope (`scope` or `all`).

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
