---
title: Authentication & Authorization
deprecated: false
hidden: false
link:
  new_tab: false
metadata:
  robots: index
next:
  pages:
    - slug: quickstarts
      title: Quickstarts
      type: basic
---
Akeyless uses a two-stage model to control access to secrets, keys, certificates, and other identity workflows: **authentication** and **authorization**. These stages determine _who_ is making the request and _what_ that identity is allowed to do.

***

## Authentication

Authentication verifies the identity of the user, service, workload, or machine attempting to access Akeyless. Akeyless supports several authentication methods that cover human identities, automated systems, and infrastructure components.

### Human Authentication

* **Username and Password**: Basic console access for administrators and users.
* **Single Sign-On (SSO)**: Authentication through identity providers using:
  * SAML 2.0
  * OpenID Connect (OIDC)
  * OAuth-based identity flows

### Machine and Workload Authentication

* **Access Keys**: Programmatic identities for automations and applications.
* **JWT-Based Authentication**: Trust established through external identity providers or platforms issuing signed tokens.
* **Kubernetes Authentication**: Pod identity validation through Kubernetes ServiceAccount tokens.
* **Cloud Provider Authentication**
  * AWS IAM
  * Azure AD Workload Identities
  * Google Cloud Workload Identity

***

## Authorization

Authorization determines _what an identity is allowed to do_ after it has been authenticated. In Akeyless, authorization is based on **roles and policies**.

### Role-Based Access Control (RBAC)

RBAC assigns permissions through **roles**. A role can specify:

* Which secrets, keys, or other items are accessible
* Which actions are permitted (read, write, list, rotate, delete)
* Whether access is limited to specific paths or namespaces

RBAC is the simplest and most common authorization model in Akeyless.

### Attribute-Based Access Control (ABAC)

ABAC evaluates **contextual attributes**, such as:

* Source IP address
* Time of day
* Environment or region
* Identity metadata or claims

ABAC policies allow dynamic, context-aware access decisions.

### Combined Policies

Akeyless allows RBAC and ABAC to be used together. For example:

* A role grants access to a secret.
* An ABAC policy restricts access to business hours.
* A context rule ensures requests must originate from a gateway inside a private network.

This layered approach provides strong access governance.

***

## Policy Enforcement

Policy enforcement happens at the **control plane**, but cryptographic operations (like signatures or decryptions) are only performed when both authentication and authorization succeed. Authorization applies to:

* Secrets and static values
* Dynamic and rotated credentials
* Certificates and SSH keys
* Encryption, decryption, and signing operations
* Gateway-proxied operations

All successful requests generate _audit events_ that can be viewed in the console or forwarded to SIEM systems.

***

## Summary

Authentication confirms the identity of the requester, while authorization determines what the identity is permitted to do. Together, these controls define how Akeyless manages access to secrets, keys, certificates, and cryptographic operations. This separation of responsibilities ensures strong security, clear governance, and consistent enforcement across cloud, on-premises, and hybrid environments.
