---
title: Google CA Target
deprecated: false
hidden: false
metadata:
  robots: index
---
The [Google CA](https://cloud.google.com/security/products/certificate-authority-service?hl=en) Target enables the use of **Google CA** as a Public Certificate Authority (CA) with an Akeyless [PKI Issuer](https://docs.akeyless.io/docs/ssh-and-pkitls-certificates).

With a public CA, Akeyless cannot access the private key that signs certificates. Akeyless validates certificate issuance requests by connecting to **Google CA** through the [Akeyless Gateway](https://docs.akeyless.io/docs/gateway-overview).

The **Google CA** integration uses an [ACME Client (v2)](https://datatracker.ietf.org/doc/html/rfc8555).

To prove domain ownership, the Akeyless integration supports DNS validation:

* **DNS validation**: Ownership is proven by adding a DNS TXT record. This requires the domain to be managed in a supported DNS provider's hosted zone (for example, Amazon Route 53, GCP Cloud DNS, or Azure DNS).

## Create a Google CA Target with the CLI

To create a Google CA target with the CLI, use one of the following examples based on the challenge method and DNS provider:

```shell DNS with AWS
akeyless target create google-trust \
--name <Target Name> \
--google-trust-url <production / staging> \
--email <ACME Account Email> \
--eab-key-id <EAB Key ID> \
--eab-hmac-key <EAB HMAC Key> \
--acme-challenge dns \
--dns-target-creds <AWS DNS Target Name> \
--hosted-zone <Route53 Hosted Zone ID>
```
```shell DNS with GCP
akeyless target create google-trust \
--name <Target Name> \
--google-trust-url <production / staging> \
--email <ACME Account Email> \
--eab-key-id <EAB Key ID> \
--eab-hmac-key <EAB HMAC Key> \
--acme-challenge dns \
--dns-target-creds <GCP DNS Target Name> \
--gcp-project <GCP Project ID>
```
```shell DNS with Azure
akeyless target create google-trust \
--name <Target Name> \
--google-trust-url <production / staging> \
--email <ACME Account Email> \
--eab-key-id <EAB Key ID> \
--eab-hmac-key <EAB HMAC Key> \
--acme-challenge dns \
--dns-target-creds <Azure DNS Target Name> \
--resource-group <Azure Resource Group Name>
```
```shell DNS with Cloudflare
akeyless target create google-trust \
--name <Target Name> \
--google-trust-url <production / staging> \
--email <ACME Account Email> \
--eab-key-id <EAB Key ID> \
--eab-hmac-key <EAB HMAC Key> \
--acme-challenge dns \
--dns-target-creds <Cloudflare DNS Target Name> \
--dns-zone <Cloudflare DNS Zone>
```

Where:

* `name`: A unique name for the target. The name can include a path to a virtual folder by using slash `/` separators. If the folder does not exist, Akeyless creates it with the target.

* `email`: Email address used for ACME account registration.

* `eab-key-id`: External Account Binding Key ID from Google CA Services.

* `eab-hmac-key`: External Account Binding HMAC Key from Google CA Services.

* `google-trust-url`: Use this when you want to select the ACME environment explicitly. Supported values are `production` (default) and `staging`.

* `acme-challenge`: Use this when you need DNS validation or want to set the challenge type explicitly.

* `dns-target-creds`: Use this when `--acme-challenge=dns`. This is required for DNS validation. Supported target types are AWS, Azure, GCP, and Cloudflare.

* `dns-zone`: Use this when `--acme-challenge=dns` and `--dns-target-creds` points to a Cloudflare target.

* `hosted-zone`: Use this when `--acme-challenge=dns` and `--dns-target-creds` points to an AWS target. This identifies the Route 53 hosted zone.

* `resource-group`: Use this when `--acme-challenge=dns` and `--dns-target-creds` points to an Azure target.

* `gcp-project`: Use this when `--acme-challenge=dns` and `--dns-target-creds` points to a GCP target and the project ID cannot be derived automatically.

* `timeout`: Use this when challenge validation needs a custom wait time. Default is `5m`. Supported range is `1m` to `1h`.

* `key`: Use this when you want to encrypt target secret values with a specific protection key instead of the account default key.

[View the complete list of parameters for this command.](https://docs.akeyless.io/docs/cli-ref-targets#lets-encrypt)

## Create a Google CA Target in the Console

1. Log in to the Akeyless Console, and go to **Targets**, then **New**, then **Certificate Automation (Google CA)**.

2. Define the Name of the target, and specify the Location as a path to the virtual folder where you want to create the new target, using slash `/` separators. If the folder does not exist, it will be created together with the target.

3. Select a **Protection key** with a Customer Fragment to enable Zero-Knowledge and click **Next**. [Read more about Zero-Knowledge Encryption](https://docs.akeyless.io/docs/gateway-zero-knowledge).

4. Define the remaining parameters as follows:
   * **Email**: Email address used to register the ACME account.

   * **URL**: Either [Production](https://acme-v02.api.letsencrypt.org/directory) or [Staging](https://acme-staging-v02.api.letsencrypt.org/directory).

   * **EAB KID**: External Account Binding Key ID from Google CA Services.

   * **EAB HMAC Key**: External Account Binding HMAC Key from Google CA Services.

   * **DNS Provider**: Either **AWS**, **GCP**, **Azure**, or **Cloudflare** (relevant only if **Challenge Type** is **DNS**).

   * **Target**: Select a target that contains the DNS provider credentials (relevant only if **Challenge Type** is **DNS**).

   * **Hosted Zone**: [Amazon Route 53](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/hosted-zones-working-with.html) hosted zone identifier. (Relevant only if **Challenge Type** is **DNS** and **DNS Provider** is **AWS**).

   * **Resource Group**: Azure resource group name. (Relevant only if **Challenge Type** is **DNS** and **DNS Provider** is **Azure**).

   * **GCP Project**: GCP Cloud DNS project ID. Optional when **DNS Provider** is **GCP**.

   * **DNS Zone**: Cloudflare DNS zone name. Relevant only when **DNS Provider** is **Cloudflare**.

   * **Timeout**: Challenge validation timeout in seconds. Default is 300 seconds (5 minutes).

5. Click Finish.
