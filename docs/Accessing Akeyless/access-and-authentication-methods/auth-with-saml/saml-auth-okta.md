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

- An Okta administrator account.
- An Akeyless account.

## Create an Okta SAML Application

1. In Okta, go to **Applications**, then create a new app integration of type **SAML 2.0**.
2. Enter an application name and continue to SAML configuration.
3. Configure the SAML app using the shared Akeyless endpoints:
   - **Single sign-on URL:** `https://auth.akeyless.io/saml/acs`
   - **Audience URI (SP Entity ID):** `https://auth.akeyless.io/saml/metadata`
4. Configure attribute mapping:
   - `email` mapped to `user.email`
   - `user` mapped to `user.login`
5. If you use group-based role association, add a group claim for `groups`.
6. Save the application.

<Callout icon="ℹ️" theme="info">
  ### **Note:**

  These are the default, shared Akeyless endpoints and work for most setups. If you need Okta to use unique endpoint values scoped to this specific Authentication Method — for example, to run multiple isolated Okta apps against the same Akeyless account — see [Optional: Dedicated SAML Endpoints](#optional-dedicated-saml-endpoints-for-okta) below.
</Callout>

## Get Okta IdP Metadata

Get one of the following from Okta:

- **IdP Metadata URL** from the active signing certificate actions.
- **IdP Metadata XML** from the Okta SAML setup instructions.

You will use this metadata in Akeyless when creating the SAML Authentication Method.

## Create the SAML Authentication Method in Akeyless

You can create the method from the Console or CLI.

### Akeyless Console

1. In the Akeyless Console, go to **Administration**, then **Users & Auth Methods**.
2. Select **New**.
3. In **Select Type**, select **SAML**.
4. Set **Name**, **Metadata URL** or **Metadata XML**, and **Unique Identifier** (for example, `email`).
5. Leave **Dedicated SAML Endpoint** off to use the shared endpoints already configured in Okta above. (See the optional section below if you need per-method endpoints instead.)
6. Save the Authentication Method.

### Akeyless CLI

```shell
akeyless auth-method create saml \
  --name "my okta app" \
  --idp-metadata-url "<okta-idp-metadata-url>" \
  --unique-identifier email
```

## Associate with Access Roles

After creating the method, associate it with one or more Access Roles so authenticated users can access the required resources.

1. In the Akeyless Console, go to **Administration**, then **Users & Auth Methods**.
2. Select the SAML Authentication Method.
3. Add the relevant Access Roles.
4. Save the changes.

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

## Dedicated SAML Endpoints for Okta

The **Dedicated SAML Endpoint** flag is set per Authentication Method,  you can enable it for one Authentication Method while other SAML methods in the same Akeyless account keep using the shared endpoints. Enable it if you plan to run more than one Okta app against Akeyless and need each one to have unique SAML values.

When enabled, this Authentication Method exposes its own endpoints scoped to its Access ID. Replace `<SAML_AUTH_METHOD_ACCESS_ID>` with the Access ID of this method:

| Endpoint                     | Format                                                                |
| ---------------------------- | --------------------------------------------------------------------- |
| Single sign-on URL / ACS URL | `https://auth.akeyless.io/saml/acs/<SAML_AUTH_METHOD_ACCESS_ID>`      |
| Audience URI / Entity ID     | `https://auth.akeyless.io/saml/sp/<SAML_AUTH_METHOD_ACCESS_ID>`       |
| SP Metadata URL              | `https://auth.akeyless.io/saml/metadata/<SAML_AUTH_METHOD_ACCESS_ID>` |

Because the Access ID doesn't exist until the Akeyless Authentication Method is created, and Akeyless needs Okta's IdP metadata to create it, use this order:

1. In Okta, create the SAML app with temporary placeholder values for **Single sign-on URL** and **Audience URI** (any unique HTTPS URLs) so Okta will save the app and expose its metadata.
2. Copy the Okta IdP metadata and create the Akeyless SAML Authentication Method with **Dedicated SAML Endpoint** enabled.
3. Copy the resulting Access ID and go back to Okta, replacing the placeholder values with the dedicated endpoints above.
4. Test sign-in.

## Troubleshooting

If authentication fails, check the following:

- Okta assertion includes the claim key configured in **Unique Identifier**.
- Okta SAML app uses the correct endpoint values for this specific Authentication Method — the shared endpoints by default, or the dedicated endpoints if **Dedicated SAML Endpoint** is enabled on this method.
- The metadata source in Akeyless is valid and current.
- The user or group is assigned to the Okta application.

<br />
