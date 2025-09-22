---
title: Okta - OIDC
excerpt: ''
deprecated: false
hidden: false
metadata:
  title: Okta- OIDC
  description: ''
  robots: index
next:
  description: ''
---
To use Okta as an IdP to authenticate into the Akeyless Platform via OIDC, follow the steps below.

## Create an Okta application

1. In your Okta account, go to** Applications > Add Application > Create App Integration**.

2. For **Sign-in method** select **OIDC - OpenID Connect** and for Application type  
   select **Web Application** and press **Next**.

![](https://files.readme.io/b6c2478-okta-oidc1.png "okta-oidc1.png")

3. On the Settings page:  
   a. For the Grant type, check **Authorization Code**.  
   b. Set `https://auth.akeyless.io/oidc/callback` into the **Sign-in redirect URIs**.

![](https://files.readme.io/42962ac-image-20210824-102417.png "image-20210824-102417.png")

4. Once the OIDC app has been created, you need to obtain the **Client ID, Client secret,** and  **Okta domain**: 

![](https://files.readme.io/7af68f3-image-20210824-103109.png "image-20210824-103109.png")

> 📘 Adding ״groups״ claim - Okta side
> 
> In Okta, add a custom "groups" claim under Authorization Server → Claims, using a filter (e.g. regex) and bind it to a custom scope.

5. In order to bind the Okta application with your Akeyless account, you need to create an OIDC Authentication Method using either CLI or UI, as described below.

## Create an OIDC Authentication Method from the CLI

```shell Akeyless CLI
akeyless auth-method create oidc --name 'My Okta app' --issuer https://{your-okta-domain}.okta.com --client-id {your-client-id}  --client-secret {your-client-secret} --required-scopes groups --unique-identifier {your-unique-identifier (e.g 'email' or 'username')}
```

> 📘 Required Scopes
> 
> Set the OIDC Auth Method "Required Scopes" to "groups" to be included it in the sub claims.

## Login with OIDC from Akeyless CLI

1. You should configure a new profile with your Access ID from the previous step and OIDC type (In case the profile name is not provided the default profile will be configured):

```shell Akeyless CLI
akeyless configure --access-id <your-access-id> --access-type oidc --profile 'okta-app'
```

2. Now, you can run any Akeyless CLI command and be authenticated with the Okta application:

```shell Akeyless CLI
akeyless list-items --profile okta-app
```