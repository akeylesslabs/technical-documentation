---
title: Certificate Revocation List
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
Akeyless enables you to proactively revoke certificates before their scheduled expiration date and seamlessly add them to a **Certificate Revocation List (CRL)**, ensuring enhanced security and trust in your certificate management process. Each [PKI Cert Issuer](https://docs.akeyless.io/docs/ssh-and-pkitls-certificates) generates a consistent **Certificate Revocation List (CRL)** for all its issued certificates. 

> 📘 Note
>
> Your PKI Issuer **Signer Key** must be set with the `keyusage:critical,cRLSign` extension to maintain a  **CRL** and support self-signed certificate revocation.

# Revoke a certificate using the Akeyless CLI

To revoke a certificate from the CLI, run the following command:

```shell
akeyless revoke-certificate \
--name <Certificate name> \
--version <Certificate version>
```

Where:

* `name`: The certificate's full name. Alternatively, it can be provided using `item-id`.
* `version`: Certificate version to revoke.

Upon successful revocation, the certificate status will change from **Valid** to **Revoked**.

You can find the complete list of parameters for this command in the [CLI-Reference-Certificates](https://docs.akeyless.io/docs/cli-reference-certificates#p-stylecolorbluerevoke-certificatep) section.

# Revoke a certificate using the Akeyless Console

To revoke a certificate from the console:

1. Log in to the Akeyless Console, go to **Items**, and find the certificate you wish to revoke.
2. Click on the **Certificate**, open the Action Menu (three dots), and click **Revoke**.

# Revocation List

Once the certificate is revoked, it is added to the **Certificate Revocation List**. For each issuer the following formats are maintaining the revocation list when applicable: 

**Public CRL** at: `https://vault.akeyless.io/crl/<account-id>/<cert-issuer-display-id>`.

**Private CRL** endpoint on the [Gateway](https://docs.akeyless.io/docs/api-gw) at `https://<gatewayURL:8000>/crl/<cert-issuer-display-id>`.

To view any existing **Certificate Revocation List** information on a **Certificate Item** click the  **View Certificate Details** and scroll down to **CRL Distribution points**, where the **CRL Endpoints** will be listed.
