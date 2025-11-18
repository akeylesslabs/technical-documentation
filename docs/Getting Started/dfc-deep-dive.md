---
title: DFC Deep Dive
deprecated: false
hidden: true
metadata:
  robots: index
---
# Distributed Fragments Cryptography (DFC) — Deep Dive

This document provides a detailed technical explanation of how Distributed Fragments Cryptography (DFC) works, including key generation, fragment storage, operation flows, refresh mechanisms, and component responsibilities.

DFC is a distributed key management framework that ensures no complete private key ever exists on any server, at any time. All operations rely on cryptographic derivation across independent fragments.

---

## 1. Cryptographic Foundations

DFC uses standard, NIST-approved primitives:

* **AES** — symmetric encryption
* **HMAC** — message authentication and integrity
* **KDFs** — for deriving per-operation values from fragments
* **Hybrid TLS 1.3 (ML-KEM768 + X25519)** — post-quantum–resistant communication

DFC does not introduce new encryption algorithms; it introduces a new key-handling model.

---

## 2. System Components

### 2.1 Key Fragment Managers (KFMs)

KFMs are isolated microservices distributed across independent cloud providers and regions. Each KFM:

* Holds one encrypted key fragment in a dedicated encrypted datastore.
* Never exposes fragment values externally.
* Performs fragment-specific cryptographic derivations.
* Operates independently without communicating with other KFMs.
* Periodically refreshes its fragment value.

### 2.2 Unified Access Manager (UAM)

The UAM:

* Orchestrates key metadata, identities, and authorizations.
* Routes operation requests to all relevant KFMs.
* Does **not** store or access fragment values.
* Never participates in fragment derivation.

### 2.3 Customer Fragment (CF)

If enabled:

* A 256-bit fragment is generated client-side.
* It remains exclusively in the customer environment (e.g., HSM, on-prem, or private cloud).
* It is never transmitted to Akeyless.
* Operations cannot complete without CF participation.

### 2.4 Akeyless Gateway

The Gateway:

* Manages the Customer Fragment when applicable.
* Performs client-side assembly of derived keys.
* Caches non-sensitive metadata for performance.
* Remains stateless for sensitive data; no fragment material is persisted.

---

## 3. Key Generation Process

### 3.1 Distributed Fragment Creation

When a key is created:

1. Each KFM independently generates a fragment using secure randomness.
2. Fragments are stored only in their local encrypted datastore.
3. No KFM sees another KFM’s fragment.
4. No system ever holds or computes the full key.

Result:  
`Key = f(Fragment_A, Fragment_B, Fragment_C, [Customer Fragment])`  
where `f()` is a one-way mathematical relationship established by distributed KDF operations.

### 3.2 Fragment Storage Characteristics

* Stored only at the KFM that generated it.
* Encrypted at disk and application level.
* Not replicated or synchronized.
* Not shared between components.
* Not transmitted during operation flows.

---

## 4. Cryptographic Operation Flow

This applies to operations such as encryption, decryption, signing, HMAC, or secret generation.

### Step-by-Step

1. **Client authenticates** to Akeyless.
2. **UAM authorizes** the operation and locates the relevant fragment holders.
3. **Parallel fragment derivation:**
   * Each KFM applies a KDF to its local fragment.
   * The customer environment applies KDF to the Customer Fragment (if present).
4. **Derivation aggregation:**
   * Partial derivations are returned.
   * The client (or Gateway) mathematically combines them into a **one-time derived key**.
5. **Operation execution:**
   * The derived key is used for the requested operation.
   * The derived key is then immediately discarded.

### Key Properties

* The original key is never reconstructed.
* Derivations do not reveal fragment values.
* Derivations cannot be reused.
* The derived key exists only ephemerally, on the client side.

---

## 5. Fragment Refreshing

Fragments are periodically refreshed to prevent long-term exposure.

### How Refresh Works

Each KFM:

1. Computes a new fragment value `Fragment'`.
2. Ensures that the mathematical relationship across all fragments still satisfies the original key value.
3. Writes the updated fragment to its encrypted datastore.
4. Performs refresh independently—no coordination between KFMs.

### Security Effect

An attacker must compromise **all fragments simultaneously**, within the same refresh window.  
This requirement is considered infeasible due to:

* geographic distribution  
* multi-cloud separation  
* independent environments  
* asynchronous refresh cycles  

---

## 6. Zero-Knowledge Architecture

DFC enables a true zero-knowledge model:

* Akeyless cannot decrypt customer data.
* Cloud providers hosting KFMs cannot reconstruct the key.
* Attackers compromising any single component gain no useful information.
* Customer-controlled fragments ensure that operations cannot occur without customer participation.

---

## 7. Post-Quantum Protections

DFC incorporates post-quantum cryptography in the transport layer:

* TLS 1.3 hybrid mode  
* ML-KEM768 (NIST PQC standard) + X25519  
* Forward secrecy and resistance to quantum attacks

This protects fragment derivation operations during transit.

---

## 8. Threat Model Characteristics

DFC mitigates the following risks:

* Storage-layer compromise of secrets  
* Insider access to reconstructed private keys  
* Lateral movement across components  
* Cloud provider access to encryption keys  
* Multi-tenant SaaS exposure  
* Quantum-era decryption of captured communications

DFC does **not** rely on:

* Shamir Secret Sharing  
* Threshold crypto requiring key reconstruction  
* Centralized vault storage

---

## 9. Operational Considerations

* Fragments must be reachable for operations to complete.
* Gateway availability affects CF-based operations.
* No backups or replication are required for fragments.
* No rotation of storage-level secrets is needed; refresh cycles replace them.

---

## 10. Supported Operation Types

DFC supports:

* Encryption and decryption  
* Signing and verification  
* HMAC  
* Certificate signing (PKI)  
* SSH key signing  
* Dynamic secret derivation  
* Token generation

All operations employ the same distributed derivation model.

---

## Summary

DFC provides a distributed, non-reconstructive key management model that ensures private keys never exist in full form. Through isolated fragment storage, independent KFMs, KDF-based derivation, optional Customer Fragment control, and continuous refresh cycles, DFC enables Akeyless to deliver secure key operations without relying on vault storage or centralized secrets.
