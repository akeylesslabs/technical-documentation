---
title: Policies
deprecated: false
hidden: false
metadata:
  robots: index
---
Identity & Secrets Intelligence continuously evaluates every secret, identity, and certificate in your Inventory against a set of built-in policies. Each policy is a named rule that checks for a specific risk pattern, an unrotated secret, an over-privileged identity, an expiring certificate  and any match is surfaced as a finding with a severity, in **Dashboard** and **Inventory**. Policies is where you review that rule set..

## What Are Policies

A policy translates raw inventory data into a "who can do what" risk signal: instead of just listing every secret, identity, and certificate you have, Policies tells you which of them violate a defined risk condition, and how severe that violation is. Findings roll up to **Dashboard** for an at-a-glance risk posture, and to **Inventory** for the underlying detail.

## Policy Categories

Policies are organized into three categories, matching the object types Identity & Secrets Intelligence inventories.

- [Secret Policies](doc:secret-policies) — Flag secret exposure risk and secret hygiene issues, such as unused, stale, or unrotated secrets. [Learn more about Secret Policies](doc:secret-policies).
- **Identity Policies** — Flag identity posture, privilege scope, and risky identity configurations. [Learn more about Identity Policies](doc:identity-policies).
- **Certificate Policies** — Flag certificate posture, lifecycle state, and certificate-related findings. [Learn more about Certificate Policies](doc:certificate-policies).

## Prerequisites

- The account has the Identity and Secrets Intelligence feature enabled.
- The user has admin-level Console access, or a role with the `isi-access` rule set to `scoped` or `all`.

For full RBAC setup instructions, see [Control Access With RBAC](doc:identity-and-secrets-intelligence#control-access-with-role-based-access-control-rbac).

## Using Policies

To review policies:

1. Log in to the Akeyless Console, and go to **Identity & Secrets Intelligence**.
2. Select **Policies**.
3. Review the available policies and their current status.
4. Enable or adjust policies based on findings surfaced in **Dashboard** and **Inventory**.

<Callout icon="ℹ️" theme="info">
  ### **Note:**

  Policies is currently available only in the Console — there is no CLI or API equivalent for reviewing or managing policies today.
</Callout>

<br />

<br />
