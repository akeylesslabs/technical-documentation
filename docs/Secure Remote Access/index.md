---
title: Secure Remote Access
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
## What Is Secure Remote Access?

Secure Remote Access (SRA) is part of the Akeyless identity security platform and provides Zero Trust access to private resources without exposing static credentials. It enables users to connect to servers, databases, Kubernetes clusters, web applications, and cloud consoles from managed entry points.

Users can connect through the Gateway-hosted portal, the public [SRA Portal](https://docs.akeyless.io/docs/sra-portal#connect-from-the-secure-remote-access-portal), the desktop application, or [Akeyless Connect](https://docs.akeyless.io/docs/sra-akeyless-connect) and [Akeyless SCP](https://docs.akeyless.io/docs/sra-akeyless-scp) commands. Supported protocols include SSH, RDP, SQL, `kubectl`, LDAP, and web access flows.

> ℹ️ **Note (Getting started):**
>
> To deploy quickly, start with the [Quick Start](https://docs.akeyless.io/docs/sra-quick-start-guide). For deployment planning and architecture decisions, continue with [Setup Overview](https://docs.akeyless.io/docs/sra-setup-overview).

## Architecture

SRA is deployed with the [Akeyless Gateway](https://docs.akeyless.io/docs/gateway-overview). Core runtime components include the gateway service, an SSH bastion service, and a web bastion service. Optional components such as Zero Trust Web Access workers and Redis are used based on the selected topology.

![Akeyless Gateway and Secure Remote Access architecture](https://files.readme.io/e02b0e922edccd3c72e9224cc5c6983b7db67dcfe164b1efedcc726777437586-Screenshot_2025-06-27_at_19.25.39.png)

1. Web bastion: Provides browser-based access from the portal and embedded clients.
2. SSH bastion: Handles terminal-based and CLI-native access flows.
3. Gateway control plane: Retrieves dynamic credentials, applies policy controls, and brokers secure sessions.

To connect to a resource, a user first authenticates by using a configured identity provider. After authorization, SRA routes access through gateway-managed SRA services and applies configured policy controls.

This model combines external identity providers for authentication, role-based access control (RBAC) for authorization, and just-in-time credentials for session establishment.

## Deployment Models

SRA supports more than one deployment pattern depending on operational requirements:

* Unified deployment: Deploy SRA by using the `akeyless-gateway` chart with SRA enabled.
* Legacy split deployment: Existing environments might still use a separate SRA deployment model, but migration to the unified deployment is recommended.
* Topology variants: Kubernetes and Docker Compose are both supported, including Zero Trust Web Access patterns for browser-isolated access.

For implementation details, start with [Setup Overview](https://docs.akeyless.io/docs/sra-setup-overview).

## Prerequisites and First Steps

Before deployment, verify that the environment has:

* A supported runtime (Kubernetes or Docker Compose).
* Required network access and open ports for gateway and SRA components.
* At least one authentication method, an access role, and an SSH certificate issuer for SSH-based access.

Then follow this order:

1. Complete [Quick Start](https://docs.akeyless.io/docs/sra-quick-start-guide) for a baseline deployment.
2. Review [Setup Overview](https://docs.akeyless.io/docs/sra-setup-overview) and advanced setup pages.
3. Configure resource-specific access in [Supported Resource Types](https://docs.akeyless.io/docs/sra-resource-types).

## Documentation Map

Use this map to move through the SRA documentation by workflow:

* Setup and deployment: [Setup Overview](https://docs.akeyless.io/docs/sra-setup-overview)
* Access configuration and policy controls: [SRA Admin Guides](https://docs.akeyless.io/docs/sra-admin-guides)
* User access flows (portal, desktop app, and CLI): [SRA User Guides](https://docs.akeyless.io/docs/sra-user-guides)
* Session operations and monitoring: [Session Management](https://docs.akeyless.io/docs/sra-sessions-overview)
* Integrations and automation (CLI and API references): [CLI Gateway Reference](https://docs.akeyless.io/docs/cli-reference-gateway) and [Akeyless API v2 Reference](https://docs.akeyless.io/reference/gatewaygetremoteaccess)
* Infrastructure planning and troubleshooting: [SRA Setup on Kubernetes](https://docs.akeyless.io/docs/sra-setup-k8s) and [SRA Setup on Docker](https://docs.akeyless.io/docs/sra-docker)

## Key Features

Akeyless Secure Remote Access provides a robust set of features designed to support secure, efficient access for teams. Here are some of the key capabilities:

1. Just-in-Time Access: With SRA, just-in-time secrets can be created and injected into a remote resource, such as a database, on the fly.
2. Rotated Secret Access: Privileged secrets can be used to access remote resources with the ability to automatically rotate the credentials once the session ends.
3. Support for Various Protocols: Akeyless supports a variety of protocols, including SSH, RDP, SQL, kubectl, and more.
4. Request for Access: Admins have the ability to enable an option for users to [request access](https://docs.akeyless.io/docs/request-access) for a specific resource on-demand, using a built-in approval workflow.
5. Audit and Session Management: Akeyless provides full session management with auditing and recording capabilities to keep you compliant. Session recordings and transcripts can be automatically exported to remote storage systems for long-term retention.
6. Granular RBAC: Access can be tightly scoped so that each user is granted only the necessary permissions to the specific targets or resources they need (Users are restricted from accessing anything beyond their defined scope). Users only need SRA permissions to initiate connections—without requiring any _Read_ access to the underlying secrets.
7. Native SSO integrations: SRA supports authentication by way of SSO protocols such as OIDC, SAML, and LDAP.
8. Multiple connection interfaces: Web UI, CLI, and desktop application

## Use Cases

### Secretless User Access

Allow your users to access sensitive infrastructure resources without credentials.

### Just-in-Time Zero-Trust Access

Implement a gold-standard Zero-Trust environment and make auditing a breeze.

### Third Party Access

Provide third-party access to resources without compromising your security.

### Manage Access to Kubernetes Clusters

Remote Access supports access to any flavor of Kubernetes cluster, including EKS, GKE or any other generic Kubernetes cluster.

## Supported Resource Types

The Akeyless Remote Access solution supports connections to the following resource types:

* [Databases](https://docs.akeyless.io/docs/sra-database)
* [Windows Remote Desktop](https://docs.akeyless.io/docs/sra-remote-desktop)
* [AWS Console](https://docs.akeyless.io/docs/sra-aws-console)
* [Azure Portal](https://docs.akeyless.io/docs/sra-azure-portal)
* [GCP Portal](https://docs.akeyless.io/docs/sra-gcp-portal)
* [SSH Servers](https://docs.akeyless.io/docs/sra-ssh)
* [LDAP Servers](https://docs.akeyless.io/docs/auth-with-ldap)
* [RabbitMQ](https://docs.akeyless.io/docs/sra-rabbitmq)
* [Kubernetes](https://docs.akeyless.io/docs/sra-k8s-cluster)
* [Web Applications](https://docs.akeyless.io/docs/sra-web-applications)
* [kubectl](https://docs.akeyless.io/docs/kubectl-access)

## Web Access

In addition, it is possible to define remote access to external software as a service systems by using the [Web Access Application](https://docs.akeyless.io/docs/sra-web-access-on-k8s) as a separate deployment that is not connected to the gateway. This enables browser-isolated access to approved web destinations, and supports secure proxy mode for internal resources.

For details about the different remote access components, see [Setup Overview](https://docs.akeyless.io/docs/sra-setup-overview).
