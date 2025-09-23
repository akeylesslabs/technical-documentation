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
Akeyless is an OpenID Connect (OIDC) identity provider enabling client applications full support of the OIDC protocol to leverage all Akeyless supported [Authentication Methods](doc:access-and-authentication-methods) as a source of identity when authenticating end-users. Client applications can configure their authentication logic to talk to Akeyless. Once enabled, Akeyless will act as the bridge to other identity providers via its existing Authentication Methods.

# Creating an OIDC App from the CLI

To create an OIDC Application from the CLI, run the following command:

```shell Shell
akeyless create-oidc-app \
--name <New OIDC App Name> \
--redirect-uris '<Comma Separated List of Allowed Redirect URIs>' \
--scopes '<Comma Separated List of Granted Scopes/Claims>' \
--audience '<Comma Separated List of Allowed Audiences>' \
--access-permission-assignment '[{"access_id":"<Akeyless Access ID>", "sub_claims":{"email":["user@example.com"]}}]'
```

Where:

* `name`: A unique name for the OIDC App. The name can include the path to the virtual folder where you want to create the new app, using slash `/` separators. If the folder does not exist, it will be created together with the OIDC app.
* `access-permission-assignment`: A JSON string defining which Akeyless Authentication Methods are allowed to use this OIDC App. This is set using the `access_id` and `sub_claims` for that Authentication Method. In addition, you can use an Akeyless [Groups](doc:groups) using `group_id` and `sub-claims`.
* `permission-assignment-file`: Instead of a string, users can add this flag in order to pass a JSON file, using the same formatting, with a path to the file. Groups are allowed.
* `redirect-uris`  (Optional): A list of URIs that the user will be directed back to after authenticating and consenting at the OIDC App.
* `scopes` (Optional): A list of scopes that third-party applications are allowed to request. These scopes (excluding special scopes) will be copied from the `sub-claims` in Akeyless to the OIDC Token. Scopes can include Groups as well.
* `audience`  (Optional) : A list of audiences that third-party applications are allowed to request. This will only affect the `access token` (the `audience` for the `id token` is always the `client id` ).

## Client Type

OAuth defines two client types, based on their ability to authenticate securely with the authorization server (i.e., the ability to maintain the confidentiality of their client credentials):

* **Confidential** Clients capable of maintaining the confidentiality of their credentials (e.g., client implemented on a secure server with restricted access to the client credentials), or capable of secure client authentication using other means. By default, an Akeyless OIDC App will be created for this client type.
* **Public** Clients are incapable of maintaining the confidentiality of their credentials (e.g., clients executing on the device used by the resource owner, such as an installed native application or a web browser-based application), and incapable of secure client authentication via any other means. To create an Akeyless OIDC App for **Public** client type use the `public` flag as part of the creation command. 

> 👍 Note
>
> **Special Scopes**\
> You can also set a scope of `offline_access` which will generate a `refresh token`.

Once created, you will see output similar to this:

```shell Shell
{
  "name": "My OIDC App",
  "client_id": "c-rchjo3266adeoufb1hj3",
  "client_secret": "1dd4ec958947ff5f85374b011e173e8a6d292cacd4fbb9466ffdf5da260728c3"
}
```

You will need this information for the next step in the process.

# Authenticating with Akeyless

Once you have created your OIDC App, you will need to authenticate agianst Akeyless using an Authentication Method  that was set as part of the  `access-permission-assignment`. 

For example, if you assigned an [AWS IAM](doc:aws-iam) Authentication Method, authenticate to Akeyless using the `auth` command:

```shell Shell
akeyless auth --access-type=aws_iam --access-id <Access ID>
```

This will return a `token`:

```shell
Authentication succeeded.
Token: t-84e46b1ef69c617d0cd4b15aaeba10da
```

You will need this token for the next step as well.

## Make a POST Request to Token Endpoint

Once authorized, make a `POST` request to the `Token Endpoint` in order to get back your OIDC Token.  The parameters should be `url encoded`.

> 📘 Info
>
> **Issuer URL, Token and well-known Endpoints**
>
> Your `Issuer URL` is always `https://auth.akeyless.io/oidc/provider/<AkeylessAccountId>`. 
>
> The `Token endpoint` is `https://auth.akeyless.io/oidc/provider/<AkeylessAccountId>/oauth2/token`.
>
> The `well-known endpoint` is  `https://auth.akeyless.io/oidc/provider/<AkeylessAccountId>/.well-known/openid-configuration`

```shell Shell
curl --location 'https://auth.akeyless.io/oidc/provider/<your-account-id>/oauth2/token' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'client_id=c-rchjo3266adeoufb1hj3' \
--data-urlencode 'client_secret=1dd4ec958947ff5f85374b011e173e8a6d292cacd4fbb9466ffdf5da260728c3' \
--data-urlencode 'assertion=t-84e46b1ef69c617d0cd4b15aaeba10da' \
--data-urlencode 'grant_type=urn:ietf:params:oauth:grant-type:token-exchange' \
--data-urlencode 'scope=openid email' #example scopes
```

Where:

`location`: Your full `Token Endpoint`.

`client_id`, `client_secret`: The output you received when creating the OIDC App earlier.

`assertion`: The `token` you received when running `akeyless auth`.

`grant_type`: This should always be `urn:ietf:params:oauth:grant-type:token-exchange` to indicate a token exchange between an Akeyelss `token` and `OIDC token`.

Optional:

`scopes`, `audience`: A list of requested scopes and/or audiences (space separated) for this request. In a machine-to-machine use case, all scopes and audiences are automatically granted to the request, where scopes can include Akeyless [Groups](doc:groups) as well.

After running this **POST** request, you will receive an OIDC token back:

```shell Shell
{
    "access_token": "eyJhbGciOiJSUzI1NiIsImtpZCI6ImstNHVqMWl0OHdrOGQwIiwidHlwIjoiSldUIn0.eyJDbGllbnRVbmlxdWVJZCI6InAtenJzMzdpeTBuZWh6IiwiYXVkIjpbXSwiZXhwIjoxNjg3OTUzMDc1LCJleHQiOnsiQ2xpZW50VW5pcXVlSWQiOiJwLXpyczM3aXkwbmVoeiJ9LCJpYXQiOjE2ODc5NDk0NzUsImlzcyI6Imh0dHBzOi8vYzkwNS04OS0xMzgtMTY2LTE5My5uZ3Jvay5pby9vaWRjL3Byb3ZpZGVyL2FjYy1nZDk1Y284MmdpMTQiLCJqdGkiOiJkZDJlMjRkNS03MzVhLTRlYzktYjNjNS1mMTRjZTI2OGFiNzMiLCJuYmYiOjE2ODc5NDk0NzUsInNjcCI6WyJvcGVuaWQiLCJDbGllbnRVbmlxdWVJZCJdLCJzdWIiOiJwLXpyczM3aXkwbmVoei9wLXpyczM3aXkwbmVoeiJ9.RxrvPdIShJB4jr75dg-QGvMy6z8GXC3Hf1_zRNFSTj6eMgBANF8hXWJ5JLCD1jK410lRjYgFMpZ0TrzsHqSUt7Q3I8D_805JqbJ0QYSnPRlFlJUGuwK0uvSdBjR_4U5sWPjNL_qDbVlNMAueWbkTkp83ciqBP4SYH0gpevp0JmfDCw8750u7DYM_QU2g4MbGeqBuvrJo7QJI_2tYdU8HiU7n25SRvF5ilRZTlePvUmhXCIgW6UP-jjtyfFKveBnyTdF_698kVQDD2NwvrufchnYH6qCRMJ7OA8n2m1G4nO3Qrz7TqSzkT-_tgB8udat4kqbc5ftNSiBE2JF7RQSiG_vt1Jkf7fEs0svtni6n_nGfyKUH6OsQFIJOH_jc6Gp2_3p-vlxIaxLZ2f1g-Wb8vUAliyJuisP3W-uzxUGFMIU_xv8-FqOXjpXHSa92EBsdMXFUPy-S6o57GmdLdvKlIiAr9KDSTTmyiUHi5wFnsFJ0seh3I9QTBhe6vywKFkBs1jL38hqT_gXopkxvgV1MQvX1H09C12sGVNfLElqU8GAfmALHaXWv0azsWNcQUGhmKPbTe89VzRCpmf0dgG0QmFEu68ogyD5WBBwENejJnqGUeejfH13uui6yXYssnIPRJuzQGqKOWSnLvVFSGomOl7JXt-IekTykW4uA2ylPahc",
    "expires_in": 3599,
    "id_token": "eyJhbGciOiJSUzI1NiIsImtpZCI6ImstNHVqMWl0OHdrOGQwIiwidHlwIjoiSldUIn0.eyJDbGllbnRVbmlxdWVJZCI6InAtenJzMzdpeTBuZWh6IiwiYXVkIjpbIm9pZGMtY2xpZW50Z2tjNzN1MmJ3dTF3NGI4ajEwOGgiXSwiYXV0aF90aW1lIjoxNjg3OTQ5NDc1LCJleHAiOjE2ODc5NTMwNzUsImlhdCI6MTY4Nzk0OTQ3NSwiaXNzIjoiaHR0cHM6Ly9jOTA1LTg5LTEzOC0xNjYtMTkzLm5ncm9rLmlvL29pZGMvcHJvdmlkZXIvYWNjLWdkOTVjbzgyZ2kxNCIsImp0aSI6IjAzY2FlZWVmLTdkODAtNDdkOC04NjNmLWIxZDhlYjVhMDI2MSIsInN1YiI6InAtenJzMzdpeTBuZWh6L3AtenJzMzdpeTBuZWh6In0.FoNRBvn4jcCl0mwq5D3symqPSjEJuTPgBoaQuUIIq2PZTDtHyZ1oCNEOtQk1v_426-5OCs0K2eep1obba8RJ9N5SXi4iva1kdXikxUMER-ONmUvMzwQlevw8CXSvtVb-HZ8ok26b0frB4MaiVZUc7ICKodOXLKTfWALTIozLZsha1hs7EmkKWl0zniqzkYtegg5LKANt3BUabdSNjTS6vcpJIETHvbyHYKs9nn7YwB_Ptt-7sDQUJfwz-1Mlr-C79xwCTLdLaJTxS4zTkDMM2unJ9OD945SDFYDdCj9BeqcYyoRdKpzYHToIGcGE0z_DTia42UPlhyVIGj4lvsLqTFIhEb1mU4k_q6-42UZ6SSKOPmzXjlF2GrlUIiNN48b8HocLUQl3N0h6TiQSa_G2GFLXoHpCv_Ca6PXRs9nfR7XzyuQ1P7i8IgQYqsWYUJopO_ypZM2XOElZ41gSWGnANzdElirLoLdPKJQyHEV7AuKTzQrdUEbndKZEDrHqz-Al5r10uRdVclo90cOByQOB8yTvrLCfIrate5VnMg-bgDjzNqlladxCO8YeD-B5nCEPRUAfQRV3Quadm0Jx4lm28UkUD0iNdPEcZm7eYafvqcvkekLoVbWgb6Ua7YtLIeTf4i8Uh0GzdM7mphPYjXiszO_spvJQQBLOzEGm7obGmss",
    "scope": "openid email",
    "token_type": "bearer"
}
```

You can now use that OIDC  `access_token` to authenticate with another resource or application.

# Updating an OIDC App from the CLI

Use the following command to update an OIDC App:

```shell
akeyless update-oidc-app \
--name <OIDC App Name> \
--redirect-uris '<Comma Separated List of Allowed Redirect URIs>' \
--scopes '<Comma Separated List of Granted Scopes/Claims>' \
--audience '<Comma Separated List of Allowed Audiences>' \
--access-permission-assignment '[{"access_id":"<Akeyless Access ID>", "sub_claims":{"email":["user@example.com"]}}]'
```

> 🚧 Warning
>
> **Overriding Information**\
> If you want to add to Redirects, Scopes, Audiences, or Access Permissions, ensure you have the original ones in the string or file as well so you don't override them.

To update the name of an OIDC App, use the following command:

```shell
akeyless update-item --name <OIDC App Name> --new-name <OIDC App New Name>
```
