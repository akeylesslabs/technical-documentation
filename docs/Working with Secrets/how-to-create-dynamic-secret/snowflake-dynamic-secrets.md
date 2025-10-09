---
title: Snowflake Dynamic Secrets
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
You can use Akeyless dynamic secrets to generate access credentials for Snowflake. To do this, configure a dynamic secret with the details required for Akeyless to authenticate and communicate with the relevant Snowflake account.

# Prerequisites

* An [Akeyless Gateway](https://docs.akeyless.io/docs/api-gw)

* Snowflake privileged account: To create a Snowflake dynamic secret, ensure that you have a Snowflake account and credentials for the admin user (with the `USERADMIN` role or higher)

# Create a Snowflake Dynamic Secret from the CLI

> 👍 Note
>
> We recommend using dynamic secrets with [Targets](https://docs.akeyless.io/docs/targets). While it saves time for multiple secret-level configurations by not requiring you to provide an [inline connection string](https://docs.akeyless.io/docs/snowflake-dynamic-secrets#inline-connection-strings) each time, it is also important for security streamlining. Using a target allows you to rotate credentials without breaking the credential chain for the objects connected to the server used, using inline will force you to go and change the credentials in each individual item instead of just the target.

To create a dynamic Snowflake secret from the CLI using the existing [Snowflake Target](https://docs.akeyless.io/docs/database-targets#snowflake), run the following command:

```shell Akeyless CLI
akeyless dynamic-secret create snowflake \
--name <New Secret Name> \
--target-name <Target Name> \
--gateway-url 'https://<Your-Akeyless-GW-URL:8000>' \ 
--role <New User Role> \
--warehouse <Wahehouse Name> \
--password-length 16
```

Or using an inline connection strings/RSA private key:

```shell Inline Login
akeyless dynamic-secret create snowflake \
--name <Secret Name> \
--gateway-url 'https://<Your-Akeyless-GW-URL:8000>' \
--role <New User Role> \
--warehouse <Wahehouse Name> \
--account <Snowflake account name> \
--username <Snowflake username> \
--password <Snowflake password> \
--db-name <Database to which the generated credentials are restricted>
```
```shell RSA Private Key Login
akeyless dynamic-secret create akeyless dynamic-secret get-valuesnowflake \
--name <Secret Name> \
--gateway-url 'https://<Your-Akeyless-GW-URL:8000>' \
--role <New User Role> \
--warehouse <Wahehouse Name> \
--snowflake-api-private-key RSA Private key (base64 encoded)\
--snowflake-api-private-key-file-name The path to the file containing the private key\
--snowflake-api-private-key-passphrase The Private key passphrase
```

Where:

* `name`: A unique name of the dynamic secret. The name can include the path to the virtual folder where you want to create the new dynamic secret, using slash `/` separators. If the folder does not exist, it will be created together with the dynamic secret.

* `target-name`: A name of the target that enables connection to the Snowflake account. The name can include the path to the virtual folder where this target resides.

* `gateway-url`: Akeyless Gateway Configuration Manager URL (port `8000`).

* `--auth-mode[=password]`: The authentication mode for the temporary user, password or key.

* `--key-algo[=RSA2048]`: The temporary key algorithm to generate

* `role`: The role to assign to the temporary user.

* `warehouse`:  A Snowflake target Warehouse name.

* `password-length`: **Optional** The temporary user password length.

### Inline connection string

If you don't have [Snowflake Target](https://docs.akeyless.io/docs/database-targets#snowflake) yet, you can use the command with your Snowflake target connection string:

* `account`: The Snowflake account name in `xy12345.region.cloud_provider` format.

* `username`: The username for a Snowflake user administrator (with the `USERADMIN` role or higher).

* `password`: The password for the Snowflake user administrator account.

* `db-name`: The name of the target Snowflake database.

another alternative to the Snowflake login is to use a private RSA key:

* `snowflake-api-private-key`: An RSA type private key that has access to the Snowflake account, in a base64 encoded format.

* `snowflake-api-private-key-file-name`: Alternatively, you can use the path to a .pem file containing the key.

* `snowflake-api-private-key-passphrase`: The passphrase needed to use the key.

You can find the complete list of parameters for this command in the [CLI Reference - Dynamic Secrets](https://docs.akeyless.io/docs/cli-reference-dynamic-secrets#p-stylecolorbluesnowflakep) section.

# Fetch a Dynamic Snowflake Secret value from the CLI

To fetch a dynamic Snowflake secret value from the CLI, run the following command:

```shell Akeyless CLI
akeyless dynamic-secret get-value --name <Path to your dynamic secret>
```

# Create a Dynamic Snowflake Secret in the Akeyless Console

> 👍 Note
>
> To start working with dynamic secrets from the [Akeyless Console](https://docs.akeyless.io/docs/snowflake-dynamic-secret#create-a-dynamic-snowflake-secret-in-the-akeyless-console), you need to configure the Gateway URL thus enabling communication between the Akeyless SaaS and the Akeyless Gateway.

1. Log in to the Akeyless Console, and go to **Items > New > Dynamic Secret**.

2. Select the Snowflake secret type and click **Next**.

3. Define a **Name** of the dynamic secret, and specify the **Location** as a path to the virtual folder where you want to create the new dynamic secret, using slash `/` separators. If the folder does not exist, it will be created together with the dynamic secret.

4. Define the remaining parameters as follows:

* **Delete Protection**: When enabled, protects the secret from accidental deletion.
* **Target mode:** In this section, you can either select an existing Snowflake Target or specify details of the target Snowflake account explicitly (e.g., if you are not authorized to create and access Targets in the Akeyless Console).

  * Use the **Choose an existing target** drop-down list to select the existing Snowflake Target.

  * Select the **Explicitly specify target properties** to provide details of the target Snowflake account in the next step.
* **User Role:** Enter the Snowflake role to be assigned to temporary users.
* **Warehouse Name:** Enter the name of the target Snowflake warehouse.
* **Authentication Mode**: The method by which the authentication will be accomplished with
  * **Password:** For authentication using **Username** and **Password**.
  * **Key** For authentication using **RSA Key**.
* **Algorithm**: The RSA key algorithm, (relevant only for **Key** Authentication Mode).
* **User TTL:** Provide a time-to-live value for a dynamic secret (i.e., a token). When TTL expires, the token becomes obsolete.
* **Custom Username Template:** Set a [custom username template](https://docs.akeyless.io/docs/dynamic-secrets-user-templating) for the generated user.
* **Temporary Password Length** Set the length of the temporary password.
* **Time Unit:** Select the time unit (seconds, minutes, hours) for the TTL value.
* **Gateway:** Select the Gateway through which the dynamic secret will create users.
* **Protection key**: To enable zero-Knowledge, select a key with a Customer Fragment. For more information, [read here](https://docs.akeyless.io/docs/implement-zero-knowledge).

5. If you selected the **Explicitly specify target properties** option, click **Next**.

6. Provide details of the target Snowflake account:

   * **Account Name:** Enter the Snowflake account name in the `xy12345.region.cloud_provider` format.

   * **Account Username:** Enter the username for a Snowflake admin user (with the _USERADMIN_ role or higher).

   * **Account Password:** Enter the password for the Snowflake admin user account.

   * **DB Name:** Enter the name of the target Snowflake database.

7. Click **Finish**.

# Fetch a Dynamic Snowflake Secret value from the Akeyless Console

1. Log in to the Akeyless Console, and go to **Items**.

2. Browse to the folder where you created a dynamic secret.

3. Select the secret and click **Get Dynamic Secret** button.
