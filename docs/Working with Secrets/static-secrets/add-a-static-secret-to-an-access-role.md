---
title: Add a Static Secret to an Access Role
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
      slug: retrievestatic
      title: Retrieve and view static secrets
---
Access roles provide clients with permission to work with secrets. When you add a secret to a role, you can specify exactly which **CRUD** (Create, Read, Update, and Delete) operations clients can perform for that secret.

> 📘 Info
>
> By default, the account owner has privilege permissions in Akeyless. Managing users' access roles and permissions can be done using Akeyless Platform [Authentication Methods](https://docs.akeyless.io/docs/access-and-authentication-methods) with [Access Roles](https://docs.akeyless.io/docs/rbac) to grant users the minimum permissions they need.

# Add a Static Secret to a Role from the Akeyless CLI

Let’s add a static secret to an existing role using the Akeyless CLI. If you’d prefer, see how to do this from the [Akeyless Console](doc:add-a-static-secret-to-an-access-role#add-a-static-secret-to-a-role-from-the-akeyless-console) instead.

The CLI command to add a secret to a role is:

```shell Akeyless CLI
akeyless set-role-rule \
  --role-name <role name> \
  --path <secret name with path> \
  --capability <read|create|update|delete|list|deny> \
  --rule-type item-rule
```

where:

* `--role-name`: The name of the role to which to add the static secret.

* `--path`: The full path to the static secret.

* `--capability`: A CRUD operation clients associated with the role can perform for the secret. Each `capability` argument can include a single permission, either `create`, `read`, `update`, `delete`, `list`, or `deny`. Use multiple `capability` arguments to assign multiple permissions.

* `--rule type`: `item-rule`.

For example, to add the **AdminCredentials** secret in the **Admin** folder to the **SystemAdmin** access role, also in the **Admin** folder, with **Read** and **List** permissions, type:

```shell Shell
akeyless set-role-rule \
  --role-name /Admin/SystemAdmin \
  --path /Admin/AdminCredentials \
  --capability read \
  --capability list \
  --rule-type item-rule
```

The response should be like this:

```shell
$ The requested rule was successfully set to the role /Admin/SystemAdmin
```

You can find the complete list of parameters for this command in the [CLI Reference - Access Roles](https://docs.akeyless.io/docs/cli-reference-access-roles) section.

# Add a Static Secret to a Role from the Akeyless Console

Let’s add a static secret to a role from the Akeyless Console. If you’d prefer, see how to do this from the [Akeyless CLI](doc:add-a-static-secret-to-an-access-role#add-a-static-secret-to-a-role-from-the-akeyless-cli) instead.

1. Log in to the Akeyless Console and go to **Access Roles**.

2. Select the role to which you want to add the secret.

3. Select the **Items**s tab, then select **Add**.

4. In the **Add Rule for Items** dialog box, in the **Allow access to the following path*** field, enter the full path to the static secret.

5. From the **Allow the following actions** options, select the **CRUD** operation(s) the client associated with the role that can perform for the secret.

> 👍 Note
>
> **Deny** overrides all other operations.

6. Click **Add**.
