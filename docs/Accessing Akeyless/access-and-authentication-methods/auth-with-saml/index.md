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
---
SAML authentication lets users sign in to Akeyless through an external Identity Provider (IdP), such as [Okta](https://docs.akeyless.io/docs/saml-auth-okta), [Ping Identity](https://docs.akeyless.io/docs/saml-auth-ping-identity), or [Microsoft Entra ID](https://docs.akeyless.io/docs/saml-auth-azure-ad).

This page explains how to create and use a SAML Authentication Method in Akeyless for browser-based sign-in and single sign-on (SSO) flows.

## Creating a SAML Authentication Method

This action is distinct from creating a new Akeyless account: it creates an additional SAML-based authentication method for an existing account.

Important SAML requirement:

* **Dedicated endpoints per Authentication Method:** Each SAML authentication method has dedicated SAML endpoints. When configuring the IdP application, use the metadata and assertion consumer service (ACS) endpoint values generated for that specific SAML authentication method.

### Creating a SAML Authentication Method with the Console

To create a new SAML-based authentication method with the Console:

1. In the Console, under **Administration**, navigate to **Users & Auth Methods**.
2. Select **+ New**. This opens the **Create Authentication Method** form.
3. On the **Type** selection screen, select **SAML**, then **Next →**.
4. Enter a name for the Authentication Method in the **Name** field. Optionally, include a path using `/` separators to place the Authentication Method in a virtual folder, then select **Next →**.
5. Configure general and SAML-specific fields:
   * **Allowed Redirect URIs:** Comma-separated redirect URIs to validate in the SAML flow.
   * **Metadata input:** Choose **URL** or **XML**, then provide your IdP metadata.
   * **Unique Identifier:** Sub-claim key used to uniquely identify users (for example, `email`, `username`, or `UPN`).
6. Select **Finish**.

> ⚠️ **Warning:**
>
> The **Unique Identifier** must be a sub-claim key name, not a user value. For example, use `email`, not an actual email address.

### Creating a SAML Authentication Method with the CLI

To create a SAML-based authentication method with the CLI:

```shell
akeyless auth-method create saml \
  --name <SAML Auth Method Name> \
  --idp-metadata-url <IdP Metadata URL> \
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

<!-- secret-stdout-scan:ok -->
```shell
akeyless auth \
  --access-type saml \
  --access-id <SAML Access ID>
```

## Optional Features

For optional features that apply across Authentication Methods, see [Common Optional Features](https://docs.akeyless.io/docs/access-and-authentication-methods#common-optional-features).

### SAML-Specific Optional Features

* **Allowed Redirect URIs:** Restrict the redirect targets that can be used in the authentication flow.
* **Unique Identifier:** Define which IdP sub-claim key identifies a user.
* **Sub-claim Delimiters:** Configure custom delimiters if your IdP uses a format other than comma-separated values.

## Related Pages

For end-to-end IdP setup examples, see:

* [Set Up Okta as a SAML Authentication Method](https://docs.akeyless.io/docs/saml-auth-okta)
* [Set Up Ping Identity as a SAML Authentication Method](https://docs.akeyless.io/docs/saml-auth-ping-identity)
* [Set Up Microsoft Entra ID as a SAML Authentication Method](https://docs.akeyless.io/docs/saml-auth-azure-ad)
