---
title: Overview
excerpt: Encryption & Key Management Overview
deprecated: false
hidden: false
metadata:
  title: ''
  description: ''
  robots: index
next:
  description: ''
---
The Akeyless Platform combines the capabilities of a Hardware Security Module (HSM) and a Key Management Service (KMS) with a built-in [KMIP Server](https://docs.akeyless.io/docs/kmip-server) to provide enhanced encryption key lifecycle management. You can generate, protect, rotate, and delete keys, as well as use them with Encryption-as-a-Service and Digital Signing functions.

There are two general types of keys available for creation and use:

* **Classic keys:** If you want to [Bring Your Own Key](https://docs.akeyless.io/docs/external-kms) to a cloud KMS provider, you can create it as a [Classic Key](https://docs.akeyless.io/docs/classic-keys). Once you share [Classic Keys](https://docs.akeyless.io/docs/classic-keys) with a cloud KMS, you can easily manage all your Keys directly from the Akeyless Platform while using them inside your cloud services directly from your Cloud KMS while simultaneously enjoying the security and centralized management provided by Akeyless. For more information, see [Classic Keys](https://docs.akeyless.io/docs/classic-keys).

* **DFC™ keys:** A key in Akeyless, by default, will be encrypted using Akeyless Distributed Fragments Cryptography™, our unique FIPS-certified encryption key management technology. With Akeyless DFC™, your encryption key is created as fragments across different regions and on different cloud providers. The key never exists as a whole, not even when it is used. For more information, see [Encryption Keys](https://docs.akeyless.io/docs/encryption-keys).

Each type has its own sub-types and unique uses that will be elaborated upon in their own pages.

# Tutorial

Check out our tutorial video on [Creating and Rotating Encryption Keys](https://tutorials.akeyless.io/docs/creating-and-rotating-encryption-keys).
