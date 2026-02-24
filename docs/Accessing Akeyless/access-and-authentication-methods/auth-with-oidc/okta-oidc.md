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
To use Okta as an IdP to authenticate into the Akeyless Platform by way of OIDC, follow the steps below.

## Create an Okta Application

1. In your Okta account, go to **Applications > Add Application > Create App Integration**.

2. For **Sign-in method**, select **OIDC - OpenID Connect** and for Application type, select **Web Application** and select **Next**.

    ![Illustration for: 1. In your Okta account, go to Applications > Add Application > Create App Integration. 2. For Sign-in method, select OIDC - OpenID Connect and for Application…](https://files.readme.io/b6c2478-okta-oidc1.png)

3. On the Settings page:
    a. For the Grant type, check **Authorization Code**.
    b. Set `https://auth.akeyless.io/oidc/callback` into the **Sign-in redirect URIs**.

    ![Illustration for configuring the Settings page with the Grant type and Sign-in redirect URIs.](https://files.readme.io/42962ac-image-20210824-102417.png)

4. Once the OIDC app has been created, you need to obtain the **Client ID**, **Client secret**, and **Okta domain**:

    ![Illustration for: Once the OIDC app has been created, you need to obtain the Client ID, Client secret, and Okta domain.](https://files.readme.io/7af68f3-image-20210824-103109.png)

    > 📘 Adding ״groups״ claim - Okta side
    >
    > In Okta, add a custom "groups" claim under Authorization Server → Claims, using a filter (For example, regex) and bind it to a custom scope.
    > In Okta, add a custom "groups" claim under Authorization Server → Claims, using a filter (for example, regex) and bind it to a custom scope.

5. To bind the Okta application with your Akeyless account, create an OIDC Authentication Method using either CLI or UI, as described below.

## Create an OIDC Authentication Method with the CLI

```shell
akeyless auth-method create oidc --name 'My Okta app' --issuer https://{your-okta-domain}.okta.com --client-id {your-client-id} --client-secret {your-client-secret} --required-scopes groups --unique-identifier {your-unique-identifier (for example, 'email' or 'username')}
```

> **Note (Required Scopes):**
>
> Set the OIDC Auth Method "Required Scopes" to "groups" so it is included in the sub-claims.

## Log in With OIDC From the Akeyless CLI

1. Configure a new profile with your Access ID from the previous step and OIDC type (if no profile name is provided, the default profile will be configured):

    ```shell
    akeyless configure --access-id <your-access-id> --access-type oidc --profile 'okta-app'
    ```

2. Now, you can run any Akeyless CLI command and be authenticated with the Okta application:

    ```shell
    akeyless list-items --profile okta-app
    ```
