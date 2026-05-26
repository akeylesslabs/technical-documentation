---
title: TLS Settings
excerpt: Transport Layer Security (TLS) on Gateway
deprecated: false
hidden: false
metadata:
  title: ''
  description: ''
  robots: index
next:
  description: ''
  pages:
    - type: basic
      slug: gateway-zero-knowledge
      title: Zero Knowledge
---

<GatewayConfigManagementNote />
## Configuring TLS

Akeyless Gateway should always be used with TLS to ensure all traffic is encrypted in transit.

If you are working with Load Balancers or reverse proxies in front of your Gateway, TLS should be used for all network connections.

> ℹ️ **Note:**
>
> The use of the HTTP protocol is considered insecure and discouraged; thus, remote Gateway configuration is not supported over HTTP. If you wish to configure your Gateway remotely, make sure you do it over HTTPS.

To configure TLS, on your [Gateway Configuration Manager](https://docs.akeyless.io/docs/configure-gateway) under the **General** tab:

1. Select the cloud icon next to **TLS Certificate**

2. Upload a TLS Certificate and provide a TLS Private Key in a PEM format and **Save**.

Example CLI command to update the TLS certificate on an existing Gateway:

```shell
akeyless gateway-update-tls-cert \
--cert-data <TLS Certificate (base64-encoded)> \
--key-data <TLS Private Key (base64-encoded)> \
--gateway-url 'https://<Your-Akeyless-GW-URL>:8000'
```

## TLS 1.3 and PQC

For Akeyless SaaS endpoints, hybrid post-quantum key exchange is enabled by default over TLS 1.3.

For Akeyless Gateway endpoints, hybrid post-quantum key exchange is enabled when the Gateway is configured to use TLS 1.3.

For deployment-specific steps, see:

* [Gateway Docker Advanced Configuration](https://docs.akeyless.io/docs/gateway-docker-advanced-configuration)
* [Gateway Kubernetes Helm Values Reference](https://docs.akeyless.io/docs/gateway-kubernetes-helm-values-reference)

After deployment, verify that the browser connection details show `X25519MLKEM768`, which confirms a hybrid key exchange (X25519 + ML-KEM 768).

## Updating a TLS Certificate

Updating a TLS certificate can be accessed through the CLI by using the following command:

```shell
akeyless gateway-update-tls-cert \
--cert-data <TLS Certificate (base64-encoded)> \
--key-data <TLS Private Key (base64-encoded)> \
--gateway-url 'https://<Your-Akeyless-GW-URL>:8000'
```

This command requires both a TLS certificate and a matching TLS private key.

The command's full parameters are:

* `cert-data`: TLS Certificate (Base64-encoded), this flag is ignored if `cert-file-name` is supplied.
* `cert-file-name`: Path to the file containing the TLS Certificate, this flag is ignored if `cert-data` is supplied
* `key-data`: TLS Private Key (Base64-encoded), this flag is ignored if `key-file-name` is supplied
* `key-file-name`: Path to the file containing the TLS Private Key, this flag is ignored if `key-data` is supplied
* `gateway-url[=http://localhost:8000]`: Akeyless Gateway URL (Configuration Management port).
