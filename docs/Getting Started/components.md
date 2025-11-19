---
title: Platform Components Overview
deprecated: false
hidden: false
metadata:
  robots: index
---
The Akeyless platform is composed of several components that work together to provide identity security services without storing or reconstructing full private keys or long-lived secrets. This page describes each component’s role at a high level.

## High-Level Components

* **Akeyless Platform** (SaaS control plane)
* Internal **Key Fragment Managers (KFMs)** and the **Unified Access Manager (UAM)**
* **Akeyless Gateway** (customer-deployed)
* **Connectors** and **Targets**
* **Client Tools** (CLI, SDKs, API)
* Optional **Customer Fragment (CF)** in the customer environment

Distributed Fragments Cryptography (DFC) and the Vaultless architecture are implemented across these components but are described in detail on their dedicated pages.

***

## Akeyless Platform (SaaS Control Plane)

The Akeyless Platform is the cloud-hosted control plane that coordinates identity operations. It is responsible for:

* Authenticating users, services, and workloads
* Evaluating authorization policies (RBAC and ABAC)
* Managing metadata for keys, secrets, and certificates
* Orchestrating cryptographic operations using DFC
* Providing administrative interfaces (UI, API)
* Recording audit events and operational metrics

Key characteristics:

* The platform never stores complete private keys or full secrets in a retrievable form.
* It routes cryptographic operations but does not perform fragment-level derivation.
* All sensitive key material stays within KFMs or customer-controlled environments.

***

## Unified Access Manager (UAM)

The Unified Access Manager coordinates authorization and routing for cryptographic operations:

* Maintains logical metadata for keys, roles, and policies
* Authorizes operations based on identity, policy, and context
* Dispatches derivation requests to the appropriate KFMs
* Does **not** hold fragment values or perform fragment-level computation

UAM knows _which fragments_ participate in an operation, not _the fragment data itself_.

***

## Key Fragment Managers (KFMs)

KFMs are internal services responsible for holding and processing key fragments.

Each KFM:

* Stores one encrypted key fragment in its own isolated datastore
* Runs in an independent region or cloud provider to ensure environmental separation
* Performs fragment-specific derivation operations when requested
* Never shares fragment values or communicates with other KFMs
* Refreshes its fragment values periodically

KFMs are not customer-facing. All access is mediated through the Akeyless Platform.

***

## Akeyless Gateway

The Akeyless Gateway is an optional, lightweight component deployed within the customer environment. It is commonly used for:

* Accessing private networks or internal systems
* Integrating with on-premises databases, directories, or services
* Participating in operations that use a Customer Fragment
* Reducing latency by keeping derivation and request handling close to workloads

Gateway characteristics:

* Performs local combination of fragment derivations when a CF is present
* Caches **non-sensitive** metadata to improve performance
* Does **not** store secrets, private keys, or cryptographic fragments
* Can run in constrained or air-gapped environments

***

## Customer Fragment (CF)

Optionally, a Customer Fragment can be enabled when organizations require customer-controlled key custody.

The CF:

* Is generated and stored entirely within the customer environment
* Is never transmitted to Akeyless
* Must participate in any operation involving its associated key

When a CF is used, the Gateway manages CF access and combines CF-derived values with derivations from KFMs.

***

## Connectors and Targets

Connectors and targets define how Akeyless interacts with external systems. They support:

* Dynamic secrets (e.g., cloud IAM credentials, database credentials)
* Secrets rotation (e.g., rotating passwords, tokens, or access keys)
* Use of Akeyless-managed encryption keys in external services

Examples include:

* Cloud provider targets (AWS, Azure, GCP)
* Database targets (PostgreSQL, MySQL, MSSQL)
* Directory services (LDAP, Active Directory)
* Application or service-specific integrations

Connectors rely on customer-supplied identities or credentials. These identities are used only by the connector; callers never receive them directly.

***

## Client Tools

Client tools are used by applications, automation systems, and administrators to interact with Akeyless services.

Available tools include:

* **Web Console** — UI for configuration, access control, and monitoring
* **CLI** — Command-line interface for administrative and operational tasks
* **SDKs** — Language clients (Go, Python, Java, JavaScript, etc.)
* **REST API** — Core entry point for programmatic access

Clients may communicate directly with the Akeyless Platform or through the Gateway.

***

## Logical Flow Between Components (High-Level)

A typical cryptographic or secret-management request works as follows:

1. A client sends a request to the Akeyless Platform or through the Gateway.
2. UAM authenticates the caller and evaluates authorization policies.
3. UAM dispatches fragment-derivation requests to relevant KFMs.
4. KFMs return fragment-derived values.
5. If a Customer Fragment is configured, the Gateway derives a customer-side value.
6. The Gateway or client assembles a one-time derived key and completes the requested operation.
7. Derived key material is discarded immediately after use.

This workflow maintains the Vaultless and non-reconstructive guarantees of the platform.

***

## Summary

The Akeyless platform consists of cloud-hosted control-plane services, internal fragment managers, and optional customer-deployed components. Each component has a clearly defined role, and none of them—individually or collectively—store or reconstruct full private keys. Together, they implement the Vaultless model and Distributed Fragments Cryptography used for secure, scalable identity operations.
