---
title: Bedrock Target
deprecated: false
hidden: true
metadata:
  robots: index
---
You can define a [Bedrock](https://www.anthropic.com/api) target to be used for [AI Insights](https://docs.akeyless.io/docs/akeyless-ai-insight) in your account.

## Create a Bedrock Target with the CLI

To create a Bedrock target with the CLI, run the following command:

```shell
akeyless target create bedrock \
  --name <target name> \
  --api-key <Bedrock API key> \
  --bedrock-url <Bedrock API base URL> \
  --key <protection key>
```

Where:

- `name`: A unique name of the target. The name can include the path to the virtual folder where you want to create the new target, using slash `/` separators. If the folder does not exist, it will be created together with the target.
- `api-key`: The Bedrock API key.
- `bedrock-url`: The Bedrock API base URL. Default: `https://bedrock-runtime.us-east-1.amazonaws.com`
- `key`: The protection key used to encrypt the target secret value. If not specified, the account default protection key is used.

## Create a Bedrock Target in the Console

1. Log in to the Akeyless Console, and go to **Targets** > **New** > **AI (Bedrock)**.&#x20;
2. Define a **Name** of the target, and specify the **Location** as a path to the virtual folder where you want to create the new target, using slash `/` separators. If the folder does not exist, it will be created together with the target.
3. Select a **Protection key** with a Customer Fragment to enable Zero-Knowledge and click **Next**.
   For more information, [read here](https://docs.akeyless.io/docs/gateway-zero-knowledge).
4. Define the remaining parameters as follows:
   - **API Key**: The Bedrock API key.
   - **Bedrock URL**: The Bedrock API base URL. Default: `https://bedrock-runtime.us-east-1.amazonaws.com`

<br />
