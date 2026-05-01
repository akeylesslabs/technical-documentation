---
title: Requirements
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

Port values below are default values from the official Helm charts and Docker Compose examples.

## Port Inventory

The following table lists the primary ports by component.

| Component | Port(s) | Purpose |
| --- | --- | --- |
| Gateway | `8000` | External API and SRA portal/web paths |
| Gateway | `8080` | Internal API and health endpoint |
| Gateway | `8889` | Metrics endpoint when metrics are enabled and exposed |
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

## Minimum Resources

Use at least 1 vCPU and 2 GiB memory for each SRA component.

## Kubernetes-Specific Requirements

* Expose the SSH bastion service with `type: LoadBalancer`.
* Run the SSH bastion container in privileged mode.

## Docker Compose Profiles

Use Docker Compose profiles as follows:

* `gateway`
* `sra`
* `metrics`
