---
title: Delete the Association Between a Classic Key and a Target
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
When you delete the association between a classic key and a target (cloud KMS), the key is deleted from the cloud KMS, but remains in the Akeyless KMS. The key might not be deleted immediately from the cloud KMS, according to the cloud KMS deletion policy.

The CLI command to delete the association between a classic key and a target is:

```shell
akeyless delete-assoc-target-item --name <classic key name> --target-name <target name>
```

where:

* **name:** The name of the classic key from which you want to delete a target association.
* **target-name:** The name of the target whose association with the classic key you want to delete.

The full list of options for this command is:

```shell
-n, --name                      *Item name
    --id, --assoc-id             The association id to be deleted. Not required if target name specified
-t, --target-name                The target name with which association will be deleted
    --profile                    Use a specific profile from your akeyless/profiles/ folder
    --username                   Optional username for various authentication flows
    --password                   Optional password for various authentication flows
    --uid-token                  The universal identity token, Required only for universal_identity authentication
-h, --help                       display help information
    --json[=false]               Set output format to JSON
    --no-creds-cleanup[=false]   Do not clean local temporary expired creds
```
