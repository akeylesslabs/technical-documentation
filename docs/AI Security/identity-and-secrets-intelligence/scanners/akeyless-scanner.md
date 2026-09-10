---
title: Akeyless  Scanner
deprecated: false
hidden: false
metadata:
  robots: index
---
The Akeyless Scanner is a native scanner type that inspects your Akeyless account, discovering the full inventory of identities, roles, and secrets it contains, along with the relationships between them. Each discovered object is evaluated against Identity & Secrets Intelligence security policies, which assess its risk posture and surface the resulting findings for review.

## Prerequisite

- An Akeyless account with the Identity & Secrets Intelligence license.
- A deployed and connected [Akeyless Gateway](doc:gateway-overview) version `4.52.0` and later.
- A Gateway with [Akeyless AI Insights](doc:akeyless-ai-insight) configured.
- A user with "Manage ISI Scanners"  or "Admin" [Gateway Permission](https://docs.akeyless.io/docs/gateway-access-permissions-reference).
- A user with  "Identity & Secrets Intelligence" [Administrative Rule](https://docs.akeyless.io/docs/rbac#administrative-rules) set to Scoped or All.<br />

## Create an Akeyless Scanner in the Akeyless Console

1. Log in to the Akeyless Console, and go to **Products** > **Identity & Secrets Intelligence** > **Scanners**.
2. Click **New**, and select the scanner type **Akeyless** then click **Next**.
3. Define a **Name** for the scanner.
4. Define a **Gateway&#x20;**&#x74;hat will execute the scans and click **Next**.
5. Use the **Object Type** drop-down list to select the scanner's scope, and click **Finish**.<br />&#x20;

## Scan Akeyless&#x20;

1. Log in to the Akeyless Console, and go to **Products** > **Identity & Secrets Intelligence** > **Scanners**.
2. Click the Akeyless scanner&#x20;
3. Click **start scan&#x20;**

Once the scan completes, results appear in [Inventory](doc:identity-and-secrets-intelligence#inventory) for review.

<br />
