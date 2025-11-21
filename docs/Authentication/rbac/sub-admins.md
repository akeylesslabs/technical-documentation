---
title: Sub-Admins
excerpt: ''
deprecated: false
hidden: false
metadata:
  title: Sub-Admins
  description: ''
  robots: index
next:
  description: ''
---
Our powerful RBAC model allows delegating some of the account owner’s permissions to other users.

While users can be added to the default **admin** role of the account using the pre-defined **admin** role without having to mention what type of access they will have explicitly. you can still segregate the account into multiple different tenants. While only the account owner and users that are part of the admin default role can still navigate between those different tenants. 

As the Akeyless Platform stores all objects (secrets, keys, targets, roles, auth methods, etc.) in a virtual filesystem. It allows organizing everything based on the domain each item belongs to. For example, an organization may have Dev, Operations, and Security departments, each having its own set of secrets, roles, and auth methods.

In such a situation, it would make sense to have a person responsible for every department. For example, 3 users can be designated to rule their own departments: **/dev/director**, **/ops/lead**, and **/security/ciso**.

To grant each one of these users full control over their department, 3 separate roles should be created, for example,**/dev/director**, **/ops/lead**, and **/security/ciso**.

Each role should be associated with the corresponding auth method to grant required permissions. Each user’s power depends on a set of permissions granted to them. There are 5 permission categories:

* Items
* Access Roles
* Auth Methods
* Targets
* Secure Remote Access

It would make sense to grant every leader full access to their departments.**/dev/director** can do any operation inside their folders, such as create new secrets, delete keys, update roles, or set up new auth methods. They can create new, limited users, that can only have a subset (but never a superset) of their own abilities.

**Logs and analytics**

* Each role can be granted “Audit Logs” and “Analytics” permissions. Any path/department does not limit these capabilities.
* Any role with “Audit Logs” permission can view all audit logs with their own Access ID.
* Any role with “Analytics” permission can view reports about their own Access ID.
* Users granted admin permissions can view all logs and see all reports. 

## FAQ

**Do I have to use the same folder structure for every category?**\
No, but we think it makes things easier. Otherwise, it is harder to keep track of roles, auth methods, and their permissions.

**Can a limited user somehow escalate their permissions?**\
No. Even if a user is granted “create role” permissions, they cannot create a role with capabilities that they themselves don’t have.

**Do I have to create “Deny” permission if I don’t want user access to some path?**\
No. By default, a role has no permissions and is not able to do anything. Any permission must be explicit. “Deny” permissions are good for cases where a user has access under a particular path (/dev/ci/\*), but is forbidden from seeing a specific item or sub-path (/dev/ci/jenkins).

**Can I only grant role management permissions to human users?**\
No. Any client (human or machine) can be granted any permission. It is possible to automate role/user management with a limited scope.

**Can a user have different permissions under “Roles” than under “Secrets and Keys”?**\
Yes! It is possible to grant different levels of access to different parts of Akeyless Platform. A user can be able to create and delete secrets, but it doesn’t mean that they can do the same for auth methods.
