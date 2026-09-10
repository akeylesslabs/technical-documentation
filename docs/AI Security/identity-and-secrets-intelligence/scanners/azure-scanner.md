---
title: Azure Scanner
deprecated: false
hidden: false
metadata:
  robots: index
---
The Azure Scanner is a native scanner type that inspects a connected Azure subscription, discovering the full inventory of identities such as Microsoft Entra ID users, groups, and service principals, secrets stored in Azure Key Vault, and certificates managed through Azure Key Vault, App Service, and Application Gateway, along with the relationships between them. <br />Each discovered object is evaluated against Identity & Secrets Intelligence security policies, which assess its risk posture and surface the resulting findings for review.

## Prerequisites

- An Akeyless account with the Identity & Secrets Intelligence license.
- A deployed and connected [Akeyless Gateway](doc:gateway-overview) version `5.0.1` and later.
- A Gateway with [Akeyless AI Insights](doc:akeyless-ai-insight) configured.
- An [Azure Target](https://docs.akeyless.io/docs/azure-targets) representing the Azure AD application that will scan the subscription.
- The Azure AD application used by the Target granted the permissions listed under [Required Azure Permissions](#required-azure-permissions) below.
- Access to configure and run the scanner, granted via:
  1. "Manage ISI Scanners" or "Admin" [Gateway Permission](https://docs.akeyless.io/docs/gateway-access-permissions-reference).
  2. "Identity & Secrets Intelligence" [Administrative Rule](https://docs.akeyless.io/docs/rbac#administrative-rules) set to Scoped or All.
  3. "List" permission on the Azure Target.

## Required Azure Permissions

The Azure AD application used by the Target needs read access to your Azure subscription and tenant. There are two ways to grant it:

- **Quick Setup** - assign built-in Azure roles plus a small set of Microsoft Graph application permissions. Fastest to configure, but grants more access than the scanner actually uses.
- **Granular Permissions** - assign only the exact actions the scanner needs, following the principle of least privilege.

Both produce a complete scan, the difference is privilege scope, not scan coverage.

### Quick Setup

Assign the built-in **Reader** and **Key Vault Reader** roles at the subscription scope, and grant the application these Microsoft Graph application permissions:

- `Application.Read.All`
- `Directory.Read.All`
- `GroupMember.Read.All`
- `AuditLog.Read.All`<br />

`GroupMember.Read.All` and `AuditLog.Read.All` require tenant admin consent.

<Callout icon="ℹ️" theme="info">
  ### Note

  For vaults using access policies instead of Azure RBAC, also add a per-vault access policy granting **Secret List** and **Certificate List** permissions, role assignments alone do not grant data-plane access on these vaults.
</Callout>

### Granular Permissions

All permissions below are **read-only**. The scanner never requires write access to your Azure environment, and never reads secret _values_, only metadata.

#### Required Permissions

The permissions listed below are required for the scan to complete successfully. If any one of them is missing, the corresponding scan will fail.

| Permission                                     | Used for                                                              | If missing                                                                    |
| ---------------------------------------------- | --------------------------------------------------------------------- | ----------------------------------------------------------------------------- |
| `Microsoft.KeyVault/vaults/read`               | Discovering Key Vaults (the source for both secrets and certificates) | Secrets/certificates scan fails                                               |
| `Microsoft.Authorization/roleAssignments/read` | Identity discovery and access mapping                                 | Identities scan fails                                                         |
| Graph `Application.Read.All`                   | Entra ID application client secrets and certificates                  | Scan fails when the subscription has service principals with role assignments |

the scan currently completes successfully but with **no secrets or certificates.**

#### Additional Permissions for Complete Coverage

These permissions are optional. If missing, the scan still completes, but with reduced visibility, and any gaps are reported in the Access Status field within the scan details.

| Permission                                              | What it adds                                                                                                             |
| ------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------ |
| `Microsoft.KeyVault/vaults/secrets/readMetadata/action` | Listing secrets inside each vault                                                                                        |
| `Microsoft.KeyVault/vaults/certificates/read`           | Listing certificates inside each vault                                                                                   |
| `Microsoft.Authorization/roleDefinitions/read`          | Resolving role names and permissions, without it, access edges in the Security Graph cannot be computed                  |
| `Microsoft.Authorization/denyAssignments/read`          | Deny assignments, without it the graph may look more permissive than reality                                             |
| `Microsoft.Web/certificates/read`                       | App Service certificates                                                                                                 |
| `Microsoft.Network/applicationGateways/read`            | Application Gateway certificates (SSL, trusted root, trusted client, authentication)                                     |
| Graph `Directory.Read.All`                              | Identity display names, types, and enabled/disabled status (otherwise identities appear as bare GUIDs)                   |
| Graph `GroupMember.Read.All`                            | Group membership expansion, required for group-based access paths in the Security Graph (admin consent required)         |
| Graph `AuditLog.Read.All`                               | Last sign-in dates for users and service principals, powers stale/never-used identity detection (admin consent required) |

## Create an Azure Scanner

1. Log in to the Akeyless Console, and go to **Products > Identity & Secrets Intelligence > Scanners**.
2. Click **New**, and select the scanner type **Azure**, then click **Next**.
3. Define a **Name** for the scanner.
4. Select the **Target** representing the Azure subscription to scan, and the **Gateway** that will execute the scans, then click **Next**.
5. Use the **Object Type** drop-down list to select the scanner's scope, and click **Finish**.

## Run a Scan

1. Log in to the Akeyless Console, and go to **Products > Identity & Secrets Intelligence > Scanners**.
2. Click the Azure scanner.
3. Click **Start Scan**.

Once the scan completes, results appear in [Inventory](doc:identity-and-secrets-intelligence#inventory) for review.

<br />
