---
title: 'AI Agents Policies '
deprecated: false
hidden: false
link:
  new_tab: false
metadata:
  robots: index
---
# AI Agent Policies

AI agents act on their own, hold their own credentials, and frequently outlive the person who deployed them, so an unowned or over-privileged agent becomes a standing risk that nobody is actively watching. AI Agent Policies encode ownership, least-privilege, and auditability expectations for every agent in your environment, so agent risk surfaces in **Inventory** the same consistent way secret and identity risk does.

Identity & Secrets Intelligence discovers AI agents as a first-class inventory type alongside secrets, identities, and certificates. Coverage currently spans Amazon Bedrock agents in both the Classic and AgentCore runtimes. Because an agent is also an identity, every applicable Identity Policy is evaluated against it as well, so an agent that is inactive or over-privileged is flagged by those rules in addition to the agent-specific ones below.

## Available AI Agent Policies

Identity & Secrets Intelligence currently ships the following built-in AI Agent Policies:

| Policy                                  | Severity | What It Flags                                                                                     |
| --------------------------------------- | -------- | ------------------------------------------------------------------------------------------------- |
| **Agentic Privilege Escalation**        | Critical | An agent whose execution role holds more privilege than the identity that created it              |
| **Orphaned Owner**                      | Critical | An active agent whose attributed owner or creator no longer resolves in IAM                       |
| **Insecure Inter-Agent Trust**          | High     | Two or more collaborator agents sharing a single execution role instead of independent identities |
| **Supervisor Aggregation Excess**       | High     | A supervisor or router agent aggregating access through more than 5 collaborator agents           |
| **Missing Guardrail**                   | High     | An agent with no guardrail attached to filter harmful content or denied topics                    |
| **Session/Credential Inheritance**      | High     | An execution role that can mint a human-scoped workload token instead of the agent's own identity |
| **Static/Long-Lived Credential in Use** | High     | A static, key-shaped credential in an action-group function's environment variables               |
| **Shared Credential Across Agents**     | High     | The same static credential referenced by two or more distinct agents                              |
| **Credential Age Violation**            | High     | Automatic rotation disabled on the agent's customer-managed KMS key                               |
| **Unowned Agent**                       | Medium   | An agent with no owner tag and no creator attributable from CloudTrail                            |
| **Missing Agent Decision Record**       | Medium   | An active agent with model-invocation logging disabled, leaving no record of its decisions        |
| **Retention Non-Compliance**            | Medium   | Agent invocation logs retained for fewer than 90 days                                             |
| **Wildcard Resource Binding**           | Medium   | An action-group function whose resource policy is not pinned to the invoking agent                |
| **Cross-Account/Cross-Tenant Reach**    | Medium   | An agent's execution role or tool resources reachable from outside the account or organization    |
| **Decommission Overdue**                | Medium   | An agent flagged stale that is still active more than 180 days after its last change              |

### What's Next

* [Policies](https://docs.akeyless.io/docs/policies)
* [Secret Policies](https://docs.akeyless.io/docs/secret-policies)
* [Identity Policies](https://docs.akeyless.io/docs/identity-policies)
* [Certificate Policies](https://docs.akeyless.io/docs/certificate-policies)
* [Agentic Runtime Authority](https://docs.akeyless.io/docs/agentic-runtime-authority)
