---
title: GCP Scanner
deprecated: false
hidden: false
metadata:
  robots: index
---
The GCP Scanner is a native scanner type that inspects a connected Google Cloud project, folder, or organization, discovering the full inventory of identities, including human and non-human identities such as Google Cloud users and groups, service accounts and their keys, and workload and workforce identity federation principals, along with secrets stored in Secret Manager and certificates managed through Private CA, Certificate Manager, and Compute Engine SSL certificates, as well as the relationships between them. Each discovered object is evaluated against Identity & Secrets Intelligence security policies, which assess its risk posture and surface the resulting findings for review.

## What the GCP Scanner Discovers

Each scanner covers one or more object types, selected when the scanner is created:

| Object Type      | What is discovered                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| ---------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Secrets**      | Secret Manager secrets, with their replication and customer-managed encryption key settings, expiration, labels, and version history (version counts by state, and last changed and last rotated dates), plus last-accessed dates from Cloud Audit Logs. Secret values are never read.                                                                                                                                                                                           |
| **Certificates** | Private CA certificate authorities and issued certificates, Certificate Manager certificates, and global and regional Compute Engine SSL certificates, each with its location, labels, and source-specific details such as CA pool, tier, and revocation status for Private CA, and managed domains and subject alternative names for Google-managed certificates.                                                                                                               |
| **Identities**   | Users, groups, service accounts and their user-managed keys, domains, workload and workforce identity federation principals, and public principals (`allUsers` and `allAuthenticatedUsers`), with the IAM roles they hold at the project, folder, and organization levels and on individual secrets and CA pools. Also IAM deny policies, service account impersonation paths, last-activity and last-authentication times, and the organization, folder, and project hierarchy. |

The scanner's scope can be set to a single Project, a Folder, or an entire Organization.

## Prerequisites

- An Akeyless account with the Identity & Secrets Intelligence license.
- A deployed and connected [Akeyless Gateway](doc:gateway-overview) version `4.52.0` and later.
- A Gateway with [Akeyless AI Insights](doc:akeyless-ai-insight) configured.
- A [GCP Target](https://docs.akeyless.io/docs/gcp-targets) representing the service account that will scan the project, folder, or organization.
- The service account used by the Target granted the permissions listed under [Required GCP Permissions](#required-gcp-permissions) below.
- Access to configure and run the scanner, granted via:
  - `Manage ISI Scanners` or `Admin` [Gateway Permission](https://docs.akeyless.io/docs/gateway-access-permissions-reference).
  - `Identity & Secrets Intelligence` [Administrative Rule](https://docs.akeyless.io/docs/rbac#administrative-rules) set to `Scoped` or `All`.
  - `List` permission on the GCP Target.

## Required GCP Permissions

The service account used by the Target needs read access to the Google Cloud services behind each object type selected on the scanner. Every table in this section has an **Object Type** column, so you can grant only what the selected object types need.

There are two ways to grant it:

- **Quick Setup** - assign a small set of predefined viewer roles. Fastest to configure, but grants more access than the scanner actually uses.
- **Granular Permissions** - assign only the exact permissions the scanner needs, following the principle of least privilege.

Both produce a complete scan, the difference is privilege scope, not scan coverage.

### Quick Setup

For each object type selected on the scanner, grant the service account the predefined roles listed below:

| Object Type      | Predefined roles                                                                             |
| ---------------- | -------------------------------------------------------------------------------------------- |
| **Secrets**      | `roles/secretmanager.viewer`, `roles/logging.privateLogViewer`                               |
| **Certificates** | `roles/privateca.auditor`, `roles/certificatemanager.viewer`, `roles/compute.viewer`         |
| **Identities**   | `roles/browser`, `roles/iam.securityReviewer`, `roles/policyanalyzer.activityAnalysisViewer` |

For **Folder** or **Organization** scope, also grant `roles/browser` on the folder or organization, whatever object types are selected, so the scanner can list the projects and folders underneath it.

<Callout icon="ℹ️" theme="info">
  ### Note

  For folder or organization scope, grant these roles at the folder or organization level so they inherit to all projects underneath. A project that does not inherit a role is reported as a gap in the scan details.
</Callout>

### Granular Permissions

All permissions below are **read-only**. The scanner never requires write access to your Google Cloud environment, and never reads secret _values_, only metadata.

#### Required Permissions

The permissions listed below are required for the scan to complete successfully. If one is missing for an object type selected on the scanner, the scan fails, in the cases described below:

| Object Type          | Used for                                                                                   | Permission                                                                                                                   | If missing                                                                                                    |
| -------------------- | ------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------- |
| **All object types** | Listing the projects and folders under the scope root (Folder and Organization scope only) | `resourcemanager.projects.list`, `resourcemanager.folders.list`                                                              | The scan fails                                                                                                |
| **Secrets**          | Discovering Secret Manager secrets                                                         | `secretmanager.secrets.list`                                                                                                 | The scan fails if the scope is a project; otherwise reported as a gap for that project                        |
| **Certificates**     | Discovering Private CA certificate authorities and certificates                            | `privateca.locations.list`, `privateca.caPools.list`, `privateca.certificateAuthorities.list`, `privateca.certificates.list` | Skipped and reported as a gap.  Fails if the scope is a project and all three certificate sources are skipped |
| **Certificates**     | Discovering Certificate Manager certificates                                               | `certificatemanager.locations.list`, `certificatemanager.certs.list`                                                         | Skipped and reported as a gap. Fails if the scope is a project and all three certificate sources are skipped  |
| **Certificates**     | Discovering Compute Engine SSL certificates                                                | `compute.sslCertificates.list`, `compute.regionSslCertificates.list`                                                         | Skipped and reported as a gap.  Fails if the scope is a project and all three certificate sources are skipped |
| **Identities**       | Resolving the project's folder and organization hierarchy (Project scope only)             | `resourcemanager.projects.get`                                                                                               | The scan fails                                                                                                |
| **Identities**       | Reading the project IAM policy, the foundation of identity discovery                       | `resourcemanager.projects.getIamPolicy`                                                                                      | The scan fails if the scope is a project; otherwise reported as a gap for that project                        |

Under **Folder** or **Organization** scope, a failure in one project is reported as a gap for that project, and the scan continues with the remaining projects.&#x20;

#### Additional Permissions for Complete Coverage

These permissions are optional. If missing, the scan still completes, but with reduced visibility, and the policies that depend on them are not evaluated. Each gap is listed under **Required Permissions For Full Scan** in the scan details.

| Object Type      | Permission                                                                                                                                              | What it adds                                                                                                                                         |
| ---------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Secrets**      | `secretmanager.versions.list`                                                                                                                           | Last changed and rotated dates, and version counts                                                                                                   |
| **Secrets**      | `logging.logEntries.list`                                                                                                                               | Last-accessed dates, from the last 90 days of audit logs. Requires Data Access audit logs, see [Prerequisites Beyond IAM](#prerequisites-beyond-iam) |
| **Secrets**      | `logging.privateLogEntries.list`                                                                                                                        | Reading the Data Access audit logs that record secret access. If missing, no gap is reported, and last-accessed dates stay empty                     |
| **Certificates** | Any certificate source not granted above                                                                                                                | Coverage across all three certificate sources                                                                                                        |
| **Identities**   | `resourcemanager.folders.get`, <br />`resourcemanager.organizations.get`                                                                                | The folder and organization hierarchy (Project scope). If missing, no gap is reported                                                                |
| **Identities**   | `resourcemanager.folders.getIamPolicy`, `resourcemanager.organizations.getIamPolicy`                                                                    | Access inherited from folder and organization bindings                                                                                               |
| **Identities**   | `iam.serviceAccounts.list`, <br />`iam.serviceAccountKeys.list`                                                                                         | Service accounts and their keys: key age, stale keys                                                                                                 |
| **Identities**   | `iam.serviceAccounts.getIamPolicy`                                                                                                                      | Service account impersonation paths                                                                                                                  |
| **Identities**   | `iam.denypolicies.list`                                                                                                                                 | Deny policies, so the graph doesn't overstate access                                                                                                 |
| **Identities**   | `iam.roles.get`                                                                                                                                         | Custom role definitions                                                                                                                              |
| **Identities**   | `secretmanager.secrets.list`, <br />`secretmanager.secrets.getIamPolicy`                                                                                | Secret-level access bindings                                                                                                                         |
| **Identities**   | `privateca.caPools.getIamPolicy`, <br />plus the Private CA permissions under **Required Permissions**                                                  | CA pool access bindings. If a list permission other than `privateca.locations.list` is missing, no gap is reported                                   |
| **Identities**   | `logging.logEntries.list`                                                                                                                               | Last-activity dates, from the last 90 days of audit logs                                                                                             |
| **Identities**   | `logging.privateLogEntries.list`                                                                                                                        | Activity recorded in Data Access audit logs. If missing, no gap is reported                                                                          |
| **Identities**   | `policyanalyzer.`<br />`serviceAccountLastAuthenticationActivities.query`, `policyanalyzer.`<br />`serviceAccountKeyLastAuthenticationActivities.query` | Service account and key last-authentication times (billing-enabled projects only)                                                                    |
| **Identities**   | `admin.directory.group.member.readonly` (Workspace scope)                                                                                               | Google Workspace group membership, see [Prerequisites Beyond IAM](#prerequisites-beyond-iam)                                                         |

### Prerequisites Beyond IAM

Granting the permissions above is not sufficient on its own, the following must also be in place:

- **APIs enabled per scanned project**: Cloud Resource Manager, IAM, Secret Manager, and (per capability) Cloud Logging, Private CA, Certificate Manager, Compute Engine, Policy Analyzer. A disabled API is reported as a warning, granting a role does not fix it.
- **Data Access audit logs**: secret last-accessed dates require a `DATA_READ` audit-log configuration for Secret Manager (or all services) in the project.
- **Workspace groups**: group expansion requires domain-wide delegation configured in the Google Workspace Admin Console, plus a Workspace admin email set in the scanner settings.

## Create a GCP Scanner

1. Log in to the Akeyless Console, and go to **Products > Identity & Secrets Intelligence > Scanners**.
2. Click **New**, and select the scanner type **GCP**, then click **Next**.
3. Define a **Name** for the scanner.
4. Select the **Gateway** that will execute the scans, and **Target** representing the project, folder, or organization to scan, then click **Next**.
5. Use the **Object Type** drop-down list to select the scanner's scope, and click **Finish**.

## Run a Scan

1. Log in to the Akeyless Console, and go to **Products > Identity & Secrets Intelligence > Scanners**.
2. Click the GCP scanner.
3. Click **Start Scan**.

Once the scan completes, results appear in **Inventory** for review.
