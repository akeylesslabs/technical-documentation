---
title: GitHub - OIDC
excerpt: ''
deprecated: false
hidden: false
metadata:
  title: GitHub - OIDC
  description: ''
  robots: index
next:
  description: ''
---
In order to use GitHub as an IdP to authenticate the Akeyless Plaftorm via OIDC, you need to follow the below steps.

## Create an OAuth Apps

1. In your GitHub account, go to **Settings > Developer settings** and press **New OAuth App**.

2. For **Homepage URL** set `https://console.akeyless.io`, for **Authorization callback URL** set `https://auth.akeyless.io/oidc/callback` and click **Register application**.

![](https://files.readme.io/d849e9e-image-20210912-161540.png "image-20210912-161540.png")

3. Once the Application has been created, you need to obtain the **Client ID, Client secret**:

![](https://files.readme.io/bc9cf03-image-20210912-161821.png "image-20210912-161821.png")

4. In order to bind the GitHub Client ID with your Akeyless account, you need to create an OIDC Authentication Method using either CLI or UI, as described below.

## Create an OIDC Authentication Method from the CLI

```shell Akeyless CLI
akeyless auth-method create oidc --name 'my GitHub app' --issuer https://github.com --client-id {your-client-id}  --client-secret {your-client-secret} --unique-identifier {your-unique-identifier (e.g 'email' or 'username'')}
```

The result should look like the following:

```shell
Auth Method my GitHub app successfully created
- Access ID: p-xxxxxxxx
```

## Login with OIDC from the CLI

1. You should configure a new profile with your Access-ID from the previous step and OIDC type (if no profile name is provided the default will be configured):

```shell Akeyless CLI
akeyless configure --access-id p-xxxxxxx --access-type oidc --profile 'github-oidc'
```

2. Now, you can run any Akeyless CLI command and be authenticated with GitHub:

```shell Akeyless CLI
akeyless list-items --profile github-oidc
```
