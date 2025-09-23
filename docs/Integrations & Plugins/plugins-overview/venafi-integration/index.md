---
title: Venafi Integration
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
      slug: venafi-tpp
      title: Venafi Trust Protection Platform
    - type: basic
      slug: venafi-cloud
      title: Venafi Cloud
    - type: basic
      slug: cert-manager
      title: Cert Manager
---
Akeyless integrates with Venafi to provide certificate automation. Akeyless can be used for [Venafi Trust Protection Platform (TPP)](https://www.venafi.com/platform/trust-protection-platform) and [Venafi Cloud](https://www.venafi.com/venaficloud) to ensure compliance with enterprise policies and consistency with industry standards.

You no longer need to manually issue new PKI certificates, and you can dynamically retrieve PKI certificates.

Either Akeyless or Venafi can act as the certificate issuer.

* **Venafi Issuer:** The certificate is signed by Venafi’s intermediate Certificate Authority (CA). The issued certificate is saved on Venafi and in the Akeyless Platform. The certificate issuing policy template is pulled from the Venafi Zone configuration.

* **Akeyless Issuer:** The certificate is signed by a CA key from the Akeyless Platform created by the user. In addition, the issued certificate is saved in the Akeyless Platform as a secret and exported to Venafi for monitoring.

A certificate can be requested based on a Common Name (CN) or via a Certificate Signing Request (CSR). Both these methods fully support [Cert Manager](https://cert-manager.io/docs/).

The outcome artifacts of certificate issuance, including the certificate, private key, and certificate chain, are saved in the Akeyless Platform as a static secret in a configurable location. 

## Venafi Dynamic Secret settings

**Venafi API Key** - The API Key to use when connecting to a Venafi Cloud environment.

**Venafi Username** - The username to use when connecting to a Venafi Trust Protection Platform environment.

**Venafi Password** - The password to use when connecting to a Venafi Trust Protection Platform environment.

**Venafi Base URL** - Base URL of the TPP environment or Venafi cloud environment.

**Venafi Zone** - The zone to use when issuing new certificates (policies will be pulled from the provided zone).

**Optional fields:**

**Sign Using Akeyless PKI** - Determines whether to use Akeyless as an issuer.

**Signer Key Name** - The signer key to use as the issuer, must be a valid RSA 2048/4096 key with a certificate (Required when using Akeyless PKI, must already exist in Akeyless).

**Allowed Domains** - A list of allowed domains when requesting a new certificate (<code>default: all</code>).

**Allow Subdomains** - Whether to allow subdomains (<code>default: false</code>).

**User TLL** - The TTL of requested certificates (<code>default: 90 days</code>).

**Certificate Chain Order-Root First** - Where to place the root certificate in the certificate chain (<code>default: root first</code>).

**Store Private Key in Akeyless** -Whether to keep the generated private key in Akeyless as a static secret (Not relevant when generating a certificate using CSR) (default: `true`)

**Artifacts Location** - The location to place the generated artifacts in Akeyless (<code>default: /cert\_automation</code>).
