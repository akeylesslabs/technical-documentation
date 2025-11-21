---
title: Delete a Classic Key
excerpt: ''
deprecated: false
hidden: true
metadata:
  title: ''
  description: ''
  robots: index
next:
  description: ''
---
When you delete a classic key that is associated with a target (cloud KMS), the key is deleted from both the Akeyless KMS and the cloud KMS.

You can specify to delete the key immediately, or only after a configurable number of days. When you specify to delete a classic key immediately, it will be deleted immediately from the Akeyless KMS, but it might not be deleted immediately from the cloud KMS, according to the cloud KMS deletion policy. 

The CLI command to delete a classic key is:

```shell
akeyless delete-item --name <classic key name> --delete-in-days <number of days> --delete-immediately <true|false>
```

where:

* **name:** The name of the classic key to be deleted.
* **version:** The version of the classic key to be deleted. If no value is specified for this option, all versions will be deleted.
* **delete-in-days:** The number of days to wait before deleting the key from the Akeyless KMS. To delete the key immediately, set the value of this option as `-1`.
* **delete-immediately:** Defines if the classic key should be deleted immediately from the Akeyless KMs (`true`), or after the number of days specified by the value of delete-in-days (`false`).

The full list of options for this command is:

```shell
-n, --name                        *Item name
    --version[=-1]                 The specific version you want to delete - 0=last version, -1=entire item with all versions (default)
    --delete-in-days[=7]           The number of days to wait before deleting the item (relevant for keys only)
    --delete-immediately[=false]   When delete-in-days=-1, must be set
    --profile                      Use a specific profile from your akeyless/profiles/ folder
    --username                     Optional username for various authentication flows
    --password                     Optional password for various authentication flows
    --uid-token                    The universal identity token, Required only for universal_identity authentication
-h, --help                         display help information
    --json[=false]                 Set output format to JSON
    --no-creds-cleanup[=false]     Do not clean local temporary expired creds
```
