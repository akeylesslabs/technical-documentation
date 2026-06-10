---
title: Session Forwarding Destinations
slug: sra-session-forwarding-destinations
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
Use this page to configure terminal-session forwarding destinations for Secure Remote Access (SRA).

Terminal-based sessions (SSH, database CLI, and Kubernetes CLI flows) can forward command and output logs to external systems for monitoring, retention, and compliance workflows.

## Supported Destinations

The supported forwarding targets are:

* Splunk
* Datadog
* Logstash
* Logz.io
* Sumo Logic
* Elasticsearch
* Azure Log Analytics
* Google Chronicle
* Syslog
* stdout
* AWS S3

This list matches the current forwarding endpoint family in the API reference.

## Configuration Surfaces

Use one of the following:

* Console path: **Gateways**, then **Manage Gateway**, then **Remote Access**, then **Session Forwarding**.
* CLI command family: `gateway-update-remote-access-session-forwarding-*`
* API endpoint family: `gwupdateremoteaccesssessionlogs*`

For full command flags and provider-specific payload details, see [CLI Reference - Gateway Secure Remote Access](https://docs.akeyless.io/docs/cli-reference-sra) and [API and SDK Workflows](https://docs.akeyless.io/docs/sra-api-and-sdk-workflows).

## Minimal CLI Pattern

```shell
akeyless gateway update remote-access-session-forwarding <provider>
```

Replace `<provider>` with the destination-specific command variant documented by the CLI reference.

## Related API Endpoints

* [AWS S3 forwarding endpoint](https://docs.akeyless.io/reference/gwupdateremoteaccesssessionlogsawss3)
* [Azure Log Analytics forwarding endpoint](https://docs.akeyless.io/reference/gwupdateremoteaccesssessionlogsazureanalytics)
* [Datadog forwarding endpoint](https://docs.akeyless.io/reference/gwupdateremoteaccesssessionlogsdatadog)
* [Elasticsearch forwarding endpoint](https://docs.akeyless.io/reference/gwupdateremoteaccesssessionlogselasticsearch)
* [Google Chronicle forwarding endpoint](https://docs.akeyless.io/reference/gwupdateremoteaccesssessionlogsgooglechronicle)
* [Logstash forwarding endpoint](https://docs.akeyless.io/reference/gwupdateremoteaccesssessionlogslogstash)
* [Logz.io forwarding endpoint](https://docs.akeyless.io/reference/gwupdateremoteaccesssessionlogslogzio)
* [Splunk forwarding endpoint](https://docs.akeyless.io/reference/gwupdateremoteaccesssessionlogssplunk)
* [stdout forwarding endpoint](https://docs.akeyless.io/reference/gwupdateremoteaccesssessionlogsstdout)
* [Sumo Logic forwarding endpoint](https://docs.akeyless.io/reference/gwupdateremoteaccesssessionlogssumologic)
* [Syslog forwarding endpoint](https://docs.akeyless.io/reference/gwupdateremoteaccesssessionlogssyslog)
