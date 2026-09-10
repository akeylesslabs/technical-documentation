---
title: Telemetry and Metrics
deprecated: false
hidden: false
metadata:
  title: ''
  description: ''
  robots: index
next:
  description: ''
---

# Gateway Telemetry Metrics

Akeyless Gateway telemetry metrics provide time-series data about the Gateway application and runtime environment. You can use these metrics to build dashboards, configure alerts, and monitor Gateway health, resource usage, API traffic, SaaS connectivity, and account quota usage.

Starting from Akeyless Gateway v5.0.0, Gateway metrics are exposed through a dedicated metrics endpoint: `https://<Your-Gateway-URL>:8000/metrics`

The endpoint can be scraped or collected by monitoring and alerting solutions such as Prometheus and Datadog.

<Callout icon="📘" theme="info">
  ### New telemetry endpoint

  Starting from Akeyless Gateway v5.0.0, the legacy metrics solution is deprecated. Gateway metrics are now exposed through the `/metrics` endpoint on port `8000` and can be collected by external monitoring solutions.
</Callout>

## Overview

Gateway telemetry metrics help you monitor the operational status of your Gateway deployment.

You can use these metrics to track:

- Gateway pod health
- Connectivity to Akeyless SaaS backend services
- Gateway API traffic
- HTTP response status codes
- Account quota usage
- CPU, memory, disk, load, and network utilization

## Collection Model

Akeyless Gateway exposes metrics through a pull-based `/metrics` endpoint.

Monitoring systems such as Prometheus can scrape this endpoint directly. If you use Datadog, see [Datadog Integration](#datadog-integration) below for the supported Agent configuration.

The Gateway does not store long-term metric history. Use an external metrics backend for historical analysis, dashboards, and alerting.

## Prerequisites

Before enabling telemetry metrics, make sure that:

- Gateway v5.0.0 or later is deployed.
- Metrics are enabled on the Gateway.
- Port `8000` is reachable from your monitoring system.
- The monitoring system is configured with the correct `http` or `https` scheme.
- For Kubernetes deployments, Prometheus or your monitoring agent can access the Gateway Service.
- If you need network I/O or memory limit metrics, `GW_METRICS_NET_IFACE` and `MEM_LIMIT` are set correctly (see [Configuration](#configuration)).

## Available Metrics

| Metric | Type | Purpose |
|---|---|---|
| `akeyless_gw_system_cpu_usage_percent` | Gauge | Process CPU utilization |
| `akeyless_gw_system_cpu_load_average_1m` | Gauge | 1-minute CPU load average |
| `akeyless_gw_system_cpu_load_average_5m` | Gauge | 5-minute CPU load average |
| `akeyless_gw_system_cpu_load_average_15m` | Gauge | 15-minute CPU load average |
| `akeyless_gw_system_cpu_throttled_periods_total` | Gauge (despite `_total` suffix) | Number of CPU throttling periods |
| `akeyless_gw_system_cpu_throttled_seconds_total` | Gauge (despite `_total` suffix) | Time spent CPU throttled, in seconds |
| `akeyless_gw_system_disk_io_read_bytes` | Gauge | Disk bytes read |
| `akeyless_gw_system_disk_io_write_bytes` | Gauge | Disk bytes written |
| `akeyless_gw_system_memory_usage_in_bytes` | Gauge | Process memory usage |
| `akeyless_gw_system_network_io_receive_bytes` | Gauge | Network bytes received. Requires `GW_METRICS_NET_IFACE` to be set, see [Configuration](#configuration) below |
| `akeyless_gw_system_network_io_transmit_bytes` | Gauge | Network bytes transmitted. Requires `GW_METRICS_NET_IFACE` to be set, see [Configuration](#configuration) below |
| `akeyless_gw_system_saas_connection_status` | Gauge (0/1) | Connectivity to the Akeyless SaaS backend (1=connected, 0=disconnected) |
| `akeyless_gw_system_healthcheck_status` | Gauge (0/1) | Container health check (1=healthy, 0=unhealthy) |
| `akeyless_gw_quota_current_transactions_number` | Gauge | Current account transaction count |
| `akeyless_gw_quota_gw_admin_client_transactions` | Gauge | Gateway default identity transactions |
| `akeyless_gw_quota_total_transactions_limit` | Gauge | Hourly transaction ceiling |
| `akeyless_gw_system_request_count_total` | Counter | Total Gateway API requests. Also emitted without the `_total` suffix as a legacy alias |
| `akeyless_gw_system_http_response_status_code_total` | Counter | HTTP response status codes. Also emitted without the `_total` suffix as a legacy alias |

<Callout icon="⚠️" theme="warning">
  ### Throttling metrics are gauges, not counters

  `akeyless_gw_system_cpu_throttled_periods_total` and `akeyless_gw_system_cpu_throttled_seconds_total` are emitted as gauges despite their `_total` suffix. Do not apply `rate()` or `increase()` to them.
</Callout>

## Configuration

**Docker:** Set environment variable `ENABLE_METRICS="true"`

**Kubernetes:** Configure in values.yaml:

```
globalConfig:
  metrics:
    enabled: true
```

**Network interface (for network I/O metrics):** Set `GW_METRICS_NET_IFACE` to the interface to measure (for example `eth0`). Without it, `network_io_receive_bytes` / `network_io_transmit_bytes` report a flat `0` - most commonly missed on standalone Docker deployments.

**Memory limit (for the memory limit metric):** Set `MEM_LIMIT` as a plain byte count (for example `536870912`), not a suffixed value such as `512Mi` - suffixed values are silently rejected and the metric never appears.

## Datadog Integration

Datadog is a push-based backend, so `/metrics` must be scraped and forwarded to it; it will not pull the endpoint on its own. Install the [Datadog Agent](https://docs.datadoghq.com/containers/kubernetes/installation/) somewhere that can reach the Gateway on port `8000`, and configure it to scrape `/metrics` via an [OpenMetrics Autodiscovery check](https://docs.datadoghq.com/integrations/openmetrics/):

```yaml
annotations:
  ad.datadoghq.com/akeyless-gateway.checks: |
    {
      "openmetrics": {
        "instances": [
          {
            "openmetrics_endpoint": "http://%%host%%:8000/metrics",
            "namespace": "akeyless",
            "metrics": ["akeyless_gw_.*"]
          }
        ]
      }
    }
```

Metrics then appear in Datadog under `<namespace>.akeyless_gw_*` (for example `akeyless.akeyless_gw_system_healthcheck_status`). For the full setup, including Docker/VM Agent configuration, HTTPS endpoints, and a ready-to-import dashboard, see the [Datadog Akeyless Gateway integration](https://github.com/DataDog/integrations-extras/tree/master/akeyless_gateway).

<Callout icon="⚠️" theme="warning">
  ### Packaged dashboard does not work on Gateway 5.x

  The Akeyless Gateway dashboard listed under Datadog Integrations queries the pre-5.0 dotted OTel metric names (`akeyless.gw.system.*`). Gateway 5.x emits underscored names (`akeyless_gw_*`), so that dashboard renders empty. Use Metrics Explorer, or the dashboard JSON linked above, instead.
</Callout>

## Prometheus Configuration

Annotate the Gateway Service with scrape directives and use `rate()` or `increase()` for counter-based metrics. This does not apply to the CPU throttling metrics described above, which are gauges despite their `_total` suffix.
