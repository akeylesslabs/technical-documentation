---
title: Email
excerpt: ''
deprecated: false
hidden: false
metadata:
  title: Email
  description: ''
  robots: index
next:
  description: >-
    Make sure to associate your new Authentication Method with an Access Role to
    grant the relevant permissions within Akeyless.
---
This page discusses creating and using an email-based authentication method in Akeyless.

Email authentication allows human users to authenticate directly to the Akeyless Console using their email address and password. It is typically used for standalone accounts, administrators, or environments where SAML or OIDC federation is not required.

Email authentication is intended for **interactive human access** and is not recommended for machine or workload authentication.

Zero-Knowledge support: Supported with the Akeyless [Zero-Knowledge Encryption architecture](https://docs.akeyless.io/docs/zero-knowledge-architecture).

Gateway service-to-service scope: This method is not listed in [Gateway Zero-Knowledge machine-identity mapping](https://docs.akeyless.io/docs/gateway-zero-knowledge#machine-identity-authentication-mapping).

## Creating an Email Authentication Method

Email authentication is available by default for Akeyless accounts. No additional configuration is required. This action is distinct from creating a new Akeyless account: it creates an additional email-based authentication method for an existing account.

### Creating an Email Authentication Method with the Console

To create a new email-based authentication method with the Console:

1. In the Console, under **Administration**, navigate to **Users & Auth Methods**.
2. Select **+ New**. This opens the **Create Authentication Method** form.
3. On the **Type** selection screen, select **Email**, then **Next →**.
4. Enter a name for the Authentication Method in the **Name** field. Optionally, include a path using `/` separators to place the Authentication Method in a virtual folder, then select **Next →**.
5. Supply the designated email address in the **Email** field. Optionally, configure [Two-Factor Authentication](#optional-features).
6. Select **Finish**.

An email prompting to set a password and activate the authentication method will be sent to the specified email address. Be sure to associate the email authentication method with one or more Roles.

### Creating an Email Authentication Method with the CLI

To create an email-based authentication method with the CLI:

```shell
akeyless auth-method create email \
  --name <Email Auth Method Name> \
  --email email-address@sample.com
```

An email prompting to set a password and activate the authentication method will be sent to the specified email address. Be sure to associate the email authentication method with one or more Roles.

[Read about more parameters available when creating an email-based authentication method.](https://docs.akeyless.io/docs/cli-ref-auth#email)

## Using an Email Authentication Method

### Using an Email Authentication Method with the Console

To use an email-based authentication method with the Console:

1. Open the Akeyless Console: [https://console.akeyless.io](https://console.akeyless.io).
2. Email authentication is the default option. Enter the email address used, then select **Sign in**.
3. Enter the password used, then select **Sign in** again.

### Using an Email Authentication Method with the CLI

To authenticate with an email address and password using the CLI, run the [Akeyless auth command](https://docs.akeyless.io/docs/cli-ref-auth#auth):

<!-- secret-stdout-scan:ok -->
```shell
akeyless auth \
  --admin-email email-address@sample.com \
  --admin-password <Password>
```

## Associate with Access Roles

After creating the authentication method, associate it with one or more Access Roles so authenticated users can perform actions in Akeyless.

1. In the Console, under **Administration**, navigate to **Users & Auth Methods**.
2. Select the email authentication method.
3. Add the required Access Roles.
4. Save the changes.

For role configuration details, see [Access Roles](https://docs.akeyless.io/docs/rbac).

## Update an Existing Email Authentication Method

Email authentication methods can require updates over time, for example when changing the configured email address or other method settings.

To update in the Console:

1. In the Console, under **Administration**, navigate to **Users & Auth Methods**.
2. Select the email authentication method to update.
3. Update the required fields.
4. Save the changes.

To update with the CLI, use the relevant `akeyless auth-method update email` flags in [CLI Reference - Authentication](https://docs.akeyless.io/docs/cli-ref-auth#update).

## Troubleshooting

If email authentication fails, check the following:

* The configured email address is correct.
* The password is valid and not expired.
* The authentication method is associated with the required Access Roles.
* If Two-Factor Authentication is enabled, the second-factor method is configured and accessible.

## Optional Features

For optional features that apply across Authentication Methods, see [Common Optional Features](https://docs.akeyless.io/docs/access-and-authentication-methods#common-optional-features).

* **Two-Factor Authentication:** When creating an email-based authentication method, **Two-Factor Authentication** can be optionally enabled. The second factor can use either **Email** or an **Authenticator App**. Only Google Authenticator is supported as an Authenticator App. The Two-Factor Authentication configuration can be enabled, edited, or disabled on an existing email-based authentication method.
* **Forgot Password:** On the Console login screen, select **Forgot Password** below the **Email** field. This opens the **Forgot Your Credentials?** page. Enter the email address, then select **Reset Credentials**.
