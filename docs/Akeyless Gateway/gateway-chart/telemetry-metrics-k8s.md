---
title: Telemetry Metrics on Kubernetes
excerpt: For Kubernetes Environments
deprecated: false
hidden: false
metadata:
  title: ''
  description: ''
  robots: index
next:
  description: ''
---
Akeyless Gateway Telemetry Metrics can be consumed by well-known monitoring and alerting solutions, such as **Datadog** or **Prometheus**. You can find a full list of supported endpoints on the official page of the Open Telemetry [project](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/exporter).

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
| `akeyless.gw.quota.gw_admin_client_transactions` | Total transactions made by the Gateway default identity (`AdminAccessID`)                                          |
| `akeyless.gw.quota.total_transactions_limit`     | Total transaction limit per hour in the account                                                                    |
| `akeyless.gw.system.http_response_status_code`   | Status of HTTP response for any request that originates from the Gateway API. (i.e. performed against the Gateway) |
| `akeyless.gw.system.request_count`               | Total number of requests that were issued directly against the Gateway API (the count of total HTTP status)        |
| `akeyless.gw.system.healthcheck.status`          | Monitors container health check status                                                                             |

# Datadog

To enable Telemetry Metrics on your Gateway for Datadog, edit the chart `values.yaml ` file under the `metrics` section and set your metrics backend configuration:

```yaml Datadog
metrics:
  enabled: true  
  config: |
    exporters:    
      datadog:
        api:
          key: "<Your Datadog API key>"
          site: <Your Datadog server site>
    service:
      pipelines:
        metrics:
          exporters: [datadog]
```

Set the relevant `API Key` of your **Datadog** server, and set the relevant site. If your Datadog server is running in the `EU` site, add `site:datadoghq.eu`. By default it is set to the `US` site. If you did this before deploying your Gateway, go to Dashboard Setup. If you are adding this to a running Gateway, update your Gateway once done and continue to Dashboard Setup.

**Dashboard Setup:**

Akeyless is an official Datadog Partner and our dashboard can be found inside the Datadog app.

* Go directly to your Datadog account and click on **Integrations** --> **Integrations**. Then choose **Akeyless Gateway** from the list of Integrations and click the **Install Integration** button.

* Once installed, go to **Dashboards** --> **Dashboard List** and choose the **Akeyless GW** Dashboard that was installed.

* If your Gateway metrics are up and running properly, you will see your Gateway metrics in the **Akeyless GW** dashboard. You can also go to the **Metrics Explorer** to see more metrics to add to the Dashboard by filtering for "akeyless.gw".

# Prometheus

To enable Telemetry Metrics on your Gateway for Prometheus, edit the chart `values.yaml ` file under the `metrics` section and set your metrics backend configuration: 

expose the port `8889` (or any other port) for **Prometheus Exporter** and the **Prometheus Scraping** as described below:

```yaml Prometheus Exporter
service:
  annotations:
    prometheus.io/scrape: "true"
    prometheus.io/port: "8889"


metrics:
  enabled: true  
  config: |
    exporters:
      prometheus:
        endpoint: "0.0.0.0:8889"
    service:
      pipelines:
        metrics:
          exporters: [prometheus]
```

Add a scraping target for the Akeyless Gateway in your **Prometheus** config file and restart your Prometheus server.

```yaml Prometheus Scraping
scrape_configs:
  - job_name: 'akeyless'
    scrape_interval: 10s
    static_configs:
      - targets: ['localhost:8889'] 
```

Once done, check your Prometheus server for the ingested metrics. 

**Grafana Dashboard**

You can visualize Akeyless metrics in Grafana Dashboard when using Prometheus as a data source.

Import the Akeykess GW dashboard for your Grafana instance using [this](https://grafana.com/grafana/dashboards/16927) link.

![](https://files.readme.io/3e6e609-Screen_Shot_2022-07-31_at_10.44.18.png "Screen Shot 2022-07-31 at 10.44.18.png")

# Using K8s Secret

Create a K8s secret with the relevant settings of your target metric server and save it to a file `config-secret.yaml`:

```yaml Datadog
exporters:
  datadog:
    api:
      key: <api-key>      
service:
  pipelines:
    metrics:
      exporters: [datadog]
```
```yaml Prometheus
exporters:
  prometheus:
    endpoint: "0.0.0.0:8889"
service:
  pipelines:
    metrics:
      exporters: [prometheus]
```

Encode the file to `base64`:

```shell
base64 --input=config-secret.yaml
```

Create a K8s secret using the encoded value and place it in the `data.otel-config.yaml` section:

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: gw-metrics-secret
  namespace: <your-namespace>
type: Opaque
data:
  otel-config.yaml: <Base64 K8s Secret value>
```

Deploy the secret on your `k8s` cluster, and make sure to deploy the secret to the correct namespace:

```shell
kubectl apply -f secret.yaml -n <your-namespace>
```

Set your `k8s` secret name on the `metrics.existingSecretName` field in the Gateway chart `values.yaml` file:

```yaml
metrics:
  enabled: true
  existingSecretName: "gw-metrics-secret"
```

# Gateway Application Log Forwarding

To collect the Gateway application logs with the metrics you can set an additional `exporter` endpoint and  `service`, for example:

Edit the Gateway  `values.yaml` file as described below:

```yaml values.yaml
metrics:
  enabled: true
  config: |
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
env:
  - name: FORWARD_GW_APP_LOG
    value: "true"
```

Where the new **Loki**  `endpoint`  is set with a new `service` for logs, using `filelog` as the `reciver` and `loki` as the `exporter`.

To add the Gateway Cluster unique identifier to your logs set the `FORWARD_GW_APP_LOG="true"` environment variable. 

**Application Logs** from all instances of this gateway will be forwarded in this format: `<date> <time> <gw-clustername-instance-id> <log>`.

After starting the Docker container, you can utilize [Loki Grafana](https://grafana.com/docs/loki/latest/) to query logs effectively. Follow these steps:

* In **Grafana**, navigate to Data Sources and add a new [Loki Data Source](https://grafana.com/docs/grafana/latest/datasources/loki/configure-loki-data-source/)

* Once the data source is configured, go to the **Explore** section

* In the **Label Filter**, select **Exporter** and [OTLP](https://opentelemetry.io/docs/specs/otel/protocol/exporter/) to filter the logs accordingly

This will enable you to monitor and analyze your application logs seamlessly.

alternatively, you can store a K8s secret to store the relevant `otel-config.yaml` as described in the [Using K8s Secret](https://docs.akeyless.io/docs/telemetry-metrics-k8s#using-k8s-secret).