---
title: Troubleshooting the Gateway
excerpt: ''
deprecated: false
hidden: false
metadata:
  title: ''
  description: ''
  robots: index
---
Use this page to troubleshoot common deployment and runtime issues for Akeyless Gateway.

## Troubleshooting Workflow

Use this sequence first, before deep component-level debugging:

1. Validate outbound connectivity to Akeyless SaaS services.
2. Validate authentication method and access permissions.
3. Validate TLS, certificate trust, and endpoint settings.
4. Validate cache behavior and runtime health.
5. Validate log forwarding and telemetry output.

## 1. Connectivity and Reachability

When Gateway cannot sync, authenticate, or retrieve data, start with network validation.

Check:

* Outbound HTTPS connectivity (`443`) to required Akeyless SaaS endpoints.
* DNS resolution for required service hostnames.
* Proxy, firewall, and egress control behavior.

Reference:

* [Gateway Network Connectivity](https://docs.akeyless.io/docs/gateway-network-connectivity)

## 2. Authentication and Permissions

Authentication failures are commonly caused by mismatched Access IDs, invalid credentials, or missing permissions.

Check:

* The configured Gateway authentication type matches the deployed environment.
* The configured Access ID and credentials are valid.
* The authentication method has required permissions for intended operations.
* Access permissions for Gateway management users are configured as expected.

Reference:

* [Gateway Authentication](https://docs.akeyless.io/docs/gateway-authentication-and-access)

## 3. TLS and Certificate Trust

TLS misconfiguration usually appears as handshake errors, certificate validation failures, or management endpoint access issues.

Check:

* TLS certificate and key are valid and correctly loaded.
* Certificate chain is complete and trusted by clients.
* Private CA certificates are present in Certificate Store when required.

References:

* [TLS Certificate](https://docs.akeyless.io/docs/gateway-tls-settings)
* [Certificate Store](https://docs.akeyless.io/docs/gateway-certificate-store)

## 4. Cache and Offline Behavior

If stale values are returned, or behavior differs during SaaS interruptions, validate that your selected caching mode and runtime options match your requirements.

Check:

* The selected caching method is configured as intended (runtime, proactive, standalone cluster cache, or HA cluster cache).
* Refresh and synchronization settings align with operational requirements.
* Workload behavior with `ignore-cache` is validated against your outage expectations.

References:

* [Gateway Caching](https://docs.akeyless.io/docs/gateway-caching)

## 5. Logging and Telemetry

When diagnosis data is missing, validate both forwarding targets and collector configuration.

Check:

* Log forwarding destination and credentials are valid.
* Telemetry exporter configuration is loaded and reachable.
* Runtime logs include expected request, auth, and connectivity events.

References:

* [Log Forwarding](https://docs.akeyless.io/docs/gateway-log-forwarding)
* [Telemetry and Metrics](https://docs.akeyless.io/docs/gateway-telemetry-and-metrics)

## Symptom-Based Quick Checks

### Gateway starts, but requests fail

* Validate authentication and permissions first.
* Validate network path to SaaS endpoints.
* Validate Gateway endpoint and TLS settings used by clients.

### Gateway cannot authenticate users or workloads

* Validate authentication method configuration and credentials.
* Validate Access Role permissions and bound conditions.
* Validate identity-provider integration assumptions when SSO is used.

### Gateway returns stale secret values

* Validate cache mode and refresh settings.
* Validate whether disconnected mode is active.
* Validate whether request paths intentionally use cache.

### No logs in SIEM or metrics backend

* Validate destination endpoint, token/key, and network reachability.
* Validate exporter configuration format.
* Validate that the enabled forwarding mode matches the deployment model.

## Deployment-Specific Checks

* Self-managed runtime options: validate environment variables, mounts, container restart history, and (when applicable) self-managed Kubernetes runtime configuration.
* Cloud-managed Kubernetes platforms: validate pod health, service account permissions, secrets, and Helm values.
* Cloud-managed serverless platforms: validate platform identity, runtime environment variables, and provider-level networking.

References:

* [Standalone Docker Deployment](https://docs.akeyless.io/docs/gateway-deploy-standalone-docker)
* [Kubernetes with Helm Deployment](https://docs.akeyless.io/docs/gateway-deploy-kubernetes-helm)
* [Cloud-Managed Serverless Platforms](https://docs.akeyless.io/docs/gateway-cloud-serverless-deployments)

## Before Escalation

Before opening an internal escalation or support ticket, capture:

* Deployment model and Gateway version.
* Exact failing operation and timestamp (UTC).
* Relevant error message and response code.
* Recent configuration changes.
* Sanitized logs from the failing time window.
