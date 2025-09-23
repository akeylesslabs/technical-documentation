---
title: Web Access Bastion Best Practices
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
* **Web Access Bastions Location** should be as close as possible to your Gateway to minimize latency. Use SRA Bastion on any environment or region, with a dedicated Gateway. In addition, your Bastion server should run with a dedicated Identity in an isolated environment.

* **Configure TLS** - Akeyless Bastion should always be used with TLS. If you are working with Load Balancers or reverse proxies in front of your Bastion, TLS should be used for all network connections to ensure all traffic is encrypted at transit.  

* **Isolation mode**  - Can be set with `list` permissions to ensure users will get their access only via isolated sessions. In addition, allowlist the relevant domains and force `HTTPS` connections only to enable credentials injection.

* **Required resources** - Default is set to 1Gb memory. If your web targets require high resolution or multiple concurrent sessions, increase the resources up to your needs.  

* **Forward Logs** - From your bastions to any logging system, to constantly track and monitor your user's activity.