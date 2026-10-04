---
title: AWS Scanner
deprecated: false
hidden: false
link:
  new_tab: false
metadata:
  robots: index
---
The AWS Scanner is a native scanner type that inspects a connected AWS account, discovering the full inventory of identities, including human and non-human identities such as IAM users, roles, and groups, and AI agents built on Amazon Bedrock Agents and Amazon Bedrock AgentCore, along with secrets stored in AWS Secrets Manager and certificates managed through AWS Certificate Manager, as well as the relationships between them. Each discovered object is evaluated against Identity & Secrets Intelligence security policies, which assess its risk posture and surface the resulting findings for review.

## What the AWS Scanner Discovers

Each scanner covers one or more object types, selected when the scanner is created:

| Object Type      | What is discovered                                                                                                                                    |
| ---------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Secrets**      | Secrets stored in AWS Secrets Manager, with their rotation status, access history, resource policies, and the identities that read them               |
| **Certificates** | Certificates managed through AWS Certificate Manager, and the identities that read them                                                               |
| **Identities**   | IAM users, roles, and groups, with their credentials, MFA status, attached policies, and group memberships                                            |
| **AI Agents**    | Amazon Bedrock Agents and Amazon Bedrock AgentCore agent runtimes, with the roles they run as, the tools they call, and the controls that govern them |

Secrets, certificates, secret usage, and AI agents are discovered in the region configured on the AWS Target. IAM identities are global, so they are discovered for the whole account. To cover several regions, create an AWS Target and a scanner for each region.

## Prerequisites

* An Akeyless account with the Identity & Secrets Intelligence license.
* A deployed and connected [Akeyless Gateway](doc:gateway-overview) version `4.53.0` and later. Scanning AI agents requires version `5.5.0` and later.
* A Gateway with [Akeyless AI Insights](doc:akeyless-ai-insight) configured.
* An [AWS Target](https://docs.akeyless.io/docs/aws-targets) representing the AWS IAM Role that will scan the account.
* The AWS IAM Role used by the Target granted the permissions listed under [AWS Service Account Permissions](#aws-service-account-permissions) below.
* Access to configure and run the scanner, granted via:
  - `Manage ISI Scanners `or `Admin` [Gateway Permission](https://docs.akeyless.io/docs/gateway-access-permissions-reference).
  - `Identity & Secrets Intelligence` [Administrative Rule](https://docs.akeyless.io/docs/rbac#administrative-rules) set to `Scoped` or `All`.
  - `List` permission on the GitLab Target.

## Required AWS Permissions

The AWS IAM Role used by the Target needs read access to the AWS services behind each object type selected on the scanner. Every table in this section has an **Object Type** column, so you can grant only what the selected object types need.

There are two ways to grant the permissions:

* **Quick Setup** - attach broad AWS managed policies. Fastest to configure, but grants more access than the scanner actually uses.
* **Granular Permissions** - attach only the exact actions the scanner needs, following the principle of least privilege.

Both produce a complete scan. The difference is privilege scope, not scan coverage.

### Quick Setup

For each object type selected on the scanner, attach the AWS managed policies and the custom policy statement listed below:

| Object Type      | AWS managed policies                                                                                                                        | Custom policy statement |
| ---------------- | ------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------- |
| **Secrets**      | `AWSCloudTrail_ReadOnlyAccess`                                                                                                              | `SecretsReadOnly`       |
| **Certificates** | `AWSCertificateManagerReadOnly`                                                                                                             | None                    |
| **Identities**   | `IAMReadOnlyAccess`                                                                                                                         | None                    |
| **AI Agents**    | `AmazonBedrockReadOnly`, `IAMReadOnlyAccess`, `AWSLambda_ReadOnlyAccess`, `AWSCloudTrail_ReadOnlyAccess`, `IAMAccessAnalyzerReadOnlyAccess` | `AIAgentsReadOnly`      |

The custom policy below covers the services that have no read-only AWS managed policy: AWS Secrets Manager, Amazon Bedrock AgentCore, and AWS KMS. Keep the statement for each object type you selected, and remove the other:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "SecretsReadOnly",
      "Effect": "Allow",
      "Action": [
        "secretsmanager:ListSecrets",
        "secretsmanager:DescribeSecret",
        "secretsmanager:ListSecretVersionIds",
        "secretsmanager:GetResourcePolicy"
      ],
      "Resource": "*"
    },
    {
      "Sid": "AIAgentsReadOnly",
      "Effect": "Allow",
      "Action": [
        "bedrock-agentcore:ListAgentRuntimes",
        "bedrock-agentcore:GetAgentRuntime",
        "bedrock-agentcore:ListGateways",
        "bedrock-agentcore:ListGatewayTargets",
        "kms:DescribeKey",
        "kms:GetKeyRotationStatus"
      ],
      "Resource": "*"
    }
  ]
}
```

`"Resource": "*"` above gives full coverage but can be scoped down. Anything out of scope is reported as a gap in the scan details.

<Callout icon="⚠️" theme="warning">
  ### Warning

  Do not use `SecretsManagerReadWrite`. It grants read and write access on secrets and is not a safe substitute.
</Callout>

### Granular Permissions

All permissions below are **read-only**. The scanner never requires write access to your AWS environment, and never reads the _values_ of secrets stored in AWS Secrets Manager, only their metadata.

#### Required Permissions

The permissions listed below are required for the scan to complete successfully. If one is missing for an object type selected on the scanner, the scan fails, in the cases described below:

| Object Type      | Used for                     | Permission                                         | If missing                                                                                                 |
| ---------------- | ---------------------------- | -------------------------------------------------- | ---------------------------------------------------------------------------------------------------------- |
| **Secrets**      | Secrets discovery            | `secretsmanager:ListSecrets`                       | The scan fails                                                                                             |
| **Certificates** | Certificate discovery        | `acm:ListCertificates`                             | The scan fails                                                                                             |
| **Certificates** | Certificate details          | `acm:DescribeCertificate`                          | The scan fails if denied for every certificate; otherwise reported as a gap                                |
| **Identities**   | Identity discovery           | `iam:ListUsers`, `iam:ListRoles`, `iam:ListGroups` | The scan fails if all three are denied; a single missing one is reported as a gap                          |
| **AI Agents**    | Bedrock Agents discovery     | `bedrock:ListAgents`                               | The scan fails, even when the account only uses AgentCore                                                  |
| **AI Agents**    | Bedrock Agents details       | `bedrock:GetAgent`                                 | Agents that can't be read are skipped and reported as a gap. The scan fails if no agent can be read        |
| **AI Agents**    | AgentCore runtimes discovery | `bedrock-agentcore:ListAgentRuntimes`              | AgentCore agents are skipped and reported as a gap. The scan fails if no Bedrock Agents were found either  |
| **AI Agents**    | AgentCore runtimes details   | `bedrock-agentcore:GetAgentRuntime`                | Runtimes that can't be read are skipped and reported as a gap. The scan fails if no agent was found at all |

A failure in any selected object type marks the whole scan as failed.

#### Additional Permissions for Complete Coverage

These permissions are optional. If missing, the scan still completes, but with reduced visibility, and the policies that depend on them are not evaluated. Each gap is listed under **Required Permissions For Full Scan** in the scan details.

| Object Type    | Permission                                                                                                                                                               | What it adds                                                                                                                                                                                |
| -------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Secrets**    | `secretsmanager:DescribeSecret`, `secretsmanager:ListSecretVersionIds`                                                                                                   | Secret metadata: rotation status, last access/change dates, version history                                                                                                                 |
| **Secrets**    | `secretsmanager:GetResourcePolicy`                                                                                                                                       | Secret resource policies - who is granted access to each secret in the Security Graph                                                                                                       |
| **Secrets**    | `cloudtrail:LookupEvents`                                                                                                                                                | Secret usage - which identities actually read each secret over the last 90 days                                                                                                             |
| **Identities** | `iam:ListAccessKeys`, `iam:GetAccessKeyLastUsed`, `iam:ListMFADevices`, `iam:GetLoginProfile`                                                                            | User credential hygiene: stale keys, missing MFA, console access                                                                                                                            |
| **Identities** | `iam:GetUserPolicy`, `iam:GetRolePolicy`, `iam:GetGroupPolicy`, `iam:GetPolicy`, `iam:GetPolicyVersion`                                                                  | Policy analysis - which identities can access which secrets                                                                                                                                 |
| **Identities** | `iam:ListUserPolicies`, `iam:ListAttachedUserPolicies`, `iam:ListRolePolicies`, `iam:ListAttachedRolePolicies`, `iam:ListGroupPolicies`, `iam:ListAttachedGroupPolicies` | Enumerating the policies attached to each identity (required for the policy analysis above)                                                                                                 |
| **Identities** | `iam:GetGroup`                                                                                                                                                           | Group membership in the Security Graph                                                                                                                                                      |
| **AI Agents**  | `bedrock:ListAgentActionGroups`, `bedrock:GetAgentActionGroup`                                                                                                           | The agent's action groups and the Lambda functions they call                                                                                                                                |
| **AI Agents**  | `lambda:GetFunctionConfiguration`                                                                                                                                        | Each action-group function's execution role, and the static credentials in its environment variables                                                                                        |
| **AI Agents**  | `lambda:GetPolicy`                                                                                                                                                       | Each action-group function's resource policy, used to check whether only this agent can invoke it                                                                                           |
| **AI Agents**  | `bedrock:ListAgentCollaborators`                                                                                                                                         | Multi-agent collaboration: a supervisor agent's collaborators and their execution roles                                                                                                     |
| **AI Agents**  | `bedrock:ListTagsForResource`                                                                                                                                            | The agent's `Owner` or `Team` tag                                                                                                                                                           |
| **AI Agents**  | `cloudtrail:LookupEvents`                                                                                                                                                | The identity that created each agent, from `CreateAgent` events in the last 90 days. If missing, no gap is reported, and each agent without an `Owner` or `Team` tag is reported as unowned |
| **AI Agents**  | `iam:ListAttachedRolePolicies`, `iam:ListAttachedUserPolicies`                                                                                                           | Comparing the agent's execution role with the privileges of the identity that created it                                                                                                    |
| **AI Agents**  | `iam:GetUser`, `iam:GetRole`                                                                                                                                             | Whether the identity that created the agent still exists                                                                                                                                    |
| **AI Agents**  | `iam:ListRolePolicies`, `iam:GetRolePolicy`, `iam:GetPolicy`, `iam:GetPolicyVersion`, together with `iam:ListAttachedRolePolicies`                                       | Policy analysis of each execution role, including whether an AgentCore execution role can obtain access tokens on behalf of users                                                           |
| **AI Agents**  | `bedrock:GetModelInvocationLoggingConfiguration`                                                                                                                         | Whether Bedrock model invocation logging is enabled                                                                                                                                         |
| **AI Agents**  | `logs:DescribeLogGroups`                                                                                                                                                 | The retention period of the CloudWatch log group that receives model invocation logs. If missing, no gap is reported                                                                        |
| **AI Agents**  | `access-analyzer:ListAnalyzers`, `access-analyzer:ListFindings`                                                                                                          | Agent execution roles and Lambda functions that IAM Access Analyzer reports as reachable from outside the account. Requires an IAM Access Analyzer in the Target's region                   |
| **AI Agents**  | `kms:DescribeKey`, `kms:GetKeyRotationStatus`                                                                                                                            | Whether automatic rotation is enabled on the customer managed KMS key that encrypts an agent                                                                                                |
| **AI Agents**  | `bedrock-agentcore:ListGateways`, `bedrock-agentcore:ListGatewayTargets`                                                                                                 | The number of MCP gateways in the account and the targets they route to                                                                                                                     |

Each gap entry names the skipped resource, the missing permissions, and the AWS managed policy or custom policy that grants them.

## Create an AWS Scanner in the Akeyless Console

1. Log in to the Akeyless Console, and go to **Products > Identity & Secrets Intelligence > Scanners**.
2. Click **New**, and select the scanner type **AWS**, then click **Next**.
3. Define a **Name** for the scanner.
4. Select the **Target** representing the AWS account to scan, and the **Gateway** that will execute the scans, then click **Next**.
5. Use the **Object Type** drop-down list to select the scanner's scope, and click **Finish**.

## Run a Scan

1. Log in to the Akeyless Console, and go to **Products > Identity & Secrets Intelligence > Scanners**.
2. Click the AWS scanner.
3. Click **Start Scan**.

Once the scan completes, results appear in **Inventory** for review.

<br />
