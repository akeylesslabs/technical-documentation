---
title: Overview
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
      slug: quick-start-guide
      title: Quick Start
---
> 📘 Unified Gateway/Secure Remote Access
> 
> Please note that these docs are written with the Gateway and Secure Remote Access single chart deployment. You may continue using the separate Gateway and Secure Remote Access solution you currently have in order to access your remote resources.

# What is Secure Remote Access?

The Akeyless Platform’s Secure Remote Access (SRA) solution offers a modern approach to Privileged Access Management (PAM), enabling users to securely connect to servers, databases, internal applications, and web apps across any environment—whether cloud hosted or on-premise, private or public—by leveraging Just-in-Time, Zero-Trust access with full auditability. 

Users can connect securely to resources through the Gateway's internal SRA Portal, the public [SRA Portal](https://docs.akeyless.io/docs/access-resources-remotely#connect-from-the-secure-remote-access-portal), a desktop application, or via the [Akeyless Connect](https://docs.akeyless.io/docs/remote-access-akeyless-connect) CLI command. Akeyless supports a variety of protocols, including SSH, RDP, SQL, kubectl, and more.

# Architecture

SRA is deployed alongside the Akeyless [Gateway](https://docs.akeyless.io/docs/api-gw) and consists of a Web application and SSH application, each a separate container in the cluster. These applications are deployed on your environment and enable an extra layer of protection between your private network and the cloud:

[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/e02b0e922edccd3c72e9224cc5c6983b7db67dcfe164b1efedcc726777437586-Screenshot_2025-06-27_at_19.25.39.png",
        "",
        ""
      ],
      "align": "center",
      "caption": "Gateway & Secure Remote Access architecture"
    }
  ]
}
[/block]


1. Web: The web application allows users to securely access internal resources on a browser-based interface via the SRA Portal, leveraging embedded clients.
2. SSH: The SSH application is primarily used for native CLI access from the users' terminal using the [Akeyless Connect](https://docs.akeyless.io/docs/remote-access-akeyless-connect) and [Akeyless SCP](https://docs.akeyless.io/docs/akeyless-scp-1) commands to any UNIX-supporting resource.

To connect to a resource, the user first authenticates to Akeyless via a configured Identity Provider (IdP). Once authorized, SRA facilitates the connection in a Zero-Trust manner by retrieving the required secret credentials via the Gateway and automatically injecting them into the target resource to establish and proxy the user’s access.

As a result, Akeyless uniquely combines the ability to interface with 3rd-party **identity providers** for authentication with granular **role-based access control** (**RBAC**) for authorization and the ability to provide **just-in-time access** to remote resources, using dynamic secrets as short-lived credentials and certificates.

# Key Features

Akeyless Secure Remote Access provides a robust set of features designed to support secure, efficient access for teams. Here are some of the key capabilities:

1. Just-in-time Access: With SRA, just-in-time secrets can be created and injected into a remote resource, such as a database, on the fly.
2. Rotated Secret Access: Privileged secrets can be used to access remote resources with the ability to automatically rotate the credentials once the session ends.
3. Support for Various Protocols: Akeyless supports a variety of protocols, including SSH, RDP, SQL, Kubectl, and more.
4. Request for Access: Admins have the ability to enable an option for users to request access for a specific resource on-demand.
5. Audit and Session Management: Akeyless provides full session management with auditing and recording capabilities to keep you compliant. Session recordings and transcripts can be automatically exported to remote storage systems for long-term retention.
6. Granular RBAC: Access can be tightly scoped so that each user is granted only the necessary permissions to the specific targets or resources they need (Users are restricted from accessing anything beyond their defined scope). Users only need SRA permissions to initiate connections—without requiring any _Read_ access to the underlying secrets.
7. Native SSO integrations: SRA supports authentication via SSO protocols such as OIDC, SAML, and LDAP.
8. Multiple connection interfaces: WebUI, CLI, Desktop app

# Use Cases

## Secretless User Access

Allow your users to access sensitive infrastructure resources without credentials.

## Just-in-Time Zero-Trust Access

Implement a gold-standard Zero-Trust environment and make auditing a breeze.

## 3rd Party Access

Provide third-party access to resources without compromising your security.

## Manage Access to K8s Clusters

Remote Access supports access to any flavor of K8s cluster, including EKS, GKE or any other generic K8s cluster.

# Supported Resource Types

Akeyless' Remote Access solution supports connections to the following resource types:

- [Databases](https://docs.akeyless.io/docs/database-secure-remote-access)
- [Windows Remote Desktop](https://docs.akeyless.io/docs/remote-desktop-secure-access)
- [AWS Console](https://docs.akeyless.io/docs/aws-console-secure-remote-access)
- [Azure Portal](https://docs.akeyless.io/docs/azure-portal-access)
- [GCP Portal](https://docs.akeyless.io/docs/gcp-portal-access)
- [SSH Servers](https://docs.akeyless.io/docs/ssh-remote-access)
- [LDAP Servers](#)
- [RabbitMQ](https://docs.akeyless.io/docs/rabbitmq-secure-remote-access)
- [Kubernetes](https://docs.akeyless.io/docs/k8s-cluster-access)
- [Web Applications](https://docs.akeyless.io/docs/web-applications-secure-remote-access)
- [Kubectl](https://docs.akeyless.io/docs/kubectl-access)

# Web Access

In addition, you can define Remote Access to external SaaS systems using the [Web Access Application](https://dash.readme.com/project/akeyless/v1.0/docs/web-access-on-k8s) as a separate deployment, not connected to the Gateway. This enables you to remotely access web-based applications in Isolated mode, which restricts user access to only the websites you determine, either while connected to a SaaS system or using a secure proxy mode to enable access for an internal resource from the external network.

For details about the various Remote Access components, see [Overview Section](https://docs.akeyless.io/docs/remote-access-setup-overview).