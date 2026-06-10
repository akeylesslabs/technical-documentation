---
title: CLI Commands and Flags
slug: sra-cli-commands-and-flags
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
Use this page as a quick index of the SRA-related CLI command families. This page is intentionally concise and links to the full command reference.

For complete syntax and flag behavior, use the Gateway CLI reference area and the SRA command page:

* [CLI Reference - Gateway](https://docs.akeyless.io/docs/cli-reference-gateway)
* [CLI Reference - Gateway Secure Remote Access](https://docs.akeyless.io/docs/cli-reference-sra)

## Command Families

* `gateway-update-remote-access`: Configure core SRA bastion behavior, such as allowed URLs, session TTL, username claim mapping, and SSH key exchange settings.
* `gateway-update-remote-access-rdp-recording`: Configure RDP session recording storage, quality, compression, and encryption.
* `gateway-update-remote-access-desktop-app`: Configure Secure Remote Access Desktop Application defaults and control-path settings.
* `gateway-update-remote-access-session-forwarding-*`: Configure session log forwarding providers.
* `list-sra-sessions`: List SRA sessions. Default behavior is scoped to active statuses and own-user scope unless explicit filters and permissions expand visibility.
* `list-sra-bastions`: List bastion clusters and instances for operational inventory and health-oriented review.

## Notes

* Use `list-sra-sessions` filters to include closed session states (`failed`, `completed`, `terminated`) when needed.
* Use `list-sra-bastions --allowed-urls-only true` when reviewing bastion URL hardening configuration.
* Use the CLI reference page as the source of truth for accepted aliases and parameter names.
