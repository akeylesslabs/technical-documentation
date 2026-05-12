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
This page explains how to create an Azure [Universal Secrets Connector](https://docs.akeyless.io/docs/universal-secrets-connector). For other cloud providers, use the matching Universal Secrets Connector documentation, because required parameters vary by provider.

## Prerequisites

### Azure requirements

* Azure subscription access.
* Existing Azure Key Vault.
* Permission to:
    * Create app registrations.
    * Assign RBAC roles to Azure resources.

### Akeyless requirements

* Active Akeyless account.
* Permission to configure Universal Secrets Connector.
* Network connectivity between the Akeyless Gateway and Azure Key Vault API endpoints
* An [Akeyless Gateway](https://docs.akeyless.io/docs/gateway-overview) with **Read** permission on the target associated with the **USC**.
* Azure [Registered Application](https://learn.microsoft.com/en-us/security/zero-trust/develop/app-registration) with the [Key Vault Secrets Officer](https://learn.microsoft.com/en-us/azure/role-based-access-control/built-in-roles/security#key-vault-secrets-officer) role assigned at the Key Vault scope. If you wish to work with certificates, assign the [Key Vault Certificates Officer](https://learn.microsoft.com/en-us/azure/role-based-access-control/built-in-roles/security#key-vault-certificates-officer) role.

## End-to-End SOP Workflow

Use this sequence when onboarding an Azure Key Vault to Universal Secrets Connector.

1. Create or identify an Azure App Registration (service principal).

2. Generate and securely store the client secret.

3. Assign role-based access at the Key Vault resource scope:

   * **Required for secrets:** Key Vault Secrets Officer or similar role.
   * **Optional for certificate operations:** Key Vault Certificates Officer or similar role.

4. Create an Akeyless Azure target. For detailed target setup instructions, see [Azure AD Targets](https://docs.akeyless.io/docs/azure-targets).

5. Create the Azure USC and associate it to the target.

6. Validate list, get, create, update, and delete operations with the CLI.

## Azure Configuration

Use this section for a complete Azure-side setup.

### Step 1: Create an app registration

1. In Azure Portal, go to **Microsoft Entra ID > App registrations**.
2. Select **New Registration**.
3. Enter an application name, such as `akeyless-usc-connector`.
4. Keep the default single-tenant setting unless the organization requires another setting.
5. Select **Register**.
6. Record these values from the app overview:

   * **Application (client) ID**
   * **Directory (tenant) ID**

### Step 2: Create a client secret

1. In the app registration, go to **Certificates & Secrets**.
2. Select **New Client Secret**.
3. Enter a description and expiration according to internal policy.
4. Select **Add**.
5. Copy the **Client Secret Value** immediately and store it in a secure location.

   > ⚠️ **Warning:**
   >
   > The secret value is only shown once in Azure Portal.

### Step 3: Assign Key Vault IAM role

1. In Azure Portal, open the target **Key Vault**.
2. Go to **Access Control (IAM)**.
3. Select **Add > Add Role Assignment**.
4. Select **Key Vault Secrets Officer** or a similar role.
5. Select the app registration service principal, such as **Akeyless USC Service Principal**.
6. Complete the role assignment.

For certificate operations, repeat the role assignment with **Key Vault Certificates Officer** or a similar role.

### Step 4: Confirm Key Vault scope

1. In Azure Portal, verify the role assignment scope is the specific Key Vault resource.
2. Avoid broader scopes unless required by policy.

### Step 5: Continue with Akeyless setup

After Azure-side setup is complete:

1. Create the Azure target in Akeyless.
2. Create the Azure USC and associate it to that target.
3. Continue with the validation checklist in this page.

## Required Azure Values

Collect the following values before creating the USC:

* Tenant ID
* Client ID (Application ID)
* Client Secret
* Azure Key Vault name

## Working With Universal Secrets Connector using the CLI

This section will discuss the different commands necessary to handle USCs. While the initial creation command is a regular Akeyless command, management of USCs is done through a set of sub-commands, which all have the prefix `usc` added to them, as will be shown later in this section. If the prefix is not added to these sub-commands, they will not work.

### Creating a USC

To create a USC, use the following command:

```shell
akeyless create-usc --name <name> --target-to-associate <target name> --azure-kv-name <key vault name>
```

The main parameters are:

* `--name`: Name for the Universal Secrets Connector. You may specify the location by adding a path to the virtual folder where you want to create the new Universal Secrets Connector, using slash `/` separators. If the folder does not exist, it will be created along with the Universal Secrets Connector.

* `--target-to-associate`: An existing [Target](https://docs.akeyless.io/docs/targets) that points to your desired endpoint.

* `--azure-kv-name`: The name of an existing Azure Key Vault.

Additional parameters can be found in the [CLI Reference](https://docs.akeyless.io/docs/cli-reference-universal-secrets-connector#create-usc).

### Listing USC Objects

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

For Azure Key Vault inventories, USC list operations support page-based retrieval:

```shell
akeyless usc list --usc-name <usc name> --page-size <items per page>
akeyless usc list --usc-name <usc name> --page-size <items per page> --page-token <next token>
```

Use `--page-size` on the first request. If the response includes `next_token`, pass that token into the next `usc list --page-token` call to continue browsing the Azure Key Vault inventory.

Connector-level prefix filtering is configured on the USC item itself by using `--usc-prefix` together with `--use-prefix-as-filter`.

To interact with prefix filtering:

1. Create or update the USC with a prefix value.
2. Enable `use-prefix-as-filter` on that USC.
3. Run `akeyless usc list --usc-name <usc name>`.

Only matching secrets are returned for that connector configuration.

Azure USC secret create and update operations also support tags.

To interact with Azure USC tag filtering:

1. Set connector tags with `--usc-tags`.
2. Enable `--use-tags-as-filter` on the USC.
3. Run `akeyless usc list --usc-name <usc name>` to view secrets filtered by the configured connector tags.

When creating a new Azure USC secret from the Console UI, the dialog inherits the connector prefix and shows connector tags in the creation form.

To view the exact supported CLI flags in your installed version, run:

```shell
akeyless usc list -h
```

### Fetching a Secret from the USC

To view a secret from your USC, use the following command:

```shell
akeyless usc get --usc-name <usc name> --secret-id <secret id or name>
```

The main parameters are:

* `--usc-name`: Name of the Universal Secrets Connector.

* `--secret-id`: The name or ID of the secret you would like to fetch.

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

* `--usc-name`: Name of the Universal Secrets Connector.

* `--secret-name`: The name of the secret you would like to create.

* `--value`: The value of the secret you would like to create, plaintext, or Base64-encoded.

* `--object-type[=secret]`: Either `secret` or `certificate`, when set to `certificate` - Provide a Base64-encoded certificate file that includes the private key.

* `--remote-secret-expires`: Optional. Expiration time for the secret in Azure Key Vault, in UTC format: `YYYY-MM-DDTHH:MM:SSZ`. Azure sets the `Expires` attribute on the secret version.

* `--remote-secret-activation-date`: Optional. Activation date for the secret in Azure Key Vault, in UTC format: `YYYY-MM-DDTHH:MM:SSZ`. Azure sets the `NotBefore` attribute on the secret version. The activation date must be earlier than or equal to the expiration date.

Additional parameters can be found in the [CLI Reference](https://docs.akeyless.io/docs/cli-reference-universal-secrets-connector#create).

### Updating an Existing USC Secret

To update an existing secret in your USC, use the following command:

```shell
akeyless usc update --usc-name <usc name> --secret-id <secret id or name> --value <secret value>
```

Use `--remote-secret-expires` to set or update the expiration time and `--remote-secret-activation-date` to set or update the activation date (Azure Key Vault `NotBefore`), both in UTC format: `YYYY-MM-DDTHH:MM:SSZ`. The activation date must be earlier than or equal to the expiration date.

Additional parameters can be found in the [CLI Reference](https://docs.akeyless.io/docs/cli-reference-universal-secrets-connector#update).

### Deleting an Existing USC Secret

Azure Key Vault uses soft-delete by default. To permanently delete a secret, use the `--force-delete` flag.

To delete an existing secret in your USC, use the following command:

```shell
akeyless usc delete --usc-name <usc name> --secret-id <secret id or name>
```

To force permanent deletion from the Azure Key Vault soft-deleted list, use:

```shell
akeyless usc delete --usc-name <usc name> --secret-id <secret id or name> --force-delete
```

Additional parameters can be found in the [CLI Reference](https://docs.akeyless.io/docs/cli-reference-universal-secrets-connector#delete).

## Validation Checklist

After setup, validate with these checks:

1. List objects:

   ```shell
   akeyless usc list --usc-name <usc name>
   ```

2. Read an existing secret:

   ```shell
   akeyless usc get --usc-name <usc name> --secret-id <secret id or name>
   ```

3. Create a test secret:

   ```shell
   akeyless usc create --usc-name <usc name> --secret-name <test secret name> --value <test value>
   ```

4. Update the test secret:

   ```shell
   akeyless usc update --usc-name <usc name> --secret-id <test secret name> --value <new value>
   ```

5. Delete the test secret:

   ```shell
   akeyless usc delete --usc-name <usc name> --secret-id <test secret name>
   ```

### Logging and auditing

Use logs to validate traceability of secret access operations:

* Azure Key Vault audit logs.
* Akeyless audit logs.

## Troubleshooting

Use this section when setup or validation fails.

### Authorization failed during list, get, create, update, or delete

Possible cause: the service principal is missing a Key Vault role, or the role was assigned at the wrong scope.

Resolution:

1. Verify **Key Vault Secrets Officer** is assigned to the app registration service principal.
2. Confirm assignment scope is the target Key Vault.
3. Wait for role propagation, then retry.

### Authentication failed for the target

Possible cause: incorrect tenant ID, client ID, or client secret.

Resolution:

1. Re-check tenant ID and client ID from the app overview.
2. Create a new client secret if the previous secret is expired or unavailable.
3. Update the Akeyless Azure target with the corrected values.

### Certificate operations fail but secret operations succeed

Possible cause: Key Vault certificates role is not assigned.

Resolution:

1. Assign **Key Vault Certificates Officer** to the same service principal.
2. Retry certificate list or update operations.

## Creating a Universal Secrets Connector from the Console

1. Log in to the Akeyless Console, and go to **Items > New > Universal Secrets Connector**.

2. Select the **Azure** secret type and click **Next**.

3. Define a **Name** of the Universal Secrets Connector, and specify the **Location** as a path to the virtual folder where you want to create the new Universal Secrets Connector, using slash `/` separators. If the folder does not exist, it will be created along with the Universal Secrets Connector.

4. Define the remaining settings as follows:

   * **Description:** Optional, enter a description of the Universal Secrets Connector.

   * **Tags:** Optional. Select one or more tags for the Universal Secrets Connector, or enter the name of a new tag to be added as part of the creation process.

   * **Delete Protection:** Optional, turn on this setting to protect the item from deletion

   * **Target:** Select an existing [Azure Target](https://docs.akeyless.io/docs/azure-targets).

   * **Gateway:** Select the desired corresponding Gateway.

   * **Key Vault Name:** The name of the Azure Key Vault you would like to connect with.

   * **USC Secret Prefix:** Optional, provide a prefix to be appended to any newly created secret.

   * **Use Prefix as Filter:** Optional, use the secret prefix as a filter.

   * **Use USC Tags:** Optional, provide tags to be appended to any newly created secret.

   * **Use Tags as Filter:** Optional, use the secret tags as a filter.

5. Click **Finish**.

## Azure Universal Secrets Details

Once connected to a Target, you can access the Universal Secrets Connector in your Akeyless Console page, which allows you to manage your Universal Secrets and display the following information about the secret:

* **Name:** Secret name

* **Type:** Secret type

* **Status:** Secret status of enabled/disabled

* **Expiration:** Secret date of expiration

More information and secret value can be viewed by selecting a specific secret, additionally, you will have the option to perform actions on the secret.

## Azure Universal Certificates Details

Once connected to a Target, you can access the Universal Secrets Connector in your Akeyless Console page, which allows you to manage your Universal Certificates and display the following information about the certificates:

* **Name:** Certificate name

* **Thumbprint:** The certificate thumbprint

* **Status:** Certificate status of enabled/disabled

* **Created:** Creation date

* **Expiration:** Certificate date of expiration

You can also import certificates in `pem` and `pfx` formats to the **Azure Key Vault** using the **Azure USC**

More information and secret value can be viewed by selecting a specific secret, additionally, you will have the option to perform actions on the secret.
