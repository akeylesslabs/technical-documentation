---
title: Gateway Access Permissions
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
Akeyless [Access Roles](doc:rbac) control all user access levels for items, analytics, and usage reports.

In parallel with [Gateway](doc:api-gw) administrative operations, you can set the exact level of access your [Gateway administrative users](https://docs.akeyless.io/docs/advance-gw-docker-configuration#gateway-admins) will have, from the management of just [Dynamic](doc:how-to-create-dynamic-secret) or [Rotated](doc:rotated-secrets) Secrets, up to, and including, complete admin rights.

> 📘 Info
>
> **Pre-Provisioned Admin Users** - Pre-Provisioned settings of your Gateway Admin users can not be modified after setup. To limit already **existing** admin users of your Gateway, you will be required to remove them from your deployment files.

# Configuring Access Permissions from the Gateway

> 👍 Note
>
> Only Gateway **Admin** users can access and manage the Access Permissions settings.

To configure **Access Permissions** in your [Gateway Configuration Manager](doc:gateway-configuration-manager), under the **Access Permissions** tab:

1. Click **New**

2. Define a meaningful **Name**  for the item. e.g., **Dynamic Secrets Admin**

3. From the **Auth Method** drop-down menu, choose the relevant [Authentication Method](doc:access-and-authentication-methods)  and set the exact [Sub-Claims](doc:sub-claims) identifying your users,  and click **Next**

4. In **Permission Settings**, select **Admin**  or **Custom**

5. If you choose **Custom**, select the relevant permissions to grant that Auth Method:

| Permission                      | Description                                                                                                                   |
| :------------------------------ | :---------------------------------------------------------------------------------------------------------------------------- |
| **Defaults**                    | Management of the default settings of your Gateway                                                                            |
| **Zero-Knowledge Encryption**   | Management of [Zero-Knowledge](https://docs.akeyless.io/docs/zero-knowledge)                                                  |
| **Targets**                     | Management of all Target items that were created using your Gateway                                                           |
| **Dynamic Secret**              | Management of [Dynamic Secrets](https://docs.akeyless.io/docs/how-to-create-dynamic-secret)                                   |
| **Rotated Secret**              | Management of [Rotated Secrets](https://docs.akeyless.io/docs/rotated-secrets)                                                |
| **Rotate Secret Value**         | Grants permission **only** to rotate the secret value, without allowing manual edits. Requires `read` permission on the item. |
| **Classic Keys**                | Management of [Classic Keys](https://docs.akeyless.io/docs/classic-keys)                                                      |
| **Kubernetes Auth**             | Management of [Kubernetes](https://docs.akeyless.io/docs/kubernetes-auth)  Auth Gateway configuration                         |
| **LDAP Auth**                   | Management of [LDAP ](https://docs.akeyless.io/docs/ldap)  Auth Gateway configuration                                         |
| **Kerberos Auth**               | Management of [Kerberos](https://docs.akeyless.io/docs/kerberos)  Auth Gateway configuration                                  |
| **Caching**                     | Management of [Gateway Cache](https://docs.akeyless.io/docs/configure-the-gateway-cache)  settings                            |
| **Automatic Migration**         | Management of [Automatic Migration](https://docs.akeyless.io/docs/automatic-migration)  settings                              |
| **Log-Forwarding**              | Management of [Log Forwarding](https://docs.akeyless.io/docs/log-forwarding)  settings                                        |
| **Event-Forwarding**            | Management of [Event](https://docs.akeyless.io/docs/event-center)  Forwarding settings                                        |
| **KMIP**                        | Management of [KMIP Servers](https://docs.akeyless.io/docs/kmip-server)                                                       |
| **ACME**                        | Management of [ACME Servers](https://docs.akeyless.io/docs/acme-server)                                                       |
| **Remote Access Configuration** | Management of Remote Access configuration                                                                                     |

Based on the selected operations, the relevant Auth Method will only have access to initiate those operations.

You can also manage your **Gateway Access Permissions** using the Console by going to the **Gateways** tab and selecting the desired **Gateway**. On the right side of the screen, click the **Access Permissions** tab.
