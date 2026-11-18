---
title: Web Access Session Recording
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
Web Access Session Recording captures browser-based Zero Trust Web Access (ZTWA) sessions for review, compliance, and incident investigation.

<Callout icon="far fa-circle-info" theme="info">
  This page describes ZTWA Helm chart 4.0.0 (app version 3.0.0). For earlier versions, see [Zero Trust Web Access on K8s (earlier versions)](https://docs.akeyless.io/docs/zero-trust-web-access-on-k8s-legacy-1).
</Callout>

> ℹ️ **Note:**
>
> If you are looking for Remote Desktop Protocol recordings, use [RDP Session Recording](https://docs.akeyless.io/docs/sra-rdp-recordings).

## Feature Scope

Web Access Session Recording covers two capabilities, both provided by the Media Server (the `mediamtx` DaemonSet, one pod per node):

* **Live view**: the user's isolated browser session is streamed to their browser by the Media Server over WebRTC, replacing the earlier VNC-based viewer. The recording is made from the same stream, so if the Media Server is unavailable, there's no live view and no recording.
* **Session recording**: the Media Server records each session to the shared volume mounted at `/etc/shared`, and the dispatcher uploads it to S3 or S3-compatible storage, with optional gzip compression and server-side encryption.

This feature is configured with deployment-time defaults in the Zero Trust Web Access chart `values.yaml`.

For ongoing Secure Remote Access session behavior, manage web and SSH settings through the Akeyless API by using the CLI or Console UI.

## Prerequisites

* **Shared storage**: recording needs a shared volume mounted at `/etc/shared`. Clusters with more than one node need a `ReadWriteMany` storage class, for example AWS EFS, Azure Files, GCP Filestore or NFS. Single-node clusters can use a node-scoped provisioner such as `local-path`. The chart fails to install if recording is enabled without it.
* **Live view connectivity**: UDP `8189` on every node must be reachable from users' browsers. If users can't reach the nodes' IPs, set a reachable address, for example a public IP, in `mediamtx.additionalHosts`.

## Session Correlation

ZTWA recordings use the same Secure Remote Access session identifier that appears in Session Overview and Audit Log entries.

For supported ZTWA versions, this identifier is a 24-digit numeric session ID.

To correlate a recording to a user account:

1. Get the session ID from the recording object key or filename.
2. Find the same session ID in Session Overview.
3. Review the associated Audit Log events for that session ID.

In audit events, the end user identity appears as `sra_unique_identifier`.

### Prerequisites For Session Visibility

If browser sessions run but Session Overview and Audit Log entries are missing, verify the following deployment settings:

* Ensure `config.clusterName` exactly matches the connected Akeyless Gateway cluster name.
* Authenticate ZTWA by using the same Access ID that the Gateway is registered with.
* If the Gateway certificate is private or self-signed, provide trust material to ZTWA by using `config.gatewayCert.tlsExistingSecret`.
* Ensure the Gateway is running and registered in the same Akeyless account.

## Configuration Surfaces

Use these surfaces:

* Primary: `recording` in `values.yaml`.

Deployment guidance: [Zero Trust Web Access on K8s](https://docs.akeyless.io/docs/sra-web-access-on-k8s).

## Configuration Reference

```yaml values.yaml
recording:
  enabled: true
  s3:
    enabled: true
    bucket: "<S3_BUCKET_NAME>"
    region: "<AWS_REGION>"
    prefix: "<OPTIONAL_PREFIX>"
    endpoint: "<OPTIONAL_S3_COMPATIBLE_ENDPOINT>"
    existingSecretName: "<S3_CREDENTIALS_SECRET_NAME>"
    accessKeyIdKey: "access-key-id"
    secretAccessKeyKey: "secret-access-key"
    compress: false
    sse:
      type: "" # "" | sse-s3 | sse-kms
      kmsKeyId: "<OPTIONAL_KMS_KEY_ID_OR_ARN>"
```

* `enabled`: Record sessions. Upload also needs `s3.enabled`.
* `s3.bucket`, `s3.region`, `s3.prefix`: Destination bucket and object path. `bucket` and `region` are required for upload.
* `s3.endpoint`: Endpoint of an S3-compatible service, for example MinIO. Leave empty for AWS S3.
* `s3.existingSecretName`: Secret with the S3 credentials, under the keys set in `accessKeyIdKey` and `secretAccessKeyKey`. When empty, the dispatcher uses the AWS default credential chain, for example IRSA or an instance profile.
* `s3.compress`: Gzip the recordings before upload.
* `s3.sse.type`, `s3.sse.kmsKeyId`: Server-side encryption (`sse-s3` or `sse-kms`). An empty `kmsKeyId` uses the default KMS key.

## End-to-End Workflow

1. Enable recording in `recording.enabled`.
2. Configure shared storage in `persistence.shareStorageVolume`. See [Prerequisites](https://docs.akeyless.io/docs/sra-web-access-session-recording#prerequisites).
3. Enable upload in `recording.s3.enabled` and configure the destination bucket and region.
4. Configure credential secret references or identity-based authentication.
5. Optionally configure compression and encryption.
6. Deploy or upgrade the chart.
7. Start a ZTWA browser session and verify the recording artifact in the configured storage destination.
8. Validate correlation by matching the session ID across the recording, Session Overview, and Audit Log.

## Related Pages

* [RDP Session Recording](https://docs.akeyless.io/docs/sra-rdp-recordings)
* [Session Management](https://docs.akeyless.io/docs/sra-session-management)
* [Zero Trust Web Access on K8s](https://docs.akeyless.io/docs/sra-web-access-on-k8s)
* [Zero Trust Web Access](https://docs.akeyless.io/docs/sra-web-access-topology)
* [Session Forwarding Destinations](https://docs.akeyless.io/docs/sra-session-forwarding-destinations)