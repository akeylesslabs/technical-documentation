---
title: Groups
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
Groups enable administrators to manage and reuse [Authentication Methods](doc:access-and-authentication-methods) more easily by associating them to an Akelyess  [OIDC Application](doc:oidc-app-provider) as a Group rather than manually associating multiple individual Authentication Methods.

# Creating a Group in the CLI

To create a group, use the following command:

```shell
akeyless create-group \
--name <New Group Name> \
--group-alias <Group Alias> \
--user-assignment <Auth Method List>
```

Where:

`name`: A unique name for the Group. The name can include the path to the virtual folder in which you want to create the new Group, using the slash `/` separators. If the folder does not exist, it will be created together with the Group.

`group-alias`: A short name for the Group. The alias cannot contain the special characters `/`, `.`, or `*` .

`user-assignment`: A JSON string defining a list of `access-ids` and `sub-claims`. For example `[{"access_id":"p-123456", "sub_claims":{"email":["user@example.com"]}}]`

`user-assignment-file`: Instead of a string, users can add this flag in order to pass a JSON file, using the same formatting, with a path to the file.