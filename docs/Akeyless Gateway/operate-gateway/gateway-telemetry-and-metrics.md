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
Akeyless Gateway telemetry metrics can be consumed by well-known monitoring and alerting solutions, such as **Datadog** and **Prometheus&#x20;**&#x66;rom the Gateway URL endpoint  `https://<Your-Gateway-URL:8000/metrics`.&#x20;

You can find a full list of supported exporters on the [OpenTelemetry Collector Contrib exporter page](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/exporter).

<Callout icon="📘" theme="info">
  ### New Telemetry endpoint&#x20;

  Starting from Akeyless Gateway V5 , the legacy metrics solution is deprecated, and now all metrics are available for scraping on new endpoint at `https://<Your-Gateway-URL:8000/metrics` and can be collected using external solutions&#x20;
</Callout>

Telemetry metrics are time-series signals from the Gateway application and runtime environment, used for dashboards, alerting, and trend analysis.

The following metrics are currently available:

| Metric                                           | Description                                                       |
| ------------------------------------------------ | ----------------------------------------------------------------- |
| `akeyless_gw_system_cpu_*`                       | CPU utilization metrics                                           |
| `akeyless_gw_system_disk_*`                      | Disk I/O metrics                                                  |
| `akeyless_gw_system_load_*`                      | CPU load metrics                                                  |
| `akeyless_gw_system_memory_*`                    | Memory utilization metrics                                        |
| `akeyless_gw_system_network_*`                   | Network interface I/O metrics and TCP connection metrics          |
| `akeyless_gw_system_saas_connection_status`      | Monitor Gateway connectivity to Akeyless SaaS services.           |
| `akeyless_gw_quota_current_transactions_number`  | Current total transaction count in the account                    |
| `akeyless_gw_quota_gw_admin_client_transactions` | Total transactions made by the Gateway default identity           |
| `akeyless_gw_quota_total_transactions_limit`     | Total transaction limit per hour in the account                   |
| `akeyless_gw_system_http_response_status_code`   | HTTP response status codes for requests served by the Gateway API |
| `akeyless_gw_system_request_count`               | Total requests issued directly against the Gateway API            |
| `akeyless_gw_system_healthcheck_status`          | Container health check status                                     |

For Gateway API traffic monitoring, use `akeyless_gw_system_request_count` together with `akeyless_gw_system_http_response_status_code`.

`akeyless_gw_system_network_*` covers network interface and TCP connection behavior.

## Health and Connection Status Values

The following metrics are numeric status metrics:

- `akeyless_gw_system_healthcheck_status`
- `akeyless_gw_system_saas_connection_status`

Use the values below when building dashboards and alerts:

- `1` = healthy/connected
- `0` = unhealthy/not connected

### What Each Metric Checks

- `akeyless_gw_system_saas_connection_status`: Checks connectivity from each Gateway pod to Akeyless SaaS backend services.
- `akeyless_gw_system_healthcheck_status`: Checks connectivity from each Gateway pod to the local cache service (Redis/Supersonic cache).

These are per-pod metrics. They are not replica counters.

### Replica Scaling Behavior

When you scale from 2 replicas to 1 replica, a healthy remaining pod still reports `1`.

The removed pod stops exposing metrics, so its time series becomes stale. This behavior does not mean the metric is stuck.

For replica-count alerts, use Kubernetes metrics such as `kube_deployment_status_replicas_available`.

### HTTP Response Metric Behavior

`akeyless_gw_system_http_response_status_code` is a counter with status-code labels.

Use `rate()` or `increase()` in PromQL for alerting and dashboard calculations, rather than using raw counter values.

## Gateway Application Log Forwarding

To collect Gateway application logs together with metrics, you can simply collect the docker logs

## Docker setup

To enable telemetry metrics on Docker set the environment variable  `ENABLE_METRICS=true`  as part of your docker command:&#x20;

```shell
docker run -d -p 8000:8000 -p 5696:5696 \
  -e GATEWAY_ACCESS_ID="Access-id" \
  -e GATEWAY_ACCESS_KEY="Access-key" \
  -e ENABLE_METRICS="true" \
  --name akeyless-gateway akeyless/base:latest-akeyless
```

### Dashboard Setup

Akeyless is an official Datadog Partner and the dashboard is available in Datadog Integrations.

- In Datadog, go to **Integrations** and install **Akeyless Gateway**.
- Go to **Dashboards** and open the **Akeyless GW** dashboard.
- Use **Metrics Explorer** and filter by `akeyless_gw` for additional metrics.

### Grafana Dashboard

You can visualize Akeyless metrics in Grafana when using Prometheus as a data source.

Import the Akeyless GW dashboard using [Grafana dashboard 16927](https://grafana.com/grafana/dashboards/16927).

![A sample screenshot of a Grafana dashboard showing metrics and charts.](https://files.readme.io/fd9e82c-Screen_Shot_2022-07-31_at_10.44.18.png)

## Kubernetes setup

On Kubernetes, set the `globalConfig.metrics.enabled` with `true` :

```yaml values.yaml
globalConfig:
  metrics:
    enabled: true
```

## Prometheus (Kubernetes)

Annotate the Gateway Service so Prometheus can scrape port `8000`:

```yaml values.yaml
gateway:
  service:
    annotations:
      prometheus.io/scrape: "true"
      prometheus.io/port: "8000"
      prometheus.io/scheme: "http"

globalConfig:
  metrics:
    enabled: true

```

## Metric Tag Configuration

You can add tags to metrics using OpenTelemetry semantic conventions. For mapping details, see [Datadog OpenTelemetry semantic mapping](https://docs.datadoghq.com/opentelemetry/mapping/semantic_mapping/?tab=datadogexporter#metrics-attribute-mapping).

## Related Pages

- [Gateway Log Forwarding](https://docs.akeyless.io/docs/gateway-log-forwarding)
- [Troubleshooting the Gateway](https://docs.akeyless.io/docs/gateway-troubleshooting-the-gateway)
- [Gateway Network Connectivity](https://docs.akeyless.io/docs/gateway-network-connectivity)

<br />
