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

### Configure the Gateway Identity with Helm

For Kubernetes Helm deployments, configure `globalConfig.gatewayAuth` in `values.yaml`:

```yaml values.yaml
globalConfig:
  gatewayAuth:
    gatewayAccessId: <Access ID>
    gatewayAccessType: <access_key|aws_iam|azure_ad|gcp|cert|universal_identity>
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

## Permission Scope Guidance

Use the minimum permissions required for each operational role.

| Permission | Typical use |
| --- | --- |
| `admin` | Full Gateway administration, including access permission management. |
| `defaults` | Manage default login and default encryption settings. |
| `targets` | Manage target-related operations through the Gateway. |
| `dynamic_secret` | Manage dynamic secret configuration. |
| `rotated_secret` | Manage rotated secret configuration. |
| `log_forwarding` | Manage log forwarding settings. |
| `caching` | Manage cache and offline behavior settings. |
| `kmip` | Manage KMIP service configuration. |
| `general` | Manage general Gateway settings, including URL and TLS behavior. |

## Recommended Access Pattern

* Use one dedicated machine identity for the Gateway primary authentication method.
* Add a separate admin group through `allowedAccessPermissions` for day-to-day management.
* Use least-privilege permissions for non-admin roles.
* Review allowed users and permission scope on a regular schedule.

## Validation Checklist

After applying authentication and access configuration:

1. Confirm the Gateway starts successfully.
2. Confirm login works for intended admin users.
3. Confirm non-admin users can only access the permitted configuration areas.
4. Confirm unauthorized users are blocked.

## Related Pages

* [Gateway Authentication](https://docs.akeyless.io/docs/gateway-authentication)
* [Access Permissions](https://docs.akeyless.io/docs/gateway-access-permissions)
* [Kubernetes with Helm Deployment](https://docs.akeyless.io/docs/gateway-chart)
* [Gateway Docker Advanced Configuration](https://docs.akeyless.io/docs/advance-gw-docker-configuration)
