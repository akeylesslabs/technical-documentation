---
title: SAML
excerpt: Security Assertion Markup Language (SAML)
deprecated: false
hidden: false
metadata:
  title: SAML
  description: ''
  robots: index
next:
  description: >-
    Make sure to associate your new Authentication Method with an Access Role to
    grant the relevant permissions within Akeyless
---
The SAML authentication method allows users to authenticate using external IdP using the SAML standard.

# Create a SAML Authentication Method in the CLI

Let's create a new SAML authentication method using the Akeyless CLI. You can also do this from the [Akeyless Console](https://docs.akeyless.io/docs/saml#create-a-saml-authentication-method-from-the-console).

To create a SAML authentication method from the CLI, run the following command:

```shell Akeyless CLI
akeyless auth-method create saml \
--name saml-am \
--idp-metadata-url your-idp-metadata-url \
--unique-identifier email
```

Where:

* `name`: A unique name for the authentication method. The name can include the path to the virtual folder where you want to create the new authentication method, using slash `/` separators. If the folder does not exist, it will be created together with the authentication method.

* `idp-metadata-url`: The Identity Provider URL (for more information check the [Okta](https://docs.akeyless.io/docs/okta) example).

* `unique-identifier`: A unique identifier is usually one of the following **keys** `email`, `username`, or `UPN`. Whenever a user logs in with a token, SAML Identity Providers issue sub-claims containing details that uniquely identify the user. A sub-claim includes a key holding the unique identifier value you configured and is used to distinguish between different users from within the same organization.

> 🚧 Note
>
> **Unique Identifier** should be a **key** name, i.e. not the value itself. for example, `email` should be provided as is, and not the actual email address.

By default, Akeyless treats the comma char `,` as a delimiter for the JWT attributes. In case your IdP uses different characters as a delimiter, you might set those using the `delimiters` parameter.

You can find the complete list of parameters for this command in the [CLI Reference - Authentication](https://docs.akeyless.io/docs/cli-ref-auth#p-stylecolorbluesamlp) section.

# Create a SAML Authentication Method in the Console

1. Log in to the Akeyless Console and go to **Users & Auth Methods > New > User (SAML)**.

2. Define a **Name** for the authentication method, and specify the **Location** as a path to the virtual folder where you want to create the new authentication method, using slash `/` separators. If the folder does not exist, it will be created together with the authentication method.

3. Define the parameters as follows:

* **Expiration Date:** Select the access expiration date. This parameter is optional. Leave it empty for access to continue without an expiration date.

* **Allowed Client IPs:** Enter a comma-separated list of CIDR blocks from which the client can issue calls to the proxy. By "client," we mean CURL, SDK, etc. This parameter is optional. Leave it empty for unrestricted access.

* **Allowed Trusted Gateway IPs:** Enter a comma-separated list of CIDR blocks. When specified, the Gateway with the IP from this range will be trusted to forward original client IPs (so that they will be visible in the logs). If empty, the Gateway's IP will be used in the logs.

* **Audit Log Sub Claims:** Enter a comma-separated list of sub-claims keys to be included in the audit logs.

4. Click **Next** and define the remaining parameters as follows:

* Choose your preferred Identity Provider (IDP) metadata type by selecting one of the options:
  * Check the **URL** radio button and enter your Identity Provider **Metadata URL** in the field below.
  * Check the **XML** radio button when using an internal domain and enter your Identity Provider **Metadata XML** in the field below.

* **Allowed Redirect URIs:** Enter a comma-separated list of Redirect URIs to be validated as part of the authentication flow. If you leave this field empty, it can be insecure. Malicious users could steal access credentials using open redirects.

* **unique-identifier:** A unique identifier is usually one of the following **keys** `email`, `username`, or `UPN`. Whenever a user logs in with a token, SAML Identity Providers issue sub-claims containing details that uniquely identify the user. A sub-claim includes a key holding the unique identifier value you configured and is used to distinguish between different users from within the same organization.

> 🚧 Note
>
> **Unique Identifier** should be a **key** name, i.e. not the value itself. for example, `email` should be provided as is, and not the actual email address.

4. Click **Finish**.
