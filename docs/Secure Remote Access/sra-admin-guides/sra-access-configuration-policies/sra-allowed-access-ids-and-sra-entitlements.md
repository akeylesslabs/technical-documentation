---
title: Allowed Access IDs and SRA Entitlements
excerpt: ''
deprecated: false
hidden: true
metadata:
  title: ''
  description: ''
  robots: index
next:
  description: ''
slug: sra-allowed-access-ids-and-sra-entitlements
---
Use this page to configure which identities can request SRA sessions from a given Gateway (or, for web application access, a given Zero Trust Web Access (ZTWA) deployment), and which privileged identity that deployment uses to fetch item data on the requester's behalf.

This is also the setting to use if you want to **restrict which users can get service from a specific Gateway** (or a specific ZTWA deployment) i.e. create an allow list scoped to one cluster/deployment, rather than relying on RBAC alone. It sits below RBAC: RBAC decides what a permitted identity is allowed to do; this allow list decides whether that identity's requests are even accepted by _this_ Gateway (or ZTWA deployment) in the first place.

## Entitlement Model

SRA request authorization at the deployment level is based on two identity classes:

- **Privileged Access ID**: The machine identity that authenticates to Akeyless and fetches the requested item data on behalf of a user. This is the Gateway's own authentication method. For Zero Trust Web Access (ZTWA), this is a the same privileged identity configured for the Gateway deployment and  this identity typically needs `read` and `list` on the relevant secrets/targets.
- **Allowed/Authorized Access IDs**: The requester identities permitted to initiate remote access sessions through that specific Gateway or ZTWA deployment. If this list is left empty, all Access IDs that otherwise pass RBAC are authorized to use the deployment; setting it restricts usage to the listed identities only.

Both must be configured correctly for a session to succeed: the Privileged Access ID must be able to fetch the item, and the requester's Access ID must be in the allow list (when one is configured) in addition to passing the [SRA RBAC](https://docs.akeyless.io/docs/sra-rbac-model) checks on the requested path.

**This is a deployment-level allow list, not a substitute for RBAC.** Passing this allow list does not by itself grant SRA access, the requester's Access Role still needs the relevant `sra-rule` capability (`allow_access`, `request_access`, or `justify_access_only`) on the target path. See [SRA RBAC Model](https://docs.akeyless.io/docs/sra-rbac-model).

## Naming Differs by Deployment Type  Use the Correct Key

There are two distinct SRA deployment types the **Gateway** and **Zero Trust Web Access (ZTWA)**- each with its own chart/env file, and each uses a different name for the requester allow list. They are functionally equivalent in purpose (restrict who may use that deployment), but the parameter name is **not interchangeable**  using the wrong name for a given deployment type silently does nothing.

| Deployment type              | Deployment model                              | Privileged identity parameter                                                                             | Requester allow list parameter                                                                          |
| ---------------------------- | --------------------------------------------- | --------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------- |
| Gateway                      | Helm (`akeyless-gateway` chart)               | Configured via the Gateway's own auth method (`globalConfig.gatewayAuth`)                                 | `globalConfig.authorizedAccessIDs` (comma-separated list, under the chart's top-level/"Global" section) |
| Gateway                      | Docker Compose                                | `GATEWAY_ACCESS_ID` / `GATEWAY_ACCESS_TYPE`  in `gateway.env`                                             | `GATEWAY_AUTHORIZED_ACCESS_ID`                                                                          |
| Zero Trust Web Access (ZTWA) | Helm (`akeyless-zero-trust-web-access` chart) | `privilegedAccess.accessID` (+ `accessKey` if using API Key auth), under the chart's configuration values | `privilegedAccess.allowedAccessIDs` (list), under the same configuration section                        |
| Zero Trust Web Access (ZTWA) | Docker Compose                                | `PRIVILEGED_ACCESS_ID` in the ZTWA Docker Compose environment variables                                   | `ALLOWED_ACCESS_IDS` in the ZTWA Docker Compose environment variables                                   |

This table is meant to prevent confusion with the following parameters`globalConfig.allowedAccessPermissions` (Helm) / `ALLOWED_ACCESS_PERMISSIONS` (Docker Compose). That setting controls which Access IDs may **administer the Gateway itself** (admin console/API access and sub-claim permissions) ,it is unrelated to who may request an SRA session.

## CLI Configuration Example For Gateway

Use the Gateway allowed access commands to add and remove requester IDs for a cluster. This is the mechanism to use for the Gateway/ SRA deployment for Docker Compose, and it also works for Kubernetes/Helm deployments as an alternative to editing `values.yaml` directly:

```shell
akeyless add-gw-access-id \
  --cluster-name <CLUSTER_NAME> \
  --access-id <REQUESTER_ACCESS_ID>
```

```shell
akeyless delete-gw-access-id \
  --cluster-name <CLUSTER_NAME> \
  --access-id <REQUESTER_ACCESS_ID>
```

For command details, see [CLI Reference - Gateway Secure Remote Access](https://docs.akeyless.io/docs/cli-reference-sra).

## Helm Example For Gateway

```yaml values.yaml
globalConfig:
  # Comma-separated list. Empty = all Access IDs that pass RBAC are authorized.
  authorizedAccessIDs: "p-1111,p-2222"
```

## Helm Example For ZTWA

```yaml values.yaml
dispatcher:
  config:
    privilegedAccess:
      accessID: "p-privileged-id"
      allowedAccessIDs:
        - p-1111
        - p-2222
```

## Docker Compose Example for ZTWA

```yaml
services:
  dispatcher:
    environment:
      - PRIVILEGED_ACCESS_ID=<PRIVILEGED_ACCESS_ID>
      - ALLOWED_ACCESS_IDS=[AccessID1,AccessID2]
```

## SSH Certificate Issuer Entitlements

For SSH-based SRA sessions, the SSH Certificate Issuer is part of the effective entitlement chain:

- Secure Remote Access must be enabled on the issuer.
- The issuer can restrict target hosts through host restriction controls.

For issuer configuration details, see [SSH Certificates](https://docs.akeyless.io/docs/sra-ssh-certificates).

## Validation Checklist

1. Confirm the Privileged Access ID/identity is configured and valid for your deployment type (Gateway/Unified SRA vs. ZTWA).
2. Confirm requester Access IDs are present in the correct allow list for the deployment type you're restricting  `authorizedAccessIDs` for Gateway/SRA , and `allowedAccessIDs` for ZTWA
3. Confirm you have not confused this with `allowedAccessPermissions`/`ALLOWED_ACCESS_PERMISSIONS` (Gateway admin access, not SRA requester access).
4. Confirm the requester's Access Role has the required SRA RBAC capability (`allow_access`, `request_access`, or `justify_access_only`) on the target path, see [SRA RBAC Model](https://docs.akeyless.io/docs/sra-rbac-model). Passing the allow list alone is not sufficient.
5. Confirm the SSH Certificate Issuer is enabled for SRA when SSH-based access is required.

## Related Pages

- [SRA RBAC Model](https://docs.akeyless.io/docs/sra-rbac-model)
- [Access Configuration and Policies](https://docs.akeyless.io/docs/sra-access-configuration-policies)
- [Zero Trust Web Access Topology](https://docs.akeyless.io/docs/sra-web-access-topology)
- [Zero Trust Web Access on Docker](https://docs.akeyless.io/docs/sra-web-access-docker)
- [Gateway Authentication and Access](https://docs.akeyless.io/docs/gateway-authentication-and-access)
- [CLI Reference - Gateway Secure Remote Access](https://docs.akeyless.io/docs/cli-reference-sra)

<br />