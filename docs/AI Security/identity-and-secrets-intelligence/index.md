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

# Identity & Secrets Intelligence

## What Is Identity & Secrets Intelligence?

Identity & Secrets Intelligence is Akeyless continuous discovery and governance of secrets, identities, and certificates that exist across connected environments, and of what each one is authorized to reach. It extends the "who can do what" model Akeyless already applies to human and machine identities to non-human identities across AWS, Azure, GCP, GitHub, Kubernetes, and Akeyless itself, closing the gap between issuing a credential and knowing how it's actually being used. ISI operates as a continuous cycle of three components: scanning, policy evaluation, and inventory-driven remediation.

## How It Works

1. **Discover**: Scanners enumerate every secret, identity, and certificate across a connected environment.
2. **Evaluate**: Policies assess that inventory against built-in rules for secret hygiene, identity privilege, and certificate lifecycle risk.
3. **Remediate**: Any object in violation surfaces as a finding in Inventory. Its **Security Graph** tab maps the roles, identities, and resources connected to that finding, and its **Remediate** tab, including **AI-Powered Remediation**, provides the fix.

## Key Features

* Continuous discovery of secrets, identities, and certificates across connected environments
* Built-in policies covering secret hygiene, identity privilege, and certificate lifecycle risk
* Graph-based investigation of related objects and blast radius
* AI-powered remediation assistance on individual findings
* Dashboard with security posture, trends, and status indicators to prioritize investigation and remediation

## Supported Environments

AWS, Azure, GCP, GitHub, Kubernetes, and Akeyless itself.

## Access And Availability

Before you can use Identity & Secrets Intelligence, confirm the following:

* The account has the Identity and Secrets Intelligence feature enabled.
* The user is account admin, or has an [Access Role](doc:rbac) with Identity & Secrets Intelligence administrative rule set to `scoped` or `all`.

To set up an Access Role for ISI, run the following commands:

1. Create a new Access Role:
   ```shell
   akeyless create-role \
     --name <role-name> \
     --isi-access <scoped|all>
   ```
   Where:
   * `--name`: the name of the Access Role to create.
   * `--isi-access`: the level of ISI administrative access to grant the role, `scoped` or `all`.
2. Associate the Role with an [Authentication Methods](doc:access-and-authentication-methods) Auth Method:
   ```shell
   akeyless update-auth-method-access \
     -n <auth-method-name> \
     --new-access-rules </path/to/role>
   ```
   Where:
   * `-n`: the Auth Method to associate with the role.
   * `--new-access-rules`: the path of the Access Role to associate.

## Operational Views

Use these views to move from high-level posture checks to specific remediation tasks:

| View                                                       | Purpose                                                                                                                                                                                                                          |
| ---------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Dashboard**                                              | trends, top 5 issues to address first, and Scanners Overview.                                                                                                                                                                    |
| Inventory                                                  | Drill into findings by type, status, and severity. Opening a finding surfaces why it matters, a graph of related objects and blast radius, and remediation steps, including AI-powered investigation and remediation assistance. |
| [Scanners](doc:identity-and-secrets-intelligence-scanners) | Manage scanners and review scan history and details.                                                                                                                                                                             |
| [Policies](doc:identity-and-secrets-intelligence-policies) | Review policy scope and status.                                                                                                                                                                                                  |

## Next Steps

* [Scanners](doc:identity-and-secrets-intelligence-scanners) for scanner setup
* [Policies](doc:identity-and-secrets-intelligence-policies) for view policies
