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

## Prerequisites

To use Ping Identity SAML authentication for the Akeyless Platform, you must have an Akeyless account and a Ping Identity account (either a trial account or a regular account with enterprise SSO support).

## Create a Ping Identity Application

1. Log in to [PingOne](https://admin.pingone.com/web-portal/login), and go to **Applications > Add Application > New SAML Application**.

2. On the **Application Details** page, define the application name, description, and category, then select **Continue to Next Step**.

3. On the **SAML Configuration** page, select **Import from URL**, and import the SAML metadata URL generated for your specific Akeyless SAML Authentication Method.

4. Once the metadata has been uploaded, configuration information appears. Ensure that:

* **Assertion Consumer Service (ACS)** matches the dedicated ACS URL for your Akeyless SAML Authentication Method.
* **Entity ID** matches the dedicated Metadata/Entity ID URL for your Akeyless SAML Authentication Method.

1. From the **Signing** options, select the **Sign Assertion** radio button, then select **Continue to Next Step**.

2. On the **Attribute Mapping** tab, select **Add New Attribute**, and add the following attribute settings:

    * **Application Attribute**: `SAML_SUBJECT` should be mapped to `User ID`
    * **Application Attribute**: `Email` should be mapped to `Email Address`

3. Edit your Application configuration and in the `SUBJECT NAMEID FORMAT` field, select `urn:oasis:names:tc:SAML:2.0:nameid-format:transient`

4. Select **Continue to Next Step**.

5. Add the groups in your Ping Identity account to this application, then select **Continue to Next Step** and **Finish**.

Your new application appears in the list of available applications.

> ℹ️ **Note:**
>
> Akeyless uses dedicated SAML endpoints per Authentication Method. Do not use hardcoded global endpoints. Always copy endpoint values from the specific Akeyless SAML Authentication Method you are configuring.

## Create a SAML Authentication Method

1. Log in to the Akeyless Web Console, and go to **Administration**, then **Users & Auth Methods**.

2. Select **+ New**, then **SAML**.

3. In the **IdP Metadata URL** field, add the metadata URL from your Ping application.

4. Set the **Unique Identifier** field with `email`.

    > 👍 Note
    >
    > **Unique Identifier** should be a **key** name, that is not the value itself. For example, `email` should be provided as is, and not the actual email address.

5. Click **Finish**.

6. Copy the dedicated SAML endpoint values from the created Akeyless Authentication Method, then verify the same values are configured in Ping Identity:
   * SAML **ACS URL**
   * SAML **Metadata/Entity ID URL**
