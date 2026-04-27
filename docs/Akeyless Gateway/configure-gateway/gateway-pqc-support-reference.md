---
title: PQC Support Reference
excerpt: Hybrid PQC profile and coverage details for Akeyless SaaS and Gateway
deprecated: false
hidden: false
metadata:
  title: ''
  description: ''
  robots: index
next:
  description: ''
---
Use this page as a formal reference for hybrid post-quantum cryptography (PQC) support in Akeyless SaaS and Akeyless Gateway TLS connections.

## Cryptography Profile

Akeyless TLS hybrid PQC connections use the following profile:

| Parameter | Value |
| --- | --- |
| TLS version | `TLS 1.3` |
| Hybrid key exchange identifier | `X25519MLKEM768` |
| Classical component | `X25519` |
| Post-quantum component | `MLKEM-768` |

`X25519MLKEM768` indicates a hybrid key exchange where both classical and post-quantum algorithms participate in the TLS handshake.

## Coverage and Configuration Matrix

| Connection path | Hybrid PQC support | Required action |
| --- | --- | --- |
| Client to Akeyless SaaS | Enabled by default | No user configuration required |
| Client to Akeyless Gateway endpoint | Supported | Configure Gateway for TLS 1.3 and set Go runtime flag |
| Gateway to Akeyless SaaS | Enabled by default | No user configuration required |

## Gateway Configuration Requirements

To enable hybrid PQC for the Akeyless Gateway endpoint, set both environment variables in the deployment:

* `MIN_TLS_VERSION=TLSv1.3`
* `GODEBUG=tlsmlkem=1`

Deployment examples:

* [Gateway Docker Advanced Configuration](https://docs.akeyless.io/docs/gateway-docker-advanced-configuration)
* [Gateway Kubernetes Helm Values Reference](https://docs.akeyless.io/docs/gateway-kubernetes-helm-values-reference)

## Verification Guidance

To verify hybrid PQC on a Gateway endpoint:

1. Open the Gateway endpoint over HTTPS in a browser.
2. Open the browser connection security details.
3. Confirm the negotiated key exchange includes `X25519MLKEM768`.

This confirms that TLS uses a hybrid key exchange with both classical and post-quantum components.

## Related Resources

* [TLS Settings](https://docs.akeyless.io/docs/gateway-tls-settings)
* [Akeyless Blog: Akeyless Advances Security with Post-Quantum Hybrid TLS 1.3](https://www.akeyless.io/blog/post-quantum-akeyless-hybrid-tls-1-3/)
