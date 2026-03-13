---
title: Gateway Caching
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
Use this page as the source of truth for Gateway cache behavior, including cache modes, proactive synchronization, `ignore-cache`, and Kubernetes cluster cache persistence.

## Cache Terms and Scope

The Gateway cache model has three separate concerns:

1. **Caching**: Enables secret caching for request handling.
2. **Proactive cache**: Runs background synchronization jobs to pre-load and refresh cached secrets.
3. **Cluster cache**: Uses Redis for shared cache across Gateway pods in Kubernetes.

The first two are runtime cache behaviors. The third is deployment topology.

## Deployment Modes

The Gateway supports the following deployment-level cache topologies:

| Topology | What is stored | Survives pod restart | Typical use |
| --- | --- | --- | --- |
| Local in-memory only | Per-pod memory cache | No | Single Gateway or low-complexity deployments |
| Cluster cache (standalone) | Shared Redis cache | Yes, only if persistence is enabled | Multi-pod Gateway deployments |
| Cluster cache HA (`cacheHA`) | Shared Redis Sentinel topology | Yes, with `cacheHA.persistentVolume.enabled` | High-availability cache service |

### Standalone Cluster Cache Persistence

In the Helm chart, standalone cluster cache persistence is controlled by `globalConfig.clusterCache.persistence.enabled`.

* If `false` (default), no PVC is mounted at `/data` for the cache pod.
* If `true`, a PVC is mounted at `/data` and Redis can persist data to disk.

> ℹ️ **Note:**
>
> By default, Redis runtime durability flags are not forced in chart templates. Operators can provide Redis flags by using `globalConfig.clusterCache.extraArgs`.

## Read Path Behavior

When cache is enabled, secret retrieval follows this behavior:

1. If a valid cached value is found, Gateway returns it immediately.
2. In parallel, Gateway can refresh from SaaS in the background.
3. If no cached value exists, Gateway reads from SaaS and stores the result in cache.

### `ignore-cache` Behavior

The `ignore-cache` flag is intended to bypass cache and fetch directly from SaaS.

```shell
akeyless get-secret-value -n /mysecret --ignore-cache true
```

In disconnected mode (SaaS unreachable), runtime code still uses cache first even when `ignore-cache=true`. If the value is not cached, the request fails.

## Write and Update Behavior

Gateway write operations are SaaS-first. Cache is not updated through a synchronous write-through path.

Current implementation pattern:

1. Write or update request is sent to SaaS.
2. Matching cached item is invalidated (removed) by update/delete/rotate flows.
3. Cache converges on the next read-through fetch or proactive synchronization cycle.

This means stale reads can exist temporarily between a successful write and the next cache refresh.

## Proactive Cache Behavior

Proactive cache runs only when both cache and proactive cache are enabled.

Core behavior:

1. **Leadership**: One Gateway pod acquires a leadership lock for proactive work.
2. **Startup full fetch**: The leader performs an initial list-and-load pass.
3. **Modified-secrets fetch**: Runs every `PROACTIVE_CACHE_MINIMUM_FETCHING_TIME` interval.
4. **Full fetch**: Runs every full-fetch interval (`CACHE_TTL`-based in current implementation).
5. **Zombie cleanup**: During full fetch, items missing from current inventory are removed from cache.

If SaaS connectivity is unavailable, proactive jobs stop pulling from SaaS and resume when connectivity returns.

## Local Cache and Cluster Cache Read Preference

When cluster cache is enabled, read preference is controlled by `PREFER_CLUSTER_CACHE_FIRST`:

* `false` (default): Prefer local in-memory cache, then Redis.
* `true`: Prefer Redis, then local in-memory cache.

In default mode, Gateway also compares local and Redis `lastModified` metadata and refreshes local entries when Redis is newer.

## Health Endpoint and Redis Outage

`IGNORE_REDIS_HEALTH` controls whether Redis/cache connectivity affects `/health` status in curl-proxy health handling:

* `false` (default): cache connectivity failures can make `/health` fail.
* `true`: cache connectivity is ignored by the `/health` handler.

## Configuration Keys

| Name | Purpose |
| --- | --- |
| `CACHE_ENABLE` | Enable or disable cache. |
| `PROACTIVE_CACHE_ENABLE` | Enable or disable proactive cache. |
| `NEW_PROACTIVE_CACHE_ENABLE` | Enable the newer proactive cache implementation. |
| `PROACTIVE_CACHE_MINIMUM_FETCHING_TIME` | Interval for modified-secrets proactive fetch. |
| `PROACTIVE_CACHE_DUMP_INTERVAL` | Interval used for cache backup workflows when enabled. |
| `CACHE_TTL` | Cache TTL and full-fetch cadence input in current implementation. |
| `PREFER_CLUSTER_CACHE_FIRST` | Prefer Redis over local cache on read. |
| `CACHE_MAX_ITEMS` | Maximum in-memory proactive cache size (default 50,000). |
| `IGNORE_REDIS_HEALTH` | Exclude Redis from `/health` decision logic. |

## Configure in Gateway UI

To manage cache runtime settings from Gateway Configuration Manager:

1. Open `https://<your-gateway-url>:8000/console`.
2. Go to **Gateways** > **Your Gateway** > **Manage Gateway** > **Caching Configuration**.
3. Configure cache and proactive cache options.
4. Save changes.

For Kubernetes deployment keys (`globalConfig.clusterCache`, `cacheHA`, and persistence options), see [Helm Values Reference](https://docs.akeyless.io/docs/gateway-kubernetes-helm-values-reference).
