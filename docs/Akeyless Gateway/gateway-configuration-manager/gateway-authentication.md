---
title: Gateway Users Authentication
excerpt: ''
deprecated: false
hidden: false
metadata:
  title: ''
  description: ''
  robots: index
next:
  description: ''
  pages:
    - type: basic
      slug: configuring-tls
      title: Configuring TLS
---
Due to its nature as an extension to Akeyless SaaS services, the Akeyless Gateway can also act as a proxy for the Akeyless SaaS console. This proxy can be found on the `/console` endpoint of the Gateway URL e.g.  `https://Your_Akeyless_Gateway_URL:8000/console`\
Any user in the account can connect without any requirements based on their [Access Roles](https://docs.akeyless.io/docs/rbac). This endpoint replicates the Akeyless SaaS console, enabling seamless work with [Zero-Knowledge](https://docs.akeyless.io/docs/zero-knowledge) items.

To set a default [Authentication Methods](https://docs.akeyless.io/docs/access-and-authentication-methods) for your users, you can set either [SAML](https://docs.akeyless.io/docs/saml), [OIDC](https://docs.akeyless.io/docs/openid) or [Certificates-Based](https://docs.akeyless.io/docs/certificate-based-authentication) Authentication. 

> 👍 Note
>
> Gateway Users Authentication does not mean those users will be able to log in and manage your Gateway deployment, to set a list of Gateway Allowed Admins please refer to the Gateway Admins section in the relevant deployment guide.

# SAML & OIDC

To configure your Gateway to work with a default [SAML](https://docs.akeyless.io/docs/saml) or [OIDC](https://docs.akeyless.io/docs/openid) authentication method for your users, take the following steps:

Open the Gateway Console by going to **Gateways -> Your-Gateway -> Manage Gateway**, on the **Defaults** page, provide the relevant `Access ID` and save your changes.

Once saved, users can log in to your Gateway Console on the `/console` endpoint of the Gateway URL i.e.  `https://Your_Akeyless_Gateway_URL:8000/console`.

# Certificate-Based Authentication

To work with Certificate-Based Authentication as the default login method for your Gateway, ensure your Gateway deployment is set with `sni-proxy` enabled, as described in this [guide](https://docs.akeyless.io/docs/advance-gw-docker-configuration#setting-a-default-login) for Docker, or for K8s deployment as described [here](https://docs.akeyless.io/docs/advanced-k8s-gateway-configuration#defaults-gateway-settings).  

Set your users' DNS records with the cert authentication subdomain  `auth-cert.akeyless.io` to point to your Gateway IP address.

Open the Gateway Console by going to **Gateways -> Your-Gateway -> Manage Gateway**, on the **Defaults** page, provide the relevant `Access ID`, and save your changes.

Once saved, users can log in to your Gateway Console on the `/console` endpoint of the Gateway URL i.e.  `https://Your_Akeyless_Gateway_URL:8000/console`.

> 🚧 Warning
>
> Certificate-Based Authentication utilizes mTLS. Therefore, it is required that the Gateway itself will manage any TLS termination for the connection to Akeyless SaaS core services.
