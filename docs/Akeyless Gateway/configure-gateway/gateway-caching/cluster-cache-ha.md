---
title: Cluster Cache HA
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
Cluster Cache HA (`cacheHA`) uses a Redis Sentinel topology for high-availability cache service.

## When to Use

Use Cluster Cache HA when:

* You need cache availability during single-pod or single-node failures.
* You run multi-pod Gateway workloads that require resilient shared cache service.
* Your platform requirements justify Sentinel operational overhead.

## When Not to Use

Do not use Cluster Cache HA when:

* You run a simple or low-scale environment where standalone Redis is sufficient.
* You want the smallest operational footprint for cache infrastructure.

## Core Configuration Areas

Common configuration areas include:

* `cacheHA.enabled`
* `cacheHA.auth`, `cacheHA.authKey`, `cacheHA.existingSecret`
* `cacheHA.persistentVolume.*`
* `cacheHA.hardAntiAffinity`
* `cacheHA.topologySpreadConstraints.*`

For production, set anti-affinity and storage classes according to your cluster design.

For complete values and examples, see [Helm Values Reference](https://docs.akeyless.io/docs/gateway-kubernetes-helm-values-reference).
