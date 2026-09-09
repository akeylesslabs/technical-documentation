---
title: Identity & Secrets Intelligence
deprecated: false
hidden: false
metadata:
  title: ''
  description: ''
  robots: index
---
Identity & Secrets Intelligence (ISI) is Akeyless's visibility and governance layer for secrets, identities, and certificates across connected environments such as AWS, Azure, GCP, GitHub, Kubernetes, and Akeyless itself. It works through three components that form a continuous cycle:&#x20;

1. Scanners discover every secret, identity, and certificate in a connected environment.
2. Policies evaluate that inventory against built-in rules for secret hygiene, identity privilege, and certificate lifecycle risk.
3. any object flagged with a violation becomes a finding in Inventory, where you can view its details, investigate its related objects and potential impact through a graph, and remediate it.

Akeyless Console, Identity and Secrets Intelligence includes these sections:

- **Dashboard**
- [Inventory](doc:identity-and-secrets-intelligence-inventory)
- [Scanners](doc:identity-and-secrets-intelligence-scanners)
- [Policies](doc:identity-and-secrets-intelligence-policies)

Identity and Secrets Intelligence complements the broader Akeyless AI security model. Secretless runtime retrieval reduces exposure to static credentials, Identity and Secrets Intelligence adds visibility and governance, and [Agentic Runtime Authority](doc:agentic-runtime-authority) adds runtime control for supported dynamic secrets.

## Access And Availability

- The account has the Identity and Secrets Intelligence feature enabled.
- The user is account admin, or has an [Access Role](doc:rbac) with Identity & Secrets Intelligence administrative rule set to `scoped` or `all`.

For quick Access Role setup instructions follow the next commands:

1. Create a new Access Role:
   ```shell
   akeyless create-role \
     --name <role-name> \
     --isi-access <scoped|all>
   ```
2. Associate the Role with an [Authentication Methods](doc:access-and-authentication-methods) Auth Method:
   ```shell
   akeyless update-auth-method-access \
     -n <auth-method-name> \
     --new-access-rules </path/to/role>
   ```

## Use Identity & Secrets Intelligence In The Console

1. Sign in to the Akeyless Console.
2. In the left navigation, open **Identity & Secrets Intelligence**.
3. Use **Dashboard** for the high-level overview.
4. Use **Inventory** to review findings and drill into finding details.
5. Use **Scanners** to create scanners, start scans, stop running scans, and review scan history.
6. Use **Policies** to review available policies.

## Dashboard

Dashboard can be used to review high-level counts, trends, and status indicators that show where investigation is needed. It's the entry point for a monitoring session — start here to identify the highest-priority signals, then move into [Inventory](doc:identity-and-secrets-intelligence-inventory), [Scanners](doc:identity-and-secrets-intelligence-scanners), and [Policies](doc:identity-and-secrets-intelligence-policies) to investigate and remediate.

## Operational Views

Use these views to move from high-level posture checks to specific remediation tasks:

| View                                                         | Purpose                                                                                                        |
| ------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------- |
| **Dashboard**                                                | Review high-level counts, trends, and status indicators that show where investigation is needed.               |
| [Inventory](doc:identity-and-secrets-intelligence-inventory) | Drill into findings by type, status, and severity, then open finding details for follow-up actions.            |
| [Scanners](doc:identity-and-secrets-intelligence-scanners)   | Track scanner status, launch or stop scans, and review scan history before validating outcomes in Inventory.   |
| [Policies](doc:identity-and-secrets-intelligence-policies)   | Review policy scope and status, then enable or adjust policies based on findings from Dashboard and Inventory. |

## Example Monitoring Workflow

Use this workflow when you need a repeatable operating pattern for Identity and Secrets Intelligence:

1. Open **Dashboard** to identify the highest-priority signals.
2. Open [Inventory](doc:identity-and-secrets-intelligence-inventory) to filter and triage findings by type and status.
3. Open [Scanners](doc:identity-and-secrets-intelligence-scanners) to run targeted scans for affected environments.
4. Open [Policies](doc:identity-and-secrets-intelligence-policies) to validate that controls match your risk posture.
5. Return to **Dashboard** and **Inventory** to verify that remediation changes are reflected.

### Console Example

1. Sign in to the Akeyless Console.
2. Open **Identity & Secrets Intelligence**.
3. Open **Scanners**, and start a scan.
4. Open **Inventory**, and review the generated findings.

## Inventory

Drill into findings by type, status, and severity. Opening a finding surfaces why it matters, a graph of what it's connected to, and remediation steps — including AI-powered remediation assistance — so you can act without leaving the flow.

<br />

## How It Fits With Other AI Features

Use Identity and Secrets Intelligence together with the other Akeyless AI surfaces:

- [Akeyless AI Insights](doc:akeyless-ai-insight) for natural-language interaction with the Akeyless identity security platform
- [Agentic Runtime Authority](doc:agentic-runtime-authority) for controlled runtime access to supported dynamic secrets
- [Prompt Injection Protection for AI Agents](doc:prompt-injection-protection-for-ai-agents) for guidance on reducing credential misuse risk in AI workflows

## Control Access With Role-Based Access Control (RBAC)

Use the `isi-access` administrative rule on a role to control access to Identity and Secrets Intelligence.

For command syntax, see [CLI Reference - Access Roles](doc:cli-reference-access-roles).

Supported values are:

- `none`
- `scoped`
- `all`

Use `create-role` when creating a new role:

```shell
akeyless create-role \
  --name <role-name> \
  --isi-access <none|scoped|all>
```
