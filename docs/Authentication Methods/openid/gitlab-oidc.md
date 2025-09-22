---
title: GitLab - OIDC
excerpt: ''
deprecated: false
hidden: false
metadata:
  title: GitLab - OIDC
  description: ''
  robots: index
next:
  description: ''
---
To use GitLabs as an IdP to authenticate the Akeyless Platform via OIDC, follow the steps below.

## Create an application

1. In your GitLab account, go to **Edit profile > Applications.**

2. For **Redirect URI** set  `https://auth.akeyless.io/oidc/callback`, select the** "openid", “profile”** and **“email“** scope and click **Save application**.

![](https://files.readme.io/0f670ff-image-20210825-084902.png "image-20210825-084902.png")

3. Once the Application has been created, you need to obtain the **Client ID, Client secret**:

![](https://files.readme.io/c2aeb6f-image-20210825-084833.png "image-20210825-084833.png")

4. In order to bind the Gitlab Client ID with your Akeyless account, you need to create an OIDC Authentication Method using either CLI or UI, as described below.

## Create an OIDC Authentication Method from the CLI

```shell Akeyless CLI
akeyless auth-method create oidc --name 'my Gitlab app' --issuer https://gitlab.com --client-id {your-client-id}  --client-secret {your-client-secret} --unique-identifier {your-unique-identifier (e.g 'email' or 'username'')}
```

## Login with OIDC from the CLI

1. You should configure a new profile with your Access-ID from the previous step and OIDC type (if no profile name is provided the default will be configured):

```shell Akeyless CLI
akeyless configure --access-id <your-access-id> --access-type oidc --profile 'gitlab-oidc'
```

2. Now, you can run any Akeyless CLI command and be authenticated with Google:

```shell Akeyless CLI
akeyless list-items --profile gitlab-oidc
```