---
title: SRA Overview
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

Secure Remote Access (SRA) is Akeyless's modern Privileged Access Management (PAM) solution. it gives users just-in-time, zero-trust access to your infrastructure, without ever exposing credentials to the user. Every connection is brokered by the Akeyless Gateway, so access stays temporary, tightly scoped, and fully auditable.

## How It Works

1. **Authenticate**: Users sign in once through their existing identity provider (SAML, OIDC, LDAP, or certificate-based auth), from whichever access point fits their workflow (see _Ways to Access_ below).
2. **Authorize**: Akeyless checks the user's role-based access control (RBAC) policies to determine exactly which resources they are authorized to access..
3. **Connect**: The user picks a target from the supported resource types.
4. **Access, Just-in-Time**: SRA generates short-lived credentials on the fly, via Dynamic Secrets (temporary accounts) or Rotated Secrets (existing credentials that cycle automatically after disconnect), and the Gateway proxies the session directly to the target, injecting the credential automatically. The user never sees, copies, or handles the real credential.<br />

![Akeyless Gateway and Secure Remote Access architecture](https://files.readme.io/e02b0e922edccd3c72e9224cc5c6983b7db67dcfe164b1efedcc726777437586-Screenshot_2025-06-27_at_19.25.39.png)

<br />

## Key Features&#x20;

- **Zero Trust by design**: users never see or touch real credentials. Every connection is brokered and injected by the Gateway.
- **Just-in-time access**: credentials are generated per session and expire automatically. There's no standing access and no long-lived secrets.
- **Full session auditing and recording**: every session is logged, with video recording for RDP and web sessions along with transcripts for SSH, supporting compliance and forensic review.
- **Session revocation on demand**: administrators can terminate an active session at any time, cutting off access immediately if something looks wrong.
- **Request and approval workflows**: access can be granted on demand with time-limited grants instead of always-on permissions.
- **File transfer via SFTP**: upload and download to protected targets over the same brokered, certificate-based tunnel, no local keys, no standing credentials.

## Ways to Access

All access methods below connect through your deployed Akeyless Gateway. They differ only in where the user-facing client lives.

- **Gateway-hosted Portal**: the web portal runs directly on your deployed Akeyless Gateway.
- **Public [SRA Portal](https://docs.akeyless.io/docs/sra-portal#connect-from-the-secure-remote-access-portal)**: Akeyless hosts the portal UI for you, but access still routes through your deployed Gateway.
- **Desktop Application**: a native app installed on the user's machine. The Akeyless Desktop app creates the connection locally and routes it through your deployed Gateway.
- **Akeyless CLI**: scriptable, terminal-based access, also routed through your deployed Gateway.

## Supported Resources

SRA supports secure access to: Databases, Windows Remote Desktop, AWS Console, Azure Portal, GCP Portal, SSH Servers, LDAP, RabbitMQ, Kubernetes, Web Applications, and kubectl. See [Supported Resource Types ](https://docs.akeyless.io/docs/sra-resource-types)for setup details on each.

## Next Steps

- New to SRA? Start with the Quick Start Guide, the fastest path to a working deployment.
- Choosing the right setup for your environment? See [SRA Setup](doc:sra-setup-overview) for deployment guides tailored to each supported environment (Kubernetes, Docker Compose).
- Need to configure access to a specific resource? Jump to [Supported Resource Types](doc:sra-resource-types).

<br />

<br />
