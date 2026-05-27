---
title: GitHub Universal Secret Connector
deprecated: false
hidden: false
metadata:
  robots: index
---
This page discusses the creation of GitHub [Universal Secrets Connectors](https://docs.akeyless.io/docs/universal-secrets-connector). If you wish to create a Universal Secrets Connector for a different cloud service, please go to the matching doc, as they have varying parameters.

In environments using Multi-Vault Governance (MVG), GitHub USC is surfaced as the MVG item for GitHub repository secret management.

Unlike other **USCs**, GitHub does not let you view secret values outside GitHub. With this USC, you can **create new secrets**, **update existing secrets**, and **delete secrets** in the repository.

GitHub USC setup and management has 3 scopes:

* **Repository**: Choose a repository by **Name**, **Topic**, or **Custom Property**.

* **Organization**: Choose **Private**, **Public**, or **Selected**.

    * **Private**: Manage secrets for **Private** repositories.

    * **Public**: Manage secrets for **Public** repositories.

    * **Selected**: Manage secrets for the repositories you choose.

* **Environment Repository**: Choose the Environment Repository where you want to manage secrets.

## Prerequisites

* [Akeyless Gateway](https://docs.akeyless.io/docs/gateway-overview) version `4.48.0` or later.
* [GitHub target](https://docs.akeyless.io/docs/github-target)

## Working With Universal Secrets Connector with the CLI

This section will discuss the different commands necessary to handle USCs. While the initial creation command is a regular Akeyless command, management of USCs is done through a set of sub-commands, which all have the prefix `usc` added to them, as will be shown later in this section. If the prefix is not added to these sub-commands, they will not work.

### Creating a USC

To create a USC, use the following command:

```shell
akeyless usc create --name <name> --target-to-associate <target name>
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

### Adding a New Secret to a USC

To create a new secret in your USC, use the following command:

```shell
akeyless usc create --usc-name <usc name> --secret-name <new secret name> --value <secret value> 
```

The main parameters are:

* `usc-name`: Name of the Universal Secrets Connector.

* `secret-name`: The name of the secret you would like to create.

* `value`: The value of the secret you would like to create, plaintext, or Base64-encoded.

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
