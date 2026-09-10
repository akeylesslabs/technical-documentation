---
title: Certificate Policies
deprecated: false
hidden: false
metadata:
  robots: index
---
Certificate Policies evaluate every certificate in your Inventory for lifecycle risk and cryptographic strength. When a certificate matches a policy's condition, it's surfaced as a finding in **Dashboard** and **Inventory**, with a severity that reflects how urgently it needs attention. For an overview of how policies fit into Identity & Secrets Intelligence as a whole, see [Policies](doc:policies).

## Available Certificate Policies

Identity & Secrets Intelligence currently ships the following built-in Certificate Policies:

| Policy                          | Severity | What It Flags                                                                                                  |
| ------------------------------- | -------- | -------------------------------------------------------------------------------------------------------------- |
| **Certificate Expired**         | High     | The certificate has already expired                                                                            |
| **Certificate About to Expire** | High     | The certificate is due to expire within the next 30 days                                                       |
| **Wildcard Certificate Usage**  | High     | The certificate is a wildcard certificate                                                                      |
| **Weak Algorithm**              | High     | The certificate uses a weak or deprecated cryptographic algorithm, such as SHA-1, MD5, or a small RSA key size |
| **Excessive Validity Period**   | Medium   | The certificate's validity period exceeds CA/Browser Forum guidance (more than 398 days)                       |
| **Not Quantum Ready**           | Low      | The certificate uses a classical algorithm (RSA, ECDSA, or ECC) that isn't resistant to quantum computing      |

### What's Next

- [Policies](doc:policies)
- [Secret Policies](doc:secret-policies)
- [Identity Policies](doc:identity-policies)
