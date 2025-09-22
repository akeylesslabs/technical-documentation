---
title: Okta SAML Authentication
excerpt: ''
deprecated: false
hidden: false
metadata:
  title: Okta SAML Authentication
  description: ''
  robots: index
next:
  description: ''
---
To use Okta as an IdP to authenticate to the Akeyless Platform, follow the steps below.

# Create an Okta application

The following configuration will enable users to authenticate using Okta SAML-based Single Sign-On.

1. Go to **Applications** in the left sidebar. Create a new app integration type **SAML 2.0 ** in your Okta account. 

![](https://files.readme.io/a915ffc-1.png "1.png")

Provide an **App name**:

![](https://files.readme.io/a4e4ada-1.2.png "1.2.png")

2. On the **SAML Settings** page:

- Set `https://auth.akeyless.io/saml/acs` into the Single sign-on URL field.
  - Set `https://auth.akeyless.io/saml/metadata` into the Audience URI (SP Entity ID) field.

![](https://files.readme.io/d58189c-3.png "3.png")

- In the **Attribute Statements** section, add the following attributes:
  - `Name`: `email` ->`Value`: `user.email`
  - `Name`: `user` -> `Value`: `user.login`
- In the  **Group Attributes Statements** section, add the following attributes:
  - `Name`: `groups`  
  - `Filter`: `Matches regex`-> `Value`: `.*`

![](https://files.readme.io/86d982d-4.png "4.png")

3. On the Feedback page,  click **Finish**.

![](https://files.readme.io/7e3cf7f-5.png "5.png")

4. You can either obtain your IdP Metadata URL by clicking on the **Actions** menu of the Active **SAML Signing Certificate** and copy the URL from the **View IDP Metadata** button.  
   Alternatively, you can obtain the IdP metadata`XML`, by clicking on **View SAML setup instructions**, and in the new tab that opens, scroll down and copy the full IdP metadata`XML`  under the **Optional** section.

![](https://files.readme.io/057d8cf-6.png "6.png")

5. Now, when an Okta Application is ready, assign users to the Okta app, just like with any other Okta app. 

6. To bind the Okta application with your Akeyless account, you need to create a [SAML](doc:saml) Authentication Method using either CLI or UI, as described below. 

# Create SAML Authentication Method

To create a SAML Auth method using the Akeyless CLI run the following command:

```shell
akeyless auth-method create saml \
--name 'my Okta app' \
--idp-metadata-url '<your-idp-metadata-url>' \
--unique-identifier email
```

Alternatively, you can create this Auth method from the Akeyless console.

1. Go to the **Users & Auth Methods** tab in your console.

2. Select **New > SAML**.

3. Fill in the mandatory parameters:

- Name: The in-system name for the authentication method.
- IDP Metadata URL: The  **App Federation Metadata URL** you copied from the Azure process.
- Unique identifier: The required identifier. In this case, you can use **email**.

# Authenticate using SAML

To log in using SAML from Akeyless CLI: 

1. You should configure a new profile with your Access-ID from the previous step and SAML type (if no profile name is provided, the default will be configured):

```shell
akeyless configure --access-id <Access ID> --access-type saml --profile 'okta-app'
```

2. Now, you can run any Akeyless CLI command and be authenticated with the Okta application:

```shell
akeyless list-items --profile okta-app
```

In the Akeyless Console login page, click on the SAML option and enter your SAML Access ID. You will be redirected to the Okta sign-in where you need to provide your Okta credentials.