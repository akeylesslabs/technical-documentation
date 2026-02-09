---
title: Let's Encrypt Target
deprecated: false
hidden: true
metadata:
  robots: index
---
**Let's Encrypt** Target enables you to use **Let's Encrypt** as a Public CA with Akeyless PKI Issuer.

With Public CA, Akeyless cannot access the private key that signs the certificates. Hence, Akeyless will programmatically contact **GoDaddy** through the Gateway using IMAP user credentials to validate the certificate request. Akeyless will store and manage the issued certificates and notify you of upcoming expiration events.
