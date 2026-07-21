---
title: Session Management
excerpt: ''
deprecated: false
hidden: false
metadata:
  title: ''
  description: ''
  robots: index
next:
  description: ''
slug: sra-session-management
---
Session Operations and Monitoring provides operational guidance for administrators who monitor active sessions, review recording data, track bastion fleet health, and detect upgrade-related drift.

Use this section to move from reactive troubleshooting to continuous runtime monitoring.

## Start Here by Objective

1. Fleet health and instance monitoring: [Cluster and Instance Health](https://docs.akeyless.io/docs/sra-cluster-and-instance-health)
2. Active and historical session visibility: [Sessions Overview](https://docs.akeyless.io/docs/sra-sessions-overview)
3. Session recording storage and retrieval: [RDP Recordings](https://docs.akeyless.io/docs/sra-rdp-recordings) and [Web Access Session Recording](https://docs.akeyless.io/docs/sra-web-access-session-recording)
4. Upgrade and compatibility monitoring: [Version Drift and Upgrade Signals](https://docs.akeyless.io/docs/sra-version-drift-and-upgrade-signals)
5. **request access**

For storage sizing and retention planning, use [Storage and Recording Capacity](https://docs.akeyless.io/docs/sra-storage-and-recording-capacity).

## Session Inventory and Recordings

Session inventory includes both active and completed lifecycle states, filtered by status, resource type, and visibility scope.

Use [Sessions Overview](https://docs.akeyless.io/docs/sra-sessions-overview) for UI monitoring and `list-sra-sessions` for CLI-driven operational queries.

## Session Recording

### RDP Session Recording

[RDP session recording](https://docs.akeyless.io/docs/sra-rdp-recordings) refers to the process of capturing and storing the activities that occur during a Remote Desktop Protocol (RDP) session. These recordings create a video file of the entire session, preserving all user interactions within the remote desktop environment.

SRA allows you to automatically upload and store these video recordings in secure locations such as AWS S3 or Azure Blob Storage for long-term retention and review, or you can store them locally on the server.

### Web Access Session Recording

[Web access session recording](https://docs.akeyless.io/docs/sra-web-access-session-recording) captures browser-based web access sessions in Zero Trust Web Access (ZTWA). These recordings preserve the interactive web session and can be stored by using the ZTWA deployment configuration.

For full recording configuration options (quality, upload destination, compression, encryption, watchdog controls, and service-level overrides), see [Web Access Session Recording](https://docs.akeyless.io/docs/sra-web-access-session-recording).

### Terminal-Based Sessions

For terminal-based sessions (such as SSH, DB, and Kubernetes), the system records a full transcript of the commands entered and their corresponding outputs. Session forwarding destination guidance is documented under Integrations and Automation.

<Callout icon="ℹ️" theme="info">
  ### **Note:**

  Session recording and terminal session forwarding are different features. Use [RDP Recordings](https://docs.akeyless.io/docs/sra-rdp-recordings) for RDP video capture and [Web Access Session Recording](https://docs.akeyless.io/docs/sra-web-access-session-recording) for browser-based ZTWA video capture.
</Callout>

## Secret Locking and Rotation Timing

For sessions that use **Static Secret** and **Rotated Secret** items, Session Management supports the following controls:

- **Lock secret while session is active:** Locks the secret for read and update actions while the SRA session is active.
- **Rotate after disconnection:** Rotates the secret value when the SRA session ends.
- **Delayed rotation after disconnection:** For rotated secrets, schedules rotation to run after a configured delay in minutes.

To configure these controls, open the relevant item and edit its **Secure Remote Access** settings in the Akeyless Console.

## Session TTL Behavior

For standalone bastion deployments, the default session TTL is unlimited (`0`). In unified deployments, administrators can configure the session TTL in Gateway **Remote Access** settings.

For upgrade-phase validation and drift handling, see [Version Drift and Upgrade Signals](https://docs.akeyless.io/docs/sra-version-drift-and-upgrade-signals).

## Hide Session Recording Indications

By default, a red blinking indicator appears to users to show that their session is being recorded. To hide the recording indicator, toggle the "Hide Session Recording Indications" slider in the "Remote Access" -> "Configuration" section within the Gateway settings in the UI.
