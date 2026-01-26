---
title: SRA Best Practices
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
      slug: web-access-bastion-best-practices
      title: Web Access Bastion Best Practices
---
* **SRA Gateway location** Use SRA Gateway on any environment or region. In addition, your Gateway server should run with a dedicated Identity in an isolated environment.

* **Configure TLS** - Akeyless Gateway should always be used with TLS. If you are working with Load Balancers or reverse proxies in front of your Bastion, TLS should be used for all network connections to ensure all traffic is encrypted at transit.

* **Limit the access** for privileged items for specific Access IDs by creating a dedicated Authentication method for privileged users only who will have `read` permission for those privileged items.

* **Principal of Least privileged**- To follow this PoLP using the Akeyless RBAC model, utilize the "list" permission which will provide your users Just-in-Time Access while not exposing them to the secret.

* **SSH and CLI access required permissions** - Make sure your users will have `read` permissions on the [SSH Certificate Issuer](hhttps://docs.akeyless.io/docs/ssh-certificates) to ensure they will be able to issue a short-lived certificate to set up the connection.

* **Forward Logs** - From your Gateway to any logging system, to constantly track and monitor your users' activity.
