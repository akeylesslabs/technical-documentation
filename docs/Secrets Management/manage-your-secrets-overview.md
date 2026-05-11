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
Akeyless supports several item types for storing, generating, protecting, and distributing sensitive data.

## Secret Types

Use these secret types to manage application and user credentials:

* **Static Secrets**: Key/value pairs that you create and update manually. Use them for values that change infrequently, such as passwords, API tokens, personal identifiers, or credit card numbers. Akeyless also provides dedicated [Password](https://docs.akeyless.io/docs/passwords) items for username, password, and website credentials. See [Static Secrets](https://docs.akeyless.io/docs/static-secrets).

* **Dynamic Secrets**: Temporary credentials generated on demand for a limited time and with a limited set of permissions. See [Dynamic Secrets](https://docs.akeyless.io/docs/how-to-create-dynamic-secret).

* **Rotated Secrets**: Passwords for privileged accounts that Akeyless updates periodically by resetting the password on the target system. The platform stores the latest value so you can retrieve it when needed. See [Rotated Secrets](https://docs.akeyless.io/docs/rotated-secrets).

## Supporting Objects

Akeyless also provides supporting objects that help you deliver secrets securely and consistently:

* **Targets**: Targets connect credentials to the systems that consume them. This helps you reuse endpoint details across secrets and reduces the risk of credential drift. See [Targets](https://docs.akeyless.io/docs/targets).

* **Encryption Keys**: AES, RSA, or EC keys that you can use to encrypt data or sign binaries and application transactions. See [Encryption Keys](https://docs.akeyless.io/docs/encryption-key-management-overview).

* **Certificates**: Akeyless can act as a certificate authority for internal environments, supporting both [PKI/TLS Certificates](https://docs.akeyless.io/docs/ssh-and-pkitls-certificates) and [SSH certificates](https://docs.akeyless.io/docs/sra-ssh-certificates).
