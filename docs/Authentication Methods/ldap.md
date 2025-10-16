---
title: LDAP
excerpt: Lightweight Directory Access Protocol (LDAP)
deprecated: false
hidden: false
metadata:
  title: LDAP
  description: ''
  robots: index
next:
  description: >-
    Make sure to associate your new Authentication Method with an Access Role to
    grant the relevant permissions within Akeyless
---
The LDAP [Authentication Method](https://docs.akeyless.io/docs/access-and-authentication-methods) uses an existing LDAP server in order to authenticate your users without sharing their credentials directly with Akeyless or any other third party. The [Akeyless Gateway](https://docs.akeyless.io/docs/api-gw) interacts directly with your LDAP server inside your internal network, acting as an internal trusted server, to ensure safe communication.

# Prerequisites

* [Akeyless Gateway](https://docs.akeyless.io/docs/api-gw) with network access to an LDAP server.

* An [Access Role](https://docs.akeyless.io/docs/rbac) with permissions to create an Authentication Method.

* A privileged LDAP User.

# Create an LDAP Authentication Method from the Akeyless Console

1. Log in to the Akeyless Console, go to **Users & Auth Methods > New > LDAP**, and click on **Next →**.
2. On the **Basic Configuration** step define a **Name** for the authentication method, and specify the **Location** as a path to the virtual folder where you want to create the new authentication method, using slash `/` separators. The folder will be created with the authentication method if it does not exist.
3. Define the remaining parameters as follows:

* **Expiration Date:** Select the access expiration date. This parameter is optional. Leave it empty for access to continue without an expiration date.

* **Allowed Client IPs:** Enter a comma-separated list of CIDR blocks from which the client can issue calls to the proxy. By "client," we mean CURL, SDK, etc. This parameter is optional. Leave it empty for unrestricted access.

* **Allowed Trusted Gateway IPs:** Enter a comma-separated list of CIDR blocks. When specified, the Gateway with the IP from this range will be trusted to forward original client IPs (so that they will be visible in the logs).
  This parameter is optional. If empty, the IP of the Gateway will be used in the logs.

* **Audit Log Sub Claims:** Enter a comma-separated list of sub-claims keys to be included in the audit logs.

* **Allowed Client Type**: Specifies which clients can use this Authentication Method, available options:
  * **Web UI**
  * **Mobile App**

* **Require Sub Claim on role association:** select to force [Sub-Claims](https://docs.akeyless.io/docs/sub-claims) during [Role](https://docs.akeyless.io/docs/rbac) association.

* **Unique Identifier:** A unique identifier is usually one of the following keys `email`, `username`, or `UPN`. Identity Providers issue sub-claims containing details that uniquely identify the user whenever a user logs in.
  A sub-claim includes a key holding the unique identifier value you configured and is used to distinguish between different users from within the same organization.

On the **LDAP Configuration** step define the following:

* **Gateway:** An [Akeyless Gateway](https://docs.akeyless.io/docs/api-gw) to create the LDAP configuration.

* **LDAP Server URL:** The LDAP server URL, e.g. `ldap://planetexpress.com:389` or secured server `ldaps://planetexpress.com:636`.

* **Server CA Certificate:** LDAP server CA certificate, requires x509 PEM encoded certificate format, **Relevant** only if secured LDAP server `ldaps` is used.

* **LDAP Bind DN:** Distinguished Name (DN) of object to bind when performing user and group search
  e.g. `cn=admin,dc=planetexpress` ,**Relevant** only if **Enable LDAP Anonymous Search**  is checked.

* **Password for LDAP Bind DN:** Password to perform user search, **Relevant** only if **Enable LDAP Anonymous Search** is NOT checked.

On the **Search Configuration** step define the following:

* **User Base DN:** Base DN to perform user membership search, e.g. `ou=people,dc=planetexpress,dc=com`.

The following **Search Configuration** steps are **Optional**:

* **LDAP User Attribute:** LDAP attribute on user object returned by user authentication, default is `cn`  attribute value. e.g. `uid`.

* **Group Base DN:** Base DN to perform group membership search, e.g. `ou=groups,dc=planetexpress,dc=com`.

* **Go Template for Group Membership query:**  Go template used when constructing the group membership query. The template can access the following context variables: `UserDN, Username`.

* **LDAP Group Attribute:** LDAP attribute to follow on objects returned by `ldap_group_filter` in order to enumerate user group membership, the default is `cn`.

* Click on **Finish**.
