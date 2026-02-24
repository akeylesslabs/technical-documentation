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
This page discusses creating and using an email-based Authentication Method in Akeyless.

Email Authentication allows human users to authenticate directly to the Akeyless Console using their email address and password. It is typically used for standalone accounts, administrators, or environments where SAML or OIDC federation is not required.

Email authentication is intended for **interactive human access** and is not recommended for machine or workload authentication.

## Creating an Email Authentication Method

Email authentication is available by default for Akeyless accounts. No additional configuration is required. This action is distinct from creating a new Akeyless account: it creates an additional email-based Authentication Method for an existing account.

### Creating an Email Authentication Method with the Console

To create a new email-based Authentication Method with the Console:

1. In the Console, under **Administration**, navigate to **Users & Auth Methods**.
2. Select **+ New**. This opens the **Create Authentication Method** form.
3. On the **Type** selection screen, select **Email**, then **Next →**.
4. Enter a name for the Authentication Method, such as `My Email User 1` in the **Name** field, then select **Next →**.
5. Supply the designated email address in the **Email** field. Optionally, configure [Two-Factor Authentication](#optional-features).
6. Select **Finish**.

An email prompting to set a password and activate the Authentication Method will be sent to the specified email address. Be sure to associate the email Authentication Method with one or more Roles.

### Creating an Email Authentication Method with the CLI

To create an email-based Authentication Method with the CLI:

```shell
akeyless auth-method create email \
  --name <Email Auth Method Name> \
  --email email-address@sample.com
```

An email prompting to set a password and activate the Authentication Method will be sent to the specified email address. Be sure to associate the email Authentication Method with one or more Roles.

[Read about more parameters available when creating an email-based Authentication Method.](https://docs.akeyless.io/docs/cli-ref-auth#email)

## Using an Email Authentication Method

### Using an Email Authentication Method with the Console

To use an email-based Authentication Method with the Console:

1. Open the Akeyless Console: [https://console.akeyless.io](https://console.akeyless.io).
2. Enter the email address used, then select **Sign in**.
3. Enter the password used, then select **Sign in** again.

### Using an Email Authentication Method with the CLI

To authenticate with an email address and password with the CLI, run the following command:

```shell
akeyless auth \
  --admin-email email-address@sample.com \
  --admin-password <Password>
```

## Optional Features

* **Two-Factor Authentication:** When creating an email-based Authentication Method, **Two-Factor Authentication** can be optionally enabled. The second factor can use either **Email** or **Google Authenticator**. Only Google Authenticator is supported as an Authenticator App. The Two-Factor Authentication configuration can be enabled, edited, or disabled on an existing email-based Authentication Method.

* **Expiration Date:** Select an access expiration date. This parameter is optional. Leave it empty for access to continue without an expiration date.

* **Allowed Client IPs:** Enter a comma-separated list of CIDR blocks from which the client can issue calls to the proxy. By "client," we mean cURL, SDKs, and so on. This parameter is optional. Leave it empty for unrestricted access.

* **Allowed Trusted Gateway IPs:** Comma-separated CIDR blocks. If specified, the Gateway using this IP range will be trusted to forward the original client IP. If empty, the Gateway's IP address will be used.

* **Audit Log Sub-Claims:** Include the following sub-claims values in Audit Logs.

* **Allowed Client Type:** Select the allowed client type that will be authorized to use this authentication method. For example, `CLI`, `Web UI`, `SDK`, `Gateway Admin`, `Mobile`, `Extension`.

* **JWT TTL (in minutes):** The time span from acceptance of the invitation to the JWT expiration.
