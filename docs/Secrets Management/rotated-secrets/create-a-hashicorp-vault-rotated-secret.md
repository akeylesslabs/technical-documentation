---
title: HashiCorp Vault Rotated Secret
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
You can create a Rotated Secret for a HashiCorp Vault target when you want Akeyless to manage a rotated secret item stored in HashiCorp Vault.

## Prerequisites

* An [Akeyless Gateway](https://docs.akeyless.io/docs/gateway-overview).
* A [HashiCorp Vault Target](https://docs.akeyless.io/docs/hashicorp-vault-target) with permissions to create, delete, update, read, and list secrets.

## Create a HashiCorp Vault Rotated Secret with the CLI

To create a HashiCorp Vault Rotated Secret using the Akeyless CLI, run the following command:

```shell
akeyless rotated-secret create hashi-vault \
--name <Rotated Secret name> \
--gateway-url 'https://<Your-Akeyless-GW-URL>:8000' \
--target-name <target name to associate> \
--auto-rotate <true|false> \
--rotation-interval <1-365>
```

Where:

* `name`: A unique name of the Rotated Secret. The name can include the path to the virtual folder where you want to create the new Rotated Secret, using slash `/` separators. If the folder does not exist, it will be created together with the Rotated Secret.

* `gateway-url`: Akeyless Gateway URL (port `8000`).

* `target-name`: The name of the [HashiCorp Vault Target](https://docs.akeyless.io/docs/hashicorp-vault-target) with which the Rotated Secret should be associated.

* `auto-rotate`: Enable auto-rotation if you need to update the secret regularly.

* `rotation-interval`: The number of days to wait between every automatic rotation (1-365).

The HashiCorp Vault variant also supports the shared rotated-secret settings for protection keys, max versions, tags, and description. For the full parameter list, see the [CLI Reference - Rotated Secrets](https://docs.akeyless.io/docs/cli-reference-rotated-secrets#hashi-vault) section.

## Create a HashiCorp Vault Rotated Secret in the Console

1. Log in to the Akeyless Console, and go to **Items > New > Rotated Secret > HashiCorp Vault**.

2. Define a **Name** of the Rotated Secret, and specify the **Location** as a path to the virtual folder where you want to create the new Rotated Secret, using slash `/` separators. If the folder does not exist, it will be created together with the Rotated Secret.

3. Define the remaining settings as follows:

    * **Target:** Select an existing [HashiCorp Vault Target](https://docs.akeyless.io/docs/hashicorp-vault-target).

    * **Gateway:** Select the desired corresponding Gateway.

    * **Description:** Optional, enter a description of the Rotated Secret.

    * **Tags:** Optional. Select one or more tags for the Rotated Secret, or enter the name of a new tag to be added as part of the creation process.

    * **Protection Key:** Optional, select the key used to encrypt the secret value.

    * **Auto rotate:** Enable automatic rotation and define the rotation interval.

4. Click **Finish**.

## Working With Version History

If secret versioning is enabled for the account, you can review the available versions for the rotated secret from the item details view.
