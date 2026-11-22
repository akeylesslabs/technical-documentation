---
title: Storage and Recording Capacity
excerpt: ''
deprecated: false
hidden: false
metadata:
  title: ''
  description: ''
  robots: index
next:
  description: ''
slug: sra-storage-and-recording-capacity
---
Use this page to plan recording storage growth, retention policy, and backend-specific lifecycle controls.

For baseline deployment prerequisites and session-recording compatibility checks, start with [SRA Requirements](https://docs.akeyless.io/docs/sra-requirements).

For recording retrieval and operational review, use [RDP Recordings](https://docs.akeyless.io/docs/sra-rdp-recordings), [Web Access Session Recording](https://docs.akeyless.io/docs/sra-web-access-session-recording), and [Session Management](https://docs.akeyless.io/docs/sra-session-management).

## Capacity Model by Session Type

Recorded size depends on codec settings, session duration, and screen activity more than on a flat per-hour rate. Static screens consume almost no storage; constant UI movement is what drives usage up. Use these ranges as initial planning inputs, not hard limits, and validate with representative workloads before final capacity commitments:

| Session type              | Typical artifact                      | Planning range                                                                       |
| ------------------------- | ------------------------------------- | ------------------------------------------------------------------------------------- |
| RDP video recording       | Encoded video (`.enc` or `.enc.gzip`) | Approximately `150 MB` to `1.5 GB` per hour, depending on screen-change rate          |
| Web access recording      | Browser session video artifact        | Approximately `100 MB` to `1.2 GB` per hour, depending on page activity and media use |
| SSH and terminal sessions | Text command transcript and metadata  | Much smaller than video artifacts; plan by retention count and audit needs, not by hourly rate |

## Recording Storage Backends

Recording storage supports these backend types:

* Local filesystem on the SRA host
* Amazon S3
* Azure Blob Storage
* NetApp StorageGRID and other S3-compatible object storage

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

### NetApp StorageGRID and Other S3-Compatible Storage

Apply vendor-specific object lifecycle policy at bucket level and validate API compatibility for lifecycle enforcement.

## Local Storage Limits and Production Risk

Local storage is useful for testing and short-lived environments, but is risky for long-term production retention.

Primary risks:

* Host disk exhaustion can interrupt recording workflows.
* Storage scaling is tied to host lifecycle operations.
* Disaster recovery is harder without external object storage replication.

For production environments, prefer object storage backends and reserve local storage for temporary buffering or non-critical scenarios.
