---
title: AWS Bedrock Scanner
deprecated: false
hidden: false
metadata:
  robots: index
---
# AWS Bedrock Scanner

The AWS Bedrock Scanner discovers the AI agents running in a connected AWS account. It covers both Amazon Bedrock Agents and Amazon Bedrock AgentCore agent runtimes. Each agent is discovered together with the execution role it runs as, the tools it can call, and the account configuration that governs it. Every agent is then evaluated against Identity & Secrets Intelligence security policies, which assess its risk posture and surface the resulting findings for review.

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
