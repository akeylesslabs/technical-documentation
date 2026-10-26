---
title: Certificate Provisioning to Cloud Targets
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
In addition to [provisioning certificates](https://docs.akeyless.io/docs/certificate-provisioning) to [SSH](https://docs.akeyless.io/docs/ssh-target), [Windows](https://docs.akeyless.io/docs/windows-target), and [F5](https://www.f5.com/) endpoints, Akeyless supports provisioning certificates directly to cloud-native certificate stores:

* [AWS Certificate Manager (ACM)](https://docs.akeyless.io/docs/aws-targets), using an **AWS Target**.
* [Azure Key Vault](https://docs.akeyless.io/docs/azure-targets), using an **Azure Target**.
* [GCP Certificate Manager](https://docs.akeyless.io/docs/gcp-targets), using a **GCP Target**.

## How Cloud Target Provisioning Differs from Host-Based Provisioning

SSH and Windows targets are execution endpoints: Akeyless connects to the target's shell to write certificate files to the filesystem and run commands. AWS, Azure, and GCP targets are used differently, purely as credential providers: they hold the IAM credentials, service principal, or service account key that Akeyless uses to call the cloud provider's certificate management API. This has a few implications for provisioning:

<Callout icon="ℹ️" theme="info">
  ### Fields Not Applicable to Cloud Targets

  Cloud certificate managers store the certificate, private key, and certificate chain together as a single object rather than as separate files, and don't expose a persistent shell to run commands after provisioning. As a result, the following fields, used for SSH/Windows/F5 provisioning, don't apply when provisioning to an AWS, Azure, or GCP target:

  * **Certificate Remote Path**
  * **Private Key Remote Path**
  * **Certificate Chain Path**
  * **Post Provision Command**
</Callout>

Every certificate Akeyless provisions to a cloud target is tagged with `provisioned-by: akeyless`, so that provisioned certificates can be identified in the cloud provider's console.

## Provisioning to AWS Certificate Manager (ACM)

To provision a certificate to AWS Certificate Manager, attach the certificate to an existing [AWS Target](https://docs.akeyless.io/docs/aws-targets) and provide the following fields:

* **Certificate Name** - The name of the certificate in ACM.

* **Certificate ARN** - Optional, relevant only when renewing or overwriting an existing certificate. If left blank, ACM automatically provisions a new certificate resource.

## Provisioning to Azure Key Vault

To provision a certificate to Azure Key Vault, attach the certificate to an existing [Azure Target](https://docs.akeyless.io/docs/azure-targets) and provide the following fields:

* **Certificate Name** - The name of the certificate in Azure Key Vault.

* **Key Vault Name** - Mandatory, the Azure Key Vault where the certificate object will be stored.

## Provisioning to GCP Certificate Manager

To provision a certificate to GCP Certificate Manager, attach the certificate to an existing [GCP Target](https://docs.akeyless.io/docs/gcp-targets) and provide the following fields:

* **Certificate Name** - The name of the certificate in GCP Certificate Manager.

* **Location Scope** - Mandatory, defines whether the certificate is deployed to the `global` namespace or a specific region, for example `us-central1`.

## Provisioning a Certificate Using the Akeyless Console

1. Log in to the Akeyless Console, and go to **Items**, find the certificate you wish to provision.
2. Click on the **Certificate** item, click on the **Provisioning** tab, and then **Attach**.
3. **Target Name** - Choose an existing AWS, Azure, or GCP [Target](https://docs.akeyless.io/docs/targets) from the drop-down list.
4. **Gateway** - Choose an existing Gateway from the drop-down list.
5. Enter the fields relevant to the chosen cloud provider, as described above.

## Post-Provisioning Automation

Since cloud certificate managers don't support a **Post Provision Command**, use the cloud provider's native eventing services to trigger downstream automation after a certificate is provisioned, for example reloading a load balancer or a web server:

* **AWS Certificate Manager** - Configure an AWS EventBridge rule on the ACM `ImportCertificate` CloudTrail event to trigger an AWS Systems Manager Run Command or an AWS Lambda function.

* **Azure Key Vault** - Configure an Azure Event Grid subscription on the `Microsoft.KeyVault.CertificateNewVersionCreated` event to trigger an Azure Function or an Azure Automation Runbook.

* **GCP Certificate Manager** - Configure a Cloud Logging sink on certificate modification operations to forward events to a Pub/Sub topic or an Eventarc trigger, which can invoke a Cloud Function or a Cloud Run instance.