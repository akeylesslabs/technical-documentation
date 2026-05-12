---
title: Identity & Secrets Intelligence
excerpt: Review the current Identity & Secrets Intelligence surfaces, access controls, and how the feature fits with other Akeyless AI capabilities.
deprecated: false
hidden: false
metadata:
  title: ''
  description: ''
  robots: index
---

> ⚠️ **Warning:**
>
> Identity and Secrets Intelligence is currently in early access. Features, behavior, and availability can change between releases.

Identity and Secrets Intelligence is a console surface for reviewing AI-related visibility and governance data in Akeyless.

In the current Akeyless Console, Identity and Secrets Intelligence includes these sections:

* Dashboard
* Inventory
* Scanners
* Policies

Identity and Secrets Intelligence complements the broader Akeyless AI security model. Secretless runtime retrieval reduces exposure to static credentials, Identity and Secrets Intelligence adds visibility and governance, and [Agentic Runtime Authority](https://docs.akeyless.io/docs/agentic-runtime-authority) adds runtime control for supported dynamic secrets.

## Access And Availability

In the current Console implementation, the menu is shown only when the account has the feature enabled and the user has admin-level Console access. The backend and CLI also expose a dedicated `isi-access` role rule.

### Use Identity & Secrets Intelligence In The Console

1. Sign in to the Akeyless Console.
2. In the left navigation, open **Identity & Secrets Intelligence**.
3. Use **Dashboard** for the high-level overview.
4. Use **Inventory** to review findings and drill into finding details.
5. Use **Scanners** to create scanners, start scans, stop running scans, and review scan history.
6. Use **Policies** to review available policies and change policy status.

The current Inventory implementation exposes finding details for secret, identity, and certificate findings, and supports updating finding status.

The current Scanner implementation supports creating scanners, starting scans, stopping active scans, reviewing scan history, and navigating from a running scan directly to **Inventory**.

### Control Access With RBAC

Use the `isi-access` administrative rule on a role to control access to Identity and Secrets Intelligence.

For command syntax, see [CLI Reference - Access Roles](https://docs.akeyless.io/docs/cli-reference-access-roles).

Supported values are:

* `none`
* `scoped`
* `all`

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

The current CLI validation accepts `none`, `scoped`, and `all`. It does not accept the legacy `own` value for `isi-access`.

## Example Workflow

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

* [Akeyless AI Insights](https://docs.akeyless.io/docs/akeyless-ai-insight) for natural-language interaction with the Akeyless identity security platform
* [Agentic Runtime Authority](https://docs.akeyless.io/docs/agentic-runtime-authority) for controlled runtime access to supported dynamic secrets
* [Prompt Injection Protection for AI Agents](https://docs.akeyless.io/docs/prompt-injection-protection-for-ai-agents) for guidance on reducing credential misuse risk in AI workflows

## Related AI Guides

* [Akeyless AI Insights](https://docs.akeyless.io/docs/akeyless-ai-insight)
* [Agentic Runtime Authority](https://docs.akeyless.io/docs/agentic-runtime-authority)
* [Prompt Injection Protection for AI Agents](https://docs.akeyless.io/docs/prompt-injection-protection-for-ai-agents)
