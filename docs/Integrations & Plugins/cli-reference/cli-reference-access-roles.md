---
title: CLI Reference - Access Roles
excerpt: ''
deprecated: false
hidden: false
metadata:
  title: ''
  description: ''
  robots: index
next:
  description: ''
---
This section outlines the CLI commands relevant to Access Roles.

General Flags:

`--profile, --token`:  Use a specific profile (located at `$HOME/.akeyless/profiles`) or a temp access token

`--uid-token`: The universal identity token, Required only for universal_identity authentication

`-h, --help`: Display help information

`--json[=false]`: Set output format to JSON

`--jq-expression`: JQ expression to filter result output

`--no-creds-cleanup[=false]`: Do not clean local temporary expired creds

### <p style="color:blue">_assoc-role-am_</p>

Create an association between role and auth method

##### Usage

```shell
akeyless assoc-role-am \
--role-name <Role Name> \
--am-name <Auth Method Name>
```

##### Flags

 `-r, --role-name`: **Required**, The role to associate                  

 `-a, --am-name`: **Required**, The auth method to associate           

 `-s, --sub-claims`: key/val of sub claims, e.g group='admins','developers' 

 `-c, --case-sensitive[=true]`: Treat sub claims as case-sensitive

### <p style="color:blue">_create-role_</p>

Creates a new role

##### Usage

```shell
akeyless create-role name <Role Name>
```

##### Flags

 `-n, --name`: **Required**, Role name                                                                                                                                                               

 `--audit-access`: Allow this role to view audit logs. Currently only 'none', 'own' and 'all' values are supported, allowing associated auth methods to view audit logs produced by the same auth methods. 

 `--analytics-access`: Allow this role to view analytics. Currently only 'none', 'own' and 'all' values are supported, allowing associated auth methods to view reports produced by the same auth methods.     

 `--gw-analytics-access`: Allow this role to view gw analytics. Currently only 'none', 'own' and 'all' values are supported, allowing associated auth methods to view reports produced by the same auth methods.  

 `--sra-reports-access`: Allow this role to view SRA Clusters. Currently only 'none', 'own' and 'all' values are supported.                                                                                      

 `--usage-reports-access`: Allow this role to view Usage reports. Currently only 'none' and 'all' values are supported.

 `--event-center-access`: Allow this role to view Event Center. Currently only 'none', 'own' and 'all' values are supported.

 `--event-forwarders-access`: Allow this role to manage Event Forwarders. Currently only 'none' and 'all' values are supported.

`--reverse-rbac-access`: Allow this role to view Reverse RBAC. Supported values: '`own`', '`all`'.

 `description`: Description of the object

`--delete-protection`: Protection from accidental deletion of this object, [true/false]

### <p style="color:blue">_delete-assoc_</p>

Delete an association between role and auth method

##### Usage

```shell
akeyless delete-assoc --assoc-id <association ID to be deleted>
```

### <p style="color:blue">_delete-role_</p>

Delete a role

##### Usage

```shell
akeyless delete-role --name <Role Name>
```

### <p style="color:blue">_delete-role-rule_</p>

Delete a rule from a role

##### Usage

```shell
akeyelss delete-role-rule \
--role-name <Role Name> \
--path <Role Path>
```

##### Flags

 `-r, --role-name`: **Required**, The role name to be updated

 `-p, --path`: **Required**, The path the rule refers to

 `--rule-type[=item-rule]`: item-rule, role-rule, auth-method-rule, search-rule, reports-rule, gw-reports-rule or sra-reports-rule.  \\nA type of the item for which permissions are deleted. Possible values: item-rule - for Items, target-rule - for Targets, role-rule - for Access Role, auth-method-rule - for Authentication Methods. By default, permissions are deleted only for Items

### <p style="color:blue">_delete-roles_</p>

Delete multiple roles from a given path

##### Usage

```shell
akeyless delete-roles --path <Path/to/roles>
```

### <p style="color:blue">_describe-permissions_</p>

See which authentication methods have access to a particular object

##### Usage

```shell
akeyless describe-permissions \
--path <Path/to/object> \
--type <Type of object (item, am, role, target)>
```

### <p style="color:blue">_describe-sub-claims_</p>

Get the sub-claims associated with the provided token or authentication profile

### <p style="color:blue">_describe-role-am-assoc_</p>

Describe role association details

##### Usage

```shell
akeyless describe-role-am-assoc \
--assoc-id <association-id>
```

### <p style="color:blue">_get-role_</p>

Get role details

##### Usage

```shell
akeyless get-role -n <Role Name>
```

### <p style="color:blue">_list-roles_</p>

List of all roles in the account

##### Flags

 `filter`: Filter by role name or part of it 

 `--pagination-token`: Next page reference

### <p style="color:blue">_request-access_</p>

Request a temporary access for an item, supporting Static Secret, and Targets

##### Usage

```shell
akeyless request-access \
--name <Item Name> \
--type <item type> \
--capability <read, update, delete>
```

##### Flags

 `-n, --name`: **Required**, Name of the item to which access is requested for                                              

 `--type`: **Required**, The type of item to which access is requested. The supported types are: [StaticSecret, Target] 

 `-c, --capability`: **Required**, List of the required capabilities, options: [read, update, delete]                             

 `--comment`: Optional, comment about the request.

### <p style="color:blue">_reverse-rbac_</p>

See which authentication methods have access to a particular object

##### Usage

```shell
akeyless reverse-rbac \
--path <path to an object> \
--type <object type>
```

##### Flags

`-p, --path`: **Required**, Path to an object

`-t, --type`: **Required**, Type of object (item, am, role, target)

### <p style="color:blue">_set-role-rule_</p>

Set a rule to a role

##### Usage

```shell
akeyless set-role-rule \
--role-name <Role Name> \
--path <Role Path> \
--rule-type <item-rule, target-rule, role-rule, auth-method-rule> \
--capability <Permission>
```

##### Flags

  `-r, --role-name`: **Required**, The role name to be updated

  `-p, --path`: **(Mandatory if `-f, file` is not given)** The path the rule refers to

  `-c, --capability`: **(Mandatory if `-f, file` is not given)** List of the approved/denied capabilities in the path options: [read, create, update, delete, list, deny]

  `rule-type[=item-rule]`: item-rule, target-rule, role-rule, auth-method-rule.  \\nA type of the item for which permissions are defined. Possible values: item-rule - for Items, target-rule - for Targets, role-rule - for Access Roles, auth-method-rule - for Authentication Methods. By default, permissions are set only for Items.

  `--ttl`: The time (in minutes) until the rule expires. If not used the rule will apply until manually removed

  `-f, --file`: Path to a JSON file containing the multiple rules as described [here](https://docs.akeyless.io/docs/rbac#multiple-rules). This  replaces the `capability`, `path` and `rule-type` 

### <p style="color:blue">_update-assoc_</p>

Update the sub-claims of an association between the role and the auth method.

##### Usage

```shell
akeyless update-assoc --assoc-id <association ID to be updated>
```

##### Flags

 `-a, --assoc-id`: **Required**, The association id to be updated   

 `-s, --sub-claims`: key/val of sub claims, e.g group=admins,developers 

 `-c, --case-sensitive[=true]`: Treat sub claims as case-sensitive                 

### <p style="color:blue">_update-role_</p>

Update role details

##### Usage

```shell
akeyless update-role -n <Role name> \
--new-name <New role name>
```

##### Flags

 `-n, --name`: **Required**, Role name.                                                                                                                                                              

 `--new-name`: New role name.                                                                                                                                                                          

 `--audit-access`: Allow this role to view audit logs. Currently only 'none', 'own' and 'all' values are supported, allowing associated auth methods to view audit logs produced by the same auth methods. 

 `--analytics-access`: Allow this role to view analytics. Currently only 'none', 'own' and 'all' values are supported, allowing associated auth methods to view reports produced by the same auth methods.     

 `--gw-analytics-access`: Allow this role to view gw analytics. Currently only 'none', 'own' and 'all' values are supported, allowing associated auth methods to view reports produced by the same auth methods.  

 `--sra-reports-access`: Allow this role to view SRA Clusters. Currently only 'none', 'own' and 'all' values are supported.                                                                                      

 `--usage-reports-access`: Allow this role to view Usage reports. Currently only 'none' and 'all' values are supported.                                                                                            

 `--event-center-access`: Allow this role to view Event Center. Currently only 'none', 'own' and 'all' values are supported.

 `--event-forwarders-access`: Allow this role to manage Event Forwarders. Currently only 'none' and 'all' values are supported.

`--reverse-rbac-access`: Allow this role to view Reverse RBAC. Supported values: '`own`', '`all`'.

 `--description`: Description of the object

`--delete-protection`: Protection from accidental deletion of this object, [true/false]