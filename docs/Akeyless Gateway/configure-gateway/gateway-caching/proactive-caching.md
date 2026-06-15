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

<GatewayConfigManagementNote />
Proactive caching preloads and refreshes cache entries in the background to reduce first-read latency.

> ℹ️ **Note:**
> Proactive caching requires [runtime cache](https://docs.akeyless.io/docs/runtime-caching) and base proactive cache to be enabled (`CACHE_ENABLE=true` and `PROACTIVE_CACHE_ENABLE=true`).
> To use the recommended implementation, also set `NEW_PROACTIVE_CACHE_ENABLE=true`.

The following diagram illustrates the Gateway proactive caching flow:

![Gateway proactive caching flow diagram.](https://files.readme.io/1fdc1d01ea89e625913853199b7ed1aba17bdebdd713ce3b708af7c1fa9b2e77-Cache_Diagaram.png)

## Sync Behavior

Proactive cache runs when `CACHE_ENABLE=true` and `PROACTIVE_CACHE_ENABLE=true`.

The recommended implementation runs when `NEW_PROACTIVE_CACHE_ENABLE=true` is also set.

1. Leadership: One Gateway pod acquires a leadership lock for proactive work.
2. Startup full fetch: The leader performs an initial list-and-load pass.
3. Modified-secrets fetch: Runs every `PROACTIVE_CACHE_MINIMUM_FETCHING_TIME` interval.
4. Full fetch: Runs every full-fetch interval (`CACHE_TTL`-based).
5. Zombie cleanup: During full fetch, items missing from current inventory are removed from cache.

If SaaS connectivity is unavailable, proactive jobs stop pulling from SaaS and resume when connectivity returns.

`--ignore-cache` attempts to bypass cache and read directly from SaaS; for full behavior details, see [Gateway Caching](https://docs.akeyless.io/docs/gateway-caching).

### Access ID Used by Proactive Cache

Proactive cache authenticates to SaaS using the Gateway admin access ID (`GW_ACCESS_ID` / `gatewayAccessId`).

All `list-items` and `get-value` calls during warm-up are issued under this identity. Proactive warm-up consumes the per-access-ID SaaS rate-limit quota for that access ID.

### Rate-Limit Behavior

429 responses can occur when startup warm-up fan-out exhausts the per-access-ID limit window. The recommended implementation handles this automatically with a shared backoff gate:

* Applies a shared backoff delay across proactive workers and RBAC refresh calls on 429.
* Honors `Retry-After` or `will be released in <duration>` headers when available.
* Retries up to `PROACTIVE_CACHE_WORKERS × 10` attempts before giving up on a cycle.

### Leadership-Loss Handling

In the recommended implementation, proactive workers are tied to the current leadership lease. When leadership is lost, active workers stop gracefully, the current cycle drains, and the next leadership cycle starts with a fresh jobs queue to avoid stale backlog carryover.

To further reduce rate-limit risk:

* Reduce `PROACTIVE_CACHE_WORKERS` to lower burst concurrency.
* Increase `PROACTIVE_CACHE_MINIMUM_FETCHING_TIME` to reduce incremental cycle frequency.
* Restrict admin access ID visibility using RBAC so fewer items are warmed up.
* Enable or restart proactive cache during low-traffic windows.

## When to Use

Use proactive caching when:

* You want to eliminate first-read latency across your full secrets inventory.
* You want cache to remain warm through planned cache restarts or Gateway reschedules.
* You run multi-pod Gateway workloads and want consistent pre-warmed state across pods.

## When Not to Use

Do not use proactive caching when:

* Your secrets inventory is very large and startup warm-up would exhaust SaaS rate limits.
* You want each read to reflect the latest SaaS value without a background warm-up delay.

## Configuring Proactive Caching

| Deployment option | How to configure |
| --- | --- |
| Gateway Console | In the Gateway UI, go to **Manage Gateway**, then **Caching** and turn on the **Enable Proactive Caching** toggle. (Requires **Enable Caching** to be on first.) |
| [Kubernetes (Helm)](https://docs.akeyless.io/docs/gateway-deploy-kubernetes-helm) | Set environment variables under `globalConfig.env` in `values.yaml` and [apply a Helm upgrade](https://helm.sh/docs/helm/helm_upgrade/). |
| [Standalone Docker](https://docs.akeyless.io/docs/gateway-deploy-standalone-docker) | Set proactive cache environment variables in container runtime configuration. |
| [Docker Compose](https://docs.akeyless.io/docs/gateway-deploy-docker-compose) | Set the same environment variables in the compose service definition and redeploy. |
| [Serverless AWS](https://docs.akeyless.io/docs/gateway-deploy-serverless-aws) and [Serverless Azure](https://docs.akeyless.io/docs/gateway-deploy-serverless-azure) | Set environment variables in the serverless deployment configuration and redeploy. |

Example (`values.yaml`):

```yaml values.yaml
globalConfig:
  env:
    - name: CACHE_ENABLE
      value: "true"
    - name: PROACTIVE_CACHE_ENABLE
      value: "true"
    - name: NEW_PROACTIVE_CACHE_ENABLE
      value: "true"
    - name: PROACTIVE_CACHE_WORKERS
      value: "3"
    - name: PROACTIVE_CACHE_MINIMUM_FETCHING_TIME
      value: "5"
    - name: CACHE_TTL
      value: "60"
```

For the full key reference, see [Helm Values Reference](https://docs.akeyless.io/docs/gateway-kubernetes-helm-values-reference).

### Proactive Caching Environment Variables

* `CACHE_ENABLE`: Enables the Gateway [runtime cache](https://docs.akeyless.io/docs/runtime-caching) subsystem required by proactive caching. Default: `false`.
* `PROACTIVE_CACHE_ENABLE`: Enables base proactive caching behavior. Default: `false`.
* `NEW_PROACTIVE_CACHE_ENABLE`: Enables proactive caching using the recommended implementation with configurable worker count and shared rate-limit backoff on 429 responses. Default: `false`. If this remains `false` while `CACHE_ENABLE=true` and `PROACTIVE_CACHE_ENABLE=true`, Gateway uses the legacy proactive implementation described in [Migrating from Legacy Proactive Caching](https://docs.akeyless.io/docs/proactive-caching#migrating-from-legacy-proactive-caching).
* `PROACTIVE_CACHE_WORKERS`: Sets the number of concurrent fetch workers for the recommended implementation (requires `NEW_PROACTIVE_CACHE_ENABLE=true`). Default: `3`. Reduce to lower startup fan-out.
* `PROACTIVE_CACHE_MINIMUM_FETCHING_TIME`: Sets the modified-secrets fetch interval in minutes for proactive caching. Default: `5`. Increase to reduce incremental cycle frequency. This value affects proactive refresh cadence in both the legacy and recommended implementations.
* `CACHE_TTL`: Influences cache time-to-live and full-fetch cadence. Default: `60`.
* `PROACTIVE_CACHE_DUMP_INTERVAL`: Sets the periodic secure cache backup interval in minutes for the legacy implementation. This variable has no effect when `NEW_PROACTIVE_CACHE_ENABLE=true`. For most tuning decisions on the legacy implementation, prefer `PROACTIVE_CACHE_MINIMUM_FETCHING_TIME`; adjust `PROACTIVE_CACHE_DUMP_INTERVAL` only when you need to change backup cadence specifically.

> ℹ️ **Note:**
> If Gateway starts without reachable SaaS configuration and initializes cache behavior from environment values, it temporarily enables `NEW_PROACTIVE_CACHE_ENABLE=true` for startup continuity until SaaS configuration becomes reachable.

For Redis topology choices, see [Cluster Cache (Standalone)](https://docs.akeyless.io/docs/cluster-cache-standalone) and [Cluster Cache High Availability (HA)](https://docs.akeyless.io/docs/cluster-cache-ha).

## Migrating from Legacy Proactive Caching

The legacy implementation is enabled when `CACHE_ENABLE=true` and `PROACTIVE_CACHE_ENABLE=true` without `NEW_PROACTIVE_CACHE_ENABLE=true`. On the legacy `akeyless-api-gateway` chart, this was also exposed as the `cachingConf.proActiveCaching.enabled` value.

| | Legacy | Current |
| --- | --- | --- |
| Enabled by | `CACHE_ENABLE=true` + `PROACTIVE_CACHE_ENABLE=true` | `CACHE_ENABLE=true` + `PROACTIVE_CACHE_ENABLE=true` + `NEW_PROACTIVE_CACHE_ENABLE=true` |
| Workers | 5 (fixed) | 3 (default, configurable via `PROACTIVE_CACHE_WORKERS`) |
| Rate-limit handling | None | `RateLimitGate` shared backoff on 429 |
| Chart | `akeyless-api-gateway` or env var only | `akeyless-gateway` |

The legacy implementation uses a fixed worker count with no 429 handling, which can cause repeated rate-limit failures during startup warm-up on large accounts. The new implementation adds backoff and retry logic, configurable concurrency, and is the only implementation that will receive improvements going forward.

If you remain on the legacy implementation, `PROACTIVE_CACHE_DUMP_INTERVAL` controls the periodic secure cache backup interval. Most legacy tuning decisions should still start with `PROACTIVE_CACHE_MINIMUM_FETCHING_TIME`, while `PROACTIVE_CACHE_DUMP_INTERVAL` is mainly relevant when you need to adjust backup cadence.

To migrate:

1. If on the `akeyless-api-gateway` chart, [migrate to the akeyless-gateway chart](https://docs.akeyless.io/docs/gateway-deploy-kubernetes-helm) first.
2. Remove any `cachingConf.proActiveCaching.*` values if present.
3. Add `CACHE_ENABLE=true`, `PROACTIVE_CACHE_ENABLE=true`, and `NEW_PROACTIVE_CACHE_ENABLE=true` to `globalConfig.env` as shown in the [configuration example above](#configuring-proactive-caching).
4. Optionally tune `PROACTIVE_CACHE_WORKERS` and `PROACTIVE_CACHE_MINIMUM_FETCHING_TIME`.
5. Apply a Helm upgrade.
