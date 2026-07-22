---
title: Copy of Storage and Recording Capacity
deprecated: false
hidden: true
metadata:
  robots: index
---
Use this page to plan recording storage growth, retention policy, and backend-specific lifecycle controls.

For baseline deployment prerequisites and session-recording compatibility checks, start with [SRA Requirements](https://docs.akeyless.io/docs/sra-requirements).

For recording retrieval and operational review, use [RDP Recordings](https://docs.akeyless.io/docs/sra-rdp-recordings), [Web Access Session Recording](https://docs.akeyless.io/docs/sra-web-access-session-recording), and [Session Management](https://docs.akeyless.io/docs/sra-session-management).

## Capacity Model by Session Type

Recorded size depends on codec settings, session duration, and user interaction density.

Use these planning ranges as initial estimates:

| Session type | Typical artifact | Planning range | Lower-band scenario | Upper-band scenario |
| --- | --- | --- | --- | --- |
| RDP video recording | Encoded video (`.enc` or `.enc.gzip`) | Approximately `150 MB` to `1.5 GB` per hour | Mostly static admin tasks, low screen-change rate, shorter sessions | High-motion UI activity, frequent full-screen refreshes, longer continuous sessions |
| Web access recording | Browser session video artifact | Approximately `100 MB` to `1.2 GB` per hour | Form-based workflows and low navigation churn | Media-heavy pages, frequent page reloads, high interaction density |
| SSH and terminal sessions | Text command transcript and metadata | Usually much smaller than video artifacts; plan by retention count and audit needs | Short command-only sessions with minimal output | Long sessions with verbose command output and frequent file/content dumps |

Treat these ranges as sizing inputs, not hard limits. Validate with representative workloads before final capacity commitments.

### How to Estimate Where You Fall in the Range

Use this quick method to choose a realistic planning band:

1. Sample 3 to 5 representative sessions per access type (RDP, web, SSH).
2. Capture duration and resulting artifact size for each sample.
3. Convert each sample to hourly size (`artifact_size / session_minutes * 60`).
4. Use the 75th percentile of your sample set as the baseline planning value.
5. Add a 20% to 30% buffer for peak periods and retention-policy overlap.

For initial planning before full measurements are available:

1. Use the lower half of the range for low-interaction operational access.
2. Use the upper half of the range for high-activity troubleshooting, GUI-heavy work, or long-lived sessions.

## Recording Storage Backends

RDP recording storage supports:

* Amazon S3
* S3-compatible object storage
* Azure Blob Storage
* Local filesystem on the SRA host

Use [RDP Recordings](https://docs.akeyless.io/docs/sra-rdp-recordings) for backend configuration flags and examples.

## Retention and Cleanup Strategy

Plan retention at two levels:

1. Platform-level retention policy (bucket/container lifecycle rules).
2. Runtime-level operational cleanup policy (for local storage and non-lifecycle paths).

Recommended approach:

* Keep raw storage retention short for high-volume environments.
* Archive only required compliance windows.
* Separate hot review window from long-term archival policy.

## Backend-Specific Lifecycle Guidance

### Amazon S3

Use S3 lifecycle rules at bucket or prefix level to expire, transition, or archive recording objects automatically.

### Azure Blob Storage

Use Azure lifecycle management and tiering policies to move older recordings to lower-cost tiers.

### GCS and Other Archive Targets

If recordings are copied to Google Cloud Storage or another archive platform in your post-processing pipeline, apply equivalent object lifecycle rules there as well.

### S3-Compatible Storage

For S3-compatible systems, apply vendor-specific object lifecycle policy at bucket level and validate API compatibility for lifecycle enforcement.

## Local Storage Limits and Production Risk

Local storage is useful for testing and short-lived environments, but is risky for long-term production retention.

Primary risks:

* Host disk exhaustion can interrupt recording workflows.
* Storage scaling is tied to host lifecycle operations.
* Disaster recovery is harder without external object storage replication.

For production environments, prefer object storage backends and reserve local storage for temporary buffering or non-critical scenarios.