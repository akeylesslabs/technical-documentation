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
slug: auth-with-saml
---
SAML authentication lets users sign in to Akeyless through an external Identity Provider (IdP), such as [Okta](https://docs.akeyless.io/docs/saml-auth-okta), [Ping Identity](https://docs.akeyless.io/docs/saml-auth-ping-identity), or [Microsoft Entra ID](https://docs.akeyless.io/docs/saml-auth-azure-ad).

This page explains how to create and use a SAML Authentication Method in Akeyless for browser-based sign-in and single sign-on (SSO) flows.

## Creating a SAML Authentication Method

This action is distinct from creating a new Akeyless account: it creates an additional SAML-based authentication method for an existing account.

### SAML Endpoints

By default, every SAML Authentication Method uses the same shared Akeyless endpoints. Use these values when configuring your IdP application:

| Endpoint | Format |
| --- | --- |
| Entity ID / Identifier | `https://auth.akeyless.io/saml/metadata` |
| Reply URL / ACS URL | `https://auth.akeyless.io/saml/acs` |

**Optional — Dedicated SAML Endpoints:** Some IdPs (for example, Microsoft Entra ID) require each SAML application to use unique Entity ID and ACS URL values, which the shared endpoints above can't satisfy if you plan to configure more than one application against the same Akeyless account. When the **Dedicated SAML Endpoint** flag is enabled on a given Authentication Method, that method exposes its own unique set of endpoints, scoped to its Access ID.

Replace `<SAML_AUTH_METHOD_ACCESS_ID>` with the Access ID of the matching SAML Authentication Method.

| Endpoint | Format |
| --- | --- |
| Entity ID / Identifier | `https://auth.akeyless.io/saml/sp/<SAML_AUTH_METHOD_ACCESS_ID>` |
| Reply URL / ACS URL | `https://auth.akeyless.io/saml/acs/<SAML_AUTH_METHOD_ACCESS_ID>` |
| Akeyless SP Metadata URL | `https://auth.akeyless.io/saml/metadata/<SAML_AUTH_METHOD_ACCESS_ID>` |

See the IdP-specific guides ([Okta](https://docs.akeyless.io/docs/saml-auth-okta), [Ping Identity](https://docs.akeyless.io/docs/saml-auth-ping-identity), [Azure AD](https://docs.akeyless.io/docs/saml-auth-azure-ad)) for setup order and IdP-specific screens when using dedicated endpoints.

### Creating a SAML Authentication Method with the Console

To create a new SAML-based authentication method with the Console:

1. In the Console, under **Administration**, navigate to **Users & Auth Methods**.
2. Select **New**. This opens the authentication method creation wizard.
3. In **Select Type**, select **SAML**, then select **Next →**.
4. Enter a name for the Authentication Method in the **Name** field. Optionally, include a path using `/` separators to place the Authentication Method in a virtual folder, then select **Next →**.
5. Configure general and SAML-specific fields, including **Allowed Redirect URIs**, **Metadata URL** or **Metadata XML**, **Unique Identifier**, and, if this method needs isolated endpoint values, the **Dedicated SAML Endpoint** toggle.
6. Select **Finish**.

> ⚠️ **Warning:**
> The **Unique Identifier** must be a sub-claim key name, not a user value. For example, use `email`, not an actual email address.

### Creating a SAML Authentication Method with the CLI

To create a SAML-based authentication method with the CLI:

```shell
akeyless auth-method create saml \
  --name <SAML Auth Method Name> \
  --idp-metadata-url <IdP Metadata URL> \
  --unique-identifier <email|username|UPN>
```

To create the method by using XML metadata, use:

```shell
akeyless auth-method create saml \
  --name <SAML Auth Method Name> \
  --idp-metadata-xml-file-path <Path to IdP Metadata XML File> \
  --unique-identifier <email|username|UPN>
```

By default, Akeyless treats comma `,` as a delimiter for sub-claim values. If your IdP uses different delimiters, configure them with the `delimiters` flag.

[Read about more parameters available when creating a SAML-based authentication method.](https://docs.akeyless.io/docs/cli-ref-auth#create)

## Using a SAML Authentication Method

### Using a SAML Authentication Method with the Console

To sign in to the Console with SAML:

1. Open the Akeyless Console: [https://console.akeyless.io](https://console.akeyless.io).
2. In the **Or continue with** section, select **SAML**.
3. Enter the SAML Authentication Method **Access ID**, then continue with the IdP sign-in flow.

### Using a SAML Authentication Method with the CLI

To use a SAML-based authentication method with a CLI profile, run the [Akeyless configure command](https://docs.akeyless.io/docs/cli-reference#configure):

```shell
akeyless configure \
  --profile saml \
  --access-id <SAML Access ID> \
  --access-type saml
```

To authenticate and retrieve a temporary Akeyless token, run the [Akeyless auth command](https://docs.akeyless.io/docs/cli-ref-auth#auth):

```shell
akeyless auth \
  --access-type saml \
  --access-id <SAML Access ID>
```

## Associate with Access Roles

After creating the authentication method, associate it with one or more Access Roles so authenticated users can perform actions in Akeyless.

To associate with Access Roles in the Console:

1. In the Console, under **Administration**, navigate to **Users & Auth Methods**.
2. Select the SAML Authentication Method.
3. Open the associated roles section, then add the required Access Roles.
4. Save the changes.

For role configuration details, see [Access Roles](https://docs.akeyless.io/docs/rbac).

## Update an Existing SAML Authentication Method

SAML authentication methods can require updates over time, for example when IdP metadata changes after certificate rotation.

To update in the Console:

1. In the Console, under **Administration**, navigate to **Users & Auth Methods**.
2. Select the SAML Authentication Method to update.
3. Update the relevant fields, such as **Metadata URL**, **Metadata XML**, **Allowed Redirect URIs**, **Unique Identifier**, and the **Dedicated SAML Endpoint** toggle.
4. Save the changes.

To update with the CLI:

```shell
akeyless auth-method update saml \
  --name <Existing SAML Auth Method Name> \
  --idp-metadata-url <Updated IdP Metadata URL> \
  --unique-identifier <email|username|UPN>
```

For all available update flags, see [CLI Reference - Authentication](https://docs.akeyless.io/docs/cli-ref-auth#saml-1).

> ⚠️ **Note:**
> Toggling **Dedicated SAML Endpoint** on an existing Authentication Method changes its Entity ID and ACS URL. Update the IdP application with the new values before or immediately after the change to avoid a sign-in outage for that method.

## Troubleshooting

If SAML sign-in fails, check the following:

- The SAML Authentication Method **Access ID** is correct.
- The IdP configuration uses the correct endpoint values for this specific Authentication Method — the shared endpoints by default, or the dedicated endpoints if **Dedicated SAML Endpoint** is enabled on that method.
- **Metadata URL** or **Metadata XML** is current.
- **Unique Identifier** matches a key that exists in IdP assertions.
- **Allowed Redirect URIs** includes the redirect URI used by the client.

## Optional Features

For optional features that apply across Authentication Methods, see [Common Optional Features](https://docs.akeyless.io/docs/access-and-authentication-methods#common-optional-features).

### SAML-Specific Optional Features

- **Dedicated SAML Endpoint:** Set per Authentication Method (not account-wide) to give this method its own Entity ID, ACS URL, and Metadata URL instead of the shared endpoints. Useful for IdPs that reject reused SAML application values across multiple applications, or when running separate environments (prod/staging/dev) against distinct IdP applications.
- **Allowed Redirect URIs:** Restrict the redirect targets that can be used in the authentication flow.
- **Unique Identifier:** Define which IdP sub-claim key identifies a user.
- **Sub-claim Delimiters:** Configure custom delimiters if your IdP uses a format other than comma-separated values.

## SCIM Provisioning

With just-in-time (JIT) provisioning, Akeyless only learns about a user when that user signs in. Changes in your identity provider's directory don't reach Akeyless until the user's next login. SCIM 2.0 provisioning closes this gap. When you enable it on a SAML Authentication Method, your identity provider (for example Okta, Microsoft Entra ID or Ping Identity) pushes user and group changes to Akeyless as they happen.

- **SCIM users** become Akeyless human identities.
- **SCIM groups** become Akeyless Groups, which you can associate with Access Roles.
- **Deactivating** a user in the identity provider (`active: false`) blocks that user's new logins and revokes their active tokens within seconds.
- **Removing a user from a group** revokes that user's active tokens. Their next login gets only the groups they still belong to.

> **Warning:** When SCIM is enabled, only users that the identity provider has provisioned and marked active can sign in through this Authentication Method. Existing users can't sign in until the identity provider's first sync creates them. Logins whose SAML assertion is missing the Unique Identifier attribute are rejected.

### Prerequisites

1. A SAML Authentication Method with a **Unique Identifier** set, for example `email`. SCIM matches each provisioned user to this attribute at login.
2. A dedicated [API Key Authentication Method](https://docs.akeyless.io/docs/auth-with-api-key) to act as the SCIM bearer, for example `/scim/okta-provisioner`. Save its **Access ID** and **Access Key**. The Access Key is shown only once.
3. For a **private** endpoint: an Akeyless Gateway that your identity provider can reach over HTTPS with a publicly trusted certificate.

### Required Permissions

#### Admin who enables SCIM

| Action                                         | Permission needed                                |
| ---------------------------------------------- | ------------------------------------------------ |
| Enable SCIM or change its settings             | **Update** on the SAML Authentication Method     |
| Bind an API Key as the SCIM bearer             | **Update** on that API Key Authentication Method |
| View the SCIM status, Base URL and sync counts | **Read** on the SAML Authentication Method       |

#### SCIM API Key (used by the identity provider)

Create a dedicated Access Role, give it the rules below, and associate it **only** with the SCIM API Key. All rules use the **Auth Method** rule type.

| Path                                                         | Capabilities                                 | Why                                                                                                                                                                              |
| ------------------------------------------------------------ | -------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `/<SAML auth method name>`, for example `/okta-saml`         | `Read`, `Create`, `Update`, `Delete`         | Read, create, update and deactivate users. Each SCIM request type needs the matching permission: GET needs Read, POST needs Create, PUT/PATCH needs Update, DELETE needs Delete. |
| `/scim/<SAML auth method Access ID>/*`                       | `Read`, `List`, `Create`, `Update`, `Delete` | SCIM groups are stored as Akeyless Groups under this path.                                                                                                                       |
| `/<SCIM API Key name>`, for example `/scim/okta-provisioner` | `Read`                                       | Lets the Gateway confirm which SAML Authentication Method the key is bound to.                                                                                                   |

- **Listing users** works with either `Read` or `List` on the `/<SAML auth method name>` path.
- **SCIM groups** are stored as Akeyless Groups named `/scim/<SAML auth method Access ID>/<group name>`, which is why the second rule's path is `/scim/<SAML auth method Access ID>/*`.

```shell
akeyless create-role --name /scim/okta-scim-role

akeyless set-role-rule --role-name /scim/okta-scim-role --rule-type auth-method-rule \
  --path /okta-saml \
  --capability read --capability create --capability update --capability delete

akeyless set-role-rule --role-name /scim/okta-scim-role --rule-type auth-method-rule \
  --path "/scim/<SAML-Access-ID>/*" \
  --capability read --capability list --capability create --capability update --capability delete

akeyless set-role-rule --role-name /scim/okta-scim-role --rule-type auth-method-rule \
  --path /scim/okta-provisioner \
  --capability read

akeyless assoc-role-am --role-name /scim/okta-scim-role --am-name /scim/okta-provisioner
```

> **Note:** Don't give this role any other access. If the role is missing a permission, the identity provider gets `401 Unauthorized`. For requests about a specific user (look up, update or deactivate), a missing permission returns `404 Not Found`, the same as a user that doesn't exist.

### Enable SCIM Provisioning

#### From the Console

1. Go to **Users & Auth Methods**, open your SAML Authentication Method, and select the **SCIM Provisioning** tab.
2. Turn on **Enable SCIM Provisioning**.
3. Select the **SCIM Endpoint**:
   - **Public**: served by Akeyless.
   - **Private**: served by your own Gateway. Your identity provider must be able to reach it.
4. In **Bearer Credential**, select the SCIM API Key Authentication Method.
5. Copy the **SCIM Base URL**.

#### From the CLI

```shell
akeyless auth-method update saml \
  --name <SAML Auth Method Name> \
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
| **Unique identifier field** | `userName`. Its value must match the SAML Unique Identifier attribute, for example the user's email.                        |
| **Supported actions**       | Create users, update user attributes, deactivate users, push groups                                                         |

> **Note:** SCIM groups can be changed only through SCIM. An admin can't edit them in the console or CLI. To control what group members can access, associate the group with an Access Role in the usual way. If SCIM stops managing the groups (for example, you turn off SCIM or remove the bound API Key), the groups stay, and they can then be edited by anyone with the usual permissions on them.

### Identity Provider Notes

- **Microsoft Entra ID:** Entra ID provisions changes in cycles that run about every 40 minutes, so a change can take up to 40 minutes to reach Akeyless. The time of the last cycle is shown on the application's Provisioning page in the Entra admin center. To push a change right away, use Provision on demand, which provisions one user, or one group with up to five members, per request. See [Set Up Microsoft Entra ID as a SAML Authentication Method](https://docs.akeyless.io/docs/saml-auth-azure-ad).
- **Okta:** Okta pushes changes to Akeyless as they happen (when a user is assigned, updated or deactivated), with no fixed sync interval. See [Set Up Okta as a SAML Authentication Method](https://docs.akeyless.io/docs/saml-auth-okta).

### Check the SCIM Status

```shell
akeyless get-scim-status --name <SAML Auth Method Name>
```

This returns the SCIM Base URL, the connection status, and counts of provisioned identities, groups and deactivated users.

### Rotate the SCIM Credential

Select **Rotate Credential** on the **SCIM Provisioning** tab to generate a new Access Key for the bound API Key. The old key stops working within about 15 seconds. Paste the new Access Key into your identity provider. The SCIM Base URL doesn't change.

### Troubleshooting

| Symptom                                      | Likely cause                                                                                                                                                                                       |
| -------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `401 Unauthorized` (JSON)                    | Wrong Access Key, the API Key's role is missing a permission, the identity provider's IPs aren't in **Allowed IPs**, or the endpoint type (public or private) doesn't match the host being called. |
| `403 Forbidden` (HTML) or `Connection reset` | The request never reached Akeyless. A firewall, WAF, load balancer, or wrong scheme or port is blocking the identity provider.                                                                     |
| Users can't sign in after SCIM is enabled    | They haven't been provisioned yet, or their identity provider `userName` doesn't match the SAML Unique Identifier.                                                                                 |
| `404 Not Found` for a user that exists       | The SCIM API Key's role is missing Read, Update or Delete on the Authentication Method path.                                                                                                        |
| `429 Too Many Requests`                      | The identity provider exceeded the SCIM rate limits: 20 requests per second per source IP address (bursts up to 100), and 50 requests per second per Authentication Method (bursts up to 200). The identity provider retries automatically. |

## Related Pages

For end-to-end IdP setup examples, see:

- [Set Up Okta as a SAML Authentication Method](https://docs.akeyless.io/docs/saml-auth-okta)
- [Set Up Ping Identity as a SAML Authentication Method](https://docs.akeyless.io/docs/saml-auth-ping-identity)
- [Set Up Microsoft Entra ID as a SAML Authentication Method](https://docs.akeyless.io/docs/saml-auth-azure-ad)