---
title: Certificate Provisioning to AWS Certificate Manager
slug: certificate-provisioning-to-aws
deprecated: false
hidden: false
metadata:
  robots: index
---
Certificate Provisioning to AWS Certificate Manager (ACM) lets you push a certificate stored in Akeyless directly into ACM, using an existing [AWS Target](https://docs.akeyless.io/docs/aws-targets). This is one of the [certificate provisioning](https://docs.akeyless.io/docs/certificate-provisioning) destinations supported by Akeyless.

Unlike provisioning to a Linux or Windows endpoint, the AWS Target holds only the credentials used to call the ACM API. The certificate is stored in ACM as a single object that bundles the certificate, private key, and chain. After a successful provisioning, future renewals of the certificate are provisioned automatically.

Every certificate provisioned by Akeyless is tagged with `provisioned-by: akeyless` in ACM, so you can identify and audit Akeyless-managed certificates.

<Callout icon="ℹ️" theme="info">
  ### **Note:**

  The host-based provisioning fields **Certificate Remote Path**, **Private Key Remote Path**, **Certificate Chain Path**, and **Post Provision Command** aren't available for cloud targets. To run actions after provisioning, see [Post-Provisioning Actions](#post-provisioning-actions).
</Callout>

## Prerequisites

- An [Akeyless Gateway](https://docs.akeyless.io/docs/gateway-overview).
- A certificate item stored in Akeyless that includes its private key. For more information, see [Certificate Storage](https://docs.akeyless.io/docs/certificate-storage).
- An AWS Target whose identity has the following permissions in the destination account:

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

## Provider-Specific Fields

| Field                | Description                                                                                                                             |
| -------------------- | ----------------------------------------------------------------------------------------------------------------------------------------- |
| **Certificate Name** | The certificate name in ACM.                                                                                                            |
| **Certificate ARN**  | Optional. Relevant only when renewing or overwriting an existing certificate. If left blank, ACM provisions a new certificate resource. |

<Callout icon="👍" theme="okay">
  ### Note

  The certificate is imported to the region defined on the [AWS Target](https://docs.akeyless.io/docs/aws-targets).
</Callout>

<Callout icon="far fa-triangle-exclamation" theme="warn">
  ### Set the Certificate ARN to Avoid Duplicates

  Without `certificate-arn`, a new ACM certificate is created on every provisioning, including after each renewal.
</Callout>

## Provisioning a Certificate Using the Akeyless CLI

Run the following CLI command to provision a certificate to AWS Certificate Manager:

```shell
akeyless assoc-target-item \
--name <Certificate name> \
--target-name <AWS Target name> \
--gateway-url 'https://<Your-Akeyless-GW-URL>:8000' \
--certificate-name <Certificate name in ACM> \
--certificate-arn <Existing certificate ARN>
```

Where:

- `name`: The Certificate item name.
- `target-name`: The AWS Target item name to provision the certificate with.
- `gateway-url`: Akeyless Gateway Configuration Manager URL (port `8000`).
- `certificate-name`: The name of the certificate in ACM.
- `certificate-arn`: Optional, the ARN of an existing ACM certificate to overwrite. If left empty, a new certificate resource is created.

You can find the complete list of additional parameters for this command in the [CLI Reference](https://docs.akeyless.io/docs/cli-reference) section.

## Provisioning a Certificate Using the Akeyless Console

1. Log in to the Akeyless Console, go to **Items**, and find the certificate you wish to provision.
2. Click on the Certificate item, click on the **Provisioning** tab, and then **Attach**.
3. Select an AWS **Target**.
4. Enter the fields:
   - **Certificate Name:** The certificate name in ACM.
   - **Certificate ARN:** Optional. Relevant only when renewing or overwriting an existing certificate. If left blank, ACM provisions a new certificate resource.
5. Select the **Gateway** through which the certificate will be provisioned.
6. Click **Save**.

## How the Certificate Is Stored in ACM

The leaf certificate, private key, and certificate chain are imported as one ACM certificate.

## Post-Provisioning Actions

ACM doesn't run commands on hosts, so **Post Provision Command** isn't supported. To reload services or update bindings after a certificate is provisioned or renewed, create an Amazon EventBridge rule that matches the `ImportCertificate` CloudTrail event, and trigger an AWS Systems Manager Run Command or an AWS Lambda function.