---
title: SAML
excerpt: Security Assertion Markup Language (SAML)
deprecated: false
hidden: false
metadata:
  title: SAML
  description: ''
  robots: index
next:
  description: >-
    Make sure to associate your new Authentication Method with an Access Role to
    grant the relevant permissions within Akeyless
slug: auth-with-saml
---
SAML authentication lets users sign in to Akeyless through an external Identity Provider (IdP), such as [Okta](https://docs.akeyless.io/docs/saml-auth-okta), [Ping Identity](https://docs.akeyless.io/docs/saml-auth-ping-identity), or [Microsoft Entra ID](https://docs.akeyless.io/docs/saml-auth-azure-ad).

This page explains how to create and use a SAML Authentication Method in Akeyless for browser-based sign-in and single sign-on (SSO) flows.

## Creating a SAML Authentication Method

This action is distinct from creating a new Akeyless account: it creates an additional SAML-based authentication method for an existing account.

Important SAML requirement:

- **Dedicated endpoints per Authentication Method:** Each SAML authentication method has dedicated SAML endpoints. When configuring the IdP application, use the metadata and assertion consumer service (ACS) endpoint values generated for that specific SAML authentication method.

## Dedicated SAML Endpoints per Authentication Method

Akeyless supports dedicated SAML endpoints for each SAML Authentication Method. This allows multiple SAML authentication methods to be configured in the same Akeyless account using the same IdP, for example to separate production, development, staging, or other environments.

Each SAML Authentication Method has its own unique Entity ID, Assertion Consumer Service (ACS) URL, and metadata URL, based on the Authentication Method Access ID.

This is useful when working with Identity Providers that require each SAML application to use a unique Entity ID or metadata URL. For example, Microsoft Entra ID may require each Enterprise Application to use unique SAML configuration values. Dedicated endpoints allow each Entra Enterprise Application to be mapped to a specific SAML Authentication Method.

Dedicated endpoints also help ensure that each IdP application is explicitly tied to the intended Akeyless SAML Authentication Method.

### Endpoint Format

Replace `<SAML_AUTH_METHOD_ACCESS_ID>` with the Access ID of the matching  SAML Authentication Method.

| Endpoint                 | Format                                                                |
| ------------------------ | --------------------------------------------------------------------- |
| Entity ID / Identifier   | `https://auth.akeyless.io/saml/sp/<SAML_AUTH_METHOD_ACCESS_ID>`       |
| Reply URL / ACS URL      | `https://auth.akeyless.io/saml/acs/<SAML_AUTH_METHOD_ACCESS_ID>`      |
| Akeyless SP Metadata URL | `https://auth.akeyless.io/saml/metadata/<SAML_AUTH_METHOD_ACCESS_ID>` |

### Creating a SAML Authentication Method with the Console

To create a new SAML-based authentication method with the Console:

1. In the Console, under **Administration**, navigate to **Users & Auth Methods**.
2. Select **New**. This opens the authentication method creation wizard.
3. In **Select Type**, select **SAML**, then select **Next →**.
4. Enter a name for the Authentication Method in the **Name** field. Optionally, include a path using `/` separators to place the Authentication Method in a virtual folder, then select **Next →**.
5. Configure general and SAML-specific fields, including **Allowed Redirect URIs**, **Metadata URL** or **Metadata XML**, and **Unique Identifier**.
6. Select **Finish**.

<Callout icon="⚠️" theme="warn">
  ### **Warning:**

  The **Unique Identifier** must be a sub-claim key name, not a user value. For example, use `email`, not an actual email address.
</Callout>

### Creating a SAML Authentication Method with the CLI

To create a SAML-based authentication method with the CLI:

```shell
akeyless auth-method create saml \
  --name <SAML Auth Method Name> \
  --idp-metadata-url <IdP Metadata URL> \
  --unique-identifier <email|username|UPN>
```

To create the method by using XML metadata, use:

```shell
akeyless auth-method create saml \
  --name <SAML Auth Method Name> \
  --idp-metadata-xml-file-path <Path to IdP Metadata XML File> \
  --unique-identifier <email|username|UPN>
```

By default, Akeyless treats comma `,` as a delimiter for sub-claim values. If your IdP uses different delimiters, configure them with the `delimiters` flag.

[Read about more parameters available when creating a SAML-based authentication method.](https://docs.akeyless.io/docs/cli-ref-auth#create)

## Using a SAML Authentication Method

### Using a SAML Authentication Method with the Console

To sign in to the Console with SAML:

1. Open the Akeyless Console: [https://console.akeyless.io](https://console.akeyless.io).
2. In the **Or continue with** section, select **SAML**.
3. Enter the SAML Authentication Method **Access ID**, then continue with the IdP sign-in flow.

### Using a SAML Authentication Method with the CLI

To use a SAML-based authentication method with a CLI profile, run the [Akeyless configure command](https://docs.akeyless.io/docs/cli-reference#configure):

```shell
akeyless configure \
  --profile saml \
  --access-id <SAML Access ID> \
  --access-type saml
```

To authenticate and retrieve a temporary Akeyless token, run the [Akeyless auth command](https://docs.akeyless.io/docs/cli-ref-auth#auth):

{/* secret-stdout-scan:ok */}

```shell
akeyless auth \
  --access-type saml \
  --access-id <SAML Access ID>
```

## Associate with Access Roles

After creating the authentication method, associate it with one or more Access Roles so authenticated users can perform actions in Akeyless.

To associate with Access Roles in the Console:

1. In the Console, under **Administration**, navigate to **Users & Auth Methods**.
2. Select the SAML Authentication Method.
3. Open the associated roles section, then add the required Access Roles.
4. Save the changes.

For role configuration details, see [Access Roles](https://docs.akeyless.io/docs/rbac).

## Update an Existing SAML Authentication Method

SAML authentication methods can require updates over time, for example when IdP metadata changes after certificate rotation.

To update in the Console:

1. In the Console, under **Administration**, navigate to **Users & Auth Methods**.
2. Select the SAML Authentication Method to update.
3. Update the relevant fields, such as **Metadata URL**, **Metadata XML**, **Allowed Redirect URIs**, and **Unique Identifier**.
4. Save the changes.

To update with the CLI:

```shell
akeyless auth-method update saml \
  --name <Existing SAML Auth Method Name> \
  --idp-metadata-url <Updated IdP Metadata URL> \
  --unique-identifier <email|username|UPN>
```

For all available update flags, see [CLI Reference - Authentication](https://docs.akeyless.io/docs/cli-ref-auth#saml-1).

## Troubleshooting

If SAML sign-in fails, check the following:

- The SAML Authentication Method **Access ID** is correct.
- The IdP configuration uses the dedicated ACS and Entity ID values from the same SAML Authentication Method.
- **Metadata URL** or **Metadata XML** is current.
- **Unique Identifier** matches a key that exists in IdP assertions.
- **Allowed Redirect URIs** includes the redirect URI used by the client.

## Optional Features

For optional features that apply across Authentication Methods, see [Common Optional Features](https://docs.akeyless.io/docs/access-and-authentication-methods#common-optional-features).

### SAML-Specific Optional Features

- **Allowed Redirect URIs:** Restrict the redirect targets that can be used in the authentication flow.
- **Unique Identifier:** Define which IdP sub-claim key identifies a user.
- **Sub-claim Delimiters:** Configure custom delimiters if your IdP uses a format other than comma-separated values.

## Related Pages

For end-to-end IdP setup examples, see:

- [Set Up Okta as a SAML Authentication Method](https://docs.akeyless.io/docs/saml-auth-okta)
- [Set Up Ping Identity as a SAML Authentication Method](https://docs.akeyless.io/docs/saml-auth-ping-identity)
- [Set Up Microsoft Entra ID as a SAML Authentication Method](https://docs.akeyless.io/docs/saml-auth-azure-ad)

<br />
