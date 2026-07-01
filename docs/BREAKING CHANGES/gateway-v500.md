---
title: Gateway v5.0.0
deprecated: false
hidden: false
metadata:
  robots: index
---
# Upcoming breaking changes for Gateway v5.0.0

The next Gateway major version, `v5.0.0`, introduces changes to Gateway logs, metrics, and runtime architecture. This is the first step toward a more lightweight, secure, and higher-performing Gateway.

These changes primarily affect log and metrics scraping. Starting with Gateway `v5.0.0`, Akeyless is deprecating support for the legacy Gateway-managed telemetry and forwarding flows, including OpenTelemetry Collector-based telemetry, **Internal** Splunk Forwarder, Loki, and Syslog/RSyslog components.&#x20;

Each change moves Gateway observability toward standard runtime-native collection patterns.

## What is changing

### Logs are shifted to `STDOUT`

Gateway logs are no longer intended to be collected from local log files.

Update your logging pipeline to collect Gateway logs from `STDOUT` using your container runtime, Kubernetes, or logging agent.

### Logs are formatted as JSON

Gateway logs now use JSON format.

Update any custom parsing rules, dashboards, alerts, or log processing pipelines that rely on the previous log format.

### Metrics are exposed through a native Gateway endpoint

The legacy OpenTelemetry Collector-based telemetry flow is deprecated.

Update your monitoring system to scrape metrics directly from the native Gateway metrics endpoint: `https://<Your-Gateway-URL>:8000/metrics`

Make sure your monitoring system has network access to the Gateway URL and port.

### Gateway and Curl Proxy are unified into a single process

Gateway `v5.0.0` unifies the Gateway and Curl Proxy runtime into a single process.

Review any deployment, monitoring, or process-level assumptions that depend on the Gateway and Curl Proxy running as separate processes.

### ARM-based Gateway images are supported

Gateway `v5.0.0` adds support for ARM-based deployments.

Review your deployment configuration and image selection if you plan to run Gateway on ARM-based infrastructure.

## Deprecated integrations

Starting with Gateway `v5.0.0`, the following Gateway-managed telemetry and **Internal** forwarding integrations are deprecated:

- OpenTelemetry Collector-based telemetry
- Splunk Forwarder
- Loki
- Syslog/RSyslog

If you currently rely on one of these **Internal&#x20;**&#x69;ntegrations, move the forwarding responsibility to your runtime, orchestration platform, or logging agent.

## Who is affected

You may be affected if you currently rely on any of the following:

- Scraping Gateway logs from local log files.
- Parsing Gateway logs in the previous non-JSON format.
- Using the embedded OpenTelemetry Collector-based telemetry flow.

## How to prepare

Before upgrading to Gateway v5.0.0, review your current Gateway observability configuration.

Update your logging configuration to collect logs from `STDOUT`.

Update your log parsers, dashboards, alerts, and processing pipelines to support the new JSON log format.

Update your metrics scraping configuration to use the native Gateway `/metrics` endpoint.

If you currently rely on Gateway-managed forwarding to OTel, Loki, etc. move that forwarding responsibility to your runtime, orchestration platform, or logging agent.

<br />