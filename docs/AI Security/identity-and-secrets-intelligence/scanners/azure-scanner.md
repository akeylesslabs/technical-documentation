---
title: Azure Scanner
deprecated: false
hidden: false
metadata:
  robots: index
---
The Azure Scanner is a native scanner type that inspects a connected Azure subscription, discovering the full inventory of identities such as Microsoft Entra ID users, groups, and service principals, secrets stored in Azure Key Vault, and certificates managed through Azure Key Vault, App Service, and Application Gateway, along with the relationships between them. <br />Each discovered object is evaluated against Identity & Secrets Intelligence security policies, which assess its risk posture and surface the resulting findings for review.

## What the Azure Scanner Discovers

Each scanner covers one or more object types, selected when the scanner is created:

| Object Type      | What is discovered                                                                                                                                                                                                                 |
| ---------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Secrets**      | Secrets stored in Azure Key Vault, with their creation, update, and expiration dates and enabled status, and Microsoft Entra ID app registration client secrets, with their expiration date, owner, and last sign-in               |
| **Certificates** | Certificates managed through Azure Key Vault, App Service, and Application Gateway (SSL, trusted root, trusted client, and authentication certificates), and Microsoft Entra ID app registration client certificates               |
| **Identities**   | Microsoft Entra ID users, groups, service principals, and managed identities, with their role assignments and the scope of each, deny assignments, group memberships, credentials, sign-in activity, and Key Vault access policies |

Each scanner covers one Azure subscription, the one set on the Azure Target. Key Vaults, App Service certificates, and Application Gateways are discovered across the whole subscription, in every region. Identities are discovered from the subscription's role assignments, so the scanner finds identities that hold a role assignment in the subscription, and the members of groups that do. Likewise, Microsoft Entra ID client secrets and certificates are discovered only for service principals that hold a role assignment in the subscription. To cover several subscriptions, create an Azure Target and a scanner for each subscription.

## Prerequisites

- An Akeyless account with the Identity & Secrets Intelligence license.
- A deployed and connected [Akeyless Gateway](doc:gateway-overview) version `5.0.1` and later.
- A Gateway with [Akeyless AI Insights](doc:akeyless-ai-insight) configured.
- An [Azure Target](https://docs.akeyless.io/docs/azure-targets) representing the Azure AD application that will scan the subscription.
- The Azure AD application used by the Target granted the permissions listed under [Required Azure Permissions](#required-azure-permissions) below.
- Access to configure and run the scanner, granted via:
  - `Manage ISI Scanners `or `Admin` [Gateway Permission](https://docs.akeyless.io/docs/gateway-access-permissions-reference).
  - `Identity & Secrets Intelligence` [Administrative Rule](https://docs.akeyless.io/docs/rbac#administrative-rules) set to `Scoped` or `All`.
  - `List` permission on the Azure Target.

## Required Azure Permissions

The Azure AD application used by the Target needs read access to the Azure subscription and the Microsoft Entra ID tenant.

There are two ways to grant it:

- **Quick Setup** - assign built-in Azure roles plus a small set of Microsoft Graph application permissions. Fastest to configure, but grants more access than the scanner actually uses.
- **Granular Permissions** - assign only the exact actions the scanner needs, following the principle of least privilege.

Both produce a complete scan, the difference is privilege scope, not scan coverage.

### Quick Setup

For each object type selected on the scanner, assign the built-in Azure roles at the subscription scope, and grant the application the Microsoft Graph application permissions listed below:

| Object Type      | Built-in Azure roles         | Microsoft Graph application permissions                                                   |
| ---------------- | ---------------------------- | ----------------------------------------------------------------------------------------- |
| **Secrets**      | `Reader`, `Key Vault Reader` | `Application.Read.All`, `AuditLog.Read.All`                                               |
| **Certificates** | `Reader`, `Key Vault Reader` | `Application.Read.All`                                                                    |
| **Identities**   | `Reader`                     | `Application.Read.All`, `Directory.Read.All`, `GroupMember.Read.All`, `AuditLog.Read.All` |

All Microsoft Graph application permissions require tenant admin consent.

<Callout icon="ℹ️" theme="info">
  ### Note

  For vaults using access policies instead of Azure RBAC, also add a per-vault access policy granting **Secret List** and **Certificate List** permissions, role assignments alone do not grant data-plane access on these vaults.
</Callout>

### Granular Permissions

Every table in this section has an **Object Type** column, so you can grant only what the selected object types need.

All permissions below are **read-only**. The scanner never requires write access to your Azure environment, and never reads secret _values_, only metadata.

#### Required Permissions

The permissions listed below are required for the scan to complete successfully. If one is missing for an object type selected on the scanner, the scan fails, in the cases described below:

| Object Type                                           | Used for                                                                                                                             | Permission                                     | If missing     |
| ----------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------ | ---------------------------------------------- | -------------- |
| **Secrets**<br />**Certificates**<br />**Identities** | Key Vault discovery, and reading the access policies of each vault                                                                   | `Microsoft.KeyVault/vaults/read`               | The scan fails |
| **Secrets**<br />**Certificates**<br />**Identities** | Identity discovery and access mapping, and finding the service principals whose Entra ID client secrets and certificates are scanned | `Microsoft.Authorization/roleAssignments/read` | The scan fails |
| **Secrets**<br />**Certificates**                     | Entra ID application client secrets and certificates                                                                                 | Graph `Application.Read.All`                   | The scan fails |

A failure in any selected object type marks the whole scan as failed.

For **Identities**, if the vaults can be listed but some of them can't be read, the access policies of those vaults are skipped and reported as a gap.

#### Additional Permissions for Complete Coverage

These permissions are optional. If missing, the scan still completes, but with reduced visibility.

| Object Type      | Permission                                              | What it adds                                                                                                                                                                                                |
| ---------------- | ------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Secrets**      | `Microsoft.KeyVault/vaults/secrets/readMetadata/action` | Listing the secrets inside each vault. If missing, no gap is reported, and the scan completes with no Key Vault secrets                                                                                     |
| **Secrets**      | Graph `AuditLog.Read.All`                               | The last sign-in date of each service principal that holds an Entra ID client secret. If missing, no gap is reported                                                                                        |
| **Certificates** | `Microsoft.KeyVault/vaults/certificates/read`           | Listing the certificates inside each vault, and their details. If missing, no gap is reported, and the scan completes with no Key Vault certificates                                                        |
| **Certificates** | `Microsoft.Web/certificates/read`                       | App Service certificates                                                                                                                                                                                    |
| **Certificates** | `Microsoft.Network/applicationGateways/read`            | Application Gateway certificates (SSL, trusted root, trusted client, authentication)                                                                                                                        |
| **Identities**   | `Microsoft.Authorization/roleDefinitions/read`          | Resolving role names and permissions, without it, access edges in the Security Graph cannot be computed                                                                                                     |
| **Identities**   | `Microsoft.Authorization/denyAssignments/read`          | Deny assignments, without it the graph may look more permissive than reality                                                                                                                                |
| **Identities**   | Graph `Application.Read.All`                            | The client secrets and certificates held by each service principal                                                                                                                                          |
| **Identities**   | Graph `Directory.Read.All`                              | Identity display names, types, and enabled/disabled status (otherwise identities appear as bare GUIDs)                                                                                                      |
| **Identities**   | Graph `GroupMember.Read.All`                            | Group membership expansion, required for group-based access paths in the Security Graph. If missing and an IdP Target is set on the scanner, group members are read from it instead, and no gap is reported |
| **Identities**   | Graph `AuditLog.Read.All`                               | Last sign-in dates for users and service principals, powers stale/never-used identity detection                                                                                                             |

Each gap entry names the skipped resource, the missing permission, and the built-in Azure role or Microsoft Graph permission that grants it.

## Create an Azure Scanner

1. Log in to the Akeyless Console, and go to **Products > Identity & Secrets Intelligence > Scanners**.
2. Click **New**, and select the scanner type **Azure**, then click **Next**.
3. Define a **Name** for the scanner.
4. Select the **Gateway** that will execute the scans, and the **Target** representing the Azure subscription to scan, then click **Next**.
5. Use the **Object Type** drop-down list to select the scanner's scope, and click **Finish**.

## Run a Scan

1. Log in to the Akeyless Console, and go to **Products > Identity & Secrets Intelligence > Scanners**.
2. Click the Azure scanner.
3. Click **Start Scan**.
