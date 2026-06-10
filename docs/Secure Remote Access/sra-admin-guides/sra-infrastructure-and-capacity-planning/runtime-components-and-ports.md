---
title: Runtime Components and Ports
slug: sra-runtime-components-and-ports
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
Use this page to verify runtime component boundaries, required network paths, and control-plane wiring for Secure Remote Access (SRA).

## Port Inventory

For the canonical baseline inventory, also see [SRA Requirements](https://docs.akeyless.io/docs/sra-requirements#port-inventory).

| Component | Port(s) | Purpose | Exposure |
| --- | --- | --- | --- |
| Gateway | `8000` | External API and SRA portal and web paths | User-facing |
| Gateway | `8080` | Internal API and health endpoint | Internal |
| Gateway | `8889` | Metrics endpoint when metrics are enabled | Internal/monitoring |
| SRA SSH bastion | `22` (Kubernetes), `2222` (Docker host mapping) | SSH data-plane sessions | User-facing |
| SRA SSH bastion | `9900` | SSH bastion control-plane API | Internal |
| SRA web bastion | `8888` | Web bastion service endpoint | Internal |
| ZTWA dispatcher | `9000` | Main web-session entrypoint | User-facing |
| ZTWA dispatcher | `19414` | Web proxy mode entrypoint | User-facing |
| ZTWA web-worker | `5800` | Worker service endpoint used by dispatcher | Internal |
| Redis/cache | `6379` | Session and cache backend | Internal |

## Component Dependency Graph

The following flow summarizes the most common runtime dependency direction.

```mermaid
flowchart LR
  User[User or CLI Client] --> GW8000[Gateway :8000]
  User --> SSH22[SRA SSH Bastion :22]
  User --> DISP9000[Dispatcher :9000]
  User --> DISP19414[Dispatcher :19414]

  GW8000 --> WEB8888[SRA Web Bastion :8888]
  GW8000 --> SSH9900[SRA SSH Bastion Control :9900]
  WEB8888 --> GW8080[Gateway Internal API :8080]
  SSH9900 --> GW8080

  GW8000 --> REDIS6379[Redis :6379]
  WEB8888 --> REDIS6379
  SSH9900 --> REDIS6379
  DISP9000 --> WORKER5800[ZTWA Web Worker :5800]
  DISP19414 --> WORKER5800
```

## Internal Service Wiring

In containerized deployments, the following runtime variables commonly define service discovery:

* `REMOTE_ACCESS_WEB_SERVICE_INTERNAL_URL` for gateway to web bastion control path (for example `http://akeyless-sra-web:8888`).
* `REMOTE_ACCESS_SSH_SERVICE_INTERNAL_URL` for gateway to SSH bastion control path (for example `http://akeyless-sra-ssh:9900`).
* `INTERNAL_GATEWAY_API` for bastion components to gateway health/internal API (`8080`).
* `REDIS_ADDR` for cache and session backend (`6379`).

## Deployment Boundary Patterns

Use one of these topologies based on security and scale requirements:

1. Same cluster, single namespace: fastest to deploy and troubleshoot.
2. Same cluster, dedicated namespace for SRA components: improves policy isolation while keeping low latency.
3. Separate clusters for gateway and SRA bastions/dispatcher: useful for large organizations and blast-radius reduction; requires explicit networking and DNS reachability between clusters.

For Kubernetes deployments, expose the SSH bastion service according to [SRA setup on Kubernetes](https://docs.akeyless.io/docs/sra-setup-k8s) and keep internal control-plane ports non-public whenever possible.

## Namespace Isolation Guidance

For Kubernetes production deployments:

* Deploy SRA-related workloads into a dedicated namespace per environment.
* Apply namespace-scoped network policies so only required east-west paths are allowed.
* Keep Redis and control-plane endpoints (`8080`, `8888`, `9900`, `5800`) cluster-internal.
* Restrict user-facing exposure to only the required entrypoints (`8000`, `22`, `9000`, `19414`) based on enabled features.
