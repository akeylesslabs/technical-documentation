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
---
Session Management provides users with full control over how session activities are recorded, stored, and forwarded for auditing and analysis. Through the platform’s UI, users can enable session recording and configure how session data is forwarded to external systems.

Key actions include enabling session recording for various types of remote access sessions, configuring log forwarding for CLI-based sessions, and managing video recordings for RDP and web-access sessions.

## Session Recording

### RDP Session Recording

[RDP session recording](https://docs.akeyless.io/docs/sra-rdp-recordings) refers to the process of capturing and storing the activities that occur during a Remote Desktop Protocol (RDP) session. These recordings create a video file of the entire session, preserving all user interactions within the remote desktop environment.

SRA allows you to automatically upload and store these video recordings in secure locations such as AWS S3 or Azure Blob Storage for long-term retention and review, or you can store them locally on the server.

### Web Access Session Recording

[Web access session recording](https://docs.akeyless.io/docs/sra-web-access-on-k8s) refers to the process of capturing browser-based web access sessions in Zero Trust Web Access (ZTWA). These recordings preserve the interactive web session and can be stored with the ZTWA deployment configuration.

### Terminal-Based Sessions

For terminal-based sessions (such as SSH, DB, and Kubernetes), the system records a full transcript of the commands entered and their corresponding outputs. This data can be forwarded to external systems like Splunk, Elasticsearch, or by way of Syslog for monitoring and archiving. See more [here](https://docs.akeyless.io/docs/sra-session-forwarding).

## Secret Locking and Rotation Timing

For sessions that use **Static Secret** and **Rotated Secret** items, Session Management supports the following controls:

* **Lock secret while session is active:** Locks the secret for read and update actions while the SRA session is active.
* **Rotate after disconnection:** Rotates the secret value when the SRA session ends.
* **Delayed rotation after disconnection:** For rotated secrets, schedules rotation to run after a configured delay in minutes.

To configure these controls, open the relevant item and edit its **Secure Remote Access** settings in the Akeyless Console.

## Session TTL Behavior

For standalone bastion deployments, the default session TTL is unlimited (`0`). In unified deployments, administrators can configure the session TTL in Gateway **Remote Access** settings.

## Hide Session Recording Indications

By default, a red blinking indicator appears to users to show that their session is being recorded. To hide the recording indicator, toggle the "Hide Session Recording Indications" slider in the "Remote Access" -> "Configuration" section within the Gateway settings in the UI.
