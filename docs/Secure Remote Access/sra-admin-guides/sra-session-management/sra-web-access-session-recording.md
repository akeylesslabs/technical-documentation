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

> ℹ️ **Note:**
>
> If you are looking for Remote Desktop Protocol recordings, use [RDP Session Recording](https://docs.akeyless.io/docs/sra-rdp-recordings).

## Feature Scope

Web Access Session Recording covers:

* Browser session video capture.
* Recording quality selection.
* Upload to S3 or S3-compatible storage.
* Optional gzip compression before upload.
* Optional server-side encryption options.
* Lifecycle watchdog controls for recording duration and client-connect timing.

This feature is configured with deployment-time defaults in the Zero Trust Web Access chart `values.yaml`.

For ongoing Secure Remote Access session behavior, manage web and SSH settings through the Akeyless API by using the CLI or Console UI.

## Session Correlation

ZTWA recordings, Session Overview entries, and Audit Log events are correlated by the same Secure Remote Access session identifier.

For supported ZTWA versions, this identifier is a 24-digit numeric session ID.

To correlate a recording to a user account:

1. Get the session ID from the recording object key or filename.
2. Find the same session ID in Session Overview.
3. Review the associated Audit Log events for that session ID.

In audit events, the end user identity appears as `sra_unique_identifier`.

### Prerequisites For Session Visibility

If browser sessions run but Session Overview and Audit Log entries are missing, verify the following deployment settings:

* Use a ZTWA version that includes session reporting (`v2.0.0-rc6` or later).
* Ensure `clusterName` exactly matches the connected Akeyless Gateway cluster name.
* Authenticate ZTWA by using the same Access ID that the Gateway is registered with.
* If the Gateway certificate is private or self-signed, provide trust material to ZTWA.
* Ensure the Gateway is running and registered in the same Akeyless account.

## Configuration Surfaces

Use these surfaces:

* Primary: `sessionRecording` in `values.yaml`.
* Advanced overrides:
    * `dispatcher.config.recording`
    * `webWorker.config.recording`

Deployment guidance: [Zero Trust Web Access on K8s](https://docs.akeyless.io/docs/sra-web-access-on-k8s).

## Configuration Reference

### Base Recording Controls

* `sessionRecording.enabled`: Enables worker-side recording capture.
* `sessionRecording.quality`: Recording quality (`144p`, `240p`, `360p`, `480p`, `720p`, `1080p`).

### Upload Controls

* `sessionRecording.upload.enabled`
* `sessionRecording.upload.s3Bucket`
* `sessionRecording.upload.s3Region`
* `sessionRecording.upload.s3Prefix`
* `sessionRecording.upload.s3Endpoint` (optional S3-compatible endpoint)
* `sessionRecording.upload.compress`

### Encryption Controls

* `sessionRecording.upload.sse.type` (`""`, `sse-s3`, `sse-kms`)
* `sessionRecording.upload.sse.kmsKeyId`

### Credentials and Secret Wiring

* `sessionRecording.upload.existingSecretNames.s3`
* `sessionRecording.upload.existingSecretNames.s3AccessKeyIdKey`
* `sessionRecording.upload.existingSecretNames.s3SecretAccessKeyKey`

If no secret is set, upload can use the AWS default credential chain.

### Watchdog Controls

* `sessionRecording.watchdog.clientConnectTimeoutSeconds`
* `sessionRecording.watchdog.intervalSeconds`
* `sessionRecording.watchdog.maxDurationSeconds`

These settings help bound long-running recordings and clean up stalled sessions.

### Service-Level Overrides

Dispatcher upload override fields can be set in `dispatcher.config.recording`.

Worker capture override fields (`enabled`, `quality`) can be set in `webWorker.config.recording`.

Use overrides only when service-specific behavior must differ from the shared `sessionRecording` block.

## End-to-End Workflow

1. Enable recording in `sessionRecording.enabled`.
2. Set desired recording quality.
3. Enable upload and configure destination bucket and region.
4. Configure credential secret references or identity-based authentication.
5. Optionally configure compression and encryption.
6. Optionally tune watchdog values for long-running workloads.
7. Deploy or upgrade the chart.
8. Start a ZTWA browser session and verify the recording artifact in the configured storage destination.
9. Validate correlation by matching the session ID across the recording, Session Overview, and Audit Log.

## Related Pages

* [RDP Session Recording](https://docs.akeyless.io/docs/sra-rdp-recordings)
* [Session Management](https://docs.akeyless.io/docs/sra-session-management)
* [Zero Trust Web Access on K8s](https://docs.akeyless.io/docs/sra-web-access-on-k8s)
* [Session Forwarding Destinations](https://docs.akeyless.io/docs/sra-session-forwarding-destinations)
