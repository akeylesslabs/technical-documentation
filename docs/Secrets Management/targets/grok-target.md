---
title: Grok Target
deprecated: false
hidden: false
metadata:
  robots: index
---
You can define a [Grok](https://grok.com/) target to be used for [AI Insights](https://docs.akeyless.io/docs/akeyless-ai-insight) in your account.

## Create a Grok Target with the CLI

To create a Grok target with the CLI, run the following command:

```shell
akeyless target create grok \
  --name <target name> \
  --api-key <Grok API key> \
  --grok-url <Grok API base URL> \
  --team-id <team ID> \
  --key <protection key>
```

Where:
- `name`: A unique name of the target. The name can include the path to the virtual folder where you want to create the new target, using slash `/` separators. If the folder does not exist, it will be created together with the target.
- `api-key`: The Grok API key.
- `grok-url`: The Grok API base URL. Default: `https://api.x.ai`
- `team-id`: The ID of the team this API key belongs to.
- `key`: The protection key used to encrypt the target secret value. If not specified, the account default protection key is used.

You can find the complete list of parameters for this command in the CLI Reference - Akeyless Targets section.

## Create a Grok Target in the Console

1. Log in to the Akeyless Console, and go to **Targets** > **New** > **AI (Grok)**.
2. Define a **Name** of the target, and specify the **Location** as a path to the virtual folder where you want to create the new target, using slash `/` separators. If the folder does not exist, it will be created together with the target.
3. Select a **Protection key** with a Customer Fragment to enable Zero-Knowledge and click **Next**.
   For more information, [read here](https://docs.akeyless.io/docs/gateway-zero-knowledge).
4. Define the remaining parameters as follows:
   - **API Key**: The Grok API key.
   - **Grok URL**: The Grok API base URL. Default: `https://api.x.ai`
   - **Team ID**: The ID of the team this API key belongs to.