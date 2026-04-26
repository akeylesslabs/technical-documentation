---
title: SRA Best Practices
excerpt: ''
deprecated: false
hidden: false
metadata:
  title: ''
  description: ''
  robots: index
---
* **SRA Gateway location**: Use SRA Gateway in any environment or region. In addition, your Gateway server should run with a dedicated identity in an isolated environment.

* **Configure TLS** - Akeyless Gateway should always be used with TLS. If you are working with Load Balancers or reverse proxies in front of your Bastion, TLS should be used for all network connections to ensure all traffic is encrypted in transit.

* **Limit the access** for privileged items for specific Access IDs by creating a dedicated Authentication method for privileged users only who will have `read` permission for those privileged items.

* **Principle of least privilege** - To follow PoLP using the Akeyless RBAC model, use the "list" permission, which provides Just-in-Time access to users without exposing the secret.

* **SSH and CLI access required permissions** - Make sure your users have `read` permissions on the [SSH Certificate Issuer](https://docs.akeyless.io/docs/sra-ssh-certificates) to ensure they can issue a short-lived certificate to set up the connection.

* **Forward Logs** - From your Gateway to any logging system, to constantly track and monitor your users' activity.
