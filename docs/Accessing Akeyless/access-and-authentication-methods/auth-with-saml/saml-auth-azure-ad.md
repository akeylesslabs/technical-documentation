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

* A Microsoft Entra ID tenant with admin permissions.
* An Akeyless account.

## Create a Microsoft Entra SAML Application

1. In the Azure portal, go to **Enterprise applications**.
2. Create a new non-gallery application.
3. Open the application, then go to **Single sign-on**, and select **SAML**.
4. In **Basic SAML Configuration**, set:
   * **Identifier (Entity ID):** Use the SAML **Metadata/Entity ID URL** generated for your Akeyless SAML Authentication Method.
   * **Reply URL (Assertion Consumer Service URL):** Use the SAML **ACS URL** generated for your Akeyless SAML Authentication Method.
5. In **Attributes & Claims**, add a claim for `email` and, if needed, configure group claims for role association.
6. Copy the **App Federation Metadata URL** from the SAML configuration. You will use it in Akeyless.
7. Assign the required users and groups to the enterprise application.

> ℹ️ **Note:**
>
> Akeyless uses dedicated SAML endpoints per Authentication Method. Do not use hardcoded global endpoints. Always copy endpoint values from the specific Akeyless SAML Authentication Method you are configuring.

## Create the SAML Authentication Method in Akeyless

You can create the method from the Console or CLI.

### Akeyless Console

1. In the Akeyless Console, go to **Administration**, then **Users & Auth Methods**.
2. Select **New**.
3. In **Select Type**, select **SAML**.
4. Set **Name**, **Metadata URL** (the App Federation Metadata URL), and **Unique Identifier** (for example, `email`).
5. Save the Authentication Method.
6. Copy the dedicated SAML endpoint values shown for this Authentication Method, then confirm the same values are configured in Microsoft Entra:
   * SAML **ACS URL**
   * SAML **Metadata/Entity ID URL**

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

## Troubleshooting

If authentication fails, check the following:

* The Microsoft Entra application uses the dedicated ACS URL and Entity ID from this specific Akeyless SAML Authentication Method.
* The configured **Unique Identifier** key exists in SAML claims.
* The user is assigned to the Microsoft Entra enterprise application.
* The App Federation Metadata URL is still valid and reachable.
