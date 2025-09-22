---
title: Ping Identity SAML Authentication
excerpt: ''
deprecated: false
hidden: false
metadata:
  title: Ping Identity SAML Authentication
  description: ''
  robots: index
next:
  description: ''
---
[Ping Identity](https://www.pingidentity.com/en.html) provides enterprise services, including SSO using the SAML protocol.

To use Ping Identity to authenticate users in the Akeyless Platform, you need to set up Akeyless as an application in the Ping Identity Platform. You can then create a SAML authentication method in Akeyless for Ping Identity.

# Prerequisites

In order to use Ping Identity SAML authentication for the Akeyless Platform, you must have an Akeyless account and a Ping Identity account (either a trial account or a regular account with enterprise SSO support).

# Create a Ping Identity Application

1. Log in to [PingOne](https://admin.pingone.com/web-portal/login), and go to **Applications > Add Application > New SAML Application**.

2. On the **Application Details** page, define the application name, description, and category, then select **Continue to Next Step**.

3. On the **SAML Configuration** page, select **Import from URL**, and enter the Akeyless metadata URL: `https://auth.akeyless.io/saml/metadata`

4. Once the metadata has been uploaded, configuration information appears. Ensure that:

- **Assertion Consumer Service (ACS)**: `https://auth.akeyless.io/saml/acs`
- **Entity ID**: `https://auth.akeyless.io/saml/metadata`

5. From the **Signing** options, select the **Sign Assertion** radio button, then select **Continue to Next Step**.

6. On the **Attribute Mapping** tab, select **Add New Attribute**, and add the following attribute settings:

- **Application Attribute**: `SAML_SUBJECT` should be mapped to `User ID`
- **Application Attribute**: `Email` should be mapped to `Email Address`

7. Edit your Application configuration and in the **SUBJECT NAMEID FORMAT** field,  
   select `urn:oasis:names:tc:SAML:2.0:nameid-format:transient`

8. Select **Continue to Next Step**.

9. Add the groups in your Ping Identity account to this application, then select **Continue to Next Step** and **Finish**.

Your new application appears in the list of available applications.

# Create a SAML Authentication Method

1. Log in to the Akeyless Web Console, and go to **Users & Auth Methods > New > SAML**.

2. In the **IDP Metadata URL** field, add the URL metadata from your Ping Application configuration tab.

3. Set the **Unique Identifier** field with `email`.

> 👍 Note
> 
> **Unique Identifier** should be a **key** name, i.e. not the value itself. for example, `email` should be provided as is, and not the actual email address.

3. Click **Finish**.