---
title: AWS Universal Secrets Connector
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
This page discusses the creation of AWS [Universal Secrets Connectors](doc:external-secrets-manager). If you wish to create a Universal Secrets Connector for a different cloud service, please go to the matching doc, as they have varying parameters.

To manage secrets stored on AWS Secret Manager, the **USC** utilizes [AWS Target](doc:aws-targets) to create local "windows" into the related Secret Manager, effectively letting you manage them indirectly. Each **USC** item derives its permissions from the identity linked to its [AWS Target](doc:aws-targets).

When a user is granted read access to a **USC** item, they can act using the permissions of that underlying identity. With USC, you can unify governance and visibility across fragmented secret stores without migrating data or altering existing workflows.

After connecting to your AWS Secret Manager source, you will be able to manage all your secrets from Akeyless, including viewing, adding, updating, deleting, and [syncing secrets](doc:sync-secret).

The **USC** solution works in a governance loop model, supporting and reflecting any changes made to your AWS secrets, either from the Akeyless side or from the AWS Secret Manager. This is done automatically as Akeyless doesn't store a copy of the AWS secrets, ensuring that data residency and security policies remain untouched. The **USC** simply reflects them in real time, without any requirements or changes that should be made on the AWS Secret Manager endpoint.

[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/60251a70458e8bb82d88317bde1ad04b9e9a7b6ea82e68e0b11086106a0f6a7c-Synced_Secret-AWS.png",
        "",
        ""
      ],
      "align": "center"
    }
  ]
}
[/block]


# Prerequisites

- An [Akeyless Gateway](doc:api-gw)  with **Read** permission on the target associated with the **USC**.
- [AWS Target](doc:aws-targets) which holds an AWS IAM Principal with the following permissions:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "secretsmanager:ListSecrets",
      "Resource": "*"
    },
    {
      "Effect": "Allow",
      "Action": [
        "secretsmanager:GetSecretValue",
        "secretsmanager:DescribeSecret",
        "secretsmanager:CreateSecret",
        "secretsmanager:UpdateSecret",
        "secretsmanager:DeleteSecret",
        "secretsmanager:PutSecretValue",
        "secretsmanager:UntagResource",
        "secretsmanager:TagResource"
      ],
      "Resource": "arn:aws:secretsmanager:<region>:<accountID>:secret:*"
    }
  ]
}

```

Note, `secretsmanager:ListSecrets` is AWS Secrets Manager operations that doesn’t support resource-level permissions. When an action is in that category, AWS requires you to grant it on `"Resource": "*"`, not on an ARN pattern, read more [here](https://docs.aws.amazon.com/service-authorization/latest/reference/list_awssecretsmanager.html#awssecretsmanager-actions-as-permissions).

# Working With Universal Secrets Connector from the CLI

This section will discuss the different commands necessary to handle USCs. While the initial creation command is a regular Akeyless command, management of USCs is done through a set of sub-commands, which all have the prefix `usc` added to them, as will be shown later in this section. If the prefix is not added to these sub-commands, they will not work.

## Creating a USC

To create a USC, use the following command:

```shell
akeyless usc create --name <name> --target-to-associate <target name>
```

The main parameters are:

- `name`: Name for the Universal Secrets Connector. You may specify the location by adding a path to the virtual folder where you want to create the new Universal Secrets Connector, using slash `/` separators. If the folder does not exist, it will be created along with the Universal Secrets Connector.

- `target-to-associate`: An existing [Target](doc:targets) that points to your desired endpoint.

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

- `usc-name`: Name of the Universal Secrets Connector.

- `secret-id`: The name or ID of the secret you would like to fetch.

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

- `usc-name`: Name of the Universal Secrets Connector.

- `secret-name`: The name of the secret you would like to create.

- `value`: The value of the secret you would like to create, plaintext or base64 encoded.

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

2. Select the **AWS** secret type and click **Next**.

3. Define a **Name** of the Universal Secrets Connector group, and specify the **Location** as a path to the virtual folder where you want to create the new Universal Secrets Connector, using slash `/` separators. If the folder does not exist, it will be created along with the Universal Secrets Connector.

4. Define the remaining settings as follows:

- **Description:** Optional, enter a description of the Universal Secrets Connector.

- **Tags:** Optional, select one or more tags for the Universal Secrets Connector, or enter the name of a new tag to be added as part of the creation process.

- **Delete Protection:** Optional, turn on this setting to protect the item from deletion.

- **Target:** Select an existing [AWS Target](doc:aws-targets).

- **Gateway:** Select the desired corresponding Gateway.

- **USC Secret Prefix:** Optional, provide a prefix to be appended to any newly created secret.

- **Use Prefix as Filter:** Optional, use the secret prefix as a filter.

5. Click **Finish**

# AWS Universal Secrets Details

Once connected to a Target, you will be able to access a Universal Secrets Connector in your Akeyless console page, which will allow you to manage your Universal Secrets, as well as display the following information about the secret:

- **Name:** Secret name

- **Description:** Secret description

- **Last Retrieved:** The last time the secret was fetched, displayed in UTC time.

More information and secret value can be viewed by selecting a specific secret, additionally, you will have the option to perform actions on the secret.

# Tutorial

Check out our tutorial video on <a href="https://tutorials.akeyless.io/docs/managing-secrets-stored-in-aws-azure-gcp-k8s" target="_blank">AWS Universal Secrets Connector</a>.