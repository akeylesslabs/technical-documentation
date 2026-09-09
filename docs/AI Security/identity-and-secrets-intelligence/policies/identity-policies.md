---
title: Identity Policies
deprecated: false
hidden: false
metadata:
  robots: index
---
Identity Policies evaluate every identity in your Inventory for privilege scope, credential hygiene, and risky configurations. When an identity matches a policy's condition, it's surfaced as a finding in **Dashboard** and **Inventory**, with a severity that reflects how urgently it needs attention. For an overview of how policies fit into Identity & Secrets Intelligence as a whole, see [Policies](doc:policies).

## Available Identity Policies

Identity & Secrets Intelligence currently ships the following built-in Identity Policies:

| Policy                                           | Severity | What It Flags                                                                                                                                                                  | Applies To                                    |
| ------------------------------------------------ | -------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | --------------------------------------------- |
| **Publicly Accessible Identity**                 | Critical | An identity reachable without IP or principal restrictions                                                                                                                     | AWS, Akeyless, GCP                            |
| **Excessive Access / Least Privilege Violation** | High     | An identity holding more permissions than it needs (for example, more than 50 permissions on AWS/GCP, or more than 20 permissions, 10 roles, or 5 wildcard grants on Akeyless) | AWS, Akeyless, GCP, Azure, GitHub, Kubernetes |
| **Missing Subject Claims or Conditions**         | High     | A trust policy that lacks the subject claims or conditions required for OIDC/SAML federation                                                                                   | AWS, Akeyless, GCP                            |
| **Human Identity Without MFA**                   | High     | A human user account without multi-factor authentication enabled                                                                                                               | AWS, Akeyless                                 |
| **Credentials Not Rotated**                      | High     | Credentials that haven't been rotated in over 90 days                                                                                                                          | AWS, Akeyless, GCP, Azure, GitHub             |
| **Credentials Expired**                          | High     | Credentials that have already expired                                                                                                                                          | Azure, GitHub                                 |
| **GitHub Workflow Default Token Permissions**    | High     | A workflow's `GITHUB_TOKEN` has write access with no release- or tag-based trigger gate                                                                                        | GitHub Actions                                |
| **GitHub Workflow Static Cloud Credentials**     | High     | A workflow authenticates with long-lived cloud credentials instead of OIDC                                                                                                     | GitHub Actions                                |
| **GitHub Workflow Automation Excessive Scope**   | High     | A scheduled automation can merge pull requests or publish packages                                                                                                             | GitHub Actions                                |
| **Namespace-Scoped Wildcard Access**             | Medium   | A Kubernetes RoleBinding that grants wildcard access within a specific namespace                                                                                               | Kubernetes                                    |
| **Credentials Never Expire**                     | Medium   | An identity's credentials have no expiration, or an extremely long one (over 365 days; 90 days for GCP service account keys)                                                   | AWS, Akeyless, GCP, Azure, GitHub             |
| **Inactive Identity**                            | Medium   | An identity marked inactive but still enabled (inactive for more than 90 days)                                                                                                 | AWS, Akeyless, GCP, Azure, GitHub             |
| **Credentials Expiring Soon**                    | Medium   | Credentials that expire within the next 30 days                                                                                                                                | Azure, GitHub                                 |
| **GitHub Workflow Self-Hosted Runner Exposure**  | Medium   | A self-hosted runner workflow accesses secrets or holds write permissions                                                                                                      | GitHub Actions                                |
| **Access Key Unused**                            | Low      | An AWS IAM user with an active access key that hasn't been used in 30 days                                                                                                     | AWS                                           |
| **IAM User Console Credentials Unused**          | Low      | An AWS IAM user whose console password hasn't been used in 30 days                                                                                                             | AWS                                           |

### What's Next

- [Policies](doc:policies)
- [Secret Policies](doc:secret-policies)
- [Certificate Policies](doc:certificate-policies)

###
