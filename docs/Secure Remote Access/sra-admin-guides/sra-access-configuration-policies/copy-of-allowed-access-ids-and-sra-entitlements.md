---
title: Copy of Allowed Access IDs and SRA Entitlements
deprecated: false
hidden: true
metadata:
  robots: index
---
Use this page to configure which identities can request SRA sessions and which privileged machine identity is used by bastion components.

## Entitlement Model

SRA request authorization is based on two identity classes:

* **Privileged Access ID**: The machine identity used by bastion components to fetch required item data and execute privileged control-plane operations.
* **Allowed Access IDs**: The requester identities allowed to initiate remote access sessions through the bastion.

Both must be configured correctly. If an Access ID is not in the allowlist, session requests are denied.

## Gateway and Bastion Configuration Areas

Common configuration areas include:

* Gateway management configuration for allowed requester IDs.
* Docker environment variables, such as `PRIVILEGED_ACCESS_ID` and `ALLOWED_ACCESS_IDS`.
* Helm values for bastion and dispatcher privileged identity settings.

For Zero Trust Web Access (ZTWA) deployments, see [Zero Trust Web Access Topology](https://docs.akeyless.io/docs/sra-web-access-topology) and [Zero Trust Web Access on Docker](https://docs.akeyless.io/docs/sra-web-access-docker).

## CLI Configuration Example

Use Gateway allowed access commands to add and remove requester IDs for a cluster:

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

## Docker Example

For Docker-based deployments, configure both the privileged identity and requester allowlist:

```shell
-e PRIVILEGED_ACCESS_ID=<PRIVILEGED_ACCESS_ID> \
-e ALLOWED_ACCESS_IDS=<ACCESS_ID_1>,<ACCESS_ID_2>
```

## SSH Certificate Issuer Entitlements

For SSH-based SRA sessions, the SSH Certificate Issuer is part of the effective entitlement chain:

* Secure Remote Access must be enabled on the issuer.
* The issuer can restrict target hosts through host restriction controls.
* For older Gateway versions, issuer allowed users can require additional `session_*` compatibility entries.

For issuer configuration details, see [SSH Certificates](https://docs.akeyless.io/docs/sra-ssh-certificates).

## Validation Checklist

1. Confirm the privileged identity is configured and valid for your deployment type.
2. Confirm requester Access IDs are present in the allowlist.
3. Confirm the requester role has the required SRA capabilities.
4. Confirm the SSH Certificate Issuer is enabled for SRA when SSH-based access is required.