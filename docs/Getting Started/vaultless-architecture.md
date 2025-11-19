---
title: Vaultless SaaS Architecture
deprecated: false
hidden: false
metadata:
  robots: index
next:
  pages:
    - slug: dfc-overview
      title: Distributed Fragments Cryptography (DFC)
      type: basic
---
Akeyless uses a Vaultless architecture to perform secret, key, and certificate operations without storing sensitive material in a retrievable form. This model removes the storage layer that traditional vault systems depend on and instead relies on distributed cryptographic operations to process identity-related workflows.

The architecture is designed to ensure that no complete secret or private key is ever present at rest within the platform.

## Architecture Overview

Traditional vault systems maintain an encrypted database that stores secrets or private keys. Akeyless replaces this model with an execution-based approach that relies on Distributed Fragments Cryptography (DFC). Instead of retrieving stored material, the platform performs cryptographic operations on demand using distributed fragments that never combine into a full key.

**Core architectural characteristics:**

* No backend storage of secrets, private keys, or credential material.
* No replication, synchronization, or database maintenance.
* No persistence of cryptographic fragments in any single location.
* Optional customer-held fragment prevents unilateral access.

All operations (such as signing, encryption, decryption, rotation, or secret generation) are executed without reconstructing full private key material inside any system component.

## Cryptographic Workflow

When a client requests an operation (for example, retrieving a secret, generating a dynamic credential, or performing a signing operation), the following occurs:

1. The request is authenticated and authorized by the Akeyless control plane.
2. The platform initiates a distributed cryptographic workflow.
3. Each fragment-holding node performs its portion of the operation.
4. Partial cryptographic results are combined into a usable output without exposing complete key material.
5. No fragment or reconstructed secret is stored or written to disk.

If the customer chooses to hold one of the fragments, the platform cannot complete operations unless the customer-controlled fragment participates. This enforces separation of duties and ensures that private material cannot be reconstructed by Akeyless staff or infrastructure.

## Comparison to Storage-Based Vault Systems

Traditional vaults:

* Store secrets and keys in encrypted form.
* Require a storage backend, replication strategy, and access controls.
* Must decrypt or reconstruct key material for certain operations.
* Are susceptible to compromise of stored secrets if the storage or master key is exposed.

In contrast, the Vaultless model:

* Does not store secrets or keys.
* Does not reconstruct key material during operations.
* Does not require storage-related operations like backups or database maintenance.
* Prevents retrieval attacks because no stored material exists.

This changes the threat model: attackers cannot exfiltrate stored secrets because none are present.

## Gateway Role

The Akeyless Gateway is used to access private networks or environments that cannot connect directly to the Akeyless service. The gateway does not store secrets or cryptographic fragments.

**Characteristics:**

* Stateless operation.
* No caching or persistence of sensitive material.
* Participates in distributed cryptographic operations only for authorization or connectivity purposes.
* Can be deployed in air-gapped or restricted environments.

The gateway extends connectivity but does not alter the Vaultless model.

## Operational Considerations

Removing the storage layer affects operational responsibilities in several ways:

* No key vault to deploy, patch, or maintain.
* No backups or replication mechanisms.
* No database recovery or migration tasks.
* No concerns related to storage compromise, disk forensics, or data exfiltration from a backend.

Capacity and performance planning are based on request throughput rather than storage scaling.

## Security Properties

Key security properties of the Vaultless architecture:

* **Non-reconstruction**: Full private keys are never assembled at runtime.
* **Non-persistence**: No sensitive material is written to disk on any component.
* **Fragment separation**: Each fragment exists only within its assigned node.
* **Customer fragment control (optional)**: Customers may control one fragment, preventing unilateral operations.
* **Isolation**: A compromise of any single fragment does not reveal usable key material.

These properties reduce the exposure surface associated with secret storage and retrieval systems.

## Summary

The Akeyless Vaultless architecture removes the need for a secrets or key storage backend by executing operations through distributed cryptographic fragments. No secret or private key is stored or fully reconstructed at any time. This model provides a predictable, storage-free way to manage secrets, keys, and certificates across distributed systems.