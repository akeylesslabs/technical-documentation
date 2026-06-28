---
title: Keycloak Target
deprecated: false
hidden: false
metadata:
  robots: index
---
You can define a [Keycloak](https://www.okta.com/) target for managing identities in your Keycloak account.

# Create a Keycloak Target with the CLI

To create a Keycloak target with the CLI, run the following command:

```shell
akeyless target create okta \
--name <target name> \
--realm <Keycloak realm>
--client-id <Keycloak client ID>
--client-secret <Keycloak client secret>
```

Where:

`name`: A unique name of the target. This identifier helps you distinguish this target from others. The name can include the path to the virtual folder where you want to create the new target, using slash `/` separators. If the folder does not exist, it will be created together with the target.

`realm`: The Keycloak realm to connect to

`client-id`: The ID of the Keycloak client configured for service account authentication

`client-secret`: The secret associated with the Keycloak client’s service account.

`url`: The base URL of your Keycloak server

`key`: The protection key used to encrypt the target secret value. This key provides an additional layer of security for your sensitive data. If not specified, the account default protection key is used.

# Create a Keycloak Target in the Console

1. Log in to the Akeyless Console, and go to **Targets** > **Infra** > **Keycloak**.
2. Define a **Name** of the target, and specify the **Location** as a path to the virtual folder where you want to create the new target, using slash `/` separators. If the folder does not exist, it will be created together with the target.
3. Select a **Protection key** with a Customer Fragment to enable Zero-Knowledge and click **Next**.
   For more information, [read here](https://docs.akeyless.io/docs/gateway-zero-knowledge).
4. Define the remaining parameters as follows:
   - **Keycloak URL**: The base URL of your Keycloak server.
   - **Realm:&#x20;**&#x54;he Keycloak realm to connect to.
   - **Client-ID**: The ID of the Keycloak client configured for service account authentication.
   - **Client-Secret:&#x20;**&#x54;he secret associated with the Keycloak client’s service account.

<br />
