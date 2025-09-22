---
title: Hashicorp Vault Universal Secrets Connector
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
This page discusses the creation of Hashicorp Vault [Universal Secrets Connector](doc:external-secrets-manager). If you wish to create a Universal Secrets Connector for a different Secret service, please go to the matching doc, as they have varying parameters.

# Prerequisites

* An [Akeyless Gateway](doc:api-gw)  with **Read** permission on the target associated with the **USC**.

# Working With Universal Secrets Connector from the CLI

This section will discuss the different commands necessary to handle USCs. While the initial creation command is a regular Akeyless command, management of USCs is done through a set of sub-commands, which all have the prefix `usc` added to them, as will be shown later in this section. If the prefix is not added to these sub-commands, they will not work.

* An [Akeyless Gateway](https://docs.akeyless.io/docs/api-gw).
* [Hashicorp Vault Target](https://docs.akeyless.io/docs/hashicorp-vault-target) which holds an access token with permissions to `create`, `delete`, `update`, `read` and `list` secrets. 

## Creating a USC

To create a USC, use the following command:

```shell
akeyless create-usc --usc-name <name> --target-to-associate <target name>
```

The main parameters are:

* `name`: Name for the Universal Secrets Connector. You may specify the location by adding a path to the virtual folder where you want to create the new Universal Secrets Connector, using slash `/` separators. If the folder does not exist, it will be created along with the Universal Secrets Connector.

* `target-to-associate`: An existing [Target](doc:targets) that points to your desired endpoint.

Additional parameters can be found in the [CLI Reference](doc:cli-reference-external-secrets-manager).

## Listing USC Secrets

To list the secrets from your USC, use the following command:

```shell
akeyless usc list --usc-name <usc name>
```

The output should look as follows:

```shell
{
  "secrets_list": [
    {
      "secret_id": "<secret id>",
      "name": "<secret name>",
      "created": "<timestamp>",
      "type": "<type>",
      "status": <activity status, true/false>
    }
  ]
}
```

## Fetching a Secret from the USC

To view a secret from your USC, use the following command:

```shell
akeyless usc get --usc-name <usc name> --secret-id <secret id or name>
```

The main parameters are:

* `usc-name`: Name of the Universal Secrets Connector.

* `secret-id`: The name or ID of the secret you would like to fetch.

Additional parameters can be found in the [CLI Reference](doc:cli-reference-external-secrets-manager).

The output should look as follows:

```shell
{
  "value": "<base64 encoded value>",
  "metadata": {
    "created": "<timestamp>",
    "updated": "<timestamp>"
  }
}
```

## Adding a New Secret to a USC

To create a new secret in your USC, use the following command:

```shell
akeyless usc create --usc-name <usc name> --secret-name <new secret name> --value <secret value>
```

The main parameters are:

* `usc-name`: Name of the Universal Secrets Connector.

* `secret-name`: The name of the secret you would like to create.

* `value`: The value of the secret you would like to create, plaintext or base64 encode - **Key = Value** format

Additional parameters can be found in the [CLI Reference](doc:cli-reference-external-secrets-manager).

## Updating an Existing USC secret

To update an existing secret in your USC, use the following command:

```shell
akelyess usc update --usc-name <usc name> --secret-id <secret id or name> --value <new secret value>
```

Additional parameters can be found in the [CLI Reference](doc:cli-reference-external-secrets-manager).

## Deleting an Existing USC secret

To delete an existing secret in your USC, use the following command:

```shell
akelyess usc delete --usc-name <usc name> --secret-id <secret id or name>
```

Additional parameters can be found in the [CLI Reference](doc:cli-reference-external-secrets-manager).

# Creating a Universal Secrets Connector from the Console

1. Log in to the Akeyless Console, and go to **Items > New > Universal Secrets Connector**.

2. Select the **Hashicorp Vault** secret type and click **Next**.

3. Define a **Name** of the Universal Secrets Connector group, and specify the **Location** as a path to the virtual folder where you want to create the new Universal Secrets Connector, using slash `/` separators. If the folder does not exist, it will be created along with the Universal Secrets Connector.

4. Define the remaining settings as follows:

* **Description:** Optional, enter a description of the Universal Secrets Connector.

* **Tags:** Optional, select one or more tags for the Universal Secrets Connector, or enter the name of a new tag to be added as part of the creation process.

* **Delete Protection:** Optional, turn on this setting to protect the item from deletion.

* **Target:** Select an existing [Hashicorp Vault Target](doc:hashicorp-vault-target)

* **Gateway:** Select the desired corresponding Gateway.

5. Click **Finish**

# Hashicorp Vault Universal Secrets Details

Once connected to a Target, you will be able to access a Universal Secrets Connector in your Akeyless console page, which will allow you to manage your Universal Secrets, as well as display the following information about the secret:

* **Name:** Secret name

* **Version:** The version of the secret

* **Creation Time:** When the secret was created

More information and secret value can be viewed by selecting a specific secret, additionally, you will have the option to perform actions on the secret.

**Note:** The **KV Secrets Engine v1** is not supported. Please use **KV Secrets Engine v2** when working with the Vault Universal Secrets Connector.
