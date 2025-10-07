---
title: Artifactory Dynamic Secrets
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
You can create an Artifactory dynamic secret to allow users to dynamically receive short-lived access tokens to interact with a JFrog Artifactory server (`v5.0.0` or later) via its [API](https://www.jfrog.com/confluence/display/JFROG/Artifactory+REST+API).

For more information on how to use access tokens in Artifactory, see the [JFrog Artifactory documentation](https://www.jfrog.com/confluence/display/JFROG/Access+Tokens).

When a client requests a dynamic secret value, the Akeyless Platform connects to the Artifactory through your [Gateway](https://docs.akeyless.io/docs/api-gw) and generates a temporary access token.

# Create a Dynamic Artifactory Secret from the CLI

> 👍 Note
>
> We recommend using dynamic secrets with [a Target](doc:artifactory-targets) . While it saves time for multiple secret-level configurations by not requiring you to provide an [inline connection string](https://docs.akeyless.io/docs/artifactory-dynamic-secret-producer#inline-connection-strings) each time, it is also important for security streamlining. Using a target allows you to rotate credentials without breaking the credential chain for the objects connected to the server used, using inline will force you to go and change the credentials in each individual item instead of just the target.

To create a dynamic Artifactory secret from the CLI using an existing [Artifactory Target](doc:artifactory-targets) , run the following command:

```shell Akeyless CLI
akeyless dynamic-secret create artifactory \
--name <Dynamic Secret Name> \
--target-name <Target Name> \
--gateway-url 'https://<Your-Akeyless-GW-URL:8000>' \
--artifactory-token-scope <Space-separated list of scopes> \
--artifactory-token-audience <Space-separated list of instances>
```

Or using an inline connection string:

```shell Akeyless CLI
akeyless dynamic-secret create artifactory \
--name <Dynamic Secret Name> \
--gateway-url 'https://<Your-Akeyless-GW-URL:8000>' \
--artifactory-token-scope <Space-separated list of scopes> \
--artifactory-token-audience <Space-separated list of instances> \
--base-url <Artifactory REST URL> \
--artifactory-admin-name <Artifactory Admin username> \
--artifactory-admin-pwd <Artifactory Admin API Key or password>
```

Where:

* `name`: A unique name of the dynamic secret. The name can include the path to the virtual folder where you want to create the new dynamic secret, using slash `/` separators. If the folder does not exist, it will be created together with the dynamic secret.

* `target-name`: A name of the target that enables connection to the Artifactory server. The name can include the path to the virtual folder where this target resides.

* `gateway-url`: Akeyless Gateway URL.

* `artifactory-token-scope`: The scope to assign to the temporary token. It is provided as a space-separated list of scopes, for example, `member-of-groups:readers`.

* `artifactory-token-audience`: A space-separated list of other Artifactory instances or services that should accept this token. For example, to accept all JFrog Artifactory instances, use `jfrt@*`.

### Inline connection string

If you don't have an [Artifactory Target](doc:artifactory-targets) yet, you can use the command with your Artifactory target server connection string:

* `base-url`: The JFrog Artifactory REST URL, which must end with the `artifactory` postfix.
  For example, if you use your JFrog URL, this could be `http://myjfrog.acme.org/artifactory/`.

* `artifactory-admin-name`: The Artifactory user with privileges to create JWT tokens.

* `artifactory-admin-pwd`: The API key or password of the admin user.

You can find the complete list of parameters for this command in the [CLI Reference - Dynamic Secrets](https://docs.akeyless.io/docs/cli-reference-dynamic-secrets#p-stylecolorblueartifactoryp) section.

# Fetch a Dynamic Artifactory Secret value from the CLI

To fetch a dynamic Artifactory secret value from the CLI, run the following command:

```shell Akeyless CLI
akeyless dynamic-secret get-value --name <Path to your dynamic secret>
```

# Create a Dynamic Artifactory Secret in the Akeyless Console

> 👍 Note
>
> To start working with dynamic secrets from the [Akeyless Console](https://docs.akeyless.io/docs/artifactory-dynamic-secrets#create-a-dynamic-artifactory-secret-in-the-akeyless-console), you need to configure the [Akeyless Gateway](https://docs.akeyless.io/docs/api-gw) URL thus enabling communication between the Akeyless SaaS and the Akeyless Gateway.

1. Log in to the Akeyless Console, and go to **Items > New > Dynamic Secret**.

2. Select the Artifactory secret type and click **Next**.

3. Define a **Name** of the dynamic secret, and specify the **Location** as a path to the virtual folder where you want to create the new dynamic secret, using slash `/` separators. If the folder does not exist, it will be created together with the dynamic secret.

4. Define the remaining settings as follows:

* **Delete Protection**: When enabled, protects the secret from accidental deletion.
* **Target mode:** In this section, you can either select an existing [Artifactory Target](doc:artifactory-targets)  or specify details of the target Artifactory server explicitly.
* **Token Scope:** Specify a scope (or a space-separated list of scopes) to assign to the temporary token.
* **Token Audience:** Specify a space-separated list of other JFrog Artifactory instances or services that should accept this token. The default value is the JFrog Artifactory service ID instance that created this token. For example, to accept all JFrog Artifactory instances, type **jfrt@***.
* **Custom Username Template:** Set a [custom username template](https://docs.akeyless.io/docs/dynamic-secrets-user-templating) for the generated user.
* **User TTL:** Provide a time-to-live value for a dynamic secret (i.e., a token).
  When TTL expires, the token becomes obsolete.
* **Time Unit:** Select the time unit (seconds, minutes, hours) for the TTL value.
* **Gateway:** Select the Gateway through which the dynamic secret will create users.
* **Protection key**: To enable zero-Knowledge, select a key with a Customer Fragment. For more information, [read here](doc:implement-zero-knowledge).

5. If you selected the **Explicitly specify target properties** mode, click **Next**.

6. Provide details of the target Artifactory server:

* **Base URL:** Specify the JFrog Artifactory REST URL, which must end with the **artifactory** postfix.

For example, if you use your JFrog URL, this could be **[\<https://myjfrog.acme.org/artifactory/>](https://myjfrog.acme.org/artifactory/)**. Or, if you use your JFrog Artifactory server hostname and port, this could be **https://ARTIFACTORY_SERVER_HOSTNAME:8081/artifactory/**.

* **Admin Username:** Provide the name of the Artifactory user with privileges to create JWT tokens.

* **Admin API Key/Password:** Provide the admin user's API key or password.

7. Click **Finish**.

# Fetch a Dynamic Artifactory Secret value from the Akeyless Console

1. Log in to the Akeyless Console, and go to **Items**.

2. Browse to the folder where you created a dynamic secret.

3. Select the secret and click the **Get Dynamic Secret** button.
