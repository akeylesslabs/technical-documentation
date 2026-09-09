---
title: Secret Policies
deprecated: false
hidden: false
metadata:
  robots: index
---
Secret hygiene is one of the most common paths to a breach, a stale, over-permissioned, or unrotated secret is exactly the kind of exposure attackers look for. Secret Policies encode what good secret hygiene looks like, so every secret in your environment is judged against the same bar instead of relying on manual review.

## Available Secret Policies

Identity & Secrets Intelligence currently ships the following built-in Secret Policies:

| Policy                                       | Severity | What It Flags                                                                           | Applies To                                    |
| -------------------------------------------- | -------- | --------------------------------------------------------------------------------------- | --------------------------------------------- |
| **Orphaned Secret**                          | Critical | A secret with no identifiable owner or associated application                           | AWS, Akeyless, GCP, Azure, GitHub             |
| **Public Access via Resource Policy**        | Critical | A resource policy that allows public access to the secret                               | AWS, Akeyless, GCP                            |
| **Live Secret Committed to Code**            | Critical | A working credential found committed to source, in repo history or the current codebase | GitHub code secrets                           |
| **Critical Blast-Radius Code Secret**        | Critical | A live, hardcoded credential in code that reaches a credential store or control plane   | GitHub code secrets                           |
| **Rotation Overdue**                         | High     | A secret that hasn't been rotated in the last 180 days                                  | AWS, Akeyless, GCP, Azure, GitHub             |
| **Automatic Rotation Disabled**              | High     | A secret that doesn't have automatic rotation enabled                                   | AWS, Akeyless, GCP, GitHub                    |
| **Least Privilege Access Control**           | High     | A secret that's accessible by an unusually large number of entities (more than 10)      | AWS, Akeyless, GCP, Azure, GitHub             |
| **Stale Privileged Secret**                  | High     | A high-privilege secret (more than 10 accessors) that hasn't been used in 90+ days      | AWS, Akeyless, GCP, GitHub                    |
| **Unused Secret**                            | Medium   | A secret that has never been used since it was created (minimum age 30 days)            | AWS, Akeyless, GCP, GitHub                    |
| **Stale Secret**                             | Medium   | A secret that hasn't been used in the last 90 days                                      | AWS, Akeyless, GCP, GitHub                    |
| **Cross-Account Access via Resource Policy** | Medium   | A resource policy that allows access from an external account                           | AWS, Akeyless, GCP                            |
| **Revoked Secret Found in Git History**      | Medium   | A revoked or rotated credential that still exists in git history                        | GitHub code secrets                           |
| **Missing Metadata**                         | Low      | A secret that lacks tags, labels, or documentation                                      | AWS, Akeyless, GCP, Azure, GitHub, Kubernetes |
| **Excessive Versions**                       | Low      | A secret with more than 10 retained versions                                            | AWS, Akeyless, GCP                            |
| **Unvalidated Secret Pattern in Code**       | Low      | A secret-like pattern found in code that hasn't been validated as a real credential     | GitHub code secrets                           |

### What's Next

- [Policies](doc:policies)
- [Identity Policies](doc:identity-policies)
- [Certificate Policies](doc:certificate-policies)
