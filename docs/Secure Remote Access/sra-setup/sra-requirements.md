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

For deeper planning guidance, use Infrastructure and Capacity Planning:

* [Runtime Components and Ports](https://docs.akeyless.io/docs/sra-runtime-components-and-ports)
* [Scaling and HPA Patterns](https://docs.akeyless.io/docs/sra-scaling-and-hpa-patterns)
* [Storage and Recording Capacity](https://docs.akeyless.io/docs/sra-storage-and-recording-capacity)

## Requirements Checklist

Validate the following requirements before rollout.

| Requirement | Applies to | Why it matters |
| --- | --- | --- |
| [Redis cache available](#redis-dependency) | SRA-enabled deployments | SRA components depend on cache and session support. |
| [Minimum resources per SRA component: 1 vCPU, 2 GiB memory](#minimum-resources) | Kubernetes and Docker deployments | Prevents insufficient sizing of SRA services. |
| [SSH bastion exposure by type LoadBalancer and privileged mode](#kubernetes-specific-requirements) | Kubernetes deployments | Required for SRA network and runtime behavior. |
| [Cloud identity override configured when metadata service is not reachable](#kubernetes-specific-requirements) | Metadata-restricted Kubernetes clusters | Prevents cloud detection failures in IAM-based authentication flows. |
| [Gateway and ingress trust chain configured for private and self-signed CAs](#gateway-certificate-trust-requirements) | Private PKI deployments | Prevents TLS verification failures between SRA components and Gateway endpoints. |
| [Session affinity (sticky sessions) configured at ingress or load balancer](#session-affinity-and-sticky-sessions) | Ingress and load balancer fronted deployments | Keeps related requests pinned to the same backend. |
| [Session persistence policy mapped for your ingress controller type](#session-affinity-and-sticky-sessions) | Non-NGINX ingress controllers | Prevents silent affinity misconfiguration when NGINX-only annotations are ignored. |
| [Idle and response timeouts aligned with session duration](#session-timeout-and-ttl-alignment) | Long-lived SSH, RDP, and web sessions | Prevents early session termination by network intermediaries. |
| [Redirect and query size limits validated for SAML and proxy redirects](#saml-and-redirect-size-limits) | SRA behind identity-aware proxies | Prevents login failures caused by oversized redirect URLs. |
| [Allowed bastion and proxy redirect URLs configured](#redirect-url-allowlist-requirements) | ZTWA and portal-based access | Prevents endpoint mismatch and dropped client endpoints. |
| [Access permissions validated by connection mode (direct and proxy)](#access-permissions-by-connection-mode) | ZTWA and SRA access policy design | Prevents mode-specific authorization failures. |
| [Session-recording upload auth tested with dispatcher auth method](#session-recording-authentication-compatibility) | ZTWA recording to object storage | Reduces risk of post-session authentication or upload failures. |

## Core Infrastructure Requirements

### Outbound Connectivity

Allow outbound connectivity to the following destinations:

* [Akeyless API endpoint](https://docs.akeyless.io/docs/gateway-network-connectivity)
* Session forwarding target endpoints, when session forwarding is configured
* Recording storage endpoints (for example, S3 or Azure Blob), when RDP recording is configured

### Redis Dependency

Redis cache support is required for SRA components. For Gateway-only deployments without SRA, cache is optional.

For Redis defaults and operational guidance, see [Redis documentation](https://redis.io/docs/latest/).

For runtime dependency paths that include Redis, see [Runtime Components and Ports](https://docs.akeyless.io/docs/sra-runtime-components-and-ports).

### Minimum Resources

Use at least 1 vCPU and 2 GiB memory for each SRA component.

For autoscaling policy and scale-in protection guidance, see [Scaling and HPA Patterns](https://docs.akeyless.io/docs/sra-scaling-and-hpa-patterns).

### Kubernetes-Specific Requirements

* Expose the SSH bastion service with `type: LoadBalancer`.
* Run the SSH bastion container in privileged mode.
* If metadata-service based cloud detection is restricted, explicitly configure the dispatcher cloud identity type in your deployment values (`aws_iam`, `azure_ad`, or `gcp`).

For platform guidance, see [Kubernetes Service type LoadBalancer](https://kubernetes.io/docs/concepts/services-networking/service/#loadbalancer) and [Linux kernel security constraints](https://kubernetes.io/docs/concepts/security/linux-kernel-security-constraints/).

### Gateway Certificate Trust Requirements

If Gateway or ingress endpoints use private or self-signed certificates, make sure SRA components trust that CA chain.

When needed, provide trusted certificate material by configuration so dispatcher and bastion runtime checks can validate TLS connections to Gateway endpoints.

For Gateway TLS configuration context, see [Gateway TLS settings](https://docs.akeyless.io/docs/gateway-tls-settings).

### Docker Compose Profiles

Use Docker Compose profiles as follows:

* `gateway`
* `sra`
* `metrics`

For profile behavior and usage, see [Docker Compose profiles](https://docs.docker.com/compose/how-tos/profiles/).

## Session Routing and Cookie Requirements

Session routing, persistence, and cookie controls keep multi-step SRA and ZTWA traffic pinned to the correct backend and preserve authenticated browser state across ingress, load balancer, and proxy hops.

### Session Affinity and Sticky Sessions

When SRA services are exposed through an ingress or cloud load balancer, use session affinity (sticky sessions) so follow-up requests remain pinned to the same backend.

Sticky sessions are required for database application access flows (for example, MySQL, MSSQL, and MongoDB) when traffic is routed through ingress.

For NGINX ingress, use cookie-based affinity annotations:

```yaml
nginx.ingress.kubernetes.io/affinity: "cookie"
nginx.ingress.kubernetes.io/session-cookie-expires: "172800"
nginx.ingress.kubernetes.io/session-cookie-max-age: "172800"
```

For cloud-provider load balancers, configure the equivalent session-persistence setting in the provider configuration.

If you are not using NGINX ingress, use the equivalent session-persistence policy for your ingress controller. For Envoy Gateway, use a `BackendTrafficPolicy`-based cookie persistence policy instead of NGINX annotations.

For Envoy policy reference, see [Envoy Gateway session persistence](https://gateway.envoyproxy.io/latest/api/extension_types/#sessionpersistence).

For scale-event safeguards that reduce sticky-session disruption, see [Scaling and HPA Patterns](https://docs.akeyless.io/docs/sra-scaling-and-hpa-patterns#scale-in-risk-and-session-protection).

### SAML and Redirect Size Limits

If SRA is published through identity-aware reverse proxies, validate request URI and redirect limits for your proxy tier.

SAML and JWT-heavy redirects can exceed proxy URI limits in some environments and fail before login completes.

When possible, prefer login flows that reduce query-string payload size and avoid static matching assumptions for dynamic SAML redirect parameters.

For Azure App Proxy behavior, see [Microsoft Entra application proxy](https://learn.microsoft.com/en-us/entra/identity/app-proxy/overview-what-is-app-proxy).

### Access Permissions by Connection Mode

Validate RBAC and item permissions separately for each access mode used by your organization.

Direct access and some proxy flows can require item read permissions in addition to SRA allow-access capabilities, depending on mode and product behavior.

### Session Cookies

For ZTWA and web-bastion browser sessions, secure cookies should remain enabled for HTTPS endpoints.

For HTTP-only lab environments, use the deployment-specific setting that disables secure cookies for the dispatcher service only when TLS termination cannot be used in that environment.

For configuration context, see [SRA Web Access Topology](https://docs.akeyless.io/docs/sra-web-access-topology).

## Session Timeout and TTL Alignment

Long SSH, RDP, and web sessions can be cut off early by default load balancer or ingress idle timeouts.

Set idle and response timeout values to at least your intended SRA session TTL (for example, 15 to 60 minutes).

If a custom bastion default session TTL is set, align these network timeout values with that TTL.

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

For autoscaling decisions that should align with these timeout values, see [Scaling and HPA Patterns](https://docs.akeyless.io/docs/sra-scaling-and-hpa-patterns).

## Redirect URL Allowlist Requirements

Configure allowed redirect URLs for bastion and web proxy endpoints as part of SRA and ZTWA deployment.

For Helm-based deployments, set:

* `allowedBastionUrls`
* `allowedProxyUrls`

For Docker-based SSH bastion deployments, configure `ALLOWED_BASTION_URLS`.

These allowlists are consumed by SRA keep-alive and bastion metadata flows. In the Zero Trust Portal client, non-allowed user-provided endpoint URLs are removed from local endpoint state.

## Session Recording Authentication Compatibility

When session recording upload is enabled, validate the dispatcher authentication path and object-storage upload authentication path together.

If you observe post-session authentication failures, test alternative credential-source combinations for dispatcher runtime authentication and storage-upload authentication, and keep the stable combination for production rollout.

For recording volume estimates, retention planning, and backend lifecycle controls, see [Storage and Recording Capacity](https://docs.akeyless.io/docs/sra-storage-and-recording-capacity).

## Port Inventory

The following table lists the primary ports by component.

For component topology and namespace isolation implementation patterns, see [Runtime Components and Ports](https://docs.akeyless.io/docs/sra-runtime-components-and-ports).

| Component | Port(s) | Purpose |
| --- | --- | --- |
| Gateway | `8000` | External API and SRA portal and web paths |
| Gateway (Docker Compose default mapping) | `8080` | Internal API and health endpoint |
| Gateway (Docker Compose default mapping) | `8889` | Metrics endpoint when metrics are enabled and exposed |
| SRA web bastion | `8888` | Web bastion service |
| SRA SSH bastion | `22` (Kubernetes service), `2222` (Docker host mapping), `9900` (control proxy) | SSH data plane and control proxy |
| ZTWA dispatcher | `9000`, `19414` | Dispatcher listener and web proxy mode |
| ZTWA web-worker | `5800` | Isolated browser worker service (internal service) |
| Redis | `6379` | Cache and session support |
