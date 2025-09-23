---
title: Monitor Your Environment
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
In a SaaS environment managing sensitive assets such as credentials, certificates, and encryption keys, effective monitoring is essential. It ensures the system remains secure, reliable, and efficient by providing real-time insights into operational health and helping to solve issues quickly. 

Continuous monitoring also helps meet regulatory standards, supports investigations, and ensures the system can grow smoothly as needed.

This guide outlines the monitoring features offered by Akeyless, including [Telemetry metrics](https://docs.akeyless.io/docs/telemetry-metrics),  [Audit Logs](https://docs.akeyless.io/docs/audit-logs), [Log Forwarding](https://docs.akeyless.io/docs/gw-docker-log-forwarding) , [Analytics](https://docs.akeyless.io/docs/analytics), and [Event Monitoring](https://docs.akeyless.io/docs/event-center).

# Audit Logs

Audit logging is important for security and compliance. Akeyless generates detailed, unchangeable logs for all operations, including API calls and administrative actions. Key features include:

**Detailed Tracking**: Record who performed what action, when, and from where.

**Unchangeable Records**: Ensure logs cannot be altered to meet compliance needs.

**Regulatory Compliance**: Align with standards such as **GDPR**, **HIPAA**, and **ISO 27001**.

Audit logs can be exported to external platforms for further analysis and long-term storage, serving as valuable resources for investigations and audits.

## Log Forwarding

Akeyless supports centralized log management by allowing audit logs to be forwarded from the Akeyless Gateway. Logs can be streamed or exported to external platforms for detailed analysis and monitoring.

A full list of the log servers to which logs can be forwarded can be found in this [guide](https://docs.akeyless.io/docs/gw-docker-log-forwarding).

Setting the [Gateway](https://docs.akeyless.io/docs/api-gw) to forward the **Audit Logs** can be configured either during deployment or after the Gateway is deployed.

> 📘 Authorized Users
> 
> Only users with access permission on the gateway to manage log forwarding will authorize to set log forwards.

# Metrics

Akeyless provides detailed telemetry metrics to offer insights into the health and performance of Akeyless components. These metrics help you track and optimize key areas, such as:

- **Request Rates**: Monitor the volume of requests handled by the Akeyless Gateway.
- **Latency**: Measure response times to ensure performance goals are met.
- **Error Rates**: Identify and fix issues by tracking errors.
- **Resource Utilization**: Monitor CPU, memory, and other system resources.

Telemetry metrics work with leading monitoring tools, including **Prometheus**, **Grafana**, and **DataDog**. By exporting metrics to these systems, you can set up dashboards and alerts to support active monitoring and quick responses. In addition to those metrics, you can also forward the Gateway application logs as well.

Refer to the [Telemetry Metrics ](https://docs.akeyless.io/docs/telemetry-metrics) official docs for the Gateway full metrics list and to the [K8s Secrets Injector](https://docs.akeyless.io/docs/how-to-provision-secret-to-your-k8s) official doc for k8s Injector metrics.

# Event Center

The Akeyless Event Center provides a centralized view of system events, ensuring operational transparency and enabling quick responses to important activities. Key features include:

**Critical Event Monitoring**: Track events such as key creation, deletion, and access.

**Notifications and Alerts**: Set up alerts for specific events to ensure timely responses.

**Real-Time Tracking**: Keep visibility into ongoing system activities.

**Event Subscriptions**: You can set up event subscriptions to receive notifications via email, webhooks, or third-party platforms, ensuring you're always informed about important activities.

Refer to the [Event Center](https://docs.akeyless.io/docs/event-center)  official doc for the full events list.

# Analytics

Akeyless provides built-in analytics to deliver clear insights into operational trends, helping you improve performance and reduce risks. With analytics, you can:

**Understand Usage Patterns**: Analyze how Akeyless is being used within your organization.

**Gain Security Insights**: Spot unusual behavior and potential security risks.

**Find Improvement Opportunities**: Identify areas to boost performance and resource use.

**Interactive Dashboards**: Use pre-configured dashboards to monitor metrics such as API usage, secret access patterns, and key management activities in real time, enabling data-driven decisions.

Information about your **Items** and **Certificates** can be found in the [Analytics](https://docs.akeyless.io/docs/analytics)  official doc.

# Gateway Status

Each **Gateway** cluster exposes a `/status` endpoint that provides basic runtime information. This endpoint is useful for verifying that the Gateway is operational. It returns the current **Gateway** version and a hashed identifier for the cluster.

# Gateway Health

To assess the Gateway’s connectivity to Akeyless SaaS core services, you can use the `/health` endpoint. Additionally, when working with [Cluster Cache](https://docs.akeyless.io/docs/advanced-chart-configuration#cache-configuration), this endpoint will also be affected by the cache status.

- If the Gateway is successfully connected, it responds with an HTTP status code `200` and the message: **Health Check Ok**.
- If the connection fails, it returns an HTTP status code `503` with the message: **Health Check Error**
- If Cluster Cache is used, and not available, even when the Gateway is successfully connected, it will return `503` with **Health Check Error** 

To disable the effect of the [Cluster Cache](https://docs.akeyless.io/docs/advanced-chart-configuration#cache-configuration) on the `/health` endpoint you can set the following env variable as part of your Gateway deployment: 

```yaml Gateway chart
env:
  - name: IGNORE_REDIS_HEALTH
    value: "true"
```

Note, the k8s [readiness](https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/) monitors the `api/v1/health` endpoint to keep the deployment up and running while working in offline mode.