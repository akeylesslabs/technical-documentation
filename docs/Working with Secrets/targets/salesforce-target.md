---
title: Salesforce Target
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
You can define a Salesforce target to be used in the [Akeyless KMS integration with Salesforce Shield](https://docs.akeyless.io/docs/salesforce-shield).

# Create a Salesforce Target in the CLI

To create a Salesforce target using the Akeyless CLI, use the following command:

```shell Akeyless CLI
akeyless target create salesforce \
--name <target name> \
--tenant-url <Salesforce tenant URL> \
--client-id <Oauth2 app client ID for connecting to Salesforce> \
--email <oauth2 app user email> \
--auth-flow <type of the auth flow> ('jwt' or 'user-password') \
#If using 'user-password' auth-flow, provide the following:
--client-secret <Oauth2 app client secret for connecting to Salesforce> \
--password <oauth2 app user password> \
--security-token <Oauth2 app user security token>
#Or If using 'jwt' auth-flow, provide the following:
--app-private-key-file-name <Name of the Base64 encoded PEM private key of the connected app> \
--app-private-key-data <Base64 encoded PEM private key of the connected app> #Used if 'app-private-key-file-name' was not provided
```

Where:

* `name`: A unique name for the target. The name can include a path to the virtual folder where you want to create a new target, using slash `/` separators. If the folder does not exist, it will be created together with the target.

* `tenant-url`: The URL of the Salesforce tenant.

* `client-id`: The Client ID of the `OAuth2.0` app to use for connecting to Salesforce.

* `email`: The email of the user attached to the `OAuth2.0` app that is used for connecting to Salesforce.

* `auth-flow`: The type of the auth flow, either `jwt` or `user-password`.

If using `user-password` `auth-flow` provide the following:

* `client-secret`: The client secret of the `OAuth2.0` app to use for connecting to Salesforce.

* `password`: The password of the user attached to the `OAuth2.0` app used for connecting to Salesforce.

* `security-token`: The security token of the user attached to the `OAuth2.0` app used for connecting to Salesforce.

Or if using `jwt` `auth-flow` provide the following:

* `app-private-key-file-name`: The name of the of the file containing a Base64 encoded `PEM` private key of the connected app.

* `app-private-key-data`: The Base64 encoded `PEM` private key of the connected app.\
  Note: Used if `app-private-key-file-name` was not provided.

You can find the complete list of parameters for this command in the [CLI Reference - Akeyless Targets](https://docs.akeyless.io/docs/cli-ref-targets#p-stylecolorbluesalesforcep) section.

# Create a Salesforce Target in the Console

1. Log in to the Akeyless Console, and go to **Targets > New > Cloud (Salesforce)**.

2. Define a **Name** of the target, and specify the **Location** as a path to the virtual folder where you want to create the new target, using slash `/` separators. If the folder does not exist, it will be created together with the target

3. Select a **Protection key** with a Customer Fragment to enable Zero-Knowledge and click **Next**.\
   For more information, [read here](doc:implement-zero-knowledge).

4. Define the parameters as follows:

* **Tenant URL:** Specify the URL of the Salesforce tenant.

* **Client ID:** Provide a Client ID of the `OAuth2.0` app to use for connecting to Salesforce.

* **Username:** Provide a username (usually, the email) of the user attached to the `OAuth2.0` app that is used for connecting to Salesforce.

* Choose your preferred authentication flow by selecting one of the options:

  * Check the **JWT** radio button to authenticate with JWT to connect to Salesforce.

  * Check the **User-Password** radio button to authenticate with the`OAuth2.0` app username and password to connect to Salesforce.

* If you selected the **JWT** radio button, provide **App Private key**, a Base64 encoded `PEM` of the connected app private key.

* If you selected the **User-Password** radio button, provide the following:
  * **Client Secret:** Client secret of the `OAuth2.0` app to use for connecting to Salesforce.
  * **Password:** Password of the user attached to the `OAuth2.0` app used for connecting to Salesforce.
  * **Security Token:** The Security token of the user attached to the `OAuth2.0` app used for connecting to Salesforce.

5. Define the remaining optional parameters as follows:

* **CA certificate name:** Specify the name of the certificate in the Salesforce tenant.
* **CA certificate:** Provide a Base64 encoded PEM cert to use when uploading a new key to Salesforce.\
  Note: Used if **CA certificate name** was not provided.

6. Click **Finish**.
