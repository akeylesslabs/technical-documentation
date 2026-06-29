---
title: Keycloak Target
deprecated: false
hidden: false
metadata:
  robots: index
---
You can define a [Keycloak](https://www.keycloak.org/) target for managing identities in your Keycloak account.

## Create a Keycloak Target with the CLI

To create a Keycloak target with the CLI, run the following command:

```shell
akeyless target create keycloak \
  --name <target name> \
  --url <Keycloak URL> \
  --realm <Keycloak realm> \
  --client-id <Keycloak client ID> \
  --client-secret <Keycloak client secret> \
  --key <protection key>
```

Where:
- `name`: A unique name of the target. The name can include the path to the virtual folder where you want to create the new target, using slash `/` separators. If the folder does not exist, it will be created together with the target.
- `url`: The base URL of your Keycloak server.
- `realm`: The Keycloak realm to connect to.
- `client-id`: The ID of the Keycloak client configured for service account authentication.
- `client-secret`: The secret associated with the Keycloak client's service account.
- `key`: The protection key used to encrypt the target secret value. If not specified, the account default protection key is used.

You can find the complete list of parameters for this command in the CLI Reference - Akeyless Targets section.

## Create a Keycloak Target in the Console

1. Log in to the Akeyless Console, and go to **Targets** > **New** > **Infra (Keycloak)**.
2. Define a **Name** of the target, and specify the **Location** as a path to the virtual folder where you want to create the new target, using slash `/` separators. If the folder does not exist, it will be created together with the target.
3. Select a **Protection key** with a Customer Fragment to enable Zero-Knowledge and click **Next**.
   For more information, [read here](https://docs.akeyless.io/docs/gateway-zero-knowledge).
4. Define the remaining parameters as follows:
   - **Keycloak URL**: The base URL of your Keycloak server.
   - **Realm**: The Keycloak realm to connect to.
   - **Client ID**: The ID of the Keycloak client configured for service account authentication.
   - **Client Secret**: The secret associated with the Keycloak client's service account.