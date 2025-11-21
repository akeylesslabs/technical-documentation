---
title: Azure AD Targets
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
You can define an Azure AD target to be used with [Azure AD dynamic secrets](https://docs.akeyless.io/docs/azure-ad-dynamic-secrets) or [Azure AD rotated secrets](https://docs.akeyless.io/docs/create-an-azure-rotated-secret). Having an Azure AD target will allow you to conserve the credentials chain between all of your dynamic secrets, as it is possible to point a target at a rotated secret, or to manually edit credentials in the target instead of having to change them individually for connecting items. Creating an Azure AD target requires an [Azure App ](https://learn.microsoft.com/en-us/entra/identity-platform/howto-create-service-principal-portal)to be configured in your Azure environment.

# Create an Azure AD Target in the CLI

To create an Azure AD target from the CLI, run the following command:

```shell Akeyless CLI
akeyless target create azure \
--name <target name> \
--client-id <Azure client/application id> \
--tenant-id <Azure tenant id> \
--client-secret <Azure client secret>
```

Where:

* `name`: A unique name of the target. The name can include the path to the virtual folder where you want to create the new target, using slash `/` separators. If the folder does not exist, it will be created together with the target.

Set the following:

* `client-id`: The Application ID of the admin user that will be used to authenticate Akeyless with Azure.

* `tenant-id`: Your Azure Tenant ID.

* `client-secret`: The client secret of the admin user that will be used to authenticate Akeyless with Azure.

If you wish the target to reference a specific Storage Account, add the following parameters:

* `subscription-id`: The ID of a Subscription that contains the Azure Storage Account.

* `resource-group-name`: The name of the Resource Group to which your Azure Storage account belongs.

* `resource-name`: The name of the Azure Storage account.

You can find the complete list of parameters for this command in the [CLI Reference - Akeyless Targets](https://docs.akeyless.io/docs/cli-ref-targets#p-stylecolorblueazurep) section.

# Create an Azure Target in the Console

1. Log in to the Akeyless Console, and go to **Targets > New > Cloud (Azure AD)**.

2. Define a **Name** of the target, and specify the **Location** as a path to the virtual folder where you want to create the new target, using slash `/` separators. If the folder does not exist, it will be created together with the target

3. Select a **Protection key** with a Customer Fragment to enable Zero-Knowledge and click **Next**.\
   For more information, [read here](https://docs.akeyless.io/docs/implement-zero-knowledge).

4. Define the remaining parameters as follows:

* Choose your preferred authentication mode by selecting one of the options:
  * Check the **Use Credentials** radio button to authenticate with the Azure AD admin user credentials.
  * Check the **Use Gateway's Cloud Identity** option to authenticate with the Gateway's Cloud IAM.

> 👍 Note
>
> **Use Gateway's Cloud Identity** is relevant for cases where your Gateway uses Azure service principal to authenticate against Akeyless. For example, when you set up a [Dynamic Secret](https://docs.akeyless.io/docs/azure-ad-dynamic-secrets) for Azure AD, the target can be used for the temporary Azure service principals creation.

* If you selected the **Use Credentials**, provide the following:
  * **Client ID (Application ID):** Application ID of the admin user that will be used to authenticate Akeyless with Azure AD.
  * **Tenant ID:** Your Azure Tenant ID.
  * **Client Secret:** Client Secret of the admin user that will be used to authenticate Akeyless with Azure AD.

* If you selected the **Use Gateway's Cloud Identity**, skip to the next step.  

* If you wish the target to reference to a specific Storage Account, click **Next** and add the following parameters:
  * **Subscription ID:** Azure Subscription ID (If this target is for the Azure Storage account).
  * **Resource Group Name:** Resource Group name in your Azure Subscription.
  * **Resource Name:** Name of the relevant Resource.

5. Click **Finish**.
