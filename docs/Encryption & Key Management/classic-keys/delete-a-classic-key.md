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
[block:code]
{
  "codes": [
    {
      "code": "akeyless delete-item --name <classic key name> --delete-in-days <number of days> --delete-immediately <true|false>",
      "language": "shell"
    }
  ]
}
[/block]
where:

- **name:** The name of the classic key to be deleted.
- **version:** The version of the classic key to be deleted. If no value is specified for this option, all versions will be deleted.
- **delete-in-days:** The number of days to wait before deleting the key from the Akeyless KMS. To delete the key immediately, set the value of this option as `-1`.
- **delete-immediately:** Defines if the classic key should be deleted immediately from the Akeyless KMs (`true`), or after the number of days specified by the value of delete-in-days (`false`).

The full list of options for this command is:
[block:code]
{
  "codes": [
    {
      "code": "-n, --name                        *Item name\n    --version[=-1]                 The specific version you want to delete - 0=last version, -1=entire item with all versions (default)\n    --delete-in-days[=7]           The number of days to wait before deleting the item (relevant for keys only)\n    --delete-immediately[=false]   When delete-in-days=-1, must be set\n    --profile                      Use a specific profile from your akeyless/profiles/ folder\n    --username                     Optional username for various authentication flows\n    --password                     Optional password for various authentication flows\n    --uid-token                    The universal identity token, Required only for universal_identity authentication\n-h, --help                         display help information\n    --json[=false]                 Set output format to JSON\n    --no-creds-cleanup[=false]     Do not clean local temporary expired creds",
      "language": "shell"
    }
  ]
}
[/block]