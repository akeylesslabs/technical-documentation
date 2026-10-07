---
title: GitHub Scanner
deprecated: false
hidden: false
metadata:
  robots: index
---
The GitHub Scanner is a native scanner type that inspects a connected GitHub organization or enterprise, discovering the full inventory of identities such as organization members, teams, and GitHub Apps, along with the secrets it contains across the organization's repositories, including support for GitHub secret scanning across source code and Git history, as well as the relationships between them. Each discovered object is evaluated against Identity & Secrets Intelligence security policies, which assess its risk posture and surface the resulting findings for review.

## What the GitHub Scanner Discovers

Each scanner covers one or more object types, selected when the scanner is created:

| Object Type    | What is discovered                                                                                                                                                                                                      |
| -------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Secrets**    | Actions, Dependabot, and Codespaces secrets at the organization and repository level, environment secrets, and deploy keys                                                                                              |
| **Identities** | Organization members, outside collaborators, teams, organization roles, repository collaborators, installed GitHub Apps, fine-grained personal access tokens, OAuth Apps, and Actions workflows, with their permissions |
| **Code**       | Credentials hardcoded in repository source code and Git history, with their validation status and the member who committed them                                                                                         |

Each scanner covers the GitHub organization its GitHub App is installed in, and only the repositories the App installation can access. To scan only some of those repositories, filter them when you create the scanner, as described in [Create a GitHub Scanner](#create-a-github-scanner). The App must be installed only on that organization, otherwise the scan fails. To scan more organizations, create a GitHub App, a Target, and a scanner for each organization.

## Prerequisites

- An Akeyless account with the Identity & Secrets Intelligence license.
- A deployed and connected [Akeyless Gateway](doc:gateway-overview) version `5.1.0` and later.Scanning the **Code** object type requires version `5.3.0` and later.
- A Gateway with [Akeyless AI Insights](doc:akeyless-ai-insight) configured.
- A [GitHub Target](https://docs.akeyless.io/docs/github-targets) representing the GitHub App that will scan the organization.
- The GitHub App used by the Target granted the permissions listed under [Required GitHub Permissions](#required-github-permissions) below.
- Access to configure and run the scanner, granted via:
  - `Manage ISI Scanners` or `Admin` [Gateway Permission](https://docs.akeyless.io/docs/gateway-access-permissions-reference).
  - `Identity & Secrets Intelligence` [Administrative Rule](https://docs.akeyless.io/docs/rbac#administrative-rules) set to `Scoped` or `All`.
  - `List` permission on the GitHub Target.

## Required GitHub Permissions

The GitHub scanner authenticates with one of the credential types below. in GitHub missing access surfaces as warnings on the scan.

All permissions below are **read-only**. The scanner never requires write access to your GitHub organization, and never reads secret _values_, only metadata.

### Authentication & Scopes

| Credential                                      | Scope / Permission                                              | Enables                                                                       |
| ----------------------------------------------- | --------------------------------------------------------------- | ----------------------------------------------------------------------------- |
| Personal Access Token (classic or fine-grained) | Read access to the organizations/repositories in scope          | Standard organization and repository scanning                                 |
| GitHub App                                      | `organization_personal_access_tokens` permission                | PAT - grant scanning                                                          |
| Classic PAT with `admin:enterprise`             | Enterprise scope (GitHub Apps cannot call enterprise endpoints) | Enterprise-level scanning; audit-log-based features require GitHub Enterprise |

Audit-log-based features are only available with GitHub Enterprise.

## Create a GitHub Scanner

1. Log in to the Akeyless Console, and go to **Products > Identity & Secrets Intelligence > Scanners**.
2. Click **New**, and select the scanner type **GitHub**, then click **Next**.
3. Define a **Name** for the scanner.
4. Select the **Gateway** that will execute the scans, and the **Target** representing the organization or enterprise to scan, then click **Next**.
5. Use the **Object Type** drop-down list to select the scanner's scope, and click **Finish**.

## Run a Scan

1. Log in to the Akeyless Console, and go to **Products > Identity & Secrets Intelligence > Scanners**.
2. Click the GitHub scanner.
3. Click **Start Scan**.

Once the scan completes, results appear in **Inventory** for review.<br />

## Required GitHub Permissions

The GitHub App used by the Target needs read access to the GitHub resources behind each object type selected on the scanner. Every table in this section has an **Object Type** column, so you can grant only what the selected object types need. Personal access tokens are not supported.

### Quick Setup

For each object type selected on the scanner, grant the GitHub App the permissions listed below:

| Object Type    | Repository permissions                                                                             | Organization permissions                                                                                |
| -------------- | -------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------- |
| **Secrets**    | `Secrets`, `Dependabot secrets`, `Codespaces secrets`, `Actions`, `Environments`, `Administration` | `Secrets`, `Organization dependabot secrets`, `Organization codespaces secrets`, `Custom properties`    |
| **Identities** | `Actions`, `Contents`                                                                              | `Members`, `Administration`, `Custom organization roles`, `Personal access tokens`, `Custom properties` |
| **Code**       | `Contents`, `Administration`                                                                       | `Members`, `Custom properties`                                                                          |

<Callout icon="⚠️" theme="warning">
  ### Warning

  GitHub requires **Read and write** access on the repository **Codespaces secrets** permission to list those secrets. Grant it only if you need repository Codespaces secrets scanned. Every other permission requires **Read-only** access.
</Callout>

### Granular Permissions

All permissions below are **read-only**, except **Codespaces secrets**. The scanner never changes your GitHub organization, and never reads the _values_ of Actions, Dependabot, or Codespaces secrets, only their metadata.

#### Required Permissions

The permissions listed below are required for each object type to return results. If one is missing, the scan still completes, and the gap is reported as a warning in the scan details:

| Object Type    | Used for                                  | Permission                                     | If missing                             |
| -------------- | ----------------------------------------- | ---------------------------------------------- | -------------------------------------- |
| **Secrets**    | Actions secrets                           | Organization: `Secrets`; Repository: `Secrets` | Skipped and reported as a scan warning |
| **Identities** | Members, outside collaborators, and teams | Organization: `Members`                        | Skipped and reported as a scan warning |
| **Code**       | Cloning repositories                      | Repository: `Contents`                         | Skipped and reported as a scan warning |

A missing permission never fails the scan. Any other failure in a selected object type, or invalid GitHub App credentials, marks the whole scan as failed.

#### Additional Permissions for Complete Coverage

These permissions are optional. If missing, the scan still completes, but with reduced visibility, and the policies that depend on them are not evaluated.

| Object Type                                   | Permission                                                                        | What it adds                                                                      |
| --------------------------------------------- | --------------------------------------------------------------------------------- | --------------------------------------------------------------------------------- |
| **Secrets**                                   | Organization: `Organization dependabot secrets`; Repository: `Dependabot secrets` | Dependabot secrets                                                                |
| **Secrets**                                   | Organization: `Organization codespaces secrets`; Repository: `Codespaces secrets` | Codespaces secrets                                                                |
| **Secrets**                                   | Repository: `Actions`, `Environments`                                             | Environment secrets                                                               |
| **Secrets**<br />**Code**                     | Repository: `Administration`                                                      | Deploy keys, and whether a private key found in code is one of them               |
| **Identities**                                | Organization: `Administration`                                                    | Installed GitHub Apps, and OAuth Apps from the audit log (GitHub Enterprise only) |
| **Identities**                                | Organization: `Custom organization roles`                                         | Organization roles                                                                |
| **Identities**                                | Organization: `Personal access tokens`                                            | Fine-grained personal access tokens                                               |
| **Identities**                                | Repository: `Actions`, `Contents`                                                 | Actions workflows                                                                 |
| **Code**                                      | Organization: `Members`                                                           | The member who committed each credential                                          |
| **Secrets**<br />**Identities**<br />**Code** | Organization: `Custom properties`                                                 | Filtering repositories by **Custom Properties**                                   |

Each gap is reported as a warning in the scan details.

## Create a GitHub Scanner

1. Log in to the Akeyless Console, and go to **Products > Identity & Secrets Intelligence > Scanners**.
2. Click **New**, and select the scanner type **GitHub**, then click **Next**.
3. Define a **Name** for the scanner.
4. Select the **Gateway** that will execute the scans, and the **Target** representing the GitHub App installed on the organization to scan, then click **Next**.
5. Use the **Object Type** drop-down list to select the object types to scan.
6. Optionally, to filter the repositories to scan, set the **Scanner Scope** to **Repository**, and select a filter in **Select Repositories By**: **Name**, **Topic**, **Custom Properties**, **Regex**, or **None** . Click **Finish**.

## Run a Scan

1. Log in to the Akeyless Console, and go to **Products > Identity & Secrets Intelligence > Scanners**.
2. Click the GitHub scanner.
3. Click **Start Scan**.

Once the scan completes, results appear in **Inventory** for review.
