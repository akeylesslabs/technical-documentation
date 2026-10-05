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

| Object Type    | What is discovered                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| -------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Secrets**    | Actions, Dependabot, and Codespaces secrets at the organization and repository level, environment secrets, and deploy keys, with the repositories each secret is available to, when it was last updated, and the identities that can manage it                                                                                                                                                                                                                                                                                                                                 |
| **Identities** | Organization members, with their organization role, two-factor authentication status, and SSO link, as well as outside collaborators, teams, organization roles, direct repository collaborators, GitHub Apps installed on the organization with their permissions and repository access, fine-grained personal access tokens approved for the organization with their expiration and last use, OAuth Apps (GitHub Enterprise Cloud only), members' public SSH keys, and Actions workflows as identities that use secrets, with their token permissions, triggers, and runners |
| **Code**       | Credentials hardcoded in repository source code and full Git history, with whether each one still works, who committed it, and, for AWS, GCP, and Azure credentials, the cloud identity it belongs to                                                                                                                                                                                                                                                                                                                                                                          |

The scanner never reads the values of Actions, Dependabot, or Codespaces secrets, because the GitHub API never returns them. Only their metadata is collected.

Select **Code** only when you need it. It clones every repository in scope, including its full Git history, which uses significant Gateway disk space and CPU. Repositories larger than 250 MB, as reported by GitHub, are skipped, and each one is reported as a scan warning. A discovered credential's value is never stored.

Each GitHub scanner covers one organization: the organization the Target's GitHub App is installed in. The App must be installed on exactly one account. If it is installed on more than one, the scan fails, because the scanner cannot tell which organization to scan. To scan several organizations, create a GitHub App, a GitHub Target, and a scanner for each one.

Within the organization, the App installation's **Repository access** setting decides which repositories are scanned: **All repositories** or **Only select repositories**. Organization-level objects, such as organization secrets, members, teams, organization roles, installed GitHub Apps, fine-grained personal access tokens, and OAuth Apps, are scanned regardless of repository access.

## Prerequisites

- An Akeyless account with the Identity & Secrets Intelligence license.
- A deployed and connected [Akeyless Gateway](doc:gateway-overview) version `5.1.0` and later.
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

Once the scan completes, results appear in **Inventory** for review.

<br />

<br />

<br />

Each GitHub scanner covers one organization: the organization the Target's GitHub App is installed in. The App must be installed on exactly one account. If it is installed on more than one, the scan fails, because the scanner cannot tell which organization to scan. To scan several organizations, create a GitHub App, a GitHub Target, and a scanner for each one.

Within the organization, the App installation's **Repository access** setting decides which repositories are scanned: **All repositories** or **Only select repositories**. Organization-level objects, such as organization secrets, members, teams, organization roles, installed GitHub Apps, fine-grained personal access tokens, and OAuth Apps, are scanned regardless of repository access.

### Filter the Scanner Scope

Filtering the scanner scope requires Gateway version `[TBD]` and later.

To scan only some of the organization's repositories, set the **Scanner Scope** in the scanner's **Advanced Options** when you create it. The scope applies to every object type selected on the scanner. Organization-level objects, such as organization secrets, members, and teams, are scanned whichever scope is selected.

* **Organization** (default): Scans every repository the GitHub App can access.
* **Repository**: Scans only the repositories that match the filter selected in **Select Repositories By**.

| Select Repositories By | Scans the repositories that                                                                         |
| ---------------------- | --------------------------------------------------------------------------------------------------- |
| **None**               | You select by hand in **Selected Repositories**                                                     |
| **Name**               | Contain the entered text in their name, ignoring case                                               |
| **Topic**              | Have any of the entered topics, up to 50                                                            |
| **Custom Properties**  | Have any of the entered values, up to 50, for one custom property                                   |
| **Regex**              | Match the regular expression, up to 512 characters, against the full `organization/repository` name |

Each scanner takes one filter, so filters cannot be combined, for example a topic and a name. There is no option to exclude repositories, and the regular expression syntax does not support negative lookahead, so a pattern cannot exclude them either.

**Selected Repositories** controls whether the list of scanned repositories follows the filter:

* **Left empty**: The filter is applied again on every scan, so new repositories that match it are scanned automatically.
* **Repositories selected**: Only the selected repositories are scanned, up to 1,000. A selected repository is still scanned after it is renamed.

While you set the filter, the console shows how many of the organization's repositories match it, and a preview of the matching repositories.

To also scan the public personal repositories of every organization member, select **Scan organization members’ public repositories**. These repositories are added to the **Code** object type only.

The following rules apply to the scanner scope:

* Forks are not scanned, whichever **Scanner Scope** is selected.
* Repositories that match the filter but are not included in the App installation are skipped, with a notice in the scan details.
* The scan fails if the filter matches no repositories, or if a **Topic** or **Custom Properties** filter matches more than 1,000 repositories, the most that GitHub search returns.
* The scope cannot be changed after the scanner is created. To scan a different set of repositories, create a new scanner.

## Prerequisites

- An Akeyless account with the Identity & Secrets Intelligence license.
- A deployed and connected [Akeyless Gateway](doc:gateway-overview) version `5.1.0` and later. Scanning the **Code** object type requires version `5.3.0` and later.
- A Gateway with [Akeyless AI Insights](doc:akeyless-ai-insight) configured.
- A [GitHub Target](https://docs.akeyless.io/docs/github-targets) representing the GitHub App that will scan the organization or enterprise.
- The GitHub App used by the Target granted the scope listed under [Required GitHub Permissions](#required-github-permissions) below.
- Access to configure and run the scanner, granted via:
  - `Manage ISI Scanners `or `Admin` [Gateway Permission](https://docs.akeyless.io/docs/gateway-access-permissions-reference).
  - `Identity & Secrets Intelligence` [Administrative Rule](https://docs.akeyless.io/docs/rbac#administrative-rules) set to `Scoped` or `All`.
  - `List` permission on the GitLab Target.

## Required GitHub Permissions

The scanner authenticates as the GitHub App stored in the GitHub Target, using a short-lived installation token for the organization the App is installed in. Personal access tokens are not supported, and neither is scanning a whole GitHub enterprise. To cover several organizations, see [What the GitHub Scanner Discovers](#what-the-github-scanner-discovers).

The GitHub App needs read access to the GitHub resources behind each object type selected on the scanner. Every table in this section has an **Object Type** column, so you can grant only what the selected object types need. Set the permissions in the GitHub App's settings, under **Permissions & events**. When you change them, an owner of the organization must approve the new permissions on the App's installation before they take effect.

All permissions below are **Read-only**, except **Codespaces secrets**, which GitHub requires at **Read and write** level even to list secret names. The scanner never changes anything in your GitHub organization. It reads repository content only for the **Code** object type, to find credentials committed to it.

### Quick Setup

For each object type selected on the scanner, grant the GitHub App the permissions listed below. Each permission is **Read-only** unless marked otherwise:

| Object Type    | Repository permissions                                                                                                          | Organization permissions                                                           |
| -------------- | ------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------- |
| **Secrets**    | `Metadata`, `Secrets`, `Dependabot secrets`, `Codespaces secrets` (Read and write), `Actions`, `Environments`, `Administration` | `Secrets`, `Organization dependabot secrets`, `Organization codespaces secrets`    |
| **Identities** | `Metadata`, `Actions`, `Contents`                                                                                               | `Members`, `Administration`, `Custom organization roles`, `Personal access tokens` |
| **Code**       | `Metadata`, `Contents`                                                                                                          | `Members`                                                                          |

<Callout icon="⚠️" theme="warning">
  ### Warning

  Grant **Read and write** on **Codespaces secrets** only if you need repository Codespaces secrets in the scan. GitHub requires write access to list them, and that access also lets the App create, change, and delete them. Without it, repository Codespaces secrets are skipped and reported as a scan warning, and the rest of the scan is unaffected. Do not grant write access to any other permission, as the scanner never uses it.
</Callout>

### Granular Permissions

The tables below explain what each permission is used for, and what the scan loses without it.

A missing GitHub App permission never fails the scan. The scan completes, skips the objects that permission covers, and lists each skipped request as a warning in the scan details.

#### Required Permissions

The permissions listed below provide the core results of each object type. If one is missing, the scan still completes, but that object type returns little or nothing:
