---
title: OAuth 2.0/JWT
excerpt: ''
deprecated: false
hidden: false
metadata:
  title: OAuth2.0/JWT
  description: ''
  robots: index
next:
  description: >-
    Make sure to associate your new Authentication Method with an Access Role to
    grant the relevant permissions within Akeyless
---
The **OAuth2.0/JWT** method allows authentication via a configured **OAuth2.0/JWT** provider.

This standard provides secure delegated access. It means that an application can take actions or access resources from a server on behalf of the user, without them having to share their credentials. It does this by allowing the identity provider (IdP) to issue tokens to third-party applications with the user’s approval.

# Create an OAuth2.0/JWT Authentication Method from the CLI

Let's create a new OAuth2.0/JWT authentication method using the Akeyless CLI. (You can do this also from the [Akeyless Console](https://docs.akeyless.io/docs/oauth20jwt#create-an-oauth20jwt-authentication-method-in-the-akeyless-console).)

```shell Akeyless CLI
akeyless auth-method create oauth2 \
--name <Auth Method Name> \
--jwks-uri <https://jwks-uri> \
--unique-identifier email
```

Where:

* `name`: A unique name for the authentication method. The name can include the path to the virtual folder where you want to create the new authentication method, using slash `/` separators. If the folder does not exist, it will be created together with the authentication method.

* `jwks-uri`: The URL to the JSON Web Key Set (`JWKS`) that contains the public keys that should be used to verify any JSON Web Token (`JWT`) issued by the authorization server. Alternatively, you can load the `JWKS` containing the public keys that should be used to verify the `JWT` issued by the authorization server in base64 format using one of the following parameters `jwks-json-data` or `jwks-json-file`. In case your `JWKS` URL is not accessible from the public network you can set your Akeyless Gateway URL for internal authentication endpoint using the `gateway-url` parameter with an option to load a self-signed `certificate` when needed.

* `unique-identifier`: A unique identifier is usually an email, username, or UPN. Whenever a user logs in with a token, `OAuth2.0/JWT` Identity Providers issue sub-claims containing details that uniquely identify the user. A sub-claim includes a key holding the unique identifier value you configured and is used to distinguish between different users from within the same organization.

By default, Akeyless treats the comma char `,` as a delimiter for the JWT attributes, in case your IdP uses different characters as a delimiter, you might set those using the `delimiters` parameter.

You can find the complete list of additional parameters for this command in the [CLI Reference - Authentication](https://docs.akeyless.io/docs/cli-ref-auth#p-stylecolorblueoauth2p) section.

# Create an OAuth2.0/JWT authentication method in the Akeyless Console

1. Log in to the Akeyless Console and go to **Users & Auth Methods > ⊕ New > OAuth2.0/JWT**, and click on **Next →**.

2. Define a **Name** for the authentication method, and specify the **Location** as a path to the virtual folder where you want to create the new authentication method, using slash `/` separators. If the folder does not exist, it will be created together with the authentication method.

3. Define the remaining parameters as follows:

* **Allowed Client IPs:** Enter a comma-separated list of CIDR blocks from which the client can issue calls to the proxy. By "client," we mean CURL, SDK, etc. This parameter is optional. Leave it empty for unrestricted access.

* **Allowed Trusted Gateway IPs:** Enter a comma-separated list of CIDR blocks. When specified, the Gateway with the IP from this range will be trusted to forward original client IPs (so that they will be visible in the logs). If empty, the IP of the Gateway will be used in the logs.

* **Audit Log Sub Claims:** Enter a comma-separated list of sub-claims keys to be included in the audit logs.

* **Allowed Client Type:** Select the allowed client type that will be authorized to use this authentication method. e.g. `CLI`, `SDK`.

* **Expiration Date:** Select the access expiration date. This parameter is optional. Leave it empty for access to continue without an expiration date.

* **Unique Identifier :** A unique identifier is usually an email, username, or UPN. Whenever a user logs in with a token, OAuth2.0/JWT Identity Providers issue sub-claims containing details that uniquely identify the user. A sub-claim includes a key holding the unique identifier value you configured and is used to distinguish between different users from within the same organization.

* **JWKS URL :** Enter the URL to the JSON Web Key Set (`JWKS`) containing the public keys that should be used to verify any JSON Web Token (`JWT`) issued by the authorization server. Alternatively, you can load the `JWKS` containing the public keys that should be used to verify the `JWT` issued by the authorization server using the `JSON` option

* **Issuer URL:** Enter the issuer URL. This parameter is optional.

* **Audience URL:** Enter the audience in the JWT. This parameter is optional.

* **Bound Client IDs:** Enter a list of the Client's IDs for which access is allowed. This parameter maps to the non-standard `cid` (Client Identification Data) sub-claim and is optional. Leave it empty for unrestricted access.

4. Click on **Finish**.
