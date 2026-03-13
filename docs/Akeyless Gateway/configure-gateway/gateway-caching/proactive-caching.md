---
title: Proactive Caching
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
Proactive caching preloads and refreshes cache entries in the background to reduce first-read latency.

## Configuring Proactive Caching

Use the following deployment-specific options to configure proactive caching:

| Deployment option | How to configure |
| --- | --- |
| Gateway Console | In the Gateway UI, go to **Manage Gateway** > **Caching Configuration** and enable proactive caching options. |
| [Kubernetes (Helm)](https://docs.akeyless.io/docs/gateway-deploy-kubernetes-helm) | Set proactive cache keys under `globalConfig.env` in `values.yaml` (for example `PROACTIVE_CACHE_ENABLE`, `NEW_PROACTIVE_CACHE_ENABLE`) and [apply a Helm upgrade](https://helm.sh/docs/helm/helm_upgrade/). |
| [Standalone Docker](https://docs.akeyless.io/docs/gateway-deploy-standalone-docker) | Set proactive cache environment variables (for example `PROACTIVE_CACHE_ENABLE`, `NEW_PROACTIVE_CACHE_ENABLE`, `PROACTIVE_CACHE_WORKERS`) in container runtime configuration. |
| [Docker Compose](https://docs.akeyless.io/docs/gateway-deploy-docker-compose) | Set the same proactive cache environment variables in the compose service definition and redeploy. |
| [Serverless AWS](https://docs.akeyless.io/docs/gateway-deploy-serverless-aws) and [Serverless Azure](https://docs.akeyless.io/docs/gateway-deploy-serverless-azure) | Set proactive cache environment variables in the serverless deployment configuration and redeploy. |

For deployment-specific examples, see [Helm Values Reference](https://docs.akeyless.io/docs/gateway-kubernetes-helm-values-reference), [Docker Advanced Configuration](https://docs.akeyless.io/docs/gateway-docker-advanced-configuration), [Docker Compose Deployment](https://docs.akeyless.io/docs/gateway-deploy-docker-compose), [Serverless AWS Deployment](https://docs.akeyless.io/docs/gateway-deploy-serverless-aws), and [Serverless Azure Deployment](https://docs.akeyless.io/docs/gateway-deploy-serverless-azure).

## Sync Behavior

Proactive cache runs only when both cache and proactive cache are enabled.

1. Leadership: One Gateway pod acquires a leadership lock for proactive work.
2. Startup full fetch: The leader performs an initial list-and-load pass.
3. Modified-secrets fetch: Runs every `PROACTIVE_CACHE_MINIMUM_FETCHING_TIME` interval.
4. Full fetch: Runs every full-fetch interval (`CACHE_TTL`-based in current implementation).
5. Zombie cleanup: During full fetch, items missing from current inventory are removed from cache.

If SaaS connectivity is unavailable, proactive jobs stop pulling from SaaS and resume when connectivity returns.

### Proactive Caching Environment Variables

* `PROACTIVE_CACHE_ENABLE`: Enables or disables proactive caching.
* `NEW_PROACTIVE_CACHE_ENABLE`: Enables the newer proactive caching implementation.
* `PROACTIVE_CACHE_WORKERS`: Sets the worker count for the new proactive cache implementation.
* `PROACTIVE_CACHE_MINIMUM_FETCHING_TIME`: Sets the modified-secrets fetch interval in minutes.
* `CACHE_TTL`: Influences cache time-to-live and full-fetch cadence in current implementation.

Helm equivalent (`values.yaml`):

```yaml values.yaml
globalConfig:
  env:
    - name: PROACTIVE_CACHE_ENABLE
      value: "true"
    - name: NEW_PROACTIVE_CACHE_ENABLE
      value: "true"
    - name: PROACTIVE_CACHE_WORKERS
      value: "3"
```

## Access ID Used by Proactive Cache

Proactive cache authenticates to SaaS using the Gateway admin access ID (`GW_ACCESS_ID` / `gatewayAccessId`).

All list-items and get-value calls during warm-up are issued under this identity. This means proactive warm-up consumes the per-access-ID SaaS rate-limit quota for that access ID.

## Implementations

| Implementation | Enabled by | Workers | Rate-limit handling |
| --- | --- | --- | --- |
| Original | `PROACTIVE_CACHE_ENABLE=true` | 5 (fixed) | None |
| New | `PROACTIVE_CACHE_ENABLE=true` + `NEW_PROACTIVE_CACHE_ENABLE=true` | 3 (default, configurable via `PROACTIVE_CACHE_WORKERS`) | `RateLimitGate` shared backoff on 429 |

The new implementation:

* Applies a shared backoff delay across workers on 429.
* Uses `Retry-After` or `will be released in <duration>` when available.
* Retries up to `PROACTIVE_CACHE_WORKERS × 10` attempts.

## Rate-Limit Behavior

429 responses can occur when startup warm-up fan-out exhausts the per-access-ID limit window.

To reduce risk:

* Enable `NEW_PROACTIVE_CACHE_ENABLE=true`.
* Reduce `PROACTIVE_CACHE_WORKERS` to lower burst concurrency.
* Increase `PROACTIVE_CACHE_MINIMUM_FETCHING_TIME` to reduce incremental cycle frequency.
* Restrict admin access ID visibility using RBAC so fewer items are warmed.
* Enable or restart proactive cache during low-traffic windows.

`--ignore-cache` attempts to bypass cache and read directly from SaaS; for full behavior details, see [Gateway Caching](https://docs.akeyless.io/docs/gateway-caching).

For Redis topology choices, see [Cluster Cache (Standalone)](https://docs.akeyless.io/docs/cluster-cache-standalone) and [Cluster Cache High Availability (HA)](https://docs.akeyless.io/docs/cluster-cache-ha).
