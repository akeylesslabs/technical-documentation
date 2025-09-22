---
title: External KMS Integration
excerpt: ''
deprecated: false
hidden: false
metadata:
  title: ''
  description: ''
  robots: index
next:
  description: ''
  pages:
    - type: basic
      slug: aws-kms
      title: AWS KMS
    - type: basic
      slug: azure-kms
      title: Azure KMS
    - type: basic
      slug: gcp-kms
      title: GCP KMS
    - type: basic
      slug: salesforce-shield
      title: Salesforce Shield
    - type: basic
      slug: key-lifecycle-management
      title: Key Lifecycle Management
---
The Akeyless Key Management System (KMS) allows organizations to simplify the lifecycle management and distribution of cryptographic keys in Multi-Cloud, Hybrid, and Enterprise Environments.

![](https://files.readme.io/8a5853e-Classic_Keys.png "Classic Keys.png")

The Akeyless KMS provides a workflow for sharing cryptographic keys with cloud KMS providers and managing the key lifecycle, including secure key generation and storage, full role-based access control, and logging and reporting of the key usage. This enables the customer to maintain centralized control of their keys in the Akeyless Platform while using the cryptographic capabilities of external cloud KMS providers. Additionally, the option to choose a custom key name when attaching a key to a KMS provides greater flexibility and control over key management within the Akeyless ecosystem.

When your cloud provider encryption keys are managed by Akeyless:

* You have centralized control of sensitive data across multiple clouds
* Encryption keys are separated from the data
* Your requirements on key complexity are met
* All your keys are managed in a uniform manner
* You have a complete audit trail of key usage

When you share a key with one of the supported cloud KMS providers, a copy of the key material is securely transferred in accordance with the key import specification (BYOK) of the KMS provider.

> 👍 Note
>
> Only [classic keys](doc:classic-keys) can be distributed to cloud KMS providers.

## Supported Cloud KMS Providers

Akeyless KMS integrates with the following cloud KMS providers:

* [AWS KMS](https://docs.akeyless.io/docs/aws-kms)
* [Azure Key Vault](https://docs.akeyless.io/docs/azure-kms)
* [Google Cloud EKM](https://docs.akeyless.io/docs/gcp-kms)
* [Salesforce Shield](https://docs.akeyless.io/docs/salesforce-shield)

# Tutorial

Check out our tutorial video on 
<a href="https://tutorials.akeyless.io/docs/external-kms-with-classic-keys" target="_blank" style={{ color: "#00e" }}>Akeyless as an External Multi-Cloud KMS</a>.