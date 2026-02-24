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
The Secure Remote Access Portal is available through the main console at `http://Your-Akeyless-Gateway-URL:8000/sra/portal` or through the public SaaS console at `https://zerotrust.akeyless.io`.

All Akeyless supported [Resource types](https://docs.akeyless.io/docs/supported-resource-types) can be accessed using the **SRA Portal**, [CLI](https://docs.akeyless.io/docs/cli) or by way of the [Desktop Application](https://docs.akeyless.io/docs/remote-access-desktop-application-beta).

Currently the SRA Portal supports the following Authentication Methods:

* [SAML](https://docs.akeyless.io/docs/auth-with-saml)
* [OIDC](https://docs.akeyless.io/docs/auth-with-oidc)
* [Certificate](https://docs.akeyless.io/docs/auth-with-certificate)
* [LDAP](https://docs.akeyless.io/docs/auth-with-ldap)

<Callout icon="👍" theme="okay">
  _Allowed Redirect URL:_ If you are using SAML or OIDC Auth Methods, ensure your Gateway URL is trusted.
</Callout>

## Connect from the Secure Remote Access Portal

1. Open the SRA Portal: `http://Your-Akeyless-Gateway-URL:8000/sra/portal`
2. Select the relevant Authentication method, the default is **SAML**, enter your SAML **Access ID**, or choose a different method.
3. If you are also working with [Zero Trust Web Access](https://docs.akeyless.io/docs/web-access-on-k8s), set the **Web Application Dispatcher** with the URL of your `web-access-dispatcher` cluster service; the default is `9000`. If you are working with Secure Proxy, also set the **Web Proxy URL** with the `web-access-dispatcher` cluster service port; the default is `19414`.
4. Click the **Generate SAML Bookmark URL** to create a link to the completed form. The link is copied to your clipboard for you to save in a convenient place, such as your browser bookmarks, and use in the future to automatically complete the login details.
5. Click **Sign in**.

The portal shows all the [resource types](https://docs.akeyless.io/docs/supported-resource-types) that you are authorized to access

<Image alt="A screenshot of the Akeyless Secure Remote Access product and its portal of available options." border={false} src="https://files.readme.io/27339b3-Screenshot_2024-08-11_at_16.12.45.png" />

### Add a Custom Target for SSH or RDP

In addition to the existing hosts that are part of the allowed hosts on the [SSH Cert Issuer](https://docs.akeyless.io/docs/ssh-remote-access), you can also add new Hostnames or IP on the fly by using the matching SSH Cert Issuer that can provide access

> 📘 Key Features
>
> * **On-the-Fly Connections**: Users can provide a hostname or IP address for **RDP** or **SSH** sessions as needed
> * **Temporary Host Addition**: Hostnames added through this feature are temporary and stored in the browser’s cache.
> * **Edit** and **Delete** Capability: Users can edit or remove the last added host from the list.

1. On the SSH or RDP window choose **Custom Target**, and click the **+** button.
2. Select the **Permission Profile**. For example, [SSH Cert Issuer](https://docs.akeyless.io/docs/ssh-remote-access).
3. Enter **Hostname** or **IP Address**.
4. Select **Confirm**.

The user can **Edit** or **Delete** the last added host and it will be removed from the list of hosts in the portal.
