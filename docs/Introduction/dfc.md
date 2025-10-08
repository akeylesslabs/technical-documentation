---
title: 'Part 3: Encryption Technology'
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
## Your key NEVER exists as a whole

Our patented technology, Akeyless Distributed Fragments Cryptography™ (DFC), enables us to perform cryptographic operations using fragments of an encryption key, without EVER combining the key fragments. As illustrated below, this technology allows Akeyless to store fragments of an encryption key in different regions on different cloud providers, and never combine those fragments.

<Image align="center" alt="An image of a physical key is split into three parts. Each part is associated with a cloud provider: Azure, GCP, and AWS." border={false} caption="Fragments of a single Encryption Key that are stored in different cloud providers and are NEVER combined" title="DFC.png" src="https://files.readme.io/0ef2ecb-DFC.png" width="80%" />

_**Q: So you're basically using key-split? Shamir's secret sharing?**_

* Answer: **NO. We're definitely not**. The known weakness of any split method is that whenever you wish to encrypt/decrypt any data, you MUST combine the fragments of the key. When you do so, a malicious attacker could potentially gain access to your constructed key, and then your key is compromised. Your data and applications are now at risk. This is why, using Akeyless DFC, the key is never constructed, not even during the encryption/decryption process, meaning, the key never exists as a whole.

## Key Fragments are constantly refreshed

An encryption key is basically a very high numeric value. Let's say that fragments of that value would have the sub-value of X, Y, and Z, where `X+Y+Z` equals the key. Now, assume that for every period of time, the X, Y, and Z values are changing to A, B, and C, where `A+B+C = X+Y+Z =` the Key. This would mean that a malicious attacker who wishes to access our key would need to access all of the key's fragments simultaneously, in a **simultaneous attack vector.**

## We use Zero-Knowledge Encryption for your Keys and Secrets

The missing piece of that puzzle is - who can access the key fragments? Some may say, that though Akeyless DFC doesn't allow cloud providers to have access to the whole key, Akeyless itself has the ability to construct the key whenever it wishes, since it manages the key fragments infrastructure.

Well, they're basically right, but, they can also be completely wrong.

Since Akeyless DFC enables Akeyless to perform cryptographic operations WITHOUT EVER COMBINING the encryption key, one of the key fragments can actually be on the customer's environment, where Akeyless has no access. This means that Akeyless, as a service provider, won't be able to decrypt any data that is encrypted by our customers (who hold one of the key fragments). The reason is simple: we don't have access to your fragment.

Therefore, in order to enable Zero-Knowledge Encryption, all you need is your own Customer Fragment.

<Image align="center" alt="1920" border={false} caption="Fragments of a single Encryption Key that are managed by Akeyless while a single fragment is stored in the customer's environment." title="API key auth (1).png" src="https://files.readme.io/3b36cbc-CFZK.png" />

<br />
