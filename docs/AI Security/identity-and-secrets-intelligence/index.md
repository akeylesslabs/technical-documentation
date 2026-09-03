---
title: Identity & Secrets Intelligence
deprecated: false
hidden: false
metadata:
  title: ''
  description: ''
  robots: index
---
Review the current **Identity & Secrets Intelligence&#x20;**&#x73;urfaces, access controls, and how the feature fits with other Akeyless AI capabilities.

<Callout icon="⚠️" theme="warn">
  ### **Warning:**

  Identity and Secrets Intelligence is currently in early access. Features, behavior, and availability can change between releases.
</Callout>

Identity and Secrets Intelligence is a console surface for reviewing AI-related visibility and governance data in Akeyless.

In the current Akeyless Console, Identity and Secrets Intelligence includes these sections:

- **Dashboard**
- [Inventory](doc:identity-and-secrets-intelligence-inventory)
- [Scanners](doc:identity-and-secrets-intelligence-scanners)
- [Policies](doc:identity-and-secrets-intelligence-policies)

Identity and Secrets Intelligence complements the broader Akeyless AI security model. Secretless runtime retrieval reduces exposure to static credentials, Identity and Secrets Intelligence adds visibility and governance, and [Agentic Runtime Authority](doc:agentic-runtime-authority) adds runtime control for supported dynamic secrets.

## Access And Availability

In the current Console implementation, the menu is shown only when the account has the feature enabled and the user has admin-level Console access. The backend and CLI also expose a dedicated `isi-access` role rule.

### Use Identity & Secrets Intelligence In The Console

1. Sign in to the Akeyless Console.
2. In the left navigation, open **Identity & Secrets Intelligence**.
3. Use **Dashboard** for the high-level overview.
4. Use **Inventory** to review findings and drill into finding details.
5. Use **Scanners** to create scanners, start scans, stop running scans, and review scan history.
6. Use **Policies** to review available policies and change policy status.

## Dashboard

Dashboard can be used to review high-level counts, trends, and status indicators that show where investigation is needed. It's the entry point for a monitoring session — start here to identify the highest-priority signals, then move into [Inventory](doc:identity-and-secrets-intelligence-inventory), [Scanners](doc:identity-and-secrets-intelligence-scanners), and [Policies](doc:identity-and-secrets-intelligence-policies) to investigate and remediate.

## Operational Views

Use these views to move from high-level posture checks to specific remediation tasks:

| View                                                             | Purpose                                                                                                        |
| ---------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------- |
| **Dashboard**                                                    | Review high-level counts, trends, and status indicators that show where investigation is needed.               |
| **[Inventory](doc:identity-and-secrets-intelligence-inventory)** | Drill into findings by type, status, and severity, then open finding details for follow-up actions.            |
| **[Scanners](doc:identity-and-secrets-intelligence-scanners)**   | Track scanner status, launch or stop scans, and review scan history before validating outcomes in Inventory.   |
| **[Policies](doc:identity-and-secrets-intelligence-policies)**   | Review policy scope and status, then enable or adjust policies based on findings from Dashboard and Inventory. |

## Example Monitoring Workflow

Use this workflow when you need a repeatable operating pattern for Identity and Secrets Intelligence:

1. Open **Dashboard** to identify the highest-priority signals.
2. Open **[Inventory](doc:identity-and-secrets-intelligence-inventory)** to filter and triage findings by type and status.
3. Open **[Scanners](doc:identity-and-secrets-intelligence-scanners)** to run targeted scans for affected environments.
4. Open **[Policies](doc:identity-and-secrets-intelligence-policies)** to validate that controls match your risk posture.
5. Return to **Dashboard** and **Inventory** to verify that remediation changes are reflected.

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

Use `update-role` when modifying an existing role:

```shell
akeyless update-role \
  --name <role-name> \
  --isi-access <none|scoped|all>
```

Use `get-role` to verify the role after the update:

```shell
akeyless get-role --name <role-name>
```

<Callout icon="📘" theme="info">
  The current CLI validation accepts `none`, `scoped`, and `all`. It does not accept the legacy `own` value for `isi-access`.
</Callout>

## Example Workflow: Granting Access And Reviewing Results

The following example shows one minimal workflow for granting access and reviewing results:

1. Create or update a role with `--isi-access scoped` or `--isi-access all`.
2. Associate the role with the authentication method that your operators use.
3. Sign in to the Akeyless Console.
4. Open **Identity & Secrets Intelligence**.
5. Review the **Dashboard**.
6. Open **Scanners**, start a scan, and then use **Inventory** to review the findings.

### CLI Example

```shell
akeyless create-role \
  --name <role-name> \
  --isi-access scoped
```

### Console Example

1. Sign in to the Akeyless Console.
2. Open **Identity & Secrets Intelligence**.
3. Open **Scanners**, and start a scan.
4. Open **Inventory**, and review the generated findings.

## How It Fits With Other AI Features

Use Identity and Secrets Intelligence together with the other Akeyless AI surfaces:

- [Akeyless AI Insights](doc:akeyless-ai-insight) for natural-language interaction with the Akeyless identity security platform
- [Agentic Runtime Authority](doc:agentic-runtime-authority) for controlled runtime access to supported dynamic secrets
- [Prompt Injection Protection for AI Agents](doc:prompt-injection-protection-for-ai-agents) for guidance on reducing credential misuse risk in AI workflows
