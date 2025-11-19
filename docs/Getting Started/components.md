---
title: Platform Components Overview
deprecated: false
hidden: false
metadata:
  robots: index
---
This page describes the main components that make up the Akeyless platform and how they interact. Understanding these pieces helps clarify where operations run, which parts are under customer control, and how responsibilities are divided between Akeyless and the customer.

At a high level, the platform consists of:

- The **Akeyless Platform** (SaaS control plane)
- Internal **Key Fragment Managers (KFMs)** and the **Unified Access Manager (UAM)**
- The **Akeyless Gateway** (deployed in customer environments)
- **Connectors** and **Targets** for external systems
- **Client tools** (CLI, SDKs, and APIs)
- An optional **Customer Fragment (CF)** component in the customer environment

DFT (Distributed Fragments Cryptography) and the Vaultless architecture are implemented across these components. This page focuses on roles and boundaries rather than cryptographic details.

## Akeyless Platform (SaaS Control Plane)

The Akeyless Platform is a multi-tenant, cloud-hosted control plane operated by Akeyless. It is responsible for:

- Authenticating users, services, and workloads
- Evaluating authorization policies (RBAC and ABAC)
- Managing metadata for keys, secrets, and certificates
- Orchestrating cryptographic operations using DFC
- Providing administration interfaces (UI, API) and audit visibility

Key responsibilities:

- Receive requests from client tools or gateways
- Validate identity and permissions
- Route cryptographic operations to internal components (KFMs)
- Record relevant audit events and metrics

The Akeyless Platform does **not** store complete private keys or full secret values in a retrievable form. Key material is managed through DFC and fragments held in KFMs and, optionally, customer-owned environments.

## Unified Access Manager (UAM)

The Unified Access Manager is an internal service within the Akeyless Platform that coordinates access and operations. UAM:

- Holds logical information about keys, secrets, and configurations (IDs, metadata, policies)
- Makes authorization decisions based on configured policies
- Routes operation requests to the appropriate Key Fragment Managers
- Does not hold or process fragment values

UAM knows *which* fragments are required for a given operation, not *what* those fragments are.

## Key Fragment Managers (KFMs)

Key Fragment Managers are internal microservices that implement Distributed Fragments Cryptography. Each KFM:

- Holds a single encrypted fragment of a key in its own isolated datastore
- Runs in a separate cloud region or provider to maintain isolation
- Performs local fragment derivation when requested by UAM
- Never exposes its fragment value or communicates with other KFMs
- Periodically refreshes its fragment values to reduce long-term exposure

KFMs are not directly accessible to customers. All interaction is mediated by the Akeyless Platform.

## Akeyless Gateway

The Akeyless Gateway is a lightweight component deployed in the customer’s environment (for example, in a VPC, data center, or Kubernetes cluster). It is used when:

- Accessing resources that are not reachable from the public internet
- Integrating with private databases, services, or infrastructure
- Using an optional Customer Fragment (CF) for zero-knowledge configurations
- Reducing latency by keeping some logic closer to workloads

The Gateway:

- Accepts requests from local clients or applications
- Forwards authenticated and authorized operations to the Akeyless Platform
- Optionally manages the Customer Fragment and performs local derivation of one-time keys
- Caches **non-sensitive** metadata for performance, but does not persist secrets, full keys, or cryptographic fragments

The Gateway extends reach and performance but does not hold full secret or key material and does not break the Vaultless design.

## Customer Fragment (CF) (Optional)

When zero-knowledge and customer-controlled key custody are required, a Customer Fragment can be enabled:

- The CF is generated and stored in the customer environment (for example, HSM, private cloud, or on-premises infrastructure).
- It is never sent to Akeyless.
- Akeyless cannot complete cryptographic operations that depend on that key without the CF.

In typical deployments, the Gateway coordinates access to the CF, deriving values that are combined with derivations from KFMs to produce a one-time derived key used for a single operation.

## Connectors and Targets

Connectors and targets are configuration objects that define how Akeyless interacts with external systems. They are used for:

- Dynamic secrets (e.g., database credentials, cloud IAM credentials)
- Secrets rotation (e.g., rotating passwords in databases or cloud services)
- Encryption key usage for external storage or services

Common examples:

- Database targets (PostgreSQL, MySQL, MSSQL, etc.)
- Cloud provider targets (AWS, Azure, GCP)
- Directory or identity provider targets (LDAP, Active Directory)
- Other application or service targets

Connectors use credentials or identities configured by the customer. Akeyless uses these configurations to perform operations on the customer’s behalf, without exposing underlying secrets to callers.

## Client Tools

Client tools are how users and workloads interact with Akeyless. They include:

- **Web Console**: Browser-based UI for administration, configuration, and monitoring.
- **CLI**: A command-line interface for scripting, local development, and operational tasks.
- **SDKs**: Language-specific SDKs (for example, Go, Python, Java, JavaScript) used by applications and automation.
- **REST API**: The core HTTP API used by tools, SDKs, and integrations.

Clients can connect directly to the Akeyless Platform or, in some environments, to the Gateway, which then forwards requests.

## Logical Flow Between Components

A typical operation such as “encrypt data with a key” involves:

1. A client (CLI, SDK, or application) sends a request to the Akeyless Platform or Gateway.
2. The Platform (via UAM) authenticates the caller and checks policies.
3. UAM dispatches derivation requests to KFMs holding relevant key fragments.
4. KFMs perform local derivations and return partial results.
5. If configured, the Gateway or customer-side component uses the Customer Fragment to derive an additional value.
6. The Gateway or client combines derivations to compute a one-time derived key and performs the cryptographic operation.
7. The derived key is discarded, and the result (for example, ciphertext or signature) is returned to the client.

Throughout this process, full key material never exists on any single component.

## Summary

The Akeyless platform is composed of a cloud-hosted control plane, internal cryptographic services, and optional customer-deployed components such as the Gateway and Customer Fragment. Together, these components implement the Vaultless architecture and Distributed Fragments Cryptography, allowing secrets, keys, and certificates to be used without storing or reconstructing complete key material.
