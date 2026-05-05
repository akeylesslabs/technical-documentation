---
title: OIDC Identity Provider
excerpt: ''
deprecated: false
hidden: false
metadata:
  title: ''
  description: ''
  robots: index
next:
  description: ''
---
Akeyless is an OpenID Connect (OIDC) identity provider enabling client applications full support of the OIDC protocol to leverage all Akeyless supported [Authentication Methods](https://docs.akeyless.io/docs/access-and-authentication-methods) as a source of identity when authenticating end-users. Client applications can configure their authentication logic to talk to Akeyless. Once enabled, Akeyless will act as the bridge to other identity providers by way of its existing Authentication Methods.

## Creating an OIDC App with the CLI

To create an OIDC Application with the CLI, run the following command:

```shell
akeyless create-oidc-app \
--name <New OIDC App Name> \
--redirect-uris '<comma-separated list of allowed redirect URIs>' \
--scopes '<comma-separated list of granted scopes/claims>' \
--audience '<comma-separated list of allowed audiences>' \
--access-permission-assignment '[{"access_id":"<Akeyless Access ID>", "sub_claims":{"email":["user@example.com"]}}]'
```

Where:

* `name`: A unique name for the OIDC App. The name can include the path to the virtual folder where you want to create the new app, using slash `/` separators. If the folder does not exist, it will be created together with the OIDC app.
* `access-permission-assignment`: A JSON string defining which Akeyless Authentication Methods are allowed to use this OIDC App. This is set using the `access_id` and `sub_claims` for that Authentication Method. In addition, you can use an Akeyless [Groups](https://docs.akeyless.io/docs/groups) using `group_id` and `sub-claims`.
* `permission-assignment-file`: Instead of a string, users can add this flag to pass a JSON file, using the same formatting, with a path to the file. Groups are allowed.
* `redirect-uris` (Optional): A list of URIs that the user will be directed back to after authenticating and consenting at the OIDC App.
* `scopes` (Optional): A list of scopes that third-party applications are allowed to request. These scopes (excluding special scopes) will be copied from the `sub-claims` in Akeyless to the OIDC Token. Scopes can include Groups as well.
* `audience` (Optional): A list of audiences that third-party applications are allowed to request. This will only affect the `access token` (the `audience` for the `id token` is always the `client id` ).

### Client Type

OAuth defines two client types, based on their ability to authenticate securely with the authorization server (in other words, the ability to maintain the confidentiality of their client credentials):

* **Confidential** Clients capable of maintaining the confidentiality of their credentials (For example, client implemented on a secure server with restricted access to the client credentials), or capable of secure client authentication using other means. By default, an Akeyless OIDC App will be created for this client type.
* **Public** Clients are incapable of maintaining the confidentiality of their credentials (For example, clients executing on the device used by the resource owner, such as an installed native application or a web browser-based application), and incapable of secure client authentication by way of any other means. To create an Akeyless OIDC App for **Public** client type use the `public` flag as part of the creation command.

> ℹ️ **Note (Special Scopes):**
> You can also set a scope of `offline_access` which will generate a `refresh token`.

Once created, you will see output similar to this:

```shell
{
  "name": "My OIDC App",
  "client_id": "<OIDC_CLIENT_ID>",
  "client_secret": "<OIDC_CLIENT_SECRET>"
}
```

You will need this information for the next step in the process.

## Authenticating With Akeyless

Once you have created your OIDC App, you will need to authenticate against Akeyless using an Authentication Method that was set as part of the `access-permission-assignment`.

For example, if you assigned an [AWS IAM](https://docs.akeyless.io/docs/auth-with-aws) Authentication Method, authenticate to Akeyless using the `auth` command:

<!-- secret-stdout-scan:ok -->
```shell
akeyless auth --access-type=aws_iam --access-id <Access ID>
```

This will return a `token`:

```shell
Authentication succeeded.
Token: <AKEYLESS_ACCESS_TOKEN>
```

You will need this token for the next step as well.

### Make a POST Request to Token Endpoint

Once authorized, make a `POST` request to the `Token Endpoint` to get your OIDC Token. The parameters should be URL encoded.

> ℹ️ **Info (Issuer URL, Token and well-known Endpoints):**
>
> Your `Issuer URL` is always `https://auth.akeyless.io/oidc/provider/<AkeylessAccountId>`.
>
> The `Token endpoint` is `https://auth.akeyless.io/oidc/provider/<AkeylessAccountId>/oauth2/token`.
>
> The `well-known endpoint` is `https://auth.akeyless.io/oidc/provider/<AkeylessAccountId>/.well-known/openid-configuration`

```shell
curl --location 'https://auth.akeyless.io/oidc/provider/<your-account-id>/oauth2/token' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'client_id=<OIDC_CLIENT_ID>' \
--data-urlencode 'client_secret=<OIDC_CLIENT_SECRET>' \
--data-urlencode 'assertion=<AKEYLESS_ACCESS_TOKEN>' \
--data-urlencode 'grant_type=urn:ietf:params:oauth:grant-type:token-exchange' \
--data-urlencode 'scope=openid email' #example scopes
```

Where:

`location`: Your full `Token Endpoint`.

`client_id`, `client_secret`: The output you received when creating the OIDC App earlier.

`assertion`: The `token` you received when running `akeyless auth`.

`grant_type`: This should always be `urn:ietf:params:oauth:grant-type:token-exchange` to indicate a token exchange between an Akeyless `token` and `OIDC token`.

Optional:

`scopes`, `audience`: A list of requested scopes and/or audiences (space separated) for this request. In a machine-to-machine use case, all scopes and audiences are automatically granted to the request, where scopes can include Akeyless [Groups](https://docs.akeyless.io/docs/groups) as well.

After running this **POST** request, you will receive an OIDC token back:

```shell
{
  "access_token": "<OIDC_ACCESS_TOKEN_JWT>",
    "expires_in": 3599,
  "id_token": "<OIDC_ID_TOKEN_JWT>",
    "scope": "openid email",
    "token_type": "bearer"
}
```

You can now use that OIDC `access_token` to authenticate with another resource or application.

## Updating an OIDC App with the CLI

Use the following command to update an OIDC App:

```shell
akeyless update-oidc-app \
--name <OIDC App Name> \
--redirect-uris '<comma-separated list of allowed redirect URIs>' \
--scopes '<comma-separated list of granted scopes/claims>' \
--audience '<comma-separated list of allowed audiences>' \
--access-permission-assignment '[{"access_id":"<Akeyless Access ID>", "sub_claims":{"email":["user@example.com"]}}]'
```

> ⚠️ **Warning (Overriding Information):**
> If you want to add to Redirects, Scopes, Audiences, or Access Permissions, ensure you have the original ones in the string or file as well so you don't override them.

To update the name of an OIDC App, use the following command:

```shell
akeyless update-item --name <OIDC App Name> --new-name <OIDC App New Name>
```
