---
title: OIDC
excerpt: OpenID Connect
deprecated: false
hidden: false
metadata:
  title: OIDC
  description: ''
  robots: index
next:
  description: >-
    Make sure to associate your new Authentication Method with an Access Role to
    grant the relevant permissions within Akeyless
---
[OpenID Connect (OIDC)](https://openid.net/connect/) is a simple identity layer on top of the OAuth 2.0 protocol. It allows Clients to verify the identity of the End-User based on the authentication performed by an Authorization Server, as well as to obtain basic profile information about the End-User in an interoperable and REST-like manner.

# Create an OIDC Authentication Method in the CLI

Let's create a new OIDC authentication method using the Akeyless CLI. (You can do this also from the [Akeyless Console](https://docs.akeyless.io/docs/openid#create-oidc-authentication-method-in-the-akeyless-console).)

To create an OIDC authentication method from the CLI, run the following command:

```shell Akeyless CLI
akeyless auth-method create oidc --name <Auth Method Name> \
--issuer <https://Idp-issuer-url> \
--client-id <client-id> \
--client-secret <client-secret> \
--unique-identifier <UID (e.g 'email' or 'username')>
```

Where:

* `name`: A unique name for the authentication method. The name can include the path to the virtual folder where you want to create the new authentication method, using slash `/` separators. If the folder does not exist, it will be created together with the authentication method.

* `issuer`: The Identity Provider URL (for more information check the [Okta](https://docs.akeyless.io/docs/okta) example).

* `client-id`: The Client ID (application ID).

* `client-secret`: The Client's secret.

* `unique-identifier`: A unique identifier is usually one of the following **keys**: `email`, `username`, or `UPN`. Whenever a user logs in with a token, OIDC Identity Providers issue sub-claims containing details that uniquely identify the user. A sub-claim includes a key holding the unique identifier value you configured and is used to distinguish between different users from within the same organization.

> 🚧 Note
>
> **Unique Identifier** should be a **key** name, i.e. not the value itself.
> For example, `email` should be provided as is, and not the actual email address.

By default, Akeyless treats the comma char `,` as a delimiter for the JWT attributes, in case your IdP uses different characters as a delimiter, you might set those using the `delimiters` parameter.

You can find the complete list of parameters for this command in the [CLI Reference - Authentication](https://docs.akeyless.io/docs/cli-ref-auth#p-stylecolorblueoidcp) section.

# Create an OIDC authentication method in the Console

1. Log in to the Akeyless Console and go to **Users & Auth Methods > New > OIDC**.

2. Define a **Name** for the authentication method, and specify the **Location** as a path to the virtual folder where you want to create the new authentication method, using slash `/` separators. If the folder does not exist, it will be created together with the authentication method.

3. Define the remaining parameters as follows:

* **Expiration Date:** Select the access expiration date. This parameter is optional. Leave it empty for access to continue without an expiration date.

* **Allowed Client IPs:** Enter a comma-separated list of CIDR blocks from which the client can issue calls to the proxy. By "client," we mean CURL, SDK, etc. This parameter is optional. Leave it empty for unrestricted access.

* **Allowed Trusted Gateway IPs:** Enter a comma-separated list of CIDR blocks. When specified, the Gateway with the IP from this range will be trusted to forward original client IPs (so that they will be visible in the logs). If empty, the Gateway's IP will be used in the logs.

* **Audit Log Sub Claims:** Enter a comma-separated list of sub-claims keys to be included in the audit logs.

* **Issuer URL:** The Identity Provider URL (for more information, check the [Okta](https://docs.akeyless.io/docs/okta) example).

* **Client ID:** The Client ID (application ID).

* **Client Secret:** Client secret.

* **Allowed Redirect URIs:** Enter a comma-separated list of Redirect URIs to be validated as part of the authentication flow. If you leave this field empty, it can be insecure. Malicious users could steal access credentials using open redirects.

* **Unique Identifier:** A unique identifier is usually one of the following **keys**: `email`, `username`, or `UPN`. Whenever a user logs in with a token, SAML Identity Providers issue sub-claims containing details that uniquely identify the user. A sub-claim includes a key holding the unique identifier value you configured and is used to distinguish between different users from within the same organization.

> 🚧 Note
>
> **Unique Identifier** should be a **key** name, i.e. not the value itself.
> For example, `email` should be provided as is, and not the actual email address.

4. Click **Finish**.
