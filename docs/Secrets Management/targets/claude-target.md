---
title: Claude Target
deprecated: false
hidden: false
metadata:
  robots: index
---
You can define a [Claude](https://www.anthropic.com/api) target to be used for [AI Insights](https://docs.akeyless.io/docs/akeyless-ai-insight) in your account.

## Create a Claude Target with the CLI

To create a Claude target with the CLI, run the following command:

```shell
akeyless target create claude \
  --name <target name> \
  --api-key <Claude API key> \
  --claude-url <Claude API base URL> \
  --key <protection key>
```

Where:

- `name`: A unique name of the target. The name can include the path to the virtual folder where you want to create the new target, using slash `/` separators. If the folder does not exist, it will be created together with the target.
- `api-key`: The Claude API key.
- `claude-url`: The Claude API base URL. Default: `https://api.anthropic.com`
- `key`: The protection key used to encrypt the target secret value. If not specified, the account default protection key is used.

You can find the complete list of parameters for this command in the [CLI Reference - Akeyless Targets]() section.

## Create a Claude Target in the Console

1. Log in to the Akeyless Console, and go to **Targets** > **New** > **AI (Claude)**.&#x20;
2. Define a **Name** of the target, and specify the **Location** as a path to the virtual folder where you want to create the new target, using slash `/` separators. If the folder does not exist, it will be created together with the target.
3. Select a **Protection key** with a Customer Fragment to enable Zero-Knowledge and click **Next**.
   For more information, [read here](https://docs.akeyless.io/docs/gateway-zero-knowledge).
4. Define the remaining parameters as follows:
   - **API Key**: The Claude API key.
   - **Claude URL**: The Claude API base URL. Default: `https://api.anthropic.com`

<br />
