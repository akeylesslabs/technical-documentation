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
You can associate a classic key with a [target](https://docs.akeyless.io/docs/targets) (cloud KMS) when you [create the key](https://docs.akeyless.io/docs/create-a-classic-key), or add this association at any time. When you associate a classic key with a target, you share the key with the cloud KMS, from where it can be used in the same way as any key created by the cloud provider. Akeyless remains responsible for managing the key lifecycle by providing secure storage, as well as full role-based access control, recording of key activities, and logging.

The CLI command to associate a classic key with a target is:

```shell
akeyless assoc-target-item --target-name <target-name> --name <classic key name>
```

where:

* **target-name:** The name of the target you want to associate with the classic key.
* **name:** The name of the classic key you want to share with the specified target.

The full list of options for this command is:

```shell
-t, --target-name               *The target to associate
  -n, --name                      *The item to associate
      --vault-name                 Name of the vault used. (Relevant only for Classic Key and target association. Required for azure targets)
      --key-operations             A list of allowed operations for the key. (Relevant only for Classic Key and target association. Required for azure targets)
      --project-id                 Project id of the GCP KMS. (Relevant only for Classic Key and target association. Required for gcp targets)
      --location-id                Location id of the GCP KMS. (Relevant only for Classic Key and target association. Required for gcp targets)
      --keyring-name               Keyring name of the GCP KMS. (Relevant only for Classic Key and target association. Required for gcp targets)
      --purpose                    Purpose if the key in GCP KMS. (Relevant only for Classic Key and target association. Required for gcp targets)
      --kms-algorithm              Algorithm of the key in GCP KMS. (Relevant only for Classic Key and target association, Required for gcp targets)
      --tenant-secret-type         The tenant secret type [Data/SearchIndex/Analytics]. (Relevant only for Classic Key and target association. Required for salesforce targets)
      --multi-region[=false]       Set to 'true' to create a multi-region managed key. (Relevant only for Classic Key AWS targets)
      --regions                    The list of regions in which to create a copy of the key. (Relevant only for Classic Key AWS targets). To specify multiple regions use argument multiple times: --regions us-east-1 --regions us-west-1
      --profile, --token           Use a specific profile (located at $HOME/.akeyless/profiles) or a temp access token
      --uid-token                  The universal identity token, Required only for universal_identity authentication
  -h, --help                       display help information
      --json[=false]               Set output format to JSON
      --no-creds-cleanup[=false]   Do not clean local temporary expired creds
```

# Shared Keys on a Cloud KMS

When you associate a classic key with a cloud KMS, you will find a new customer-managed key on the cloud KMS. The key alias is built as `managed-by-<account-id>-<item-id>`, as shown in the following example:

<Image className="border" width="100%" border={true} src="https://files.readme.io/5ffc31d-image-20210518-114015.png" />
