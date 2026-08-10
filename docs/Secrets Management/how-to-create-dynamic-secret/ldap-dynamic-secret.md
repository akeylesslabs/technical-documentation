---
title: LDAP Dynamic Secrets
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
You can define a dynamic LDAP secret to dynamically generate LDAP access credentials. When a client requests the dynamic secret value, the [Akeyless Gateway](https://docs.akeyless.io/docs/gateway-overview) connects to your LDAP server and generates a temporary set of restricted access credentials.

## Prerequisites

- An [Akeyless Gateway](https://docs.akeyless.io/docs/gateway-overview) with network access to the LDAP server.

- An [LDAP Target](https://docs.akeyless.io/docs/ldap-target)

- LDAP server with a privileged LDAP User.

## Create a Dynamic LDAP Secret with the CLI

To create a dynamic LDAP secret with the CLI using an existing [LDAP Target](https://docs.akeyless.io/docs/ldap-target), run the following command:

```shell
akeyless dynamic-secret create ldap \
--name <Dynamic Secret Name> \
--target-name <Target Name> \
--gateway-url 'https://<Your-Akeyless-GW-URL>:8000' \
--user-dn <User Base DN> \
--password-length 16
```

Where:

- `name`: A unique name of the dynamic secret. The name can include the path to the virtual folder where you want to create the new dynamic secret, using slash `/` separators. If the folder does not exist, it will be created together with the dynamic secret.

- `target-name`: A name of the target that enables connection to the LDAP server. The name can include the path to the virtual folder where this target resides.

- `gateway-url`: Akeyless Gateway URL (port `8000`).

- `user-dn`: User Base DN.

- `password-length`: **Optional** The temporary user password length.

- `external-username[=false]`: Externally provided username

- `fixed-user-claim-keyname[=ext_username]`: For externally provided users, denotes the key-name of IdP claim to extract the username from (relevant only for external-username=true)

You can find the complete list of parameters for this command in the [CLI Reference - Dynamic Secrets](https://docs.akeyless.io/docs/cli-reference-dynamic-secrets#ldap) section.

## Fetch a Dynamic LDAP Secret Value with the CLI

To fetch a dynamic LDAP secret value with the CLI, run the following command:

```shell
akeyless dynamic-secret get-value --name <Path to your dynamic secret>
```

## Create a Dynamic LDAP Secret in the Akeyless Console

<Callout icon="ℹ️" theme="info">
  ### **Note:**

  To start working with Dynamic Secrets from the [Akeyless Console](https://docs.akeyless.io/docs/ldap-dynamic-secret#create-a-dynamic-ldap-secret-in-the-akeyless-console), you need to configure the Gateway URL thus enabling communication between the Akeyless SaaS and the Akeyless Gateway.
</Callout>

1. Log in to the Akeyless Console, and go to **Items > New > Dynamic Secret**.

2. Select the LDAP secret type and click **Next**.

3. Define a **Name** of the dynamic secret, and specify the **Location** as a path to the virtual folder where you want to create the new dynamic secret, using slash `/` separators. If the folder does not exist, it will be created together with the dynamic secret.

4. Define the remaining parameters as follows:

   - **Delete Protection**: When enabled, protects the secret from accidental deletion.
   - **Target:** Select an existing [LDAP Target](https://docs.akeyless.io/docs/ldap-target).
   - **User Base DN:** Specify user base DN settings.
   - **LDAP User Attribute:** Specify the default value CN.
   - **Externally Provided Username:** Select this checkbox to add an existing user based on the user identity which issues the secret value. It is relevant only when authenticating using an external IdP.
     - **Override:** Explicitly enter the username.
     - **Extract:** Extract the user from a Sub Claim configured on your IdP, where the default value is `ext_username`
   - **Custom Username Template:** Set a [custom username template](https://docs.akeyless.io/docs/dynamic-secrets-user-templating) for the generated user (relevant only when **not using** externally provided username).
   - **User TTL:** Provide a time-to-live value for a dynamic secret (that is, a token). When TTL expires, the token becomes obsolete.
   - **Temporary Password Length:** Set the length of the temporary password.
   - **Time Unit:** Select the time unit (seconds, minutes, hours) for the TTL value.
   - **Gateway:** Select the Gateway through which the dynamic secret will create users.
   - **Protection key**: To enable zero-Knowledge, select a key with a Customer Fragment. For more information, [read here](https://docs.akeyless.io/docs/gateway-zero-knowledge).

5. Click **Finish**.

## Fetch a Dynamic LDAP Secret Value from the Akeyless Console

1. Log in to the Akeyless Console, and go to **Items**.

2. Browse to the folder where you created a dynamic secret.

3. Select the secret and click the **Get Dynamic Secret** button.

## Username Length Policy

To control the temporary username policy, you can add to your Gateway deployment the following environment variable:

- `LDAP_USERNAME_LEN`

Or using the [Custom Username template for Dynamic Secrets](https://docs.akeyless.io/docs/dynamic-secrets-user-templating) mechanism
