---
title: Redirect and SSH URL Hardening
slug: sra-redirect-and-ssh-url-hardening
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
Use this page to restrict redirect endpoints and bastion callback URLs to approved destinations.

These controls reduce the risk of endpoint spoofing, unsafe callback routing, and user-supplied URL abuse in portal-assisted access flows.

## Bastion Redirect Allowlists

For Gateway remote access configuration, use bastion URL allowlists:

```shell
akeyless gateway update remote-access \
  --allowed-urls https://<BASTION_URL_1>,https://<BASTION_URL_2> \
  --gateway-url https://<YOUR_AKEYLESS_GW_URL>:8000
```

In ZTWA deployment configuration, allowlist controls include:

* `dispatcher.config.allowedBastionUrls`
* `dispatcher.config.allowedProxyUrls`

For requirements context, see [SRA Requirements](https://docs.akeyless.io/docs/sra-requirements#redirect-url-allowlist-requirements).

## Authentication Method Redirect URIs

Authentication methods also have redirect restrictions. For example, SAML and OIDC auth methods support `--allowed-redirect-uri` configuration.

These redirect URI controls are separate from SRA bastion allowlists and should be configured consistently.

For auth method reference, see [CLI Reference - Auth](https://docs.akeyless.io/docs/cli-ref-auth).

## SSH Endpoint Hardening Context

For SSH-based SRA, combine URL allowlists with host restrictions on SSH Certificate Issuers and approved bastion endpoint configuration.

For host restriction controls, see [SSH Access](https://docs.akeyless.io/docs/sra-ssh) and [SSH Certificates](https://docs.akeyless.io/docs/sra-ssh-certificates).

## Validation Checklist

1. Define allowed bastion URLs in Gateway configuration.
2. Define allowed proxy URLs for ZTWA dispatcher where applicable.
3. Verify authentication method redirect URIs are restricted.
4. Confirm user-provided endpoints outside allowlists are rejected.
