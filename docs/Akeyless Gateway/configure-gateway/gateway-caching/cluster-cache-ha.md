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

<GatewayConfigManagementNote />
Cluster Cache High Availability (HA) uses a [Redis Sentinel](https://redis.io/docs/latest/operate/oss_and_stack/management/sentinel/) topology for resilient shared cache service.

> ℹ️ **Note:**
> Cluster Cache HA uses Redis Sentinel for failover and higher cache service resilience.
> If you prefer a simpler single-Redis topology with lower operational overhead, use [Cluster Cache (Standalone)](https://docs.akeyless.io/docs/cluster-cache-standalone).

## Read Behavior

When Cluster Cache HA is enabled, runtime reads follow this flow:

1. Gateway receives a read request and starts a cache lookup.
2. Read order is controlled by `PREFER_CLUSTER_CACHE_FIRST`.
3. If a valid cached value is found, Gateway returns it.
4. If no cached value is found, Gateway fetches from SaaS, stores the result in cache, and returns it.
5. If SaaS is unreachable and the value is not already cached, the request fails.

`--ignore-cache` attempts to bypass cache and read directly from SaaS; for full behavior details, see [Gateway Caching](https://docs.akeyless.io/docs/gateway-caching).

### Local Cache and Cluster Cache Read Preference

When Cluster Cache HA is enabled, `PREFER_CLUSTER_CACHE_FIRST` controls read preference between the local in-memory cache and the HA Redis cache.

When `PREFER_CLUSTER_CACHE_FIRST=false` (the default local-first mode), Gateway compares local and Redis `lastModified` metadata and refreshes local entries when Redis is newer.

## Write and Update Behavior

Cluster Cache HA does not change write semantics. Writes are SaaS-first:

1. Gateway writes the update to SaaS.
2. Related cached entries are invalidated.
3. Cache is repopulated on the next read-through fetch (or proactive sync, if enabled).

As a result, short-lived stale reads can occur between a successful write and the next cache refresh.

To reduce this stale-read window:

* For the first read after a write, use `--ignore-cache true` when SaaS connectivity is available.
* Enable proactive caching and tune refresh intervals to shorten convergence time.
* Avoid immediate dependent reads that assume strict read-after-write consistency from cache.

## Persistence

In the Helm chart, HA persistence is controlled by `cacheHA.persistentVolume.enabled`:

* `true` (default): PVCs are mounted and Redis can persist to disk so cache data can be retained across restarts and rescheduling.
* `false`: no PersistentVolumeClaim (PVC) is mounted, so cache data is ephemeral and can be lost when cache pods restart or are rescheduled.

For Kubernetes storage behavior details, see [Persistent Volumes and Claims](https://kubernetes.io/docs/concepts/storage/persistent-volumes/) and [StorageClasses](https://kubernetes.io/docs/concepts/storage/storage-classes/).

## When to Use

Use Cluster Cache HA when:

* You need cache availability during single-pod or single-node failures.
* You run multi-pod Gateway workloads that require resilient shared cache service.
* Your platform requirements justify [Redis Sentinel operational overhead](https://redis.io/docs/latest/operate/oss_and_stack/management/sentinel/#fundamental-things-to-know-about-sentinel-before-deploying).

## When Not to Use

Do not use Cluster Cache HA when:

* You run a simple or low-scale environment where standalone Redis is sufficient.
* You want the smallest operational footprint for cache infrastructure.

## Configuring Cluster Cache High Availability (HA)

Use the following deployment-specific options to configure Cluster Cache HA:

| Deployment option | How to configure |
| --- | --- |
| Gateway Console | Not supported. Cluster Cache HA is deployment-level and is configured in infrastructure manifests. |
| [Kubernetes (Helm)](https://docs.akeyless.io/docs/gateway-deploy-kubernetes-helm) | Set `cacheHA.enabled=true` in `values.yaml`. Configure authentication, persistence, and scheduling keys under `cacheHA.*`, then [apply a Helm upgrade](https://helm.sh/docs/helm/helm_upgrade/). |
| [Standalone Docker](https://docs.akeyless.io/docs/gateway-deploy-standalone-docker) | Not supported. Cluster Cache HA topology is not configured as a Docker-only deployment option. |
| [Docker Compose](https://docs.akeyless.io/docs/gateway-deploy-docker-compose) | Not supported as a documented deployment mode for Cluster Cache HA topology. |
| [Serverless AWS](https://docs.akeyless.io/docs/gateway-deploy-serverless-aws) and [Serverless Azure](https://docs.akeyless.io/docs/gateway-deploy-serverless-azure) | Not supported. Cluster Cache HA topology requires Kubernetes deployment resources. |

Example (`values.yaml`):

```yaml values.yaml
globalConfig:
  env:
    - name: PREFER_CLUSTER_CACHE_FIRST
      value: "false"
cacheHA:
  enabled: true
  replicas: 3
  auth: true
  authKey: redis-password
  existingSecret: "gw-cluster-cache-ha"
  persistentVolume:
    enabled: true
    storageClass: ""
    size: 10Gi
```

For the full key reference, see [Helm Values Reference](https://docs.akeyless.io/docs/gateway-kubernetes-helm-values-reference).

### Cluster Cache (HA) Values

* `cacheHA.enabled`: Enables HA cluster cache with Redis Sentinel.
* `PREFER_CLUSTER_CACHE_FIRST` (under `globalConfig.env`): Controls read order between local in-memory cache and HA Redis cache. For value behavior, see [Local Cache and Cluster Cache Read Preference](https://docs.akeyless.io/docs/cluster-cache-ha#local-cache-and-cluster-cache-read-preference).
* `cacheHA.replicas`: Sets the number of HA Redis pods.
* `cacheHA.auth`: Enables password authentication for HA Redis and Sentinel endpoints. Use `true` in shared or multi-tenant clusters where unauthenticated Redis access is not acceptable.
* `cacheHA.authKey`: Sets the secret key name that stores the Redis password in the [Kubernetes Secret](https://kubernetes.io/docs/concepts/configuration/secret/) referenced by `cacheHA.existingSecret`.
* `cacheHA.existingSecret`: Uses an existing [Kubernetes Secret](https://kubernetes.io/docs/concepts/configuration/secret/) that contains the Redis password. Use this when your platform manages secrets centrally (for example, External Secrets or an existing secret-management workflow).
* `cacheHA.persistentVolume.enabled`: Enables or disables persistent storage for HA Redis data so cache data can survive pod restarts, container restarts, and pod rescheduling events.
* `cacheHA.persistentVolume.storageClass`: Sets the [Kubernetes StorageClass](https://kubernetes.io/docs/concepts/storage/storage-classes/) used for HA Redis [PersistentVolumeClaims (PVCs)](https://kubernetes.io/docs/concepts/storage/persistent-volumes/#persistentvolumeclaims).
* `cacheHA.persistentVolume.size`: Sets the requested PVC size for HA Redis data. See [Kubernetes Resource Management for Pods and Containers](https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/#meaning-of-memory).
* `cacheHA.hardAntiAffinity`: Uses required [pod anti-affinity](https://kubernetes.io/docs/concepts/scheduling-eviction/assign-pod-node/#affinity-and-anti-affinity) rules to spread HA cache pods across nodes. Use this when node-level failure tolerance is required.
* `cacheHA.topologySpreadConstraints.*`: Configures [topology spread constraints](https://kubernetes.io/docs/concepts/scheduling-eviction/topology-spread-constraints/) to balance pods across zones or nodes according to your availability policy.

For complete values and examples, see [Helm Values Reference](https://docs.akeyless.io/docs/gateway-kubernetes-helm-values-reference).
