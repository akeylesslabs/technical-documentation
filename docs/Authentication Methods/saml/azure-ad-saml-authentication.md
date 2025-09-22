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
This guide will take you through the steps to set up SAML authentication with Azure AD, both on the Azure end and on the Akeyless end.

> 🚧 Note
> 
> The Azure AD limit for groups per user is set by default to 150. Users with more groups cannot use SAML with Azure.

# Create an Azure AD application

1. On your Azure Dashboard, select **Enterprise Applications**.

2. Create a new application and select the **Create your own application** option.

3. Name your application **Akeyless** and select the **Integrate any application you don't find in the gallery (Non-gallery)** option.

4. Under Getting Started, choose **Set up single sign-on**.

5. Select **SAML** to be transferred to the SAML configuration page.

6. Insert the following URLs to the configuration:

- Identifier (Entity ID): `https://auth.akeyless.io/saml/metadata`

- Reply URL (Assertion Consumer Service URL): `https://auth.akeyless.io/saml/acs`

7. After filling in the details, you will be able to view the SAML Signing Certificate.  
   Copy the **App Federation Metadata URL** (starts with `https://login.microsoftonline.com/...`) and paste it somewhere accessible, as you will need it for the Akeyless-side steps.

8. In your SAML application's **Attributes & Claims**, select Edit to add user & group claims.

9. Select **Add new claim** - and fill in the following details:

- `Name` = `email`
- `Source attribute` = `user.userprincipalname`

> 📘 Info
> 
> **Customize SAML token claims**
> 
> You can customize your SAML token claims in Azure as decsribed in [this](https://learn.microsoft.com/en-us/azure/active-directory/develop/saml-claims-customization#edit-nameid) guide.

10. Select **Add a group claim** - Configure the group claim according to the instructions provided in [here](https://learn.microsoft.com/en-us/azure/active-directory/hybrid/how-to-connect-fed-group-claims#add-group-claims-to-tokens-for-saml-applications-using-sso-configuration). See the following example:

- On the multiple-choice groups-association question, select **Security groups**.
- Source attribute `Group ID` (or, `sAMAccountName`, for Active Directory-synchronized groups).
- under Advanced options, select **Customize**, and set the name to **groups**.

> 👍 Note
> 
> The group sub-claim by default will provide the group's Azure AD object identifier (OID), and not the group name - which affects how you should set the groups' sub-claims when configuring Access Roles. If you wish to expose the group display name as an attribute instead, you can either use `sAMAccountName` - but **only** for groups that were synced from an on-premise Active Directory, or you can follow the instruction on how to [emit cloud-only group display name](https://learn.microsoft.com/en-us/azure/active-directory/hybrid/how-to-connect-fed-group-claims#emit-cloud-only-group-display-name-in-token-preview).

11. Finally, make sure to add and assign the relevant **Users and groups** to the application.

Now for the Akeyless side:

# Create SAML Authentication Method

The Akeyless side of the setup can be done either from the CLI or the console. Choose whichever you find preferable.

## Using the Akeyless CLI

Run the following command:

```shell
akeyless auth-method create saml \
--name '<saml-name>' \
--idp-metadata-url  '<your-idp-metadata-url>' \
--unique-identifier email
```

The IDP metadata URL is the **App Federation Metadata URL** you copied from the Azure process.

## Using the Akeyless Console

1. Go to the **Users & Auth Methods** tab in your console.

2. Select **New > SAML**.

3. Fill in the mandatory parameters:

- Name: The in-system name for the authentication method.
- IDP Metadata URL: The  **App Federation Metadata URL** you copied from the Azure process.
- Unique identifier: The required identifier. In this case, you can use **email**.

Your SAML authentication should be up and running.