---
title: SCEP Server
excerpt: 'Deploy a SCEP Server on your Gateway to let devices enroll for certificates automatically.'
deprecated: false
hidden: false
metadata:
  title: 'SCEP Server'
  description: 'Configure a PKI Cert Issuer with a SCEP Server and static challenge authentication for automated device certificate enrollment.'
  robots: index
---
[SCEP](https://datatracker.ietf.org/doc/html/rfc8894), or **Simple Certificate Enrollment Protocol**, allows network devices and endpoint management systems to request certificates automatically, without a person generating a CSR for each device. It is widely supported by MDM platforms, network equipment, and operating system certificate clients.

The SCEP protocol uses a **challenge password** to authenticate enrollment requests, ensuring that only authorized clients can obtain certificates from the server.

Akeyless supports creating a [PKI Cert Issuer](https://docs.akeyless.io/docs/ssh-and-pkitls-certificates) that deploys a **SCEP Server** on the [Gateway](https://docs.akeyless.io/docs/gateway-overview), with **static challenge** support for client authentication. This allows SCEP clients to enroll for certificates within the organization's existing chain of trust.

Before proceeding, ensure you have permission to manage certificate issuers on your Gateway.

## Enable SCEP Server

### Create a Signer Key

The SCEP Server signs certificates using a **Signer Key** on the PKI Cert Issuer. If you do not already have one, follow [PKI Certificate Issuer](https://docs.akeyless.io/docs/ssh-and-pkitls-certificates) to upload an existing CA key or generate a new RSA key with a self-signed certificate.

### Create a PKI Cert Issuer with SCEP

Run the following command to create a **PKI Cert Issuer** with a **SCEP Server**:

```shell
akeyless create-pki-cert-issuer \
--name /SCEP/Server/SCEPIssuer \
--signer-key-name /SCEP/Server/SignerKey \
--gw-cluster-url 'https://<Your-Akeyless-GW-URL>:8000' \
--destination-path /SCEP/Server/Certificates \
--ttl 90d \
--allowed-domains scep.com \
<TBC: enable-scep flag> \
<TBC: static challenge flag>
```

Where:

* `name`: A unique name for the PKI issuer. The name can include a path to the virtual folder where you want to create a new PKI cert issuer using the slash / separators. If the folder does not exist, it will be created together with the item.

* `signer-key-name`: The **Signer Key** which will sign the issued certificates.

* `gw-cluster-url`: Akeyless Gateway Console URL (port `8000`).

* `destination-path`: A path in Akeyless to save generated certificates.

* `ttl`: The requested TTL for the issued certificate.

* `allowed-domains`: Allowed domains that clients can request to be included in the certificate.

* `<TBC: enable flag>`: Enable **SCEP Server**.

* `<TBC: challenge flag>`: The static challenge password that clients must present when enrolling.

Upon successful creation, the generated **SCEP Server** URL will use the following format:

`<TBC: URL format>`

To extract the `issuer-display-id` with the CLI, run the following command:

```shell
akeyless describe-item \
--name /SCEP/Server/SCEPIssuer | jq -r '.display_id'
```

Alternatively, you can extract the full **SCEP Server** URL from the console.

## Static Challenge Authentication

SCEP clients authenticate to the server by presenting a **challenge password** with the enrollment request. Akeyless supports a **static challenge**: a single value configured on the issuer and shared by every client enrolling against it.

<Callout icon="⚠️" theme="warn">
  ### **Scope the issuer accordingly:**

  A static challenge does not expire on use and is shared across all clients of the issuer. Restrict the issuer's **Allowed Domains**, keep the `ttl` short, and treat the challenge value as a secret.
</Callout>

### Enroll a Client

<TBC: client enrollment example>

## Related Pages

- [PKI Certificate Issuer](https://docs.akeyless.io/docs/ssh-and-pkitls-certificates)
- [ACME Server](https://docs.akeyless.io/docs/acme-server)
- [Certificate Renewal](https://docs.akeyless.io/docs/certificate-renewal)
