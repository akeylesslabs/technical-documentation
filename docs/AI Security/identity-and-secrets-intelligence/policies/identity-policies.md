---
title: Identity Policies
deprecated: false
hidden: false
metadata:
  robots: index
---
Over-privileged and poorly governed identities are the connective tissue behind most lateral-movement attacks. Identity Policies encode least-privilege and credential-hygiene best practices across human, agents, machine, and cloud identities, so identity risk surfaces in Inventory the same consistent way secret risk does.

## Available Identity Policies

Identity & Secrets Intelligence currently ships the following built-in Identity Policies:

| Policy                                           | Severity | What It Flags                                                                                                                                                                  |
| ------------------------------------------------ | -------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Publicly Accessible Identity**                 | Critical | An identity reachable without IP or principal restrictions                                                                                                                     |
| **Excessive Access / Least Privilege Violation** | High     | An identity holding more permissions than it needs (for example, more than 50 permissions on AWS/GCP, or more than 20 permissions, 10 roles, or 5 wildcard grants on Akeyless) |
| **Missing Subject Claims or Conditions**         | High     | A trust policy that lacks the subject claims or conditions required for OIDC/SAML federation                                                                                   |
| **Human Identity Without MFA**                   | High     | A human user account without multi-factor authentication enabled                                                                                                               |
| **Credentials Not Rotated**                      | High     | Credentials that haven't been rotated in over 90 days                                                                                                                          |
| **Credentials Expired**                          | High     | Credentials that have already expired                                                                                                                                          |
| **GitHub Workflow Default Token Permissions**    | High     | A workflow's `GITHUB_TOKEN` has write access with no release- or tag-based trigger gate                                                                                        |
| **GitHub Workflow Static Cloud Credentials**     | High     | A workflow authenticates with long-lived cloud credentials instead of OIDC                                                                                                     |
| **GitHub Workflow Automation Excessive Scope**   | High     | A scheduled automation can merge pull requests or publish packages                                                                                                             |
| **Namespace-Scoped Wildcard Access**             | Medium   | A Kubernetes RoleBinding that grants wildcard access within a specific namespace                                                                                               |
| **Credentials Never Expire**                     | Medium   | An identity's credentials have no expiration, or an extremely long one (over 365 days; 90 days for GCP service account keys)                                                   |
| **Inactive Identity**                            | Medium   | An identity marked inactive but still enabled (inactive for more than 90 days)                                                                                                 |
| **Credentials Expiring Soon**                    | Medium   | Credentials that expire within the next 30 days                                                                                                                                |
| **GitHub Workflow Self-Hosted Runner Exposure**  | Medium   | A self-hosted runner workflow accesses secrets or holds write permissions                                                                                                      |
| **Access Key Unused**                            | Low      | An AWS IAM user with an active access key that hasn't been used in 30 days                                                                                                     |
| **IAM User Console Credentials Unused**          | Low      | An AWS IAM user whose console password hasn't been used in 30 days                                                                                                             |

### What's Next

- [Policies](doc:policies)
- [Secret Policies](doc:secret-policies)
- [Certificate Policies](doc:certificate-policies)

###
