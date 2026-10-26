---
title: AWS Organization-Wide Universal Secrets Connector
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
This page discusses extending an [AWS Universal Secrets Connector](https://docs.akeyless.io/docs/aws-universal-secrets-connector) across an entire AWS Organization, so that a single **USC** item can discover and manage secrets across every member account and region in scope, instead of being limited to the single account and region tied to its [AWS Target](https://docs.akeyless.io/docs/aws-targets). This brings AWS **USC** to parity with the **Organization** scope already available on the [GCP Universal Secrets Connector](https://docs.akeyless.io/docs/gcp-universal-secrets-connector).

## How It Works

GCP's Organization scope works because a single org-level IAM binding cascades automatically to every project, including ones created later. AWS has no equivalent binding — a trusted cross-account role has to be deployed into every member account individually, and there is no built-in way to be notified when a new account joins the organization. Org-wide AWS **USC** addresses both gaps:

- **Provisioning:** an Akeyless-provided CloudFormation StackSet template deploys the IAM role Akeyless needs into every account in scope, including accounts added to the organization later.
- **Discovery:** AWS Organizations account-membership events, forwarded to Akeyless, trigger an inventory refresh as soon as a new account joins, backed by a periodic reconciliation poll.

Once provisioned, a single AWS **USC** item is no longer bound to one account and region. You can target any in-scope account and region per use, by supplying either a full secret ARN or a discrete Account ID/Region pair wherever a secret identifier is accepted today.

## Prerequisites

- An existing [AWS Universal Secrets Connector](https://docs.akeyless.io/docs/aws-universal-secrets-connector), associated with an [AWS Target](https://docs.akeyless.io/docs/aws-targets) that has an [External ID](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_common-scenarios_third-party.html) configured.
- Permission in AWS Organizations to deploy a CloudFormation StackSet, with service-managed permissions and automatic deployment, against the organization root or a chosen Organizational Unit (OU).
- A decision on which account will authenticate the integration to AWS Organizations — the **management account** or a **delegated administrator** account, see [Choosing the Authenticating Account](#choosing-the-authenticating-account) below.

## Provisioning the Cross-Account Role

1. Deploy the Akeyless-provided CloudFormation StackSet template once, against either the organization root or a specific OU.
2. Enable **service-managed permissions** and **automatic deployment** on the StackSet. AWS Organizations then keeps the role in sync automatically: it is created in every account currently in the targeted scope, and deployed automatically into any account added to that scope afterward, with no separate activation step on the Akeyless side.
3. The template creates, in every in-scope account, an IAM role whose trust policy references the External ID already configured on your Akeyless AWS Target, and whose permission policy matches the [permission set documented for AWS USC](https://docs.akeyless.io/docs/aws-universal-secrets-connector#prerequisites) — applied uniformly through the StackSet instead of being configured by hand per account.

To change scope later, for example to add or remove an OU, re-run the StackSet against the new set of targets.

## Choosing the Authenticating Account

AWS Organizations requires a single account to authenticate the account-discovery integration described below. You can use either:

- **Management account:** Simplest option, requiring no additional AWS-side setup. Many organizations' security policies restrict placing third-party roles in the management account, so this option may not be available to you.
- **Delegated administrator** (recommended): Keeps the Akeyless integration's role out of the management account. Two constraints to be aware of before registering one:
  - AWS caps an organization at 5 registered delegated administrators in total, shared across every AWS service and vendor that uses this pattern, for example Security Hub, GuardDuty, or other third-party integrations. Confirm you have an available slot before registering Akeyless.
  - Once a delegated administrator is registered for StackSets, it receives full organization-wide StackSet deployment authority that the management account cannot further restrict at the AWS Organizations level. To narrow scope, target a specific OU with the StackSet itself, rather than relying on a permission boundary on the delegated administrator.

## Account Discovery

To keep the connector's inventory current as accounts are added to or removed from the organization, configure an EventBridge rule in the authenticating account that listens for AWS Organizations' native account-membership events, and forward matching events to Akeyless:

- `AccountJoinedOrganization`: Triggers an immediate inventory refresh and begins scanning the new account.
- `AccountDepartedOrganization`: Flags the removed account for review.

This detects organization membership changes in near real time, rather than waiting on a periodic re-sync. As a backstop, Akeyless also periodically polls the AWS Organizations `ListAccounts` API to reconcile its inventory, catching any account change missed by the EventBridge rule, for example in an organization where the rule has not been configured.

## Addressing Secrets by Account ID and Region

Unlike a GCP Secret Manager call, which is addressed by a fully-qualified resource path that embeds the project, an AWS Secrets Manager call is addressed by secret name or ARN, with the account and region determined by which role is assumed and which regional endpoint is used. To target a specific account and region from an org-wide AWS **USC** item, provide one of the following wherever a secret identifier is accepted:

- A full **ARN**: `arn:aws:secretsmanager:<region>:<account-id>:secret:<name>`, or
- A bare secret name together with discrete **Account ID** and **Region** parameters, as a convenience alternative to the full ARN.

The Gateway resolves whichever form is supplied to the matching regional endpoint and the per-account role provisioned by the StackSet, then assumes that role before calling AWS Secrets Manager.

This is supported consistently across every surface that resolves an AWS-backed **USC** item:

- **CLI:** Pass an Account ID and Region (or supply a full ARN as the secret identifier) on commands such as `akeyless usc get`, `akeyless usc create`, `akeyless usc update`, and `akeyless usc delete`. See the [CLI Reference](https://docs.akeyless.io/docs/cli-reference-universal-secrets-connector) for the exact flags.
- **API:** The Get/Describe/List request messages for AWS-backed **USC** items accept the same optional Account ID/Region (or ARN) fields, so Terraform, SDKs, and other programmatic callers can target a specific account and region without going through the CLI.
- **Sync:** Each [sync](https://docs.akeyless.io/docs/sync-secret) mapping to an AWS-backed **USC** item has its own Account ID/Region (or ARN) set at configuration time, since a sync mapping is a standing configuration rather than a one-off call.
- **Injector:** The [Akeyless Kubernetes Secrets Injector](https://docs.akeyless.io/docs/akeyless-kubernetes-secrets-injector) annotation syntax for an AWS-backed secret reference can specify an Account ID/Region (or ARN) per secret, so a single Injector deployment pointed at one org-wide **USC** item can still pull different secrets from different accounts and regions within the same workload.

> ℹ️ Assumed-Role Session Caching
>
> Targeting a different account requires the Gateway to call `sts:AssumeRole` before the first access to that account, and AWS STS sessions are valid for up to an hour. The Gateway caches assumed-role sessions per Account ID and reuses them until they are near expiry, instead of re-assuming on every fetch, to avoid unnecessary latency and STS rate limits when a single **USC** item spans many accounts.

## Global/All Regions Aggregation

Aggregating secrets across every region, and, combined with org-wide provisioning, every account in scope, into a single inventory view is a distinct, governance-focused capability from the per-secret Account ID/Region addressing described above. Every individual AWS secret still lives in exactly one region, aside from Secrets Manager's own native cross-region replicas.
