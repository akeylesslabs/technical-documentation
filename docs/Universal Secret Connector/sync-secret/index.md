---
title: Sync Secrets
slug: sync-secret
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
The Akeyless [Universal Secret Connector](https://docs.akeyless.io/docs/universal-secrets-connector) provides a powerful way to ensure that secrets remain synchronized across multiple external secret management solutions. Whenever a secret value is updated in Akeyless, the connector automatically ensures that the updated value is propagated to all integrated systems in real time, eliminating the need for manual synchronization.

Sync workflows are available for both [Static Secrets](https://docs.akeyless.io/docs/sync-a-static-secret) and [Rotated Secrets](https://docs.akeyless.io/docs/sync-a-rotated-secret).

## Prerequisites

* Universal Secret Connector Item.

* An [Akeyless Gateway](https://docs.akeyless.io/docs/gateway-overview) with **Read** permission on the associated USC and its target.

* An [Authentication Method](https://docs.akeyless.io/docs/access-and-authentication-methods) with **Read** and **Update** permission on the [Rotated Secret](https://docs.akeyless.io/docs/rotated-secrets) item, and **Read** permission on the associated USC.

![Illustration for: An Authentication Method with Read and Update permission on the Rotated Secret item, and Read permission on the associated USC.](https://files.readme.io/84d68fd1c6e90bb12b48f538b74db51f35ad9c15a90235524268f07b20572d61-Synced_Secret-2.png)

This solution makes managing secrets in remote endpoints more efficient and consistent, enabling a secure, centralized approach to secret lifecycle management.

## Sync Entire Folder Contents

For HashiCorp Vault USC integrations in Multi-Vault Governance (MVG), you can sync all supported secrets under a folder in one operation.

Use `folder-sync` to create sync associations for folder contents, and `folder-sync-all` to trigger sync for all folder associations:

```shell
akeyless folder-sync --name </folder/path> --usc-name </usc-name>
```

```shell
akeyless folder-sync-all --name </folder/path>
```

Use `folder-delete-sync` to remove folder-level associations:

```shell
akeyless folder-delete-sync --name </folder/path> --usc-name </usc-name>
```

For complete flags and behavior details, see [CLI Reference - Universal Secrets Connector](https://docs.akeyless.io/docs/cli-reference-universal-secrets-connector#folder-sync-commands).
