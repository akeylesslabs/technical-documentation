---
title: Certificate Provisioning to Cloud Providers
deprecated: false
hidden: false
metadata:
  robots: index
---
Certificate Provisioning to cloud certificate managers lets you push a certificate stored in Akeyless directly into AWS Certificate Manager (ACM), Azure Key Vault, or GCP Certificate Manager, using an existing [AWS Target](https://docs.akeyless.io/docs/aws-targets), [Azure Target](https://docs.akeyless.io/docs/azure-targets), or [GCP Target](https://docs.akeyless.io/docs/gcp-targets).

Unlike provisioning to a Linux or Windows endpoint, the cloud target holds only the credentials used to call the cloud provider's API. The certificate is stored in the cloud certificate manager as a single object that bundles the certificate, private key, and chain. After a successful provisioning, future renewals of the certificate are provisioned automatically.

Every certificate provisioned by Akeyless is tagged with `provisioned-by: akeyless` in the cloud provider, so you can identify and audit Akeyless-managed certificates.

<Callout icon="ℹ️" theme="info">
  ### **Note:**

  The host-based provisioning fields **Certificate Remote Path**, **Private Key Remote Path**, **Certificate Chain Path**, and **Post Provision Command** aren't available for cloud targets. To run actions after provisioning, see [Post-Provisioning Actions](#post-provisioning-actions).
</Callout>

## Prerequisites

- An [Akeyless Gateway](https://docs.akeyless.io/docs/gateway-overview).
- A certificate item stored in Akeyless that includes its private key. For more information, see [Certificate Storage](https://docs.akeyless.io/docs/certificate-storage).
- A cloud target whose identity has the following permissions in the destination account:

**AWS Target → ACM**

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "acm:ImportCertificate",
        "acm:DescribeCertificate",
        "acm:ListCertificates",
        "acm:AddTagsToCertificate"
      ],
      "Resource": "*"
    }
  ]
}
```

**Azure Target → Azure Key Vault**

The service principal needs the **Key Vault Certificates Officer** role on the Key Vault, or, when using access policies, the **Get**, **List**, and **Import** certificate permissions.

**GCP Target → GCP Certificate Manager**

The service account needs the **Certificate Manager Editor** (`roles/certificatemanager.editor`) role on the project, or at least the `certificatemanager.certs.create`, `certificatemanager.certs.get`, and `certificatemanager.certs.update` permissions.

## Provider-Specific Fields

Each cloud provider requires its own set of fields when you attach the certificate to the target:

| Provider                | Field                | Description                                                                                                                             |
| ----------------------- | -------------------- | --------------------------------------------------------------------------------------------------------------------------------------- |
| AWS Certificate Manager | **Certificate Name** | The certificate name in ACM.                                                                                                            |
| AWS Certificate Manager | **Certificate ARN**  | Optional. Relevant only when renewing or overwriting an existing certificate. If left blank, ACM provisions a new certificate resource. |
| Azure Key Vault         | **Certificate Name** | The certificate name in Azure Key Vault.                                                                                                |
| Azure Key Vault         | **Key Vault Name**   | Mandatory. The Azure Key Vault where the certificate object will be stored.                                                             |
| GCP Certificate Manager | **Certificate Name** | The certificate name in GCP Certificate Manager.                                                                                        |
| GCP Certificate Manager | **Location Scope**   | Mandatory. Whether the certificate is deployed to the `global` namespace or to a specific region, for example `us-central1`.            |

<Callout icon="👍" theme="okay">
  ### Note

  For ACM, the certificate is imported to the region defined on the [AWS Target](https://docs.akeyless.io/docs/aws-targets). For GCP, the certificate is created in the project of the service account defined on the [GCP Target](https://docs.akeyless.io/docs/gcp-targets).
</Callout>

## Provisioning a Certificate Using the Akeyless CLI

Run the following CLI command to provision a certificate to a cloud certificate manager:

```shell AWS ACM
akeyless assoc-target-item \
--name <Certificate name> \
--target-name <AWS Target name> \
--gateway-url 'https://<Your-Akeyless-GW-URL>:8000' \
--certificate-name <Certificate name in ACM> \
--certificate-arn <Existing certificate ARN>
```
```shell Azure Key Vault
akeyless assoc-target-item \
--name <Certificate name> \
--target-name <Azure Target name> \
--gateway-url 'https://<Your-Akeyless-GW-URL>:8000' \
--certificate-name <Certificate name in Key Vault> \
--key-vault-name <Key Vault name>
```
```shell GCP Certificate Manager
akeyless assoc-target-item \
--name <Certificate name> \
--target-name <GCP Target name> \
--gateway-url 'https://<Your-Akeyless-GW-URL>:8000' \
--certificate-name <Certificate name in GCP> \
--location-scope <global|region>
```

Where:

- `name`: The Certificate item name.
- `target-name`: The cloud Target item name to provision the certificate with.
- `gateway-url`: Akeyless Gateway Configuration Manager URL (port `8000`).
- `certificate-name`: The name of the certificate in the cloud certificate manager.
- `certificate-arn`: AWS only. Optional, the ARN of an existing ACM certificate to overwrite. If left empty, a new certificate resource is created.
- `key-vault-name`: Azure only. The name of the Azure Key Vault where the certificate will be stored.
- `location-scope`: GCP only. `global`, or a specific region such as `us-central1`.

You can find the complete list of additional parameters for this command in the [CLI Reference](https://docs.akeyless.io/docs/cli-reference) section.

## Provisioning a Certificate Using the Akeyless Console

1. Log in to the Akeyless Console, go to **Items**, and find the certificate you wish to provision.
2. Click on the Certificate item, click on the **Provisioning** tab, and then **Attach**.
3. Select the **Target**: an AWS, Azure, or GCP target.
4. Enter the fields for the selected cloud provider:
   - **AWS Certificate Manager:**
     - **Certificate Name:** The certificate name in ACM.
     - **Certificate ARN:** Optional. Relevant only when renewing or overwriting an existing certificate. If left blank, ACM provisions a new certificate resource.
   - **Azure Key Vault:**
     - **Certificate Name:** The certificate name in Azure Key Vault.
     - **Key Vault Name:** The Azure Key Vault where the certificate object will be stored.
   - **GCP Certificate Manager:**
     - **Certificate Name:** The certificate name in GCP.
     - **Location Scope:** `global`, or a specific region (for example, `us-central1`).
5. Select the **Gateway** through which the certificate will be provisioned.
6. Click **Save**.

## How Certificates Are Stored in Each Provider

- **AWS Certificate Manager:** The leaf certificate, private key, and certificate chain are imported as one ACM certificate.
- **Azure Key Vault:** The certificate, private key, and full chain are imported as a single native Key Vault **Certificate** object. Azure stores the private key securely and exposes the public certificate attributes.
- **GCP Certificate Manager:** The leaf and intermediate chain are uploaded as the certificate, together with the matching private key, as one Certificate Manager certificate.

## Post-Provisioning Actions

Cloud certificate managers don't run commands on hosts, so **Post Provision Command** isn't supported. To reload services or update bindings after a certificate is provisioned or renewed, use the provider's native events:

- **AWS:** Create an Amazon EventBridge rule that matches the `ImportCertificate` CloudTrail event, and trigger an AWS Systems Manager Run Command or an AWS Lambda function.
- **Azure:** Create an Azure Event Grid subscription on the Key Vault for the `Microsoft.KeyVault.CertificateNewVersionCreated` event, and trigger an Azure Function or Automation Runbook.
- **GCP:** Create a Cloud Logging sink for Certificate Manager certificate operations that routes to Pub/Sub or Eventarc, and trigger a Cloud Function or Cloud Run service.