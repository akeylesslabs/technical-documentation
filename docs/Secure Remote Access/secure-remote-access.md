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

Secure Remote Access (SRA) is part of the Akeyless identity security platform. It provides Zero Trust access to private resources by brokering access through gateway and SRA services with dynamic and rotated secret patterns, rather than long-lived static credentials. This model follows a Zero Standing Privileges (ZSP) approach by minimizing persistent credentials in access flows.

SRA supports interactive access to servers, databases, Kubernetes clusters, web applications, and cloud consoles. Users can connect from the Gateway-hosted portal, the public [SRA Portal](https://docs.akeyless.io/docs/sra-portal#connect-from-the-secure-remote-access-portal), the desktop application, or CLI tools such as [Akeyless Connect](https://docs.akeyless.io/docs/sra-akeyless-connect) and [Akeyless File Transfer](https://docs.akeyless.io/docs/sra-akeyless-scp).

Supported access patterns include SSH, RDP, SQL, `kubectl`, LDAP, and web access workflows.

<Callout icon="ℹ️" theme="info">
  ### **Note (Getting started):**

  To deploy quickly, start with the [Quick Start](https://docs.akeyless.io/docs/sra-quick-start-guide). For deployment planning and architecture decisions, continue with [Setup Overview](https://docs.akeyless.io/docs/sra-setup-overview).
</Callout>

## How It Works

At a high level, SRA follows this flow:

1. A user authenticates with a configured identity provider.
2. Configured SRA access restrictions and policy settings, such as allowed access IDs and authentication controls, are applied through gateway and SRA components, and traffic is routed to SRA services.
3. The session is established through SRA web or SSH bastion components.

In gateway-managed deployments, SRA runtime and management paths include:

- `/sra/portal`
- `/sra/web-client`
- `/sra/ssh-config`
- `/config/sra`

These paths are part of the gateway route and SRA configuration model described in the implementation.

## Architecture

SRA is deployed with the [Akeyless Gateway](https://docs.akeyless.io/docs/gateway-overview). Core components are:

- Gateway service for routing and configuration management.
- SSH bastion service for terminal and CLI-native access.
- Web bastion service for browser-based sessions.
- Optional cache and optional Zero Trust Web Access components, depending on topology.

![Akeyless Gateway and Secure Remote Access architecture](https://files.readme.io/e02b0e922edccd3c72e9224cc5c6983b7db67dcfe164b1efedcc726777437586-Screenshot_2025-06-27_at_19.25.39.png)

## Deployment Models

SRA supports multiple deployment patterns:

- Unified deployment: Deploy SRA by using the `akeyless-gateway` chart with SRA enabled.
- Topology variants: Kubernetes and Docker Compose are both supported, including Zero Trust Web Access patterns for browser-isolated access.

## Before Deployment

Before deployment, confirm these prerequisites:

- A supported runtime (Kubernetes or Docker Compose).
- Required network access and open ports for gateway and SRA components.
- At least one authentication method, an access role, and an SSH certificate issuer for SSH-based access.

## Start Here by Goal

Use this path based on the immediate objective:

1. Baseline deployment: [Quick Start](https://docs.akeyless.io/docs/sra-quick-start-guide)
2. Deployment planning and architecture: [Setup Overview](https://docs.akeyless.io/docs/sra-setup-overview)
3. Resource onboarding: [Supported Resource Types](https://docs.akeyless.io/docs/sra-resource-types)
4. User operation model: [Accessing Resources](https://docs.akeyless.io/docs/sra-accessing-resources)
5. Admin controls and policies: [SRA Admin Guides](https://docs.akeyless.io/docs/sra-admin-guides)

## Documentation Map

Use this map to move through the SRA documentation by workflow:

- Setup and deployment: [Setup Overview](https://docs.akeyless.io/docs/sra-setup-overview)
- Access configuration and policy controls: [SRA Admin Guides](https://docs.akeyless.io/docs/sra-admin-guides)
- User access flows (portal, desktop app, and CLI): [Accessing Resources](https://docs.akeyless.io/docs/sra-user-guides)
- Session operations and monitoring: [Session Management](https://docs.akeyless.io/docs/sra-sessions-overview)
- Integrations and automation (CLI and API references): [CLI Gateway Reference](https://docs.akeyless.io/docs/cli-reference-gateway) and [Akeyless API v2 Reference](https://docs.akeyless.io/reference/gatewaygetremoteaccess)
- Infrastructure planning and troubleshooting: [SRA Setup on Kubernetes](https://docs.akeyless.io/docs/sra-setup-k8s) and [SRA Setup on Docker](https://docs.akeyless.io/docs/sra-docker)

## What to Configure Next

After baseline deployment, most teams configure these in order:

1. Access and entitlement policy for SRA users.
2. Session recording and forwarding destination settings.
3. Resource-specific access configuration for required target types.
4. CLI and API workflows for automation.

## Supported Resource Types

The Akeyless Remote Access solution supports connections to the following resource types:

- [Databases](https://docs.akeyless.io/docs/sra-database)
- [Windows Remote Desktop](https://docs.akeyless.io/docs/sra-remote-desktop)
- [AWS Console](https://docs.akeyless.io/docs/sra-aws-console)
- [Azure Portal](https://docs.akeyless.io/docs/sra-azure-portal)
- [GCP Portal](https://docs.akeyless.io/docs/sra-gcp-portal)
- [SSH Servers](https://docs.akeyless.io/docs/sra-ssh)
- [LDAP Servers](https://docs.akeyless.io/docs/auth-with-ldap)
- [RabbitMQ](https://docs.akeyless.io/docs/sra-rabbitmq)
- [Kubernetes](https://docs.akeyless.io/docs/sra-k8s-cluster)
- [Web Applications](https://docs.akeyless.io/docs/sra-web-applications)
- [kubectl](https://docs.akeyless.io/docs/kubectl-access)

## Web Access

Remote access to external software as a service systems can also be configured through the [Web Access Application](https://docs.akeyless.io/docs/sra-web-access-on-k8s). This supports browser-isolated access to approved web destinations and secure proxy mode for internal resources.

For details about the different remote access components, see [Setup Overview](https://docs.akeyless.io/docs/sra-setup-overview).
