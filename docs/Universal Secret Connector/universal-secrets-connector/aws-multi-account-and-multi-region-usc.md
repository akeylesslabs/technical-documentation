---
title: AWS Multi-Account & Multi-Region Universal Secrets Connector
excerpt: ''
deprecated: false
hidden: false
metadata:
  title: ''
  description: ''
  robots: index
next:
  description: ''
---
A standard [AWS Universal Secrets Connector](https://docs.akeyless.io/docs/aws-universal-secrets-connector) is bound to the single AWS account and region reachable through its [AWS Target](https://docs.akeyless.io/docs/aws-targets). This page describes how to extend that USC item to cover every account in an AWS Organization, and to pick the target account and region per call instead of creating a separate USC item (and target) for each one.

This brings AWS USC closer to parity with the [GCP Universal Secrets Connector](https://docs.akeyless.io/docs/gcp-universal-secrets-connector)'s **Organization** scope. GCP reaches that parity natively: every Secret Manager resource path embeds its project ID (`projects/<project>/secrets/<secret>`), and a GCP organization-level IAM binding cascades automatically to every project created under it, including ones created later. AWS has neither property; a cross-account IAM role has to be deployed into each member account individually, and secrets are addressed by name or ARN rather than by a path that carries the account with it. Reaching the same experience in AWS therefore requires two separate mechanisms:

* **Provisioning** - getting a trusted IAM role into every account in scope, including accounts added after the initial setup.
* **Discovery** - finding out that a new account was added to the organization (or an existing one removed), so scanning and inventory stay current without a manual step.

## Provisioning the role across every account

Akeyless provides a CloudFormation **StackSet** template that deploys the IAM role USC needs into every account under a chosen Organization root or organizational unit (OU):

1. Deploy the StackSet once, with **service-managed permissions** and **automatic deployment** enabled, against the org root or the OU you want covered.
2. The StackSet creates, in every account currently in scope and any account added to that OU later, an IAM role whose trust policy references the **External ID** already configured on your Akeyless [AWS Target](https://docs.akeyless.io/docs/aws-targets).
3. The role carries the same IAM policy documented under [Prerequisites](https://docs.akeyless.io/docs/aws-universal-secrets-connector#prerequisites) for a standard, single-account AWS USC - this is not a new permission model, the same policy is simply applied uniformly through the StackSet instead of being attached by hand in each account.

Because the trust policy and the account's permissions are both established by the customer's own StackSet execution, there is no separate manual "activate this account" step once an account lands in a targeted OU: deploying the StackSet is what grants Akeyless access, and adding an account to the OU is what extends it there.

**Scope is fully flexible.** Target the org root, or one or more specific OUs, at StackSet deployment time. To change scope later, re-run the StackSet against a different OU set.

### Choosing the authenticating account

The StackSet (and the discovery mechanism described below) run from an **authenticating account** - either the Organization's management account or a delegated administrator account. Either works, but the trade-offs differ:

| Authenticating account | Pros | Cons |
| --- | --- | --- |
| **Management account** | Simplest, no extra AWS-side setup | Places a third-party role in the org's single most sensitive account. Most customers' security policy disallows this outright |
| **Delegated administrator** (recommended) | Keeps the Akeyless role out of the management account | AWS caps an organization at 5 registered delegated administrators total, shared across every service that uses the pattern (Security Hub, GuardDuty, other CNAPPs, and so on) - a customer may already be at the cap. Also, once a delegated administrator is registered for StackSets, AWS grants it full org-wide deployment authority that the management account cannot further restrict; narrower scope has to come from which OU the StackSet targets, not from an AWS-side permission boundary on the delegated administrator |

Akeyless recommends using a delegated administrator account where the organization has capacity for one.

## Discovering new and removed accounts

Provisioning alone only covers accounts that already existed in the targeted OU when the StackSet last ran. To keep scanning current as the organization changes, Akeyless relies on AWS Organizations' native CloudTrail events for org membership changes:

* **`AccountJoinedOrganization`** - fired when an account is created in, or invited into, the organization. Akeyless recommends an EventBridge rule in the authenticating account that forwards this event to Akeyless, triggering an immediate inventory refresh and kicking off scanning for the new account - detection happens as the account joins, rather than on the next periodic sync.
* **`AccountDepartedOrganization`** - fired when an account leaves the organization, flagging the corresponding inventory entry for review.

A periodic `ListAccounts` poll runs alongside the event-driven path as a reconciliation backstop, to catch any organization where the EventBridge rule isn't configured, or where an individual event is missed.

## Addressing a secret by account and region

GCP's "one USC item, pick the project per call" experience works because every GCP Secret Manager resource path already embeds its project ID. AWS Secrets Manager calls don't carry that information - which account and region a `GetSecretValue` call reaches depends on which regional endpoint the SDK client is pointed at and which account's role its credentials were assumed into, not on anything in the call itself. To reach the same "one USC item, pick the target per call" behavior in AWS, the secret identifier itself has to become self-describing.

Anywhere an AWS USC item accepts a bare secret name today, it also accepts:

* A full ARN - `arn:aws:secretsmanager:<region>:<account-id>:secret:<name>` - as the secret identifier, or
* Discrete **Account ID** and **Region** parameters alongside a bare secret name, as a convenience alternative to building the ARN by hand.

Whichever form is supplied, the Gateway resolves it to the matching regional endpoint and the per-account role provisioned by the StackSet above, and assumes into that role before calling AWS.

This applies consistently across every surface that resolves an AWS-backed USC item, not only the Console:

* **CLI** - an `--account-id` / `--region` pair, or a full ARN supplied as the secret identifier, on every command that resolves an AWS USC item (`usc get`, `usc create`, `usc update`, `usc delete`, and so on).
* **API** - the equivalent optional `account_id` / `region` (or `secret_arn`) fields on the Get/Describe/List request messages for AWS-backed items, so Terraform, SDKs, and other programmatic callers get the same override without going through the CLI.
* **Sync** - a [sync](https://docs.akeyless.io/docs/sync-secret) mapping is a standing, declarative configuration rather than a one-off call, so each mapping carries its own Account ID/Region (or ARN) set at configuration time.
* **Injector** - the [Kubernetes Injector](https://docs.akeyless.io/docs/akeyless-kubernetes-secrets-injector)'s injection template/annotation syntax carries an Account ID/Region (or ARN) per secret reference, so one Injector deployment pointed at a single org-wide USC item can still pull different secrets from different accounts and regions within the same workload spec.

<Callout icon="ℹ️" theme="info">
  ### Note

  "Global/All Regions" aggregation - viewing secrets across every account and region in scope in a single pane of glass - is a related but distinct, inventory-side capability. It is separate from the per-call Account ID/Region parameter described above, which only controls which single account and region a given secret access hits.
</Callout>

## Operational note: assumed-role session caching

Unlike GCP, switching accounts per call in AWS requires an `sts:AssumeRole` call before the first access to a given account in a while - STS sessions typically last up to an hour. The Gateway caches assumed-role sessions per Account ID and reuses them until they're close to expiry, rather than re-assuming on every fetch. This keeps routine fetches against an org-wide USC item spanning many accounts from turning into extra STS round-trips, and avoids hitting STS rate limits under load.