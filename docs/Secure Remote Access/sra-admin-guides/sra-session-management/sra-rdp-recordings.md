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
RDP Session Recording is managed entirely through your Gateway's console under the **Remote Access** section in the Gateway settings. These sessions generate video recordings that can be uploaded to **Amazon S3**, **S3-compatible object storage** (for example, NetApp StorageGRID), or **Azure Blob Storage** for secure storage, or can be saved locally.

Use this page together with [Sessions Overview](https://docs.akeyless.io/docs/sra-sessions-overview) to correlate session inventory records with recording storage location and retrieval path.

For backend sizing, retention windows, and lifecycle policy planning, use [Storage and Recording Capacity](https://docs.akeyless.io/docs/sra-storage-and-recording-capacity).

> ℹ️ **Note:**
>
> If you are working with browser-based Zero Trust Web Access recordings, use [Zero Trust Web Access on K8s](https://docs.akeyless.io/docs/sra-web-access-on-k8s).

RDP recordings support configurable quality, compression, and encryption for stored sessions.

## RDP Session Initialization Prerequisites

Before setting up RDP session recording, ensure the following prerequisites are met to avoid recording attempts when RDP connections fail.

### Account Region and Authentication Endpoint

For deployments in non-default account regions, ensure account region and authentication endpoint configuration are aligned:

* Verify `UAM_ADDR` environment variable in bastion deployment matches your account's region.
* Confirm account region setting in Gateway console under **Remote Access** configuration.
* Test RDP connection initiation before enabling recording to confirm the session succeeds.

When account region and authentication endpoint are misaligned, RDP sessions may close without meaningful error messages, preventing recording from ever starting.

### RDP Connection Validation

If RDP sessions terminate immediately after authentication succeeds (browser tab closes without error):

1. Review bastion authentication logs for errors during RDP session initiation.
2. Verify `UAM_ADDR` matches your account's region.
3. Check browser console and network traffic for WebSocket connectivity issues.
4. Confirm Gateway Remote Access configuration in console.

After confirming RDP connectivity, enable session recording.

### Ingress and Load Balancer Timeout Alignment

Session recording starts only after a stable RDP connection is established and maintained.

If ingress or load balancer timeout values are too short, sessions can disconnect before recording is useful.

For Kubernetes ingress environments:

* Verify timeout values on ingress and backend policies for Gateway and bastion routes.
* In GKE ingress deployments, confirm timeout is not left at the `30s` backend default.
* Align timeout values with expected RDP session duration.

For timeout planning baselines, see [SRA Requirements](https://docs.akeyless.io/docs/sra-requirements#session-timeout-and-ttl-alignment).

## Session Recording

SRA supports the recording of RDP sessions. You can choose to store RDP Session Recordings by clicking **Remote Access -> Session Recording -> RDP Recordings**, clicking the slider to Enable, and then choosing the location to keep the recordings of those sessions.

**RDP** sessions provide video recordings that can be saved to **Amazon S3** buckets, **S3-compatible object storage**, **Azure Blob Storage**, or locally. To work with session recording for RDP, provide the following settings to upload your recording to object storage.

### Compression & Encryption

SRA supports compressing and encrypting RDP session recordings to optimize storage and protect sensitive content. The feature is available for both legacy Helm charts and the latest unified charts by way of the Console.

#### Quality (Resolution)

Choose the output resolution for the encoded video file (default is `1280×720`).

#### Compression (gzip)

Optionally compress the encoded video file using `GZIP`.

* **When to use:** Enable compression to reduce storage footprint, especially for long sessions.

#### Encryption

Protect recordings at rest with encryption.

* **Algorithm:** Encryption uses Akeyless-supported key types.
* **Scope:** Entire video payload is encrypted after encoding (and after optional compression).
* **Access:** Only authorized users with the appropriate permissions can decrypt and access the file.

#### File Naming & Formats

The final file name indicates which operations were applied:

* **Encrypted (no compression):** `*.enc`
* **Compressed, then encrypted:** `*.enc.gzip`

> _Note:_ Compression occurs before encryption to preserve compression efficiency; the final artifact reflects both operations in its suffix.

#### How Encoding Runs

Encoding is executed by way of a **[decrypt file command](https://docs.akeyless.io/docs/cli-reference-encryption-keys#decrypt-file)**.

#### Where to Configure

* **Latest (Console UI):** Open the gateway configuration UI, then navigate to **Remote Access** and **RDP Recordings**.
  From here you can set the recording **Quality**, toggle **gzip Compression**, and enable **Encryption**.

* **Legacy Helm Chart:** Configure under the **`rdpRecord`** section of your values file to set **quality**, **compression**, and **encryption** parameters for RDP recordings.

## Storage Options

Here are the options for storing RDP recordings:

### Local

Local session recordings will be stored inside the SRA server under `/home/akeyless/recordings`.

Retention for local storage depends on host disk lifecycle and your operational cleanup policy.

### Amazon S3

When storing RDP session recordings in Amazon S3, the user can choose between two authentication methods:

#### Use Gateway Identity

With this option, the system uses the Gateway’s instance identity (such as an IAM Role) to authenticate with AWS. The user needs to provide the following details:

* **Region** (required): The AWS region where the S3 bucket is located.
* **Bucket Name**: The name of the S3 bucket where the recordings will be uploaded.
* **Bucket Prefix**: A folder structure within the bucket to organize the recordings.

Use lifecycle rules on the bucket or prefix to enforce retention policy.

#### Provide Credentials

With this option, the user provides explicit AWS credentials for authentication. The following details are required:

* **AWS Access Key ID** (required): The access key ID for AWS authentication.
* **AWS Secret Access Key** (required): The corresponding secret access key for the provided access key ID.
* **Region** (required): The AWS region where the S3 bucket is located.
* **Bucket Name**: The name of the S3 bucket where the recordings will be stored.
* **Bucket Prefix**: A folder structure within the bucket to organize the recordings.

### S3-Compatible Object Storage (for example, NetApp StorageGRID)

For S3-compatible platforms, configure the S3 connection with a custom endpoint URL.

Use the following values:

* **Endpoint URL** (required): The S3-compatible endpoint, for example `https://<storagegrid-host>:<port>`.
* **Access Key ID** (required): The access key used for S3 API authentication.
* **Secret Access Key** (required): The secret access key paired with the access key ID.
* **Bucket Name** (required): The bucket where recordings will be stored.
* **Bucket Prefix** (optional): A folder path inside the bucket for organizing recordings.

SRA uses the standard S3 API for this flow. This allows recording uploads to compatible object storage providers without requiring AWS-specific identity integration.

Use object lifecycle policy in the target platform to enforce retention windows.

### Azure Blob Storage

For storing RDP session recordings in Azure Blob Storage, the user can also select between two options:

#### Use Gateway Identity

This option allows the system to use the Gateway’s identity (such as Managed Identity) for authentication with Azure. The user must provide the following details:

* **Storage Account Name** (required) The name of the Azure Storage Account where the recordings will be uploaded.
* **Storage Container Name** (required): The container within the Storage Account where recordings will be saved.

#### Provide Credentials

With this option, the user provides explicit credentials for Azure authentication. The following details are required:

* **Azure Client ID** (required): The client ID used for Azure authentication.
* **Azure Client Secret** (required): The corresponding secret key for the provided client ID.
* **Azure Tenant ID** (required): The tenant ID associated with the Azure account.
* **Storage Account Name**: The name of the Azure Storage Account where the recordings will be uploaded.
* **Storage Container Name**: The container within the Storage Account where recordings will be saved.

Use Azure lifecycle management policy to enforce retention windows in the target container.

This can also be done by way of the CLI. For a full flag reference, see [CLI Reference - Gateway Secure Remote Access](https://docs.akeyless.io/docs/cli-reference-sra).

```shell
akeyless gateway update remote-access-rdp-recording \
--rdp-session-recording true \
--rdp-session-storage aws \
--gateway-url https://<your-gateway-url>:8000 \
--aws-storage-region <your-region> \
--aws-storage-bucket-name <S3-bucket-name> \
--aws-storage-bucket-prefix <S3-bucket-prefix> \
--aws-storage-endpoint-url <optional-s3-compatible-endpoint-url> \
--aws-storage-access-key-id <optional-explicit-key-id> \
--aws-storage-secret-access-key <optional-explicit-access-key>
```
```shell
akeyless gateway update remote-access-rdp-recording \
--rdp-session-recording true \
--rdp-session-storage azure \
--gateway-url https://<your-gateway-url>:8000 \
--azure-storage-account-name <your-storage-account-name> \
--azure-storage-container-name <your-storage-container-name> \
--azure-storage-client-id  <optional-client-id> \
--azure-storage-client-secret <optional-client-secret> \
--azure-storage-tenant-id <optional-tenant-id>
```
```shell
akeyless gateway update remote-access-rdp-recording \
--rdp-session-recording true \
--rdp-session-storage local
```

## Related Pages

* [Web Access Session Recording](https://docs.akeyless.io/docs/sra-web-access-session-recording)
* [Session Management](https://docs.akeyless.io/docs/sra-session-management)
* [Sessions Overview](https://docs.akeyless.io/docs/sra-sessions-overview)
