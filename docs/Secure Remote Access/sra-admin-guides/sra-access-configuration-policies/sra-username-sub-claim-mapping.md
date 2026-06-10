---
title: Username Sub-Claim Mapping
slug: sra-username-sub-claim-mapping
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
Use this page to map authenticated identity claims to the runtime username used for Secure Remote Access target sessions.

This setting directly affects whether users can actually log in to target hosts after they authenticate to Akeyless.

Correct mapping helps you:

1. Prevent avoidable session failures caused by username resolution mismatch.
2. Keep access behavior consistent across SSH and RDP workflows.
3. Maintain cleaner audit trails by aligning identity claims with expected target usernames.

## Why Mapping Matters

When SRA opens SSH or RDP sessions that rely on an externally provided username, Gateway configuration determines which identity claim is used to resolve that username.

Incorrect claim mapping can cause valid users to authenticate successfully but fail target login authorization.

## Mapping Controls

The primary controls are:

* `--rdp-target-configuration`
* `--ssh-target-configuration`

These flags specify the claim name (for example, `email`) that should be used as the username source for the corresponding session type.

## CLI Examples

Configure both SSH and RDP mapping:

```shell
akeyless gateway update remote-access \
  --rdp-target-configuration email \
  --ssh-target-configuration email \
  --gateway-url https://<YOUR_AKEYLESS_GW_URL>:8000
```

Configure only SSH mapping:

```shell
akeyless gateway update remote-access \
  --ssh-target-configuration email \
  --gateway-url https://<YOUR_AKEYLESS_GW_URL>:8000
```

For complete flag behavior, see [CLI Reference - Gateway Secure Remote Access](https://docs.akeyless.io/docs/cli-reference-sra).

## Authentication Source Considerations

For SAML and OIDC flows, use a claim that is consistently present in your IdP token assertions.

When the selected claim is missing for a user, the target username cannot be derived from that claim, and connection establishment can fail.

## Operational Guidance

1. Choose a stable claim that is consistently issued by the IdP.
2. Validate mapping against both SSH and RDP test sessions.
3. Avoid claim names that vary across identity providers or environments.
4. Revalidate mapping after IdP schema or claim policy changes.
