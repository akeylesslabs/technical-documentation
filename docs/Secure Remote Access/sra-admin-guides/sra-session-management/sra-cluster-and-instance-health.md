---
title: Cluster and Instance Health
slug: sra-cluster-and-instance-health
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
Use this page to monitor Secure Remote Access (SRA) cluster availability, bastion instance state, and telemetry signals that indicate degraded runtime behavior.

## Runtime Health Signals

Use these health signals together:

* Gateway internal health endpoint on port `8080`.
* Gateway metrics endpoint on port `8889` when metrics are enabled.
* Bastion and dispatcher container or pod liveness and readiness state.
* Bastion fleet inventory by way of `list-sra-bastions`.

For deployment-level port context, see [SRA Requirements](https://docs.akeyless.io/docs/sra-requirements).

## Bastion Fleet Inventory

Use `list-sra-bastions` to inspect registered bastion clusters and instance-level details.

```shell
akeyless list-sra-bastions
```

To focus on URL hardening configuration only:

```shell
akeyless list-sra-bastions --allowed-urls-only true
```

For API details, see [List SRA Bastions](https://docs.akeyless.io/reference/listsrabastions).

## Health Signals to Monitor

Recommended operational signals include:

* Bastion instance heartbeat recency (`last_report`-style freshness).
* Instance version consistency inside a cluster.
* Connectivity state and total active sessions per cluster.
* Gateway health endpoint availability.
* Metrics scrape success for gateway and observability stack targets.

In Console fleet views, health state can be derived from last-report consistency and instance-level data.

## Console Warning States and Cluster Metadata

In Console SRA cluster views, warning or degraded state can be raised when cluster instances are inconsistent.

Common warning conditions include:

* Mixed instance versions within the same cluster.
* Inconsistent allowed access ID sets across cluster instances.
* Inconsistent Akeyless URL values across cluster instances.

If no instance report is received within the expected recency window, the cluster can appear inactive.

SRA cluster metadata also includes a cluster display name field, which can be updated from Console and used for operator-friendly fleet identification.

## Prometheus Scrape Targets

In Docker Compose deployments with metrics profile enabled, scrape targets typically include:

* Gateway metrics endpoint (`8889`).
* Prometheus and Grafana service targets used by your observability stack.

In Kubernetes deployments, configure equivalent scrape targets through your cluster monitoring stack.

## Recommended Alerts

Start with alerts for:

1. Bastion disconnect or stale last report window.
2. Gateway health endpoint failure.
3. Sustained session queue depth growth (or equivalent pending-session backlog metric in your monitoring stack).
4. Rapid increase in failed or terminated session states.

Tune thresholds by environment size and normal traffic patterns.
