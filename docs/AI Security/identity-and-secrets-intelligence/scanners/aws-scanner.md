---
title: AWS scanner
excerpt: AWS Scanner — Setup & Required Permissions
deprecated: false
hidden: false
metadata:
  robots: index
---
# AWS Scanner — Setup & Required Permissions

## Quick Setup

Attach the AWS-managed policies `IAMReadOnlyAccess` and `AWSCertificateManagerReadOnly`, plus the small custom read-only Secrets Manager policy below.

> **Do not use&#x20;**`SecretsManagerReadWrite` — despite the name, it grants write access and is not a safe substitute.

All permissions below are **read-only**. The scanner never requires write access to your AWS environment, and never reads secret _values_ — only metadata.

***

## Must-Have Permissions

Without these, the scan **fails** and no results are produced.

| Permission                                               | Used for                            | If missing                                                                               |
| -------------------------------------------------------- | ----------------------------------- | ---------------------------------------------------------------------------------------- |
| `secretsmanager:ListSecrets`                             | Secrets discovery (Secrets Manager) | Secrets scan fails                                                                       |
| `acm:ListCertificates`                                   | Certificate discovery (ACM)         | Certificates scan fails                                                                  |
| `acm:DescribeCertificate`                                | Certificate details                 | Certificates scan fails if denied everywhere; otherwise reported as a gap                |
| `iam:ListUsers`, <br />`iam:ListRoles`, `iam:ListGroups` | Identity discovery                  | Identities scan fails if all three are denied; a single missing one is reported as a gap |

***

## Additional Permissions for a Full Scan

Without these, the scan still **completes**, but with reduced visibility. Missing permissions are reported in the scan's _Access Status_ (visible in scan details).

| Permission                                                                                                                                                               | What it adds                                                                                |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------- |
| `secretsmanager:DescribeSecret`, `secretsmanager:ListSecretVersionIds`                                                                                                   | Secret metadata: rotation status, last access/change dates, version history                 |
| `secretsmanager:GetResourcePolicy`                                                                                                                                       | Secret resource policies — who is granted access to each secret in the Security Graph       |
| `iam:ListAccessKeys`, `iam:GetAccessKeyLastUsed`, `iam:ListMFADevices`, `iam:GetLoginProfile`                                                                            | User credential hygiene: stale keys, missing MFA, console access                            |
| `iam:GetUserPolicy`, `iam:GetRolePolicy`, `iam:GetGroupPolicy`, `iam:GetPolicy`, `iam:GetPolicyVersion`                                                                  | Policy analysis — which identities can access which secrets                                 |
| `iam:ListUserPolicies`, `iam:ListAttachedUserPolicies`, `iam:ListRolePolicies`, `iam:ListAttachedRolePolicies`, `iam:ListGroupPolicies`, `iam:ListAttachedGroupPolicies` | Enumerating the policies attached to each identity (required for the policy analysis above) |
| `iam:GetGroup`                                                                                                                                                           | Group membership in the Security Graph                                                      |

***

## Custom Secrets Manager Read-Only Policy

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "secretsmanager:ListSecrets",
        "secretsmanager:DescribeSecret",
        "secretsmanager:ListSecretVersionIds",
        "secretsmanager:GetResourcePolicy"
      ],
      "Resource": "*"
    }
  ]
}
```

> `"Resource": "*"` above gives full coverage but can be scoped down — anything out of scope is simply reported as a gap in the Access Status.
