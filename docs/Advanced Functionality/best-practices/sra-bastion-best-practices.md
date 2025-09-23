---
title: SRA Bastion Best Practices
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
* **SRA Bastion location** should be as close as possible to your Gateway to minimize latency. Use SRA Bastion on any environment or region, with a dedicated Gateway. In addition, your Bastion server should run with a dedicated Identity in an isolated environment.

* **Configure TLS** - Akeyless Bastion should always be used with TLS. If you are working with Load Balancers or reverse proxies in front of your Bastion, TLS should be used for all network connections to ensure all traffic is encrypted at transit.  

* **Limit the access** for privileged items for specific Access IDs by creating a dedicated Authentication method for privileged users only who will have `read` permission for those privileged items. 

* **Principal of Least privileged**- To follow this PoLP using the Akeyless RBAC model, utilize the "list" permission which will provide your users just-in-time access while not exposing them to the secret. 

* **SSH sessions** - While working with Akeyless [Secure Remote Access Bastion](doc:secure-remote-access-bastion) for SSH, a shared persistence volume should be used on those bastions to ensure the best performance for multiple concurrent SSH sessions.

* **SSH and CLI access required permissions** - Make sure your users will have `read` permissions on the [SSH Certificate Issuer](doc:how-to-configure-ssh) to ensure they will be able to issue a short-lived certificate to set up the connection. 

* **Forward Logs** - From your Bastions to any logging system, to constantly track and monitor your users' activity.