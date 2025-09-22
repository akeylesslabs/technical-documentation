---
title: Key Rotation
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
# Introduction

Key rotation is the process in which a new version of an encryption key is created. The key fragment instances and split level remain the same throughout the versions, as well as the customer fragment associated with it (if any).  
There are some constraints when rotating a key:

- For **DFC™**, only **AES** keys can be rotated.
- Only **Enabled** keys can be rotated.

A key can be set to automatically rotate every 7-365 days.  
When rotating a key, the last version of it will be used for **Encryption** and **Decryption** operations, previous versions can still be used for **Decryption** operations done by them.

## Why would I want to rotate my keys?

Key rotation is considered a best practice for management for a few reasons:

- Like with passwords, it is advised to rotate a key every once in a while to prevent cracking. Shifting the key components around makes any progress made on cracking it obsolete.
- Using different versions of a key allows you to compartmentalize and manage a key, and any information encrypted with it.

# Managing a Key in the CLI

To rotate a key in the CLI, use the following command:  

```shell MyAES256SIVKey
akeyless rotate-key --name MyAES256SIVKey
```

Where:

- `name`: The key name.

If you wish to add a rotation schedule, use the following command:

```shell MyAES256SIVKey
akeyless update-rotation-settings --name <key name> --auto-rotate=<true/false>\
--rotation-interval <days between rotation>
```

Where:

- `name`:  The key name
- `auto-rotate`: Select if you wish to autorotate the key, the default is false.
- `rotation-interval`: Desired rotation interval, in days.

Full parameters can be found [here](https://docs.akeyless.io/docs/cli-reference-encryption-keys#p-stylecolorblueupdate-rotation-settingsp)

To view the key's existing versions, use the describe item command using the following parameters:

- `name`: The key name
- `show-versions`: If you want to see all the key versions

```shell MyAES256SIVKey
akeyless describe-item --name MyAES256SIVKey --show-versions
```

example output:

```shell MyAES256SIVKey
akeyless describe-item -n MyAES256SIVKey --show-versions
{
   "item_name": "/MyAES256SIVKey",
   "item_type": "AES256GCM",
   "item_metadata": "",
   "item_size": 32,
   "last_version": 2,
   "with_customer_fragment": false,
   "is_enabled": true,
   "public_value": "",
   "certificates": "",
   "protection_key_name": "",
   "cert_issuer_signer_key_name": "",
   "certificate_issue_details": {
      "max_ttl": 0,
      "cert_issuer_type": "",
      "ssh_cert_issuer_details": null,
      "pki_cert_issuer_details": null
   },
   "client_permissions": [
      "read",
      "list",
      "update",
      "delete",
      "create"
   ],
   "item_state": "Enabled",
   "item_versions": [
      {
         "version": 1,
         "item_version_state": "PendingDeletion",
         "deletion_date": "2020-01-30T13:00:00Z"
      },
      {
         "version": 2,
         "item_version_state": "Enabled"
      }
   ]
}
```

To delete a specific key version, use these parameters on the  **Delete Item** command:

- `name`: The key name.
- `version`: The version of the key you wish to delete.
- `delete-in-days`: The time in days until deletion.

```shell MyAES256SIVKey
akeyless delete-item --name MyAES256SIVKey --version=1 --delete-in-days=30
```

# Managing a Key in the Console

To rotate a key in the console, 

1. Go to the folder in Akeyless where you saved the desired key and select it

2. If you wish to rotate it once, tap **Rotate Key Now**

- If you wish to set an auto-rotate schedule tap **Auto Rotate Configuration**

- **Rotation Notification**: If you wish to get a notification before the next **Automatic Rotation**, click on ⊕ Add Notification and adjust the day count to any number you desire. This can be done multiple times to be notified more than once.

- If you wish to view and manage previous versions open the **Versions** tab.

# Tutorial

Check out our tutorial video on <a href="https://tutorials.akeyless.io/docs/creating-and-rotating-encryption-keys" target="_blank" style="color: #00e">Creating and Rotating Encryption Keys</a>.