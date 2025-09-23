---
title: Bulk Operations
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
## Delete items

This command deletes an entire items folder with its contents  
The user running the command must have `Get`, `List`, and `Delete` permissions on the designated path and recursively on each item inside it.

Only items visible to the user making the action will be deleted. However, the operation will fail if the user has only `Get/List` (meaning they are visible to him) and not `Delete` on some of the items inside the path.

> 🚧 Warning
> 
> If the designated folder contains one or more items of type `AES` or `RSA` keys the command will fail. To delete the folder first delete or move any `AES` or `RSA` keys inside it.

Example prerequisite - `/folder/` is created with 2 secrets and 1 key:

```shell
$ akeyless create-secret -n /folder/sec1 -v val
A new secret named /folder/sec1 was successfully created

$ akeyless create-secret -n /folder/sec2 -v val
A new secret named /folder/sec2 was successfully created

$ akeyless list-items --path /folder
{
   "items": [
      {
         "item_name": "/folder/sec1",
         "item_type": "STATIC_SECRET",
         ...
         ...
         ...
      },
      {
         "item_name": "/folder/sec2",
         "item_type": "STATIC_SECRET",
         ...
         ...
         ...
      }
   ],
   ...
   ...
}
```

Example 1 - Deleting items in `/folder`:

```shell
$ akeyless delete-items --path /folder
Item(s) deleted successfully from /folder

$ akeyless list-items --path /folder
{
   "items": null,
   "folders": null,
   "next_page": ""
}
```

Example 2 - In case an `AES` key is inside the designated folder, deleting the folder `/folder` fails on a `403`:

```shell
$ akeyless create-dfc-key -n /folder/sub-aes-key --alg AES256GCM
=====================
Encryption Key Fragement #1 created succsessfully in 17 milliseconds
Encryption Key Fragement #2 created succsessfully in 18 milliseconds
=====================
A new AES256GCM key named /folder/sub-aes-key was successfully created

$ akeyless list-items --path /folder
{
   "items": [
      {
         "item_name": "/folder/sec1",
         "item_type": "STATIC_SECRET",
         ...
         ...
         ...
      },
      {
         "item_name": "/folder/sec2",
         "item_type": "STATIC_SECRET",
         ...
         ...
         ...
      },
      {
         "item_name": "/folder/sub-aes-key",
         "item_type": "AES256GCM",
         ...
         ...
         ...
      }
   ],
   ...
   ...
}


$ akeyless delete-items --path /folder
Failed to delete items from path /folder. Error: Desc: Failed to delete items in path. Status 403 Forbidden, Error: ForbiddenTypesDeletion. Message: account id: <account id>, access id: <access id>. Items list include one or more items that cannot be deleted in a bulk operation: [AES128GCM AES256GCM AES128SIV AES256SIV RSA1024 RSA2048]. Either delete those items manually or move them to proceed.
```

## Delete Auth Methods

This command deletes an entire Auth Methods folder with its contents  
The user running the command must have `Get`, `List`, and `Delete` permissions on the designated path and recursively on each Auth Method inside it.

Only Auth Methods visible to the user making the action will be deleted. However, the operation will fail if the user has only `Get/List` (meaning they are visible to him) and not `Delete` on some of the Auth Methods inside the path.

Examples of prerequisites -  `/folder/` is created with two Auth Methods:

```shell
$ akeyless create-auth-method -n /folder/am1
Auth Method /folder/am1 successfully created
- Access ID: p-vhr2********
- Access Key: 7QeCpbr********************************************

$ akeyless create-auth-method-universal-identity -n /folder/amUID
Auth Method /folder/amUID successfully created
- Access ID: p-35ds********


$ akeyless list-auth-methods
{
   "auth_methods": [
      {
         "auth_method_name": "folder/am1",
         ...
         ...
         "access_info": {
            ...
            ...
            "rules_type": "api_key",
            "api_key_access_rules": {
                ...
                ...
            },
            ...
            ...
         },
         ...
         ...
      },
      {
         "auth_method_name": "folder/amUID",
         ...
         ...
         "access_info": {
            ...
            ...
            "rules_type": "universal_identity",
            ...
            ...
         },
         ...
         ...
      }
   ],
   ...
}
```

Deleting Auth Methods in `/folder`:

```shell
$ akeyless delete-auth-methods --path /folder
Auth Method(s) deleted successfully from /folder
```

## Delete Roles

This command deletes an entire Roles folder with its contents  
The user running the command must have `Get`, `List`, and `Delete` permissions on the designated path and recursively on each role inside it.

Only Roles visible to the user making the action will be deleted. However, the operation will fail if the user has only `Get/List` (meaning they are visible to him) and not Delete on some of the roles inside the path.

Examples prerequisites - `/folder/` is created with two Roles:

```shell
$ akeyless create-role -n /folder/role1
A new role named /folder/role1 was successfully created

$ akeyless create-role -n /folder/role2
A new role named /folder/role2 was successfully created

$ akeyless list-roles
{
   "roles": [
      {
         "role_name": "folder/role1",
         ...
         ...
      },
      {
         "role_name": "folder/role2",
         ...
         ...
      }
   ],
   ...
}
```

Deleting roles in `/folder`:

```shell
$ akeyless delete-roles --path /folder
Role(s) deleted successfully from /folder
```

## Move Objects

The move-objects flow can move multiple items, Auth Methods, or Roles from a specific folder to a different one or similarly rename a folder.  
The user running the command must have `Get`, `List`, and `Update` permissions on the designated source path and recursively on each role inside and on the target path.

Only objects visible to the user making the action will be moved. However, the operation will fail if the user has only `Get/List` (meaning they are visible to him) and not `Update` on some of the objects inside the source path.

In the case of a duplicate as a result of running the operation, the operation will fail on a `409`.

For example the CLI command use: 

- `objects-type` - The object type you like to move ( `item/auth_method/target/role` ), the default is `item`
- `source` - Path to the folder to move
- `target` - Path to the new/existing folder 

Examples of prerequisites - `/folder/src` is created with 2 items:

```shell
$ akeyless create-secret --name /folder/src/sec1 -value val
A new secret named /folder/src/sec1 was successfully created

$ akeyless create-secret --name /folder/src/sec2 -value val
A new secret named /folder/src/sec2 was successfully created
```

Example 1 - Renaming `/folder/src` to `/folder/tgt`:

```shell
$ akeyless move-objects --source /folder/src --target /folder/tgt
Object(s) moved successfully from /folder/src to /folder/tgt
```

Example 2 - Moving `/folder/src` to `/folder/tgt` with preexisting items in `/folder/tgt`:

```shell
$ akeyless create-secret -n /folder/tgt/sec3 -v val
A new secret named /folder/tgt/sec3 was successfully created
$ akeyless create-secret -n /folder/tgt/sec4 -v val
A new secret named /folder/tgt/sec4 was successfully created

$ akeyless list-items --path /folder/
{
   "items": null,
   "folders": [
      "/folder/src/",
      "/folder/tgt/"
   ],
   ...
}

$ akeyless list-items --path /folder/src
{
   "items": [
      {
         "item_name": "/folder/src/sec1",
         "item_type": "STATIC_SECRET",
         ...
         ...
      },
      {
         "item_name": "/folder/src/sec2",
         "item_type": "STATIC_SECRET",
         ...
         ...
      }
   ],
   "folders": null,
   ...
}

$ akeyless list-items --path /folder/tgt
{
   "items": [
      {
         "item_name": "/folder/tgt/sec3",
         "item_type": "STATIC_SECRET",
         ...
         ...
      },
      {
         "item_name": "/folder/tgt/sec4",
         "item_type": "STATIC_SECRET",
         ...
         ...
      }
   ],
   "folders": null,
   ...
}
```

After running the `move-objects` command:

```shell
$ akeyless move-objects --source /folder/src --target /folder/tgt
Object(s) moved successfully from /folder/src to /folder/tgt
$ akeyless list-items --path /folder/
{
   "items": null,
   "folders": [
      "/folder/tgt/"
   ],
   ...
}

$ akeyless list-items --path /folder/src
{
   "items": null,
   "folders": null,
   "next_page": ""
}

$ akeyless list-items --path /folder/tgt
{
   "items": [
      {
         "item_name": "/folder/tgt/sec1",
         "item_type": "STATIC_SECRET",
         ...
         ...
      },
      {
         "item_name": "/folder/tgt/sec2",
         "item_type": "STATIC_SECRET",
         ...
         ...
      },
      {
         "item_name": "/folder/tgt/sec3",
         "item_type": "STATIC_SECRET",
         ...
         ...
      },
      {
         "item_name": "/folder/tgt/sec4",
         "item_type": "STATIC_SECRET",
         ...
         ...
      }
   ],
   "folders": null,
   ...
}
```