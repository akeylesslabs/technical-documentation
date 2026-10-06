---
title: GitLab Scanner
deprecated: false
hidden: false
metadata:
  robots: index
---
The GitLab Scanner is a native scanner type that inspects a connected GitLab group on GitLab.com or a self-managed GitLab instance, discovering credentials hardcoded in the source code and Git history of its projects, along with the users who committed them and the cloud identities they belong to. Each discovered object is evaluated against Identity & Secrets Intelligence security policies, which assess its risk posture and surface the resulting findings for review.

## What the GitLab Scanner Discovers

The GitLab Scanner is a code scanner. It finds credentials committed to your GitLab projects, and shows where each one was committed, who committed it, and whether it still works:

* **Hardcoded credentials in source and history**: The full commit history of every project in scope. This includes merge-request refs, which hold commits pushed to a merge request whose source branch was later deleted, and keep-around refs, which hold commits GitLab retains after a force-push or branch deletion.
* **Validation status**: Whether each credential still authenticates, has been revoked or rotated, or could not be validated. For a credential that still works, the scanner also analyzes its reach, for example whether it can access a credential store, create new credentials, or call control-plane APIs.
* **Authorship**: The GitLab user who committed each credential, matched against the members of the scanned group.
* **Cloud identity correlation**: A validated AWS, GCP, or Azure credential is linked in the Security Graph to the same identity discovered by the matching [AWS](https://docs.akeyless.io/docs/aws-scanner), [GCP](https://docs.akeyless.io/docs/gcp-scanner), or [Azure](https://docs.akeyless.io/docs/azure-scanner) Scanner.

A scanner with a **GitLab Group** set covers that group and, by default, its subgroups. A scanner with no group set covers every group the token's user is a member of. Archived projects are scanned in both cases. To scan only some of the projects, filter them when you create the scanner, as described in [Create a GitLab Scanner in the Akeyless Console](#create-a-gitlab-scanner-in-the-akeyless-console). To cover more groups, add the token's user to each of them and leave the group blank, or create a scanner for each group.

<Callout icon="ℹ️" theme="info">
  ### **Note:**

  If you also scan that cloud account with the [AWS](https://docs.akeyless.io/docs/aws-scanner), [GCP](https://docs.akeyless.io/docs/gcp-scanner), or [Azure](https://docs.akeyless.io/docs/azure-scanner) Scanner, both scanners link to the same identity. The GitLab finding then shows what the leaked credential grants: the identity's permissions and the resources it can access, as discovered by that scanner. Without the cloud scanner, the identity is shown by name only.
</Callout>

## Prerequisites

* An Akeyless account with the Identity & Secrets Intelligence license.
* A deployed and connected [Akeyless Gateway](https://docs.akeyless.io/docs/gateway-overview) version `5.5.0` and later.
* A Gateway with [Akeyless AI Insights](https://docs.akeyless.io/docs/akeyless-ai-insight) configured.
* Outbound HTTPS access from the Gateway to your GitLab instance.
* A [GitLab Target](https://docs.akeyless.io/docs/gitlab-target) representing the GitLab user that will scan the group.&#x20;
* The access token used by the Target granted the scopes listed under [Required GitLab Permissions](#required-gitlab-permissions) below.
* Access to configure and run the scanner, granted via:
  1. `Manage ISI Scanners `or `Admin` [Gateway Permission](https://docs.akeyless.io/docs/gateway-access-permissions-reference).
  2. `Identity & Secrets Intelligence` [Administrative Rule](https://docs.akeyless.io/docs/rbac#administrative-rules) set to `Scoped` or `All`.
  3. `List` permission on the GitLab Target.

## Required GitLab Permissions

The access token used by the Target needs read access to the GitLab resources behind each object type selected on the scanner. Every table in this section has an **Object Type** column, so you can grant only what the selected object types need. Both a [personal access token](https://docs.gitlab.com/user/profile/personal_access_tokens/) and a [group access token](https://docs.gitlab.com/user/group/settings/group_access_tokens/) are supported.

The permissions listed below are required for the scan to complete successfully. If one is missing on the scanner, the scan fails, in the cases described below:

| Object Type | Used for                                                 | Permission        | If missing                                              |
| ----------- | -------------------------------------------------------- | ----------------- | ------------------------------------------------------- |
| **Code**    | Listing groups, projects, and group members              | `read_api`        | The scan fails                                          |
| **Code**    | Cloning each project to scan its source code and history | `read_repository` | Every project is skipped and reported as a scan warning |

Use a personal access token, or a group access token with the **Reporter** role or higher.

### Scan Warnings

Some access gaps do not fail the scan. The scan completes and reports each gap as a warning, visible in the scan details:

| Situation                                              | Result                                                                                             |
| ------------------------------------------------------ | -------------------------------------------------------------------------------------------------- |
| The token cannot list the members of a group           | All credentials are still found, but some or all are not attributed to the user who committed them |
| A project cannot be cloned                             | The project is skipped, and a warning names it                                                     |
| A project is larger than 250 MB, as reported by GitLab | The project is skipped, and a warning names it                                                     |

## Self-Managed GitLab Instances

The GitLab Scanner scans GitLab.com by default. To scan a self-managed instance, set the GitLab Target's **URL** to that instance, for example `https://gitlab.example.com`. Instances served under a path, for example `https://example.com/gitlab`, are supported.

The following restrictions apply to self-managed instances:

* The URL must use HTTPS. Plain HTTP is accepted only for a loopback address, such as a local test instance, because the access token would otherwise cross the network unencrypted.
* A private certificate authority is not supported. A scanner that uses a GitLab Target with a **TLS Certificate** configured fails with an error. Use a separate GitLab Target, without a certificate, for scanning.

## Create a GitLab Scanner in the Akeyless Console<br />(this needs to be validated with the new version)

GitLab scanners are created and run from the Akeyless Console. The GitLab Target can be created from the Console or the CLI, as described in [GitLab Target](https://docs.akeyless.io/docs/gitlab-target).

1. Log in to the Akeyless Console, and go to **Products > Identity & Secrets Intelligence > Scanners**.
2. Click **New**, and select the scanner type **GitLab**, then click **Next**.
3. Define a **Name** for the scanner.
4. Select the **Gateway** that will execute the scans, and the **Target** representing the GitLab instance and access token to use.
5. Optionally, enter a **GitLab Group** path, for example `acme/platform`, to limit the scan to that group and its subgroups. Leave it blank to scan every group the token is a member of. Click **Next**.
6. The **Object Type** is set to **Code**, the only object type the GitLab Scanner supports. Click **Finish**.

## Run a Scan

1. Log in to the Akeyless Console, and go to **Products > Identity & Secrets Intelligence > Scanners**.
2. Click the GitLab scanner.
3. Click **Start Scan**.

Once the scan completes, results appear in **Findings** for review. Scan warnings, such as skipped projects, appear in the scan details.

## GitLab Findings and Policies

GitLab findings are evaluated against the following Identity & Secrets Intelligence policies for credentials committed to code:

- Live Secret Committed to Code
- Critical Blast-Radius Code Secret
- Live Secret with Contained Reach
- Revoked Secret Found in Git History
- Unvalidated Secret Pattern in Code

For more information, see [Secret Policies](doc:secret-policies)​.

Secret lifecycle policies such as Unused Secret, Stale Secret, and Rotation Overdue do not apply to GitLab findings, because they describe secrets held in a managed secret store rather than values committed to code.

<Callout icon="✅" theme="success">
  ### **Tip:**

  Deleting a branch or force-pushing does not remove a credential from GitLab, because keep-around and merge-request refs keep the commit reachable. After you rotate a leaked credential, purge it from the project's history and run GitLab housekeeping so those refs are expired.
</Callout>
