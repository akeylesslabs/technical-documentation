---
title: LDAP Dynamic Secret
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
You can define a dynamic LDAP secret to dynamically generate LDAP access credentials. When a client requests the dynamic secret value, the [Akeyless Gateway](doc:api-gw) connects to your LDAP server and generates a temporary set of restricted access credentials.

# Prerequisites

* An [Akeyless Gateway](doc:api-gw) with network access to the LDAP server.

* LDAP server with a privileged LDAP User.

# Create a Dynamic LDAP Secret from the CLI

> 👍 Note
>
> We recommend using dynamic secrets with [Targets](doc:targets). While it saves time for multiple secret-level configurations by not requiring you to provide an [inline connection string](https://docs.akeyless.io/docs/ldap-dynamic-secret#inline-connection-strings) each time, it is also important for security streamlining. Using a target allows you to rotate credentials without breaking the credential chain for the objects connected to the server used, using inline will force you to go and change the credentials in each individual item instead of just the target.

To create a dynamic LDAP secret from the CLI using an existing [LDAP Target](doc:ldap-target), run the following command: 

```shell Akeyless CLI
akeyless dynamic-secret create ldap \
--name <Dynamic Secret Name> \
--target-name <Target Name> \
--gateway-url 'https://<Your-Akeyless-GW-URL:8000>' \
--user-dn <User Base DN> \
--password-length 16
```

 Or using an inline connection string:

```shell Akeyless CLI
akeyless dynamic-secret create akeyless dynamic-secret get-valueldap \
--name <Dynamic Secret Name> \
--gateway-url 'https://<Your-Akeyless-GW-URL:8000>' \
--ldap-url <LDAP server URL> \
--bind-dn <LDAP Bind DN> \
--bind-dn-password <Password>\
--ldap-ca-cert <LDAP base-64 encoded CA Certificate> \
--user-dn <User Base DN>
```

Where:

* `name`: A unique name of the dynamic secret. The name can include the path to the virtual folder where you want to create the new dynamic secret, using slash `/` separators. If the folder does not exist, it will be created together with the dynamic secret.

* `target-name`: A name of the target that enables connection to the LDAP server. The name can include the path to the virtual folder where this target resides.

* `gateway-url`: Akeyless Gateway Configuration Manager URL (port `8000`).

* `user-dn`: User Base DN.

* `password-length`: **Optional** The temporary user password length.

* `external-username[=false]`: Externally provided username

* `fixed-user-claim-keyname[=ext_username]`: For externally provided users, denotes the key-name of IdP claim to extract the username from (relevant only for external-username=true)

### Inline connection string

If you don't have [LDAP Target](doc:ldap-target) yet, you can use the command with your LDAP target server connection string:

* `ldap-url`: The LDAP server URL.

* `bind-dn`: The LDAP Bind DN.

* `bind-dn-password`: The password for LDAP Bind DN.

* `ldap-ca-cert`: The LDAP base-64 encoded CA Certificate.

You can find the complete list of parameters for this command in the [CLI Reference - Dynamic Secrets](https://docs.akeyless.io/docs/cli-reference-dynamic-secrets#p-stylecolorblueldapp) section.

# Fetch a Dynamic LDAP Secret value from the CLI

To fetch a dynamic LDAP secret value from the CLI, run the following command: 

```shell Akeyless CLI
akeyless dynamic-secret get-value --name <Path to your dynamic secret>
```

# Create a Dynamic LDAP Secret in the Akeyless Console

> 👍 Note
>
> To start working with dynamic secrets from the [Akeyless Console](https://docs.akeyless.io/docs/ldap-dynamic-secret#create-a-dynamic-ldap-secret-in-the-akeyless-console), you need to configure the Gateway URL thus enabling communication between the Akeyless SaaS and the Akeyless Gateway.

1. Log in to the Akeyless Console, and go to **Items > New > Dynamic Secret**.

2. Select the LDAP secret type and click **Next**.

3. Define a **Name** of the dynamic secret, and specify the **Location** as a path to the virtual folder where you want to create the new dynamic secret, using slash `/` separators. If the folder does not exist, it will be created together with the dynamic secret.

4. Define the remaining parameters as follows:

* **Delete Protection**: When enabled, protects the secret from accidental deletion.
* **Target mode:** In this section, you can either select an existing [LDAP Target](doc:ldap-target) or specify details of the target LDAP server explicitly.

  * Use the **Choose an existing target** drop-down list to select the existing [LDAP Target](doc:ldap-target).

  * Check the **Explicitly specify target properties**  to provide details of the target LDAP Server in the next step.
* **User Base DN:** Specify user base DN settings.
* **LDAP User Attribute:** Specify the default value CN.
* **Externally Provided Username:** Select this checkbox to add an existing user based on the user identity which issues the secret value. It is relevant only when authenticating using an external IDP.
  * **Override:** Explicitly enter the username.
  * **Extract:** Extract the user from a Sub Claim configured on your IDP, where the default value is `ext_username`
* **Custom Username Template:** Set a [custom username template](https://docs.akeyless.io/docs/dynamic-secrets-user-templating) for the generated user (relevant only when **not using** externally provided username).
* **User TTL:** Provide a time-to-live value for a dynamic secret (i.e., a token). When TTL expires, the token becomes obsolete.
* **Temporary Password Length** Set the length of the temporary password.
* **Time Unit:** Select the time unit (seconds, minutes, hours) for the TTL value.
* **Gateway:** Select the Gateway through which the dynamic secret will create users.
* **Protection key**: To enable zero-Knowledge, select a key with a Customer Fragment. For more information, [read here](doc:implement-zero-knowledge).

5. If you selected the **Explicitly specify target properties**, click **Next**.

6. Provide details of the target LDAP server connection:

* **LDAP Server URL:** Specify the LDAP Server URL.

* **CA Certificate File Content:** Provide the base64-encoded CA Certificate to enable the secure connection.

* **LDAP Bind DN:** Provide Bind DN for authentication of a privileged user.

* **Password for LDAP Bind DN:** Provide the password of the privileged user for authentication.

7. Click **Finish**.

# Fetch a Dynamic LDAP Secret value from the Akeyless Console

1. Log in to the Akeyless Console, and go to **Items**.

2. Browse to the folder where you created a dynamic secret.

3. Select the secret and click **Get Dynamic Secret** button.

# Username Length Policy

To control the temporary username policy, you can add to your Gateway deployment the following environment variable: 

* `LDAP_USERNAME_LEN`

Or using the [Custom Username template for Dynamic Secrets](doc:dynamic-secrets-user-templating) mechanism
