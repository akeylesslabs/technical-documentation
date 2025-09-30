---
title: Azure AD Dynamic Secrets
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
You can define an Azure AD dynamic secret to dynamically generate access credentials in one of two modes:

1. Programmatic: Access Azure AD using a secret for a specific application.

2. Portal: Access Azure AD using a username and password.

# Prerequisites

* An [Akeyless Gateway](doc:api-gw)

* Azure AD Service Account

To provide access to the Akeyless Platform from Azure AD, create a **Registration for Application** within your Microsoft Identity Platform. This registration will serve as a service account to enable API calls from the Akeyless Platform.

To create a Service Account in your Azure AD, follow the guide on [how to create an Application Registration](https://docs.microsoft.com/en-us/azure/active-directory/develop/howto-create-service-principal-portal) in Azure Active Directory.

**Required Permissions by Action Type:**

| Action                           | Permissions                                                                | Usage                                     |
| :------------------------------- | :------------------------------------------------------------------------- | :---------------------------------------- |
| Create/Delete user               | User.ReadWrite.All, Directory.ReadWrite.All                                | Ephemeral Azure Web Portal Credentials    |
| Add user to group                | GroupMember.ReadWrite.All, Group.ReadWrite.All and Directory.ReadWrite.All | Ephemeral Azure Web Portal Credentials    |
| Add user role                    | RoleManagement.ReadWrite.Directory                                         | Ephemeral Azure Web Portal Credentials    |
| Create\Delete Application secret | Application.ReadWrite.OwnedBy, Application.ReadWrite.All                   | Ephemeral Azure Service Principal Secrets |

**Entra ID Custom Roles**

[Custom roles](https://learn.microsoft.com/en-us/entra/identity/role-based-access-control/custom-create?tabs=admin-center) in Entra ID allow you to define specific [permissions](https://learn.microsoft.com/en-us/entra/identity/role-based-access-control/custom-available-permissions) for users or groups. These roles help control access to resources and actions, ensuring users have only the permissions they need for their tasks.

for example, the `microsoft.directory/applications/credentials/update` permission, Allows the ability to update the certificates and client secrets properties on single-tenant and multitenant applications.

# Create a Dynamic Azure AD Secret from the CLI

> 👍 Note
>
> We recommend using dynamic secrets with [Targets](doc:azure-targets). It both saves time for multiple secret-level configurations (by not requiring you to provide an [inline connection string](https://docs.akeyless.io/docs/azure-targets#create-an-azure-target-from-the-cli) each time), and it's also important for security streamlining. Using a target allows you to rotate credentials without breaking the credential chain for the objects connected to the server used, using inline will force you to go and change the credentials in each individual item instead of just the target.

To create a dynamic Azure AD secret from the CLI using an existing [Azure Target](doc:azure-targets), run the following command:

```shell Akeyless CLI
akeyless dynamic-secret create azure \
--name <Dynamic Secret Name> \
--target-name <Target Name> \
--gateway-url 'https://<Your-Akeyless-GW-URL:8000>' \
--azure-user-portal-access <true|false> \
--azure-user-programmatic-access <true|false> \
--azure-app-obj-id <Azure App Object ID> \
--azure-user-principal-name <Azure User Principal Name> \
--fixed-user-only <true|false> \
--fixed-user-claim-keyname <Key name of the IdP claim> \
--password-length 16
```

Or using an inline connection string:

```shell Akeyless CLI
akeyless dynamic-secret create akeyless dynamic-secret get-valueazure \
--name <Dynamic Secret Name> \
--gateway-url 'https://<Your-Akeyless-GW-URL:8000>' \
--azure-user-portal-access <true|false> \
--azure-user-programmatic-access <true|false> \
--azure-app-obj-id <Azure App Object ID> \
--azure-user-principal-name <Azure User Principal Name> \
--fixed-user-only <true|false> \
--fixed-user-claim-keyname <Key name of the IdP claim> \
--azure-tenant-id <Azure Tenant ID> \
--azure-client-id <Azure Client ID> \
--azure-client-secret <Azure AD Client Secret>
```

Where:

* `name`: A unique name of the dynamic secret. The name can include the path to the virtual folder where you want to create the new dynamic secret, using slash `/` separators. If the folder does not exist, it will be created together with the dynamic secret.

* `target-name: A name of the [target](http://google.com) that enables connection to the Azure AD server. The name can include the path to the virtual folder where this target resides.

* `gateway-url`: Akeyless Gateway URL.

* `azure-user-portal-access`: Enable Azure AD user portal access.

* `azure-user-programmatic-access`: Enable Azure AD user programmatic access.

* `azure-app-obj-id`: Azure App Object ID (required if programmatic access is enabled).

* `azure-user-principal-name`: Azure Domain for your User Principal Name to be created (required if portal access is enabled).

* `fixed-user-only`: Allow access using the externally provided username.

* `fixed-user-claim-keyname`: For externally provided users, denotes the key name of the IdP claim to extract the username from.

* `password-length`: **Optional** The temporary user password length.

### Inline connection string

If you don't have an [Azure AD Target](doc:azure-targets) yet, you can use the command with your Azure AD connection settings:

* `azure-tenant-id`: Azure Tenant ID.

* `azure-client-id`: Azure Client ID (Application ID).

* `azure-client-secret`: Azure AD Client Secret.

You can find the complete list of parameters for this command in the [CLI Reference - Dynamic Secrets](https://docs.akeyless.io/docs/cli-reference-dynamic-secrets#p-stylecolorblueazurep) section.

# Fetch a Dynamic Azure AD Secret value from the CLI

To fetch a dynamic Azure AD secret value from the CLI, run the following command:

```shell Akeyless CLI
akeyless dynamic-secret get-value --name <Path to your dynamic secret>
```

# Create a Dynamic Azure AD Secret in the Akeyless Console

> 👍 Note
>
> To start working with dynamic secrets from the [Akeyless Console](https://docs.akeyless.io/docs/azure-ad-dynamic-secrets#create-a-dynamic-azure-ad-secret-in-the-akeyless-console), you need to configure the Gateway URL thus enabling communication between the Akeyless SaaS and the Akeyless Gateway.

1. Log in to the Akeyless Console, and go to **Items > New > Dynamic Secret**.

2. Select the Azure AD secret type and click **Next**.

3. Define a **Name** of the dynamic secret, and specify the **Location** as a path to the virtual folder where you want to create the new dynamic secret, using slash `/` separators. If the folder does not exist, it will be created together with the dynamic secret.

4. Define the remaining parameters as follows:

* **Delete Protection:** When enabled, it protects the secret from accidental deletion.

* **Target mode:** In this section, you can either select an existing Azure AD Target or specify details of the target Azure AD server explicitly (e.g., if you are not authorized to create and access Targets in the Akeyless Console).

  * Use the **Choose an existing target** drop-down list to select the existing [Azure AD Target](https://docs.akeyless.io/docs/cloud-targets).

  * Check the **Explicitly specify target properties**  to provide details of the target Azure AD in the next step.

* **Programmatic Access:** Select this radio button to create a new secret to access a specific App.

* **Portal Access:** Select this radio button to create a new user and password.

* **App Object ID:** Provide the ID of the App Object to access using a dynamic secret. (Required if **Programmatic Access** is selected.)

* **User Principal Name:** Provide your Azure Domain for the User Principal Name to be created. (Required if **Portal Access** is selected.)

* **User Groups Object ID:** Provide the ID of the Group Object to add the new user to this group. Multiple values should be separated by a comma. (If **Portal Access** is selected.)

* **User Roles Template ID:** Provide the ID of the Role Template to add this role to the new user. Multiple values should be separated by a comma. (If **Portal Access** is selected.)

* **Entra ID Administrative Unit**: Provide the Object ID of the Administrative Unit the user will be created in.

* **Externally Provided Username:** Select this checkbox to allow the dynamic secret engine to add and remove the assigned groups and roles for an existing user (instead of creating a new temporary user). (If **Portal Access** is selected.)

* **Extract username from the following claim (Key name):** Provide the name of the claim in the authentication token from which the "externally provided username" will be taken. The value should be either the full principal user name or the user display name.

* **User TTL:** Provide a time-to-live value for a dynamic secret (i.e., a token). When TTL expires, the token becomes obsolete.

* **Custom Username Template:** Set a [custom username template ](https://docs.akeyless.io/docs/dynamic-secrets-user-templating) for the generated user.

* **Temporary Password Length** Set the length of the temporary password.

* **Time Unit:** Select the time unit (seconds, minutes, hours) for the TTL value.

* **Gateway:** Select the Gateway through which the dynamic secret will create users.

* **Protection key**: To enable zero-Knowledge, select a key with a Customer Fragment. For more information, [read here](doc:implement-zero-knowledge).

5. If you checked the **Explicitly specify target properties** radio button, click **Next**.

6. Provide details of the target Azure AD server:

* **Client ID (Application ID):** The Application ID.

* **Tenant ID:** Your Azure Tenant ID.

* **Client Secret:** Your Azure Client Secret.

7. Click **Finish**.

# Fetch a Dynamic Azure AD Secret Value from the Akeyless Console

1. Log in to the Akeyless Console, and go to **Items**.

2. Browse to the folder where you created a dynamic secret.

3. Select the secret and click **Get Dynamic Secret** button.
