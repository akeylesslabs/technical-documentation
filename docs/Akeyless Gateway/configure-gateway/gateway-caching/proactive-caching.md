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

## Core Behavior

Proactive cache runs only when both cache and proactive cache are enabled.

1. Leadership: One Gateway pod acquires a leadership lock for proactive work.
2. Startup full fetch: The leader performs an initial list-and-load pass.
3. Modified-secrets fetch: Runs every `PROACTIVE_CACHE_MINIMUM_FETCHING_TIME` interval.
4. Full fetch: Runs every full-fetch interval (`CACHE_TTL`-based in current implementation).
5. Zombie cleanup: During full fetch, items missing from current inventory are removed from cache.

If SaaS connectivity is unavailable, proactive jobs stop pulling from SaaS and resume when connectivity returns.

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

## 429 and Rate-Limit Guidance

429 responses can occur when startup warm-up fan-out exhausts the per-access-ID limit window.

To reduce risk:

* Enable `NEW_PROACTIVE_CACHE_ENABLE=true`.
* Reduce `PROACTIVE_CACHE_WORKERS` to lower burst concurrency.
* Increase `PROACTIVE_CACHE_MINIMUM_FETCHING_TIME` to reduce incremental cycle frequency.
* Restrict admin access ID visibility using RBAC so fewer items are warmed.
* Enable or restart proactive cache during low-traffic windows.

For read-path semantics and `ignore-cache`, see [Runtime Caching](https://docs.akeyless.io/docs/runtime-caching).
