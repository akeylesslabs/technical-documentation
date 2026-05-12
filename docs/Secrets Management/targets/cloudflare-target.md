---
title: Cloudflare Target
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
The Cloudflare Target stores Cloudflare credentials in Akeyless. It is used as a DNS provider in certificate automation flows that rely on ACME DNS-01 validation.

Akeyless uses a Cloudflare credentials target as the DNS provider reference (`dns-target-creds`) when creating or updating Public Certificate Authority (CA) targets.

## How Cloudflare Fits in Akeyless

Cloudflare is part of the certificate lifecycle path, not a standalone public CA in Akeyless.

Use a Cloudflare target with the following target types:

* [Let's Encrypt Target](https://docs.akeyless.io/docs/lets-encrypt)
* [DigiCert Target](https://docs.akeyless.io/docs/digicert-target)
* [Google CA Target](https://docs.akeyless.io/docs/google-ca-target)

In these flows:

1. The public CA target handles ACME issuance.
2. The Cloudflare credentials target handles DNS TXT record updates for DNS-01 validation.
3. The PKI Issuer issues and stores certificates through Akeyless.

## Create a Cloudflare Target with the CLI

```shell
akeyless target create cloudflare \
--name <Target Name> \
--api-token <Cloudflare API Token> \
--account-id <Cloudflare Account ID>
```

Where:

* `name`: A unique name for the target. The name can include a path to a virtual folder by using slash `/` separators. If the folder does not exist, Akeyless creates it with the target.

* `api-token`: Required. A Cloudflare API token with permission to create and delete DNS TXT records in the relevant zone.

* `account-id`: Optional. The Cloudflare account ID associated with the token.

* `key`: Optional. Use this when you want to encrypt target secret values with a specific protection key instead of the account default key.

[View the complete list of parameters for this command.](https://docs.akeyless.io/docs/cli-ref-targets)

## Create a Cloudflare Target in the Console

1. Log in to the Akeyless Console, and go to **Targets**, then **New**, then **Cloudflare**.

2. Define the **Name** of the target, and specify the **Location** as a path to the virtual folder where you want to create the new target, using slash `/` separators. If the folder does not exist, it will be created together with the target.

3. Select a **Protection key** with a Customer Fragment to enable Zero-Knowledge and click **Next**. [Read more about Zero-Knowledge Encryption](https://docs.akeyless.io/docs/gateway-zero-knowledge).

4. Define the following parameters:

   * **API Token**: Required. A Cloudflare API token with permission to create and delete DNS TXT records.

   * **Account ID**: Optional. The Cloudflare account ID associated with the token.

5. Click **Finish**.

## Use the Cloudflare Target in ACME Flows

When using DNS-01 challenge with Cloudflare, configure the Public CA target with:

* `--dns-target-creds`: The name of the Cloudflare target.
* `--dns-zone`: The Cloudflare DNS zone name used for DNS-01 records.

For parameter-level details, see [CLI Reference - Akeyless Targets](https://docs.akeyless.io/docs/cli-ref-targets).

## Related Akeyless Capabilities

Cloudflare-connected certificate automation works together with:

* [PKI Issuers and Certificate Issuance](https://docs.akeyless.io/docs/ssh-and-pkitls-certificates)
* [Certificate Storage](https://docs.akeyless.io/docs/certificate-storage)
* [Event Center](https://docs.akeyless.io/docs/event-center) for pending expiration and expired certificate events
* [Gateway](https://docs.akeyless.io/docs/gateway-overview) when required by target and forwarding architecture

## Implementation Flow

1. Create a Cloudflare target using the steps above.
2. Create a public CA target (Let's Encrypt, DigiCert, or Google CA) with `--acme-challenge=dns`.
3. Set `--dns-target-creds` to the Cloudflare target name and set `--dns-zone`.
4. Create or update your PKI Issuer to use that public CA target.
5. Configure certificate expiration notifications in Event Center forwarders.
