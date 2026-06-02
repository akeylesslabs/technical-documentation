---
title: Secure Remote Access Portal
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
The Secure Remote Access Portal is available through the main console at `http://Your-Akeyless-Gateway-URL:8000/sra/portal` or through the public SaaS console at `https://zerotrust.akeyless.io`. The portal includes a theme switch that lets users toggle between light and dark mode.

All Akeyless-supported [resource types](https://docs.akeyless.io/docs/sra-resource-types) can be accessed using the **SRA Portal**, [CLI](https://docs.akeyless.io/docs/cli), or the [Desktop Application](https://docs.akeyless.io/docs/sra-desktop-application-beta).

Currently, the SRA Portal supports the following authentication methods:

* [SAML](https://docs.akeyless.io/docs/auth-with-saml)
* [OIDC](https://docs.akeyless.io/docs/auth-with-oidc)
* [Certificate](https://docs.akeyless.io/docs/auth-with-certificate)
* [LDAP](https://docs.akeyless.io/docs/auth-with-ldap)

> ✅ **Tip (Allowed redirect URL):** If you are using SAML or OIDC auth methods, ensure your Gateway URL is trusted.

## Connect from the Secure Remote Access Portal

1. Open the SRA Portal: `http://Your-Akeyless-Gateway-URL:8000/sra/portal`
2. Select the relevant authentication method. The default is **SAML**. Enter your SAML **Access ID**, or choose a different method.
3. If you are also working with [Zero Trust Web Access](https://docs.akeyless.io/docs/sra-web-access-on-k8s), set the **Web Application Dispatcher** with the external URL of your dispatcher service on port `9000`. If you are working with Secure Proxy, also set the **Web Proxy URL** using port `19414`. For instructions on how to retrieve these URLs from your cluster, see [Get the Dispatcher Service URL](https://docs.akeyless.io/docs/sra-web-access-on-k8s#get-the-dispatcher-service-url).
4. Click the **Generate SAML Bookmark URL** to create a link to the completed form. The link is copied to your clipboard for you to save in a convenient place, such as your browser bookmarks, and use in the future to automatically complete the login details.
5. Click **Sign in**.

The portal shows all the [resource types](https://docs.akeyless.io/docs/sra-resource-types) that you are authorized to access.

![A screenshot of the Akeyless Secure Remote Access product and its portal of available options.](https://files.readme.io/27339b3-Screenshot_2024-08-11_at_16.12.45.png)

## Clipboard Behavior for Long Text

Portal copy actions use browser clipboard APIs.

In the frontend implementation, copy operations call the browser clipboard API with a fallback copy method. The implementation does not define a fixed character limit for copied text.

For long text payloads in active SRA sessions, behavior can vary by browser and session components.

For large payload transfers, use file transfer workflows instead of clipboard copy and paste.

### Add a Custom Target for SSH or RDP

In addition to existing hosts that are part of the allowed hosts on the [SSH Cert Issuer](https://docs.akeyless.io/docs/sra-ssh), you can add new hostnames or IP addresses on the fly by using a matching SSH Cert Issuer that can provide access.

> ℹ️ **Note (Key Features):**
>
> * **On-the-Fly Connections**: Users can provide a hostname or IP address for **RDP** or **SSH** sessions as needed.
> * **Temporary Host Addition**: Hostnames added through this feature are temporary and stored in the browser’s cache.
> * **Edit** and **Delete** Capability: Users can edit or remove the last added host from the list.

1. In the SSH or RDP window, choose **Custom Target** and click the **+** button.
2. Select the **Permission Profile**. For example, [SSH Cert Issuer](https://docs.akeyless.io/docs/sra-ssh).
3. Enter **Hostname** or **IP Address**.
4. Select **Confirm**.

Users can **Edit** or **Delete** the last added host, and it will be removed from the list of hosts in the portal.
