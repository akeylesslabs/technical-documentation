---
title: Google - OIDC
excerpt: ''
deprecated: false
hidden: false
metadata:
  title: Google - OIDC
  description: ''
  robots: index
next:
  description: ''
---
To use Google as an IdP to authenticate the Akeyless Platform by way of OIDC, follow the steps below.

> **Critical:**
>
> Ensure your OAuth consent configuration **includes only authorized domains** of your organization, and that the User type is set to **Internal** only.

To set your OAuth consent screen with **User type** internal, click on your OAuth consent settings and ensure the following are set for User type:

![Illustration for: > Ensure your OAuth consent configuration includes only authorized domains of your organization, and that the User type is set to Internal only. To set your OAuth…](https://files.readme.io/1e3e783-.png)

And for Authorized domains:

![Illustration for: To set your OAuth consent screen with User type internal, click on your OAuth consent settings and ensure the following are set for Authorized domains.](https://files.readme.io/ac48b2f-authdomain.png)

## Create an OAuth Client ID

1. Visit the [Google API Console](https://accounts.google.com/signin/v2/identifier?service=cloudconsole\&passive=1209600\&osid=1\&continue=https%3A%2F%2Fconsole.developers.google.com%2F\&followup=https%3A%2F%2Fconsole.developers.google.com%2F\&flowName=GlifWebSignIn\&flowEntry=ServiceLogin).

2. Go to **Credentials > Create Credentials > OAuth Client ID**.

3. For the **Application Type** select **Web Application**, for the **Authorized redirect URIs** set `https://auth.akeyless.io/oidc/callback` and click **Create**.

    ![Illustration for setting the Application Type to Web Application and setting the Authorized redirect URIs.](https://files.readme.io/14f1ca6-image-20210825-071403_copy.png)

4. Once the OAuth Client ID has been created, you need to obtain the **Client ID** and **Client secret**:

    ![Illustration for: Once the OAuth Client ID has been created, you need to obtain the Client ID and Client secret:](https://files.readme.io/001e838-image-20210825-071706.png)

5. To bind the OAuth Client ID with your Akeyless Platform account, create an OIDC Authentication Method using either CLI or UI, as described below.

## Create an OIDC Authentication Method with the CLI

```shell
akeyless auth-method create oidc --name 'Google-OIDC' --issuer https://accounts.google.com --client-id {your-client-id} --client-secret {your-client-secret} --unique-identifier {your-unique-identifier (for example, 'email' or 'username')}
```

## Log in With OIDC Using the CLI

1. Configure a new profile with your Access ID from the previous step and OIDC type (if no profile name is provided, the default will be configured):

    ```shell
    akeyless configure --access-id <your-access-id> --access-type oidc --profile 'google-oidc'
    ```

2. Now, you can run any Akeyless CLI command and be authenticated with Google:

    ```shell
    akeyless list-items --profile google-oidc
    ```
