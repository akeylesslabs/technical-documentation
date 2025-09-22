---
title: ACME Server
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
[ACME](https://en.wikipedia.org/wiki/Automatic_Certificate_Management_Environment), or **Automated Certificate Management Environment**, streamlines certificate management by enabling clients to interact directly with the Certificate Authority (CA) at every stage of the certificate lifecycle, including **issuance**, **revocation**, and **renewal**.

The ACME protocol defines an external account binding (**EAB**), allowing clients to securely interact with the **ACME Server** for certificate management.

Akeyless supports creating a [PKI Cert Issuer](https://docs.akeyless.io/docs/ssh-and-pkitls-certificates) that deploys an **ACME Server** on the [Gateway](https://docs.akeyless.io/docs/api-gw), with **EAB** support for secure registration. This setup allows external ACME clients (like [CertBot](https://certbot.eff.org/instructions?ws=other\&os=windows)) to automate the management of TLS certificates within the organization’s security framework.

Before proceeding, ensure you have permission to manage **ACME** on your Gateway.

# Enable ACME Server

In this guide, we will create a **PKI Cert Issuer** with  **ACME Server** where we will register [CertBot](https://certbot.eff.org/instructions?ws=other\&os=windows) as an **ACME Client** using External Account Binding. 

## Create a Signer Key

Let's create  [DFC Key](https://docs.akeyless.io/docs/implement-zero-knowledge#create-dfc-key-from-the-akeyless-console) for our **PKI Cert Issuer** with a self-signed certificate, first let's create the **CSR** conf file:

```shell
cat <<EOF > csr.conf
countryName= US
stateOrProvinceName= NY
localityName= NY
organizationName= Akeyless
organizationalUnitName= Security
commonName= acme.com

[ v3_req ]
basicConstraints  = critical, CA:TRUE, pathlen:3
keyUsage = critical, digitalSignature, cRLSign, keyCertSign
EOF
```

Where:

* `basicConstraints`:   Basic Constraints that indicate the certificate requested in the CSR can be used as a Certificate Authority (CA) to sign other certificates.

* `keyUsage`: Key Usage for CA certificate with  `digitalSignature`,`KeyCertSign`,`cRLSign`.

Run the following command to create the **Signer Key**:

```shell
akeyless create-dfc-key \
--name /ACME/Server/SignerKey \
--alg RSA2048 \
--generate-self-signed-certificate true \
--certificate-ttl 365 \
--certificate-format pem \
--conf-file-path csr.conf
```

Where:

* `name`: A unique name for the DFC Key. The name can include a path to the virtual folder where you want to create a new DFC Key using the slash / separators. If the folder does not exist, it will be created together with the item.

* `alg`: DFC Key type, options: [`AES128GCM`, `AES256GCM`, `AES128SIV`, `AES256SIV`, `AES128CBC`, `AES256CBC`, `RSA1024`, `RSA2048`, `RSA3072`, `RSA4096`].

* `generate-self-signed-certificate`: Whether to generate a self signed certificate with the key. If set, `--certificate-ttl` must be provided.

* `certificate-ttl`: TTL in days for the generated certificate. Required only for generate-self-signed-certificate.

* `certificate-format`: The format of the returned certificate can be `pem` or `der`.

* `conf-file-path`: Path to the configuration file that contains CSR config data.

Upon successful creation, we will have a Private Key with a Self-Signed Certificate valid for a year, that we will use as a **Signer Key** for our [PKI Cert Issuer](doc:ssh-and-pkitls-certificates). 

## Create a PKI Cert Issuer

Run the following command to create a **PKI Cert Issuer** with **ACME Server**:

```shell
akeyless create-pki-cert-issuer \
--name /ACME/Server/ACMEIssuer \
--signer-key-name /ACME/Server/SignerKey \
--gw-cluster-url 'https://<Your-Akeyless-GW-URL:8000>' \
--destination-path /ACME/Server/Certificates \
--ttl 90d \
--allowed-domains acme.com \
--enable-acme true
```

Where:

* `name`: A unique name for the PKI issuer. The name can include a path to the virtual folder where you want to create a new PKI cert issuer using the slash / separators. If the folder does not exist, it will be created together with the item.

* `signer-key-name`: The **Signer Key** that was created earlier which will sign the certificates.

* `gw-cluster-url`: Akeyless Gateway Configuration Manager URL (port `8000`).

* `destination-path`: A path in Akeyless to save generated certificates.

* `ttl`: The requested TTL for the issued certificate, Maximum **90 days**.

* `allowed-domains`: Allowed domains that clients can request to be included in the certificate.

* `enable-acme`: Enable  **ACME Server**.

Upon successful creation,  the generated **ACME Server**  URL will use the following format:

`https://<Your-Akeyless-GW-URL:8000/acme/<issuer-display-id>/directory` 

To extract the `issuer-display-id`  from the CLI, run the following command:

```shell
akeyless describe-item \
--name /ACME/Server/ACMEIssuer | jq -r '.display_id'
```

Alternatively, you can extract the full **ACME Server** URL from the console. 

# External Account Binding

**External Account Binding**, defined in the [ACME Protocol RFC 8555](https://datatracker.ietf.org/doc/html/rfc8555/#section-7.3.4), is a feature that improves the security of certificate issuance by connecting certificate requests to specific accounts. This ensures that only authorized clients can request and receive certificates for those accounts, making the process much safer.

Run the following command to generate an external account binding token which will be restricted for one-time use and valid only for **1 Hour**  for the registration of a new client: 

```shell
akeyless generate-acme-eab \
--cert-issuer-name /ACME/Server/ACMEIssuer
```

Upon successful generation of an external account binding token, the following will be presented:

```shell
{
  "kid": "...",
  "mac_key": "...",
  "expires_at": "..."
}
```

Where:

* `kid`: The **Key Identifier** for the external account will be used by the **ACME client**.

* `mac_key`: The **HMAC key** for the external account will be used by the **ACME client**.

This external account binding token will be used to register an **ACME client** to request a certificate from the **ACME server**.

## Request a Certificate

In the following example, we will request a certificate from the  **ACME server**, using  **Certbot**:

```shell Windows
certbot certonly --standalone --server https://<Your-Akeyless-GW-URL:8000/acme/<issuer-display-id>/directory --domain acme.com --eab-kid <kid> --eab-hmac-key <mac key> --config-dir  C:\Users\<username>\certbot\conf --work-dir C:\Users\<username>\certbot\work --logs-dir C:\Users\<username>\certbot\logs
```
```shell Linux
certbot certonly --standalone --server https://<Your-Akeyless-GW-URL:8000/acme/<issuer-display-id>/directory --domain acme.com --eab-kid <kid> --eab-hmac-key <mac key> --config-dir /home/ubuntu/certbot/conf --work-dir /home/ubuntu/certbot/work --logs-dir /home/ubuntu/certbot/logs
```

Where:

* `server`: The **ACME Server URL**, can be found under **ACME Server** tab on the **PKI Cert Issuer** in the console.

* `domain`: The domain name for which you want to issue the certificate, must be listed in the [PKI Cert Issuer](https://docs.akeyless.io/docs/acme-server#create-a-pki-cert-issuer) under the `Allowed domains list` field. 

* `eab-kid`: The external accounts binding  **Key Identifier** .

* `eab-hmac-key`: The external account binding **HMAC key**. 

Upon successful certificate request, the certificate will be issued.

# Manage External Accounts

Multiple external accounts can be created under the same **PKI Cert Issuer**, therefore, it's possible to monitor the status of each external account. These external accounts can be used to request certificates using external clients. Keeping track of external accounts' status helps ensure that only authorized users can create certificates and reduces potential security risks.

The following endpoints show how to list and deactivate external accounts when necessary.

## List External Accounts

To list the external accounts, both in the status of `valid` or `deactivated` run the following command:

```shell
akeyless list-acme-accounts \
--cert-issuer-name /ACME/Server/ACMEIssuer
```

The output of this command:

```shell
{
  "accounts": [
    {
      "account_id": "...",
      "key_digest": "...",
      "status": "valid"
    }
  ]
}
```

## Deactivate an External Account

To deactivate an external Account, run the following command:

```shell
akeyless deactivate-acme-account \
--cert-issuer-name /ACME/Server/ACMEIssuer \
--acme-account-id <account-id> \
--delete-account true / flase
```

Where:

* `cert-issuer-name`: The full path of the **PKI Cert Issuer** of the **ACME Server**.

* `acme-account-id`: The **Account ID** of the external account.

* `delete-account`: Set to `true` to delete the account.

You can find the complete list of parameters for these commands in the [CLI Reference - ACME](https://docs.akeyless.io/docs/cli-reference-certificates#acme) section.
