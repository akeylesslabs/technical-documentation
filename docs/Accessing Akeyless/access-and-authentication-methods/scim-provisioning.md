---
title: SCIM Provisioning
excerpt: System for Cross-domain Identity Management (SCIM)
deprecated: false
hidden: false
metadata:
  title: SCIM Provisioning
  description: ''
  robots: index
---
With just-in-time (JIT) provisioning, Akeyless only learns about a user when that user signs in. Changes in your identity provider's directory don't reach Akeyless until the user's next login. SCIM 2.0 provisioning closes this gap. SCIM is enabled per [SAML](https://docs.akeyless.io/docs/auth-with-saml) or [OIDC](https://docs.akeyless.io/docs/auth-with-oidc) Authentication Method, and your identity provider - for example Okta, Microsoft Entra ID or Ping Identity - provisions users and groups into that Authentication Method, pushing changes to Akeyless as they happen.

> **Warning:** When SCIM is enabled, only users that the identity provider has provisioned and marked active can sign in through that Authentication Method. Existing users can't sign in until the identity provider's first sync creates them. Logins missing the Unique Identifier are rejected.

## Authentication Model

Your identity provider authenticates to the SCIM endpoint with a dedicated [API Key Authentication Method](https://docs.akeyless.io/docs/auth-with-api-key) - the SCIM bearer - bound to the SAML or OIDC Authentication Method.

- **SCIM Base URL:** `https://<host>/scim/v2/<API-Key-Access-ID>/`
- **Authentication:** The Access Key alone is sent as the Bearer token. The Access ID is already part of the URL.
- Every SCIM request runs as that API Key, so it can only do what its Access Role allows.
- The endpoint can be **public** (served by Akeyless) or **private** (served by your own Gateway, which the identity provider must be able to reach).

## How Akeyless Maps SCIM Resources

| SCIM resource | Akeyless mapping |
| --- | --- |
| `User` | An Akeyless human identity on the SAML or OIDC Authentication Method. `userName` must match the Authentication Method's Unique Identifier (for example, `email`). Stored attributes: display name, given and family name, a work email, and the enterprise extension attributes (employee number, cost center, organization, division, department, manager). |
| `Group` | An Akeyless Group named `/scim/<Authentication Method Access ID>/<group name>`. Associate it with Access Roles to control what members can access. |
| Deactivating a user (`active: false`) | Blocks new logins and revokes the user's active tokens. |
| Deleting a user | Removes the identity, with the same effect as deactivating. |

## Supported SCIM Operations

| Endpoint | Supported methods |
| --- | --- |
| `/Users` | GET (list, and by ID), POST, PUT, PATCH, DELETE |
| `/Groups` | GET (list, and by ID), POST, PUT, PATCH, DELETE |
| `/ServiceProviderConfig` | GET |
| `/ResourceTypes` | GET |
| `/Schemas` | GET |

PATCH and filtering are supported, with up to 500 results per page. Bulk operations, sorting, ETags and password changes aren't supported.

## Limitations

- Users that existed before SCIM was enabled must be provisioned by the identity provider before they can sign in again.
- An API Key can be the SCIM bearer of only one Authentication Method.
- SCIM groups can be changed only through SCIM. An admin can't edit them in the console or CLI. To control what group members can access, associate the group with an Access Role in the usual way. If SCIM stops managing the groups (for example, you turn off SCIM or remove the bound API Key), the groups stay, and they can then be edited by anyone with the usual permissions on them.
- Rate limits: 20 requests per second per source IP address (bursts up to 100), and 50 requests per second per Authentication Method (bursts up to 200). The identity provider retries automatically.

### Supported Filters

- Operators: `eq`, `gt`, `ge`, combined with `and` and `or`.
- Users: `id`, `userName`, `externalId`, `meta.lastModified`.
- Groups: `id`, `displayName`, `externalId`, `meta.lastModified`, `members.value`.
- `meta.lastModified` accepts only `gt` and `ge`, with an RFC 3339 timestamp.

## Set Up SCIM Provisioning

### Prerequisites

1. A SAML or OIDC Authentication Method with a **Unique Identifier** set, for example `email`. SCIM matches each provisioned user to this attribute (a SAML attribute or an OIDC claim) at login.
2. A dedicated [API Key Authentication Method](https://docs.akeyless.io/docs/auth-with-api-key) to act as the SCIM bearer, for example `/scim/okta-provisioner`. Save its **Access ID** and **Access Key**. The Access Key is shown only once.
3. For a **private** endpoint: an Akeyless Gateway that your identity provider can reach over HTTPS with a publicly trusted certificate.

### Required Permissions

#### Admin who enables SCIM

| Action                                         | Permission needed                                |
| ---------------------------------------------- | ------------------------------------------------ |
| Enable SCIM or change its settings             | **Update** on the SAML or OIDC Authentication Method |
| Bind an API Key as the SCIM bearer             | **Update** on that API Key Authentication Method |
| View the SCIM status, Base URL and sync counts | **Read** on the SAML or OIDC Authentication Method |

#### SCIM API Key (used by the identity provider)

Create a dedicated Access Role, give it the rules below, and associate it **only** with the SCIM API Key. All rules use the **Auth Method** rule type.

| Path                                                         | Capabilities                                 | Why                                                                                                                                                                              |
| ------------------------------------------------------------ | --------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `/<SAML or OIDC auth method name>`, for example `/okta-saml` | `Read`, `Create`, `Update`, `Delete`         | Read, create, update and deactivate users. Each SCIM request type needs the matching permission: GET needs Read, POST needs Create, PUT/PATCH needs Update, DELETE needs Delete. |
| `/scim/<SAML or OIDC auth method Access ID>/*`                | `Read`, `List`, `Create`, `Update`, `Delete` | SCIM groups are stored as Akeyless Groups under this path.                                                                                                                       |
| `/<SCIM API Key name>`, for example `/scim/okta-provisioner` | `Read`                                       | Lets the Gateway confirm which Authentication Method the key is bound to.                                                                                                       |

- **Listing users** works with either `Read` or `List` on the `/<SAML or OIDC auth method name>` path.
- **SCIM groups** are stored as Akeyless Groups named `/scim/<SAML or OIDC auth method Access ID>/<group name>`, which is why the second rule's path is `/scim/<SAML or OIDC auth method Access ID>/*`.

```shell
akeyless create-role --name /scim/okta-scim-role

akeyless set-role-rule --role-name /scim/okta-scim-role --rule-type auth-method-rule \
  --path /okta-saml \
  --capability read --capability create --capability update --capability delete

akeyless set-role-rule --role-name /scim/okta-scim-role --rule-type auth-method-rule \
  --path "/scim/<SAML-or-OIDC-Access-ID>/*" \
  --capability read --capability list --capability create --capability update --capability delete

akeyless set-role-rule --role-name /scim/okta-scim-role --rule-type auth-method-rule \
  --path /scim/okta-provisioner \
  --capability read

akeyless assoc-role-am --role-name /scim/okta-scim-role --am-name /scim/okta-provisioner
```

> **Note:** Don't give this role any other access. If the role is missing a permission, the identity provider gets `401 Unauthorized`. For requests about a specific user (look up, update or deactivate), a missing permission returns `404 Not Found`, the same as a user that doesn't exist.

### Enable SCIM Provisioning

#### From the Console

1. Go to **Users & Auth Methods**, open your SAML or OIDC Authentication Method, and select the **SCIM Provisioning** tab.
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

For an OIDC Authentication Method, use `akeyless auth-method update oidc` with the same flags.

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
| **Unique identifier field** | `userName`. Its value must match the SAML or OIDC Unique Identifier (a SAML attribute or an OIDC claim), for example the user's email. |
| **Supported actions**       | Create users, update user attributes, deactivate users, push groups                                                         |

> **Note:** SCIM groups can be changed only through SCIM. An admin can't edit them in the console or CLI. To control what group members can access, associate the group with an Access Role in the usual way. If SCIM stops managing the groups (for example, you turn off SCIM or remove the bound API Key), the groups stay, and they can then be edited by anyone with the usual permissions on them.

## Identity Provider Notes

- **Microsoft Entra ID:** Entra ID provisions changes in cycles that run about every 40 minutes, so a change can take up to 40 minutes to reach Akeyless. The time of the last cycle is shown on the application's Provisioning page in the Entra admin center. To push a change right away, use Provision on demand, which provisions one user, or one group with up to five members, per request. See [Set Up Microsoft Entra ID as a SAML Authentication Method](https://docs.akeyless.io/docs/saml-auth-azure-ad) or [Set Up Microsoft Entra ID as an OIDC Authentication Method](https://docs.akeyless.io/docs/azure-active-directory-oidc).
- **Okta:** Okta pushes changes to Akeyless as they happen (when a user is assigned, updated or deactivated), with no fixed sync interval. See [Set Up Okta as a SAML Authentication Method](https://docs.akeyless.io/docs/saml-auth-okta) or [Set Up Okta as an OIDC Authentication Method](https://docs.akeyless.io/docs/okta-oidc).

## Check the SCIM Status

```shell
akeyless get-scim-status --name <SAML or OIDC Auth Method Name>
```

This returns the SCIM Base URL, the connection status, and counts of provisioned identities, groups and deactivated users.

## Rotate the SCIM Credential

Select **Rotate Credential** on the **SCIM Provisioning** tab to generate a new Access Key for the bound API Key. The old key stops working within about 15 seconds. Paste the new Access Key into your identity provider. The SCIM Base URL doesn't change.

## Troubleshooting

| Symptom                                      | Likely cause                                                                                                                                                                                       |
| -------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `401 Unauthorized` (JSON)                    | Wrong Access Key, the API Key's role is missing a permission, the identity provider's IPs aren't in **Allowed IPs**, or the endpoint type (public or private) doesn't match the host being called. |
| `403 Forbidden` (HTML) or `Connection reset` | The request never reached Akeyless. A firewall, WAF, load balancer, or wrong scheme or port is blocking the identity provider.                                                                     |
| Users can't sign in after SCIM is enabled    | They haven't been provisioned yet, or their identity provider `userName` doesn't match the SAML or OIDC Unique Identifier.                                                                         |
| `404 Not Found` for a user that exists       | The SCIM API Key's role is missing Read, Update or Delete on the Authentication Method path.                                                                                                        |
| `429 Too Many Requests`                      | The identity provider exceeded the SCIM rate limits: 20 requests per second per source IP address (bursts up to 100), and 50 requests per second per Authentication Method (bursts up to 200). The identity provider retries automatically. |

## Related Pages

- [SAML Authentication Method](https://docs.akeyless.io/docs/auth-with-saml)
- [OIDC Authentication Method](https://docs.akeyless.io/docs/auth-with-oidc)
- [Set Up Okta as a SAML Authentication Method](https://docs.akeyless.io/docs/saml-auth-okta)
- [Set Up Ping Identity as a SAML Authentication Method](https://docs.akeyless.io/docs/saml-auth-ping-identity)
- [Set Up Microsoft Entra ID as a SAML Authentication Method](https://docs.akeyless.io/docs/saml-auth-azure-ad)