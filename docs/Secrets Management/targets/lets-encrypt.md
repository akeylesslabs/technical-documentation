---
title: Let's Encrypt Target
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
The [Let's Encrypt](https://letsencrypt.org/) Target enables the use of **Let's Encrypt** as a Public Certificate Authority (CA) with an Akeyless [PKI Issuer](https://docs.akeyless.io/docs/ssh-and-pkitls-certificates).

With a public CA, Akeyless cannot access the private key that signs certificates. Akeyless validates certificate issuance requests by connecting to **Let's Encrypt** through the [Akeyless Gateway](https://docs.akeyless.io/docs/gateway-overview).

The Let's Encrypt integration uses an [ACME Client (v2)](https://datatracker.ietf.org/doc/html/rfc8555).

To prove domain ownership, Let's Encrypt requires an ACME challenge. Let's Encrypt documents `HTTP-01`, `DNS-01`, and `TLS-ALPN-01` challenge methods. For the Akeyless Let's Encrypt target, the supported challenge types are:

* `http` (default)
* `dns`

To prove domain ownership, the Akeyless integration supports the following validation methods:

* **DNS validation**: Ownership is proven by adding a DNS TXT record. This requires the domain to be managed in a supported DNS provider's hosted zone (for example, Amazon Route 53, GCP Cloud DNS, or Azure DNS).

* **HTTP validation**: Ownership is proven by hosting a challenge file at `http://<YOUR_DOMAIN>/.well-known/acme-challenge/` and returning the expected value during validation.

## Before You Begin

* Ensure an [Akeyless Gateway](https://docs.akeyless.io/docs/gateway-overview) is deployed and reachable.
* For DNS challenge flows, create the DNS provider target before creating the Let's Encrypt target.
* Confirm that the DNS target has permissions to manage TXT records in the relevant zone.
* Use the ACME `staging` environment for initial validation before switching to `production`.

## Choose a Validation Method

Choose one of the supported challenge types based on the DNS and web access model in your environment:

* **DNS challenge (`dns`)**: Recommended when DNS automation is available. This method requires a DNS provider target and provider-specific DNS parameters.
* **HTTP challenge (`http`)**: Recommended when a challenge file can be served from `/.well-known/acme-challenge/` on the requested domain.

Use the sections below to configure the target and complete certificate issuance for your selected method.

## Configure the Let's Encrypt Target

### Use the CLI

Use the following examples based on challenge type and DNS provider.

#### DNS challenge examples

```shell DNS with AWS
akeyless target create lets-encrypt \
--name <Target Name> \
--email <ACME Account Email> \
--acme-challenge dns \
--dns-target-creds <AWS DNS Target Name> \
--hosted-zone <Route53 Hosted Zone ID>
```
```shell DNS with GCP
akeyless target create lets-encrypt \
--name <Target Name> \
--email <ACME Account Email> \
--acme-challenge dns \
--dns-target-creds <GCP DNS Target Name> \
--gcp-project <GCP Project ID>
```
```shell DNS with Azure
akeyless target create lets-encrypt \
--name <Target Name> \
--email <ACME Account Email> \
--acme-challenge dns \
--dns-target-creds <Azure DNS Target Name> \
--resource-group <Azure Resource Group Name>
```
```shell DNS with Cloudflare
akeyless target create lets-encrypt \
--name <Target Name> \
--email <ACME Account Email> \
--acme-challenge dns \
--dns-target-creds <Cloudflare DNS Target Name> \
--dns-zone <Cloudflare DNS Zone>
```

#### HTTP challenge example

```shell
akeyless target create lets-encrypt \
--name <Target Name> \
--email <ACME Account Email> \
--acme-challenge http
```

#### Key CLI flags

* `name`: A unique name for the target. The name can include a path to a virtual folder by using slash `/` separators. If the folder does not exist, Akeyless creates it with the target.

* `email`: Email address used for ACME account registration.

* `lets-encrypt-url`: Use this when you want to select the ACME environment explicitly. Supported values are `production` (default) and `staging`.

* `acme-challenge`: Use this when you need DNS validation or want to set the challenge type explicitly. Supported values are `http` (default) and `dns`.

* `dns-target-creds`: Use this when `--acme-challenge=dns`. This is required for DNS validation. Supported target types are AWS, Azure, GCP, and Cloudflare.

* `dns-zone`: Use this when `--acme-challenge=dns` and `--dns-target-creds` points to a Cloudflare target.

* `hosted-zone`: Use this when `--acme-challenge=dns` and `--dns-target-creds` points to an AWS target. This identifies the Route 53 hosted zone.

* `resource-group`: Use this when `--acme-challenge=dns` and `--dns-target-creds` points to an Azure target.

* `gcp-project`: Use this when `--acme-challenge=dns` and `--dns-target-creds` points to a GCP target and the project ID cannot be derived automatically.

* `timeout`: Use this when challenge validation needs a custom wait time. Default is `5m`. Supported range is `1m` to `1h`.

* `key`: Use this when you want to encrypt target secret values with a specific protection key instead of the account default key.

[View the complete list of parameters for this command.](https://docs.akeyless.io/docs/cli-ref-targets#lets-encrypt)

### Use the Console

1. Log in to the Akeyless Console, and go to **Targets**, then **New**, then **Certificate Automation (Let's Encrypt)**.

2. Define the Name of the target, and specify the Location as a path to the virtual folder where you want to create the new target, using slash `/` separators. If the folder does not exist, it will be created together with the target.

3. Select a **Protection key** with a Customer Fragment to enable Zero-Knowledge and click **Next**. [Read more about Zero-Knowledge Encryption](https://docs.akeyless.io/docs/gateway-zero-knowledge).

4. Define the remaining parameters as follows:

* **Server URL**: Either [Production](https://acme-v02.api.letsencrypt.org/directory) or [Staging](https://acme-staging-v02.api.letsencrypt.org/directory).

* **Email**: Email address used to register the ACME account.

* **Challenge Type**: Either **HTTP** or **DNS**.

* **DNS Provider**: Either **AWS**, **GCP**, or **Azure** (relevant only if **Challenge Type** is **DNS**).

* **Target**: Select a target that contains the DNS provider credentials (relevant only if **Challenge Type** is **DNS**).

* **Hosted Zone**: [Amazon Route 53](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/hosted-zones-working-with.html) hosted zone identifier. (Relevant only if **Challenge Type** is **DNS** and **DNS Provider** is **AWS**).

* **Resource Group**: Azure resource group name. (Relevant only if **Challenge Type** is **DNS** and **DNS Provider** is **Azure**).

* **GCP Project**: GCP Cloud DNS project ID. Optional when **DNS Provider** is **GCP**.

* **Timeout**: Challenge validation timeout in seconds. Default is 300 seconds (5 minutes).

> ℹ️ **Note:**
>
> Cloudflare DNS configuration for Let's Encrypt is available through the CLI flow.

1. Click Finish.

## Configure DNS Provider Authentication (Optional)

For DNS challenge flows, a provider target can use Gateway cloud identity instead of static credentials.

### Gateway Cloud Identity Examples

The following examples show how to create DNS provider targets with Gateway cloud identity for AWS, Azure, and GCP.

```shell AWS
# Create the DNS provider target with Gateway cloud identity
akeyless target create aws \
--name <AWS DNS Target Name> \
--use-gw-cloud-identity \
--region <AWS Region>
```
```shell Azure
# Create the DNS provider target with Gateway cloud identity
akeyless target create azure \
--name <Azure DNS Target Name> \
--connection-type cloud-identity \
--subscription-id <Azure Subscription ID> \
--resource-group-name <Azure DNS Resource Group Name>
```
```shell GCP
# Create the DNS provider target with Gateway cloud identity
akeyless target create gcp \
--name <GCP DNS Target Name> \
--use-gw-cloud-identity
```

## DNS Provider Permissions for DNS-01

When using `dns` challenge validation, the cloud target referenced by `dns-target-creds` must have permission to create and update ACME TXT records in the relevant DNS zone.

Required permissions by provider:

* **AWS Route 53**
    * **Required for DNS-01 record changes**: `route53:ChangeResourceRecordSets` on the target hosted zone.
    * **Common read permissions** (if zone lookup or record inspection is needed): `route53:GetHostedZone`, `route53:ListHostedZonesByName`, and `route53:ListResourceRecordSets`.
    * Reference: [Actions, resources, and condition keys for Amazon Route 53](https://docs.aws.amazon.com/service-authorization/latest/reference/list_amazonroute53.html) and [Permissions required to use the Route 53 API](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/r53-api-permissions-ref.html)

* **GCP Cloud DNS**
    * **Required for DNS-01 record changes**: `dns.changes.create` and the relevant record set permission (`dns.resourceRecordSets.create`, `dns.resourceRecordSets.update`, and/or `dns.resourceRecordSets.delete`).
    * **Common read permissions**: `dns.managedZones.get`, `dns.managedZones.list`, `dns.resourceRecordSets.get`, and `dns.resourceRecordSets.list`.
    * Reference: [Access control with IAM](https://docs.cloud.google.com/dns/docs/access-control)

* **Azure DNS**
    * **Recommended built-in role**: **DNS Zone Contributor** at the DNS zone scope.
    * This role includes `Microsoft.Network/dnsZones/*` (manage DNS zones and record sets).
    * Reference: [Azure built-in roles for Networking - DNS Zone Contributor](https://learn.microsoft.com/en-us/azure/role-based-access-control/built-in-roles/networking#dns-zone-contributor)

### Troubleshoot DNS challenge flows

If certificate issuance fails during DNS challenge validation, validate the following:

* The `dns-target-creds` target exists and is configured for the expected provider.
* The DNS challenge field for the selected provider is set correctly:
    * AWS: `hosted-zone`
    * Azure: `resource-group`
    * GCP: `gcp-project` (when project ID cannot be derived automatically)
* The domain requested in the certificate is hosted in the DNS zone managed by the provider target.
* The Gateway has network access to the provider DNS APIs.
* The identity used by the provider target has permissions to create and update TXT records for ACME validation.

> ℹ️ **Note (Least Privilege):**
>
> Scope permissions to only the DNS zones and record operations required for certificate validation.

## Issue Certificates With HTTP Challenge

When the Let's Encrypt target is configured with `--acme-challenge=http`, certificate issuance is a two-phase flow:

1. Request the certificate:

```shell
akeyless get-pki-certificate \
--cert-issuer-name <PKI Issuer Name> \
--csr-file-path <path/to/request.csr>
```

1. Deploy the challenge file to the URL path returned in `http_challenge_info.file_path` using the value in `http_challenge_info.file_content`.

1. Finalize validation and issuance:

```shell
akeyless validate-certificate-challenge \
--cert-display-id <Certificate Display ID> \
--timeout 120
```

1. Retrieve the issued certificate value:

```shell
akeyless get-certificate-value \
--cert-issuer-name <PKI Issuer Name> \
--display-id <Certificate Display ID>
```

> ℹ️ **Note:**
>
> `validate-certificate-challenge` is required for HTTP challenge flows. DNS challenge flows do not require this additional validation command.
> For a PKI issuer that uses a Let's Encrypt target, requested TTL values in certificate requests can be between 30 and 90 days. The issued Let's Encrypt certificate validity is fixed at 90 days.
