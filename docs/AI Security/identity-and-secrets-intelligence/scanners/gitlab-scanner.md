---
title: GitLab Scanner
deprecated: false
hidden: false
metadata:
  robots: index
---
# GitLab Scanner

The GitLab Scanner is a native scanner type that inspects a connected GitLab group on GitLab.com or a self-managed GitLab instance. It clones each project in the group and its subgroups, then scans the source code and the full Git history for hardcoded credentials. Each discovered credential is validated with a read-only check to determine whether it still works, then evaluated against Identity & Secrets Intelligence security policies, which assess its risk posture and surface the resulting findings for review.

## What the GitLab Scanner Discovers

The GitLab Scanner is a code scanner. It finds credentials committed to your GitLab projects, and shows where each one was committed, who committed it, and whether it still works:

* **Hardcoded credentials in source and history**: The full commit history of every project in scope. This includes merge-request refs, which hold commits pushed to a merge request whose source branch was later deleted, and keep-around refs, which hold commits GitLab retains after a force-push or branch deletion.
* **Validation status**: Whether each credential still authenticates, has been revoked or rotated, or could not be validated. For a credential that still works, the scanner also analyzes its reach, for example whether it can access a credential store, create new credentials, or call control-plane APIs.
* **Authorship**: The GitLab user who committed each credential, matched against the members of the scanned group.
* **Cloud identity correlation**: A validated AWS, GCP, or Azure credential is linked in the Security Graph to the same identity discovered by the matching [AWS](https://docs.akeyless.io/docs/aws-scanner), [GCP](https://docs.akeyless.io/docs/gcp-scanner), or [Azure](https://docs.akeyless.io/docs/azure-scanner) Scanner.

Each finding records the file, line, and commit where the credential was found, a direct link to that line in GitLab, whether the credential is still present in the latest commit, and who introduced it and when. The credential value itself is never stored.

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

The GitLab Scanner authenticates with the access token stored in the GitLab Target. Both a [personal access token](https://docs.gitlab.com/user/profile/personal_access_tokens/) and a [group access token](https://docs.gitlab.com/user/group/settings/group_access_tokens/) are supported.

Both scopes below are **read-only**. The scanner never requires write access to your GitLab instance. It reads repository content in order to find credentials, but never stores a discovered credential's value.

The token needs both scopes, as neither one alone is enough:

| Scope             | Used for                                                            | If missing                                                                                                      |
| ----------------- | ------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------- |
| `read_api`        | Listing groups, projects, and group members                         | The scan fails before any project is scanned                                                                    |
| `read_repository` | Cloning each project over HTTPS to scan its source code and history | The scan completes, but every project is reported as a warning in the scan details and no findings are produced |

When you use a group access token, give it a role that can read the repository of every project in the group, such as **Reporter** or higher.

<Callout icon="ℹ️" theme="info">
  ### **Note:**

  For a self-managed instance, the Target's **URL** must point to that instance, and its **TLS Certificate** field must be empty.&#x20;

  For more information, see [Self-Managed GitLab Instances](#self-managed-gitlab-instances) below.
</Callout>

### Scan Warnings

Some access gaps do not fail the scan. The scan completes and reports each gap as a warning, visible in the scan details:

| Situation                                              | Result                                                                                             |
| ------------------------------------------------------ | -------------------------------------------------------------------------------------------------- |
| The token cannot list the members of a group           | All credentials are still found, but some or all are not attributed to the user who committed them |
| A project cannot be cloned                             | The project is skipped, and a warning names it                                                     |
| A project is larger than 250 MB, as reported by GitLab | The project is skipped, and a warning names it                                                     |

A few conditions fail the scan instead of producing a partial result, so that findings from earlier scans are kept:

* The token is invalid, expired, or missing the `read_api` scope.
* The **GitLab Group** is left blank, and the token is not a member of any group.
* The **GitLab Group** is a user namespace, not a group.
* The projects of one of the groups in scope cannot be listed. The remaining groups are still scanned, and a warning names the group that was skipped.

## Scan Scope

The **GitLab Group** field on the scanner controls which projects are scanned:

* **Blank**: Scans every group the token is a member of, including subgroups.
* **A group path**, for example `acme` or `acme/platform`: Scans only that group and its subgroups.

<Callout icon="ℹ️" theme="info">
  ### **Note:**

  Scan coverage follows the token user's group memberships. To scan every group you want covered, make sure the token's user is a member of each of them. The scanner only discovers groups the user belongs to, so a group the user is not a member of is outside the scan scope and is not listed in the scan results.
</Callout>

Archived projects are scanned, because a live credential in an archived project can still be used.

Scanners with overlapping scopes do not create duplicate findings. For example, one scanner for `acme` and another for `acme/platform` both scan `acme/platform/api`, and a credential in that project appears as a single finding.

## Self-Managed GitLab Instances

The GitLab Scanner scans GitLab.com by default. To scan a self-managed instance, set the GitLab Target's **URL** to that instance, for example `https://gitlab.example.com`. Instances served under a path, for example `https://example.com/gitlab`, are supported.

The following restrictions apply to self-managed instances:

* The URL must use HTTPS. Plain HTTP is accepted only for a loopback address, such as a local test instance, because the access token would otherwise cross the network unencrypted.
* A private certificate authority is not supported. A scanner that uses a GitLab Target with a **TLS Certificate** configured fails with an error. Use a separate GitLab Target, without a certificate, for scanning.

## Create a GitLab Scanner in the Akeyless Console

GitLab scanners are created and run from the Akeyless Console. There is no CLI or API command for scanners. The GitLab Target can be created from the Console or the CLI, as described in [GitLab Target](https://docs.akeyless.io/docs/gitlab-target).

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

| Policy                              | Severity | Applies when                                                                                                                                |
| ----------------------------------- | -------- | ------------------------------------------------------------------------------------------------------------------------------------------- |
| Live Secret Committed to Code       | Critical | The credential still works and its reach is unknown or wide, or it is a production credential the scanner treats as live without testing it |
| Critical Blast-Radius Code Secret   | Critical | The credential can reach a credential store, create new credentials, or call control-plane APIs                                             |
| Live Secret with Contained Reach    | High     | The credential still works, but its reach is limited, for example to a sandbox account or a principal with minimal permissions              |
| Revoked Secret Found in Git History | Medium   | The credential no longer works, but it remains in the project's history                                                                     |
| Unvalidated Secret Pattern in Code  | Low      | A likely credential was found, but whether it works could not be confirmed                                                                  |

A credential that still works is rated Critical unless its reach was confirmed to be limited, so a credential with unknown reach is always treated as the worst case.

<Callout icon="✅" theme="success">
  ### **Tip:**

  Deleting a branch or force-pushing does not remove a credential from GitLab, because keep-around and merge-request refs keep the commit reachable. After you rotate a leaked credential, purge it from the project's history and run GitLab housekeeping so those refs are expired.
</Callout>

Secret lifecycle policies such as Unused Secret, Stale Secret, and Rotation Overdue do not apply to GitLab findings, because they describe secrets held in a managed secret store rather than values committed to code.

### What's Next

* [Scanners](https://docs.akeyless.io/docs/scanners)
* [GitHub Scanner](https://docs.akeyless.io/docs/github-scanner)
* [GitLab Target](https://docs.akeyless.io/docs/gitlab-target)
