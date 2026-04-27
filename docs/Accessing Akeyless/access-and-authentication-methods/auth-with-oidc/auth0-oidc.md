---
title: Auth0 - OIDC
excerpt: ''
deprecated: false
hidden: false
metadata:
  title: Auth0 - OIDC
  description: ''
  robots: index
next:
  description: ''
---
To use Auth0 as an IdP to authenticate the Akeyless Platform by way of OIDC, follow the steps below.

## Create an Auth0 Application

1. In your Auth0 account, go to **Applications > Applications > Create Application**.

2. For **Application Type** choose **Native** and click **Create**.

    ![Screenshot of the Auth0 Console while Creating a New Application](https://files.readme.io/78d1964-image-20210824-110648.png "image-20210824-110648.png")

3. On the Settings tab, under the **Application URIs** section, set `https://auth.akeyless.io/oidc/callback` in **Allowed Callback URLs**.

    ![Screenshot of the Auth0 Console while Configuring Application URIs](https://files.readme.io/3edb775-image-20210824-111105.png "image-20210824-111105.png")

4. Once the OIDC app has been created, you need to obtain the **Client ID, Client Secret,** and **Auth0 domain**:

    ![Screenshot of the Auth0 Console while Retrieving Basic Application Information](https://files.readme.io/4884e36-aut03.png "4884e36-aut03.png")

5. To bind the Auth0 application with your Akeyless account, create an OIDC Authentication Method using either Akeyless CLI or UI, as described below.

## Create an OIDC Authentication Method with the CLI

```shell
akeyless auth-method create oidc --name 'My Auth0 app' --issuer https://{your-auth0-domain}.auth0.com --client-id {your-client-id} --client-secret {your-client-secret} --unique-identifier {your-unique-identifier (for example, 'email' or 'username')}
```

## Log in With OIDC Using the CLI

1. Configure a new profile with your Access ID from the previous step and OIDC type (if no profile name is provided, the default profile will be configured):

    ```shell
    akeyless configure --access-id <your-access-id> --access-type oidc --profile 'auth0-app'
    ```

   For more information about creating and managing CLI profiles, see [CLI Profiles](https://docs.akeyless.io/docs/cli-profiles).

2. Now, you can run any Akeyless CLI command and be authenticated with the Auth0 application:

    ```shell
    akeyless list-items --profile auth0-app
    ```
