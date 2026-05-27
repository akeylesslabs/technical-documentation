---
title: Authentication and Access
excerpt: ''
deprecated: false
hidden: false
metadata:
  title: ''
  description: ''
  robots: index
---

<GatewayConfigManagementNote />
Use this page to configure how administrators authenticate to Akeyless Gateway and how permissions are delegated to additional users.

## What This Configuration Controls

Authentication and access settings define:

* The default identity used by the Gateway to connect to Akeyless.
* Which human users can manage Gateway settings.
* Which Gateway components each authorized user can manage.

This configuration affects the management plane of the Gateway, including login to the Gateway Configuration Manager and configuration operations.

## Authentication Model

Gateway access is typically configured in two layers:

1. A primary Gateway authentication method.
2. A list of additional allowed users or identities with explicit permissions.

Supported authentication methods vary by deployment type. Common methods include:

* API key
* Cloud identity (AWS IAM, Azure Active Directory, or GCP)
* Certificate-based authentication
* Universal Identity

## Configure the Primary Gateway Identity

Set a primary authentication method that the Gateway uses for control-plane operations.

The primary Gateway identity must be associated with an RBAC policy that includes an Administrative rule scoped to Gateway management.
For Gateway Console (UI) access, this Administrative rule permission scope must be set to `scope` or `all`.

### Configure the Gateway Identity with Helm

For Kubernetes Helm deployments, configure `globalConfig.gatewayAuth` in `values.yaml`:

```yaml values.yaml
globalConfig:
  gatewayAuth:
    gatewayAccessId: <Access ID>
    gatewayAccessType: <access_key|aws_iam|azure_ad|gcp|cert|uid>
```

For standalone Docker deployments, set the corresponding environment variables in the `docker run` command.

### Configure the Gateway Identity with Docker

For standalone Docker deployments, set the corresponding environment variables in the `docker run` command.
 Use one of the following patterns for the primary Gateway identity:

| Auth method | Required environment variables |
| --- | --- |
| API key | `GATEWAY_ACCESS_ID`, `GATEWAY_ACCESS_KEY` |
| AWS IAM / Azure Active Directory / GCP | `GATEWAY_ACCESS_ID` |
| Certificate-based authentication | `GATEWAY_ACCESS_ID`, `GATEWAY_CERTIFICATE`, `GATEWAY_CERTIFICATE_KEY` |
| Universal Identity | `ADMIN_UID_TOKEN` |

For compatibility with older deployments, legacy variable names may still appear in existing commands, such as `ADMIN_ACCESS_ID` and `ADMIN_ACCESS_KEY`.

Example API key command:

```shell
docker run -d -p 8000:8000 -p 5696:5696 \
  -e GATEWAY_ACCESS_ID="p-xxxxxx" \
  -e GATEWAY_ACCESS_KEY="<Access-Key>" \
  --name akeyless-gw akeyless/base:latest-akeyless
```

## Configure Allowed Access Permissions

After setting the primary identity, define who can manage Gateway settings with `allowedAccessPermissions`.

Gateway access is permission-based. Access is granted from configured `allowedAccessPermissions` entries and their assigned permissions.

This means your primary RBAC policy defines baseline administrative access, while `allowedAccessPermissions` delegates Gateway-scoped access to additional identities.
If the Administrative rule permission scope is not set to `scope` or `all`, admin users will be blocked from Gateway Console (UI) access.
CLI and API management operations can still be allowed when the role grants the required permissions.

```yaml values.yaml
globalConfig:
  allowedAccessPermissions:
    - name: Administrators
      access_id: p-xxxxxxx
      permissions:
        - admin
```

To restrict access further, include `sub_claims` in each entry:

```yaml values.yaml
globalConfig:
  allowedAccessPermissions:
    - name: Operations
      access_id: p-xxxxxxx
      sub_claims:
        email:
          - admin@example.com
        group:
          - platform-team
      permissions:
        - admin
```

`allowedAccessPermissions` also supports wildcard matching in `access_id`.
Use `*` to apply a permission set to any access ID.

```yaml values.yaml
globalConfig:
  allowedAccessPermissions:
    - name: Default read-only
      access_id: "*"
      permissions:
        - defaults
        - general
```

In this example, all users in the current account can perform actions on this Gateway according to their existing RBAC permissions. For example, if a user has RBAC permissions to create Dynamic Secrets or Rotated Secrets for a specific path, they can create items associated with this Gateway for that path.

## Permission Scope Guidance

For role-and-scope planning across common deployment patterns, see [Permission baseline by use case](https://docs.akeyless.io/docs/gateway-best-practices#permission-baseline-by-use-case).

Use the minimum permissions required for each operational role.

> ℹ️ **Note:**
>
> In current Gateway behavior, `general` and `defaults` are treated as a compatible pair for effective access. If one is configured, the other is included in effective permission evaluation.

| Permission | Typical use |
| --- | --- |
| `admin` | Full Gateway administration, including access permission management. |
| `defaults` | Manage default login and default encryption settings. |
| `targets` | Manage target-related operations through the Gateway. |
| `classic_keys` | Manage [Classic Keys](https://docs.akeyless.io/docs/classic-keys) through the Gateway. |
| `automatic_migration` | Manage [Dynamic Secrets](https://docs.akeyless.io/docs/how-to-create-dynamic-secret) settings used by automatic migration workflows. |
| `dynamic_secret` | Manage dynamic secret configuration. |
| `rotated_secret` | Manage rotated secret configuration. |
| `rotate_secret_value` | Rotate secret values through the Gateway without enabling broader manual secret editing. |
| `log_forwarding` | Manage log forwarding settings. |
| `zero_knowledge_encryption` | Manage [Zero-Knowledge](https://docs.akeyless.io/docs/zero-knowledge) Gateway settings. |
| `caching` | Manage cache and offline behavior settings. |
| `event_forwarding` | Manage [Event Forwarding](https://docs.akeyless.io/docs/event-center) settings. |
| `ldap_auth` | Manage [LDAP](https://docs.akeyless.io/docs/auth-with-ldap) authentication configuration for the Gateway. |
| `kerberos_auth` | Manage Kerberos authentication configuration for the Gateway. |
| `k8s_auth` | Manage [Kubernetes](https://docs.akeyless.io/docs/auth-with-kubernetes) authentication configuration for the Gateway. |
| `sra_config` | Manage Secure Remote Access (SRA) Gateway configuration. |
| `hsm` | Manage Gateway HSM integration settings. |
| `acme` | Manage Gateway ACME configuration and workflows. |
| `sdr` | Manage Gateway SDR scanner configuration and operations. |
| `kmip` | Manage KMIP service configuration. |
| `general` | Manage general Gateway settings, including URL and TLS behavior. |

Administrative operations for Gateway Allowed Access management require `admin` permission.

For item-related operations (`targets`, `classic_keys`, `dynamic_secret`, `rotated_secret`, and `rotate_secret_value`), access is evaluated in two scopes:

1. Gateway Allowed Access permission for the relevant component.
2. RBAC path permission for the specific item path.

Both scopes must allow the operation.

## Recommended Access Pattern

* Use one dedicated machine identity for the Gateway primary authentication method.
* Add a separate admin group through `allowedAccessPermissions` for day-to-day management.
* Use least-privilege permissions for non-admin roles.
* Review allowed users and permission scope on a regular schedule.

## Validation Checklist

After applying authentication and access configuration:

1. Confirm the Gateway starts successfully.
2. Confirm login works for intended admin users.
3. Confirm each admin role used for Gateway management has Administrative permission scope set to `scope` or `all`.
4. Confirm non-admin users can only access the permitted configuration areas.
5. Confirm unauthorized users are blocked.

## Related Pages

* [Gateway Authentication](https://docs.akeyless.io/docs/gateway-authentication-and-access)
* [Access Permissions](https://docs.akeyless.io/docs/gateway-authentication-and-access)
* [Kubernetes with Helm Deployment](https://docs.akeyless.io/docs/gateway-deploy-kubernetes-helm)
* [Gateway Docker Advanced Configuration](https://docs.akeyless.io/docs/gateway-docker-advanced-configuration)
