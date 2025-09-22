---
title: Azure Rotated Secret
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
You can create Rotated Secrets for Azure Apps and Azure Storage Account. Before you get started, ensure you have a [Target](doc:azure-targets) for your [Azure App](https://docs.akeyless.io/docs/create-an-azure-ad-app-service-account) or for your [Azure Storage Account](doc:azure-targets). 

The target must include the Azure tenant ID and client ID, as well as a client secret for a privileged App authorized to rotate credentials.

When a client requests a Rotated Secret value, the Akeyless Platform connects to the Azure App through your [Gateway](https://docs.akeyless.io/docs/api-gw) to rotate the Key of the target Azure App.

# Prerequisites

[Azure AD App](https://docs.akeyless.io/docs/create-an-azure-ad-app-service-account) or an [Azure AD Storage Account](https://docs.microsoft.com/en-us/azure/storage/common/storage-account-keys-manage?tabs=azure-portal#manually-rotate-access-keys) 

**Azure permissions description** 

| Action                          | Permissions \\ Role                                            |
| :------------------------------ | :------------------------------------------------------------- |
| To`Rotate` Application Secret   | `Application.ReadWrite.OwnedBy` or `Application.ReadWrite.All` |
| To`Reset password`for user      | `User-PasswordProfile.ReadWrite.All`                           |
| To`Rotate storage account keys` | `Storage Account Key Operator Service Role`                    |

Where:

* `Application.ReadWrite.OwnedBy`: Allows reading and writing of properties for applications owned by the user. 

* `Application.ReadWrite.All`: Allows read and write access to all applications in **Azure Active Directory**. 

* `User-PasswordProfile.ReadWrite.All`: Allows the app to read and write password profiles and reset passwords for all users.

* `Storage Account Key Operator Service Role`: Allows listing and regenerating keys on Storage Accounts. For more information, see the [Azure built-in roles](https://learn.microsoft.com/en-us/azure/role-based-access-control/built-in-roles/storage#storage-account-key-operator-service-role) documentation. 

For more information, see the Microsoft Graph [permissions reference](https://learn.microsoft.com/en-us/graph/permissions-reference) 

# Create a Rotated Azure Secret from the CLI

To create a Rotated Azure Secret using the Akeyless CLI, run the following command:

```shell Akeyless CLI
akeyless rotated-secret create azure \
--name <Rotated Secret name> \
--gateway-url 'https://<Your-Akeyless-GW-URL:8000>' \
--target-name <target name to associate> \
--authentication-credentials <use-user-creds|use-target-creds> \
--rotator-type <azure-storage-account|api-key|target|password> \
--api-id <client id> \
--api-key <client secret> \
--app-id <ID of the low-privileged app holding the secret to rotate>
```

Where:

* `name`: A unique name of the Rotated Secret. The name can include the path to the virtual folder where you want to create the new Rotated Secret, using slash `/` separators. If the folder does not exist, it will be created together with the Rotated Secret.

* `gateway-url`: Akeyless Gateway Configuration Manager URL (port `8000`).

* `target-name`: The name of the [Azure Target](doc:azure-targets) with which the Rotated Secret should be associated.

* `authentication-credentials`: Determines how to connect to the target Azure App.
  * `use-user-creds` - Use credentials defined on the Rotated Secret item.
  * `use-target-creds` - Use credentials of the privileged Azure App defined inside the [Azure Target](doc:azure-targets) item.

> 👍 Note
>
> Select `use-target-creds` if the Rotated Secret target App is not authorized to change its own client secret, and the privileged [Azure Target](doc:azure-targets) App is required to change the client secret on behalf of the Rotated Secret target App.

* `rotator_type`: The type of credentials to be rotated. For [Azure Target](doc:azure-targets), choose:
  * `api-key` - to rotate the client secret specified in the Rotated Secret
  * `target` - to rotate the client secret of the privileged App specified in the [Azure Target](doc:azure-targets)
  * `password` - to rotate a user password in Azure Entra
  * `azure-storage-account` - to rotate Azure Storage Account Key

* `api-id`: The client secret ID of the Azure App whose client secret should be rotated.  If left empty, the rotated secret will try to create a new secret and manage its rotation only. **Note** when  `api-id` is not provided, upon successful creation, the Azure Secret Key will be automatically created, and upon deletion of the Rotated Secret item using the `rotated-secret delete` command. , the Azure Secret Key will be deleted from the cloud as well.

* `api-key`: The client's secret to rotate.

* `app-id`: The ID of the Azure App that holds the secret being rotated.

* `username`: The user principal name to rotate his password (relevant only for `rotator-type=password`)

* `storage-account-key-name`: Provide the storage account key name `[key1/key2/kerb1/kerb2]` (relevant only for `rotator-type=azure-storage-account`)

* `explicitly-set-sa[=false]`: If set, explicitly provide the storage account details `[true/false]`
  * `resource-group-name`: The resource group name (only relevant when `explicitly-set-sa=true`)
  * `resource-name`: The name of the storage account (only relevant when `explicitly-set-sa=true`)

* `grace-rotation`: A boolean flag, when enabled, a graceful mode of rotation will be conducted, where only the older secret will be rotated. When there is only one secret, a new version will be created - to maintain 2 values at the same time.  Relevant only for **Client Secret**.

* `auto-rotate`: Enable auto-rotation if you need to update the secret regularly. If this value is set to **true**, specify the `rotation-interval` in days, and optionally also the `rotation-hour`.
  * `grace-rotation-interval` and `grace-rotation-hour` relevant only when `grace-rotation` is **enabled**, if not provided, the main `rotation-interval` settings will take place.

You can find the complete list of parameters for this command in the [CLI Reference - Rotated Secrets](https://docs.akeyless.io/docs/cli-reference-rotated-secrets#p-stylecolorblueazurep) section.

# Create a Rotated Azure Secret in the Akeyless Console.

> 👍 Note
>
> To start working with Rotated Secrets from the [Akeyless Console](https://docs.akeyless.io/docs/create-an-azure-rotated-secret#create-a-rotated-azure-secret-in-the-akeyless-console), you need to configure the [Gateway](https://docs.akeyless.io/docs/api-gw) URL thus enabling communication between the Akeyless SaaS and the Akeyless Gateway.

1. Log in to the Akeyless Console, and go to **Items > New > Rotated Secret > Azure**.

2. Define a **Name** of the Rotated Secret, and specify the **Location** as a path to the virtual folder where you want to create the new Rotated Secret, using slash `/` separators. If the folder does not exist, it will be created together with the Rotated Secret.

3. Define the remaining settings as follows:

* **Delete Protection:** When enabled, protects the Rotated Secret from accidental deletion.
* **Target:** Defines the name of the [Azure Target](doc:azure-targets) to be associated with the Rotated Secret. 

> 👍 Note
>
> You need to select the Rotator Type first, and then only those targets appear in the list that use the corresponding type of credentials.

* **Authenticate with the following credentials:** Determines how to connect to the target Azure App:

  * **User credentials:** Use credentials defined inside the Rotated Secret item.
  * **Target credentials:** Use credentials of the privileged App defined inside the [Azure Target](doc:azure-targets) item.

> 👍 Note
>
> Select **Target credentials** if the Rotated Secret target App is not authorized to change its own client secret, and the privileged [Azure Target](doc:azure-targets) App is required to change the client secret on behalf of the Rotated Secret target App.

* **Rotator type:** Determines the rotator type:
  * **API Key**: Rotates the client secret defined inside the Rotated Secret item.
  * **Target**: Rotates the client secret of the privileged App defined inside the [Azure Target](doc:azure-targets) item.
  * **Password**: To rotate a user password in Azure Entra.
  * **Azure Storage Account**: To rotate a storage account based on the [Azure Target](doc:azure-targets) details or provide them explicitly.

* **Access Key ID:** Defines the client secret ID of the Azure App for which the Access Key should be rotated.

* **Access Key:** Defines the client secret to rotate.

* **Application ID:** Defines the ID of the Azure App that holds the secret being rotated.

* **Username**: The user's principal name to rotate his password (relevant only for **Password Rotator type**)

* **Storage Account Key Name** :  Defines the storage account Key name (relevant only for **Azure Storage Account**)
  * **Resource Group Name** : Resource group name, relevant only when **Storage Account Details** are provided explicitly.
  * **Resource Name** : Resource name, relevant only when **Storage Account Details** are provided explicitly.

> 👍 Note
>
> You can rotate the client secret for the [Azure Target](doc:azure-targets) too by creating a Rotated Secret with the **Rotator type** set to **Target**. When you're using a **Target** rotator, the access role with which this Rotated Secret is associated must have read and update permissions on the corresponding Target.

* **Gateway:** Select the Gateway through which the secret will be rotated.

* **Protection key**: To enable zero-Knowledge, select a key with a Customer Fragment. For more information, [read here](doc:implement-zero-knowledge).

* **Graceful Rotation:**  When enabled, a graceful mode of rotation will be conducted, where only the older secret will be rotated. When there is only one secret, a new version will be created to maintain 2 values at the same time.  Relevant only for **Client Secret**.

* **Auto rotate:** Determines if automatic rotation is enabled.

* **Rotation interval (in days):** Defines the number of days (1-365) to wait between automatic client secret rotations when **Auto Rotate** is enabled.

* **Rotation hour (local time zone):** Defines the time when the client secret should be rotated if **Auto Rotate** is enabled.

* **Graceful Rotation Interval (in days):**  Specifies the number of days (range: 1–365) to wait between the main **Rotation Interval** and the **Grace Rotation**. This setting is applicable only when both Auto Rotate and Graceful Rotation are enabled. If left empty, the system will apply the main **Rotation Interval** to both versions of the secret.

* **Rotation Notification**: If you wish to get a notification before the next **Automatic Rotation**, click on ⊕ Add Notification and adjust the day count to any number you desire. This can be done multiple times to be notified more than once.

* **Delete Protection:** When enabled, it protects the Rotated Secret from accidental deletion.

4. Click **Finish**.
