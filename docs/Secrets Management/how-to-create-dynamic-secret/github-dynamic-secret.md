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

## Prerequisites

- An [Akeyless Gateway](https://docs.akeyless.io/docs/gateway-overview)

- A [GitHub Target](https://docs.akeyless.io/docs/github-target)

- A GitHub application with permissions you would like to grant to the temporary tokens. Then, you need to install this app and select the repositories you want to allow access to.

For more information on how to use installation access tokens in GitHub, see the [GitHub documentation](https://docs.github.com/en/developers/apps/building-github-apps/creating-a-github-app).

## Create a Dynamic GitHub Secret with the CLI

To create a dynamic GitHub secret with the CLI using an existing GitHub target, run the following command:

```shell
akeyless dynamic-secret create github \
--name <Dynamic Secret Name> \
--target-name <Target Name> \
--gateway-url 'https://<Your-Akeyless-GW-URL>:8000' \
--installation-id <Your GitHub Installation ID>
```

Where:

- `name`: A unique name of the dynamic secret. The name can include the path to the virtual folder where you want to create the new dynamic secret, using slash `/` separators. If the folder does not exist, it will be created together with the dynamic secret.

- `target-name`: A name of the target that enables connection to the GitHub repository. The name can include the path to the virtual folder where this target resides.

- `gateway-url`: Akeyless Gateway URL (port `8000`).

- `installation-id`: The GitHub installation ID.

- `installation-organization`: Optional, mutually exclusive with installation ID, GitHub organization name.

- `installation-repository`: Optional, mutually exclusive with installation ID, GitHub repository `<owner>/<repo-name>`

You can find the complete list of parameters for this command in the [CLI Reference - Dynamic Secrets](https://docs.akeyless.io/docs/cli-reference-dynamic-secrets#github) section.

## Fetch a Dynamic GitHub Secret Value with the CLI

To fetch a dynamic GitHub secret value with the CLI, run the following command:

```shell
akeyless dynamic-secret get-value --name <Path to your dynamic secret>
```

## Create a Dynamic Secret for GitHub in the Akeyless Console

1. Log in to the Akeyless Console, and go to **Items > New > Dynamic Secret**.

2. Select the GitHub secret type and click **Next**.

3. Define a **Name** of the dynamic secret, and specify the **Location** as a path to the virtual folder where you want to create the new dynamic secret, using slash `/` separators. If the folder does not exist, it will be created together with the dynamic secret.

4. Define the remaining parameters as follows:

   - **Delete Protection**: When enabled, protects the secret from accidental deletion.
   - **Target:** Select an existing [GitHub Target](https://docs.akeyless.io/docs/github-target).&#x20;
   - **Installation ID\ Repository path\ Organization Name:** Specify a GitHub application installation ID or repository path or Organization name.
   - **Installation Token Repositories:** Specify repositories that will accept generated tokens. By default, repositories of the GitHub installation will be used.
   - **Installation Token Permissions:** Specify permissions for generated tokens. By default, permissions for the GitHub installation will be used. Input format: `key=value` pairs or a `JSON`, for example, `{"content":"read"}`.
   - **User TTL:** Provide a time-to-live value for a dynamic secret (that is, a token). When TTL expires, the token becomes obsolete.
   - **Time Unit:** Select the time unit (seconds, minutes, hours) for the TTL value.
   - **Gateway:** Select the Gateway through which the dynamic secret will create users.
   - **Protection key**: To enable zero-Knowledge, select a key with a Customer Fragment. For more information, [read here](https://docs.akeyless.io/docs/gateway-zero-knowledge).

5. Click **Finish**.

## Fetch a Dynamic GitHub Secret Value from the Akeyless Console

1. Log in to the Akeyless Console, and go to **Items**.

2. Browse to the folder where you created a dynamic secret.

3. Select the secret and click the **Get Dynamic Secret** button.

<br />
