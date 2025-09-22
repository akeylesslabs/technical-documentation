---
title: Zero-Knowledge Encryption
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
## We use Zero-Knowledge Encryption for your Keys and Secrets

The missing piece of that puzzle is - who can access the key fragments? Some may say that though DFC doesn't allow cloud providers to access the whole key, Akeyless itself can construct the key whenever it wishes since it manages the key fragments infrastructure. 

Well, they're basically correct, but, they can also be completely wrong.

Since Akeyless DFC enables Akeyless to perform cryptographic operations WITHOUT EVER COMBINING the encryption key, one of the key fragments can actually be on the customer's environment, to which Akeyless has no access. This means that Akeyless, as a service provider, won't be able to decrypt any encrypted data by our customers (who hold one of the key fragments). The reason is simple: we don't have access to your fragment.

Therefore, in order to enable Zero-Knowledge Encryption, all you need is your own Customer Fragment. 

<Image title="API key auth (1).png" alt={1920} align="center" width="100%" src="https://files.readme.io/8c54a7f-CFZK.png">
  Simplified scheme of key storage breakdown. The cloud platform key fragments are backed up by Akeyless, and the customer fragment is kept by the customer.
</Image>

> 📘 Info
>
> **Implementing Zero Knowledge**\
> In order to implement the Zero Knowledge Encryption solution on your gateway, refer to the [Implementing Zero Knowledge](https://docs.akeyless.io/docs/implement-zero-knowledge) guide.
