---
title: Runtime Caching
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
Runtime caching controls how the Akeyless Gateway serves and refreshes cached secrets during request handling.

## Read Behavior

When runtime caching is enabled, secret retrieval follows this flow:

1. The request reaches the Gateway and a cache lookup begins.
2. If cluster cache is enabled, lookup order is controlled by `PREFER_CLUSTER_CACHE_FIRST`:
    * `false` (default): local in-memory cache first, then Redis cluster cache.
    * `true`: Redis cluster cache first, then local in-memory cache.
3. If a valid cached value is found, the Gateway returns it immediately to the caller.
4. After a cache hit, the Gateway can refresh from SaaS in the background to keep cache entries current.
5. If no cached value exists, the Gateway reads from SaaS, stores the value in cache, and then returns it to the caller.
6. If SaaS is unreachable and no cached value exists, the request fails.

### ignore-cache Behavior

The `ignore-cache` flag is intended to bypass cache and fetch directly from SaaS.

```shell
akeyless get-secret-value -n /mysecret --ignore-cache true
```

In disconnected mode (when SaaS is unreachable), the runtime still checks cache first even when `ignore-cache=true`. If the value is not cached, the request fails.

## Write and Update Behavior

Gateway write operations are SaaS-first. There is no synchronous write-through update to cache.

Current implementation pattern:

1. A write or update request is sent to SaaS.
2. Matching cached items are invalidated (removed) by update, delete, and rotate flows.
3. Cache converges on the next read-through fetch or proactive synchronization cycle.

As a result, stale reads can occur temporarily between a successful write and the next cache refresh.

## Local Cache and Cluster Cache Read Preference

When cluster cache is enabled, `PREFER_CLUSTER_CACHE_FIRST` controls read preference:

* `false` (default): Prefer local in-memory cache, then Redis.
* `true`: Prefer Redis, then local in-memory cache.

When `PREFER_CLUSTER_CACHE_FIRST=false` (the default local-first mode), the Gateway also compares local and Redis `lastModified` metadata and refreshes local entries when Redis is newer.

For proactive cache warm-up and rate-limit behavior, see [Proactive Caching](https://docs.akeyless.io/docs/proactive-caching).

For Redis deployment topology, see [Cluster Cache (Standalone)](https://docs.akeyless.io/docs/cluster-cache-standalone) and [Cluster Cache High Availability (HA)](https://docs.akeyless.io/docs/cluster-cache-ha).
