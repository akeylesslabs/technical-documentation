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
Runtime caching controls how Gateway serves secrets from cache during request execution.

## Read Path Behavior

When cache is enabled, secret retrieval follows this behavior:

1. If a valid cached value is found, Gateway returns it immediately.
2. In parallel, Gateway can refresh from SaaS in the background.
3. If no cached value exists, Gateway reads from SaaS and stores the result in cache.

### ignore-cache Behavior

The `ignore-cache` flag is intended to bypass cache and fetch directly from SaaS.

```shell
akeyless get-secret-value -n /mysecret --ignore-cache true
```

In disconnected mode (SaaS unreachable), runtime code still uses cache first even when `ignore-cache=true`. If the value is not cached, the request fails.

## Write and Update Behavior

Gateway write operations are SaaS-first. Cache is not updated through a synchronous write-through path.

Current implementation pattern:

1. Write or update request is sent to SaaS.
2. Matching cached item is invalidated (removed) by update, delete, and rotate flows.
3. Cache converges on the next read-through fetch or proactive synchronization cycle.

This means stale reads can exist temporarily between a successful write and the next cache refresh.

## Local Cache and Cluster Cache Read Preference

When cluster cache is enabled, read preference is controlled by `PREFER_CLUSTER_CACHE_FIRST`:

* `false` (default): Prefer local in-memory cache, then Redis.
* `true`: Prefer Redis, then local in-memory cache.

In default mode, Gateway also compares local and Redis `lastModified` metadata and refreshes local entries when Redis is newer.

For proactive cache warm-up and rate-limit behavior, see [Proactive Caching](https://docs.akeyless.io/docs/proactive-caching).
For Redis deployment topology, see [Cluster Cache (Standalone)](https://docs.akeyless.io/docs/cluster-cache-standalone) and [Cluster Cache HA](https://docs.akeyless.io/docs/cluster-cache-ha).
