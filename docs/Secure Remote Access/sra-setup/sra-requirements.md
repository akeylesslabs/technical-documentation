---
title: SRA Requirements
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
Use this page to validate infrastructure requirements before deploying Akeyless Gateway with Secure Remote Access (SRA) and Zero Trust Web Access (ZTWA).

Port values below are default values from the official Helm charts and Docker Compose examples. Exact exposure can vary by deployment model, ingress, and service configuration.

## Port Inventory

The following table lists the primary ports by component.

| Component | Port(s) | Purpose |
| --- | --- | --- |
| Gateway | `8000` | External API and SRA portal/web paths |
| Gateway (Docker Compose default mapping) | `8080` | Internal API and health endpoint |
| Gateway (Docker Compose default mapping) | `8889` | Metrics endpoint when metrics are enabled and exposed |
| SRA web bastion | `8888` | Web bastion service |
| SRA SSH bastion | `22` (Kubernetes service), `2222` (Docker host mapping), `9900` (control proxy) | SSH data plane and control proxy |
| ZTWA dispatcher | `9000`, `19414` | Dispatcher listener and web proxy mode |
| ZTWA web-worker | `5800` | Isolated browser worker service (internal service) |
| Redis | `6379` | Cache and session support |

## Outbound Connectivity

Allow outbound connectivity to the following destinations:

* [Akeyless API endpoint](https://docs.akeyless.io/docs/gateway-network-connectivity)
* Session forwarding target endpoints, when session forwarding is configured
* Recording storage endpoints (for example, S3 or Azure Blob), when RDP recording is configured

## Redis Dependency

Redis cache support is required for SRA components. For Gateway-only deployments without SRA, cache is optional.

For Redis defaults and operational guidance, see [Redis documentation](https://redis.io/docs/latest/).

## Minimum Resources

Use at least 1 vCPU and 2 GiB memory for each SRA component.

## Kubernetes-Specific Requirements

* Expose the SSH bastion service with `type: LoadBalancer`.
* Run the SSH bastion container in privileged mode.

For platform guidance, see [Kubernetes Service type LoadBalancer](https://kubernetes.io/docs/concepts/services-networking/service/#loadbalancer) and [Linux kernel security constraints](https://kubernetes.io/docs/concepts/security/linux-kernel-security-constraints/).

## Session Affinity and Sticky Sessions

When SRA services are exposed through an ingress or cloud load balancer, use session affinity (sticky sessions) so follow-up requests remain pinned to the same backend.

Sticky sessions are required for database application access flows (for example, MySQL, MSSQL, and MongoDB) when traffic is routed through ingress.

For NGINX ingress, use cookie-based affinity annotations:

```yaml
nginx.ingress.kubernetes.io/affinity: "cookie"
nginx.ingress.kubernetes.io/session-cookie-expires: "172800"
nginx.ingress.kubernetes.io/session-cookie-max-age: "172800"
```

For cloud-provider load balancers, configure the equivalent session-persistence setting in the provider configuration.

## Session Cookies

For ZTWA and web-bastion browser sessions, secure cookies should remain enabled for HTTPS endpoints.

For HTTP-only lab environments, set `DISABLE_SECURE_COOKIE=true` for the dispatcher service. Use this only when TLS termination cannot be used in that environment.

For configuration context, see [SRA Web Access Topology](https://docs.akeyless.io/docs/sra-web-access-topology).

## Load Balancer Timeout Baselines

Long SSH, RDP, and web sessions can be cut off early by default load balancer or ingress idle timeouts. Set idle and response timeout values to at least your intended SRA session TTL (for example, 15 to 60 minutes).

| Platform | Common default timeout | Recommended action |
| --- | --- | --- |
| Google Cloud Load Balancer (GKE) | `30s` backend timeout | Configure BackendConfig or GCPBackendPolicy `spec.timeoutSec` for SRA services. |
| AWS Application Load Balancer (ALB) | `60s` idle timeout | Set `idle_timeout.timeout_seconds` to match expected SRA session duration. |
| AWS Network Load Balancer (NLB) | `350s` TCP idle timeout | Increase timeout as needed and enable TCP keepalives. |
| Azure Load Balancer (L4) | `4m` idle timeout | Increase idle timeout for long-running sessions. |
| Azure Application Gateway (L7) | `4m` TCP idle, `20s` HTTP request timeout | Increase both values to match session and backend response requirements. |
| NGINX ingress | Often around `60s` without traffic | Increase `proxy-read-timeout` and `proxy-send-timeout` annotations. |

Vendor references:

* [Google Cloud backend service timeout](https://docs.cloud.google.com/load-balancing/docs/backend-service#timeout-setting)
* [Google Kubernetes Engine ingress configuration](https://docs.cloud.google.com/kubernetes-engine/docs/how-to/ingress-configuration)
* [AWS Application Load Balancers](https://docs.aws.amazon.com/elasticloadbalancing/latest/application/application-load-balancers.html)
* [AWS Network Load Balancer idle timeout](https://docs.aws.amazon.com/elasticloadbalancing/latest/network/update-idle-timeout.html)
* [Azure Load Balancer TCP idle timeout](https://learn.microsoft.com/en-us/azure/load-balancer/load-balancer-tcp-idle-timeout)
* [Azure Application Gateway FAQ](https://learn.microsoft.com/en-us/azure/application-gateway/application-gateway-faq)
* [NGINX WebSocket proxying](https://nginx.org/en/docs/http/websocket.html)

## Docker Compose Profiles

Use Docker Compose profiles as follows:

* `gateway`
* `sra`
* `metrics`

For profile behavior and usage, see [Docker Compose profiles](https://docs.docker.com/compose/how-tos/profiles/).
