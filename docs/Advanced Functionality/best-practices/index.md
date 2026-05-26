---
title: best-practices
excerpt: ''
deprecated: false
hidden: false
metadata:
  title: ''
  description: ''
  robots: index
next:
  description: ''
  pages:
    - type: basic
      slug: gateway-best-practices
      title: Gateway Best Practices
    - type: basic
      slug: sra-bastion-best-practices
      title: SRA Bastion Best Practices
    - type: basic
      slug: web-access-bastion-best-practices
      title: Web Access Bastion Best Practices
---
For Gateway-related guidance, see [Gateway Best Practices](https://docs.akeyless.io/docs/gateway-best-practices).

In this article, we are going to map some of Akeyless's best practices related to both performance and security.

## Glossary

**Superuser** - The user who signed up for Akeyless and owns the account.

**RBAC** - Akeyless [Role-Based Access Control](https://docs.akeyless.io/docs/rbac).

**CSP IAM** - Cloud Service Provider Identity and Access Management.

**Customer Fragment** - [Zero Knowledge](https://docs.akeyless.io/docs/gateway-zero-knowledge) Akeyless unique encryption patented technology.

**SRA Bastion** - Akeyless [Remote Access on Kubernetes](https://docs.akeyless.io/docs/sra-setup-k8s).

## Akeyless Platform

* **Do not run as a superuser** for general purposes. An Akeyless superuser should ideally sign up using an email distribution list for the Administrators team, create a strong password, and then enable Email MFA for it in the Account Settings. The superuser should be used to set up the system initially, particularly for setting up the selected admin users who will be part of your admin role. Those admin users will create authentication methods so regular users can authenticate.

* **Avoid API Key Authentication on production** - Due to the secret zero problem and management challenges, [Universal Identity](https://docs.akeyless.io/docs/auth-with-universal-identity) should be used on production for on-premise environments or any CSP IAM on cloud environments for workloads or automated services, as well as SAML or OIDC for human access.  

* [Authentication Methods](https://docs.akeyless.io/docs/access-and-authentication-methods) - Shared authentication methods such as SAML, OIDC, LDAP, IAM, JWT, or Kubernetes should be used with sub-claims on role association to avoid mistakes and overriding existing Access Roles.

* [Access Roles (RBAC)](https://docs.akeyless.io/docs/rbac) - In general, regular users do not have permission to change their Access Role or Authentication method settings. Make sure your Access Roles are not granting regular users permission to view or create neither Access Roles nor Authentication methods. In addition, avoid creating multiple different [Access Roles](https://docs.akeyless.io/docs/rbac) with a single path. Instead, create an access role for multiple paths.

* **Audit & Analytics** - On Access Roles, it's recommended to let your users view their analytics and logs rather than providing them broader permissions to view your account's entire Audit Logs and analytics.

## Items

* **Storing item** - Items location inside Akeyless should not be saved on the default root path (`/`). The recommended mode is to create those items under the relevant tree folders that describe the exact unit in your organization. This will enable easier and clearer tenant management.

* [SSH certificates](https://docs.akeyless.io/docs/sra-ssh-certificates) - Should **not** be set with `*` on the `principals` field. Instead, this field should be used for special use cases where your users need special permissions. In addition, SSH certificates should be used with a `list of allowed users` who can log in using those certificates.

* [Dynamic Secrets](https://docs.akeyless.io/docs/how-to-create-dynamic-secret) - Should be used and set while following the Principle Of Least Privileges (PoLP). Each Dynamic Secret has its permission profile which will determine your temporary users' access level. For example, a database's Dynamic Secret should be used with the minimum permissions for your users based on the `creation statement`, where you should limit the access to a specific database and table.

```sql
CREATE USER '{{name}}'@'%' IDENTIFIED WITH mysql_native_password BY '{{password}}' PASSWORD EXPIRE INTERVAL 30 DAY;GRANT SELECT ON <DATABASE NAME>.<TABLE_NAME> TO '{{name}}'@'%';
```

* [Rotated Secrets](https://docs.akeyless.io/docs/rotated-secrets) - These should be used as a break-glass admin static credentials, which should automatically rotate strong users' passwords. Primarily for your superusers, which their passwords should be rotated automatically.

* [Targets](https://docs.akeyless.io/docs/targets) - To save time during Dynamic and Rotated Secrets creation and avoid using your privileged user credentials often, you can create Targets. Those items should not be shared with regular users, while those who need to use the Targets items can only have 'list' permissions.

## System Prerequisites: Kubernetes Versioning

Different components of the Akeyless Platform require different versions of Kubernetes, while we recommend you use one that works with all components to allow you to work with the full scope of the platform, the requirements are:

* For the Akeyless native injector: 1.19 or higher

* For Akeyless Secrets Management Authentication and policy isolation: 1.21 or higher

* For Kubernetes External KMS: 1.10 or higher

* For Kubernetes External Secrets Operator: 1.19 or higher

* For Kubernetes Secrets Store CSI Provider: 1.16 or higher
