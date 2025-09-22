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
To use Azure Active Directory (AAD) as an IdP to authenticate the Akeyless Platform via OIDC, follow the steps below.

## Create an application

1. In your Azure account, go to **App registrations > New registrations**.

![](https://files.readme.io/c9edb74-image-20210902-145138.png "image-20210902-145138.png")

2. For **Redirect URI** type select **Web** for **Application type**  
   Set `https://auth.akeyless.io/oidc/callback` as a value and press **Register**.

![](https://files.readme.io/d399957-image-20210902-145556.png "image-20210902-145556.png")

3. Once the app has been created, you need to obtain the **Client ID**, **Client Secret**, and the **Issuer URL**:

- The **Client Id** can be fetched from **Overview > Application (client) ID**: 

![](https://files.readme.io/963adb9-image-20210902-150241.png "image-20210902-150241.png")

- The **Client Secret** can be created under **Certificates & secrets > New Client Secret** (make sure to copy the Secret **Value**, not the Secret ID):

![](https://files.readme.io/73548af-image-20210902-150722.png "image-20210902-150722.png")

- The **Issuer URL** can be fetched from **Overview > Endpoints > OpenID Connect metadata document** (note that the suffix **/.well-known/openid-configuration** should be omitted so that the Issuer URL will look like: `https://login.microsoftonline.com/tenant-id-abcd-efgh-a123-b456/v2.0`): 

![](https://files.readme.io/cb76d3c-image-20210902-151402.png "image-20210902-151402.png")

4. In order to add the  AD group as a sub-claim, go to **Token configuration > Add Groups Claim**:

![](https://files.readme.io/938b863-image-20210902-155120.png "image-20210902-155120.png")

5. In order to bind the Azure application with your Akeyless account, you need to create an OIDC Authentication Method using either CLI or UI, as described below.

## Create an OIDC Authentication Method from the CLI

```shell
akeyless auth-method create oidc --name 'my Azure app' --issuer https://{your-issuer-url} --client-id {your-client-id}  --client-secret {your-client-secret} --unique-identifier {your-unique-identifier (e.g 'email' or 'username'')}
```

This can also be done from the Console UI by creating a New OIDC Auth Method and filling in the same required parameters.

Notice the **unique-identifier** must be an available claim, which out of the box might be the "**preferred_username**" field.  
If you wish to use a field such as **email** instead, make sure to first **Add optional claim** under **Token configuration** (in the Azure App), and add the **email** claim.

To log in with SSO to Akeyless with your new Azure AD OIDC auth method, login to the Console, browse to Auth Methods, select the newly created OIDC auth method, and hit the "**Generate OIDC Bookmark URL**" - this will provide you with the SSO link.

## Login with OIDC from the CLI

You should configure a new profile with your Access-ID from the previous step and OIDC type (if no profile name is provided the default will be configured):

```shell
akeyless configure --access-id <your access ID >  --access-type oidc --profile 'azure-app'
```

Now, you can run any Akeyless CLI command and be authenticated with the Azure application:

```shell
akeyless list-items --profile azure-app
```