---
title: Cluster Cache (Standalone)
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
Standalone cluster cache uses Redis as a shared cache service for Gateway pods.

## When to Use

Use standalone cluster cache when:

* You run multiple Gateway pods and want shared cache state.
* You want lower operational complexity than HA Sentinel.
* A single Redis instance is acceptable for your availability target.

## When Not to Use

Do not use standalone cluster cache when:

* You require Redis high availability across node failures.
* You need Sentinel-managed failover behavior.

## Persistence

In the Helm chart, standalone persistence is controlled by `globalConfig.clusterCache.persistence.enabled`:

* `false` (default): no PVC is mounted at `/data`.
* `true`: a PVC is mounted at `/data` and Redis can persist to disk.

By default, Redis durability flags are not forced in chart templates. You can pass Redis runtime flags through `globalConfig.clusterCache.extraArgs`.

For the full key reference and YAML examples, see [Helm Values Reference](https://docs.akeyless.io/docs/gateway-kubernetes-helm-values-reference).
