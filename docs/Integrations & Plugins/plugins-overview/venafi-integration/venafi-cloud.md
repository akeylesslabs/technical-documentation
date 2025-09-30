---
title: Venafi Cloud
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
To work with the Venafi Cloud platform, you can choose either to work with Venafi as your certificate issuer or to work with Akeyless as your issuer.

## Prerequisites

* Akeyless [Gateway](doc:api-gw)

* Venafi Cloud

## Usage

**Venafi Issuer**

The following command creates a Venafi **Dynamic Secret** using Venafi as the **certificate issuer**.

```shell
akeyless dynamic-secret create venafi \
  --name my-venafi-dynamic-secret \
  --gateway-url 'https://<Your-Akeyless-GW-URL:8000>' \
  --venafi-api-key <YOUR VENAFI API KEY> \
  --venafi-zone <YOUR VENAFI ZONE>
```

Where:

`name`: Dynamic secret name.

`gateway-url`: Akeyless Gateway Configuration Manager URL (port `8000`).

`venafi-api-key`: Venafi API key.

`venafi-zone`:  The Venafi zone to use when issuing new certificates (policies will be pulled from here) - for example: `<Application_Name>/<Issuing_template_name>`

**Akeyless Issuer**

The following commands create a Venafi **Dynamic Secret** using Akeyless as the **certificate issuer**.

When using Akeyless as the issuer, first, you need to create an RSA key with a **self-signed certificate** attached:

```shell
akeyless create-dfc-key \
--name venafi-cloud \
--alg RSA2048 \
--generate-self-signed-certificate \
--certificate-common-name venafi-cloud \
--certificate-ttl 10
```

Where:

`name`: A unique name for the encryption key. The name can include the path to the virtual folder where you want to create the new authentication method, using slash / separators. If the folder does not exist, it will be created together with the encryption key.

`alg`: Supporting algorithms: `RSA1024`,`RSA2048`, `RSA3072` `RSA4096`.

`generate-self-signed-certificate`: Generate a self-signed certificate.

`certificate-common-name`: Common name for the generated certificate.

`certificate-ttl`: TTL in days for the generated certificate.

**Note: Once the key is created, it will be uploaded automatically to Akeyless.**

The certificate attached to the private key must have at least a Common Name (CN) with it.

Create the Venafi **Dynamic Secret** in Akeyless gateway:

```shell
akeyless dynamic-secret create venafi \
  --name my-venafi-dynamic-secret \
  --gateway-url 'https://<Your-Akeyless-GW-URL:8000>' \
  --venafi-api-key <YOUR VENAFI API KEY> \
  --venafi-zone <YOUR VENAFI ZONE> \
  --allowed-domains '[*]' \
  --allow-subdomains \
  --sign-using-akeyless-pki \
  --signer-key-name venafi-cloud \
  --user-ttl 2160h
```

Where:

`name`: Dynamic secret name.

`gateway-url`: Akeyless Gateway Configuration Manager URL (port `8000`).

`venafi-api-key`: Venafi-API-Key.

`venafi-zone`:  Venafi zone.

`allowed-domains:` List of allowed-domains.

`allow-subdomains`: Whether to allow subdomains.

`sign-using-akeyless-pki`: Issue certificates using Akeyless PKI.

`signer-key-name`: Signer key name in Akeyless.

Once your Venafi dynamic secret has been successfully created, you can request a new certificate.

**Certificate request**:

Certificate request using **Common Name (CN)**:

```shell
akeyless get-dynamic-secret-value \
  -n my-venafi-dynamic-secret \
  --args common_name=any-common-name.company.example.com
```

Certificate request using a **Certificate Signing Request (CSR)**:

To fetch a new certificate via **CSR** , you need to create your **CSR** in Akeyless:

```shell
CSR=$(akeyless generate-csr \
--name venafi-test \
--generate-key \
--key-type dfc \
--alg RSA2048 \
--common-name marketing.newyork.company.com | base64)
```

Get the Dynamic Secret using the **Certificate request:**

```shell
akeyless get-dynamic-secret-value \
  -n my-venafi-dynamic secret \
  --args csr=$CSR
```

In the response you’ll see the relevant information and artifacts for the request including the `certificate`, `serial number`, `common name`, and `expiration`.

Depending on your flow you may also see the `certificate chain`, `issuing ca`, `ca chain`, and `private key`.

The artifacts `certificate`, `certificate chain`, and `private key`can also be found as Static Secrets under the Artifacts Folder defined in the Dynamic Secret's settings.
