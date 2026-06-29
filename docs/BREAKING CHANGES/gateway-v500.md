---
title: Gateway v5.0.0
deprecated: false
hidden: false
metadata:
  robots: index
---
````md
# Upcoming breaking changes for Akeyless Gateway v5.0.0

The next Akeyless Gateway major version, v5.0.0, introduces changes to Gateway logs, metrics, and runtime architecture. This is the first step toward a more lightweight, secure, and higher-performing Gateway.

These changes primarily affect log and metrics scraping. Starting with Gateway v5.0.0, Akeyless is deprecating support for the legacy Gateway-managed telemetry and forwarding flows, including OpenTelemetry Collector-based telemetry, Splunk Forwarder, Loki, and Syslog/RSyslog.

Each change moves Gateway observability toward standard runtime-native collection patterns:

- **Logs are shifted to `STDOUT`**: Gateway logs are no longer intended to be collected from local log files. Update your logging pipeline to collect logs from `STDOUT` using your container runtime, Kubernetes, or logging agent.

- **Logs are formatted as JSON**: Gateway logs now use JSON format. Update any custom parsing rules, dashboards, alerts, or log processing pipelines that rely on the previous log format.

- **Metrics are exposed through a native Gateway endpoint**: The legacy OpenTelemetry Collector-based telemetry flow is deprecated. Update your monitoring system to scrape metrics directly from:

  ```text
  https://<Your-Gateway-URL>:8000/metrics
````

* **Gateway and Curl Proxy are unified into a single process**: Gateway v5.0.0 unifies the Gateway and Curl Proxy runtime. Review any deployment, monitoring, or process-level assumptions that depend on them running as separate processes.

* **ARM-based Gateway images are supported**: Gateway v5.0.0 adds support for ARM-based deployments.

## How to prepare

Before upgrading to Gateway v5.0.0, review your current Gateway observability configuration.

Update your logging configuration to collect logs from `STDOUT`, update log parsers to support JSON, and update metrics scraping to use the native Gateway `/metrics` endpoint. If you currently rely on Gateway-managed forwarding to OTel, Splunk Forwarder, Loki, or Syslog/RSyslog, move that forwarding responsibility to your runtime, orchestration platform, or logging agent.

More details are available in the Gateway telemetry documentation: <ADD_LINK>.

For questions or feedback, contact Akeyless Support or your Akeyless representative.

```
```
