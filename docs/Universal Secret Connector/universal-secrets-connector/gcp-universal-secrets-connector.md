---
title: GCP Universal Secrets Connector
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
This page discusses the creation of GCP [Universal Secrets Connectors](https://docs.akeyless.io/docs/universal-secrets-connector). If you wish to create a Universal Secrets Connector for a different cloud service, please go to the matching doc, as they have varying parameters.

## Prerequisites

* An [Akeyless Gateway](https://docs.akeyless.io/docs/gateway-overview) with **Read** permission on the target associated with the **USC**.
* [GCP Service Account](https://cloud.google.com/iam/docs/service-account-overview) with the [Secret Manager Admin](https://cloud.google.com/secret-manager/docs/access-control) role assigned, to allow selecting a KMS encryption key for the secret, add the following roles: [Cloud KMS Viewer](https://docs.cloud.google.com/kms/docs/reference/permissions-and-roles#cloudkms.viewer) and [Cloud KMS CryptoKey Encrypter and Decrypter](https://docs.cloud.google.com/kms/docs/reference/permissions-and-roles#cloudkms.cryptoKeyEncrypterDecrypter).

## Working with Universal Secrets Connector with the CLI

This section will discuss the different commands necessary to handle USCs. While the initial creation command is a regular Akeyless command, management of USCs is done through a set of sub-commands, which all have the prefix `usc` added to them, as will be shown later in this section. If the prefix is not added to these sub-commands, they will not work.

### Creating a USC

To create a USC, use the following command:

```shell
akeyless create-usc --usc-name <name> --target-to-associate <target name>
```

The main parameters are:

* `name`: Name for the Universal Secrets Connector. You may specify the location by adding a path to the virtual folder where you want to create the new Universal Secrets Connector, using slash `/` separators. If the folder does not exist, it will be created along with the Universal Secrets Connector.

* `target-to-associate`: An existing [Target](https://docs.akeyless.io/docs/targets) that points to your desired endpoint.

* `gcp-sm-regions`: Optional, comma-separated list of GCP Secret Manager regions used when listing regional secrets (maximum 12).

Additional parameters can be found in the [CLI Reference](https://docs.akeyless.io/docs/cli-reference-universal-secrets-connector#create-usc).

### Listing USC Secrets

To list the secrets from your USC, use the following command:

```shell
akeyless usc list --usc-name <usc name>
```

This command lists global secrets by default.

To list regional secrets for a GCP USC, use:

```shell
akeyless usc list --usc-name <usc name> --object-type regional-secrets
```

Regional listing uses the regions configured on the USC item (`--gcp-sm-regions` in `create-usc` or `update-item`).

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
akeyless usc get --usc-name <usc name> --secret-id <secret id>
```

The main parameters are:

* `usc-name`: Name of the Universal Secrets Connector.

* `secret-id`: The ID of the secret you would like to fetch.

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
akeyless usc create --usc-name <USC name> --secret-id <secret id> --value <new secret value>
```

The main parameters are:

* `usc-name`: Name of the Universal Secrets Connector.

* `secret-name`: The name of the secret you would like to create.

* `value`: The value of the secret you would like to create, plaintext, or Base64-encoded.

* `--remote-secret-expires`: Optional. Expiration time for the secret in GCP Secret Manager, in UTC format: `YYYY-MM-DDTHH:MM:SSZ`. Once this time passes, GCP automatically disables access to the secret.

Additional parameters can be found in the [CLI Reference](https://docs.akeyless.io/docs/cli-reference-universal-secrets-connector#create).

For GCP USC, you can create a regional secret by adding `--region <gcp-region>`. If omitted, the secret is created as global.

### Updating an Existing USC Secret

To update an existing secret in your USC, use the following command:

```shell
akeyless usc update --usc-name <USC name> --secret-id <secret id> --value <new secret value>
```

Use `--remote-secret-expires` to set or update the expiration time for the secret in GCP Secret Manager, in UTC format: `YYYY-MM-DDTHH:MM:SSZ`.

Additional parameters can be found in the [CLI Reference](https://docs.akeyless.io/docs/cli-reference-universal-secrets-connector#update).

### Deleting an Existing USC Secret

To delete an existing secret in your USC, use the following command:

```shell
akeyless usc delete --usc-name <USC name> --secret-id <secret id>
```

Additional parameters can be found in the [CLI Reference](https://docs.akeyless.io/docs/cli-reference-universal-secrets-connector#delete).

## Creating a Universal Secrets Connector from the Console

1. Log in to the Akeyless Console, and go to **Items > New > Universal Secrets Connector**.

2. Select the **GCP** secret type and click **Next**.

3. Define a **Name** of the Universal Secrets Connector, and specify the **Location** as a path to the virtual folder where you want to create the new Universal Secrets Connector, using slash `/` separators. If the folder does not exist, it will be created along with the Universal Secrets Connector.

4. Define the remaining settings as follows:

   * **Description:** Optional, enter a description of the Universal Secrets Connector.

   * **Tags:** Optional. Select one or more tags for the Universal Secrets Connector, or enter the name of a new tag to be added as part of the creation process.

   * **Delete Protection:** Optional, turn on this setting to protect the item from deletion

   * **Target:** Select an existing [GCP Target](https://docs.akeyless.io/docs/gcp-targets).

   * **Project ID:** Optional. The GCP Project ID to use when specifying a project different from the one attached to the [GCP Target](https://docs.akeyless.io/docs/gcp-targets).

   * **Region:** Optional. Choose the regions where this Universal Secrets Connector can manage secrets. You can select up to 12 regions.

   * **Gateway:** Select the desired corresponding Gateway.

5. Click **Finish**.

## GCP Universal Secrets Details

Once connected to a Target, you can access a Universal Secrets Connector in your Akeyless Console page, which allows you to manage your Universal Secrets and display the following information about the secret:

* **Name:** Secret name

* **Location:** Secret location

* **Encryption:** Encryption information

* **Labels:** GCP connected labels

* **Status:** Secret status of enabled/disabled

* **Created:** Secret date of creation

More information and secret value can be viewed by selecting a specific secret, additionally, you will have the option to perform actions on the secret.
