---
title: Azure AD - OIDC
excerpt: ''
deprecated: false
hidden: false
metadata:
  title: Azure AD - OIDC
  description: ''
  robots: index
next:
  description: ''
---
To use Azure Active Directory (AAD) as an IdP to authenticate the Akeyless Platform by way of OIDC, follow the steps below.

## Create an Application

1. In your Azure account, go to **App registrations > New registrations**.

    ![Illustration for: Create an Application 1. In your Azure account, go to App registrations > New registrations.](https://files.readme.io/c9edb74-image-20210902-145138.png)

2. For **Redirect URI**, select **Web** for **Application type**. Set `https://auth.akeyless.io/oidc/callback` as the value and select **Register**.

    ![Illustration for: 1. In your Azure account, go to App registrations > New registrations. 2. For Redirect URI, type select Web for Application type. Set…](https://files.readme.io/d399957-image-20210902-145556.png)

3. Once the app has been created, you need to obtain the **Client ID**, **Client Secret**, and the **Issuer URL**:

    * The **Client ID** can be fetched from **Overview > Application (client) ID**:

    ![Illustration for: 3. Once the app has been created, you need to obtain the Client ID, Client Secret, and the Issuer URL: The Client ID can be fetched from Overview >…](https://files.readme.io/963adb9-image-20210902-150241.png)

    * The **Client Secret** can be created under **Certificates & Secrets > New Client Secret** (make sure to copy the Secret **Value**, not the Secret ID):

    ![Illustration for: The Client ID can be fetched from Overview > Application (client) ID: The Client Secret can be created under Certificates and Secrets > New Client Secret…](https://files.readme.io/73548af-image-20210902-150722.png)

    * The **Issuer URL** can be fetched from **Overview > Endpoints > OpenID Connect metadata document** (note that the suffix **/.well-known/openid-configuration** should be omitted so that the Issuer URL will look like: `https://login.microsoftonline.com/tenant-id-abcd-efgh-a123-b456/v2.0`):

    ![Illustration for: The Issuer URL can be fetched from Overview > Endpoints > OpenID Connect metadata document (note that the suffix /.well-known/openid-configuration should be…](https://files.readme.io/cb76d3c-image-20210902-151402.png)

4. To add the AD group as a sub-claim, go to **Token configuration > Add Groups Claim**:

    ![Illustration for: The Issuer URL can be fetched from Overview > Endpoints > OpenID Connect metadata document (note that the suffix /.well-known/openid-configuration should be…](https://files.readme.io/938b863-image-20210902-155120.png)

5. To bind the Azure application with your Akeyless account, create an OIDC Authentication Method using either CLI or UI, as described below.

## Create an OIDC Authentication Method with the CLI

```shell
akeyless auth-method create oidc --name 'my Azure app' --issuer https://{your-issuer-url} --client-id {your-client-id} --client-secret {your-client-secret} --unique-identifier {your-unique-identifier (for example, 'email' or 'username')}
```

This can also be done from the Console UI by creating a New OIDC Auth Method and filling in the same required parameters.

Notice that **unique-identifier** must be an available claim, which out of the box might be the `preferred_username` field.
If you wish to use a field such as **email** instead, make sure to first **Add optional claim** under **Token configuration** (in the Azure App), and add the **email** claim.

To log in with SSO to Akeyless using your new Azure AD OIDC Auth Method, log in to the Console, browse to Auth Methods, select the newly created OIDC Auth Method, and click **Generate OIDC Bookmark URL**. This provides the SSO link.

## Log in With OIDC Using the CLI

Configure a new profile with your Access ID from the previous step and OIDC type (if no profile name is provided, the default will be configured):

```shell
akeyless configure --access-id <your-access-id> --access-type oidc --profile 'azure-app'
```

Now, you can run any Akeyless CLI command and be authenticated with the Azure application:

```shell
akeyless list-items --profile azure-app
```

## Azure Groups Overage Claim

Azure AD enforces a limit on the number of groups it includes directly in a token: 200 for JWT/OIDC tokens and 150 for SAML tokens. When a user is a member of more groups than this limit (directly or indirectly), Azure omits the `groups` claim from the token and instead includes a distributed-claim pointer:

```json
{
  "_claim_names": {
    "groups": "src1"
  },
  "_claim_sources": {
    "src1": {
      "endpoint": "https://graph.microsoft.com/v1.0/users/{objectId}/getMemberObjects"
    }
  }
}
```

Akeyless automatically detects this pattern and resolves the full group list by calling the Microsoft Graph API on behalf of the OIDC auth method. No additional Akeyless configuration is required. However, the Azure app registration must be granted the Microsoft Graph **Application** permission `GroupMember.Read.All` (or the broader `Directory.Read.All`), with admin consent granted, so that Akeyless can retrieve the user's group memberships.

### Grant the Required API Permission

1. In the Azure portal, navigate to **App registrations** and select your Akeyless OIDC application.
2. Go to **API permissions** and select **Add a permission**.
3. Select **Microsoft Graph**.
4. Select **Application permissions**.
5. Search for and add `GroupMember.Read.All` (or `Directory.Read.All`).
6. Select **Grant admin consent for \<your directory\>** and confirm.

> ℹ️ **Note:**
>
> This permission is only required when users may belong to more than 200 groups. If no user in your tenant exceeds the overage limit, no additional permissions are needed.
