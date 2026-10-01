---
title: SCEP Server
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
[SCEP](https://datatracker.ietf.org/doc/html/rfc8894), or **Simple Certificate Enrollment Protocol**, allows clients and devices (for example, network equipment, MDM-managed endpoints, and other systems that speak SCEP) to request and enroll certificates from a Certificate Authority without requiring a full ACME or manual CSR workflow.

Akeyless supports creating a [PKI Cert Issuer](https://docs.akeyless.io/docs/ssh-and-pkitls-certificates) that deploys a **SCEP Server** on the [Gateway](https://docs.akeyless.io/docs/gateway-overview), with **static challenge** authentication for secure enrollment. This allows SCEP clients to automate certificate enrollment within the organization's security framework.

Before proceeding, ensure you have permission to manage **SCEP** on your Gateway.

## Enable SCEP Server

In this guide, we will create a **PKI Cert Issuer** with **SCEP Server** enabled and a static challenge password for client authentication.

### Create a Signer Key

Create a [DFC Key](https://docs.akeyless.io/docs/gateway-zero-knowledge#create-dfc-key-from-the-akeyless-console) with a self-signed certificate to use as the **Signer Key** for the **PKI Cert Issuer**, the same way as described in [Create a Signer Key](https://docs.akeyless.io/docs/acme-server#create-a-signer-key) for the ACME Server.

### Create a PKI Cert Issuer

Run the following command to create a **PKI Cert Issuer** with **SCEP Server** enabled:

```shell
akeyless create-pki-cert-issuer \
--name /SCEP/Server/SCEPIssuer \
--signer-key-name /SCEP/Server/SignerKey \
--gw-cluster-url 'https://<Your-Akeyless-GW-URL>:8000' \
--destination-path /SCEP/Server/Certificates \
--ttl 90d \
--allowed-domains acme.com \
--enable-scep true \
--scep-challenge-password <Static Challenge Password>
```

Where:

* `name`: A unique name for the PKI issuer. The name can include a path to the virtual folder where you want to create a new PKI cert issuer using the slash `/` separators. If the folder does not exist, it will be created together with the item.

* `signer-key-name`: The **Signer Key** that will sign the certificates.

* `gw-cluster-url`: Akeyless Gateway Console URL (port `8000`).

* `destination-path`: A path in Akeyless to save generated certificates.

* `ttl`: The requested TTL for the issued certificate.

* `allowed-domains`: Allowed domains that clients can request to be included in the certificate.

* `enable-scep`: Enable **SCEP Server**.

* `scep-challenge-password`: The static challenge password SCEP clients must present during enrollment (see **Static Challenge Authentication** below).

Upon successful creation, the generated **SCEP Server** URL will use a format similar to:

`https://<Your-Akeyless-GW-URL>:8000/scep/<issuer-display-id>`

Alternatively, you can extract the full **SCEP Server** URL from the console, on the **SCEP Server** tab of the **PKI Cert Issuer**.

## Static Challenge Authentication

Akeyless SCEP enrollment uses a two-stage flow:

* **Stage 1 - Static Verification**: The SCEP client submits its enrollment request together with the static challenge password configured on the **PKI Cert Issuer** (`scep-challenge-password`). Akeyless verifies the password before proceeding; requests with a missing or incorrect password are rejected at this stage.

* **Stage 2 - Certificate Issuance**: Once the static challenge password is verified, Akeyless signs and returns the certificate to the client using the configured **Signer Key**.

<Callout icon="ℹ️" theme="info">
  ### **Note:**

  Rotate the static challenge password periodically and distribute it to SCEP clients through a secure, out-of-band channel.
</Callout>

### Request a Certificate

In the following example, we request a certificate from the **SCEP server** using a generic SCEP client (for example, [sscep](https://github.com/certnanny/sscep)):

```shell
sscep enroll \
-u https://<Your-Akeyless-GW-URL>:8000/scep/<issuer-display-id> \
-c ca.crt \
-k client.key \
-r client.csr \
-l client.crt \
-t 60 \
-n 5
```

Where the CSR used for enrollment includes the static challenge password (configured via `scep-challenge-password`) in its `challengePassword` attribute.

Upon successful verification of the static challenge, the certificate will be issued.

You can find the complete list of parameters for `create-pki-cert-issuer` in the [CLI Reference - Certificates](https://docs.akeyless.io/docs/cli-reference-certificates#create-pki-cert-issuer) section.
