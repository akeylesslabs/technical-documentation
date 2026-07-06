---
title: Okta Target
deprecated: false
hidden: false
metadata:
  robots: index
---
You can define an [Okta](https://www.okta.com/) target for managing identities in your Okta account.

## Create an Okta Target with the CLI

To create an Okta target with the CLI, run the following command:

```shell
akeyless target create okta \
  --name <target name> \
  --api-token <Okta API token> \
  --url <Okta URL> \
  --key <protection key>
```

Where:
- `name`: A unique name of the target. The name can include the path to the virtual folder where you want to create the new target, using slash `/` separators. If the folder does not exist, it will be created together with the target.
- `api-token`: The Okta API token.
- `url`: The URL of your Okta account.
- `key`: The protection key used to encrypt the target secret value. If not specified, the account default protection key is used.

You can find the complete list of parameters for this command in the CLI Reference - Akeyless Targets section.

## Create an Okta Target in the Console

1. Log in to the Akeyless Console, and go to **Targets** > **New** > **Infra (Okta)**.
2. Define a **Name** of the target, and specify the **Location** as a path to the virtual folder where you want to create the new target, using slash `/` separators. If the folder does not exist, it will be created together with the target.
3. Select a **Protection key** with a Customer Fragment to enable Zero-Knowledge and click **Next**.
   For more information, [read here](https://docs.akeyless.io/docs/gateway-zero-knowledge).
4. Define the remaining parameters as follows:
   - **API Token**: The Okta API token.
   - **Okta URL**: The URL of your Okta account.