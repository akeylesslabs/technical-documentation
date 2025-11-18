---
title: Distributed Fragments Cryptography (DFC)
deprecated: false
hidden: false
metadata:
  robots: index
next:
  pages:
    - slug: dfc-deep-dive
      title: DFC Deep Dive
      type: basic
---
Distributed Fragments Cryptography (DFC) is the core cryptographic mechanism used by Akeyless to ensure that private key material and sensitive secret data are never stored, reconstructed, or exposed in complete form. DFC enables the platform to perform signing, encryption, decryption, and secret generation operations without holding a full private key at any stage.

DFC operates by dividing cryptographic material into independent fragments that are distributed across multiple isolated locations. Each fragment performs its portion of an operation, and the combined output is returned to the requesting client without any system ever assembling the full private key.

## Purpose of DFC

The primary purpose of DFC is to remove the need for centralized secret storage and to prevent unilateral access to sensitive key material. By ensuring that no single system or operator can access or reconstruct a complete private key, DFC provides strong separation of duties and minimizes risk from infrastructure compromise, insider threats, and privileged access.

DFC also enables Akeyless to deliver a Vaultless architecture, because private material does not need to be saved in a persistent store and is never available in full form.

## Fragment Distribution Model

DFC divides key material into multiple independent fragments. These fragments have the following properties:

* Each fragment is stored and used in isolation.
* No fragment contains enough information to derive the full key.
* Fragments never leave their assigned location.
* Fragments do not require synchronization, replication, or backup.
* One fragment may be optionally held and controlled by the customer.

When a customer chooses to control a fragment, the platform cannot perform cryptographic operations unless the customer fragment participates. This enforces distributed control across trust boundaries.

## Cryptographic Operation Flow

When a client initiates a cryptographic operation (such as signing, encryption, or dynamic secret generation), the following occurs:

1. **Client authentication and authorization** is performed by the Akeyless control plane.
2. The control plane determines which fragments must participate in the operation.
3. Each fragment holder performs its partial computation using its local fragment.
4. Partial results are returned to the control plane.
5. The control plane combines partial results into the final output _without reconstructing the private key_.
6. The result is returned to the requesting client.

Throughout this process:

* Full private key material never exists at rest or in memory on any system.
* Fragments are never transmitted across the network.
* No intermediate artifacts can be used to derive the complete key.

## Customer-Controlled Fragment

Customers may choose to operate one of the DFC fragments in their own environment. In this configuration:

* Akeyless cannot complete cryptographic operations without customer participation.
* Customers maintain guaranteed unilateral control of key usage.
* Compromise of the Akeyless service alone is insufficient to expose private material.
* The customer's fragment remains under their governance, keys, and lifecycle controls.

This configuration is typically deployed when organizations require full enforcement of separation-of-duties or must satisfy regulatory requirements related to key custody.

## Security Properties

DFC provides several well-defined security guarantees:

* **Non-reconstruction**: Full private keys are never assembled or exposed during any operation.
* **Distributed trust**: Multiple components must cooperate to complete a cryptographic operation.
* **Boundary isolation**: A compromise of any fragment holder yields no useful key information.
* **Optional customer custody**: Customers can enforce independent control of key usage.
* **No storage requirement**: No system stores private key material, eliminating traditional vault retrieval risks.

These properties hold regardless of the operation type, workload environment, or deployment model.

## Key Lifecycle

DFC supports the creation, rotation, and deactivation of cryptographic keys without reconstructing full key material. Lifecycle operations follow the same distributed flow:

* **Key creation** generates fragments independently across fragment holders.
* **Rotation** triggers creation of new fragments and retirement of old ones.
* **Revocation** disables the ability to perform future operations using a fragment set.

No single system ever has access to the full key during any lifecycle stage.

## Operational Considerations

DFC's distributed model affects system operations in several ways:

* Fragment holders do not require shared storage or synchronization.
* No backups, snapshots, or replication processes are needed for private material.
* Fragment holders must be reachable for cryptographic operations to complete.
* If a customer-controlled fragment is used, customer-side availability directly affects operation availability.
* Fragment compromise alone does not expose any sensitive key data.

Performance is primarily influenced by network latency between fragment holders rather than storage I/O.

## Supported Operations

DFC supports a broad set of operations used throughout the Akeyless platform:

* Secret generation and retrieval workflows
* Key-based signing and verification
* Encryption and decryption operations
* Certificate signing for PKI workflows
* SSH certificate issuance
* Dynamic secret generation
* Token issuance for identity-based access

In all cases, the same distributed principles apply.

## Summary

Distributed Fragments Cryptography (DFC) ensures that sensitive key material is never stored, reconstructed, or exposed in complete form. By splitting cryptographic material across isolated fragment holders—optionally including a customer-controlled fragment—DFC provides strong separation of duties and supports the Vaultless architecture used by Akeyless for secret, key, and certificate operations.