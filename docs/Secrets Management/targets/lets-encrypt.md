---
title: Let's Encrypt Target
deprecated: false
hidden: false
metadata:
  robots: index
---
The [Let's Encrypt](https://letsencrypt.org/) Target enables you to use **Let's Encrypt** as a Public Certificate Authority (CA) with Akeyless PKI Issuer.

With a public CA, Akeyless cannot access the private key that signs certificates. Akeyless will programmatically validate the certificate signing request by connecting to **Let’s Encrypt** as a **Public CA** integration through the Akeyless Gateway.

With a public CA, Akeyless cannot access the private key that signs certificates. Akeyless will programmatically validate the certificate signing request by contacting **Let’s Encrypt** through the Akeyless Gateway.

The Let’s Encrypt integration uses an [ACME Client (v2)](https://datatracker.ietf.org/doc/html/rfc8555).

To prove you own the domain, **Let’s Encrypt** requires an **ACME challenge**, which can be complete using [DNS](https://letsencrypt.org/docs/challenge-types/#dns-01-challenge) or [HTTP](https://letsencrypt.org/docs/challenge-types/#http-01-challenge) validation.

* **DNS validation** -  Ownership is proven by adding a **DNS record**. This requires the domain to be managed in a supported DNS provider’s hosted zone (for example **AWS Route 53**, **GCP Cloud DNS**, or **Azure DNS**).

* **HTTP validation** - Ownership is proven by hosting a challenge file at a specific HTTP endpoint under the `http://<YOUR_DOMAIN>/.well-known/acme-challenge/` path. The certificate authority verifies ownership by sending an HTTP request to that **URL** and confirming that the expected value is returned.

## Create a Let's Encrypt Target with the CLI

To create a Let's Encrypt target with the CLI, run the following command:

```shell
akeyless target create lets-encrypt \
--name <Target Name> \
--lets-encrypt-url[=production] <[production]/[staging]> \
--acme-challenge[=http] <[http]/[dns] \
--dns-target-creds <[AWS/Azure/GCP] target name, relevant only when --acme-challenge=dns> \
--hosted-zone <AWS Route 53 hosted zone identifier, relevant only when --acme-challenge=dns and the DNS credentials target is AWS> 
```

Where:

* `name`: A unique name of the target. The name can include the path to the virtual folder where you want to create the new target, using slash `/` separators. If the folder does not exist, it will be created together with the target.

* `lets-encrypt-url`: Either **Production** - `https://acme-v02.api.letsencrypt.org/directory` (default) or **Staging** - `https://acme-staging-v02.api.letsencrypt.org/directory`.

* `acme-challenge[=http]`: Either **HTTP** or **DNS**

* `dns-target-creds`: The name of the `AWS`/`Azure`/`GCP` target that holds the connection details to the DNS provider endpoint where the **ACME DNS-01 challenge TXT record** will be created and deleted.

* `hosted-zone`: AWS Route 53 hosted zone, relevant only if `--acme-challenge=dns` and the DNS credentials target is **AWS**.

[View the complete list of parameters for this command.](https://docs.akeyless.io/docs/cli-ref-targets#lets-encrypt)

## Create a Let's Encrypt Target in the Console

1. Log in to the Akeyless Console, and go to **Targets** > **New** > **Certificate Automation (Let's Encrypt)**.

2. Define the Name of the target, and specify the Location as a path to the virtual folder where you want to create the new target, using slash `/` separators. If the folder does not exist, it will be created together with the target.

3. Select a **Protection key** with a Customer Fragment to enable Zero-Knowledge and click **Next**. [Read more about Zero-Knowledge Encryption](https://docs.akeyless.io/docs/implement-zero-knowledge).

4. Define the remaining parameters as follows:
   * **Server URL**: Either [Production](https://acme-v02.api.letsencrypt.org/directory) or [Staging](https://acme-staging-v02.api.letsencrypt.org/directory).

   * **Email**: Email address for the Let's Encrypt account.

   * **Challenge Type**:  **HTTP** or **DNS**

     * **DNS Provider**: Either **AWS**, **GCP** or **Azure** (relevant only if **Challenge Type** is **DNS**).
     * **Target**: Select a target that contains the DNS provider credentials (relevant only if **Challenge Type** is **DNS**).
     * **Hosted Zone**: [AWS Route 53](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/hosted-zones-working-with.html) hosted zone identifier. (Relevant only if **Challenge Type** is **DNS** and **DNS Provider** is **AWS**).
     * **Resource Group**: Azure resource group name. (Relevant only if **Challenge Type** is **DNS** and **DNS Provider** is **Azure**).

5. Click Finish.
