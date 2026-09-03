---
title: GitHub Scanner
excerpt: Setup & Required Permissions
deprecated: false
hidden: false
metadata:
  robots: index
---
## Quick Setup

The GitHub scanner authenticates with one of the credential types below. Unlike the cloud scanners, missing access here surfaces as **warnings on the scan** rather than structured Must-have / Full-scan permission gaps.

All permissions below are **read-only**. The scanner never requires write access to your GitHub organization, and never reads secret _values_ — only metadata.

***

## Authentication & Scopes

| Credential                                      | Scope / permission                                              | Enables                                                                       |
| ----------------------------------------------- | --------------------------------------------------------------- | ----------------------------------------------------------------------------- |
| Personal Access Token (classic or fine-grained) | Read access to the organizations/repositories in scope          | Standard organization and repository scanning                                 |
| GitHub App                                      | `organization_personal_access_tokens` permission                | PAT-grant scanning                                                            |
| Classic PAT with `admin:enterprise`             | Enterprise scope (GitHub Apps cannot call enterprise endpoints) | Enterprise-level scanning; audit-log-based features require GitHub Enterprise |

***

## Notes

- There is no separate Must-have / Full-scan split for GitHub — scope is effectively all-or-nothing per credential type.
- GitHub Apps **cannot** call enterprise-level endpoints — enterprise scanning requires a classic PAT with `admin:enterprise`.
- Audit-log-based features are only available with GitHub Enterprise.
