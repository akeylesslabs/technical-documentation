---
title: Build Your Chain of Trust
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
Akeyless offers the creation of a private certificate authority, in which you can use your certificate authority to sign intermediate certificates, which will sign server/client certificates, which is also called, **Chain of Trust**. 

The certificate chain includes the following components: 

* **Root CA**: The Root CA is an authority responsible for signing Intermediate certificates. In our scenario, it functions as the Certificate Authority and we will use a [DFC Key](https://docs.akeyless.io/docs/encryption-keys) which brings an air-gapped solution out of the box, as your **Private** key never exists as a single piece. 

* **Intermediate CA**: Signed by the **Root CA**, the Intermediate CA is tasked with signing Client certificates. These certificates are trusted by the Root CA, as it has authorized the Intermediate CA.

* **Leaf Certificate**: A certificate that is being used by any application. 

<Image align="center" width="123% " src="https://files.readme.io/61741a52fb97a98d5eacb4c17b807b6ca1b9a75a504e506af7e9c6c6b67dfcaf-Akeyless_Certificate-Chain.png" />

# Creating a Chain of Trust

The whole chain of trust can be generated using one dedicated CLI command, which automatically creates:

* **Root** and **Intermediate**PKI Issuers.

* **Signer key** with a signed certificate for each issuer which includes the following parameters:

  * **basicConstraints**: `critical`, `CA:TRUE`, `pathlen:1`

  * **keyUsage**: `critical`, `cRLSign`, `digitalSignature`, `keyCertSign`

> 🚧 Warning
>
> Automatic creation of a Chain of Trust is not supported if the Item Naming Convention configured in Global Settings contains a literal space character. In this case, follow the [manual guide](https://docs.akeyless.io/docs/ca-chain-of-trust-manually) to build the Chain of Trust.

Example for generating a **Chain of Trust** where the `common-name` for the **Root** issuer will be: `My-First-Chain root CA` and the `common-name` for the  **Intermediate** issuer will be: `My-First-Chain intermediate CA` (You can customize the maximum path length by using the `--max-path-len` flag):

```shell
akeyless generate-ca \
--pki-chain-name My-First-Chain \
--allowed-domains example.com \
--extended-key-usage clientauth \
--ttl 10d \
--gateway-url 'https://<Your-Akeyless-GW-URL:8000>'
```

Where:

* `pki-chain-name`: The name of the **Root** and **Intermediate** issuers and the main folder contain all of the related objects.

* `allowed-domains`: Domains that will be allowed by the issuer.

* `extended-key-usage[=serverauth,clientauth]`: extended key usage for the intermediate (`serverauth` / `clientauth` / `codesigning`).

* `ttl`: The maximum requested Time To Live for the issued certificate by default in seconds, supported formats are `s`,`m`,`h`,`d`.

* `gateway-url`: Akeyless Gateway Configuration Manager URL (port `8000`).

Running the command above will create  a **Certificate Chain** under **/My-First-Chain** folder, where certificates for `example.com` domain can be issued with a `TTL` of 10 days.

> 👍 Tip
>
> The `pathlen` value can be change by using the `--max-path-len` flag.

You can find the complete list of parameters for this command in the [CLI Reference - Certificates section.](https://docs.akeyless.io/docs/cli-reference-certificates#chain-of-trust)

## Items Structure

The following is the structure of the items related to the newly created CA:

* **pki** - A root folder that will contain all **Certs**, **Issuers** and **Keys**.
* **Certs** - Contains the certificate for both **Root** and **Intermediate** issuers.
* **Issuers** -  Contains the both **Root** and **Intermediate** issuers.
* **Keys** - Contains the signer keys for both **Root** and **Intermediate** issuers.

Once the certificate is generated, a new folder named **certificates** will be created, containing the newly generated certificate. 

## Issuing a Leaf Certificate

Once the chain is created, a certificate can be generated from the **Intermediate** issuer.

First, Create a [Certificate Signing Request](https://docs.akeyless.io/docs/cli-reference-certificates#p-stylecolorbluegenerate-csrp):

```shell
akeyless generate-csr \
--name <key name> \
--common-name example.com >> example.csr
```

Where:

* `name`: **Required**, Full path to the key to sign the CSR.

* `common-name`: **Required**, `common-name` to be included in the CSR certificate. In this case, we use `example.com` as this is the `common-name` that we set in the allowed domains of the issuer.

The next step will be to generate the certificate using the **Intermediate** issuer:

```shell
akeyless get-pki-certificate \
--cert-issuer-name /My-First-Chain/pki/issuers/intermediate/issuer \
--csr-file-path example.csr
```

Where:

* `cert-issuer-name`: The full path for the **Intermediate** issuer.

* `csr-file-path`: Path to the CSR that was created earlier.

Running the command above will create a certificate with the called `example.com`, where clicking the **View Certificate Details** button will show the full certificate chain.
