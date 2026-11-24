---
title: Claude Scanner
deprecated: false
hidden: false
metadata:
  robots: index
---
The Claude Scanner is a native scanner type that inspects a connected Anthropic organization, discovering its Managed Agents: the agents running in Claude, the MCP servers they connect to, the vault users that own their credentials, and the vault credentials themselves, along with the relationships between them. Each discovered object is evaluated against Identity & Secrets Intelligence security policies, which assess its risk posture and surface the resulting findings for review.

## What the Claude Scanner Discovers

Each scanner covers one or more object types, selected when the scanner is created:

| Object Type    | What is discovered                                                                                                                                                                                                        |
| -------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **AI Agents**  | Managed Agents, one per agent per workspace, with the model, the MCP servers they connect to, their toolsets, skills, sub-agents, session count, last session, the networking mode of the environments their sessions ran in, and whether the agent is archived |
| **Identities** | The vault users that own the credentials Managed Agents use, one per vault external user ID                                                                                                                             |
| **Secrets**    | The vault credentials used by Managed Agents, with their type, the MCP server URL or environment variable they target, allowed hosts, and expiry                                                                       |

Every distinct MCP server URL found across the agents of the organization is also shown once, with its host, the names agents gave it, and how many agents and credentials connect to it.

The scanner covers the whole Anthropic organization behind the [Claude Target](doc:claude-target), fanning out across every workspace the target's API key can read.

## Prerequisites

- An Akeyless account with the Identity & Secrets Intelligence license.
- A deployed and connected [Akeyless Gateway](doc:gateway-overview).
- A Gateway with [Akeyless AI Insights](doc:akeyless-ai-insight) configured.
- A [Claude Target](doc:claude-target) representing the Anthropic organization to scan.
- The Claude Target configured with the API key described under [Required Anthropic Credentials](doc:claude-scanner#required-anthropic-credentials) below.
- Access to configure and run the scanner, granted via:
  - `Manage ISI Scanners` or `Admin` [Gateway Permission](doc:gateway-access-permissions-reference).
  - `Identity & Secrets Intelligence` [Administrative Rule](doc:rbac#administrative-rules) set to `Scoped` or `All`.
  - `List` permission on the Claude Target.

## Required Anthropic Credentials

The Claude Scanner authenticates with the single **API Key** set on the Claude Target. Use an organization-scoped API key of a service account:

| Role          | Enables                                                                                                                                      |
| ------------- | -------------------------------------------------------------------------------------------------------------------------------------------- |
| **Admin**     | Full coverage: members, invites, workspaces, API keys, usage, the compliance settings, workspace member roles, and Managed Agents             |
| **Developer** | The same Managed Agents coverage, with least privilege, but not the compliance settings or the workspace member roles                         |

An Admin API key, or an `org:admin` OAuth access token, is also accepted on the Target. Either reads every other listing, but not the Managed Agents endpoints.

<Callout icon="⚠️" theme="warning">
  ### Warning

  A scan whose Target holds an Admin API key or an `org:admin` token reports the permission gap **Anthropic managed agents**, and the AI Agents object type is not covered. Earlier AI Agents findings from a previous scan with a service-account key are kept, not pruned, while the gap is open.
</Callout>

Credential values are never returned by Anthropic. The scanner only reads credential metadata: its type, the MCP server URL or environment variable name it is bound to, and its allowed hosts.

## Per-Workspace Scanning

An organization-scoped API key reads every workspace the organization has, one at a time, using the workspace's ID. A workspace-scoped API key reads only its own workspace. A workspace the key cannot read is reported as a gap in the scan details, and the scan continues with the remaining workspaces. A failed or truncated listing for a workspace skips pruning of its earlier findings, so a temporary access or API error does not remove existing findings from Inventory.

## Create a Claude Scanner

1. Log in to the Akeyless Console, and go to **Products > Identity & Secrets Intelligence > Scanners**.
2. Click **New**, and select the scanner type **Claude**, then click **Next**.
3. Define a **Name** for the scanner.
4. Select the **Gateway** that will execute the scans, and the **Target** representing the Anthropic organization to scan, then click **Next**.
5. Use the **Object Type** drop-down list to select **Identities**, **Secrets**, **AI Agents**, or any combination, and click **Finish**.

## Run a Scan

1. Log in to the Akeyless Console, and go to **Products > Identity & Secrets Intelligence > Scanners**.
2. Click the Claude scanner.
3. Click **Start Scan**.

Once the scan completes, results appear in **Inventory** for review. The permission gap, and any workspace the Target's key could not read, appear in the scan details.

## Claude Findings and Policies

Claude findings are evaluated against the following Identity & Secrets Intelligence policies:

- **Agent With Unrestricted Network Access** (Medium)
- **MCP Server Without Credential** (Medium)
- **Shared Credential Across Agents** (High)
- **Static/Long-Lived Credential in Use** (High)

For more information, see [AI Agent Policies](doc:ai-agents-policies).

Vault credentials are also evaluated against the regular [Secret Policies](doc:secret-policies), once the scanner knows how a credential is used by an agent.
