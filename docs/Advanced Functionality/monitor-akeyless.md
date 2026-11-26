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

This guide outlines the monitoring features offered by Akeyless, including [Telemetry metrics](https://docs.akeyless.io/docs/gateway-telemetry-and-metrics), [Audit Logs](https://docs.akeyless.io/docs/audit-logs), [Log Forwarding](https://docs.akeyless.io/docs/gateway-log-forwarding), [Analytics](https://docs.akeyless.io/docs/analytics), and [Event Monitoring](https://docs.akeyless.io/docs/event-center).

## Audit Logs

Audit logging is important for security and compliance. Akeyless generates detailed, unchangeable logs for all operations, including API calls and administrative actions. Key features include:

**Detailed Tracking**: Record who performed what action, when, and from where.

**Unchangeable Records**: Ensure logs cannot be altered to meet compliance needs.

**Regulatory Compliance**: Align with standards such as **GDPR**, **HIPAA**, and **ISO 27001**.

Audit Logs can be exported to external platforms for further analysis and long-term storage, serving as valuable resources for investigations and audits.

### Log Forwarding

Akeyless supports centralized log management by allowing Audit Logs to be forwarded from the Akeyless Gateway. Logs can be streamed or exported to external platforms for detailed analysis and monitoring.

A full list of the log servers to which logs can be forwarded can be found in this [guide](https://docs.akeyless.io/docs/gateway-log-forwarding).

Setting the [Gateway](https://docs.akeyless.io/docs/gateway-overview) to forward the **Audit Logs** can be configured either during deployment or after the Gateway is deployed.

> ℹ️ **Authorized Users:**
>
> Only users with access permission on the gateway to manage log forwarding will authorize to set log forwards.

## Metrics

Akeyless provides detailed telemetry metrics to offer insights into the health and performance of Akeyless components. These metrics help you track and optimize key areas, such as:

* **Request Rates**: Monitor the volume of requests handled by the Akeyless Gateway.
* **HTTP Response Status Trends**: Track API response status patterns to detect service issues.
* **Resource Utilization**: Monitor CPU, memory, and other system resources.
* **Network Activity**: Monitor interface I/O and TCP connection metrics.

Telemetry metrics work with leading monitoring tools, including **Prometheus**, **Grafana**, and **Datadog**. By exporting metrics to these systems, you can set up dashboards and alerts to support active monitoring and quick responses. In addition to those metrics, you can also forward the Gateway application logs as well.

Refer to the [Telemetry Metrics](https://docs.akeyless.io/docs/gateway-telemetry-and-metrics) official docs for the Gateway full metrics list and to the [Kubernetes Secrets Injector](https://docs.akeyless.io/docs/akeyless-kubernetes-secrets-injector) official doc for Kubernetes Injector metrics.

## Event Center

The Akeyless Event Center provides a centralized view of system events, ensuring operational transparency and enabling quick responses to important activities. Key features include:

**Critical Event Monitoring**: Track events such as key creation, deletion, and access.

**Notifications and Alerts**: Set up alerts for specific events to ensure timely responses.

**Real-Time Tracking**: Keep visibility into ongoing system activities.

**Event Subscriptions**: You can set up event subscriptions to receive notifications by way of email, webhooks, or third-party platforms, ensuring you're always informed about important activities.

Refer to the [Event Center](https://docs.akeyless.io/docs/event-center) official doc for the full events list.

## Analytics

Akeyless provides built-in analytics to deliver clear insights into operational trends, helping you improve performance and reduce risks. With analytics, you can:

**Understand Usage Patterns**: Analyze how Akeyless is being used within your organization.

**Gain Security Insights**: Spot unusual behavior and potential security risks.

**Find Improvement Opportunities**: Identify areas to boost performance and resource use.

**Interactive Dashboards**: Use pre-configured dashboards to monitor metrics such as API usage, secret access patterns, and key management activities in real time, enabling data-driven decisions.

Information about your **Items** and **Certificates** can be found in the [Analytics](https://docs.akeyless.io/docs/analytics) official doc.

## Gateway Status

Each **Gateway** cluster exposes a `/status` endpoint that provides basic runtime information. This endpoint is useful for verifying that the Gateway is operational. It returns the current **Gateway** version and a hashed identifier for the cluster.

## Gateway Health

The Gateway exposes several /health endpoints. They are not equivalent: some report SaaS connectivity, and others report process/cache readiness.

**Configuration / SaaS connectivity — :8000/health**

Use this endpoint to assess the Gateway’s connectivity to Akeyless SaaS.

Connected: HTTP 200 with Health Check Ok
Disconnected or offline (no SaaS connectivity): HTTP 503 with Health Check Error
This endpoint does not depend on Cluster Cache availability.

**API process health — :8080/health and :8081/health**

These endpoints report whether the Gateway API listeners are up.

* `:8080/health` — API v1 listener
* `:8081/health` — API v2 listener

They do not check SaaS connectivity, so they can return 200 while the Gateway is offline or disconnected from SaaS.

If Cluster Cache is enabled and Redis is unavailable, these endpoints return 503 status code with `Health Check Error`. 
To keep them healthy when Redis should not affect process readiness, set:

,,,yaml Gateway chart
env:
  - name: IGNORE_REDIS_HEALTH
    value: "true"
,,,

If Cluster Cache is not enabled, Redis health is not evaluated.

**Proxied API health — `/api/v1/health` and `/api/v2/health`**

On the configuration port (:8000), these paths are reverse-proxied to the API listeners:

* `http://<gateway>:8000/api/v1/health` → `:8080/health`
* `http://<gateway>:8000/api/v2/health` → `:8081/health`

Behavior matches the corresponding :8080 / :8081 endpoints above (including Cluster Cache / IGNORE_REDIS_HEALTH).

I checked the live page. The best fit is a new subsection at the end of **Gateway Health**, after **Kubernetes probes**. The extended check changes how the Gateway decides it is offline. It does not change any `/health` endpoint on that page. Placing it under the `:8000/health` subsection would imply it does.

---

**Kubernetes probes**

The Kubernetes [ReadinessProbe](https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/) monitors the `api/v1/health` endpoint to keep the deployment up and running while working in offline mode.

**Extended Connectivity Check**

By default, the Gateway checks only the UAM `/health` endpoint to decide whether it is connected to Akeyless SaaS. Set `EXTENDED_HEALTH_CHECK` to `true` to also check Auth and Gator.

Gateway chart env:

```yaml
- name: EXTENDED_HEALTH_CHECK
  value: "true"
```

**Default:** Disabled.

**Behavior when enabled:**

1. The Gateway sends `GET /health` to UAM, Auth, and Gator. It also checks the read-only (`-ro`) variant of each, if one exists.
2. Each check must return HTTP `200`. Any other status or a network error fails the check.
3. An empty UAM URL fails the check. An empty Auth or Gator URL is skipped.
4. The read-only variant is not checked for `localhost`, IP addresses, or hosts that already contain `-ro`.
5. If any check fails, the Gateway enters offline (disconnected) mode. It returns to connected mode when all checks pass again.

**Scope:** This setting only affects the Gateway's offline/connected state. It does not change the responses of the `/health` endpoints described above, including the Kubernetes readiness probe.

**Notes:**

- The Gateway reads this variable at startup. Restart the Gateway after you change it.
- Individual endpoint failures are logged as warnings. The Gateway logs a single error when it loses connectivity.
- With this option enabled, a failure in Auth, Gator, or their read-only endpoints can switch the Gateway to offline mode even when UAM is healthy.
