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

<Callout icon="ℹ️" theme="info">
  ### **Before you start:**

  Microsoft Entra ID requires each Enterprise Application to use unique SAML endpoint values. If you plan to configure more than one Entra application against the same Akeyless account, you'll need **Dedicated SAML Endpoint** enabled on the corresponding Authentication Method — see [Configure Dedicated SAML Endpoints](#configure-dedicated-saml-endpoints-for-microsoft-entra-id) below. If you're only configuring a single Entra application, the shared endpoints work and you can skip straight to using them.
</Callout>

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

If you need this application to use dedicated, isolated endpoint values instead — because you're configuring multiple Entra applications against Akeyless — skip this section and follow [Configure Dedicated SAML Endpoints](#configure-dedicated-saml-endpoints-for-microsoft-entra-id) instead.

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

1. Open [https://console.akeyless.io](https://console.akeyless.io).
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

The **Dedicated SAML Endpoint** flag is set per Authentication Method, you can enable it for one Entra Authentication Method while other SAML methods in the same Akeyless account keep using the shared endpoints. This is the recommended mode for Entra ID whenever you're configuring more than one Enterprise Application, since Entra requires unique SAML values per application.

When enabled, this Authentication Method exposes its own Entity ID, Assertion Consumer Service (ACS) URL, and metadata URL, based on its Access ID. Replace `<SAML_AUTH_METHOD_ACCESS_ID>` with the Access ID of this Authentication Method.

| Endpoint                 | Format                                                                |
| ------------------------ | --------------------------------------------------------------------- |
| Entity ID / Identifier   | `https://auth.akeyless.io/saml/sp/<SAML_AUTH_METHOD_ACCESS_ID>`       |
| Reply URL / ACS URL      | `https://auth.akeyless.io/saml/acs/<SAML_AUTH_METHOD_ACCESS_ID>`      |
| Akeyless SP Metadata URL | `https://auth.akeyless.io/saml/metadata/<SAML_AUTH_METHOD_ACCESS_ID>` |

The dedicated Entity ID and Reply URL depend on the Access ID, which only exists after the Akeyless Authentication Method is created — but Akeyless needs an IdP metadata value to create the method in the first place, and that metadata isn't available until the Entra application exists. Since **Identifier** and **Reply URL** fields cannot reliably be edited on an existing Entra Enterprise Application after creation, avoid editing Entra at all: create the Akeyless method first with a temporary metadata value, configure Entra once with the real dedicated endpoints, then finish by updating the Akeyless method with Entra's real metadata. No step requires going back into Entra to change a value.

1. **Create the Akeyless SAML Authentication Method with a temporary metadata value.**

   Create the method with **Dedicated SAML Endpoint** enabled and a placeholder metadata URL or XML file — the value only needs to satisfy the create command for now and will be replaced in step 4.

   ```shell
   akeyless auth-method create saml \
     --name "<SAML Auth Method Name>" \
     --idp-metadata-url "https://auth.akeyless.io/saml/metadata" \
     --unique-identifier <email|username|UPN> \ 
     --dedicated-saml-endpoint true
   ```

   > **Note**
   > The `--idp-metadata-url` value above is a placeholder only, used to satisfy method creation before the real Entra metadata exists. It is not used for authentication until it's replaced in step 4.

   Enable **Dedicated SAML Endpoint** for this method in the Console if it isn't set by your CLI version. After creation, copy the returned SAML Authentication Method **Access ID** — you will not need to touch Entra's Identifier or Reply URL fields again after this point.

2. **Create the Microsoft Entra Enterprise Application with the real dedicated endpoints.**

   In Microsoft Entra ID, create a new Enterprise Application and configure SAML using the dedicated values built from the Access ID in step 1 — set these once, correctly, the first time:

   ```
   Identifier / Entity ID:
   https://auth.akeyless.io/saml/sp/<SAML_AUTH_METHOD_ACCESS_ID>

   Reply URL / ACS URL:
   https://auth.akeyless.io/saml/acs/<SAML_AUTH_METHOD_ACCESS_ID>
   ```

3. **Copy the Entra App Federation Metadata URL.**

   From the Entra SAML configuration page, copy the **App Federation Metadata URL** for the Enterprise Application.

4. **Update the Akeyless SAML Authentication Method with the real Entra metadata.**

   Replace the placeholder metadata from step 1 with the real App Federation Metadata URL from Entra:

   ```shell
   akeyless auth-method update saml \
     --name "<SAML Auth Method Name>" \
     --idp-metadata-url "<ENTRA_APP_FEDERATION_METADATA_URL>" \
     --unique-identifier <email|username|UPN> \
     --dedicated-saml-endpoint true
   ```

   Or, in the Console: go to **Administration** > **Users & Auth Methods**, select the Authentication Method, update the **Metadata URL** field, and save.

5. **Test SAML authentication.**

   Test the SAML login using the Akeyless SAML Authentication Method Access ID. Since the Entra application was configured with its final dedicated values in step 2 and never edited afterward, no further changes are needed on the Entra side.

## Troubleshooting

If authentication fails, check the following:

- The Microsoft Entra application uses the correct endpoint values for this specific Authentication Method — the shared endpoints, or the dedicated endpoints if **Dedicated SAML Endpoint** is enabled on this method.
- The configured **Unique Identifier** key exists in SAML claims.
- The user is assigned to the Microsoft Entra enterprise application.
- The App Federation Metadata URL configured in Akeyless is current — if the Entra application's certificate or configuration changed since the metadata was last copied, re-run the update step above with a fresh App Federation Metadata URL.

<br />
