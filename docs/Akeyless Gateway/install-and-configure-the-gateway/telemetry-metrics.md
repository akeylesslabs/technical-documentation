---
title: Telemetry Metrics
excerpt: For Docker Environment
deprecated: false
hidden: false
metadata:
  title: ''
  description: ''
  robots: index
next:
  description: ''
---
Akeyless Gateway Telemetry Metrics can be consumed by well-known monitoring and alerting solutions, such as **Datadog** or **Prometheus**.  You can find a full list of supported endpoints on the official page of the Open Telemetry [project](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/exporter).

The Telemetry Metrics are based on time series telemetry data metrics from the application and the runtime environment, storing them in a unique database or index, and analyzing data trends over time.

The metrics visualization uses a pre-made/custom dashboard (Grafana marketplace dashboard, Datadog integration dashboard, etc.).

The following Metrics are currently available:

| Metric                                           | Description                                                                                                        |
| :----------------------------------------------- | :----------------------------------------------------------------------------------------------------------------- |
| `akeyless.gw.system.cpu.*`                       | CPU utilization metrics                                                                                            |
| `akeyless.gw.system.disk.*`                      | Disk I/O metrics                                                                                                   |
| `akeyless.gw.system.load.*`                      | CPU load metrics                                                                                                   |
| `akeyless.gw.system.memory.*`                    | Memory utilization metrics                                                                                         |
| `akeyless.gw.system.network.*`                   | Network interface I/O metrics & TCP connection metrics                                                             |
| `akeyless.gw.system.saas.connection_status`      | Monitor the connection of the Gateway with all Akeyless SaaS services.                                             |
| `akeyless.gw.quota.current_transactions_number`  | The current total transaction count in the account                                                                 |
| `akeyless.gw.quota.gw_admin_client_transactions` | Total transactions made by the Gateway default identity (`ADMIN_ACCESS_ID`)                                        |
| `akeyless.gw.quota.total_transactions_limit`     | Total transaction limit per hour in the account                                                                    |
| `akeyless.gw.system.http_response_status_code`   | Status of HTTP response for any request that originates from the Gateway API. (i.e. performed against the Gateway) |
| `akeyless.gw.system.request_count`               | Total number of requests that were issued directly against the Gateway API (the count of total HTTP status         |
| `akeyless.gw.system.healthcheck.status`          | Monitors container health check status                                                                             |

In addition to those metrics, you can also [forward](https://docs.akeyless.io/docs/gw-docker-log-forwarding) the Gateway application logs using **OTEL**.

# Datadog

To enable Telemetry Metrics on your Gateway for Datadog, set the `ENABLE_METRICS=true` variable and mount the Telemetry config file, i.e.,`otel-config.yaml` as described below:

```yaml otel-config.yaml
exporters:
  datadog:
    api:
      key: "<Datadog API key>"
      site: datadoghq.eu # optional. default to Datadog US site when missing site
service:
  pipelines:
    metrics:
      exporters: [datadog]
```

Set the relevant `API Key` of your **Datadog** server, and set the relevant site. If your Datadog server is running in the `EU` site, add site:` datadoghq.eu`. By default it is set to the `US` site.

```shell Shell
docker run -d -p 8000:8000 -p 5696:5696 -e ADMIN_ACCESS_ID="Access-id" -e ADMIN_ACCESS_KEY="Access-key" -e ENABLE_METRICS="true" -v $PWD/otel-config.yaml:/akeyless/otel-config.yaml --name akeyless-gateway akeyless/base:latest-akeyless
```

Alternatively, you can use an environment variable `METRICS_CONFIG_BASE64` to provide those settings in base64, for example:  `base64 -w 0 otel-config.yaml`.

**Dashboard Setup:**

Akeyless is an official Datadog Partner and our dashboard can be found inside the Datadog app.

* Go directly to your Datadog account and click on **Integrations** --> **Integrations**. Then choose **Akeyless Gateway** from the list of Integrations and click the **Install Integration** button.

* Once installed, go to **Dashboards** --> **Dashboard List** and choose the **Akeyless GW** Dashboard that was installed.

* If your Gateway metrics are up and running properly, you will see your Gateway metrics in the **Akeyless GW** dashboard. You can also go to the **Metrics Explorer** to see more metrics to add to the Dashboard by filtering for "akeyless.gw".

# Prometheus

To enable Telemetry Metrics on your Gateway for Prometheus, set the `ENABLE_METRICS=true` variable, expose the port `8889` (or any other port) for Prometheus scraping, and mount the Telemetry config file, i.e.,`otel-config.yaml` for the **Prometheus Exporter** as described below:

```yaml Prometheus Exporter
exporters:
  prometheus:
    endpoint: "0.0.0.0:8889"
service:
  pipelines:
    metrics:
      exporters: [prometheus]
```

Add a scraping target for the Akeyless Gateway container in the **Prometheus** config file and restart your Prometheus server.

```yaml Prometheus Scraping
scrape_configs:
  - job_name: 'akeyless'
    scrape_interval: 10s
    static_configs:
    # docker for linux
      - targets: ['localhost:8889'] # for docker on macOS use['host.docker.internal:8889']
```

Run the Gateway installation command:

```shell
docker run -d -p 8000:8000 -p 5696:5696 -p 8889:8889 -e ADMIN_ACCESS_ID="Access-id" -e ADMIN_ACCESS_KEY="Access-key" -e ENABLE_METRICS="true" -v $PWD/otel-config.yaml:/akeyless/otel-config.yaml --name akeyless-gateway akeyless/base:latest-akeyless
```

Once done, check your Prometheus server for the ingested metrics.

**Grafana Dashboard**

You can visualize Akeyless metrics in the Grafana Dashboard when using Prometheus as a data source.

Import the Akeyless GW dashboard for your Grafana instance using [this](https://grafana.com/grafana/dashboards/16927) link.

<Image align="center" alt="A sample screenshot of a Grafana dashboard showing metrics and charts." border={false} src="https://files.readme.io/fd9e82c-Screen_Shot_2022-07-31_at_10.44.18.png" title="Screen Shot 2022-07-31 at 10.44.18.png" />

# Gateway Application Log Forwarding

To collect the Gateway application logs with the metrics you can set an additional `exporter` endpoint and  `service`, for example:

Edit the `otel-config.yaml` file as described below:

```yaml otel-config.yaml
exporters:
  prometheus:
    endpoint: "0.0.0.0:8889"
  loki:
    endpoint: "http://loki:3100/loki/api/v1/push"
    
service:
  pipelines:
    metrics:
      exporters: [prometheus]
      
    logs:
      receivers: [filelog]
      processors: [batch]
      exporters: [loki]
```

Where the new **Loki**  `endpoint`  is set with a new `service` for logs, using `filelog` as the `reciver` and `loki` as the `exporter`.  Note, that this example uses local [Loki](https://grafana.com/docs/loki/latest/setup/install/docker/) on Docker.

To add the Gateway Cluster unique identifier to your logs set the `FORWARD_GW_APP_LOG="true"` environment variable and mount the Telemetry config file:

```shell
docker run -d -p 8000:8000 -p 5696:5696 -p 8889:8889 -e ADMIN_ACCESS_ID="Access-id" -e ADMIN_ACCESS_KEY="Access-key" -e ENABLE_METRICS="true" -e FORWARD_GW_APP_LOG="true"  -v $PWD/otel-config.yaml:/akeyless/otel-config.yaml --name akeyless-gateway akeyless/base:latest-akeyless
```

**Application Logs** from all instances of this gateway will be forwarded using this format: `<date> <time> <gw-clustername-instance-id> <log>`.

After starting the container, you can utilize [Loki Grafana](https://grafana.com/docs/loki/latest/) to query logs effectively. Follow these steps:

* In Grafana, navigate to Data Sources and add a new [Loki Data Source](https://grafana.com/docs/grafana/latest/datasources/loki/configure-loki-data-source/)

* Once the data source is configured, go to the Explore section

* In the Label Filter, select **Exporter** and [OTLP](https://opentelemetry.io/docs/specs/otel/protocol/exporter/) to filter the logs accordingly

This will enable you to monitor and analyze your application logs seamlessly.
