---
title: Venafi Trust Protection Platform (TPP)
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
To work with Venafi TPP, you can choose either to work with Venafi as your certificate issuer or to work with Akeyless as your issuer. 

## Prerequisites

* Akeyless [Gateway](doc:api-gw).

* Venafi TPP.

## Usage

**Venafi Issuer** 

The following command creates a Venafi Dynamic Secret using Venafi as the **certificate issuer**:

```shell
akeyless dynamic-secret create venafi \
  --name my-venafi-dynamic-secret \
  --gateway-url 'https://<Your-Akeyless-GW-URL:8000>' \
  --venafi-use-tpp \
  --venafi-access-token <Venafi Access Token> \
  --venafi-refresh-token <Venafi Refresh Token> \
  --venafi-baseurl <YOUR TPP ENVIRONMENT BASE URL> \
  --venafi-zone <YOUR VENAFI ZONE>
```

Where:

`name`: A unique name of the Dynamic Secret. The name can include the path to the virtual folder where you want to create the new dynamic secret, using the slash/separators. If the folder does not exist, it will be created together with the Dynamic Secret.

`gateway-url`: Akeyless Gateway Configuration Manager URL (port `8000`).

`venafi-use-tpp`: Required when working with TPP. 

`venafi-access-token`: Venafi Access Token to use to access the TPP environment (Relevant when using TPP).

`venafi-refresh-token`: Venafi Refresh Token to use when the Access Token is expired (Relevant when using TPP).

`venafi-baseurl`: Base URL of the TPP environment. Or Cloud environment which isn't [https://venafi.cloud/](https://venafi.cloud/).

`venafi-zone`: Venafi Zone.

**Akeyless Issuer**

The following commands create a Venafi Dynamic Secret using Akeyless as the **certificate issuer**.

When using Akeyless as the issuer, first, you need to create an RSA key with a **self-signed certificate** attached: 

```shell
akeyless create-dfc-key \
--name venafi-tpp \
--alg RSA2048 \
--generate-self-signed-certificate \
--certificate-common-name venafi-test \
--certificate-ttl 10
```

Where:

`name`: A unique name for the encryption key. The name can include the path to the virtual folder where you want to create the new authentication method, using slash / separators. If the folder does not exist, it will be created together with the encryption key.

`alg`: Supporting algorithms: `RSA1024`,`RSA2048`, `RSA3072` `EC256`, `EC384`, `EC521` (`EC` type is relevant for **Classic key** only).

`generate-self-signed-certificate`: Generate a self-signed certificate with the key.

`certificate-common-name`: Common name for the generated certificate.

`certificate-ttl`: TTL in days for the generated certificate.

**Note: Once the key is created, it will be uploaded automatically to Akeyless.**

The certificate attached to the private key must have at least a **Common Name (CN)** with it. 

Create the Venafi Dynamic Secret in Akeyless gateway: 

```shell
akeyless dynamic-secret create venafi \
  --name my-venafi-dynamic-secret \
  --gateway-url 'https://<Your-Akeyless-GW-URL:8000>' \
  --sign-using-akeyless-pki \
  --signer-key-name venafi-tpp \
  --allowed-domains '[*]' \
  --allow-subdomains \
  --user-ttl 2160h \
  --venafi-use-tpp \
  --venafi-access-token <Venafi Access Token> \
  --venafi-refresh-token <Venafi Refresh Token> \
  --venafi-baseurl <YOUR TPP ENVIRONMENT BASE URL> \
  --venafi-zone <YOUR VENAFI ZONE>
```

Where:

`name`: A unique name of the Dynamic Secret. The name can include the path to the virtual folder where you want to create the new dynamic secret, using the slash/separators. If the folder does not exist, it will be created together with the Dynamic Secret.

`gateway-url`: Akeyless Gateway Configuration Manager URL (port `8000`).

`sign-using-akeyless-pki`: Creating certificates using Akeyless PKI.

`signer-key-name`: Signer key name in Akeyless.

`allowed-domains`: List of allowed-domains.

`allow-subdomains`:  whether subdomains are allowed or not.

`-user-ttl`: User TTL.

`venafi-use-tpp`: Required when working with TPP.

`venafi-access-token`: Venafi Access Token to use to access the TPP environment (Relevant when using TPP).

`venafi-refresh-token`: Venafi Refresh Token to use when the Access Token is expired (Relevant when using TPP).

`venafi-baseurl`: Base URL of the TPP environment. Or a Cloud environment which isn't [https://venafi.cloud/](https://venafi.cloud/).

`venafi-zone`: Venafi Zone.

Once your Venafi Dynamic Secret has been successfully created, you can request a new **certificate**.

**Certificate request**:

Certificate request using **Common Name (CN)**: 

```shell
akeyless get-dynamic-secret-value \
  -n my-venafi-dynamic-secret \
  --args common_name=any-common-name.company.example.com
```

Certificate request via **Certificate Signing Request (CSR)**:

To fetch a new certificate via **CSR**, you need to create your **CSR** and send it to the Akeyless gateway in base64 encoding.

Create a **CSR**: 

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
  -n my-venafi-dynamic-secret \
  --args csr=$CSR
```

In the response, you’ll see the relevant information and artifacts for the request including the `certificate`, `serial number`, `common name` and `expiration`.

 Depending on your flow you may also see the `certificate chain`, `issuing ca`, `ca chain`, and `private key`. 

The artifacts `certificate`, `certificate chain` and `private key` can also be found as static secrets under the Artifacts Folder defined in the dynamic secret's settings.
