---
title: Secret Types
excerpt: ''
deprecated: false
hidden: false
metadata:
  title: ''
  description: ''
  robots: index
next:
  description: ''
---
Akeyless enables you to work with the following secret types:

* **Static Secrets:** Key/value pairs that you create and update manually. The values usually remain the same for long periods. Typically, you use static secrets to protect passwords, API tokens, and personal identifiers (PII) or credit card numbers. See [Static Secrets](doc:static-secrets).

* **Dynamic Secrets**: Temporary credentials generated on-demand to provide a client with access to a resource for a limited period of time, with a limited set of permissions. See [Dynamic Secrets](https://docs.akeyless.io/docs/how-to-create-dynamic-secret).

* **Rotated Secrets**: Passwords for privileged-user accounts that are periodically updated by resetting a password on a target machine. The Akeyless Platform stores the updated secret value to retrieve it when required. see [Rotated Secrets](doc:rotated-secrets).

In addition, Akeyless enables you to work with:

* **Targets**: Targets act as a connector between credentials and the items that need to utilize them, both saving time for the user and protecting your flows from credential breakage. For more detail, see [Targets](doc:targets).

* **Encryption Keys**: AES, RSA, or EC keys of various sizes. Use these keys to encrypt secrets or any other kind of data and also to sign binaries or application transactions. See [Encryption Keys](doc:encryption-key-management-overview).

* **Certificates**: Akeyless acts as a Certificate Authority for the internal environment. Supporting both types of [PKI/TLS Certificates](doc:ssh-and-pkitls-certificates) and [SSH certificates](doc:how-to-configure-ssh).
