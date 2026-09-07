---
title: GitHub Scanner
deprecated: false
hidden: false
metadata:
  robots: index
---
The GitHub Scanner is a native scanner type that inspects a connected GitHub organization or enterprise, discovering the full inventory of identities (organization members, teams, and GitHub Apps) and secrets it contains across the organization's repositories, along with the relationships between them. Each discovered object is evaluated against Identity & Secrets Intelligence security policies, which assess its risk posture and surface the resulting findings for review.

## Prerequisites

- An Akeyless account with the Identity & Secrets Intelligence license.
- A deployed and connected [Akeyless Gateway](doc:gateway-overview) version `5.1.0` and later.
- A Gateway with [Akeyless AI Insights](doc:akeyless-ai-insight) configured.
- A [GitHub Target](https://docs.akeyless.io/docs/github-targets) representing the GitHub App that will scan the organization or enterprise.
- The GitHub App used by the Target granted the scope listed under [Required GitHub Permissions](#required-github-permissions) below.
- Access to configure and run the scanner, granted via:
  1. "Manage ISI Scanners" or "Admin" [Gateway Permission](https://docs.akeyless.io/docs/gateway-access-permissions-reference).
  2. "Identity & Secrets Intelligence" [Administrative Rule](https://docs.akeyless.io/docs/rbac#administrative-rules) set to Scoped or All.
  3. "List" permission on the GitHub Target.

## Required GitHub Permissions

### Quick Setup

The GitHub scanner authenticates with one of the credential types below. in GitHub missing access surfaces as warnings on the scan.

All permissions below are **read-only**. The scanner never requires write access to your GitHub organization, and never reads secret _values_, only metadata.

### Authentication & Scopes

| Credential                                      | Scope / Permission                                              | Enables                                                                       |
| ----------------------------------------------- | --------------------------------------------------------------- | ----------------------------------------------------------------------------- |
| Personal Access Token (classic or fine-grained) | Read access to the organizations/repositories in scope          | Standard organization and repository scanning                                 |
| GitHub App                                      | `organization_personal_access_tokens` permission                | PAT-grant scanning                                                            |
| Classic PAT with `admin:enterprise`             | Enterprise scope (GitHub Apps cannot call enterprise endpoints) | Enterprise-level scanning; audit-log-based features require GitHub Enterprise |

## Notes

- GitHub Apps **cannot** call enterprise-level endpoints — enterprise scanning requires a classic PAT with `admin:enterprise`.
- Audit-log-based features are only available with GitHub Enterprise.

## Create a GitHub Scanner

1. Log in to the Akeyless Console, and go to **Products > Identity & Secrets Intelligence > Scanners**.
2. Click **New**, and select the scanner type **GitHub**, then click **Next**.
3. Define a **Name** for the scanner.
4. Select the **Target** representing the organization or enterprise to scan, and the **Gateway** that will execute the scans, then click **Next**.
5. Use the **Object Type** drop-down list to select the scanner's scope, and click **Finish**.

## Run a Scan

1. Log in to the Akeyless Console, and go to **Products > Identity & Secrets Intelligence > Scanners**.
2. Click the GitHub scanner.
3. Click **Start Scan**.

Once the scan completes, results appear in [Inventory](doc:identity-and-secrets-intelligence#inventory) for review.
