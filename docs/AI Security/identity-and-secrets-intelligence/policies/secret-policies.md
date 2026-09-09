---
title: Secret Policies
deprecated: false
hidden: false
metadata:
  robots: index
---
Secret Policies evaluate every secret in your Inventory for exposure risk and secret-hygiene issues. When a secret matches a policy's condition, it's surfaced as a finding in **Dashboard** and **Inventory**, with a severity that reflects how urgently it needs attention. For an overview of how policies fit into Identity & Secrets Intelligence as a whole, see [Policies](doc:policies).

## Available Secret Policies

Identity & Secrets Intelligence currently ships the following built-in Secret Policies:

| Policy                                       | Severity | What It Flags                                                                           |
| -------------------------------------------- | -------- | --------------------------------------------------------------------------------------- |
| **Unused Secret**                            | Medium   | A secret that has never been used since it was created (minimum age 30 days)            |
| **Stale Secret**                             | Medium   | A secret that hasn't been used in the last 90 days                                      |
| **Rotation Overdue**                         | High     | A secret that hasn't been rotated in the last 180 days                                  |
| **Automatic Rotation Disabled**              | High     | A secret that doesn't have automatic rotation enabled                                   |
| **Orphaned Secret**                          | Critical | A secret with no identifiable owner or associated application                           |
| **Least Privilege Access Control**           | High     | A secret that's accessible by an unusually large number of entities (more than 10)      |
| **Missing Metadata**                         | Low      | A secret that lacks tags, labels, or documentation                                      |
| **Stale Privileged Secret**                  | High     | A high-privilege secret (more than 10 accessors) that hasn't been used in 90+ days      |
| **Excessive Versions**                       | Low      | A secret with more than 10 retained versions                                            |
| **Public Access via Resource Policy**        | Critical | A resource policy that allows public access to the secret                               |
| **Cross-Account Access via Resource Policy** | Medium   | A resource policy that allows access from an external account                           |
| **Live Secret Committed to Code**            | Critical | A working credential found committed to source, in repo history or the current codebase |
| **Critical Blast-Radius Code Secret**        | Critical | A live, hardcoded credential in code that reaches a credential store or control plane   |
| **Revoked Secret Found in Git History**      | Medium   | A revoked or rotated credential that still exists in git history                        |
| **Unvalidated Secret Pattern in Code**       | Low      | A secret-like pattern found in code that hasn't been validated as a real credential     |

Coverage for these policies isn't uniform across every connected source:

<Callout icon="ℹ️" theme="info">
  ### **Note:**

  Applies To reflects which connected sources currently support each policy. Coverage can vary by source when the signal a policy needs — for example version history or resource-policy contents — isn't available from that source.
</Callout>

### What's Next

- [Policies](doc:policies)
- [Identity Policies](doc:identity-policies)
- [Certificate Policies](doc:certificate-policies)
