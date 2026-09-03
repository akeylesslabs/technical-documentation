---
title: Scanners
deprecated: false
hidden: false
metadata:
  robots: index
---
Create and run scanners, stop active scans, review scan history, and navigate directly to Inventory to validate scan outcomes.

## Access

Scanners is shown only when:

- The account has the Identity and Secrets Intelligence feature enabled.
- The user has admin-level Console access, or a role with the `isi-access` rule set to `scoped` or `all`.

For full RBAC setup instructions, see [Control Access With RBAC](doc:identity-and-secrets-intelligence#control-access-with-role-based-access-control-rbac).

## Scanner Types

When you create a scanner, choose a **Source Type** for the environment you want to scan. The following source types are supported:

### AWS

Scans an AWS environment for secret, identity, and certificate findings.

<Callout icon="✏️" theme="default">
  ### **Required permissions:** _\[add AWS scanner permissions here]_
</Callout>

### Akeyless

Scans your Akeyless account itself for secret, identity, and certificate findings.

<Callout icon="✏️" theme="default">
  ### **Required permissions:** _\[add Akeyless scanner permissions here]_
</Callout>

### Azure

Scans an Azure environment for secret, identity, and certificate findings.

<Callout icon="✏️" theme="default">
  ### **Required permissions:** _\[add Azure scanner permissions here]_
</Callout>

### GCP

Scans a GCP environment for secret, identity, and certificate findings.

<Callout icon="✏️" theme="default">
  ### **Required permissions:** _\[add GCP scanner permissions here]_
</Callout>

### GitHub

Scans a GitHub organization or repository set for secret, identity, and certificate findings.

<Callout icon="✏️" theme="default">
  ### **Required permissions:** _\[add GitHub scanner permissions here]_
</Callout>

### Kubernetes

Scans a Kubernetes cluster for secret, identity, and certificate findings.

<Callout icon="✏️" theme="default">
  ### **Required permissions:** _\[add Kubernetes scanner permissions here]_
</Callout>

## Using Scanners

1. Sign in to the Akeyless Console.
2. In the left navigation, open **Identity & Secrets Intelligence**.
3. Select **Scanners**.
4. Create a scanner and choose a source type (see [Scanner Types](#scanner-types) above).
5. Start a scan.
6. Stop the scan if needed, or let it complete.
7. Review scan history for past runs.
8. Navigate directly to **Inventory** from a running scan to review generated findings.

<br />

##
