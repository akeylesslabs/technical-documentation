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
slug: auth-with-oidc
---
[OpenID Connect (OIDC)](https://openid.net/connect/) is a simple identity layer on top of the OAuth 2.0 protocol. It allows Clients to verify the identity of the End-User based on the authentication performed by an Authorization Server, as well as to obtain basic profile information about the End-User in an interoperable and REST-like manner.

## Create an OIDC Authentication Method with the CLI

Let's create a new OIDC authentication method using the Akeyless CLI. (You can also do this from the [Akeyless Console](https://docs.akeyless.io/docs/auth-with-oidc#create-an-oidc-authentication-method-in-the-console).)

To create an OIDC authentication method with the CLI, run the following command:

```shell
akeyless auth-method create oidc --name <Auth Method Name> \
--issuer https://Idp-issuer-url \
--client-id <client-id> \
--client-secret <client-secret> \
--unique-identifier <UID (for example, 'email' or 'username')>
```

Where:

* `name`: A unique name for the authentication method. The name can include the path to the virtual folder where you want to create the new authentication method, using slash `/` separators. If the folder does not exist, it will be created together with the authentication method.

* `issuer`: The Identity Provider URL (for more information, check the [Okta](https://docs.akeyless.io/docs/okta-oidc) example).

* `client-id`: The Client ID (application ID).

* `client-secret`: The Client's secret.

* `unique-identifier`: A unique identifier is usually one of the following **keys**: `email`, `username`, or `UPN`. Whenever a user logs in with a token, OIDC Identity Providers issue sub-claims containing details that uniquely identify the user. A sub-claim includes a key holding the unique identifier value you configured and is used to distinguish between different users from within the same organization.

> ℹ️ **Note:**
>
> **Unique Identifier** should be a **key** name, not the value itself.
> For example, `email` should be provided as is, and not the actual email address.

By default, Akeyless treats the comma char `,` as a delimiter for the JWT attributes. If your IdP uses different characters as a delimiter, you can set those using the `delimiters` parameter.

You can find the complete list of parameters for this command in the [CLI Reference - Authentication](https://docs.akeyless.io/docs/cli-ref-auth#create) section.

## Create an OIDC Authentication Method in the Console

1. Log in to the Akeyless Console and go to **Users & Auth Methods > New > OIDC**.

2. Define a **Name** for the authentication method, and specify the **Location** as a path to the virtual folder where you want to create the new authentication method, using slash `/` separators. If the folder does not exist, it will be created together with the authentication method.

3. Define the remaining parameters as follows:

    * **Expiration Date:** Select the access expiration date. This parameter is optional. Leave it empty for access to continue without an expiration date.

    * **Allowed Client IPs:** Enter a comma-separated list of CIDR blocks from which the client can issue calls to the proxy. By "client," we mean cURL, SDK, and so on. This parameter is optional. Leave it empty for unrestricted access.

    * **Allowed Trusted Gateway IPs:** Enter a comma-separated list of CIDR blocks. When specified, the Gateway with the IP from this range will be trusted to forward original client IPs (so that they will be visible in the logs). If empty, the Gateway's IP will be used in the logs.

    * **Audit Log Sub Claims:** Enter a comma-separated list of sub-claims keys to be included in the Audit Logs.

    * **Allowed Client Type:** Select the allowed client type that will be authorized to use this authentication method. For example, `CLI`, `Web UI`, `SDK`, `Mobile`, `Extension`.

    * **Issuer URL:** The Identity Provider URL (for more information, check the [Okta](https://docs.akeyless.io/docs/okta-oidc) example).

    * **Client ID:** The Client ID (application ID).

    * **Client Secret:** Client secret.

    * **Allowed Redirect URIs:** Enter a comma-separated list of Redirect URIs to be validated as part of the authentication flow. If you leave this field empty, it can be insecure. Malicious users could steal access credentials using open redirects.

    * **Unique Identifier:** A unique identifier is usually one of the following **keys**: `email`, `username`, or `UPN`. Whenever a user logs in with a token, OIDC Identity Providers issue sub-claims containing details that uniquely identify the user. A sub-claim includes a key holding the unique identifier value you configured and is used to distinguish between different users from within the same organization.

    > 🚧 Note
    >
    > **Unique Identifier** should be a **key** name, not the value itself.
    > For example, `email` should be provided as is, and not the actual email address.

4. Click **Finish**.

## SCIM Provisioning

With just-in-time (JIT) provisioning, Akeyless only learns about a user when that user signs in. Changes in your identity provider's directory don't reach Akeyless until the user's next login. SCIM 2.0 provisioning closes this gap. When you enable it on an OIDC Authentication Method, your identity provider (for example Okta, Microsoft Entra ID or Ping Identity) pushes user and group changes to Akeyless as they happen.

- **SCIM users** become Akeyless human identities.
- **SCIM groups** become Akeyless Groups, which you can associate with Access Roles.
- **Deactivating** a user in the identity provider (`active: false`) blocks that user's new logins and revokes their active tokens within seconds.
- **Removing a user from a group** revokes that user's active tokens. Their next login gets only the groups they still belong to.

> **Warning:** When SCIM is enabled, only users that the identity provider has provisioned and marked active can sign in through this Authentication Method. Existing users can't sign in until the identity provider's first sync creates them. Logins whose ID token is missing the Unique Identifier attribute are rejected.

### Prerequisites

1. An OIDC Authentication Method with a **Unique Identifier** set, for example `email`. SCIM matches each provisioned user to this claim at login.
2. A dedicated [API Key Authentication Method](https://docs.akeyless.io/docs/auth-with-api-key) to act as the SCIM bearer, for example `/scim/okta-provisioner`. Save its **Access ID** and **Access Key**. The Access Key is shown only once.
3. Recommended: set **Allowed IPs** (`--bound-ips`) on the API Key to your identity provider's published egress IP ranges.
4. For a **private** endpoint: an Akeyless Gateway that your identity provider can reach over HTTPS with a publicly trusted certificate.

### Required Permissions

#### Admin who enables SCIM

| Action                                         | Permission needed                                |
| ---------------------------------------------- | ------------------------------------------------ |
| Enable SCIM or change its settings             | **Update** on the OIDC Authentication Method     |
| Bind an API Key as the SCIM bearer             | **Update** on that API Key Authentication Method |
| View the SCIM status, Base URL and sync counts | **Read** on the OIDC Authentication Method       |

#### SCIM API Key (used by the identity provider)

Create a dedicated Access Role, give it the rules below, and associate it **only** with the SCIM API Key. All rules use the **Auth Method** rule type.

| Path                                                         | Capabilities                       | Why                                                                                                                                                                              |
| ------------------------------------------------------------ | ---------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `/<OIDC auth method name>`, for example `/okta-oidc`         | Read, Create, Update, Delete       | Read, create, update and deactivate users. Each SCIM request type needs the matching permission: GET needs Read, POST needs Create, PUT/PATCH needs Update, DELETE needs Delete. |
| `/scim/<OIDC auth method Access ID>/*`                       | Read, List, Create, Update, Delete | SCIM groups are stored as Akeyless Groups under this path.                                                                                                                       |
| `/<SCIM API Key name>`, for example `/scim/okta-provisioner` | Read                               | Lets the Gateway confirm which OIDC Authentication Method the key is bound to.                                                                                                   |

- **Listing users** works with either `Read` or `List` on the `/<OIDC auth method name>` path.
- **SCIM groups** are stored as Akeyless Groups named `/scim/<OIDC auth method Access ID>/<group name>`, which is why the second rule's path is `/scim/<OIDC auth method Access ID>/*`.

```shell
akeyless create-role --name /scim/okta-scim-role

akeyless set-role-rule --role-name /scim/okta-scim-role --rule-type auth-method-rule \
  --path /okta-oidc \
  --capability read --capability create --capability update --capability delete

akeyless set-role-rule --role-name /scim/okta-scim-role --rule-type auth-method-rule \
  --path "/scim/<OIDC-Access-ID>/*" \
  --capability read --capability list --capability create --capability update --capability delete

akeyless set-role-rule --role-name /scim/okta-scim-role --rule-type auth-method-rule \
  --path /scim/okta-provisioner \
  --capability read

akeyless assoc-role-am --role-name /scim/okta-scim-role --am-name /scim/okta-provisioner
```

> **Note:** Don't give this role any other access. If the role is missing a permission, the identity provider gets `401 Unauthorized`. For requests about a specific user (look up, update or deactivate), a missing permission returns `404 Not Found`, the same as a user that doesn't exist.

### Enable SCIM Provisioning

#### From the Console

1. Go to **Users & Auth Methods**, open your OIDC Authentication Method, and select the **SCIM Provisioning** tab.
2. Turn on **Enable SCIM Provisioning**.
3. Select the **SCIM Endpoint**:
   - **Public**: served by Akeyless.
   - **Private**: served by your own Gateway. Your identity provider must be able to reach it.
4. In **Bearer Credential**, select the SCIM API Key Authentication Method.
5. Copy the **SCIM Base URL**.

#### From the CLI

```shell
akeyless auth-method update oidc \
  --name <OIDC Auth Method Name> \
  --scim-enabled true \
  --scim-bearer-access-id <API Key Access ID> \
  --scim-endpoint private \
  --scim-gateway-url https://<your-gateway-host>
```

| Parameter                 | Description                                                                                                                               |
| ------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------- |
| `--scim-enabled`          | Turns SCIM provisioning on or off for this Authentication Method.                                                                         |
| `--scim-bearer-access-id` | The Access ID of the API Key Authentication Method the identity provider uses. An API Key can be bound to only one Authentication Method. |
| `--scim-endpoint`         | `public` (served by Akeyless) or `private` (served by your own Gateway).                                                                  |
| `--scim-gateway-url`      | The Gateway URL your identity provider calls. Required when `--scim-endpoint` is `private`.                                               |

> **Note:** An API Key can be the SCIM bearer of only one Authentication Method.

> **Note:** While an API Key is bound as the SCIM bearer, it can't be deleted. Turn off SCIM or bind another key first.

### Configure Your Identity Provider

| Setting                     | Value                                                                                                                       |
| --------------------------- | --------------------------------------------------------------------------------------------------------------------------- |
| **SCIM Base URL**           | Copy it from the **SCIM Provisioning** tab or from `get-scim-status`. Format: `https://<host>/scim/v2/<API-Key-Access-ID>/` |
| **Authentication**          | HTTP Header / Bearer token                                                                                                  |
| **Token**                   | The API Key's **Access Key alone**. Don't include the Access ID; it's already in the URL.                                   |
| **Unique identifier field** | `userName`. Its value must match the OIDC Unique Identifier claim, for example the user's email.                            |
| **Supported actions**       | Create users, update user attributes, deactivate users, push groups                                                         |

> **Note:** SCIM groups can be changed only through SCIM. An admin can't edit them in the console or CLI. To control what group members can access, associate the group with an Access Role in the usual way. If SCIM stops managing the groups (for example, you turn off SCIM or remove the bound API Key), the groups stay, and they can then be edited by anyone with the usual permissions on them.

### Identity Provider Notes

- **Microsoft Entra ID:** Entra ID provisions changes in cycles that run about every 40 minutes, so a change can take up to 40 minutes to reach Akeyless. The time of the last cycle is shown on the application's Provisioning page in the Entra admin center. To push a change right away, use Provision on demand, which provisions one user, or one group with up to five members, per request. See [Set Up Microsoft Entra ID as an OIDC Authentication Method](https://docs.akeyless.io/docs/azure-active-directory-oidc).
- **Okta:** Okta pushes changes to Akeyless as they happen (when a user is assigned, updated or deactivated), with no fixed sync interval. See [Set Up Okta as an OIDC Authentication Method](https://docs.akeyless.io/docs/okta-oidc).

### Check the SCIM Status

```shell
akeyless get-scim-status --name <OIDC Auth Method Name>
```

This returns the SCIM Base URL, the connection status, and counts of provisioned identities, groups and deactivated users.

### Rotate the SCIM Credential

Select **Rotate Credential** on the **SCIM Provisioning** tab to generate a new Access Key for the bound API Key. The old key stops working within about 15 seconds. Paste the new Access Key into your identity provider. The SCIM Base URL doesn't change.

### Troubleshooting

| Symptom                                      | Likely cause                                                                                                                                                                                       |
| -------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `401 Unauthorized` (JSON)                    | Wrong Access Key, the API Key's role is missing a permission, the identity provider's IPs aren't in **Allowed IPs**, or the endpoint type (public or private) doesn't match the host being called. |
| `403 Forbidden` (HTML) or `Connection reset` | The request never reached Akeyless. A firewall, WAF, load balancer, or wrong scheme or port is blocking the identity provider.                                                                     |
| Users can't sign in after SCIM is enabled    | They haven't been provisioned yet, or their identity provider `userName` doesn't match the OIDC Unique Identifier.                                                                                 |
| `404 Not Found` for a user that exists       | The SCIM API Key's role is missing Read, Update or Delete on the Authentication Method path.                                                                                                        |
| `429 Too Many Requests`                      | The identity provider exceeded the SCIM rate limits: 20 requests per second per source IP address (bursts up to 100), and 50 requests per second per Authentication Method (bursts up to 200). The identity provider retries automatically. |