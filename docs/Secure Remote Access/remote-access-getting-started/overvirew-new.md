---
title: About SRA
deprecated: false
hidden: true
metadata:
  robots: index
---
# What is Secure Remote Access?

The Akeyless Platform’s Secure Remote Access (SRA) solution offers a modern approach to Privileged Access Management (PAM), enabling users to securely connect to **servers**, **databases**, **internal applications**, and **web apps** across any environment, whether cloud hosted or on-premise, private or public, by leveraging Just-in-Time, Zero-Trust access with full audibility.

Users can connect securely to resources through the Gateway's internal SRA Portal, the public [SRA Portal](https://docs.akeyless.io/docs/access-resources-remotely#connect-from-the-secure-remote-access-portal), a desktop application, or via the [Akeyless Connect](https://docs.akeyless.io/docs/remote-access-akeyless-connect) CLI command. Akeyless supports a variety of protocols, including `SSH`, `RDP`, `SQL`, and more.

## How it works

SRA is deployed alongside the Akeyless [Gateway](https://docs.akeyless.io/docs/api-gw) and consists of a **Web** application and **SSH** application, each has a separate pod in the cluster. These applications are deployed on your environment and enable an extra layer of protection between your private network and the cloud:

* **Web**: The web application allows users to securely access internal resources on a browser-based interface via the SRA Portal, leveraging embedded clients.

* **SSH**: The SSH application is primarily used for native CLI access from the users' terminal using the [Akeyless Connect](https://docs.akeyless.io/docs/remote-access-akeyless-connect) and [Akeyless SCP](https://docs.akeyless.io/docs/akeyless-scp-1) commands to any UNIX-supporting resource.

## Key Features

Akeyless Secure Remote Access provides a robust set of features designed to support secure, efficient access for teams. Here are some of the key capabilities:

* **Just-in-time Access**: With SRA, just-in-time secrets can be created and injected into a remote resource, such as a database, on the fly.

* **Rotated Secret Access**: Privileged secrets can be used to access remote resources with the ability to automatically rotate the credentials once the session ends.

* **Request for Access**: Admins have the ability to enable an option for users to request access for a specific resource on demand.

* **Audit and Session Management**: Akeyless provides full session management with auditing and recording capabilities to keep you compliant. Session recordings and transcripts can be automatically exported to remote storage systems for long-term retention.

* **Granular RBAC**: Access can be tightly scoped so that each user is granted only the necessary permissions to the specific targets or resources they need. Users only need SRA permissions to initiate connections, without requiring any  `read` access to the underlying secrets.

* **Native SSO integrations**: SRA supports authentication via SSO protocols such as **OIDC**, **SAML**, and **LDAP**.

## Supported Resource Types

Using SRA supports connections to the following resource types:

* [Databases](https://docs.akeyless.io/docs/database-secure-remote-access)
* [Windows Remote Desktop](https://docs.akeyless.io/docs/remote-desktop-secure-access)
* [AWS Console](https://docs.akeyless.io/docs/aws-console-secure-remote-access)
* [Azure Portal](https://docs.akeyless.io/docs/azure-portal-access)
* [GCP Portal](https://docs.akeyless.io/docs/gcp-portal-access)
* [SSH Servers](https://docs.akeyless.io/docs/ssh-remote-access)
* [LDAP Servers](#)
* [RabbitMQ](https://docs.akeyless.io/docs/rabbitmq-secure-remote-access)
* [Kubernetes](https://docs.akeyless.io/docs/k8s-cluster-access)
* [Web Applications](https://docs.akeyless.io/docs/web-applications-secure-remote-access)
* [Kubectl](https://docs.akeyless.io/docs/kubectl-access)