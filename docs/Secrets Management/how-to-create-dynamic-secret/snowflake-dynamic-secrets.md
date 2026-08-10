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
You can use Akeyless Dynamic Secrets to generate access credentials for Snowflake. To do this, configure a dynamic secret with the details required for Akeyless to authenticate and communicate with the relevant Snowflake account.

## Prerequisites

- An [Akeyless Gateway](https://docs.akeyless.io/docs/gateway-overview)

- A [Snowflake Target](https://docs.akeyless.io/docs/database-targets#snowflake)

- Snowflake privileged account: To create a Snowflake dynamic secret, ensure that you have a Snowflake account and credentials for the admin user (with the `USERADMIN` role or higher)

## Create a Snowflake Dynamic Secret with the CLI

To create a dynamic Snowflake secret with the CLI using the existing [Snowflake Target](https://docs.akeyless.io/docs/database-targets#snowflake), run the following command:

```shell
akeyless dynamic-secret create snowflake \
--name <New Secret Name> \
--target-name <Target Name> \
--gateway-url 'https://<Your-Akeyless-GW-URL>:8000' \
--role <New User Role> \
--warehouse <Wahehouse Name> \
--password-length 16
```

Where:

- `name`: A unique name of the dynamic secret. The name can include the path to the virtual folder where you want to create the new dynamic secret, using slash `/` separators. If the folder does not exist, it will be created together with the dynamic secret.

- `target-name`: A name of the target that enables connection to the Snowflake account. The name can include the path to the virtual folder where this target resides.

- `gateway-url`: Akeyless Gateway URL (port `8000`).

- `--auth-mode[=password]`: The authentication mode for the temporary user, password or key.

- `--key-algo[=RSA2048]`: The temporary key algorithm to generate

- `role`: The role to assign to the temporary user.

- `warehouse`: A Snowflake target Warehouse name.

- `password-length`: **Optional** The temporary user password length.

another alternative to the Snowflake login is to use a private RSA key:

- `snowflake-api-private-key`: An RSA type private key that has access to the Snowflake account, in a Base64-encoded format.

- `snowflake-api-private-key-file-name`: Alternatively, you can use the path to a .pem file containing the key.

- `snowflake-api-private-key-passphrase`: The passphrase needed to use the key.

You can find the complete list of parameters for this command in the [CLI Reference - Dynamic Secrets](https://docs.akeyless.io/docs/cli-reference-dynamic-secrets#snowflake) section.

## Fetch a Dynamic Snowflake Secret Value with the CLI

To fetch a dynamic Snowflake secret value with the CLI, run the following command:

```shell
akeyless dynamic-secret get-value --name <Path to your dynamic secret>
```

## Create a Dynamic Snowflake Secret in the Akeyless Console

<Callout icon="ℹ️" theme="info">
  ### **Note:**

  To start working with Dynamic Secrets from the [Akeyless Console](https://docs.akeyless.io/docs/snowflake-dynamic-secrets?isFramePreview=true#fetch-a-dynamic-snowflake-secret-value-from-the-akeyless-console), you need to configure the Gateway URL thus enabling communication between the Akeyless SaaS and the Akeyless Gateway.
</Callout>

1. Log in to the Akeyless Console, and go to **Items > New > Dynamic Secret**.

2. Select the Snowflake secret type and click **Next**.

3. Define a **Name** of the dynamic secret, and specify the **Location** as a path to the virtual folder where you want to create the new dynamic secret, using slash `/` separators. If the folder does not exist, it will be created together with the dynamic secret.

4. Define the remaining parameters as follows:

   - **Delete Protection**: When enabled, protects the secret from accidental deletion.
   - **Target:** Select an existing [Snowflake Target](https://docs.akeyless.io/docs/database-targets#snowflake).
   - **User Role:** Enter the Snowflake role to be assigned to temporary users.
   - **Warehouse Name:** Enter the name of the target Snowflake warehouse.
   - **Authentication Mode**: The method by which the authentication will be accomplished with
     - **Password:** For authentication using **Username** and **Password**.
     - **Key** For authentication using **RSA Key**.
   - **Algorithm**: The RSA key algorithm, (relevant only for **Key** Authentication Mode).
   - **User TTL:** Provide a time-to-live value for a dynamic secret (that is, a token). When TTL expires, the token becomes obsolete.
   - **Custom Username Template:** Set a [custom username template](https://docs.akeyless.io/docs/dynamic-secrets-user-templating) for the generated user.
   - **Temporary Password Length:** Set the length of the temporary password.
   - **Time Unit:** Select the time unit (seconds, minutes, hours) for the TTL value.
   - **Gateway:** Select the Gateway through which the dynamic secret will create users.
   - **Protection key**: To enable zero-Knowledge, select a key with a Customer Fragment. For more information, [read here](https://docs.akeyless.io/docs/gateway-zero-knowledge).

5. Click **Finish**.

## Fetch a Dynamic Snowflake Secret Value from the Akeyless Console

1. Log in to the Akeyless Console, and go to **Items**.

2. Browse to the folder where you created a dynamic secret.

3. Select the secret and click the **Get Dynamic Secret** button.

<br />
