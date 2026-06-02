---
title: Build Your Chain of Trust - Manual Guide
excerpt: ''
deprecated: false
hidden: true
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

![Illustration for: Intermediate CA: Signed by the Root CA, the Intermediate CA is tasked with signing Client certificates. These certificates are trusted by the Root CA, as it has…](https://files.readme.io/61741a52fb97a98d5eacb4c17b807b6ca1b9a75a504e506af7e9c6c6b67dfcaf-Akeyless_Certificate-Chain.png)

## Creating a Root CA

Given the critical role of the Root CA in validating end-user certificates, it's strongly recommended to store both the Root PKI Cert Issuer and the Root CA key in a secure location accessible only to authorized users.

Using a [DFC Key](https://docs.akeyless.io/docs/encryption-keys) which brings an air-gapped solution out of the box, as your **Private** key adds an extra level of protection.

> ℹ️ **Note:**
>
> In this guide, we used the environment variable `MY_GW` to store the gateway address (`https://<Your-Akeyless-GW-URL>:8000`). You can also directly use the gateway address if preferred.

### Creating a Root CA Signer Key

Let's create [DFC Key](https://docs.akeyless.io/docs/gateway-zero-knowledge#create-dfc-key-from-the-akeyless-console) for our **Root CA** with a self-signed certificate, first let's create the **CSR** conf file:

```shell
cat <<EOF > csr.conf
countryName= US
stateOrProvinceName= NY
localityName= NY
organizationName= Akeyless
organizationalUnitName= Security
commonName= example.com

[ v3_req ]
basicConstraints  = critical, CA:TRUE, pathlen:3
keyUsage = critical, digitalSignature, cRLSign, keyCertSign
EOF
```

Where:

* `CA:TRUE`: Basic Constraints that indicate the certificate requested in the CSR can be used as a Certificate Authority (CA) to sign other certificates.

* `digitalSignature`, `KeyCertSign`, `cRLSign`: Key Usage for CA certificates.

Run the following command to create [DFC key](https://docs.akeyless.io/docs/gateway-zero-knowledge#create-dfc-key-from-the-akeyless-console) and the certificate:

```shell
akeyless create-dfc-key \
--name /Chain/Root/CA \
--alg RSA2048 \
--generate-self-signed-certificate true \
--certificate-ttl 365 \
--certificate-format pem \
--conf-file-path csr.conf
```

Where:

* `name`: A unique name for the DFC Key. The name can include a path to the virtual folder where you want to create a new DFC Key using the slash / separators. If the folder does not exist, it will be created together with the item.

* `alg`: DFC Key type, options: `AES128GCM`, `AES256GCM`, `AES128SIV`, `AES256SIV`, `AES128CBC`, `AES256CBC`, `RSA1024`, `RSA2048`, `RSA3072`, `RSA4096`.

* `generate-self-signed-certificate`: Whether to generate a self signed certificate with the key. If set, `--certificate-ttl` must be provided.

* `certificate-ttl`: TTL in days for the generated certificate. Required only for generate-self-signed-certificate.

* `certificate-format`: The format of the returned certificate can be `pem` or `der`.

* `--conf-file-path`: Path to the configuration file that contains CSR config data.

You can find the complete list of parameters for this command in the [CLI Reference - Encryption Keys](https://docs.akeyless.io/docs/cli-reference-encryption-keys#create-dfc-key) section.

Upon successful creation, we will have a Private Key with a Self-Signed Certificate valid for a year, that we will use as a **Signer Key** of our top chain [PKI Certificate Issuer](https://docs.akeyless.io/docs/ssh-and-pkitls-certificates). This issuer will be used to issue the Intermediate layer of PKI Issuers in our chain of trust.

### Creating a Root PKI Issuer

Run the following command to create the Root PKI Issuer:

```shell
akeyless create-pki-cert-issuer \
--name /Chain/Root/RootIssuer \
--signer-key-name /Chain/Root/CA \
--gw-cluster-url $MY_GW \
--allowed-domains example.com \
--destination-path /Chain/Intermediate/Certificates \
--create-public-crl \
--ttl 100d \
--expiration-event-in 30 \
--is-ca true \
--key-usage digitalSignature,cRLSign,keyCertSign \
--organization-units Security \
--organizations Akeyless \
--country US \
--locality NY 
```

At this point, we have created the following:

* **Root CA Key**: A Signer Key with a Self Signed Certificate.
* **Root PKI Cert Issuer**: To sign new Intermediate CA.

Where **only** certificates with the domain `example.com` will be accepted and valid for 100 days, they will be automatically stored under the `/Chain/Intermediate/Certificates` folder, with basic constraints of `CA: TRUE` and the mentioned **KeyUsage**, **OU**, and **Location** settings as defined in the issuer. An event about the upcoming expiration will be triggered 30 days before expiration.

You can find the complete list of parameters for this command in the [CLI Reference - Certificates](https://docs.akeyless.io/docs/cli-reference-certificates#create-pki-cert-issuer) section.

The next step will be the creation of an **Intermediate Signer Key** with a signed certificate by our **Root PKI Cert Issuer** and using this key as a signer for our **Intermediate PKI Issuer**.

## Creating Intermediate CA

Intermediate certificates act as a middle-man between the secure root certificates and the server certificates distributed to the public. While a chain will always include at least one intermediate certificate, it may contain multiple ones as well.

### If You Started with `generate-ca`

If you used `generate-ca` as an initial bootstrap, continue this manual flow to add additional intermediate layers.

`generate-ca` creates a single Root → Intermediate chain in one step and does not expose all PKI issuer options. For example, flags such as `--allow-subdomains` must be set manually on `create-pki-cert-issuer`.

For full details, see [Build Your Chain of Trust](https://docs.akeyless.io/docs/build-your-chain-of-trust#multi-intermediate-pki-chains).

### Create an Intermediate Signer Key

Run the following command to create a **CSR** and a **Key** that will be used as our **Intermediate Signer Key**:

```shell
akeyless generate-csr \
--name /Chain/Intermediate/InterKey \
--generate-key \
--key-type classic-key \
--gateway-url $MY_GW \
--alg RSA2048 \
--common-name example.com >> intermediate.csr
```

Now let's issue the certificate using the **Root PKI Issuer** which we created earlier:

```shell
akeyless get-pki-certificate \
--cert-issuer-name /Chain/Root/RootIssuer \
--csr-file-path intermediate.csr > intermediate.crt
```

Let's add the issued certificate to our **Intermediate Signer Key**:

```shell
akeyless update-classic-key-certificate \
--name /Chain/Intermediate/InterKey \
--cert-file-path ./intermediate.crt
```

Now, we have our **Intermediate Signer Key** which has a certificate signed by our **Root CA**, let's create the **Intermediate PKI Issuer** to start issuing leaf certificates.

### Create an Intermediate PKI Cert Issuer

Run the following command to create the **Intermediate PKI Cert Issuer:**

```shell
akeyless create-pki-cert-issuer \
--name /Chain/Intermediate/InterPKIIssuer \
--signer-key-name /Chain/Intermediate/InterKey \
--gw-cluster-url $MY_GW \
--allowed-domains myexample.com \
--destination-path /MyChain/Intermediate/Leaf \
--create-public-crl \
--ttl 30d \
--expiration-event-in 10 \
--client-flag true \
--organization-units IT \
--organizations Akeyless \
--country US \
--locality NY 
```

Where **only** certificates with the domain `myexample.com` will be accepted and valid for 30 days, and they will be automatically stored under the `/MyChain/Intermediate/Leaf/` folder, with the **Extended Key Usage** of `client auth`, **OU**, and **Location** settings as defined in the issuer. An event about the upcoming expiration will be triggered 10 days before expiration.

> ℹ️ **Note:**
>
> The `--client-flag true` setting configures Client Authentication Extended Key Usage (EKU) policy on the PKI issuer. Certificates issued from this issuer, including console-based issuance flows, apply the configured EKU policy.

## Issuing a Leaf Certificate

Now that we have our **Intermediate PKI Cert Issuer** we can start issuing leaf certificates.

Run the following command to create a CSR with a [Classic Keys](https://docs.akeyless.io/docs/classic-keys) pair:

```shell
akeyless generate-csr \
--name /Chain/Intermediate/Leaf/MyFirstCertificate \
--generate-key \
--gateway-url $MY_GW \
--alg RSA2048 \
--common-name myexample.com >> leaf.csr
```

Generate a certificate using the **Intermediate PKI Cert Issuer**:

```shell
akeyless get-pki-certificate \
--cert-issuer-name /Chain/Intermediate/InterPKIIssuer \
--csr-file-path leaf.csr
```

## Intermediate CA Expiry and Sunset Behavior

When an intermediate CA's certificate expires, any leaf certificates it has signed become invalid per standard PKI validation rules, because the chain of trust can no longer be verified up to a trusted root. Some relying-party applications may be configured to ignore expired intermediates, but this is not standard behavior and should not be relied upon.

To replace an expired or retiring intermediate CA:

1. Create a new intermediate signer key and have it signed by the root PKI issuer.
2. Create a new intermediate PKI cert issuer using the new signer key.
3. Begin issuing new leaf certificates from the new issuer.

Because the root CA and its trust anchor remain in place, only the intermediate signing key needs to be replaced — not the root. This limits the blast radius of an intermediate expiry or compromise to the scope of that intermediate alone.

> ℹ️ **Note:**
>
> Akeyless plans to add validation to prevent issuing leaf certificates with a validity period longer than their issuer's remaining lifetime. This check is not yet enforced; plan your intermediate and leaf TTLs accordingly to avoid unexpected expiry scenarios.

## Rate Limits for Certificate Issuance

Standard Akeyless API rate limits apply to all certificate signing requests, including `get-pki-certificate`. For high-volume use cases — such as a large fleet of devices enrolling in parallel — plan request batching or staggered enrollment to avoid hitting rate limits. Contact [Akeyless support](mailto:support@akeyless.io) if you need guidance on rate limit thresholds for your account tier.
