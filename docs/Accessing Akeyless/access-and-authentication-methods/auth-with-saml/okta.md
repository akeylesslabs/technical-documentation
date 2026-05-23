---
title: Okta SAML Authentication
excerpt: ''
deprecated: false
hidden: false
metadata:
  title: Okta SAML Authentication
  description: ''
  robots: index
next:
  description: ''
---
This guide explains how to configure Okta as the Identity Provider (IdP) for SAML authentication in Akeyless.

## Prerequisites

* An Okta administrator account.
* An Akeyless account.

## Create an Okta SAML Application

1. In Okta, go to **Applications**, then create a new app integration of type **SAML 2.0**.
2. Enter an application name and continue to SAML configuration.
3. Configure the SAML app:
   * **Single sign-on URL:** Use the SAML **ACS URL** generated for your Akeyless SAML Authentication Method.
   * **Audience URI (SP Entity ID):** Use the SAML **Metadata/Entity ID URL** generated for your Akeyless SAML Authentication Method.
4. Configure attribute mapping:
   * `email` mapped to `user.email`
   * `user` mapped to `user.login`
5. If you use group-based role association, add a group claim for `groups`.
6. Save the application.

> ℹ️ **Note:**
>
> Akeyless uses dedicated SAML endpoints per Authentication Method. Do not use hardcoded global endpoints. Always copy endpoint values from the specific Akeyless SAML Authentication Method you are configuring.

## Get Okta IdP Metadata

Get one of the following from Okta:

* **IdP Metadata URL** from the active signing certificate actions.
* **IdP Metadata XML** from the Okta SAML setup instructions.

You will use this metadata in Akeyless when creating the SAML Authentication Method.

## Create the SAML Authentication Method in Akeyless

You can create the method from the Console or CLI.

### Akeyless Console

1. In the Akeyless Console, go to **Administration**, then **Users & Auth Methods**.
2. Select **+ New**, then **SAML**.
3. Set:
   * **Name**
   * **IdP Metadata URL** or **IdP Metadata XML**
   * **Unique Identifier** (for example, `email`)
4. Save the Authentication Method.
5. Copy the dedicated SAML endpoint values shown for this Authentication Method, then confirm the same values are configured in Okta:
   * SAML **ACS URL**
   * SAML **Metadata/Entity ID URL**

### Akeyless CLI

```shell
akeyless auth-method create saml \
  --name "my okta app" \
  --idp-metadata-url "<okta-idp-metadata-url>" \
  --unique-identifier email
```

## Authenticate with Okta SAML

### Akeyless CLI

```shell
akeyless configure \
  --profile okta-app \
  --access-id <SAML Access ID> \
  --access-type saml
```

Then run commands with that profile, for example:

```shell
akeyless list-items --profile okta-app
```

### Akeyless Console

1. Open [https://console.akeyless.io](https://console.akeyless.io).
2. Select **SAML**.
3. Enter the SAML Authentication Method **Access ID**.
4. Complete sign-in in Okta.
