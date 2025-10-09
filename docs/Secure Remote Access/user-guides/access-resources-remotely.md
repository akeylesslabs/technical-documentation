---
title: SRA Web Portal
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
Depending on the [resource type](https://docs.akeyless.io/docs/supported-resource-types), you can securely access resources in the following ways:

* From the [Secure Remote Access Portal](https://docs.akeyless.io/docs/access-resources-remotely#connect-from-the-secure-remote-access-portal), access a resource over the web or using native CLI.

* With the [Akeyless Connect](https://docs.akeyless.io/docs/akeyless-connect) command, access a resource using native CLI from any UNIX terminal.

# Prerequisites

* [Secure Remote Access](https://dash.readme.com/project/akeyless/v1.0/docs/remote-access-setup-k8s) Installed. 

* [SAML](https://docs.akeyless.io/docs/saml), [OIDC](https://docs.akeyless.io/docs/openid) , [Certificate](https://docs.akeyless.io/docs/certificate-based-authentication) or [LDAP](https://docs.akeyless.io/docs/ldap) Authentication method available. 

* **Optional** - [Web Access](https://docs.akeyless.io/docs/web-access-bastion) Installed. 

# Connect from the Secure Remote Access Portal

The default authentication method for logging in to the Secure Remote Access Portal is Security Assertion Markup Language (SAML). For details about integrating your SAML authentication with the Akeyless Platform, see [here](https://docs.akeyless.io/docs/saml). Alternatively, you can choose [OIDC](https://docs.akeyless.io/docs/openid) to set the default authentication method. 

1. Go to `https://zerotrust.akeyless.io`.
2. In the **SAML Access ID** field, enter your SAML Access ID. or click the **OIDC** button to work with OpenID Connect. 
3. In the **Akeyless Gateway URL** field, enter your Akeyless Gateway URL on port 8000.

> 📘 Reminder
>
> The unified Gateway with Remote Access has simplified access to the various components by creating [internal mapping of the endpoints](https://docs.akeyless.io/docs/upgrading-to-the-unified-gateway-with-remote-access#what-does-the-unification-include).

4. If you are connecting to a database, SSH server, Windows Server, or RabbitMQ resources, in the **Web Client URL** field, enter the URL of your [Secure Remote Access](https://dash.readme.com/project/akeyless/v1.0/docs/remote-access-setup-k8s) (\<THIS URL IS BROKEN) with your `web-sra` cluster service port.
5. (Optional) If you are connecting to applications using Web Access in Isolated mode, in the **Web Application Dispatcher** field, enter the URL of your Web Access with your `web-access-dispatcher` cluster service port, the default set to `9000`. If you are working with Secure Proxy, also set the **Web Proxy URL** with the `web-access-dispatcher` cluster service port, the default set to`19414`.
6. Click **Sign in**.\
   The portal shows all the [supported resource types](https://docs.akeyless.io/docs/supported-resource-types). The number of resources of a particular type that you are authorized to access appears in the top-right corner of the resource tile. 

<Image align="center" src="https://files.readme.io/27339b3-Screenshot_2024-08-11_at_16.12.45.png" />

> 👍 Note
>
> To simplify login, after you enter all the required information but before you sign in, select **Generate SAML Bookmark URL** to create a link to the completed form. The link is copied to your clipboard for you to save in a convenient place, such as your browser bookmarks, and use in the future to automatically complete the login details.

## Add-hoc Hostnames for RDP/SSH Sessions

The Ad-hoc Hostnames feature in the portal allows users to quickly connect to hosts that are not part of the static host list by manually entering hostnames or IP addresses. This capability is especially useful for accessing dynamically created or temporary hosts without requiring updates to the static configuration.

> 📘 Key Features
>
> * **On-the-Fly Connections**: Users can provide a hostname or IP address for **RDP** or **SSH** sessions as needed
> * **Temporary Host Addition**: Hostnames added through this feature are temporary and stored in the browser’s cache.
> * **Edit** and **Delete** Capability: Users can edit or remove the last added host from the list.

1. Press on **Create Custom Target** button
2. Select the **Permission Profile**
3. Enter **Hostname** or **IP Address**
4. Press on **Confirm**

The user can **Edit** or **Delete** the last added host and it will be removed from the list of hosts in the portal.

## Start a Web Proxy Session

1. Click **Connect** next to the web resource you want to open.
2. Review the “Connection Info” pop‑up:
3. Press Connect in the pop‑up. A new **Incognito** / Private window launches automatically and loads the destination through the Akeyless Web Proxy.
4. Using a private window keeps session cookies and cached data isolated from your regular browsing session.

> 👍 NOTE
>
> If you do not see the new window, check your browser’s pop‑up blocker and allow pop‑ups for the Secure Remote Access portal.
