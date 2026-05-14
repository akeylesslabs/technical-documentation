---
title: PQC Support Reference
excerpt: Hybrid PQC profile and coverage details for Akeyless SaaS and Gateway
deprecated: false
hidden: false
metadata:
  title: 'PQC Support Reference | Akeyless'
  description: 'Hybrid post-quantum cryptography (PQC) profile, coverage matrix, and verification guidance for Akeyless SaaS and Gateway TLS connections.'
  robots: index
next:
  description: ''
---
Akeyless implements hybrid post-quantum cryptography (PQC) for TLS connections between clients and both the Akeyless SaaS platform and Akeyless Gateway deployments. This page provides the cryptographic profile, coverage matrix, and verification steps for compliance and operational reference.

## Cryptography Profile

Akeyless TLS hybrid PQC connections use the following profile:

| Parameter | Value |
| --- | --- |
| TLS version | `TLS 1.3` |
| Hybrid key exchange identifier | `X25519MLKEM768` |
| Classical component | X25519 |
| Post-quantum component | ML-KEM 768 (NIST FIPS 203) |

`X25519MLKEM768` indicates a hybrid key exchange where both classical and post-quantum algorithms participate in the TLS handshake.

## Coverage and Configuration Matrix

| Connection path | Hybrid PQC support | Required action |
| --- | --- | --- |
| Client to Akeyless SaaS | Enabled by default | No user configuration required |
| Client to Akeyless Gateway endpoint | Supported, configuration required | Set `MIN_TLS_VERSION=TLSv1.3` on the Gateway deployment |
| Gateway to Akeyless SaaS | Enabled by default | No user configuration required |

## Gateway Configuration Requirements

To enable hybrid PQC for the Akeyless Gateway endpoint, set the following environment variable in the deployment:

* `MIN_TLS_VERSION=TLSv1.3`

When TLS 1.3 is enabled, the Go runtime negotiates `X25519MLKEM768` automatically. No additional flags are required.

After changing `MIN_TLS_VERSION`, restart or redeploy the Gateway so the updated value is applied.

Deployment examples:

* [Gateway Docker Advanced Configuration](https://docs.akeyless.io/docs/gateway-docker-advanced-configuration)
* [Gateway Kubernetes Helm Values Reference](https://docs.akeyless.io/docs/gateway-kubernetes-helm-values-reference)

## Client Compatibility

Hybrid PQC key exchange requires both peers to support `X25519MLKEM768`. The following clients negotiate it automatically:

* Current major browsers
* Go runtime 1.24 and later (including the Akeyless Go SDK and CLI)

Older clients that do not support `X25519MLKEM768` fall back to a classical key exchange without disrupting the TLS connection.

## Verification Guidance

To verify hybrid PQC on a Gateway endpoint using a browser:

1. Open the Gateway endpoint over HTTPS in a browser.
2. Open the browser connection security details.
3. Confirm the negotiated key exchange includes `X25519MLKEM768`.

To verify using OpenSSL (requires OpenSSL 3.5.0 or later):

```shell Linux and macOS
openssl s_client -connect <gateway-host>:<port> -tls1_3 2>&1 | grep "Server Temp Key"
```
```powershell Windows
openssl s_client -connect <gateway-host>:<port> -tls1_3 2>&1 | Select-String "Server Temp Key"
```

A hybrid PQC key exchange returns output similar to:

```text
Server Temp Key: X25519MLKEM768
```

Interpretation:

* `Server Temp Key: X25519MLKEM768`: Hybrid PQC is active.
* `Server Temp Key: X25519`: The connection negotiated classical key exchange.

If you expect hybrid PQC but observe `X25519`, confirm that the client supports `X25519MLKEM768` and that the Gateway is configured with `MIN_TLS_VERSION=TLSv1.3`.

Troubleshooting checklist:

* Confirm the command is targeting the Gateway endpoint directly.
* Confirm the Gateway has restarted after applying `MIN_TLS_VERSION=TLSv1.3`.
* Confirm the client and OpenSSL version support `X25519MLKEM768`.

## Related Resources

* [TLS Settings](https://docs.akeyless.io/docs/gateway-tls-settings)
* [FIPS Certifications](https://docs.akeyless.io/docs/fips)
* [Akeyless Blog: Akeyless Advances Security with Post-Quantum Hybrid TLS 1.3](https://www.akeyless.io/blog/post-quantum-akeyless-hybrid-tls-1-3/)
