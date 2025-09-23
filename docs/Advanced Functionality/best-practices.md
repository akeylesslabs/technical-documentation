---
title: Best Practices
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
In this article, we are going to map some of Akeyless's best practices related to both performance and security.

# Glossary

**Superuser** - The user who signed up for Akeyless and owns the account. 

**RBAC** - Akeyless [Role Based  Access Control](doc:rbac).

**CSP IAM** - Cloud Service Provider Identity and Access Management.

**Customer Fragment** - [Zero Knowledge](doc:implement-zero-knowledge) Akeyless unique encryption patented technology. 

**SRA Bastion** - Akeyless [Secure Remote Access Bastion](doc:secure-remote-access-bastion).

# Akeyless Platform

* **Do not run as a superuser** for general purposes. An Akeyless superuser should ideally sign up using an email distribution list for the Administrators team, create a strong password, and then enable Email MFA for it in the Account Settings. The superuser should be used to set up the system initially, particularly for setting up the selected admin users who will be part of your admin role. Those admin users will create the authentication methods so regular users will be able to authenticate. 

* **Avoid API Key Authentication on production** - Due to the secret zero problem and management challenges, [Universal Identity](doc:universal-identity) should be used on production for on-premise environments or any CSP IAM on cloud environments for workloads or automated services, as well as SAML or OIDC for human access.  

* [Authentication Methods](doc:access-and-authentication-methods)  - Shared authentication methods such as SAML, OIDC, LDAP, IAM, JWT, or K8s should be used with sub-claims on role association to avoid mistakes and overriding existing access roles.

* [Access Roles (RBAC)](doc:rbac) - In general, regular users do not have permission to change their Access Role or Authentication method settings. Make sure your Access Roles are not granting regular users permission to view or create neither Access Roles nor Authentication methods. In addition, avoid creating multiple different [Access Roles](doc:rbac) with a single path. Instead, create an access role for multiple paths.

* **Audit & Analytics** - On access roles, it's recommended to let your users view their analytics and logs rather than providing them broader permissions to view your account's entire audit logs and analytics. 

# Items

* **Storing item** - Items location inside Akeyless should not be saved on the default root path, i.e., `/`. The recommended mode is to create those items under the relevant tree folders that describe the exact unit in your organization. This will enable easier and clearer tenant management.

* [SSH certificates](doc:ssh-certificates) - Should **not** be set with `*` on the `principals` field. Instead, this field should be utilized for special use cases where your users need special permissions. In addition, SSH certificates should be used with a `list of allowed users` who will be able to log in using those certificates.

* [Dynamic Secrets](doc:how-to-create-dynamic-secret) - Should be used and set while following the Principle Of Least Privileges (PoLP). Each dynamic secret has its permission profile which will determine your temporary users' access level.\
  E.g., Databases Dynamic secret should be used with the minimum permissions for your users based on the `creation statement`, where you should limit the access to a specific database and table.

```sql
CREATE USER '{{name}}'@'%' IDENTIFIED WITH mysql_native_password BY '{{password}}' PASSWORD EXPIRE INTERVAL 30 DAY;GRANT SELECT ON <DATABASE NAME>.<TABLE_NAME> TO '{{name}}'@'%';
```

* [Rotated Secrets](doc:rotated-secrets) - This should be used as a breakglass admin static credentials, which should automatically rotate strong users' passwords. Primarily for your super users, which their passwords should be rotated automatically.

* [Targets](doc:targets) - To save time during Dynamic and Rotated secrets creation and avoid using your privileged user credentials often, you can create Targets.\
  Those items should not be shared with regular users, while those who need to use the Targets items can only have 'list' permissions.

# System Prerequisites

**Kubernetes Version**

Different components of the Akeyless platform require different versions of Kubernetes, while we recommend you use one that works with all components to allow you to work with the full scope of the platform, the requirements are:

* For the Akeyless native injector: 1.19 or higher

* For Akeyless Secrets Management Authentication and policy segregation: 1.21 or higher

* For Kubernetes External KMS: 1.10 or higher

* For Kubernetes External Secrets Operator or secret store provider: 1.16 or higher
