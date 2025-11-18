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
Distributed Fragments Cryptography (DFC) is the cryptographic framework that enables Akeyless to perform secret, key, and certificate operations without ever storing or reconstructing complete private key material. Instead of placing full keys in a vault or database, DFC divides key material into multiple fragments and performs cryptographic operations directly across those fragments.

DFC supports the Vaultless architecture by ensuring that no complete encryption key exists on any server, at any point.

## Core Concepts

DFC splits an encryption key into multiple mathematical fragments. These fragments:

* Are created independently across isolated environments.
* Never combine into a full key, including during key generation or use.
* Can optionally include a Customer Fragment (CF), held exclusively by the customer.
* Are processed independently using standard, NIST-approved cryptographic primitives.

The complete key is never assembled. Instead, cryptographic operations are completed by combining mathematical derivations from each fragment, resulting in a short-lived, derived key used only for a single operation.

## How Operations Work

At a high level:

1. A client requests an operation such as encryption, decryption, signing, or key-based secret generation.
2. Each fragment holder computes a partial derivation using its fragment.
3. These derivations are combined into a one-time-use derived key on the client side (or on the customer's Gateway when using a Customer Fragment).
4. The derived key is used for the requested operation and then discarded.

At no point is the original key constructed or exposed.

## Customer Fragment (CF)

Organizations may hold one of the key fragments in their own environment. When used:

* The platform cannot perform operations unless the CF participates.
* The customer maintains exclusive control over key usage.
* No entity—including Akeyless—can derive or reconstruct the key without the CF.

This enforces separation of duties and supports regulated environments requiring customer-held key material.

## Fragment Refreshing

DFC includes built-in fragment refreshing:

* Fragment values are periodically updated.
* The mathematical relationship between fragments remains constant.
* No downtime or operational changes are required.

This refresh mechanism makes long-term exposure of a fragment insufficient to compromise the key.

## Cryptographic Foundations

DFC relies on standard, NIST-approved algorithms:

* AES for symmetric encryption
* HMAC for integrity
* KDFs for fragment derivation
* Hybrid TLS 1.3 with ML-KEM768 and X25519 for post-quantum protection (communication layer)

No proprietary encryption algorithms are introduced; only the key-handling model is unique.

## Summary

DFC provides the foundation for Akeyless’s Vaultless architecture by ensuring that complete key material never exists on any server. By performing cryptographic operations directly on independent fragments, including optionally a Customer Fragment, Akeyless enforces strict separation of duties, reduces exposure, and removes the need for sensitive data storage.
