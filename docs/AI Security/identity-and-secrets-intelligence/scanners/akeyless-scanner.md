---
title: Akeyless  Scanner
deprecated: false
hidden: false
metadata:
  robots: index
---
The Akeyless Scanner is a native scanner type that inspects your Akeyless account, discovering the full inventory of identities, roles, secrets and certificates, as well as the relationships between them. Each discovered object is evaluated against Identity & Secrets Intelligence security policies, which assess its risk posture and surface the resulting findings for review.

## What the Akeyless Scanner Discovers

Each scanner covers one or more object types, selected when the scanner is created:

| Object Type      | What is discovered                                                                                                   |
| ---------------- | -------------------------------------------------------------------------------------------------------------------- |
| **Secrets**      | Static and rotated secrets, with their tags, dates, and rotation details, plus Targets                               |
| **Certificates** | Certificates stored in Akeyless, with their status, algorithms, and validity dates                                   |
| **Identities**   | Auth methods, Access Roles, and role assignments, showing which identities can access which secrets and certificates |

## Prerequisite

- An Akeyless account with the Identity & Secrets Intelligence license.
- A deployed and connected [Akeyless Gateway](doc:gateway-overview) version `4.52.0` and later.
- A Gateway with [Akeyless AI Insights](doc:akeyless-ai-insight) configured.
- A user with `Manage ISI Scanners`  or `Admin` [Gateway Permission](https://docs.akeyless.io/docs/gateway-access-permissions-reference).
- A user with  `Identity & Secrets Intelligence` [Administrative Rule](https://docs.akeyless.io/docs/rbac#administrative-rules) set to Scoped or All.

## Required Akeyless Permissions

The Akeyless Scanner does not use a Target. Grant the **List** capability on the Access Role associated with the Gateway's Admin Access ID. The scanner only lists objects, and never reads secret values.

| Object Type      | Access Role rules          | Capability |
| ---------------- | -------------------------- | ---------- |
| **Secrets**      | Items, Targets             | **List**   |
| **Certificates** | Items                      | **List**   |
| **Identities**   | Auth Methods, Access Roles | **List**   |

To scan the whole account, set the path of each rule to `/*`.

<Callout icon="⚠️" theme="warning">
  ### Warning

  Objects the Admin Access ID can't list are skipped without a warning. If an object is missing from **Findings**, check the rules of the Access Role associated with the Gateway's Admin Access ID.
</Callout>

## Create an Akeyless Scanner in the Akeyless Console

1. Log in to the Akeyless Console, and go to **Products** > **Identity & Secrets Intelligence** > **Scanners**.
2. Click **New**, and select the scanner type **Akeyless** then click **Next**.
3. Define a **Name** for the scanner.
4. Define a **Gateway&#x20;**&#x74;hat will execute the scans and click **Next**.
5. Use the **Object Type** drop-down list to select the scanner's scope, and click **Finish**.&#x20;

## Scan Akeyless&#x20;

1. Log in to the Akeyless Console, and go to **Products** > **Identity & Secrets Intelligence** > **Scanners**.
2. Click the Akeyless scanner&#x20;
3. Click **start scan&#x20;**

Once the scan completes, results appear in **Inventory** for review.

<br />
