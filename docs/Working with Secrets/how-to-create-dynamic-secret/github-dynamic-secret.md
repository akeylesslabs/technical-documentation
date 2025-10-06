---
title: GitHub Dynamic Secrets
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
You can define a GitHub Dynamic Secret to generate just-in-time installation access tokens for your GitHub repository. Tokens are generated based on the GitHub App information.

# Prerequisites

* An [Akeyless Gateway](doc:api-gw)

* A GitHub application with permissions you would like to grant to the temporary tokens. Then, you need to install this app and select the repositories you want to allow access to.

For more information on how to use installation access tokens in GitHub, see the [GitHub documentation](https://docs.github.com/en/developers/apps/building-github-apps/creating-a-github-app).

# Create a Dynamic GitHub Secret from the CLI

> 👍 Note
>
> We recommend using dynamic secrets with [Targets](doc:targets). While it saves time for multiple secret-level configurations by not requiring you to provide an [inline connection string](https://docs.akeyless.io/docs/rdp-dynamic-secrets#github-connection-strings) each time, it is also important for security streamlining. Using a target allows you to rotate credentials without breaking the credential chain for the objects connected to the server used, using inline will force you to go and change the credentials in each individual item instead of just the target.

To create a dynamic GitHub secret from the CLI using an existing GitHub target, run the following command:

```shell Akeyless CLI
akeyless dynamic-secret create github \
--name <Dynamic Secret Name> \
--target-name <Target Name> \
--gateway-url 'https://<Your-Akeyless-GW-URL:8000>' \
--installation-id <Your GitHub Installation ID>
```

Or using an inline connection string:

```shell Akeyless CLI
akeyless dynamic-secret create github \
--name <Dynamic Secret Name> \
--gateway-url 'https://<Your-Akeyless-GW-URL:8000>' \
--installation-id <Your GitHub Installation ID> \
--github-app-id <Your GitHub application ID> \
--github-app-private-key <Base64-encoded application private key> \
--github-base-url <Github base URL>
```

Where:

* `name`: A unique name of the dynamic secret. The name can include the path to the virtual folder where you want to create the new dynamic secret, using slash `/` separators. If the folder does not exist, it will be created together with the dynamic secret.

* `target-name`: A name of the target that enables connection to the GitHub repository. The name can include the path to the virtual folder where this target resides.

* `gateway-url`: Akeyless Gateway Configuration Manager URL (port `8000`).

* `installation-id`: The GitHub installation ID.

* `installation-organization`: Optional, mutually exclusive with installation ID, GitHub organization name.

* `installation-repository`: Optional, mutually exclusive with installation ID, GitHub repository `<owner>/<repo-name>`

### Inline connection string

If you don't have [GitHub Target](doc:github-target) yet, you can use the command with your GitHub connection string:

* `github-app-id`: Your GitHub application ID.

* `github-app-private-key`: After you create a GitHub application, you need to [generate private keys](https://docs.github.com/en/developers/apps/building-github-apps/authenticating-with-github-apps). You'll use the private key to sign access token requests.

* `github-base-url`: Base URL of the GitHub repository.

You can find the complete list of parameters for this command in the [CLI Reference - Dynamic Secrets](https://docs.akeyless.io/docs/cli-reference-dynamic-secrets#p-stylecolorbluegithubp) section.

# Fetch a Dynamic GitHub Secret value from the CLI

To fetch a dynamic GitHub secret value from the CLI, run the following command:

```shell Akeyless CLI
akeyless dynamic-secret get-value --name <Path to your dynamic secret>
```

# Create a Dynamic Secret for GitHub in the Akeyless Console

> 👍 Note
>
> To start working with dynamic secrets from the [Akeyless Console](https://docs.akeyless.io/docs/github-dynamic-secrets#create-a-dynamic-github-secret-in-the-akeyless-console), you need to configure the Gateway URL thus enabling communication between the Akeyless SaaS and the Akeyless Gateway.

1. Log in to the Akeyless Console, and go to **Items > New > Dynamic Secret**.

2. Select the GitHub secret type and click **Next**.

3. Define a **Name** of the dynamic secret, and specify the **Location** as a path to the virtual folder where you want to create the new dynamic secret, using slash `/` separators. If the folder does not exist, it will be created together with the dynamic secret.

4. Define the remaining parameters as follows:

* **Delete Protection**: When enabled, protects the secret from accidental deletion.
* **Target mode:** In this section, you can either select an existing GitHub Target or specify details of the target GitHub repository explicitly (e.g., if you are not authorized to create and access Targets in the Akeyless Console).

  * Use the **Choose an existing target** drop-down list to select the existing GitHub Target.

  * Select the **Explicitly specify target properties** option, to provide details of the target GitHub repository in the next step.
* **Installation ID\ Repository path\ Organization Name:** Specify a GitHub application installation ID or repository path or Organization name.
* **Installation Token Repositories:** Specify repositories that will accept generated tokens. By default, repositories of the GitHub installation will be used.
* **Installation Token Permissions:** Specify permissions for generated tokens. By default, permissions for the GitHub installation will be used. Input format: `key=value` pairs or a `JSON`  e.g., `{"content":"read"}`.
* **User TTL:** Provide a time-to-live value for a dynamic secret (i.e., a token). When TTL expires, the token becomes obsolete.
* **Time Unit:** Select the time unit (seconds, minutes, hours) for the TTL value.
* **Gateway:** Select the Gateway through which the dynamic secret will create users.
* **Protection key**: To enable zero-Knowledge, select a key with a Customer Fragment. For more information, [read here](doc:implement-zero-knowledge).

5. If you checked the **Explicitly specify target properties** radio button, click **Next**.

6. Provide details of the target GitHub repository:

* **App ID:** Specify the ID of the GitHub application.

* **App Private Key:** Upload a base64-encoded private key of the GitHub application. It will be used to sign access token requests.

* **Base URL:** Specify the base URL of the GitHub repository. The default value is [https://api.github.com/](https://api.github.com/).

7. Click **Finish**.

# Fetch a Dynamic GitHub Secret value from the Akeyless Console

1. Log in to the Akeyless Console, and go to **Items**.

2. Browse to the folder where you created a dynamic secret.

3. Select the secret and click **Get Dynamic Secret** button.