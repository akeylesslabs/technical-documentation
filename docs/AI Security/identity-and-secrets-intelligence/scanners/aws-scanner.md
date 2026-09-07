---
title: AWS Scanner
deprecated: false
hidden: false
link:
  new_tab: false
metadata:
  robots: index
---
The AWS Scanner is a native scanner type that inspects a connected AWS account, discovering the full inventory of identities (IAM users, roles, and groups), secrets (AWS Secrets Manager), and certificates (AWS Certificate Manager) it contains, along with the relationships between them. Each discovered object is evaluated against Identity & Secrets Intelligence security policies, which assess its risk posture and surface the resulting findings for review.

## Prerequisite

- An Akeyless account with the Identity & Secrets Intelligence license.
- A deployed and connected [Akeyless Gateway](doc:gateway-overview) version `4.53.0` and later .
- A Gateway with [Akeyless AI Insights](doc:akeyless-ai-insight) configured.
- An [AWS Target](https://docs.akeyless.io/docs/aws-targets) representing the AWS service account that will scan the account.
- The AWS principal used by the Target (IAM user or Gateway Cloud Identity role) granted the permissions listed under [AWS Service Account Permissions](#aws-service-account-permissions) below.
- A user with:&#x20;
  1. &#x20;"Manage ISI Scanners" or "Admin" [Gateway Permission](https://docs.akeyless.io/docs/gateway-access-permissions-reference).
  2. &#x20;"Identity & Secrets Intelligence" [Administrative Rule](https://docs.akeyless.io/docs/rbac#administrative-rules) set to Scoped or All.
  3. "list" permission on the AWS Target.<br />

## AWS Service Account Permissions

The AWS target bounded to a service account that scans your cloud environment. There are two permission levels:&#x20;

- Minimal set to get started, some features will be limited and results won't reflect the full security posture of your environment.
- Full set for a complete scan. Quick Setup perform a full scan but it relies on broad AWS-managed policies that grant more than the scanner actually uses.

### Quick Setup

Attach the AWS-managed policies `IAMReadOnlyAccess` and `AWSCertificateManagerReadOnly`, plus this custom read-only Secrets Manager policy:

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

<Callout icon="⚠️" theme="warning">
  ### Warning

  Do not use `SecretsManagerReadWrite` — it grants read and write access on secrets and is not a safe substitute.
</Callout>

<Callout icon="ℹ️" theme="info">
  ### Note

  `"Resource": "*"` above gives full coverage but can be scoped down — anything out of scope is simply reported as a gap in the Access Status.
</Callout>

### Full scan setup

All permissions below are **read-only**. The scanner never requires write access to your AWS environment, and never reads secret _values_, only metadata.

#### Must-Have Permissions

Without these, the scan **fails** and no results are produced.

| Used for                            | Permission                                         | If missing                                                                               |
| ----------------------------------- | -------------------------------------------------- | ---------------------------------------------------------------------------------------- |
| Secrets discovery (Secrets Manager) | `secretsmanager:ListSecrets`                       | Secrets scan fails                                                                       |
| Certificate discovery (ACM)         | `acm:ListCertificates`                             | Certificates scan fails                                                                  |
| Certificate details                 | `acm:DescribeCertificate`                          | Certificates scan fails if denied everywhere; otherwise reported as a gap                |
| Identity discovery                  | `iam:ListUsers`, `iam:ListRoles`, `iam:ListGroups` | Identities scan fails if all three are denied; a single missing one is reported as a gap |

#### Additional Permissions for a Full Scan

Without these, the scan still **completes**, but with reduced visibility. Missing permissions are reported in the scan's _Access Status_ (visible in scan details).

| Permission                                                                                                                                                               | What it adds                                                                                |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------- |
| `secretsmanager:DescribeSecret`, `secretsmanager:ListSecretVersionIds`                                                                                                   | Secret metadata: rotation status, last access/change dates, version history                 |
| `secretsmanager:GetResourcePolicy`                                                                                                                                       | Secret resource policies — who is granted access to each secret in the Security Graph       |
| `iam:ListAccessKeys`, `iam:GetAccessKeyLastUsed`, `iam:ListMFADevices`, `iam:GetLoginProfile`                                                                            | User credential hygiene: stale keys, missing MFA, console access                            |
| `iam:GetUserPolicy`, `iam:GetRolePolicy`, `iam:GetGroupPolicy`, `iam:GetPolicy`, `iam:GetPolicyVersion`                                                                  | Policy analysis — which identities can access which secrets                                 |
| `iam:ListUserPolicies`, `iam:ListAttachedUserPolicies`, `iam:ListRolePolicies`, `iam:ListAttachedRolePolicies`, `iam:ListGroupPolicies`, `iam:ListAttachedGroupPolicies` | Enumerating the policies attached to each identity (required for the policy analysis above) |
| `iam:GetGroup`                                                                                                                                                           | Group membership in the Security Graph                                                      |

## Create an AWS Scanner in the Akeyless Console

1. Log in to the Akeyless Console, and go to **Products > Identity & Secrets Intelligence > Scanners**.
2. Click **New**, and select the scanner type **AWS**, then click **Next**.
3. Define a **Name** for the scanner.
4. Select the **Target** representing the AWS account to scan, and the **Gateway** that will execute the scans, then click **Next**.
5. Use the **Object Type** drop-down list to select the scanner's scope, and click **Finish**.

## Scan AWS

1. Log in to the Akeyless Console, and go to **Products > Identity & Secrets Intelligence > Scanners**.
2. Click the AWS scanner.
3. Click **Start Scan**.

