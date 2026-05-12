---
title: RDP Session Recording
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
RDP Session Recording captures interactive Remote Desktop Protocol (RDP) sessions as video for auditability, investigation, and long-term retention.

> ℹ️ **Note:**
>
> If you are looking for browser-based Zero Trust Web Access recordings, use [Web Access Session Recording](https://docs.akeyless.io/docs/sra-web-access-session-recording).

## Feature Scope

RDP Session Recording covers:

* Video capture of RDP sessions.
* Storage to local disk or cloud/object storage.
* Recording quality selection.
* Optional gzip compression.
* Optional encryption before upload.

This feature is configured from Gateway **Remote Access** settings and by way of Gateway CLI commands.

## Configuration Surfaces

Use one of the following:

* Console UI: **Gateway Manager → Remote Access → Session Recording → RDP recordings**.
* CLI: `akeyless gateway update remote-access-rdp-recording`.

For CLI flags and command syntax, see [CLI Reference - Gateway Secure Remote Access](https://docs.akeyless.io/docs/cli-reference-sra).

## Configuration Reference

### Required Base Controls

* `rdp-session-recording`: Enables or disables RDP recording.
* `rdp-session-storage`: Recording destination (`local`, `aws`, `azure`).

### Quality, Compression, and Encryption

* `rdp-session-recording-quality`: Recording quality (`low`, `medium`, `high`).
* `rdp-session-recording-compress`: Compress recordings before upload.
* `rdp-session-recording-encryption-key`: Encrypt recordings by using an Akeyless key.

### AWS Storage Settings

* `aws-storage-region`
* `aws-storage-bucket-name`
* `aws-storage-bucket-prefix`
* `aws-storage-access-key-id` (optional when identity-based auth is used)
* `aws-storage-secret-access-key` (optional when identity-based auth is used)
* `aws-storage-endpoint-url` (for S3-compatible platforms)

### Azure Storage Settings

* `azure-storage-account-name`
* `azure-storage-container-name`
* `azure-storage-client-id` (optional when managed identity is used)
* `azure-storage-client-secret` (optional when managed identity is used)
* `azure-storage-tenant-id` (optional when managed identity is used)

## Storage Workflows

### Local Storage

Set storage to `local` to keep recordings on the Gateway host under `/home/akeyless/recordings`.

### AWS S3 or S3-Compatible Storage

Set storage to `aws` and configure bucket, region, and optional prefix. For S3-compatible platforms, add a custom endpoint URL.

Authentication can use either:

* Gateway identity.
* Explicit access key and secret key.

### Azure Blob Storage

Set storage to `azure` and configure account and container.

Authentication can use either:

* Gateway identity (for example, managed identity).
* Explicit client ID, secret, and tenant ID.

## End-to-End Workflow

1. Enable RDP recording.
2. Select storage type (`local`, `aws`, or `azure`).
3. Configure storage authentication.
4. Set quality, compression, and encryption options.
5. Save configuration.
6. Start an RDP session and verify that the recording artifact is created in the selected destination.

## Related Pages

* [Web Access Session Recording](https://docs.akeyless.io/docs/sra-web-access-session-recording)
* [Session Management](https://docs.akeyless.io/docs/sra-session-management)
* [Session Log Forwarding](https://docs.akeyless.io/docs/sra-session-forwarding)
* [Zero Trust Web Access on K8s](https://docs.akeyless.io/docs/sra-web-access-on-k8s)
