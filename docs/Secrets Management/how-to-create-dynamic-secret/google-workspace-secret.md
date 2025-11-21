---
title: Google Workspace Dynamic Secrets
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
**Google Workspace Dynamic Secret** can be used to add users to resources in the Google Workspace Admin Console using the user's email as a claim in the **IDP**. once configured, the users can use the **Google Workspace** Dynamic Secret to be added as one of the specified types in the Google Workspace Admin Console:

* **Role** - Assigns a user to an admin role in Google Workspace.
* **Group** - Adds the user to a group in Google Workspace.

# Prerequisites

* An [Akeyless Gateway](https://docs.akeyless.io/docs/api-gw)

* `ext_email`Subclaim exists in your IdP

* [GCP Target](https://docs.akeyless.io/docs/gcp-targets) with a **privileged service account**

## Create a Service Account in GCP

To create a **Google Workspace** Dynamic Secret, a Service Account that will be used for authentication is required.

Follow these steps to create a **Service Account** in **Google Cloud Platform**:

1. **Enable the Google Workspace API**: In **GCP**, search for `admin sdk api` and enable the **API** for the project.

2. **Create a Service Account** with the following roles:
   * **Group User** - Enables use access on group resources
   * **Service Account Key Admin** - Create and manage (and rotate) service account keys
   * **Service Account Token Creator** - Impersonate service accounts (create OAuth2 access tokens, sign blobs or JWT, etc)
   * **Service Account User** - Run operations as the service account

3. **Generate and download JSON key**: Click on the **Service Account** that was created, go to **Keys**, click **Add Key > Create new key > Json**. The key will be downloaded automatically to your computer.

4. **Delegate Domain-Wide Authority**: In the **Google Workspace Admin Console**, go to **Security** > **Access and data control > API controls** click on **Manage Domain Wide Delegation** > **Add new** > enter the client **ID** from the **JSON** file downloaded earlier.
   * In the same location, add the following scopes:
     ```
     https://www.googleapis.com/auth/admin.directory.group.member
     https://www.googleapis.com/auth/admin.directory.rolemanagement
     https://www.googleapis.com/auth/admin.directory.user.readonly
     https://www.googleapis.com/auth/admin.directory.customer.readonly
     ```

# Create a Dynamic Google Workspace Secret from the CLI

> 👍 Note
>
> We recommend using dynamic secrets with [Targets](https://docs.akeyless.io/docs/targets). While it saves time for multiple secret-level configurations by not requiring you to provide an [inline connection string](https://docs.akeyless.io/docs/rdp-dynamic-secrets#github-connection-strings) each time, it is also important for security streamlining. Using a Target allows you to rotate credentials without breaking the credential chain for the objects connected to the server used. Using inline will force you to change the credentials in each individual item instead of just the Target.

To create a dynamic Google Workspace secret from the CLI using an existing GCP target, run the following command:

```shell Akeyless CLI
akeyless dynamic-secret create google-workspace \
--name <Dynamic Secret Name> \
--gateway-url 'https://<Your-Akeyless-GW-URL:8000>'
--target-name <Target Name> \
--access-mode [group / role] \
--admin-name <admin user email> \
--group-name <group email> \
--group-role-type <OWNER/MANAGER/MEMBER> \
--role-name <admin role to assign to the user> \
--role-scope[=CUSTOMER] <[CUSTOMER/ORG_UNIT]>
```

**Or using an inline connection string** :

```shell Akeyless CLI
akeyless dynamic-secret create google-workspace \
--name <Dynamic Secret Name> \
--gateway-url 'https://<Your-Akeyless-GW-URL:8000>' \
--access-mode [group / role] \
--admin-name <admin user email> \
--group-name <group email> \
--group-role-type <OWNER/MANAGER/MEMBER> \
--role-name <admin role to assign to the user> \
--role-scope[=CUSTOMER] <[CUSTOMER/ORG_UNIT]> \
--gcp-key-file-path <service account path> \
--gcp-key <Base64-encoded service account text>
```

Where:

* `name`: A unique name of the dynamic secret. The name can include the path to the virtual folder where you want to create the new dynamic secret, using slash `/` separators. If the folder does not exist, it will be created together with the dynamic secret.

* `target-name`: A name of the target that enables connection to the Google Workspace. The name can include the path to the virtual folder where this target resides.

* `gateway-url`: Akeyless Gateway Configuration Manager URL (port `8000`).

* `access-mode`: Adding a user to an existing group or assigning an admin role to a user [`group` / `role`].

* `admin-email`: The email of the Google Workspace Account.

* `group-email`: A group email, relevant only for `group` access-mode.

* `group-role`: Group role [`OWNER`/`MANAGER`/`MEMBER`], relevant only for `group` access-mode.

* `role-name`: Name of the admin role to assign to the user, relevant only for `role` access-mode.

* `role-scope[=CUSTOMER]`: The scope in which this role is assigned [`CUSTOMER`/`ORG_UNIT`], relevant only for `role` access-mode.

* `fixed-user-claim-keyname[=ext_email]`: For externally provided users, denotes the key-name of IdP claim to extract the username from

* `gcp-key-file-path`: Path to file with the service account private key (relevant only when not using a Target)

* `gcp-key`: Base64-encoded service account private key text (relevant only when not using a Target)

You can find the complete list of parameters for this command in the [CLI Reference - Dynamic Secrets](https://docs.akeyless.io/docs/cli-reference-dynamic-secrets#/google-workspace) section.

# Fetch a Dynamic Google Workspace Secret value from the CLI

To fetch a dynamic Google Workspace secret value from the CLI, run the following command:

```shell Akeyless CLI
akeyless dynamic-secret get-value --name <Path to your dynamic secret>
```

# Create a Dynamic Secret for Google Workspace in the Akeyless Console

> 👍 Note
>
> To start working with dynamic secrets from the [Akeyless Console](https://docs.akeyless.io/docs/github-dynamic-secrets#create-a-dynamic-github-secret-in-the-akeyless-console), you need to configure the Gateway URL thus enabling communication between the Akeyless SaaS and the Akeyless Gateway.

1. Log in to the Akeyless Console, and go to **Items > New > Dynamic Secret**.

2. Select the **Workspace** secret type and click **Next**.

3. Define a **Name** of the dynamic secret, and specify the **Location** as a path to the virtual folder where you want to create the new dynamic secret, using slash `/` separators. If the folder does not exist, it will be created together with the dynamic secret.

4. Define the remaining parameters as follows:

* **Delete Protection**: When enabled, protects the secret from accidental deletion.
* **Target mode:** In this section, you can either select an existing GCP Target or specify details of the target GCP Service Account explicitly.

  * Use the **Choose an existing target** drop-down list to select the existing GCP Target.
  * Select the **Explicitly specify target properties** option, to provide details of the target GCP Service Account Key in the next step.
* **Access Mode**: Select the GCP access mode, either **Group** or **Role**.

  * **Group**: Add a user to an existing group.
  * **Role**: Assign an admin role to a user.
* **Group Name**: Email of the Group to add the user to.
* **Group Role**: **Owner, Manager or Member**
* **Role Name**: Name of the admin role to assign to the user.
* **Scope**: The scope in which this role is assigned **CUSTOMER**/**ORG_UNIT**.
* **Admin Email** : The email of the Google Workspace Account.
* **Sub Claim Name**: From which Sub Claim configured on your IDP to extract the user, where the default value is `ext_email`
* **User TTL**: Provide a time-to-live value for a dynamic secret (i.e., a token). When TTL expires, the token becomes obsolete.
* **Time Unit**: Select the time unit (seconds, minutes, hours) for the TTL value.
* **Gateway**: Select the Gateway through which the dynamic secret will create users.
* **Protection key**: To enable zero-Knowledge, select a key with a Customer Fragment. For more information, [read here](https://docs.akeyless.io/docs/implement-zero-knowledge).

# Fetch a Dynamic Google Workspace Secret value from the Akeyless Console

1. Log in to the Akeyless Console, and go to **Items**.

2. Browse to the folder where you created a dynamic secret.

3. Select the secret and click **Get Dynamic Secret** button.
