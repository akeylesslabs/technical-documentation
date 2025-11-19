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
Akeyless uses a Vaultless architecture to perform secret, key, and certificate operations without storing sensitive material in a retrievable form. Instead of relying on a storage backend, operations are executed through distributed cryptographic workflows that never reconstruct full private key material. This eliminates the risks associated with stored secrets and removes the need to maintain vault servers or encrypted databases.

The architecture ensures that no complete secret or private key is ever present at rest within the platform.

## Architecture Overview

Traditional vault systems maintain encrypted storage that contains secrets or private keys. Akeyless replaces this model with an execution-based approach built on Distributed Fragments Cryptography (DFC). In this model:

* Sensitive key material is represented as independent fragments.
* Fragments remain confined to their respective locations.
* Cryptographic operations use fragment-derived values rather than reconstructing a full key.

The result is an architecture where cryptographic operations occur without persisting or retrieving complete secrets or private keys.

**Core architectural characteristics:**

* No storage of full secrets, private keys, or reconstructable credential material.
* No database to replicate, synchronize, or back up.
* Fragment values remain isolated in their assigned locations.
* Optional customer-held fragment enforces separation of control.

All identity operations—such as signing, encryption, decryption, or generating short-lived credentials—are completed without assembling full private key material at any stage of the workflow.

## Cryptographic Workflow

When a client requests an operation (e.g., retrieving a secret, generating a dynamic credential, or performing a signing operation):

1. The Akeyless control plane authenticates and authorizes the request.
2. The platform triggers a distributed cryptographic workflow based on the key or secret type.
3. Each participating fragment holder processes its own fragment and returns a derived value.
4. Derived values are combined to produce an operation-specific result without exposing complete key material.
5. No reconstructed secret or private key is written to disk or retained after the operation.

If a Customer Fragment (CF) is configured, Akeyless cannot complete cryptographic operations without the customer's involvement.

## Comparison to Storage-Based Vault Systems

Traditional vaults:

* Store secrets and keys in encrypted form.
* Require a persistent storage backend, backup strategy, and replication.
* Often decrypt or reassemble keys during operations.
* Are vulnerable if the storage or master key is compromised.

Under the Vaultless model:

* Secrets and keys are **not stored** and cannot be retrieved.
* Key material is **never reconstructed** during operation execution.
* No storage lifecycle tasks (backups, snapshots, migrations) are required.
* Retrieval attacks are not possible because no recoverable material exists.

This changes the threat model: compromising the storage layer yields no useful data because none is kept there.

## Gateway Role

The Akeyless Gateway provides access to private networks, closed environments, and on-premises infrastructure. Its role is limited to communication and optional customer-fragment participation. The Gateway:

* Does not store secrets or cryptographic fragments.
* May cache **non-sensitive metadata** for performance, but never key material or secret values.
* Remains stateless with respect to sensitive data.
* Can be deployed in restricted, air-gapped, or isolated environments.

The Gateway does not alter the Vaultless architecture; it only extends access to networks not reachable by the SaaS control plane.

## Operational Considerations

Removing the storage layer eliminates several operational concerns:

* No vault servers to deploy, patch, or maintain.
* No backups or replication mechanisms for stored secrets.
* No need for database migration or recovery processes.
* Reduced exposure to storage compromise, disk forensics, or exfiltration attacks.

Capacity planning focuses on request throughput rather than storage performance.

## Security Properties

Key security properties of the Vaultless architecture include:

* **Non-reconstruction** — Full private keys never exist in memory on any single component.
* **Non-persistence** — Sensitive material is never written to disk.
* **Fragment isolation** — Fragment values exist only within their respective fragment holders.
* **Optional customer control** — A customer-held fragment prevents unilateral operation execution.
* **Compartmentalization** — Compromise of any single component yields no usable key information.

These properties reduce the exposure surface associated with stored-secret systems.

## Summary

The Akeyless Vaultless architecture removes the need for a secrets or key storage backend by executing operations entirely through distributed cryptographic fragments. No secret or private key is stored or reconstructed at any time. This model provides a predictable, storage-free approach to managing secrets, keys, and certificates across distributed environments.
