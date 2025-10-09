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

Key actions include enabling session recording for various types of remote access sessions, configuring log forwarding for CLI-based sessions, and managing video recordings for RDP sessions.

# Session Recording

## RDP Session Recording

[RDP session recording](https://docs.akeyless.io/docs/rdp-recordings) refers to the process of capturing and storing the activities that occur during a Remote Desktop Protocol (RDP) session. These recordings create a video file of the entire session, preserving all user interactions within the remote desktop environment. 

SRA allows you to automatically upload and store these video recordings in secure locations such as AWS S3 or Azure Blob Storage for long-term retention and review, or you can store them locally on the server.

## Terminal-Based Sessions

For terminal-based sessions (such as SSH, DB, and Kubernetes), the system records a full transcript of the commands entered and their corresponding outputs. This data can be forwarded to external systems like Splunk, ElasticSearch, or via Syslog for monitoring and archiving. See more [here](https://docs.akeyless.io/docs/session-forwarding).

# Hide Session Recording Indications

By default, an red blinking indicator will appear to users noting that their session is being recorded. To hide the recording indicator, toggle the "Hide Session Recording Indications" slider in the "Remote Access" -> "Configuration" section within the Gateway settings in the UI.
