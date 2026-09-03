---
title: Azure Scanner
excerpt: Setup & Required Permissions
deprecated: false
hidden: false
metadata:
  robots: index
---
# &#x20;Quick Setup

Assign the built-in **Reader** and **Key Vault Reader** roles at the subscription scope, and grant the application these Microsoft Graph **application** permissions: `Application.Read.All`, `Directory.Read.All`, `GroupMember.Read.All`, `AuditLog.Read.All`.

> The last two Graph permissions (`GroupMember.Read.All`, `AuditLog.Read.All`) require tenant **admin consent**.

For vaults using **access policies** (rather than Azure RBAC), also add a per-vault access policy with secret **List** and certificate **List** permissions.

All permissions below are **read-only**. The scanner never requires write access to your Azure environment, and never reads secret _values_ — only metadata.

***

## Must-Have Permissions

Without these, the scan **fails** and no results are produced.

| Permission                                     | Used for                                                              | If missing                                                                    |
| ---------------------------------------------- | --------------------------------------------------------------------- | ----------------------------------------------------------------------------- |
| `Microsoft.KeyVault/vaults/read`               | Discovering Key Vaults (the source for both secrets and certificates) | Secrets/certificates scan fails                                               |
| `Microsoft.Authorization/roleAssignments/read` | Identity discovery and access mapping                                 | Identities scan fails                                                         |
| Graph `Application.Read.All`                   | Entra ID application client secrets and certificates                  | Scan fails when the subscription has service principals with role assignments |

<Callout icon="⚠️" theme="warn">
  ### **Key Vault data-plane access is effectively must-have.** The two data-plane permissions below (part of **Key Vault Reader**) are what let the scanner actually list secrets and certificates inside each vault. Without them the scan **completes successfully but empty** — no secrets or certificates are found, and previously discovered findings may be closed as resolved. Always verify data-plane access is in place.

  Also note: the actions `Microsoft.KeyVault/vaults/secrets/list` and `.../certificates/list` **do not exist** in Azure — the correct action names are the ones listed below.
</Callout>

***

## Additional Permissions for a Full Scan

Without these, the scan still **completes**, but with reduced visibility. Missing permissions are reported in the scan's _Access Status_ (visible in scan details).

| Permission                                              | What it adds                                                                                                              |
| ------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------- |
| `Microsoft.KeyVault/vaults/secrets/readMetadata/action` | Listing secrets inside each vault (data plane — see warning above)                                                        |
| `Microsoft.KeyVault/vaults/certificates/read`           | Listing certificates inside each vault (data plane — see warning above)                                                   |
| `Microsoft.Authorization/roleDefinitions/read`          | Resolving role names and permissions — without it, access edges in the Security Graph cannot be computed                  |
| `Microsoft.Authorization/denyAssignments/read`          | Deny assignments — without it the graph may look more permissive than reality                                             |
| `Microsoft.Web/certificates/read`                       | App Service certificates                                                                                                  |
| `Microsoft.Network/applicationGateways/read`            | Application Gateway certificates (SSL, trusted root, trusted client, authentication)                                      |
| Graph `Directory.Read.All`                              | Identity display names, types, and enabled/disabled status (otherwise identities appear as bare GUIDs)                    |
| Graph `GroupMember.Read.All`                            | Group membership expansion — required for group-based access paths in the Security Graph (admin consent required)         |
| Graph `AuditLog.Read.All`                               | Last sign-in dates for users and service principals — powers stale/never-used identity detection (admin consent required) |

***

## Scope Note

Granting roles at a lower scope (resource group / vault, instead of subscription) narrows visibility the same way as with the other cloud scanners — anything out of scope is simply reported as a gap in the Access Status.
