---
title: GitHub Target
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
You can define a GitHub target to be used with [GitHub Dynamic Secret](doc:github-dynamic-secret).

# Create a GitHub Target in the CLI

To create a GitHub target from the CLI, run the following command:

```shell GitHub Target
akeyless target create github \
--name <target name> \
--github-app-id <Github application ID> \
--github-app-private-key <Github application private key (base64-encoded key)> \
--github-base-url https://api.github.com
```

Where:

* `name`: A unique name of the target. The name can include the path to the virtual folder where you want to create the new target, using slash `/` separators. If the folder does not exist, it will be created together with the target.

* `github-app-id`: Provide the GitHub application ID.

* `github-app-private-key`: The [GitHub application private key](https://docs.github.com/en/developers/apps/building-github-apps/authenticating-with-github-apps).

* `github-base-url`: Provide the GitHub base URL, default is [https://api.github.com/](https://api.github.com/).

You can find the complete list of parameters for this command in the [CLI Reference - Akeyless Targets](https://docs.akeyless.io/docs/cli-ref-targets#p-stylecolorbluegithubp) section.

# Create a GitHub Target in the Console

1. Log in to the Akeyless Console, and go to **Targets > New > Infra > GitHub**.

2. Define a **Name** of the target, and specify the **Location** as a path to the virtual folder where you want to create the new target, using slash `/` separators. If the folder does not exist, it will be created together with the target.

3. Select a **Protection key** with a Customer Fragment to enable Zero-Knowledge and click **Next**.\
   For more information, [read here](doc:implement-zero-knowledge).

4. Define the remaining parameters as follows:

* **App ID:** Provide the GitHub application ID.

* **App Private Key:** The [GitHub application private key](https://docs.github.com/en/developers/apps/building-github-apps/authenticating-with-github-apps).

* **Base URL:** Provide the Github base URL, default is `https://api.github.com`

5. Click **Finish**.
