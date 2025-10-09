---
title: Akeyless Gateway Best Practices
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
      slug: sra-bastion-best-practices
      title: SRA Bastion Best Practices
    - type: basic
      slug: web-access-bastion-best-practices
      title: Web Access Bastion Best Practices
---
## Network & Security

* [Akeyless Gateway (GW)](https://docs.akeyless.io/docs/api-gw) cluster should not be reachable from the external network, i.e., ingress traffic should be blocked, while egress traffic should be able to reach the required services. A list of the required endpoints that should be reachable from your GW can be found [here](https://docs.akeyless.io/docs/api-gateway-network-connectivity). 

* **Gateway Authentication method** - Should be used with a dedicated authentication method, stored under a path that only your admin users can access. When creating items associated with the Gateway, the Gateway's authentication method needs to have the following permissions:

  * For **Dynamic and Rotated Secrets** - List, Read, and Update permissions are required both on the secret item and on the target associated with the secret.

  * For **Universal Secret Connector** - Read permission is required both on the USC item and on the target associated with the USC.

* **Dedicated environment** - GW should be the only application running on the machine. This can be done using a dedicated docker that runs on that machine or a dedicated Kubernetes (K8s) cluster. This reduces the risk that another process running on the same machine is compromised and can interact with your GW.

* **Configure[TLS](https://docs.akeyless.io/docs/tls-certificate)**

* **Use your own Customer Fragment to[enable Zero-Knowledge](https://docs.akeyless.io/docs/implement-zero-knowledge)**

* **Configure your[default encryption key](https://docs.akeyless.io/docs/implement-zero-knowledge#set-up-a-default-encryption-key)**

## Management

* **Log Forwarding** - Create a dedicated GW with a dedicated Authentication method to collect and forward all Akeyless logs to your logs system. Such a dedicated Authentication Method should be associated with a dedicated Access Role, which will have permission to view all GWs logs. Only admins will have permission to view this GW Authentication Method and Access Role.

## High Availability

* **Configure a meaningful name for your cluster** - GW instances can be set as a cluster where the mutual identifier for your GW instances is a combination of your cluster name and the access ID of the authentication method you used to spin the GW instance. Providing a meaningful name to your clusters will ensure easier management and scalable environments of your GWs. 

* **High Availability** - You can create GW clusters to ensure service continuity and resiliency. Your GW instances can be located in different regions while working as a Geo-Cluster. GW instances don't need to communicate with each other directly. Akeyless Platform does the entire operation of synchronizing your instances. Working with Geo-Cluster provides an extra level of resiliency. In addition, your GW instances can work either in active-active or active-passive modes to address high loads.
