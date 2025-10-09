---
title: Overview - Old
excerpt: ''
deprecated: false
hidden: true
metadata:
  title: ''
  description: ''
  robots: index
next:
  description: ''
---
> ❗️ Legacy Docs
>
> Please note that this version of our Remote Access documentation is not current. Please see our most updated docs [here](https://docs.akeyless.io/docs/secure-remote-access).

The Akeyless Platform's Secure Remote Access solution enables users to securely connect directly to resources - servers, databases, internal applications, and SaaS - in any of your environments, whether private, public, or on-prem.

Users can connect securely to resources either from the [Remote Access Portal](https://docs.akeyless.io/docs/access-resources-remotely#connect-from-the-secure-remote-access-portal) via the web or using the [Akeyless Connect](https://docs.akeyless.io/docs/akeyless-connect) command for native CLI access to some resources from any UNIX terminal. Akeyless supports a variety of protocols, including SSH, RDP, SQL, Kubectl, and more.

<Image align="center" border={false} width="100%" src="https://files.readme.io/145d617-Secure_Remote_Access_Overview.png" />

> 📘 Info
>
> For more information about the resource types to which you can connect and how to set up access, see [Supported Resource Types](https://docs.akeyless.io/docs/supported-resource-types).

# Remote Access Basics

Remote Access is enabled from within the [Akeyless Gateway](https://docs.akeyless.io/docs/api-gw) deployment. This will create two additional containers in the gateway cluster, one for web-based remote access (labeled "web") and the other for native, CLI-based access (labeled "ssh").

When a user needs to connect to a resource, Akeyless [Remote Access](https://docs.akeyless.io/docs/secure-remote-access-bastion) interfaces with the Akeyless Platform for user authentication and authorization. It then retrieves the required credentials from the Akeyless account and automatically injects them into the resource to give the user access.

In this way, our Remote Access solution uniquely combines the ability to interface with 3rd-party **identity providers** for authentication with granular **role-based access control** for authorization and the ability to provide **just-in-time access** to remote endpoint resources, using dynamic secrets as short-lived credentials and certificates.

As the network communication flows between the user and the resource, it passes through Akeyless [Remote Access](https://docs.akeyless.io/docs/secure-remote-access-bastion) and Akeyless can provide full session management with auditing and recording capabilities to keep you compliant. You can also forward the system logs to your log management solution, as described in [Log Forwarding](https://docs.akeyless.io/docs/ssh-log-forwarding).

# Web Access

In addition, you can define remote access to external SaaS systems using the [Web Access Bastion](https://docs.akeyless.io/docs/web-access-bastion) as a separate deployment. This enables you to remotely access web-based applications in Isolated mode, which restricts user access to only the websites you determine, either while connected to a SaaS system or using a secure proxy mode to enable access for an internal resource from the external network.

For details about these components, see [Infrastructure Components](https://docs.akeyless.io/docs/infrastructure-components).

# Tutorial

Check out our tutorial video on [Install and Configure Remote Access Bastion](https://tutorials.akeyless.io/docs/install-and-configure-remote-access-bastion).
