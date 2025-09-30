---
title: Overview
excerpt: Secure Remote Access (SRA) Overview
deprecated: false
hidden: true
metadata:
  title: ''
  description: ''
  robots: index
next:
  description: ''
  pages:
    - type: basic
      slug: access-resources-remotely
      title: Access Resources Remotely
    - type: basic
      slug: supported-resource-types
      title: Supported Resource Types
    - type: basic
      slug: infrastructure-components
      title: Infrastructure Components
---
The Akeyless Platform's Secure Remote Access solution enables users to securely connect directly to resources - servers, databases, internal applications, and SaaS - in any of your environments, whether private, public, or on-prem.

<Image align="center" border={false} width="100%" src="https://files.readme.io/145d617-Secure_Remote_Access_Overview.png" />

Users can connect securely to resources from the [Secure Remote Access Portal](https://docs.akeyless.io/docs/access-resources-remotely#connect-from-the-secure-remote-access-portal) or using the [Akeyless Connect](doc:akeyless-connect) command. Akeyless supports a variety of protocols, including SSH, RDP, SQL, Kubectl, and more.

Depending on the resource type, users can select to access the resource either over the Web or using native CLI. In addition, [Akeyless Connect](doc:akeyless-connect) command provides users with CLI access to some resource types from any UNIX terminal.

> 📘 Info
>
> For more information about the resource types to which you can connect and how to set up access, see [Supported Resource Types](doc:supported-resource-types).

Secure Remote Access is enabled by the [Secure Remote Access Bastion](doc:secure-remote-access-bastion). When you define secure remote access to external SaaS systems, the [Web Access Bastion](doc:web-access-bastion) enables you only to allow access in Isolated mode, which restricts user access to other websites while they are connected to a SaaS system or using a secure proxy mode to enable access for an internal resource from the external network.

For details about these components, see [Infrastructure Components](doc:infrastructure-components).

When a user needs to connect to a resource, the [Secure Remote Access Bastion](doc:secure-remote-access-bastion) interfaces with the Akeyless Platform for user authentication and authorization. It then retrieves the required credentials from the Akeyless Platform and automatically injects them into the resource to give the user access.

In this way, our Secure Remote Access solution uniquely combines the ability to interface with 3rd-party **identity providers** for authentication with granular **role-based access control** for authorization and the ability to provide **just-in-time access** to endpoint resources, using dynamic secrets as short-lived credentials and certificates.

As the network communication flows between the user and the resource, it passes through the [Secure Remote Access Bastion](doc:secure-remote-access-bastion) and Akeyless can provide full session management with auditing and recording capabilities to keep you compliant. You can forward the system logs to your log management solution, as described in [Log Forwarding](doc:ssh-log-forwarding).

# Tutorial

Check out our tutorial video on [Install and Configure Remote Access Bastion](https://tutorials.akeyless.io/docs/install-and-configure-remote-access-bastion).
