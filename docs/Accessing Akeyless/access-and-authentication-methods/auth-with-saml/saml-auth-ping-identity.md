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

5. From the **Signing** options, select the **Sign Assertion** radio button, then select **Continue to Next Step**.

6. On the **Attribute Mapping** tab, select **Add New Attribute**, and add the following attribute settings:

    * **Application Attribute**: `SAML_SUBJECT` should be mapped to `User ID`
    * **Application Attribute**: `Email` should be mapped to `Email Address`

7. Edit your Application configuration and in the `SUBJECT NAMEID FORMAT` field, select `urn:oasis:names:tc:SAML:2.0:nameid-format:transient`.

8. Select **Continue to Next Step**.

9. Add the groups in your Ping Identity account to this application, then select **Continue to Next Step** and **Finish**.

Your new application appears in the list of available applications.

> ℹ️ **Note:**
>
> Akeyless uses dedicated SAML endpoints per Authentication Method. Do not use hardcoded global endpoints. Always copy endpoint values from the specific Akeyless SAML Authentication Method you are configuring.

## Create a SAML Authentication Method

1. Log in to the Akeyless Web Console, and go to **Administration**, then **Users & Auth Methods**.

2. Select **New**.

3. In **Select Type**, select **SAML**.

4. In the **Metadata URL** field, add the metadata URL from your Ping application.

5. Set the **Unique Identifier** field with `email`.

    > 👍 Note
    >
    > **Unique Identifier** should be a **key** name, that is not the value itself. For example, `email` should be provided as is, and not the actual email address.

6. Select **Finish**.

7. Copy the dedicated SAML endpoint values from the created Akeyless Authentication Method, then verify the same values are configured in Ping Identity:
   * SAML **ACS URL**
   * SAML **Metadata/Entity ID URL**

## Associate with Access Roles

After creating the method, associate it with one or more Access Roles so authenticated users can access the required resources.

1. In the Akeyless Console, go to **Administration**, then **Users & Auth Methods**.
2. Select the SAML Authentication Method.
3. Add the relevant Access Roles.
4. Save the changes.

## Authenticate with Ping Identity SAML

### Akeyless Console

1. Open [https://console.akeyless.io](https://console.akeyless.io).
2. In the **Or continue with** section, select **SAML**.
3. Enter the SAML Authentication Method **Access ID**.
4. Complete sign-in in Ping Identity.

### Akeyless CLI

```shell
akeyless configure \
  --profile ping-saml \
  --access-id <SAML Access ID> \
  --access-type saml
```

## Troubleshooting

If authentication fails, check the following:

* The Ping application uses the dedicated ACS URL and Entity ID from this specific Akeyless SAML Authentication Method.
* The Ping assertion includes the key configured in **Unique Identifier**.
* The user is assigned to the Ping application.
* The metadata URL configured in Akeyless is valid and current.
