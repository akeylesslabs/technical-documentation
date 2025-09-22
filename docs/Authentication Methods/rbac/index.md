---
title: RBAC
excerpt: Role-based Access Control (RBAC)
deprecated: false
hidden: false
metadata:
  title: Access Roles & RBAC
  description: ''
  robots: index
next:
  description: ''
---
Akeyless Role-based Access Control (RBAC) follows the least privilege principle to limit access rights for machines/human users to the bare minimum of permissions they need to perform their work.

We associate specific clients with a certain Authentication Method to an Access Role to increase operational flexibility. The user can define any number of roles with permissions per each role.

![](https://files.readme.io/54c7a41-RBAC.JPG "RBAC.JPG")

Access Roles can be configured to grant permissions on Secrets & Encryption Keys, Targets, Authentication methods and Access Roles, you can also control user access to audit logs, analytics, Gateways settings and Secure Remote Access (SRA) information.

To set permission for a user to work with any item in the Platform, an appropriate Access Role must be assigned to the Authentication Method that represents this user. By default, users don't have any permissions in Akeyless unless explicitly granted. 

To Associate an [Authentication Methods](doc:access-and-authentication-methods) with a role from the Akeyless [Command Line Interface (CLI)](doc:cli), first run the following command to create an [API Key](doc:api-key):

```shell CLI
akeyless auth-method create api-key --name client1
```

Create a new access role: 

```shell CLI
akeyless create-role --name role1
```

To set all authentication methods associated with a specific role access to all **Items** under **/path/to/folder/** with read, create, and update permissions, use:

```shell CLI
akeyless set-role-rule --role-name role1 --path "/path/to/folder/*" --capability read --capability create --capability update
```

To set the role with access for additional items type like **Targets**, **Auth Methods**, **Access Roles**, or **Secure Remote Access**, you can simply set the `rule-type` inside the command:

```shell Targets
akeyless set-role-rule --role-name role1 --path "/path/to/folder/*" --rule-type target-rule --capability read --capability create --capability update
```
```shell Auth Methods
akeyless set-role-rule --role-name role1 --path "/path/to/folder/*" --rule-type auth-method-rule --capability read --capability create --capability update
```
```shell Access Roles
akeyless set-role-rule --role-name role1 --path "/path/to/folder/*" --rule-type role-rule --capability read --capability create --capability update
```
```shell Secure Remote Access
akeyless set-role-rule --role-name role1 --path "/path/to/folder/*" --rule-type sra-rule --capability allow_access # other options '--capability justify_access_only' '--capability request_access'
```

Despite the fact that users do not have access to items unless granted explicitly, to protect sensitive items from access, you can **deny** all the authentication methods associated with a role to access the relevant item, for example **/path/to/folder/topSecret** (does not include Secure Remote Access):

```shell CLI
akeyless set-role-rule --role-name role1 --path /path/to/folder/topSecret --capability deny
```

Add **client1** to the **role1**, so client1 will be able to access all items under **/path/to/folder/** apart from **/path/to/folder/topSecret**:

```shell CLI
akeyless assoc-role-am --role-name role1 --am-name client1
```

# Permission Types

Akeyless has six main permission types for Items, Access Roles, Auth Methods, and Targets that can be assigned to specific items, folders, or entire accounts. For Secure Remote Access only, there are six permission types.

The built-in admin role has full access to all parts of the accounts.

> 🚧 Warning
>
> It is considered a best practice **not** to use an API key as the authentication method associated with your Admin role. We highly recommend you select one of the other available [Authentication Methods.](doc:access-and-authentication-methods)

## Permissions for Items, Access Roles, Auth Methods, and Targets

The existing permissions for Items, Access Roles, Auth Methods, and Targets are as follows:

* List: Allows a user to list the items available under an authorized path.
* Read: Allows a user to read the items available in an authorized path.
* Create: Allows a user to create new secrets and items in an authorized path.
* Update: Allows a user to update existing secrets and items in an authorized path.
* Delete: Allows a user to delete existing secrets and items in an authorized path.
* Deny: Allows a user to deny any permission to other users in their authorized path.

> 👍 Note
>
> **Permission Hierarchy**
>
> Some Akeyless permissions include others in them. For example, `list` is included under all other permissions, and `deny` has a complete override over any other permission.

### Deny Rule Application and Role Management

Deny rules will be automatically added to a role only when the user creating the role has existing deny restrictions (i.e. non-admin users only). In such cases, all deny rules that apply to the user will also be applied to the newly created role. This is intended to prevent users from creating roles with broader permissions than they are allowed.

After the role is created, it functions independently, and any user with sufficient permissions not affected by those deny rules, can modify or delete the role. Removing a deny role does not automatically remove it from other roles that were affected. If the rule was applied to multiple roles, it must be removed explicitly from each related role by an authorized user for security reasons.

This design ensures that the RBAC system remains resilient against permission elevation, upholding strict access control and enforcement standards.

## Permissions for Secure Remote Access

The existing permissions for Secure Remote Access are as follows:

* Allow Access: Allows a user full access to login to a remote resource.
* Request Access: Allows a user to request access and requires adding a reason for access. Once the request is sent, an admin or approver receives a notification in the Event Center to approve or deny. If approved, the user can then access the remote resource.
* Justify Access Only: Allows a user to access a remote resource only after entering the reason for access.
* Approval Authority: Allows a user to be part of the eligible approvers for Secure Remote Access Requests of the organization in the specified path. This option cannot be selected if “Request Access” is enabled.
* Upload Files: For RDP only. Allows a user to upload local files to a remote Windows machine using a button on the top menu. More information [here](https://docs.akeyless.io/docs/remote-desktop-secure-access#download--upload-files).
* Download Files: For RDP only. Allows a user to download files from a remote Windows machine to their local machine. More information [here](https://docs.akeyless.io/docs/remote-desktop-secure-access#download--upload-files).

# Administrative Rules

With Administrative Rules, you can choose whether users have access only to the resources they own (**Own**) or to all resources (**All**).

The following **Administrative Rules** can be set:

* `Audit Log`

* `Analytics`

* `Gateways`

* `Secure Remote Access`

* `Event Center`

* `Reverse RBAC`

* `Manage Event Forwarders`

* `Usage Reports`

Example:

If **Audit Log** is set to **Own**, the user will see only logs related to themselves. If it is set to **All**, the user will see logs related to all users in the account.

# Access Roles Syntax

In general, you can set an Access Role to a specific item only:

In this example we will create a role that grants `read` permission to `mysecret`, which is located under `/foo` folder:

```shell
akeyless set-role-rule --role-name role1 --path "/foo/mysecret" --capability read
```

To provide access to all secrets with a well-defined prefix: 

In this example, we will create a role that grants `read` permission to all secrets or any items under a folder that starts with `devops-` prefix, which are located under `/foo` folder:

```shell
akeyless set-role-rule --role-name role1 --path "/foo/devops-*" --capability read
```

In addition, a `+` can be used to denote any number of characters bounded within a single path segment:

```shell
akeyless set-role-rule --role-name role1 --path "foo/+/+/bar/*" --capability read
```

 This Access Role will permit reading secrets under those folders path:\
 `foo/any/folder/bar/*`, `foo/other/folder/bar/*`, etc.

# Multiple rules

If you wish to apply multiple rules to your role in one command, you can use a `JSON` file using `-f` or `--file` parameter to the command, that will lead to a JSON file in the following way:

```shell
akeyless set-role-rule --role-name role1 --file-rules path/to/file.json
```

The JSON file structure should be as follows:

```json
{
	"secret/foo": [{
			"rule-type": "item-rule",
			"capabilities": "[read, list]",
			"ttl": "30"
		},
		{
			"rule-type": "role-rule",
			"capabilities": "[read, list]"
		}
	],
	"secret/bar": [{
		"rule-type": "target-rule",
		"capabilities": "[delete, list]"
	}]
}
```

Where the relevant Akeyless paths, e.g `secret/foo` and `secret/bar` correlate with the `--path` parameter, the rule type with the `rule-type` key, and the capabilities with the `capabilities` key that you would attach to a single rule command as described above.

# View As

To verify the settings of your Access Roles, you can use the **Impersonate As** feature inside the Akeyless Console. Admins can validate and explore what kind of access they grant to clients.\
Click on your account logo on the top right corner of your console, and select **Impersonate As**.\
On the dialog, choose from the drop-down menu and existing [Authentication Methods](doc:access-and-authentication-methods). Where needed, provide the relevant [Sub-Claims](doc:sub-claims) as well to validate the level of access the relevant audience has.

# Tutorial

Check out our tutorial video on [Role-based Access Control (RBAC)](https://tutorials.akeyless.io/docs/role-based-access-control-with-api-key-authentication).
