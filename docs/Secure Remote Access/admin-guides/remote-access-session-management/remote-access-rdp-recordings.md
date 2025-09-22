---
title: RDP Recordings
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
RDP Session Recording is managed entirely through your Gateway's console under the "Remote Access" section in the Gateway settings. These sessions generate video recordings that can be uploaded to either AWS S3 or Azure Blob Storage for secure storage or can be saved locally. 

# Session Recording

SRA supports the recording of RDP sessions. You can choose to store RDP Session Recordings by clicking "Remote Access" -> "Session Recording" -> "RDP Recordings", clicking the slider to Enable, and then choosing the location to keep the recordings of those sessions.

**RDP** sessions provide video recordings that can be saved to AWS S3 buckets, Azure Blob storage, or locally. To work with session recording for RDP, provide the following settings to upload your recording to an S3 bucket or to an Azure Blob storage.

## Compression & Encryption

SRA supports compressing and encrypting RDP session recordings to optimize storage and protect sensitive content. The feature is available for both legacy Helm charts and the latest unified charts via the Console. 

### Quality (Resolution)

Choose the output resolution for the encoded video file (default is 1280×720).

### Compression (GZIP)

Optionally compress the encoded video file using GZIP.

* **When to use:** Enable compression to reduce storage footprint, especially for long sessions.

### Encryption (AES)

Protect recordings at rest with AES-based encryption.

* **Algorithm:** AES (Akeyless supported key types).
* **Scope:** Entire video payload is encrypted after encoding (and after optional compression).
* **Access:** Only authorized users with the appropriate permissions can decrypt and access the file.

### File Naming & Formats

The final file name indicates which operations were applied:

* **Encrypted (no compression):** `*.enc`
* **Compressed, then encrypted:** `*.enc.gzip`

> **Note:** Compression occurs before encryption to preserve compression efficiency; the final artifact reflects both operations in its suffix.

### How Encoding Runs

Encoding is executed via a **[decrypt file command](https://docs.akeyless.io/docs/cli-reference-encryption-keys#p-stylecolorbluedecrypt-filep)**. 

### Where to Configure

* **Latest (Console UI):** **Gateway Manager → Remote Access → Session Recording → RDP recordings**\
  From here you can set the recording **Quality**, toggle **GZIP Compression**, and enable **Encryption**.

* **Legacy Helm Chart:** Configure under the **`rdpRecord`** section of your values file to set **quality**, **compression**, and **encryption** parameters for RDP recordings.

# Storage Options

Here are the options for storing RDP recordings:

## Local

Local session recordings will be stored inside the SRA server under /home/akeyless/recordings.

## AWS S3

When storing RDP session recordings in AWS S3, the user can choose between two authentication methods:

### Use Gateway Identity

With this option, the system uses the Gateway’s instance identity (such as an IAM Role) to authenticate with AWS. The user needs to provide the following details:

**Region** (required): The AWS region where the S3 bucket is located.\
**Bucket Name**: The name of the S3 bucket where the recordings will be uploaded.\
**Bucket Prefix**: A folder structure within the bucket to organize the recordings.

### Provide Credentials

With this option, the user provides explicit AWS credentials for authentication. The following details are required:

**AWS Access Key ID** (required): The access key ID for AWS authentication.\
**AWS Secret Access Key** (required): The corresponding secret access key for the provided access key ID.\
**Region** (required): The AWS region where the S3 bucket is located.\
**Bucket Name**: The name of the S3 bucket where the recordings will be stored.\
**Bucket Prefix**: A folder structure within the bucket to organize the recordings.

## Azure Blob Storage

For storing RDP session recordings in Azure Blob Storage, the user can also select between two options:

### Use Gateway Identity

This option allows the system to use the Gateway’s identity (such as Managed Identity) for authentication with Azure. The user must provide the following details:

**Storage Account Name** (required) The name of the Azure Storage account where the recordings will be uploaded.\
**Storage Container Name** (required): The container within the storage account where recordings will be saved.

### Provide Credentials

With this option, the user provides explicit credentials for Azure authentication. The following details are required:

**Azure Client ID** (required): The client ID used for Azure authentication.\
**Azure Client Secret** (required): The corresponding secret key for the provided client ID.\
**Azure Tenant ID** (required): The tenant ID associated with the Azure account.\
**Storage Account Name**: The name of the Azure Storage account where the recordings will be uploaded.\
**Storage Container Name**: The container within the storage account where recordings will be saved.

This can also be done via the CLI:

```shell AWS S3
akeyless gateway update remote-access-rdp-recording \
--rdp-session-recording true \
--rdp-session-storage aws \
--gateway-url https://<your-gateway-url>:8000 \
--aws-storage-region <your-region> \
--aws-storage-bucket-name <s3-bucket-name> \
--aws-storage-bucket-prefix <s3-bucket-prefix> \
--aws-storage-access-key-id <optional-explicit-key-id> \
--aws-storage-secret-access-key <optional-explicit-access-key>
```
```shell Azure Blob
akeyless gateway update remote-access-rdp-recording \
--rdp-session-recording true \
--rdp-session-storage azure \
--gateway-url https://<your-gateway-url>:8000 \
--azure-storage-account-name <your-storage-account-name> \
--azure-storage-container-name <your-storage-container-name> \
--azure-storage-client-id  <optional-client-id> \
--azure-storage-client-secret <optional-client-secret> \
--azure-storage-tenant-id <optional-tenant-id> \
```
```shell Local
akeyless gateway update remote-access-rdp-recording \
--rdp-session-recording true \
--rdp-session-storage local \
```
