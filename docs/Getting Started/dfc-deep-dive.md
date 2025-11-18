---
title: DFC Deep Dive
deprecated: false
hidden: true
metadata:
  keywords:
    - distributed fragment cryptography
  robots: index
---
This document provides a detailed technical explanation of how Distributed Fragments Cryptography (DFC) works, including key generation, fragment storage, operation flows, fragment refreshing, cryptographic foundations, and component responsibilities.

DFC is a distributed key management framework that ensures no complete private key ever exists on any server, at any time. All operations rely on cryptographic derivation across independent fragments.

<br />

<br />

```mermaid
sequenceDiagram
    autonumber
    participant C as Client
    participant G as Akeyless Gateway<br/>(Customer Env)
    participant U as UAM<br/>(Unified Access Manager)
    participant K1 as KFM A<br/>(Fragment A)
    participant K2 as KFM B<br/>(Fragment B)
    participant K3 as KFM C<br/>(Fragment C)
    participant CF as Customer Fragment<br/>(CF Store)

    Note over C,G: 1. Client requests crypto operation<br/>(e.g., encrypt, decrypt, sign)
    C->>G: Authenticated request<br/>(operation + key ID)
    G->>U: Forward request<br/>(with client identity/context)

    Note over U: 2. Authorization and routing
    U->>U: Authorize request<br/>(policies, roles, attributes)
    U->>K1: Operation request for key ID<br/>(derive fragment value)
    U->>K2: Operation request for key ID<br/>(derive fragment value)
    U->>K3: Operation request for key ID<br/>(derive fragment value)

    Note over K1,K2,K3: 3. Local fragment derivation<br/>(no fragment leaves KFM)
    K1-->>U: Partial derivation dA
    K2-->>U: Partial derivation dB
    K3-->>U: Partial derivation dC

    Note over U,G: 4. UAM returns derivations<br/>without fragment values
    U-->>G: {dA, dB, dC}

    alt Customer Fragment enabled
        Note over G,CF: 5. CF derivation in customer environment
        G->>CF: Request CF derivation for key ID
        CF-->>G: dCF
    else No Customer Fragment
        Note over G: 5. No CF; use platform-only fragments
    end

    Note over G: 6. Local combination into one-time derived key<br/>K_derived = f(dA, dB, dC, [dCF])
    G->>G: Compute K_derived<br/>(ephemeral, not stored)

    Note over G: 7. Execute crypto operation with K_derived
    G->>G: Perform encrypt/decrypt/sign using K_derived
    G->>C: Return operation result
    G->>G: Discard K_derived

    Note over K1,K2,K3,CF: Fragments remain stored only<br/>in their isolated locations<br/>and are never exposed or combined

```

***

## 1. Cryptographic Foundations

DFC uses standard, NIST-approved primitives:

* **AES** — symmetric encryption
* **HMAC** — message authentication and integrity
* **KDFs** — for deriving per-operation values from fragments
* **Hybrid TLS 1.3 (ML-KEM768 + X25519)** — post-quantum–resistant communication

DFC does not introduce new encryption algorithms; it introduces a new key-handling and fragmentation model.

***

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

***

## 3. Key Generation Process

### 3.1 Distributed Fragment Creation

When a key is created:

1. Each KFM independently generates a fragment using secure randomness.
2. Fragments are stored only in their local encrypted datastore.
3. No KFM sees another KFM’s fragment.
4. No system ever holds or computes the full key.

Result:  
`Key = f(Fragment_A, Fragment_B, Fragment_C, [Customer Fragment])`  
where `f()` is a one-way mathematical relationship established by KDF operations.

### 3.2 Fragment Storage Characteristics

* Stored only at the KFM that generated it.
* Encrypted at disk and application level.
* Not replicated or synchronized.
* Not transmitted during operation flows.

***

## 4. Cryptographic Operation Flow

This applies to operations such as encryption, decryption, signing, HMAC, or secret generation.

### Step-by-Step

1. **Client authenticates** to Akeyless.
2. **UAM authorizes** the operation.
3. **Parallel fragment derivation:**
   * Each KFM applies a KDF to its local fragment.
   * If present, the customer environment applies KDF to the Customer Fragment.
4. **Derivation aggregation:**
   * Partial derivations are returned.
   * The client (or Gateway) combines them into a **one-time derived key**.
5. **Operation execution:**
   * The derived key is used once for the requested operation and then discarded.

### Key Properties

* The original key is never reconstructed.
* Derivations do not reveal fragment values.
* Derived keys cannot be reused.
* No fragment leaves its environment.

***

## 5. Fragment Refreshing

DFC includes continuous fragment refreshing to reduce exposure duration.

### How Refresh Works

Each KFM:

1. Computes a new fragment value `Fragment'`.
2. Ensures the new fragment set still resolves mathematically to the original key.
3. Updates the fragment in its encrypted datastore.
4. Operates independently—no coordination with other KFMs.

### Security Impact

An attacker must compromise all fragments **within the same refresh interval** to have any chance of deriving a key—an infeasible requirement due to:

* geographic distribution
* multi-cloud isolation
* independent refresh timing
* separate operational domains

***

## 6. Zero-Knowledge Architecture

DFC enables a zero-knowledge model:

* Akeyless cannot decrypt customer data.
* Cloud providers hosting KFMs cannot reconstruct the key.
* Customer Fragment prevents unilateral operations.
* Compromise of a single component yields no meaningful key information.

***

## 7. Post-Quantum Protections

DFC uses hybrid TLS 1.3 with:

* **ML-KEM768** (NIST PQC KEM)
* **X25519** (classical elliptic curve)

This provides protection against future quantum attacks on captured traffic.

***

## 8. Operational Considerations

* Fragment holders must be reachable for operations.
* Gateway availability is required for CF-based operations.
* No backups or replication are required for fragments.
* Fragment refreshing replaces the need for secret rotation at storage level.

***

## 9. Supported Operation Types

DFC supports:

* Encryption and decryption
* Signing and verification
* HMAC
* Certificate signing (PKI)
* SSH key signing
* Dynamic secret derivation
* Token generation

***

## Summary

The DFC deep-dive model shows how Akeyless performs distributed, non-reconstructive cryptographic operations using independent fragments, optional customer participation, continuous refresh cycles, and NIST-approved primitives. Keys are never stored or reconstructed, enabling secure and verifiable operations across distributed environments.
