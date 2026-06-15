---
title: Sessions Overview
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
The Sessions Overview provides administrators and authorized users with the ability to view and track the status of SRA sessions. This view helps ensure that all session activities are visible, auditable, and managed effectively over a specified timeframe (default: last 30 days).

For CLI-driven monitoring and automation, use `list-sra-sessions` to query the same operational inventory by status and resource type.

## Session Overview Grid

The Session Overview page displays detailed information for each session. The following key details are provided:

* **Client Interface**: Indicates how the session was initiated. Options include: Web Portal - CLI, Web Portal - Web, CLI and Desktop Application)
* **User**: The username of the individual who initiated the session.
* **Gateway Name**: The name of the gateway through which the session is managed.
* **Resource Type**: The type of resource accessed during the session. Examples include: SSH, RDP, databases, Kubernetes (K8s), and more.
* **Secret Name**: The identifier for the secret used during the session.
* **Session ID**: The unique Secure Remote Access session identifier.
* **Status**: The current state of the session (For example, active, closed, or terminated).
* **Duration**: The length of time the session has been active.

For Zero Trust Web Access sessions, the same session ID is used in Session Overview, Audit Log entries, and recording artifacts.

## Real-Time Updates

* **Auto-Refresh**: The sessions list automatically updates every 20 seconds to ensure the displayed information is current.
* **Manual Refresh**: Users have the option to manually refresh the list by clicking the Refresh button.

## Filtering Options

Users can filter the session list based on the following criteria to quickly locate specific sessions:

* Client Interface
* Resource Type
* Gateway Name
* Status

## CLI Session Inventory

Use `list-sra-sessions` to retrieve session inventory from the command line:

```shell
akeyless list-sra-sessions
```

By default, this command returns active statuses only (`connecting`, `connected`).

To include closed or ended sessions, specify status filters explicitly:

```shell
akeyless list-sra-sessions --status-type completed
```

Filter by resource type as needed:

```shell
akeyless list-sra-sessions --status-type connected --resource-type ssh
```

Supported status filters include `connecting`, `connected`, `failed`, `completed`, and `terminated`.

For API details, see [List SRA Sessions](https://docs.akeyless.io/reference/listsrasessions).

## Audit Logging

Every session update is captured in the Audit Log, including the Secure Remote Access Session ID. This ensures that any changes (such as status updates or modifications) are recorded for compliance and troubleshooting purposes.

For Zero Trust Web Access session events, user identity is recorded in `sra_unique_identifier`.

## Permissions

* **Self-Session Visibility**: Any user who initiates a session is permitted to view their own session details (there is no need to specify any permission for that).
* **Extended Visibility for SRA Application Servers**: If a user has permissions to access one or more SRA application servers, they can view all sessions managed by those servers.
* **Admin Access**: Administrators have full visibility of all sessions within the selected timeframe.

> ℹ️ **Note (Permission Configuration):**
>
> To configure access to SRA Application servers, go to **Access Roles** -> **Administrative Rules** -> **Secure Remote Access.**
>
> Choose **Own** for allowing access to specific SRA servers (also known as Extended Visibility) or **All** for all SRA servers (also known as Admin Access)

## Accessing Session Monitoring

To access the Session Monitoring feature:

1. Log in to the Console UI.
2. Open the Secure Remote Access sessions view in the Console UI. From this interface, you can view all SRA sessions within the selected timeframe, apply filters, refresh session data, and review Audit Logs.
