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
SCIM provisioning keeps Akeyless in sync with your identity provider. Without it, Akeyless learns about a user only when that user signs in, so changes in your directory (a new hire, a role change, someone leaving) don't reach Akeyless until the user's next login. With SCIM, your identity provider pushes those changes to Akeyless as they happen.

SCIM is turned on per [SAML](https://docs.akeyless.io/docs/auth-with-saml) or [OIDC](https://docs.akeyless.io/docs/auth-with-oidc) Authentication Method. It works with identity providers such as Okta, Microsoft Entra ID and Ping Identity.

<Callout icon="far fa-triangle-exclamation" theme="warn">
  ### Warning:

  When SCIM is enabled, only users that your identity provider has provisioned and marked active can sign in through that Authentication Method. Existing users can't sign in until the identity provider's first sync adds them.
</Callout>

## How It Works

- **Users:** Each user your identity provider assigns is added to Akeyless as an identity on the SAML or OIDC Authentication Method, with their name, email and work details. Akeyless matches each user to the Authentication Method's **Unique Identifier**, for example their email.
- **Groups:** Each group your identity provider pushes becomes an Akeyless Group. Associate the group with an Access Role to control what its members can access.
- **Leavers:** When the identity provider deactivates or removes a user, the user can no longer sign in, and any active sessions are ended right away. You don't have to wait for their tokens to expire.
- **Connection:** Your identity provider connects to Akeyless with a dedicated [API Key Authentication Method](https://docs.akeyless.io/docs/auth-with-api-key) that's linked to the SAML or OIDC Authentication Method. The identity provider can do only what that API Key's Access Role allows.
- **Endpoint:** The identity provider can connect through Akeyless (**public**) or through your own Gateway (**private**).

## Before You Start

- SCIM groups can be changed only by your identity provider, not in the Akeyless Console or CLI. If you turn off SCIM later, the groups stay in Akeyless and can then be edited as usual.
- Each API Key can be linked to only one Authentication Method, and it can't be deleted while it's linked.

## Set Up SCIM Provisioning

### Prerequisites

1. A SAML or OIDC Authentication Method with a **Unique Identifier** set, for example `email`.
2. A dedicated [API Key Authentication Method](https://docs.akeyless.io/docs/auth-with-api-key) for your identity provider to use, for example `/scim/okta-provisioner`. Save its **Access ID** and **Access Key**. The Access Key is shown only once.
3. For a **private** endpoint: an Akeyless Gateway that your identity provider can reach over HTTPS, with a publicly trusted certificate.

### Required Permissions

**To turn on SCIM**, you need **Update** on the SAML or OIDC Authentication Method and on the API Key Authentication Method. To view the SCIM status, you need **Read** on the SAML or OIDC Authentication Method.

**For the identity provider's API Key**, create a dedicated Access Role, add the rules below, and associate the role **only** with that API Key. All rules use the **Auth Method** rule type.

| Path                                                         | Permissions                        | Why                                                              |
| ------------------------------------------------------------ | ---------------------------------- | ---------------------------------------------------------------- |
| `/<SAML or OIDC auth method name>`, for example `/okta-saml` | Read, Create, Update, Delete       | To add, update and deactivate users.                             |
| `/scim/<SAML or OIDC auth method Access ID>/*`               | Read, List, Create, Update, Delete | To manage groups. Akeyless stores SCIM groups under this path.   |
| `/<API Key name>`, for example `/scim/okta-provisioner`      | Read                               | To confirm which Authentication Method the API Key is linked to. |

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

> **Note:** Don't give this role any other access.

### Turn On SCIM

#### From the Console

1. Go to **Users & Auth Methods**, open your SAML or OIDC Authentication Method, and select the **SCIM Provisioning** tab.
2. Turn on **Enable SCIM Provisioning**.
3. Select the **SCIM Endpoint**:
   - **Public**: served by Akeyless.
   - **Private**: served by your own Gateway. Your identity provider must be able to reach it.
4. In **Bearer Credential**, select the API Key Authentication Method.
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

| Parameter                 | Description                                                                      |
| ------------------------- | -------------------------------------------------------------------------------- |
| `--scim-enabled`          | Turns SCIM provisioning on or off.                                               |
| `--scim-bearer-access-id` | The Access ID of the API Key Authentication Method your identity provider uses.  |
| `--scim-endpoint`         | `public` (served by Akeyless) or `private` (served by your own Gateway).         |
| `--scim-gateway-url`      | The Gateway URL your identity provider calls. Required for a `private` endpoint. |

### Connect Your Identity Provider

In your identity provider's SCIM settings for the Akeyless app, enter:

| Setting                     | Value                                                                                                                            |
| --------------------------- | -------------------------------------------------------------------------------------------------------------------------------- |
| **SCIM Base URL**           | Copy it from the **SCIM Provisioning** tab.                                                                                      |
| **Authentication**          | HTTP Header / Bearer token                                                                                                       |
| **Token**                   | The API Key's **Access Key** only. Don't include the Access ID; it's already in the URL.                                         |
| **Unique identifier field** | `userName`. Its value must match the Unique Identifier of your SAML or OIDC Authentication Method, for example the user's email. |
| **Actions to enable**       | Create users, update user attributes, deactivate users, push groups                                                              |

## How Fast Changes Arrive

- **Microsoft Entra ID:** Entra ID sends changes about every 40 minutes, so a change can take up to 40 minutes to reach Akeyless. The time of the last sync is shown on the application's **Provisioning** page in the Entra admin center. To send a change right away, use **Provision on demand** for one user, or one group with up to five members. See [Set Up Microsoft Entra ID as a SAML Authentication Method](https://docs.akeyless.io/docs/saml-auth-azure-ad) or [Set Up Microsoft Entra ID as an OIDC Authentication Method](https://docs.akeyless.io/docs/azure-active-directory-oidc).
- **Okta:** Okta sends changes as they happen, when a user is assigned, updated or deactivated. See [Set Up Okta as a SAML Authentication Method](https://docs.akeyless.io/docs/saml-auth-okta) or [Set Up Okta as an OIDC Authentication Method](https://docs.akeyless.io/docs/okta-oidc).

## Check the SCIM Status

The **SCIM Provisioning** tab shows the connection status and how many users and groups were provisioned and how many users were deactivated. From the CLI:

```shell
akeyless get-scim-status --name <SAML or OIDC Auth Method Name>
```

## Rotate the API Key

Select **Rotate Credential** on the **SCIM Provisioning** tab to generate a new Access Key. The old key stops working within about 15 seconds, so paste the new Access Key into your identity provider right away. The SCIM Base URL doesn't change.

## Troubleshooting

| Problem                                                           | Likely cause                                                                                                                                                                                                       |
| ----------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| The identity provider gets `401 Unauthorized`                     | Wrong Access Key, the API Key's role is missing a permission, the identity provider's IP addresses aren't in the API Key's **Allowed IPs**, or the identity provider calls the wrong endpoint (public or private). |
| The identity provider gets `403 Forbidden` or `Connection reset`  | The request never reached Akeyless. A firewall, load balancer, or wrong address or port is blocking it.                                                                                                            |
| The identity provider gets `404 Not Found` for a user that exists | The API Key's role is missing a permission on the SAML or OIDC Authentication Method.                                                                                                                              |
| The identity provider gets `429 Too Many Requests`                | The identity provider sent too many requests at once. It retries automatically.                                                                                                                                    |
| Users can't sign in after SCIM is turned on                       | They haven't been provisioned yet, or their `userName` in the identity provider doesn't match the Unique Identifier.                                                                                               |

## Related Pages

- [SAML Authentication Method](https://docs.akeyless.io/docs/auth-with-saml)
- [OIDC Authentication Method](https://docs.akeyless.io/docs/auth-with-oidc)
- [Set Up Okta as a SAML Authentication Method](https://docs.akeyless.io/docs/saml-auth-okta)
- [Set Up Ping Identity as a SAML Authentication Method](https://docs.akeyless.io/docs/saml-auth-ping-identity)
- [Set Up Microsoft Entra ID as a SAML Authentication Method](https://docs.akeyless.io/docs/saml-auth-azure-ad)