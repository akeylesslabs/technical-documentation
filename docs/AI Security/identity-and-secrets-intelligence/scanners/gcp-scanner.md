---
title: GCP Scanner
excerpt: ' Setup & Required Permissions'
deprecated: false
hidden: false
metadata:
  robots: index
---
# &#x20;Quick Setup

Grant the scanner's service account `roles/browser` and `roles/iam.securityReviewer`, plus per-capability viewer roles: `roles/secretmanager.viewer`, `roles/logging.viewer`, `roles/policyanalyzer.activityAnalysisViewer`, `roles/privateca.auditor`, `roles/certificatemanager.viewer`, `roles/compute.viewer`.

For folder or organization scope, grant these at the folder/org level so they inherit to all projects.

All permissions below are **read-only**. The scanner never requires write access to your GCP environment, and never reads secret _values_ — only metadata.

***

## Must-Have Permissions

Without these, the scan **fails** and no results are produced.

| Permission                                                                                                                                                                                                             | Used for                                                                 | If missing                                                   |
| ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------ | ------------------------------------------------------------ |
| `resourcemanager.projects.get`                                                                                                                                                                                         | Resolving the scanned project and its folder/organization hierarchy      | Scan fails                                                   |
| `resourcemanager.projects.list`, `resourcemanager.folders.list`                                                                                                                                                        | Enumerating projects under a folder/organization (folder/org scope only) | Scan fails                                                   |
| `resourcemanager.projects.getIamPolicy`                                                                                                                                                                                | Reading the project IAM policy — the foundation of identity discovery    | Identities scan fails                                        |
| `secretmanager.secrets.list`                                                                                                                                                                                           | Secrets discovery (Secret Manager)                                       | Secrets scan fails                                           |
| At least one certificate source: `privateca.certificateAuthorities.list` + `privateca.certificates.list`, or `certificatemanager.certs.list`, or `compute.sslCertificates.list` + `compute.regionSslCertificates.list` | Certificate discovery (Private CA / Certificate Manager / Compute SSL)   | Certificates scan fails only if all three sources are denied |

> When scanning a folder or organization, a permission problem in one project degrades to a per-project warning instead of failing the whole scan.

***

## Additional Permissions for a Full Scan

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

***

## Prerequisites Beyond IAM

- **APIs enabled** per scanned project: Cloud Resource Manager, IAM, Secret Manager, and (per capability) Cloud Logging, Private CA, Certificate Manager, Compute Engine, Policy Analyzer. A disabled API is reported as a warning — granting a role does not fix it.
- **Data Access audit logs:** secret _last-accessed_ dates require a `DATA_READ` audit-log configuration for Secret Manager (or all services) in the project.
- **Workspace groups:** group expansion requires domain-wide delegation configured in the Google Workspace Admin Console plus a Workspace admin email in the scanner settings.

***

## Scope Note

Granting roles at a lower scope (project instead of folder/org) narrows visibility the same way as with the other cloud scanners — anything out of scope is simply reported as a gap in the Access Status.
