---
title: Let's Encrypt Target
deprecated: false
hidden: true
metadata:
  robots: index
---
The **Let's Encrypt** Target enables you to use **Let's Encrypt** as a Public Certificate Authority (CA) with Akeyless PKI Issuer.

With a public CA, Akeyless cannot access the private key that signs certificates. Akeyless will programmatically validate the certificate signing request by connecting to **Let’s Encrypt** as a **Public CA** integration through the Akeyless Gateway.

With a public CA, Akeyless cannot access the private key that signs certificates. Akeyless will programmatically validate the certificate signing request by contacting **Let’s Encrypt** through the Akeyless Gateway using the domain owner's account details. The Let’s Encrypt integration works via an **ACME Client V2**, and requires an **ACME Challenge** for domain validation, supporting both **DNS** and **HTTP** methods.

Akeyless will store the issued certificates, manage them, and notify you of upcoming expiration events.

# Create a Let's Encrypt Target in the Console

1. Log in to the Akeyless Console, and go to **Targets** > **New** > **Certificate Automation (Let's Encrypt)**.

2. Define the Name of the target, and specify the Location as a path to the virtual folder where you want to create the new target, using slash `/` separators. If the folder does not exist, it will be created together with the target.

3. Select a **Protection key** with a Customer Fragment to enable Zero-Knowledge and click **Next**. [Read more about Zero-Knowledge Encryption](https://docs.akeyless.io/docs/implement-zero-knowledge).

4. Define the remaining parameters as follows:
   * **Server URL**: Either [Production](https://acme-v02.api.letsencrypt.org/directory) or [Staging](https://acme-staging-v02.api.letsencrypt.org/directory).

   * **Email**:

   * **Challenge Type**: Either **DNS** or **HTTP**.

     * **DNS Provider**: Either **AWS**, **GCP** or **Azure** (relevant only if **Challenge Type** is **DNS**).

     * **Target**: Select a target that contains the DNS provider credentials.

     * **Hosted Zone**: [AWS Route 53](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/hosted-zones-working-with.html) hosted zone identifier. (relevant only if **Challenge Type** is **DNS** and **DNS Provider** is **AWS**).

Click Finish.
