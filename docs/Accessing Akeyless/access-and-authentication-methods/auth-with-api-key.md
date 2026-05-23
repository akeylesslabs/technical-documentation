---
title: API Key 
excerpt: ''
deprecated: false
hidden: false
metadata:
  title: API Key
  description: ''
  robots: index
next:
  description: >-
    Make sure to associate your new Authentication Method with an Access Role to
    grant the relevant permissions within Akeyless.
---
This page discusses creating and using an API key-based authentication method in Akeyless.

API key authentication allows users and workloads to authenticate to Akeyless using an **Access ID** and **Access Key** pair. It is typically used for CLI, SDK, and automation workflows.

API key authentication is intended for **programmatic access** and is not recommended for direct interactive Console sign-in.

![Flow diagram for API key authentication in Akeyless, showing Access ID and Access Key based authentication.](https://files.readme.io/574347a-API_key_auth.png)

<ApiKeyWarning />

## Creating an API Key Authentication Method

API key authentication is available by default for Akeyless accounts. No additional configuration is required.

This action is distinct from creating a new Akeyless account: it creates an additional API key-based authentication method for an existing account.

### Creating an API Key Authentication Method with the Console

To create a new API key-based authentication method with the Console:

1. In the Console, under **Administration**, navigate to **Users & Auth Methods**.
2. Select **+ New**. This opens the **Create Authentication Method** form.
3. On the **Type** selection screen, select **API Key**, then **Next →**.
4. Enter a name for the Authentication Method in the **Name** field. Optionally, include a path using `/` separators to place the Authentication Method in a virtual folder, then select **Finish**.
5. Download the generated CSV file that includes the **Access ID** and **Access Key**. Save it in a secure location. This is the last time this access key will be available to view or download.

The **Access Key** is displayed only once. Store it securely. However, you can reset the access key at any time.

### Creating an API Key Authentication Method with the CLI

To create an API key-based authentication method with the CLI:

```shell
akeyless auth-method create api-key \
  --name <API Key Auth Method Name>
```

The command returns credentials for the new authentication method. The **Access Key** is displayed only once. Store it securely. Be sure to associate the API key authentication method with one or more Roles.

[Read about more parameters available when creating an API key-based authentication method.](https://docs.akeyless.io/docs/cli-ref-auth#create)

## Using an API Key Authentication Method

### Using an API Key Authentication Method with the Console

To use an API key-based authentication method with the Console:

1. Open the Akeyless Console: [https://console.akeyless.io](https://console.akeyless.io).
2. In the **Or continue with** section, select **Access Key**.
3. Enter the **Access ID** and **Access Key**, then select **Sign in**.

### Using an API Key Authentication Method with the CLI

To use an API key-based authentication method with a CLI profile, run the [Akeyless configure command](https://docs.akeyless.io/docs/cli-reference#configure). For more information about profiles, see [CLI Profiles](https://docs.akeyless.io/docs/cli-profiles):

```shell
akeyless configure \
  --profile default \
  --access-id <Access ID> \
  --access-key <Access Key>
```

To authenticate with an Access ID and Access Key using the CLI, run the [Akeyless auth command](https://docs.akeyless.io/docs/cli-ref-auth#auth):

<!-- secret-stdout-scan:ok -->
```shell
akeyless auth \
  --access-type access_key \
  --access-id <Access ID> \
  --access-key <Access Key>
```

## Optional Features

For optional features that apply across Authentication Methods, see [Common Optional Features](https://docs.akeyless.io/docs/access-and-authentication-methods#common-optional-features).

### Reset Access Key

To reset the Access Key for an existing API key-based authentication method with the Console:

1. In the Console, under **Administration**, navigate to **Users & Auth Methods**.
2. Select the API key authentication method name. The details sidebar opens.
3. In the default **General** tab, select **Reset Access Key**.
4. In the confirmation window, enter the authentication method name, then select **Reset Access Key**.

To reset the Access Key with the CLI, run the [Akeyless reset-access-key command](https://docs.akeyless.io/docs/cli-ref-auth#reset-access-key):

```shell
akeyless reset-access-key \
  --name <API Key Auth Method Name>
```
