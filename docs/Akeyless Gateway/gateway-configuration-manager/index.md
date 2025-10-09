---
title: Gateway Configuration Manager
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
      slug: gateway-authentication
      title: Gateway SAML & OIDC
    - type: basic
      slug: tls-certificate
      title: Gateway TLS Settings
    - type: basic
      slug: implement-zero-knowledge
      title: Implementing Zero Knowledge
    - type: basic
      slug: configure-the-gateway-cache
      title: Gateway Cache
---
The Gateway Configuration Manager is available via the main console under **Gateways -> Your-Gateway -> Manage Gateway** 

> 👍 Note
>
> The use of HTTP protocol is considered insecure and discouraged; thus, remote Gateway configuration is not supported over HTTP. If you wish to configure your gateway remotely make sure you do it over HTTPS.
>
> In case of connectivity issue, you can enter your legacy gateway console available at: `http://Your-Akeyless-Gateway-URL:8000`

In the Gateway Configuration Manager, the Gateway Admin can:

* [Manage Zero Knowledge](https://docs.akeyless.io/docs/implement-zero-knowledge) encryption. 

* Manage [TLS Settings](https://docs.akeyless.io/docs/tls-certificate)

* Set up [Log Forwarding](https://docs.akeyless.io/docs/log-forwarding) 

* Enable and configure [Gateway Cache](https://docs.akeyless.io/docs/configure-the-gateway-cache) 

* Setup [Automatic Migration](https://docs.akeyless.io/docs/automatic-migration) from external Secrets Management system.

As well as setting the default [Authentication Method](https://docs.akeyless.io/docs/access-and-authentication-methods) for the users on that Gateway, setting the default encryption key for that specific Gateway, and triggering an event of the Gateway state when it goes inactive to the Akeyless [Event Center](https://docs.akeyless.io/docs/event-center)

After the first login to the Gateway Configuration Manager, a record for the new Gateway instance is created in the Akeyless Console. 

> 📘 Info
>
> Each Gateway instance is uniquely identified by the combination of the **Access ID** of the first logged-in Authentication Method and the **Cluster Name** (*defaultCluster* by default).

You can identify and manage your [Gateway](https://docs.akeyless.io/docs/api-gw) inside the Akeyless Console, under the Gateways section.\
The Gateway's instance name is comprised of three strings, appearing in this order:

* **Account ID:** The string with the following format `acc-xxxxxxx`

* **Access ID:** The string with the following format `p-xxxxxxx`

* **Cluster name:** The remaining string component

To create a new Gateway instance or cluster, it is important to change the access or name strings.

To complete the setup of your Gateway, on the Akeyless Console, navigate to the Gateways screen, set a meaningful name for your Gateway, and provide the Gateway server URL to work with your Gateway from the Akeyless Console.
