---
title: Cloudflare and Akeyless Targets
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
Cloudflare in Akeyless is used as a DNS provider in certificate automation flows that rely on ACME DNS validation.

Akeyless uses a Cloudflare credentials target as the DNS provider reference (`dns-target-creds`) when creating or updating Public CA targets.

## How Cloudflare Fits in Akeyless

Cloudflare is part of the certificate lifecycle path, not a standalone Public CA in Akeyless.

Use Cloudflare with the following target types:

* [Let's Encrypt Target](https://docs.akeyless.io/docs/lets-encrypt)
* [DigiCert Target](https://docs.akeyless.io/docs/digicert-target)
* [Google CA Target](https://docs.akeyless.io/docs/google-ca-target)

In these flows:

1. The Public CA target handles ACME issuance.
2. The Cloudflare credentials target handles DNS TXT record updates for DNS-01 validation.
3. The PKI Issuer issues and stores certificates through Akeyless.

## Cloudflare Parameters in ACME Target Flows

When using DNS challenge with Cloudflare, configure:

* `dns-target-creds`: The target that stores Cloudflare credentials.
* `dns-zone`: The Cloudflare DNS zone used for DNS-01 records.

For parameter-level details, see [CLI Reference - Akeyless Targets](https://docs.akeyless.io/docs/cli-ref-targets).

## Related Akeyless Capabilities

Cloudflare-connected certificate automation works together with:

* [PKI Issuers and Certificate Issuance](https://docs.akeyless.io/docs/ssh-and-pkitls-certificates)
* [Certificate Storage](https://docs.akeyless.io/docs/certificate-storage)
* [Event Center](https://docs.akeyless.io/docs/event-center) for pending expiration and expired certificate events
* [Gateway](https://docs.akeyless.io/docs/gateway-overview) when required by target and forwarding architecture

## Suggested Implementation Flow

1. Create or identify your Cloudflare credentials target.
2. Create a Public CA target (Let's Encrypt, DigiCert, or Google CA) with `acme-challenge=dns`.
3. Set `dns-target-creds` to the Cloudflare target and set `dns-zone`.
4. Create or update your PKI Issuer to use that Public CA target.
5. Configure certificate expiration notifications in Event Center forwarders.
