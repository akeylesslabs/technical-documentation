---
title: Session Log Forwarding
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
Remote Access supports the forwarding of SSH, Database, and Kubernetes session logs.

> ℹ️ **Note:**
>
> Session forwarding destination configuration is part of Integrations and Automation content structure. Keep this page as command-level reference content.

These terminal-based sessions provide a full transcript of input commands and output responses which can be forwarded to any Log Management / SIEM solution (such as Splunk, Elasticsearch, or just using Syslog).

## Configure

From the Console, click on "Gateways" in the left-side menu.

Choose the Gateway you want to update and then click the "Manage Gateway" button. If you don't have enough permissions, the button will be greyed out and you should check with your Admin for permissions.

From the Manage Gateway section, choose "Remote Access" -> "Session Forwarding" -> "Session Forwarding", click the slider to Enable, and add the log forwarder information. Once done, click "Save".

You can also configure session forwarding by using the CLI:

```shell
akeyless gateway update remote-access-session-forwarding <provider>
```

For provider-specific commands and flags, see [CLI Reference - Gateway Secure Remote Access](https://docs.akeyless.io/docs/cli-reference-sra).
