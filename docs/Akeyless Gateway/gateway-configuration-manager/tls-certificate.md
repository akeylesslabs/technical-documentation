---
title: Gateway TLS Settings
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
      slug: implement-zero-knowledge
      title: Implementing Zero Knowledge
---
# Configuring TLS 

Akeyless Gateway should always be used with TLS to ensure all traffic is encrypted at transit. 

If you are working with Load Balancers or reverse proxies in front of your Gateway, TLS should be used for all network connections. 

> 👍 Note
> 
> The use of HTTP protocol is considered insecure and discouraged; thus, remote Gateway configuration is not supported over HTTP. If you wish to configure your gateway remotely make sure you do it over HTTPS.

To configure TLS, on your [Gateway Configuration Manager](doc:gateway-configuration-manager) under the **General** tab: 

1. Select the cloud icon next to **TLS Certificate**

2. Upload a TLS Certificate and provide a TLS Private Key in a PEM format and **Save**.

# Updating a TLS Certificate

Updating a TLS certificate can be accessed through the CLI by using the following command:

```shell
akeyless gateway-update-tls-cert --gateway-url <https://Your-Akeyless-Gateway-URL:8000> --cert-data <TLS Certificate(base64 encoded)>
```

The command's full parameters are:

- `cert-data`: TLS Certificate (base64 encoded), this flag is ignored if `cert-file-name` is supplied.
- `cert-file-name`: Path to the file containing the TLS Certificate, this flag is ignored if `cert-data` is supplied
- `key-data`: TLS Private Key (base64 encoded), this flag is ignored if `key-file-name` is supplied
- ` key-file-name`: Path to the file containing the TLS Private Key, this flag is ignored if `key-data` is supplied
- `gateway-url[=http://localhost:8000]`: Akeyless Gateway URL (Configuration Management port).