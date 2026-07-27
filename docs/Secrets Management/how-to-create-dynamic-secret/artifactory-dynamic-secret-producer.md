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
You can create an Artifactory dynamic secret to allow users to dynamically receive short-lived access tokens to interact with a JFrog Artifactory server (`v5.0.0` or later) by way of its [API](https://jfrog.com/help/r/jfrog-rest-apis/artifactory-rest-apis).

For more information on how to use access tokens in Artifactory, see the [JFrog Artifactory documentation](https://jfrog.com/help/r/jfrog-platform-administration-documentation/access-tokens).

When a client requests a dynamic secret value, the Akeyless Platform connects to the Artifactory through your [Gateway](https://docs.akeyless.io/docs/gateway-overview) and generates a temporary access token.

# Prerequisites

- An [Akeyless Gateway](https://docs.akeyless.io/docs/gateway-overview)
- [Artifactory Target](https://docs.akeyless.io/docs/artifactory-targets)

## Create a Dynamic Artifactory Secret with the CLI

<Callout icon="ℹ️" theme="info">
  ### **Note:**

  We recommend using Dynamic Secrets with [a Target](https://docs.akeyless.io/docs/artifactory-targets). While it saves time for multiple secret-level configurations by not requiring you to provide an [inline connection string](https://docs.akeyless.io/docs/artifactory-dynamic-secret-producer#inline-connection-strings) each time, it is also important for security streamlining. Using a target allows you to rotate credentials without breaking the credential chain for the objects connected to the server used, using inline will force you to go and change the credentials in each individual item instead of just the target.
</Callout>

To create a dynamic Artifactory secret with the CLI using an existing [Artifactory Target](https://docs.akeyless.io/docs/artifactory-targets), run the following command:

```shell
akeyless dynamic-secret create artifactory \
--name <Dynamic Secret Name> \
--target-name <Target Name> \
--gateway-url 'https://<Your-Akeyless-GW-URL>:8000' \
--artifactory-token-scope <Space-separated list of scopes> \
--artifactory-token-audience <Space-separated list of instances>
```

Where:

- `name`: A unique name of the dynamic secret. The name can include the path to the virtual folder where you want to create the new dynamic secret, using slash `/` separators. If the folder does not exist, it will be created together with the dynamic secret.

- `target-name`: A name of the target that enables connection to the Artifactory server. The name can include the path to the virtual folder where this target resides.

- `gateway-url`: Akeyless Gateway URL.

- `artifactory-token-scope`: The scope to assign to the temporary token. It is provided as a space-separated list of scopes, for example, `member-of-groups:readers`.

- `artifactory-token-audience`: A space-separated list of other Artifactory instances or services that should accept this token. For example, to accept all JFrog Artifactory instances, use `jfrt@*`.

You can find the complete list of parameters for this command in the [CLI Reference - Dynamic Secrets](https://docs.akeyless.io/docs/cli-reference-dynamic-secrets#artifactory) section.

## Fetch a Dynamic Artifactory Secret Value with the CLI

To fetch a dynamic Artifactory secret value with the CLI, run the following command:

```shell
akeyless dynamic-secret get-value --name <Path to your dynamic secret>
```

## Create a Dynamic Artifactory Secret in the Akeyless Console

<Callout icon="ℹ️" theme="info">
  ### **Note:**

  To start working with Dynamic Secrets from the [Akeyless Console](https://docs.akeyless.io/docs/artifactory-dynamic-secret-producer#/create-a-dynamic-artifactory-secret-in-the-akeyless-console), you need to configure the [Akeyless Gateway](https://docs.akeyless.io/docs/gateway-overview) URL thus enabling communication between the Akeyless SaaS and the Akeyless Gateway.
</Callout>

1. Log in to the Akeyless Console, and go to **Items > New > Dynamic Secret**.

2. Select the Artifactory secret type and click **Next**.

3. Define a **Name** of the dynamic secret, and specify the **Location** as a path to the virtual folder where you want to create the new dynamic secret, using slash `/` separators. If the folder does not exist, it will be created together with the dynamic secret.

4. Define the remaining settings as follows:

   - **Delete Protection**: When enabled, protects the secret from accidental deletion.
   - **Target:** Select an existing [Artifactory Target.](https://docs.akeyless.io/docs/artifactory-targets)
   - **Token Scope:** Specify a scope (or a space-separated list of scopes) to assign to the temporary token.
   - **Token Audience:** Specify a space-separated list of other JFrog Artifactory instances or services that should accept this token. The default value is the JFrog Artifactory service ID instance that created this token. For example, to accept all JFrog Artifactory instances, type `jfrt@*`.
   - **Custom Username Template:** Set a [custom username template](https://docs.akeyless.io/docs/dynamic-secrets-user-templating) for the generated user.
   - **User TTL:** Provide a time-to-live value for a dynamic secret (that is, a token).
     When TTL expires, the token becomes obsolete.
   - **Time Unit:** Select the time unit (seconds, minutes, hours) for the TTL value.
   - **Gateway:** Select the Gateway through which the dynamic secret will create users.
   - **Protection key**: To enable zero-Knowledge, select a key with a Customer Fragment. Read more about [Zero-Knowledge Encryption](https://docs.akeyless.io/docs/gateway-zero-knowledge).

5. Click **Finish**.

## Fetch a Dynamic Artifactory Secret Value from the Akeyless Console

1. Log in to the Akeyless Console, and go to **Items**.

2. Browse to the folder where you created a dynamic secret.

3. Select the secret and click the **Get Dynamic Secret** button.

<br />
