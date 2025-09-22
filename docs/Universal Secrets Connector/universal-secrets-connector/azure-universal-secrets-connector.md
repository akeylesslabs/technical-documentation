---
title: Azure Universal Secrets Connector
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
This page discusses the creation of Azure [Universal Secrets Connectors](doc:external-secrets-manager). If you wish to create a Universal Secrets Connector for a different cloud service, please go to the matching doc, which has varying parameters.

# Prerequisites

* An [Akeyless Gateway](doc:api-gw)  with **Read** permission on the target associated with the **USC**.
* Azure [Registered Application](https://learn.microsoft.com/en-us/security/zero-trust/develop/app-registration) with the [Key Vault Secrets Officer](https://learn.microsoft.com/en-us/azure/role-based-access-control/built-in-roles/security#key-vault-secrets-officer) role assigned. If you wish to work with Certificates, assign the [Certificate Officer](https://learn.microsoft.com/en-us/azure/role-based-access-control/built-in-roles/security#key-vault-secrets-officer) role.

# Working With Universal Secrets Connector from the Console

This section will discuss the different commands necessary to handle USCs. While the initial creation command is a regular Akeyless command, management of USCs is done through a set of sub-commands, which all have the prefix `usc` added to them, as will be shown later in this section. If the prefix is not added to these sub-commands, they will not work.

## Creating a USC

To create a USC, use the following command:

```shell
akeyless create-usc --usc-name <name> --target-to-associate <target name> --azure-kv-name <key vault name>
```

The main parameters are:

* `name`: Name for the Universal Secrets Connector. You may specify the location by adding a path to the virtual folder where you want to create the new Universal Secrets Connector, using slash `/` separators. If the folder does not exist, it will be created along with the Universal Secrets Connector.

* `target-to-associate`: An existing [Target](doc:targets) that points to your desired endpoint.

* `azure-kv-name`: The name of an existing Azure key vault. 

Additional parameters can be found in the [CLI Reference](doc:cli-reference-external-secrets-manager).

## Listing USC Objects

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

To list the certificates from your USC, use the following command:

```shell
akeyless usc list --usc-name <usc name> --object-type certificate
```

## Fetching a Secret from the USC

To view a secret from your USC, use the following command:

```shell
akeyless usc get --usc-name <usc name> --secret-id <secret id or name>
```

The main parameters are:

* `usc-name`: Name of the Universal Secrets Connector.

* `secret-id`: The name or ID of the secret you would like to fetch.

* `object-type[=secret]` Either secret or certificate, the default is set to secret.

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

* `value`: The value of the secret you would like to create, plaintext or base64 encoded.

* `object-type[=secret]`: Either `secret` or `certificate`, when set to `certificate` -  Provide a Base64-encoded certificate file that includes the private key.

Additional parameters can be found in the [CLI Reference](doc:cli-reference-external-secrets-manager).

## Updating an Existing USC secret

To update an existing secret in your USC, use the following command:

```shell
akelyess usc update --usc-name <usc name> --secret-name <new secret name> --value <secret value>
```

Additional parameters can be found in the [CLI Reference](doc:cli-reference-external-secrets-manager).

## Deleting an Existing USC secret

To delete an existing secret in your USC, use the following command:

```shell
akelyess usc delete --usc-name <usc name> --secret-name < secret name>
```

Additional parameters can be found in the [CLI Reference](doc:cli-reference-external-secrets-manager).

# Creating a Universal Secrets Connector from the Console

1. Log in to the Akeyless Console, and go to **Items > New > Universal Secrets Connector**.

2. Select the **Azure** secret type and click **Next**.

3. Define a **Name** of the Universal Secrets Connector, and specify the **Location** as a path to the virtual folder where you want to create the new Universal Secrets Connector, using slash `/` separators. If the folder does not exist, it will be created along with the Universal Secrets Connector.

4. Define the remaining settings as follows:

* **Description:** Optional, enter a description of the Universal Secrets Connector.

* **Tags:** Optional, select one or more tags for the Universal Secrets Connector, or enter the name of a new tag to be added as part of the creation process.

* **Delete Protection:** Optional, turn on this setting to protect the item from deletion

* **Target:** Select an existing [Azure Target](https://docs.akeyless.io/docs/cloud-targets).

* **Gateway:** Select the desired corresponding Gateway.

* **Key Vault Name:** The name of the Azure key vault you would like to connect with.

5. Click **Finish**.

# Azure Universal Secrets Details

Once connected to a Target, you will be able to access the Universal Secrets Connector in your Akeyless console page, which will allow you to manage your Universal Secrets, as well as display the following information about the secret:

* **Name:** Secret name

* **Type:** Secret type

* **Status:** Secret status of enabled/disabled

* **Expiration:** Secret date of expiration

More information and secret value can be viewed by selecting a specific secret, additionally, you will have the option to perform actions on the secret.

# Azure Universal Certificates Details

Once connected to a Target, you will be able to access the Universal Secrets Connector in your Akeyless console page, which will allow you to manage your Universal Certificates, as well as display the following information about the Certificates:

* **Name:** Certifitcate name

* **Thumbprint:** The certificate thumbprint

* **Status:** Certificate status of enabled/disabled

* **Created:** Creation date

* **Expiration:** Certificate date of expiration

You can also import certificates in `pem` and `pfx` formats to the **Azure Key Vault** using the **Azure USC**

More information and secret value can be viewed by selecting a specific secret, additionally, you will have the option to perform actions on the secret.
