---
title: Server Inventory
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
Akeyless Server Inventory discovery enables importing and managing **Local Users** from remote servers into  [Rotated Secrets](https://docs.akeyless.io/docs/rotated-secrets) in the Akeyless Platform. 

The discovery process can work against a standalone [Windows](https://docs.akeyless.io/docs/windows-target), [SSH](https://docs.akeyless.io/docs/ssh-target), and the migration will use the Target credentials to connect to the endpoint server using `Winrm` or `ssh` correspondingly. On each server, the discovery will search for all users except the **Ignored Users List**. 

# Set Up Automatic Migration for Server Inventory

To create the Server Inventory Migration, login to your Gateway on port `8000`, navigate to the **Automatic Migration -> Server Inventory -> Add**, and set the following:

* **Name:** A unique name for the migration object. 

* **Migration Target:** Select an existing [SSH Target](https://docs.akeyless.io/docs/ssh-target) or a [Windows Target](https://docs.akeyless.io/docs/windows-target) to discover local users on that Target.

* **Ignore the Following Local Users:** Comma-separated list of Local Usernames to exclude while migrating.

* **User Name Template:** A template for the created items, where the imported Local Users will be saved as Rotated Secrets ) inside the Akeyless Platform, i.e: `Users/{{COMPUTER_NAME}}/{{USERNAME}}`,  This path includes the prefix of the Destination Folder.

* **Search in Privileged Users Groups** : A list of groups to scan.

* **Target Location:** Destination folder path inside the Akeyless Platform for the migrated users. Make sure your Gateway has enough permissions to create Secrets under this location. The migrated [Rotated Secrets](https://docs.akeyless.io/docs/rotated-secrets) (https://docs.akeyless.io/docs/targets) of your Local Users will be saved under this location.

* **Enable SRA:** Enable/Disable Secure Remote Access setup for the migrated local users via the Rotated Secrets. Default is Disabled, the Rotated Secrets will not be created with SRA configuration. **Available only for accounts with the SRA package** .

* **Auto Rotate:** Enable/Disable automatic/recurrent rotation for the migrated secrets. By default is **Disabled**. If Enabled, this should be set with rotation-interval and rotation-hour settings.
