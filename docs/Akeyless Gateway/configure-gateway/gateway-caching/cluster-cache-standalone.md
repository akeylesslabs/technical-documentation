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

<GatewayConfigManagementNote />
Standalone cluster cache provides a shared Redis-backed cache across Gateway pods. This improves cross-pod cache consistency compared to [local in-memory cache](https://docs.akeyless.io/docs/runtime-caching).

> ℹ️ **Note:**
> Standalone cluster cache uses a single Redis topology with lower operational overhead.
> If you need Redis failover and higher cache service resilience, use [Cluster Cache High Availability (HA)](https://docs.akeyless.io/docs/cluster-cache-ha).

## Read Behavior

When standalone cluster cache is enabled, runtime reads follow this flow:

1. Gateway receives a read request and starts a cache lookup.
2. Read order is controlled by `PREFER_CLUSTER_CACHE_FIRST`.
3. If a valid cached value is found, Gateway returns it.
4. If no cached value is found, Gateway fetches from SaaS, stores the result in cache, and returns it.
5. If SaaS is unreachable and the value is not already cached, the request fails.

`--ignore-cache` attempts to bypass cache and read directly from SaaS; for full behavior details, see [Gateway Caching](https://docs.akeyless.io/docs/gateway-caching).

### Local Cache and Cluster Cache Read Preference

When standalone cluster cache is enabled, `PREFER_CLUSTER_CACHE_FIRST` controls read preference between the local in-memory cache and the standalone Redis cache.

When `PREFER_CLUSTER_CACHE_FIRST=false` (the default local-first mode), Gateway compares local and Redis `lastModified` metadata and refreshes local entries when Redis is newer.

## Write and Update Behavior

Standalone cluster cache does not change write semantics. Writes are SaaS-first:

1. Gateway writes the update to SaaS.
2. Related cached entries are invalidated.
3. Cache is repopulated on the next read-through fetch (or proactive sync, if enabled).

As a result, short-lived stale reads can occur between a successful write and the next cache refresh.

To reduce this stale-read window:

* For the first read after a write, use `--ignore-cache true` when SaaS connectivity is available.
* Enable proactive caching and tune refresh intervals to shorten convergence time.
* Avoid immediate dependent reads that assume strict read-after-write consistency from cache.

## Persistence

In the Helm chart, standalone persistence is controlled by `globalConfig.clusterCache.persistence.enabled`:

* `false` (default): no PersistentVolumeClaim (PVC) is mounted at `/data`, so cached data is ephemeral and can be lost when the cache pod restarts or is rescheduled.
* `true`: a PVC is mounted at `/data` and Redis can persist to disk so cache data can be retained across restarts and rescheduling.

By default, Redis durability flags are not forced in chart templates. You can pass Redis runtime flags through `globalConfig.clusterCache.extraArgs`. For supported options, see [Redis configuration](https://redis.io/docs/latest/operate/oss_and_stack/management/config/) and [Redis persistence](https://redis.io/docs/latest/operate/oss_and_stack/management/persistence/).

For Kubernetes storage behavior details, see [Persistent Volumes and Claims](https://kubernetes.io/docs/concepts/storage/persistent-volumes/) and [StorageClasses](https://kubernetes.io/docs/concepts/storage/storage-classes/).

## When to Use

Use standalone cluster cache when:

* You run multiple Gateway pods and want shared cache state.
* You want lower operational complexity than HA Sentinel.
* A single Redis instance is acceptable for your availability target.

## When Not to Use

Do not use standalone cluster cache when:

* You require Redis high availability across node failures.
* You need Sentinel-managed failover behavior.

## Configuring Cluster Cache (Standalone)

Use the following deployment-specific options to configure standalone cluster cache:

| Deployment option | How to configure |
| --- | --- |
| Gateway Console | Not supported. Standalone cluster cache topology is deployment-level and is configured in infrastructure manifests. |
| [Kubernetes (Helm)](https://docs.akeyless.io/docs/gateway-deploy-kubernetes-helm) | Set `globalConfig.clusterCache.enabled=true` in `values.yaml`. Configure persistence with `globalConfig.clusterCache.persistence.*` as needed, then [apply a Helm upgrade](https://helm.sh/docs/helm/helm_upgrade/). |
| [Standalone Docker](https://docs.akeyless.io/docs/gateway-deploy-standalone-docker) | Not supported. Standalone cluster cache topology is not configured as a Docker-only deployment option. |
| [Docker Compose](https://docs.akeyless.io/docs/gateway-deploy-docker-compose) | Not supported as a documented deployment mode for standalone cluster cache topology. |
| [Serverless AWS](https://docs.akeyless.io/docs/gateway-deploy-serverless-aws) and [Serverless Azure](https://docs.akeyless.io/docs/gateway-deploy-serverless-azure) | Not supported. Standalone cluster cache topology requires Kubernetes deployment resources. |

Example (`values.yaml`):

```yaml values.yaml
globalConfig:
  env:
    - name: PREFER_CLUSTER_CACHE_FIRST
      value: "false"
  clusterCache:
    enabled: true
    persistence:
      enabled: true
      existingClaim: ""
      accessMode: "ReadWriteOnce"
      storageClass: ""
      size: 10Gi
```

For the full key reference, see [Helm Values Reference](https://docs.akeyless.io/docs/gateway-kubernetes-helm-values-reference).

### Cluster Cache (Standalone) Values

* `globalConfig.clusterCache.enabled`: Enables standalone cluster cache.
* `PREFER_CLUSTER_CACHE_FIRST` (under `globalConfig.env`): Controls read order between local in-memory cache and standalone Redis cache. For value behavior, see [Local Cache and Cluster Cache Read Preference](https://docs.akeyless.io/docs/cluster-cache-standalone#local-cache-and-cluster-cache-read-preference).
* `globalConfig.clusterCache.persistence.enabled`: Enables Redis data persistence for standalone cluster cache so cached data can survive pod restarts, container restarts, and pod rescheduling events.
* `globalConfig.clusterCache.persistence.existingClaim`: Uses an existing [PersistentVolumeClaim (PVC)](https://kubernetes.io/docs/concepts/storage/persistent-volumes/#persistentvolumeclaims) instead of creating a new one.
* `globalConfig.clusterCache.persistence.accessMode`: Sets the PVC access mode (for example, `ReadWriteOnce`). See [Access Modes](https://kubernetes.io/docs/concepts/storage/persistent-volumes/#access-modes).
* `globalConfig.clusterCache.persistence.storageClass`: Sets the Kubernetes [StorageClass](https://kubernetes.io/docs/concepts/storage/storage-classes/) for the PVC.
* `globalConfig.clusterCache.persistence.size`: Sets the requested PVC size. See [Kubernetes Resource Management for Pods and Containers](https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/#meaning-of-memory).
* `globalConfig.clusterCache.extraArgs`: Passes Redis runtime arguments to the standalone cache container. For supported options, see [Redis configuration](https://redis.io/docs/latest/operate/oss_and_stack/management/config/) and [Redis persistence](https://redis.io/docs/latest/operate/oss_and_stack/management/persistence/).
