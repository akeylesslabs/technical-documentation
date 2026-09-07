---
title: GCP Scanner
deprecated: false
hidden: false
metadata:
  robots: index
---
The GCP Scanner is a native scanner type that inspects a connected Google Cloud project, folder, or organization, discovering the full inventory of identities (Google Cloud users, groups, and service accounts), secrets (Secret Manager), and certificates (Private CA, Certificate Manager, and Compute Engine SSL certificates) it contains, along with the relationships between them. Each discovered object is evaluated against Identity & Secrets Intelligence security policies, which assess its risk posture and surface the resulting findings for review.

## Prerequisites

- An Akeyless account with the Identity & Secrets Intelligence license.
- A deployed and connected [Akeyless Gateway](doc:gateway-overview) version `4.52.0` and later.
- A Gateway with [Akeyless AI Insights](doc:akeyless-ai-insight) configured.
- A [GCP Target](https://docs.akeyless.io/docs/gcp-targets) representing the service account that will scan the project, folder, or organization.
- The service account used by the Target granted the permissions listed under [Required GCP Permissions](#required-gcp-permissions) below.
- Access to configure and run the scanner, granted via:
  1. "Manage ISI Scanners" or "Admin" [Gateway Permission](https://docs.akeyless.io/docs/gateway-access-permissions-reference).
  2. "Identity & Secrets Intelligence" [Administrative Rule](https://docs.akeyless.io/docs/rbac#administrative-rules) set to Scoped or All.
  3. "List" permission on the GCP Target.

## Required GCP Permissions

The service account used by the Target needs read access to your Google Cloud resource hierarchy. There are two ways to grant it:

- **Quick Setup** - assign a small set of predefined viewer roles. Fastest to configure, but grants more access than the scanner actually uses.
- **Granular Permissions** - assign only the exact permissions the scanner needs, following the principle of least privilege.

Both produce a complete scan, the difference is privilege scope, not scan coverage.

### Quick Setup

Grant the scanner's service account these predefined roles:

- `roles/browser`
- `roles/resourcemanager.folderViewer`
- `roles/iam.securityReviewer`
- `roles/secretmanager.viewer`
- `roles/logging.viewer`
- `roles/policyanalyzer.activityAnalysisViewer`
- `roles/privateca.auditor`
- `roles/certificatemanager.viewer`
- `roles/compute.viewer`

<Callout icon="ℹ️" theme="info">
  ### Note

  For folder or organization scope, grant these roles at the folder or organization level so they inherit to all projects underneath.
</Callout>

### Granular Permissions

All permissions below are **read-only**. The scanner never requires write access to your Google Cloud environment, and never reads secret _values_, only metadata.

#### Required Permissions

Without these, the scan **fails** and no results are produced.

| Permission                                                                                                                                                                                                             | Used for                                                                 | If missing                                                   |
| ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------ | ------------------------------------------------------------ |
| `resourcemanager.projects.get`                                                                                                                                                                                         | Resolving the scanned project and its folder/organization hierarchy      | Scan fails                                                   |
| `resourcemanager.projects.list`, `resourcemanager.folders.list`                                                                                                                                                        | Enumerating projects under a folder/organization (folder/org scope only) | Scan fails                                                   |
| `resourcemanager.projects.getIamPolicy`                                                                                                                                                                                | Reading the project IAM policy — the foundation of identity discovery    | Identities scan fails                                        |
| `secretmanager.secrets.list`                                                                                                                                                                                           | Secrets discovery (Secret Manager)                                       | Secrets scan fails                                           |
| At least one certificate source: `privateca.certificateAuthorities.list` + `privateca.certificates.list`, or `certificatemanager.certs.list`, or `compute.sslCertificates.list` + `compute.regionSslCertificates.list` | Certificate discovery (Private CA / Certificate Manager / Compute SSL)   | Certificates scan fails only if all three sources are denied |

<Callout icon="ℹ️" theme="info">
  ### Note

  When scanning a folder or organization, a permission problem in one project degrades to a per-project warning instead of failing the whole scan.
</Callout>

#### Extended Visibility Permissions

Without these, the scan still **completes**, but with reduced visibility. Missing permissions are reported in the scan's _Access Status_ (visible in scan details).

| Permission                                                                                                                              | What it adds                                                                                   |
| --------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------- |
| `resourcemanager.folders.getIamPolicy`, `resourcemanager.organizations.getIamPolicy`                                                    | Inherited access from folder/organization-level IAM bindings                                   |
| `iam.serviceAccounts.list`, `iam.serviceAccountKeys.list`                                                                               | Service accounts and their keys (key age, stale keys)                                          |
| `iam.serviceAccounts.getIamPolicy`                                                                                                      | Service-account impersonation paths in the Security Graph                                      |
| `iam.denypolicies.list`                                                                                                                 | IAM deny policies — without it the graph may look more permissive than reality                 |
| `iam.roles.get`                                                                                                                         | Custom role definitions — without it custom roles resolve to zero permissions                  |
| `secretmanager.secrets.getIamPolicy`                                                                                                    | Secret-level access bindings                                                                   |
| `secretmanager.versions.list`                                                                                                           | Secret lifecycle metadata: last changed/rotated dates, version counts                          |
| `logging.logEntries.list`                                                                                                               | Last-accessed dates for secrets and last-activity for identities, from Cloud Audit Logs        |
| `policyanalyzer.serviceAccountLastAuthenticationActivities.query`, `policyanalyzer.serviceAccountKeyLastAuthenticationActivities.query` | Service-account and key last-authentication times (requires the project to be billing-enabled) |
| All three certificate sources (whichever were not granted above)                                                                        | Complete certificate coverage across Private CA, Certificate Manager, and Compute SSL          |
| Workspace scope `admin.directory.group.member.readonly` (domain-wide delegation)                                                        | Google Workspace group membership expansion in the Security Graph                              |

### Prerequisites Beyond IAM

Granting the permissions above is not sufficient on its own — the following must also be in place:

- **APIs enabled per scanned project**: Cloud Resource Manager, IAM, Secret Manager, and (per capability) Cloud Logging, Private CA, Certificate Manager, Compute Engine, Policy Analyzer. A disabled API is reported as a warning — granting a role does not fix it.
- **Data Access audit logs**: secret last-accessed dates require a `DATA_READ` audit-log configuration for Secret Manager (or all services) in the project.
- **Workspace groups**: group expansion requires domain-wide delegation configured in the Google Workspace Admin Console, plus a Workspace admin email set in the scanner settings.

## Create a GCP Scanner

1. Log in to the Akeyless Console, and go to **Products > Identity & Secrets Intelligence > Scanners**.
2. Click **New**, and select the scanner type **GCP**, then click **Next**.
3. Define a **Name** for the scanner.
4. Select the **Target** representing the project, folder, or organization to scan, and the **Gateway** that will execute the scans, then click **Next**.
5. Use the **Object Type** drop-down list to select the scanner's scope, and click **Finish**.

## Run a Scan

1. Log in to the Akeyless Console, and go to **Products > Identity & Secrets Intelligence > Scanners**.
2. Click the GCP scanner.
3. Click **Start Scan**.

Once the scan completes, results appear in [Inventory](doc:identity-and-secrets-intelligence#inventory) for review.
