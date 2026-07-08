---
title: Azure AD SAML Authentication
excerpt: ''
deprecated: false
hidden: false
metadata:
  title: Azure AD SAML Authentication
  description: ''
  robots: index
next:
  description: ''
---
This guide explains how to configure Microsoft Entra ID (Azure AD) as the Identity Provider (IdP) for SAML authentication in Akeyless.

## Prerequisites

- A Microsoft Entra ID tenant with admin permissions.
- An Akeyless account.

> ℹ️ **Before you start:**
> Microsoft Entra ID requires each Enterprise Application to use unique SAML endpoint values. If you plan to configure more than one Entra application against the same Akeyless account, you'll need **Dedicated SAML Endpoint** enabled on the corresponding Authentication Method — see [Configure Dedicated SAML Endpoints](#configure-dedicated-saml-endpoints-for-microsoft-entra-id) below. If you're only configuring a single Entra application, the shared endpoints work and you can skip straight to using them.

## Create a Microsoft Entra SAML Application

1. In the Azure portal, go to **Enterprise applications**.
2. Create a new non-gallery application.
3. Open the application, then go to **Single sign-on**, and select **SAML**.
4. In **Basic SAML Configuration**, set:
   - **Identifier (Entity ID):** `https://auth.akeyless.io/saml/metadata`
   - **Reply URL (Assertion Consumer Service URL):** `https://auth.akeyless.io/saml/acs`
5. In **Attributes & Claims**, add a claim for `email` and, if needed, configure group claims for role association.
6. Copy the **App Federation Metadata URL** from the SAML configuration. You will use it in Akeyless.
7. Assign the required users and groups to the enterprise application.

If you need this application to use dedicated, isolated endpoint values instead — because you're configuring multiple Entra applications against Akeyless — skip the values in step 4 and follow [Configure Dedicated SAML Endpoints](#configure-dedicated-saml-endpoints-for-microsoft-entra-id) instead.

## Create the SAML Authentication Method in Akeyless

You can create the method from the Console or CLI.

### Akeyless Console

1. In the Akeyless Console, go to **Administration**, then **Users & Auth Methods**.
2. Select **New**.
3. In **Select Type**, select **SAML**.
4. Set **Name**, **Metadata URL** (the App Federation Metadata URL), and **Unique Identifier** (for example, `email`).
5. Leave **Dedicated SAML Endpoint** off if you used the shared endpoints above.
6. Save the Authentication Method.

### Akeyless CLI

```shell
akeyless auth-method create saml \
  --name "<saml-name>" \
  --idp-metadata-url "<app-federation-metadata-url>" \
  --unique-identifier email
```

## Associate with Access Roles

After creating the method, associate it with one or more Access Roles so authenticated users can access the required resources.

1. In the Akeyless Console, go to **Administration**, then **Users & Auth Methods**.
2. Select the SAML Authentication Method.
3. Add the relevant Access Roles.
4. Save the changes.

## Validate Authentication

1. Open <https://console.akeyless.io>.
2. Select **SAML** and provide the SAML Authentication Method **Access ID**.
3. Complete sign-in through Microsoft Entra.

For CLI usage after setup:

```shell
akeyless configure \
  --profile entra-saml \
  --access-id <SAML Access ID> \
  --access-type saml
```

## Configure Dedicated SAML Endpoints for Microsoft Entra ID

The **Dedicated SAML Endpoint** flag is set per Authentication Method, not per account — you can enable it for this Entra Authentication Method while other SAML methods in the same Akeyless account keep using the shared endpoints. This is the recommended mode for Entra ID whenever you're configuring more than one Enterprise Application, since Entra requires unique SAML values per application.

When enabled, this Authentication Method exposes its own Entity ID, Assertion Consumer Service (ACS) URL, and metadata URL, based on its Access ID. Replace `<SAML_AUTH_METHOD_ACCESS_ID>` with the Access ID of this Authentication Method:

| Endpoint | Format |
| --- | --- |
| Entity ID / Identifier | `https://auth.akeyless.io/saml/sp/<SAML_AUTH_METHOD_ACCESS_ID>` |
| Reply URL / ACS URL | `https://auth.akeyless.io/saml/acs/<SAML_AUTH_METHOD_ACCESS_ID>` |
| Akeyless SP Metadata URL | `https://auth.akeyless.io/saml/metadata/<SAML_AUTH_METHOD_ACCESS_ID>` |

When configuring Microsoft Entra ID, you may need to create the Entra Enterprise Application before the Akeyless SAML Authentication Method exists. However, Akeyless needs the Entra App Federation Metadata URL to create the SAML Authentication Method, while Entra needs the Akeyless Entity ID and ACS URL to save the SAML application.

To handle this, use temporary unique placeholder values when creating the Entra Enterprise Application. After the Akeyless SAML Authentication Method is created, replace the placeholders with the real dedicated Akeyless endpoints.

1. **Create the Microsoft Entra Enterprise Application.**

   In Microsoft Entra ID, create a new Enterprise Application and configure SAML.

   Use temporary unique HTTPS values for the Identifier and Reply URL. These values are used only to allow the Entra application to be saved and to expose the App Federation Metadata URL.

   For example:

Identifier / Entity ID:
https://auth.akeyless.io/saml/sp/prod
Reply URL / ACS URL:
https://auth.akeyless.io/saml/acs/prod
> **Important**
   > These are temporary bootstrap values only. They must be unique and use HTTPS. After the Akeyless SAML Authentication Method is created, replace them with the real dedicated endpoints based on the Auth Method Access ID.

2. **Copy the Entra App Federation Metadata URL.**

   From the Entra SAML configuration page, copy the **App Federation Metadata URL** for the Enterprise Application.

3. **Create the Akeyless SAML Authentication Method with Dedicated SAML Endpoint enabled.**

```shell
   akeyless auth-method create saml \
     --name "<SAML Auth Method Name>" \
     --idp-metadata-url "<ENTRA_APP_FEDERATION_METADATA_URL>" \
     --unique-identifier <email|username|UPN>
```

   Enable **Dedicated SAML Endpoint** for this method in the Console if not set via CLI. After the Authentication Method is created, copy the returned SAML Authentication Method Access ID.

4. **Replace the temporary values in Microsoft Entra ID.**

   Go back to the Entra Enterprise Application and replace the temporary SAML values with the dedicated Akeyless endpoints for the matching SAML Authentication Method.