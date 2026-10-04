---
title: AWS Bedrock Scanner
deprecated: false
hidden: false
metadata:
  robots: index
---
# AWS Bedrock Scanner

The AWS Bedrock Scanner discovers the AI agents running in a connected AWS account. It covers both Amazon Bedrock Agents and Amazon Bedrock AgentCore agent runtimes. Each agent is discovered together with the execution role it runs as, the tools it can call, and the account configuration that governs it. Every agent is then evaluated against [ Identity & Secrets Intelligence security policies](doc:policies) , which assess its risk posture and surface the resulting findings for review.

Bedrock scanning is part of the [AWS Scanner](https://docs.akeyless.io/docs/aws-scanner). To scan Bedrock agents, create an AWS scanner and select the **AI Agents** object type, alone or together with the other AWS object types.

## What the AWS Bedrock Scanner Discovers

An AI agent is discovered as a workload identity: it runs as an execution role, and its effective access is whatever that role can reach. Discovered agents appear in **Findings** with the type **AI Agent**, alongside secrets, identities, and certificates:

* **Bedrock Agents**: Each agent with its execution role, its action groups and the AWS Lambda functions behind them, including each function's own execution role, its collaborator agents, its guardrail and foundation model, its `Owner` or `Team` tag, and the identity that created it, taken from CloudTrail.
* **Bedrock AgentCore agent runtimes**: Each agent runtime with its execution role, and an inventory of the MCP gateways in the account and the number of targets they route to.
* **Account configuration**: Whether Bedrock model invocation logging is enabled and how long its CloudWatch logs are retained, which agent resources IAM Access Analyzer reports as reachable from outside the account, and whether automatic rotation is enabled on the customer managed KMS key that encrypts an agent.
* **Execution identity relationships**: Each agent is linked in the Security Graph to the roles it runs as, its own execution role and the execution role of each Lambda function it can call. Privilege tends to accumulate on those Lambda roles.

To detect static credentials, the scanner reads the environment variables of each action-group Lambda function. A credential value found there is never stored. Only a short fingerprint is kept, to detect the same credential being used by more than one agent.

## Prerequisites

* An Akeyless account with the Identity & Secrets Intelligence license.
* A deployed and connected [Akeyless Gateway](https://docs.akeyless.io/docs/gateway-overview) version `5.5.0` and later.
* A Gateway with [Akeyless AI Insights](https://docs.akeyless.io/docs/akeyless-ai-insight) configured.
* An [AWS Target](https://docs.akeyless.io/docs/aws-targets) representing the AWS IAM Role that will scan the account, with its region set to the region where your agents run. The scanner uses an AWS Target, not a [Bedrock Target](https://docs.akeyless.io/docs/bedrock-target).
* The AWS IAM Role used by the Target granted the permissions listed under [Required AWS Permissions](#required-aws-permissions) below.
* Access to configure and run the scanner, granted via:
  1. `Manage ISI Scanners` or `Admin` [Gateway Permission](https://docs.akeyless.io/docs/gateway-access-permissions-reference).
  2. `Identity & Secrets Intelligence` [Administrative Rule](https://docs.akeyless.io/docs/rbac#administrative-rules) set to `Scoped` or `All`.
  3. `List` permission on the AWS Target.

## Required AWS Permissions

The AWS IAM Role used by the Target needs read access to Amazon Bedrock and to the AWS services an agent depends on. There are two ways to grant it:

* **Quick Setup** - attach broad AWS managed policies, plus one small custom policy for the services that have no read-only managed policy. Fastest to configure, but grants more access than the scanner actually uses.
* **Granular Permissions** - attach only the exact actions the scanner needs, following the principle of least privilege.

Both produce a complete scan. The difference is privilege scope, not scan coverage.

All permissions below are **read-only**. The scanner never requires write access to your AWS environment.

### Quick Setup

Attach the AWS managed policies `AmazonBedrockReadOnly`, `IAMReadOnlyAccess`, `AWSLambda_ReadOnlyAccess`, and `AWSCloudTrail_ReadOnlyAccess`, plus this custom read-only policy:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "bedrock-agentcore:ListAgentRuntimes",
        "bedrock-agentcore:GetAgentRuntime",
        "bedrock-agentcore:ListGateways",
        "bedrock-agentcore:ListGatewayTargets",
        "access-analyzer:ListAnalyzers",
        "access-analyzer:ListFindingsV2",
        "kms:DescribeKey",
        "kms:GetKeyRotationStatus",
        "logs:DescribeLogGroups"
      ],
      "Resource": "*"
    }
  ]
}
```

If the same Target is also used to scan secrets, certificates, or identities, also grant the permissions listed in [AWS Scanner](https://docs.akeyless.io/docs/aws-scanner).

### Granular Permissions

The tables below list every action the scanner calls when the **AI Agents** object type is selected, and what happens when each one is missing.

#### Required Permissions

The permissions listed below are required for agent discovery. If one is missing, agents are skipped, and in the cases described below, the scan fails:

| Used for                     | Permission                            | If missing                                                                                                 |
| ---------------------------- | ------------------------------------- | ---------------------------------------------------------------------------------------------------------- |
| Bedrock Agents discovery     | `bedrock:ListAgents`                  | The scan fails, even when the account only uses AgentCore                                                  |
| Bedrock Agents details       | `bedrock:GetAgent`                    | Agents that can't be read are skipped and reported as a gap. The scan fails if no agent can be read        |
| AgentCore runtimes discovery | `bedrock-agentcore:ListAgentRuntimes` | AgentCore agents are skipped and reported as a gap. The scan fails if no Bedrock Agents were found either  |
| AgentCore runtimes details   | `bedrock-agentcore:GetAgentRuntime`   | Runtimes that can't be read are skipped and reported as a gap. The scan fails if no agent was found at all |

Grant `bedrock:ListAgents` even if the account only uses AgentCore, because every Bedrock scan starts by listing Bedrock Agents.

#### Additional Permissions for Complete Coverage

These permissions are optional. If missing, the scan still completes, but with reduced visibility, and the policies that depend on them are not evaluated. Unless noted otherwise, each gap is listed under **Required Permissions For Full Scan** in the scan details.

| Permission                                                                                                                         | What it adds                                                                                                                                                                                |
| ---------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `bedrock:ListAgentActionGroups`, `bedrock:GetAgentActionGroup`                                                                     | The agent's action groups and the Lambda functions they call                                                                                                                                |
| `lambda:GetFunctionConfiguration`                                                                                                  | Each action-group function's execution role, and the static credentials in its environment variables                                                                                        |
| `lambda:GetPolicy`                                                                                                                 | Each action-group function's resource policy, used to check whether only this agent can invoke it                                                                                           |
| `bedrock:ListAgentCollaborators`                                                                                                   | Multi-agent collaboration: a supervisor agent's collaborators and their execution roles                                                                                                     |
| `bedrock:ListTagsForResource`                                                                                                      | The agent's `Owner` or `Team` tag                                                                                                                                                           |
| `cloudtrail:LookupEvents`                                                                                                          | The identity that created each agent, from `CreateAgent` events in the last 90 days. If missing, no gap is reported, and each agent without an `Owner` or `Team` tag is reported as unowned |
| `iam:ListAttachedRolePolicies`, `iam:ListAttachedUserPolicies`                                                                     | Comparing the agent's execution role with the privileges of the identity that created it                                                                                                    |
| `iam:GetUser`, `iam:GetRole`                                                                                                       | Whether the identity that created the agent still exists                                                                                                                                    |
| `iam:ListRolePolicies`, `iam:GetRolePolicy`, `iam:GetPolicy`, `iam:GetPolicyVersion`, together with `iam:ListAttachedRolePolicies` | Policy analysis of each execution role, including whether an AgentCore execution role can obtain access tokens on behalf of users                                                           |
| `bedrock:GetModelInvocationLoggingConfiguration`                                                                                   | Whether Bedrock model invocation logging is enabled                                                                                                                                         |
| `logs:DescribeLogGroups`                                                                                                           | The retention period of the CloudWatch log group that receives model invocation logs. If missing, no gap is reported                                                                        |
| `access-analyzer:ListAnalyzers`, `access-analyzer:ListFindingsV2`                                                                  | Agent execution roles and Lambda functions that IAM Access Analyzer reports as reachable from outside the account. Requires an IAM Access Analyzer in the Target's region                   |
| `kms:DescribeKey`, `kms:GetKeyRotationStatus`                                                                                      | Whether automatic rotation is enabled on the customer managed KMS key that encrypts an agent                                                                                                |
| `bedrock-agentcore:ListGateways`, `bedrock-agentcore:ListGatewayTargets`                                                           | The number of MCP gateways in the account and the targets they route to                                                                                                                     |

When no IAM Access Analyzer is enabled in the Target's region, cross-account reach is reported as a gap rather than as "no external access". Enable an analyzer in that region to get this check.

## Scan Scope

The scope of a Bedrock scan is set by the AWS Target and the object types selected on the scanner:

* **Region**: Agents are discovered only in the region configured on the AWS Target. To cover agents in several regions, create an AWS Target and a scanner for each region.
* **Agent types**: Bedrock Agents and AgentCore agent runtimes are both scanned under the **AI Agents** object type. They can't be selected separately.
* **Object types**: **AI Agents** is not selected by default. Select it explicitly when you create the scanner.

An agent's execution roles appear in the Security Graph whatever object types are selected. To also see what those roles are allowed to access, select **Identities**. To see which secrets they actually read in AWS Secrets Manager over the last 90 days, select **Secrets**. Both use the permissions listed in [AWS Scanner](https://docs.akeyless.io/docs/aws-scanner), and reading secret usage also requires `cloudtrail:LookupEvents`.

## Create an AWS Bedrock Scanner in the Akeyless Console

AWS Bedrock scanning is configured on an AWS scanner, which is created and run from the Akeyless Console. The AWS Target can be created from the Console or the CLI, as described in [AWS Targets](https://docs.akeyless.io/docs/aws-targets).

1. Log in to the Akeyless Console, and go to **Products > Identity & Secrets Intelligence > Scanners**.
2. Click **New**, and select the scanner type **AWS**, then click **Next**.
3. Define a **Name** for the scanner.
4. Select the **Gateway** that will execute the scans, and the **Target** representing the AWS account and region to scan, then click **Next**.
5. Use the **Object Type** drop-down list to select **AI Agents**. Optionally, also select **Identities** and **Secrets** for a complete Security Graph. Click **Finish**.

## Run a Scan

1. Log in to the Akeyless Console, and go to **Products > Identity & Secrets Intelligence > Scanners**.
2. Click the AWS scanner.
3. Click **Start Scan**.

Once the scan completes, discovered agents appear in **Findings** with the type **AI Agent**. Permission gaps appear in the scan details.

## AWS Bedrock Findings and Policies

AI agents are evaluated against the following Identity & Secrets Intelligence AI Agent Policies:

- Agentic Privilege Escalation
- Orphaned Owner
- Insecure Inter-Agent Trust
- Supervisor Aggregation Excess
- Missing Guardrail
- Session/Credential Inheritance
- Static/Long-Lived Credential in Use
- Shared Credential Across Agents
- Credential Age Violation
- Unowned Agent
- Missing Agent Decision Record
- Retention Non-Compliance
- Wildcard Resource Binding
- Cross-Account/Cross-Tenant Reach
- Decommission Overdue

For more information, see [AI Agent Policies](doc:ai-agent-policies).

Because an AI agent is also an identity, applicable [Identity Policies](doc:identity-policies) are evaluated against it as well, so an agent that is inactive or over-privileged is also flagged by those policies.

Most AI Agent Policies depend on details that only Bedrock Agents expose, such as action groups, collaborators, guardrails, and the identity that created the agent. AgentCore agent runtimes are mainly evaluated by Session/Credential Inheritance, Cross-Account/Cross-Tenant Reach, and the Identity Policies.

<Callout icon="✅" theme="success">
  ### **Tip:**

  Tag every Bedrock Agent with an `Owner` or `Team` tag. The tag identifies a responsible owner even when the agent was created more than 90 days ago, beyond the CloudTrail history the scanner reads.
</Callout>
