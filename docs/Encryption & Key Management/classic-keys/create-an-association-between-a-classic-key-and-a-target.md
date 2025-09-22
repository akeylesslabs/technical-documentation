---
title: Associate a Classic Key and a Target
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
You can associate a classic key with a [target](doc:targets) (cloud KMS) when you [create the key](doc:create-a-classic-key), or add this association at any time. When you associate a classic key with a target, you share the key with the cloud KMS, from where it can be used in the same way as any key created by the cloud provider. Akeyless remains responsible for managing the key lifecycle by providing secure storage, as well as full role-based access control, recording of key activities, and logging.

The CLI command to associate a classic key with a target is:
[block:code]
{
  "codes": [
    {
      "code": "akeyless assoc-target-item --target-name <target-name> --name <classic key name>",
      "language": "shell"
    }
  ]
}
[/block]
where:
- **target-name: **The name of the target you want to associate with the classic key.
- **name:** The name of the classic key you want to share with the specified target.

The full list of options for this command is:
[block:code]
{
  "codes": [
    {
      "code": "  -t, --target-name               *The target to associate\n  -n, --name                      *The item to associate\n      --vault-name                 Name of the vault used. (Relevant only for Classic Key and target association. Required for azure targets)\n      --key-operations             A list of allowed operations for the key. (Relevant only for Classic Key and target association. Required for azure targets)\n      --project-id                 Project id of the GCP KMS. (Relevant only for Classic Key and target association. Required for gcp targets)\n      --location-id                Location id of the GCP KMS. (Relevant only for Classic Key and target association. Required for gcp targets)\n      --keyring-name               Keyring name of the GCP KMS. (Relevant only for Classic Key and target association. Required for gcp targets)\n      --purpose                    Purpose if the key in GCP KMS. (Relevant only for Classic Key and target association. Required for gcp targets)\n      --kms-algorithm              Algorithm of the key in GCP KMS. (Relevant only for Classic Key and target association, Required for gcp targets)\n      --tenant-secret-type         The tenant secret type [Data/SearchIndex/Analytics]. (Relevant only for Classic Key and target association. Required for salesforce targets)\n      --multi-region[=false]       Set to 'true' to create a multi-region managed key. (Relevant only for Classic Key AWS targets)\n      --regions                    The list of regions in which to create a copy of the key. (Relevant only for Classic Key AWS targets). To specify multiple regions use argument multiple times: --regions us-east-1 --regions us-west-1\n      --profile, --token           Use a specific profile (located at $HOME/.akeyless/profiles) or a temp access token\n      --uid-token                  The universal identity token, Required only for universal_identity authentication\n  -h, --help                       display help information\n      --json[=false]               Set output format to JSON\n      --no-creds-cleanup[=false]   Do not clean local temporary expired creds",
      "language": "shell"
    }
  ]
}
[/block]
# Shared Keys on a Cloud KMS

When you associate a classic key with a cloud KMS, you will find a new customer-managed key on the cloud KMS. The key alias is built as `managed-by-<account-id>-<item-id>`, as shown in the following example:
[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/5ffc31d-image-20210518-114015.png",
        "image-20210518-114015.png",
        891,
        290,
        "#f0f3f4"
      ],
      "border": true,
      "sizing": "full"
    }
  ]
}
[/block]