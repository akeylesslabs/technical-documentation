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

## Before You Begin

- Ensure an [Akeyless Gateway](https://docs.akeyless.io/docs/gateway-overview) is deployed and reachable.
- Create a DNS provider target before creating the Google CA target.
- Confirm that the DNS target has permissions to manage TXT records in the relevant zone.
- Collect Google CA external account binding (EAB) values: `eab-key-id` and `eab-hmac-key`.

## Validation Method

DigiCert public CA integration in Akeyless uses **DNS** and **HTTP** challenge for domain ownership validation.

## Configure the Google CA Target

### Use the CLI

Use one of the following DNS challenge examples by provider.

#### DNS challenge examples

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

```shell
akeyless target create google-trust \
--name <Target Name> \
--google-trust-url <production / staging> \
--email <ACME Account Email> \
--acme-challenge http
```

#### Key CLI flags

- `name`: A unique name for the target. The name can include a path to a virtual folder by using slash `/` separators. If the folder does not exist, Akeyless creates it with the target.

- `email`: Email address used for ACME account registration.

- `eab-key-id`: External Account Binding Key ID from Google CA Services.

- `eab-hmac-key`: External Account Binding HMAC Key from Google CA Services.

- `google-trust-url`: Use this when you want to select the ACME environment explicitly. Supported values are `production` (default) and `staging`.

- `acme-challenge`: Challenge type. Either `dns` or `http`.

- `dns-target-creds`: Use this when `--acme-challenge=dns`. This is required for DNS validation. Supported target types are AWS, Azure, GCP, and Cloudflare.

- `dns-zone`: Use this when `--acme-challenge=dns` and `--dns-target-creds` points to a Cloudflare target.

- `hosted-zone`: Use this when `--acme-challenge=dns` and `--dns-target-creds` points to an AWS target. This identifies the Route 53 hosted zone.

- `resource-group`: Use this when `--acme-challenge=dns` and `--dns-target-creds` points to an Azure target.

- `gcp-project`: Use this when `--acme-challenge=dns` and `--dns-target-creds` points to a GCP target and the project ID cannot be derived automatically.

- `timeout`: Challenge validation timeout. Default is `5m`. Supported range is `1m` to `1h`.

- `key`: Use this when you want to encrypt target secret values with a specific protection key instead of the account default key.

[View the complete list of target command parameters.](https://docs.akeyless.io/docs/cli-ref-targets)

### Use the Console

1. Log in to the Akeyless Console, and go to **Targets**, then **New**, then **Certificate Automation (Google CA)**.

2. Define the Name of the target, and specify the Location as a path to the virtual folder where you want to create the new target, using slash `/` separators. If the folder does not exist, it will be created together with the target.

3. Select a **Protection key** with a Customer Fragment to enable Zero-Knowledge and click **Next**. [Read more about Zero-Knowledge Encryption](https://docs.akeyless.io/docs/gateway-zero-knowledge).

4. Define the remaining parameters as follows:

- **Email**: Email address used to register the ACME account.

- **Challenge Type**: Either **DNS&#x20;**&#x20;or **HTTP.**

- **URL**: Either [Production](https://dv.acme-v02.api.pki.goog/directory) or [Staging](https://dv.acme-v02.test-api.pki.goog/directory).

- **EAB KID**: External Account Binding Key ID from Google CA Services.

- **EAB HMAC Key**: External Account Binding HMAC Key from Google CA Services.

- **DNS Provider**: Either **AWS**, **GCP**, **Azure**, or **Cloudflare** (relevant only if **Challenge Type** is **DNS**).

- **Target**: Select a target that contains the DNS provider credentials (relevant only if **Challenge Type** is **DNS**).

  - **Hosted Zone**: [Amazon Route 53](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/hosted-zones-working-with.html) hosted zone identifier. (Relevant only if **Challenge Type** is **DNS** and **DNS Provider** is **AWS**).

  - **Resource Group**: Azure resource group name. (Relevant only if **Challenge Type** is **DNS** and **DNS Provider** is **Azure**).

  - **GCP Project**: GCP Cloud DNS project ID. Optional when **DNS Provider** is **GCP**.

  - **DNS Zone**: Cloudflare DNS zone name. (Relevant only if **Challenge Type** is **DNS** and **DNS Provider** is **Cloudflare**).

1. Click Finish.

## Configure DNS Provider Authentication (Optional)

For DNS challenge flows, a provider target can use Gateway cloud identity instead of static credentials.

### Gateway Cloud Identity Examples

```shell AWS
akeyless target create aws \
--name <AWS DNS Target Name> \
--use-gw-cloud-identity \
--region <AWS Region>
```
```shell Azure
akeyless target create azure \
--name <Azure DNS Target Name> \
--connection-type cloud-identity \
--subscription-id <Azure Subscription ID> \
--resource-group-name <Azure DNS Resource Group Name>
```
```shell GCP
akeyless target create gcp \
--name <GCP DNS Target Name> \
--use-gw-cloud-identity
```

## DNS Provider Permissions for DNS-01

When using `dns` challenge validation, the target referenced by `dns-target-creds` must have permission to create and update ACME TXT records in the relevant DNS zone.

- **AWS Route 53**
  - **Required for DNS-01 record changes**: `route53:ChangeResourceRecordSets` on the target hosted zone.
  - **Common read permissions**: `route53:GetHostedZone`, `route53:ListHostedZonesByName`, and `route53:ListResourceRecordSets`.
  - Reference: [Actions, resources, and condition keys for Amazon Route 53](https://docs.aws.amazon.com/service-authorization/latest/reference/list_amazonroute53.html) and [Permissions required to use the Route 53 API](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/r53-api-permissions-ref.html)

- **GCP Cloud DNS**
  - **Required for DNS-01 record changes**: `dns.changes.create` and relevant record set permissions.
  - **Common read permissions**: `dns.managedZones.get`, `dns.managedZones.list`, `dns.resourceRecordSets.get`, and `dns.resourceRecordSets.list`.
  - Reference: [Access control with IAM](https://docs.cloud.google.com/dns/docs/access-control)

- **Azure DNS**
  - **Recommended built-in role**: **DNS Zone Contributor** at the DNS zone scope.
  - Reference: [Azure built-in roles for Networking - DNS Zone Contributor](https://learn.microsoft.com/en-us/azure/role-based-access-control/built-in-roles/networking#dns-zone-contributor)

## Troubleshoot DNS Challenge Flows

If certificate issuance fails during DNS challenge validation, validate the following:

- The `dns-target-creds` target exists and is configured for the expected provider.
- The provider-specific parameter is set correctly:
  - AWS: `hosted-zone`
  - Azure: `resource-group`
  - GCP: `gcp-project` (when project ID cannot be derived automatically)
  - Cloudflare: `dns-zone`
- The requested domain is hosted in the DNS zone managed by the provider target.
- The Gateway has network access to provider DNS APIs.

<Callout icon="ℹ️" theme="info">
  ### **Note (Least Privilege):**

  Scope permissions to only the DNS zones and record operations required for certificate validation.
</Callout>

<br />
