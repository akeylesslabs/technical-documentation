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
2. If cluster cache is enabled ([Cluster Cache (Standalone)](https://docs.akeyless.io/docs/cluster-cache-standalone) or [Cluster Cache High Availability (HA)](https://docs.akeyless.io/docs/cluster-cache-ha)), lookup order is controlled by `PREFER_CLUSTER_CACHE_FIRST`.
3. If a valid cached value is found, the Gateway returns it immediately to the caller.
4. After a cache hit, the Gateway can refresh from SaaS in the background to keep cache entries current.
5. If no cached value exists, the Gateway reads from SaaS, stores the value in cache, and then returns it to the caller.
6. If SaaS is unreachable and no cached value exists, the request fails.

`--ignore-cache` attempts to bypass cache and read directly from SaaS; for full behavior details, see [Gateway Caching](https://docs.akeyless.io/docs/gateway-caching).

### Local Cache and Cluster Cache Read Preference

When cluster cache is enabled, `PREFER_CLUSTER_CACHE_FIRST` controls read preference between the local in-memory cache and the Redis cache.

When `PREFER_CLUSTER_CACHE_FIRST=false` (the default local-first mode), the Gateway also compares local and Redis `lastModified` metadata and refreshes local entries when Redis is newer.

For Redis deployment topology, see [Cluster Cache (Standalone)](https://docs.akeyless.io/docs/cluster-cache-standalone) and [Cluster Cache High Availability (HA)](https://docs.akeyless.io/docs/cluster-cache-ha).

## Write and Update Behavior

Gateway write operations are SaaS-first. There is no synchronous write-through update to cache.

Current implementation pattern:

1. A write or update request is sent to SaaS.
2. Matching cached items are invalidated (removed) by update, delete, and rotate flows.
3. Cache converges on the next read-through fetch or proactive synchronization cycle.

As a result, stale reads can occur temporarily between a successful write and the next cache refresh.

## When to Use

Use runtime caching when:

* You want lower read latency for repeated secret retrieval requests.
* You want Gateway to continue serving cached values during temporary SaaS interruptions.
* You need a baseline caching mode that can be combined with proactive caching or cluster cache.

## When Not to Use

Do not rely on runtime caching alone when:

* You require strict read-after-write consistency for every request.
* You need shared cache state across multiple Gateway pods without local cache divergence.
* Your workload requires every read to fetch directly from SaaS.

## Configuring Runtime Caching

Use the following deployment-specific options to configure runtime caching:

| Deployment option | How to configure |
| --- | --- |
| Gateway Console | In the Gateway UI, go to **Manage Gateway**, then **Caching** and turn on the **Enable Caching** toggle. |
| [Kubernetes (Helm)](https://docs.akeyless.io/docs/gateway-deploy-kubernetes-helm) | Set runtime behavior keys under `globalConfig.env` in `values.yaml` (for example `CACHE_ENABLE`, `PREFER_CLUSTER_CACHE_FIRST`) and [apply a Helm upgrade](https://helm.sh/docs/helm/helm_upgrade/). Set `IGNORE_REDIS_HEALTH` separately when you want to change health-check behavior. |
| [Standalone Docker](https://docs.akeyless.io/docs/gateway-deploy-standalone-docker) | Set cache-related environment variables (for example `CACHE_ENABLE`, `PREFER_CLUSTER_CACHE_FIRST`) in container runtime configuration. |
| [Docker Compose](https://docs.akeyless.io/docs/gateway-deploy-docker-compose) | Set the same cache-related environment variables in the compose service definition and redeploy. |
| [Serverless AWS](https://docs.akeyless.io/docs/gateway-deploy-serverless-aws) and [Serverless Azure](https://docs.akeyless.io/docs/gateway-deploy-serverless-azure) | Set cache-related environment variables in the serverless deployment configuration and redeploy. |

Example (`values.yaml`):

```yaml values.yaml
globalConfig:
  env:
    - name: CACHE_ENABLE
      value: "true"
    - name: PREFER_CLUSTER_CACHE_FIRST
      value: "false"
    - name: IGNORE_REDIS_HEALTH
      value: "false"
```

### Runtime Caching Environment Variables

* `CACHE_ENABLE`: Enables or disables the Gateway cache subsystem. This controls runtime caching behavior and is a prerequisite for proactive cache activity.
* `PREFER_CLUSTER_CACHE_FIRST`: Controls cache lookup order when cluster cache is enabled. For value behavior, see [Local Cache and Cluster Cache Read Preference](https://docs.akeyless.io/docs/runtime-caching#local-cache-and-cluster-cache-read-preference).
* `IGNORE_REDIS_HEALTH`: Controls whether Redis connectivity affects the `/health` handler result. This does not change runtime cache read or write behavior directly, but it does affect how orchestration and load balancers treat Gateway availability when Redis is degraded.
    * `false` (default): Redis connectivity failures can fail `/health`.
    * `true`: Redis connectivity is ignored by `/health` checks.
