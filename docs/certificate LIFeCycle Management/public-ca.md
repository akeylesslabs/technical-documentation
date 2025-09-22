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
Akeyless supports [ZeroSSL](https://zerossl.com/), [GlobalSign](https://www.globalsign.com/), [Venafi](https://venafi.com/), [GoDaddy](https://www.godaddy.com/) and [Sectigo](https://www.sectigo.com/) as a Public CAs. 

The public certificate authority will sign and issue the certificate, while Akeyless will store and manage the certificate lifecycle.

The issuance flow utilizes a Public CA Target with Akeyless [PKI Issuer](doc:ssh-and-pkitls-certificates), ensuring full automation and storage of your public certificate while providing real-time expiration notification inside the [Event Center](doc:event-center) to manage the lifecycle of your certificates.

# Prerequisites

- An [Akeyless Gateway](doc:api-gw) to interact with the Public Certificate Authority.
- Target of the public CA.

## PKI Cert issuer with a Target

Run the following command to create a PKI Certificate Issuer with a Public CA Target:

```shell shell
akeyless create-pki-cert-issuer \ 
--name <PKI Issuer name> \
--ca-target <Path/To/Target> \
--gw-cluster-url https://<Your-Gateway-URL:8000> \
--ttl <7776000> \
--allowed-domains <domain1.com,domain2.com> \
--destination-path </Certificate/Storage/Folder> \
--expiration-event-in <5>
```

Where:

- `name`: A unique name for the PKI issuer item. The name can include a path to the virtual folder where you want to create a new PKI cert issuer using the slash `/` separators. If the folder does not exist, it will be created together with the item.

- `ca-target`: The name of an existing CA target to attach this PKI Certificate Issuer.

- `gw-cluster-url`: Akeyless Gateway Configuration Manager URL (port `8000`).

- `ttl`: The maximum requested Time To Live for an issued certificate by default in seconds, supported formats are `s`,`m`,`h`,`d`.

- `allowed-domains`: A list of domains that will be allowed to issue certificates for using this item.

- `destination-path`:  A path in Akeyless for [Certificate Storage](doc:certificate-storage), the issued certificate will be stored under this folder.

- `expiration-event-in`: How many days before the expiration of the certificate would you like to be notified. To specify multiple events, use the argument multiple times: `expiration-event-in 10` `expiration-event-in 15`.

You can find the complete list of parameters for this command in the [CLI Reference - Certificates](https://docs.akeyless.io/docs/cli-reference-certificates#p-stylecolorbluecreate-pki-cert-issuerp) section.

> 👍 Allowed Domains
> 
> Due to the nature of some Public CAs e.g. GoDaddy, **CN** might be sent with the classic `www.` prefix, it is recommended to check this in advance for future automated renewal.

## Issuing a certificate

Run the following command to create a new Certificate Signing Request (CSR):

```shell
akeyless generate-csr \
--name <Name/of/New/Classic-Key> \
--generate-key \
--alg <RSA1024> \
--common-name <common name to be included in the CSR certificate> \
--gateway-url <https://Akeyless-Gateway-URL:8000>
```

Where:

- `name`:  Full name of a new [Classic Key](doc:classic-keys) that will be generated.

- `generate-key`: Use this flag to generate a new classic key with the CSR.

- `alg`: Algorithm to use for generating the new key supporting: `RSA1024`, `RSA2048`, `RSA3072`, `RSA4096`, `EC256`, `EC384`.

- `common-name`: Certificate common name.

- `gateway-url`: Akeyless Gateway Configuration Manager URL (port `8000`). to generate the classic key, relevant only when using `generate-key` option.

You can find the complete list of parameters for this command in the [CLI Reference - Certificates](https://docs.akeyless.io/docs/cli-reference-certificates#p-stylecolorbluegenerate-csrp) section.

> 👍 Note
> 
> The `Common Name` field (e.g., server FQDN) - Should be listed under the `allowed-domains` as configured in the [PKI Issuer](doc:ssh-and-pkitls-certificates) item.

To issue a new certificate, run the following command:

```shell
akeyless get-pki-certificate \
--cert-issuer-name <PKI Issuer name> \
--csr-file-path MyCSR.csr
```

The output of this command contains the following value: 

- `display ID` - Certificate display ID.

You can find the complete list of parameters for this command in the [CLI Reference - Certificates](https://docs.akeyless.io/docs/cli-reference-certificates#p-stylecolorblueget-pki-certificatep) section.

To retrieve the certificate, run the following command:

```shell
akeyless get-certificate-value \
--cert-issuer-name <Issuer Name> \
--display-id <Certificate display ID>
```

You can find the complete list of parameters for this command in the [CLI Reference - certificates](https://docs.akeyless.io/docs/cli-reference-certificates#p-stylecolorblueget-certificate-valuep) section.

Once the certificate issue request is processed, a validation email will be sent to the email address listed in the Target, and it will be processed automatically by the [Akeyless Gateway](doc:api-gw)

The issued [Certificate item](doc:certificate-storage)  should be created under the `destination-path` storage folder inside Akeyless.