---
title: Cloud Targets
excerpt: ''
deprecated: false
hidden: true
metadata:
  title: ''
  description: ''
  robots: index
next:
  description: ''
---
## Azure

You can define an Azure AD target to be used with [Azure AD Dynamic Secrets](https://docs.akeyless.io/docs/azure-ad-dynamic-secrets) or [Azure AD Rotated Secrets](https://docs.akeyless.io/docs/create-an-azure-rotated-secret).

### Create an Azure AD Target with the CLI

To create an Azure AD target with the CLI, run the following command:

```shell
akeyless create-azure-target \
--name <target name> \
--client-id <Azure client/application id> \
--tenant-id <Azure tenant id> \
--client-secret <Azure client secret>
```

Where:

* `name`: A unique name of the target. The name can include the path to the virtual folder where you want to create the new target, using slash `/` separators. If the folder does not exist, it will be created together with the target.

* `client-id`: The Application ID of the admin user that will be used to authenticate Akeyless with Azure.

* `client-secret`: The client secret of the admin user that will be used to authenticate Akeyless with Azure.

* `tenant-id`: Your Azure Tenant ID.

You can find the complete list of parameters for this command in the [CLI Reference - Targets](https://docs.akeyless.io/docs/cli-ref-targets#/azure) section.

### Create an Azure AD Target in the Akeyless Console

1. Log in to the Akeyless Console, and go to **Targets > New > Cloud Targets > Azure**.

2. Define a **Name** of the target, and specify the **Location** as a path to the virtual folder where you want to create the new target, using slash `/` separators. If the folder does not exist, it will be created together with the target

3. Choose your preferred authentication mode by selecting one of the options:

   * Check the **Use Credentials** radio button to authenticate with the Azure AD admin user credentials.

   * Check the **Use Gateway's Cloud Identity** option to authenticate with the Gateway's Cloud IAM.

    > 👍 Note
    >
    > **Use Gateway's Cloud Identity** relevant for cases where your Gateway uses Azure service principal to authenticate against Akeyless.
    > For example, when you set up a [Dynamic Secret](https://docs.akeyless.io/docs/azure-ad-dynamic-secrets) for Azure, the target can be used for the temporary Azure service principals creation.

4. Define the remaining parameters as follows:

    * **Azure Client ID (Application ID):** If you selected the **Use Credentials** option in the previous step, specify the Application ID of the admin user that will be used to authenticate Akeyless with Azure AD.

    * **Azure Client Secret:** Provide the client secret of the admin user that will be used to authenticate Akeyless with Azure AD.

    * **Azure Tenant ID:** Specify your Azure Tenant ID.

    * **Subscription ID:** If this target is for the Azure Storage Account, then provide Azure Subscription ID.

    * **Resource Group Name:** Specify the Resource Group name in your Azure Subscription.

    * **Resource Name:** Provide the name of the relevant Resource.

    * **Protection key:** To enable Zero-Knowledge, select a key with a Customer Fragment. For more information about Zero-Knowledge, see [Implement Zero Knowledge](https://docs.akeyless.io/docs/implement-zero-knowledge).

5. Click **Save**.

### Create an Azure Storage Account Target with the CLI

To create a new Azure Target for an Azure Storage Account, run the following command with the CLI:

```shell
akeyless create-azure-target \
--name <target name> \
--tenant-id <Azure Tenant ID> \
--client-id <Azure client id> \
--client-secret <Azure client secret> \
--subscription-id <Subscription ID> \
--resource-group-name <Resource Group name> \
--resource-name <Resource name>
```

Where:

* `name`: A unique name of the target. The name can include the path to the virtual folder where you want to create the new secret, using slash `/` separators. If the folder does not exist, it will be created together with the target.

* `tenant-id`: The ID of your Azure tenant.

* `client-id`: The client ID of the App with the “Storage Account Key Operator Service Role“ permissions that is assigned to the Azure Storage Account.

* `client-secret`: The client secret of the App with the “Storage Account Key Operator Service Role“ permissions that is assigned to the Azure Storage Account.

* `subscription-id`: The ID of a Subscription that contains the Azure Storage Account.

* `resource-group-name`: The name of the Resource Group to which your Azure Storage Account belongs.

* `resource-name`: The name of the Azure Storage Account.

## GCP

You can define a GCP target to be used with [GCP Dynamic Secrets](https://docs.akeyless.io/docs/gcp-dynamic-secrets).

### Create a GCP Target with the CLI

To create a GCP target with the CLI, run the following command:

```shell
akeyless create-gcp-target \
--name <target name> \
--gcp-key-file-path <Path to the service account private key> \
--gcp-sa-email <GCP service account email>
```

Where:

* `name`: A unique name of the target. The name can include the path to the virtual folder where you want to create the new target, using slash `/` separators. If the folder does not exist, it will be created together with the target.

* `gcp-key-file-path`: A path to the file with the base64-encoded private key of the service account.

* `gcp-sa-email`: The GCP service account email.

You can find the complete list of parameters for this command in the [CLI Reference - Targets](https://docs.akeyless.io/docs/cli-ref-targets#/gcp) section.

### Create a GCP Target in the Akeyless Console

1. Log in to the Akeyless Console, and go to **Targets > New > Cloud Targets > GCP**.

2. Define a **Name** of the target, and specify the **Location** as a path to the virtual folder where you want to create the new target, using slash `/` separators. If the folder does not exist, it will be created together with the target

3. Choose your preferred authentication mode by selecting one of the options:

   * Check the **Use Credentials** radio button to authenticate with the GCP admin user credentials.

   * Check the **Use Gateway's Cloud Identity** radio button to authenticate with the Gateway's Cloud IAM.

    > 👍 Note
    >
    > **Use Gateway's Cloud Identity** relevant for cases where your Gateway uses a GCP service account to authenticate against Akeyless.
    >
    > For example, when you set up a [Dynamic Secret](https://docs.akeyless.io/docs/gcp-dynamic-secrets) for GCP, the target can be used for the temporary GCP service account keys creation.

4. Define the remaining parameters as follows:

    * **Service Account Email:** If you selected the **Use Credentials** option in the previous step, specify the superuser service account email that will be used to authenticate Akeyless with GCP.

    * **Service Account Key:** Provide a Base64-encoded private key of the superuser service account.

    * **Protection key:** To enable Zero-Knowledge, select a key with a Customer Fragment. For more information about Zero-Knowledge, see [Implement Zero Knowledge](https://docs.akeyless.io/docs/implement-zero-knowledge).

5. Click **Save**.
