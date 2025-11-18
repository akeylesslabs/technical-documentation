---
title: PKI Certificate Issuer
excerpt: ''
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
      slug: kubectl-access
      title: Kubectl Access
---
# Introduction

Akeyless can act as a Certificate Authority (CA) for the internal environment. This page focuses on PKI Cert Issuer, if you wish to see how to create and work with SSH certificates, please follow this [link](https://docs.akeyless.io/docs/ssh-certificates).

To start building your chain of trust using Akeyless PKI Issuer, you can either bring your own CA certificate with the signing RSA key or simply generate your CA certificate as part of the signing key creation.

Using the PKI Issuer templates alongside the defined constraints enables maximum security with common PKI use cases, for example, limiting a PKI Issuer to accept issuance requests of specific key types and algorithms for example **RSA4096**  for specific **Allowed Domains** while templating the resulted certificate to use a specific list of **Key Usage** with a well defined **Location** settings.

In case you want to use your existing key, upload your RSA private key with the matching certificate for signing intermediate CA or leaf certificates based on your chain of trust, using the following command:

```shell Upload CA
akeyless upload-rsa \
--name <Key Name> \
--alg <RSA2048> \
--rsa-key-file-path </path/to/RSAKey.pem> \
--cert </path/to/CACert>
```

Alternatively, you can create a new RSA key with a self-signed certificate:

1. Create a CSR configuration file. for example:

```shell shell
cat <<EOF > csr.conf
countryName=US
stateOrProvinceName=NY
localityName=NY
organizationName=Akeyless
organizationalUnitName=Security
commonName=akeylessSign

[ v3_req ]
basicConstraints=critical, CA:TRUE
keyUsage=critical, keyCertSign, digitalSignature, cRLSign
EOF
```

2. Create the **Signer Key**:

```shell Create-Key-In-Akeyless
akeyless create-dfc-key \
--name <RSA-key-name> \
--alg RSA2048 \
--generate-self-signed-certificate true \
--certificate-ttl 365 \
--conf-file-path ./csr.conf \
--certificate-format pem

```

You can find the complete list of parameters for this command in the [CLI Reference - Encryption Keys](https://docs.akeyless.io/docs/cli-reference-encryption-keys#p-stylecolorbluecreate-dfc-keyp) section.

> 👍 Note
>
> The example above demonstrates a very basic usage of Signer key, to support all PKI settings You can work with Classic Keys as well to generate a signing key with a self-signed certificate.

## Creating a Certificate Issuer

A PKI Issuer enables you to issue certificates while the certificate templates are well-defined at the issuer level. To create the PKI Issuer, use the following command:

```shell Create PKI Cert Issuer
akeyless create-pki-cert-issuer \
--name <my_pki_cert_issuer> \
--signer-key-name <RSA-key-name> \
--ttl 30d \
--destination-path /path/to/store/issued/certificates \
--create-public-crl \
--gw-cluster-url <https://Gateway URL:8000> \
--expiration-event-in 30 \
--allowed-extra-extensions '{"OID":["Value"]}'
```

Where:

* `name`: A unique name for the PKI issuer item. The name can include a path to the virtual folder where you want to create a new PKI cert issuer using the slash / separators. If the folder does not exist, it will be created together with the item.

* `signer-key-name`: The CA private key which contains the root certificate to be used for certificate signing.

* `ttl`: The time to live of the issued certificates supported units are `s,m,h,d`.

* `destination-path`:  A path in Akeyless to save generated certificates using the issued certs under this path, to work with advanced features and events. Required for **CRL**.

* `create-public-crl`: Optional, to maintain a public CRL at: `https://vault.akeyless.io/crl/<account-id>/<cert-issuer-display-id>`.

* `create-private-crl`  Optional, creates the CRL endpoint on the [Gateway](https://docs.akeyless.io/docs/api-gw) at: `https://<gatewayURL>/crl/<cert-issuer-display-id>`.

* `gw-cluster-url`  Akeyless Gateway Configuration Manager URL (port 8000). Required for **private CRL**.

* `expiration-event-in`: How many days before the expiration of the certificate would you like to be notified. To specify multiple events, use the argument multiple times: --expiration-event-in 30 --expiration-event-in 60 to get events 60 and 30 days in advance.

* `allowed-extra-extensions`:  A `json `string that defines the allowed extra extensions for the PKI cert issuer, e.g. `'{"1.2.3":["test"]}'`.

You can find the complete list of parameters for this command in the [CLI Reference - Certificates](https://docs.akeyless.io/docs/cli-reference-certificates#p-stylecolorbluecreate-pki-cert-issuerp) section.

> 👍 Note
>
> **Automatically store & renew certificate**  
> Set the PKI Issuer item to automatically store & renew any issued certificate with default expiration events to gain full automation of your PKI environments.

## Creating a Certificate Signing Request

You can generate a Certificate Signing Request (CSR) in Akeyless to issue a new certificate using the PKI Issuer.

It is possible to either use an existing Classic Key/DFC key or [create a new one](https://docs.akeyless.io/docs/classic-keys).

Generate a new Certificate Signing Request:

```shell
akeyless generate-csr \
--name <name/of/new/Classic-Key> or <name/of/new/DFC-Key> \
--generate-key \
--alg <RSA2048> \
--common-name <mydomain.com> \
--gateway-url <https://Akeyless-Gateway-URL:8000> 
```

Where:

* `name`:  Full name of a new [Classic Key](https://docs.akeyless.io/docs/classic-keys) or DFC Key that will be generated.

* `generate-key`: Use this flag to generate a new classic key or dfc key with the CSR.

* `alg`: Algorithm to use for generating the new key supporting: `RSA1024`, `RSA2048`, `RSA3072`, `RSA4096`, `EC256`, `EC384`.

* `common-name`: Certificate common name.

* `gateway-url`: Akeyless Gateway Configuration Manager URL (port `8000`). to generate the classic key/dfc key, relevant only when using `generate-key` option.

> 📘 Note
>
> When using a wildcard certificate, if the `*` character is used in the name, it is automatically replaced with `~` in the Akeyless Console when the `--destination-path` is specified (i.e., when the certificate is stored in Akeyless).

You can find the complete list of parameters for this command in the [CLI Reference - Certificates](https://docs.akeyless.io/docs/cli-reference-certificates#p-stylecolorbluegenerate-csrp) section.

## Issuing a Certificate

To issue and sign a new certificate, use the following command:

```shell Issue Certificate
akeyless get-pki-certificate \
--cert-issuer-name <my_pki_cert_issuer> \
--csr-file-path ./mycsr.csr \
--outfile pki-certificate.pem
```

Where:

* `cert-issuer-name`: **Required**, the name of the PKI certificate issuer.

* `csr-file-path`: Path to the Certificate Signing Request file.

* `outfile`: Output file path with the certificate. If not provided, the file with the certificate will be created in the same location as the provided public key with the -cert extension.

> 👍 Tip
>
> You can provide the private key as well as part of the sign command for future certificate renewals using the `key-file-path` option.

You can find the complete list of parameters for this command in the [CLI Reference - Certificates](https://docs.akeyless.io/docs/cli-reference-certificates#p-stylecolorblueget-pki-certificatep) section.

## Revoke a Certificate

To revoke an existing certificate run the following command:

```shell CLI
akeyless revoke-certificate \
--name <certificate name> \
--item-id <certificate item id> \
--version <certificate version> \
--serial-number <certificate serial number>
```

Where:

* `name`: Certificate item name to revoke.

* `item-id`: The item id of the certificate to revoke.

* `serial-number`: The serial number of the certificate to revoke, in `base10` or `hex` format.

* `version`: Certificate version to revoke. Required if `item-id` or `name` are used.

Here you can provide a certificate full name, or use the`item-id`  or the certificate `serial-number` instead. In case a CRL (Certificate Revocation List) is maintained, the certificate will be added to the revocation list.

> 📘 Note
>
> In order to view the **Certificate Revocation List**, the **PKI Cert Issuer's** signing key **must** include the `cRLSign` extention.

# Working with Certificates in the Console

## Prerequisites

Creating a CA private key and root certificate to build your chain of trust:

1. Log in to the Akeyless Console, and go to **Items > New > Encryption Key > DFC**.

2. Define a **Name** of the key, and specify the **Location** as a path to the virtual folder where you want to create the new key, using slash `/` separators. If the folder does not exist, it will be created together with the key.

3. Define the remaining parameters as follows:

* **Description:** General description of the key (optional).

* **Tags:** Assign tags to the key (optional).

* **Delete Protection:** When enabled, protects the secret from accidental deletion.

* **Type:** The encryption algorithm used for the key.

* **Customer Fragment:** If you have an existing [customer fragment](https://docs.akeyless.io/docs/dfc), you may attach it to the key. If you wish to generate one, please refer to [these instructions](https://docs.akeyless.io/docs/cli-reference-encryption-keys#p-stylecolorbluegen-customer-fragmentp).

* **Generate-Self-Signed-Certificate:** Enable this option to generate your root CA certificate as part of the key creation.

## Creating a Certificate Issuer

1. Go to **Items > New > PKI Cert Issuer**

2. Define a **Name** of the cert issuer, and specify the **Location** as a path to the virtual folder where you want to create it, using slash `/` separators. If the folder does not exist, it will be created together with the cert issuer.

3. Define the remaining parameters as follows:

* **Description:** General description of the key (optional).

* **Tags:** Assign tags to the key (optional).

* **Delete Protection:** When enabled, protects the secret from accidental deletion.

* **Signer Key:** The name of the signer key you defined in advance.

* **Certificate TTL:** The time to the expiration of the certificate.

* **Allowed domains list:** Specify the allowed domains for the certificates issued.

* **Allowed URI sans:** Specify the allowed URI for the certificates issued.

4. The description for the advanced and location parameters can be found [here](https://docs.akeyless.io/docs/cli-reference-certificates#p-stylecolorbluecreate-pki-cert-issuerp).

## Issuing a Certificate

To issue a certificate using an existing PKI issuer through the console, go through the following steps:

1. Go to the folder in which your certificate issuer is located and select it.

2. Under the key details, you will see a button reading **Generate PKI Certificate**, tap it.

3. Fill in the public key (`PEM` format) or the `CSR` .

4. Tap generate, and if all parameters are valid, you will get a certificate.
