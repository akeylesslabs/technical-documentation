---
title: HashiCorp Vault Universal Secrets Connector
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
This page discusses the creation of HashiCorp Vault [Universal Secrets Connector](https://docs.akeyless.io/docs/universal-secrets-connector). If you wish to create a Universal Secrets Connector for a different Secret service, please go to the matching doc, as they have varying parameters.

## Prerequisites

* An [Akeyless Gateway](https://docs.akeyless.io/docs/gateway-overview) with **Read** permission on the target associated with the **USC**.

## Working With Universal Secrets Connector with the CLI

This section will discuss the different commands necessary to handle USCs. While the initial creation command is a regular Akeyless command, management of USCs is done through a set of sub-commands, which all have the prefix `usc` added to them, as will be shown later in this section. If the prefix is not added to these sub-commands, they will not work.

* An [Akeyless Gateway](https://docs.akeyless.io/docs/gateway-overview).
* [HashiCorp Vault Target](https://docs.akeyless.io/docs/hashicorp-vault-target) which holds an access token with permissions to `create`, `delete`, `update`, `read` and `list` secrets.

### Creating a USC

To create a USC, use the following command:

```shell
akeyless create-usc --usc-name <name> --target-to-associate <target name>
```

The main parameters are:

* `name`: Name for the Universal Secrets Connector. You may specify the location by adding a path to the virtual folder where you want to create the new Universal Secrets Connector, using slash `/` separators. If the folder does not exist, it will be created along with the Universal Secrets Connector.

* `target-to-associate`: An existing [Target](https://docs.akeyless.io/docs/targets) that points to your desired endpoint.

Additional parameters can be found in the [CLI Reference](https://docs.akeyless.io/docs/cli-reference-universal-secrets-connector#create-usc).

### Listing USC Secrets

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

### Fetching a Secret from the USC

To view a secret from your USC, use the following command:

```shell
akeyless usc get --usc-name <USC name> --secret-id <secret id or name>
```

The main parameters are:

* `usc-name`: Name of the Universal Secrets Connector.

* `secret-id`: The name or ID of the secret you would like to fetch.

Additional parameters can be found in the [CLI Reference](https://docs.akeyless.io/docs/cli-reference-universal-secrets-connector#get).

The output should look as follows:

```shell
{
  "value": "<Base64-encoded value>",
  "metadata": {
    "created": "<timestamp>",
    "updated": "<timestamp>"
  }
}
```

### Adding a New Secret to a USC

To create a new secret in your USC, use the following command:

```shell
akeyless usc create --usc-name <usc name> --secret-name <new secret name> --value <secret value>
```

The main parameters are:

* `usc-name`: Name of the Universal Secrets Connector.

* `secret-name`: The name of the secret you would like to create.

* `value`: The value of the secret you would like to create. Plaintext or Base64 encoded - `Key = Value` format

Additional parameters can be found in the [CLI Reference](https://docs.akeyless.io/docs/cli-reference-universal-secrets-connector#create).

### Updating an Existing USC Secret

To update an existing secret in your USC, use the following command:

```shell
akeyless usc update --usc-name <usc name> --secret-id <secret id or name> --value <new secret value>
```

Additional parameters can be found in the [CLI Reference](https://docs.akeyless.io/docs/cli-reference-universal-secrets-connector#update).

### Deleting an Existing USC Secret

To delete an existing secret in your USC, use the following command:

```shell
akeyless usc delete --usc-name <usc name> --secret-id <secret id or name>
```

Additional parameters can be found in the [CLI Reference](https://docs.akeyless.io/docs/cli-reference-universal-secrets-connector#delete).

## Creating a Universal Secrets Connector from the Console

1. Log in to the Akeyless Console, and go to **Items > New > Universal Secrets Connector**.

2. Select the **HashiCorp Vault** secret type and click **Next**.

3. Define a **Name** of the Universal Secrets Connector group, and specify the **Location** as a path to the virtual folder where you want to create the new Universal Secrets Connector, using slash `/` separators. If the folder does not exist, it will be created along with the Universal Secrets Connector.

4. Define the remaining settings as follows:

    * **Description:** Optional, enter a description of the Universal Secrets Connector.

    * **Tags:** Optional. Select one or more tags for the Universal Secrets Connector, or enter the name of a new tag to be added as part of the creation process.

    * **Delete Protection:** Optional, turn on this setting to protect the item from deletion.

    * **Target:** Select an existing [HashiCorp Vault Target](https://docs.akeyless.io/docs/hashicorp-vault-target)

    * **Gateway:** Select the desired corresponding Gateway.

5. Click **Finish**

## HashiCorp Vault Universal Secrets Details

Once connected to a Target, you can access a Universal Secrets Connector in your Akeyless Console page, which allows you to manage your Universal Secrets and display the following information about the secret:

* **Name:** Secret name

* **Version:** The version of the secret

* **Creation Time:** When the secret was created

More information and secret value can be viewed by selecting a specific secret, additionally, you will have the option to perform actions on the secret.

Additional capabilities include:

* Account-level secret versioning applies across Akeyless item types such as Static Secrets, Rotated Secrets, and Targets, and is not specific to HashiCorp integrations.
* For USC-backed external secrets, the version details shown in the console can vary by provider and by the metadata and history returned by that provider.
* For larger HashiCorp Vault structures, you can sync the contents of an entire folder by using the folder sync commands.

### Sync Entire Folder Contents

For HashiCorp Vault USC flows in Multi-Vault Governance (MVG), use folder-level sync commands to apply sync associations across all supported secrets in a folder path.

Common commands:

```shell
akeyless folder-sync --name </folder/path> --usc-name </usc-name>
```

```shell
akeyless folder-sync-all --name </folder/path>
```

```shell
akeyless folder-delete-sync --name </folder/path> --usc-name </usc-name>
```

For Vault-specific mapping, `folder-sync` also supports `--namespace` and `--engine-name` (engine prefix must end with `/`).

For full command flags and examples, see [CLI Reference - Universal Secrets Connector](https://docs.akeyless.io/docs/cli-reference-universal-secrets-connector#folder-sync-commands-mvg).

_Note:_ The **KV Secrets Engine v1** is not supported. Please use **KV Secrets Engine v2** when working with the Vault Universal Secrets Connector.
