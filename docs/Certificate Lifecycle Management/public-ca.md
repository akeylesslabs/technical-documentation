---
title: Public CA
excerpt: Working with Public CA
deprecated: false
hidden: false
metadata:
  title: ''
  description: ''
  robots: index
next:
  description: ''
---
Akeyless supports [ZeroSSL](https://zerossl.com/), [GlobalSign](https://www.globalsign.com/), [Venafi (now part of CyberArk)](https://www.cyberark.com/venafi-and-cyberark-machine-identity-security/), [GoDaddy](https://www.godaddy.com/), [Sectigo](https://www.sectigo.com/), [Google Trust Services (Google CA)](https://cloud.google.com/security/products/certificate-authority-service), [DigiCert](https://www.digicert.com/), and [Let's Encrypt](https://letsencrypt.org/) as Public CAs.

The public certificate authority will sign and issue the certificate, while Akeyless will store and manage the certificate lifecycle.

The issuance flow uses a Public CA Target with Akeyless [PKI Issuer](https://docs.akeyless.io/docs/ssh-and-pkitls-certificates), ensuring full automation and storage of your public certificate, and providing real-time expiration notifications in the [Event Center](https://docs.akeyless.io/docs/event-center) to manage the lifecycle of your certificates.

## Prerequisites

* An [Akeyless Gateway](https://docs.akeyless.io/docs/gateway-overview) to interact with the Public Certificate Authority.
* Target of the public CA.

### PKI Cert Issuer With a Target

Run the following command to create a PKI Certificate Issuer with a Public CA Target:

```shell
akeyless create-pki-cert-issuer \
--name <PKI Issuer name> \
--ca-target <Path/To/Target> \
--gw-cluster-url https://<Your-Gateway-URL>:8000 \
--ttl <7776000> \
--allowed-domains <domain1.com,domain2.com> \
--destination-path </Certificate/Storage/Folder> \
--expiration-event-in <5> \
--auto-renew \
--scheduled-renew <14>
```

Where:

* `name`: A unique name for the PKI issuer item. The name can include a path to the virtual folder where you want to create a new PKI cert issuer using the slash `/` separators. If the folder does not exist, it will be created together with the item.

* `ca-target`: The name of an existing CA target to attach this PKI Certificate Issuer.

* `gw-cluster-url`: Akeyless Gateway URL (port `8000`).

* `ttl`: The maximum requested Time To Live for an issued certificate by default in seconds, supported formats are `s`, `m`, `h`, `d`.

* `allowed-domains`: A list of domains that will be allowed to issue certificates for using this item.

* `destination-path`: A path in Akeyless for [Certificate Storage](https://docs.akeyless.io/docs/certificate-storage), the issued certificate will be stored under this folder.

* `expiration-event-in`: How many days before the expiration of the certificate would you like to be notified. To specify multiple events, use the argument multiple times: `expiration-event-in 10` `expiration-event-in 15`.

* `auto-renew`: Automatically renew the certificate before expiration. Requires a `destination-path` to be set on the issuer.

* `scheduled-renew`: Number of days before the certificate's expiration date to trigger automatic renewal.

You can find the complete list of parameters for this command in the [CLI Reference - Certificates](https://docs.akeyless.io/docs/cli-reference-certificates#create-pki-cert-issuer) section.

* **Note (Allowed Domains)**: Due to the nature of some Public CAs, for example, GoDaddy, **CN** might be sent with the classic `www.` prefix; it is recommended to check this in advance for future automated renewal.
* **Note (Auto-Renew and Public CA Certificate Validity)**: `scheduled-renew` schedules renewal relative to the **certificate's actual expiration date**, not the issuer `ttl`. Public CAs may issue certificates with a shorter validity period than the `ttl` requested. For example, GlobalSign might cap validity at 200 days even if the issuer `ttl` is set to 365 days. In that case, Akeyless bases the renewal schedule on the real certificate expiry. With `--scheduled-renew 14` and a 200-day certificate, renewal is triggered on day 186.

### Issuing a Certificate

Run the following command to create a new Certificate Signing Request (CSR):

```shell
akeyless generate-csr \
--name <Name/of/New/Classic-Key> \
--generate-key \
--alg <RSA1024> \
--common-name <common name to be included in the CSR certificate> \
--gateway-url 'https://Akeyless-Gateway-URL:8000'
```

Where:

* `name`: Full name of a new [Classic Key](https://docs.akeyless.io/docs/classic-keys) that will be generated.

* `generate-key`: Use this flag to generate a new classic key with the CSR.

* `alg`: Algorithm to use for generating the new key supporting: `RSA1024`, `RSA2048`, `RSA3072`, `RSA4096`, `EC256`, `EC384`.

* `common-name`: Certificate common name.

* `gateway-url`: Akeyless Gateway URL (port `8000`). to generate the classic key, relevant only when using the `generate-key` option.

You can find the complete list of parameters for this command in the [CLI Reference - Certificates](https://docs.akeyless.io/docs/cli-reference-certificates#generate-csr) section.

> ℹ️ **Note:**
>
> The `Common Name` field (For example, server FQDN) - Should be listed under the `allowed-domains` as configured in the [PKI Issuer](https://docs.akeyless.io/docs/ssh-and-pkitls-certificates) item.

To issue a new certificate, run the following command:

```shell
akeyless get-pki-certificate \
--cert-issuer-name <PKI Issuer name> \
--csr-file-path MyCSR.csr
```

The output of this command contains the following value:

* `display ID` - Certificate display ID.

> ℹ️ **Note (GlobalSign targets):**
>
> For GlobalSign-based issuance, a single `get-pki-certificate` request is handled as a single issuance flow to avoid duplicate certificate issuance during transient retries.

You can find the complete list of parameters for this command in the [CLI Reference - Certificates](https://docs.akeyless.io/docs/cli-reference-certificates#get-pki-certificate) section.

To retrieve the certificate, run the following command:

```shell
akeyless get-certificate-value \
--cert-issuer-name <Issuer Name> \
--display-id <Certificate display ID>
```

You can find the complete list of parameters for this command in the [CLI Reference - certificates](https://docs.akeyless.io/docs/cli-reference-certificates#get-certificate-value) section.

Once the certificate issue request is processed, the selected public CA target validation flow is triggered and handled through the [Akeyless Gateway](https://docs.akeyless.io/docs/gateway-overview).

> ℹ️ **Note (Validation Method):**
>
> Validation depends on the selected public CA target. Some targets use email-based validation, while the [Let's Encrypt Target](https://docs.akeyless.io/docs/lets-encrypt) uses ACME challenge validation (`http` or `dns`).
>
> For DNS-based validation, ensure the referenced cloud target has the required DNS-zone permissions. For provider guidance, see [Let's Encrypt Target](https://docs.akeyless.io/docs/lets-encrypt#dns-provider-permissions-for-dns-01).

The issued [Certificate item](https://docs.akeyless.io/docs/certificate-storage) should be created under the `destination-path` storage folder inside Akeyless.
