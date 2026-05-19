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
Use this section to choose the right Gateway caching method for your environment.

> ❗ **Important:**
>
> For ongoing cache configuration changes, use the Gateway Configuration Manager, CLI, or Helm values (for Kubernetes) instead of per-instance container startup command changes.

## Cache Types

Gateway caching has four practical patterns to choose from:

| Type | Best for | Avoid when |
| --- | --- | --- |
| [Runtime Caching](https://docs.akeyless.io/docs/runtime-caching) | Standard request acceleration and reduced repeated SaaS fetches | You need all reads to always bypass cache |
| [Proactive Caching](https://docs.akeyless.io/docs/proactive-caching) | Pre-warming and refresh jobs to reduce first-read latency | Your environment is rate-limit constrained |
| [Cluster Cache (Standalone)](https://docs.akeyless.io/docs/cluster-cache-standalone) | Shared Redis cache for multi-pod Gateway with low operational overhead | You require cache failover across Redis node or pod failures |
| [Cluster Cache High Availability (HA)](https://docs.akeyless.io/docs/cluster-cache-ha) | Sentinel-based high-availability cache service for resilient shared cache | You prefer the simplest deployment footprint and can accept standalone Redis risk |

## Choosing a Caching Method

Use this starting decision flow:

1. Start with runtime caching for most environments.
2. Add proactive caching when you need faster first-read performance for frequently used secrets.
3. Add standalone cluster cache when running multiple Gateway pods that should share cache state.
4. Use Cluster Cache High Availability (HA) when shared cache availability across failures is a requirement.

For planning guidance and tradeoffs, see [Gateway Best Practices: Caching strategy considerations](https://docs.akeyless.io/docs/gateway-best-practices#caching-strategy-considerations).

For Kubernetes proactive cache sizing guidance, see [Gateway Best Practices: Resource planning for Kubernetes proactive cache](https://docs.akeyless.io/docs/gateway-best-practices#resource-planning-for-kubernetes-proactive-cache).

## Configure in Gateway UI

To manage cache runtime settings from Gateway Configuration Manager:

1. Open `https://<your-gateway-url>:8000/console`.
2. Go to **Gateways**, then **Your Gateway**, then **Manage Gateway**, then **Caching Configuration**.
3. Configure cache and proactive cache options.
4. Save changes.

For Kubernetes deployment keys (`globalConfig.clusterCache`, `cacheHA`, and persistence options), see [Helm Values Reference](https://docs.akeyless.io/docs/gateway-kubernetes-helm-values-reference).

Use the Akeyless CLI to update cache runtime settings, for example:

```shell
akeyless gateway update cache \
--enable-cache true \
--enable-proactive true \
--stale-timeout 60 \
--minimum-fetch-interval 5 \
--gateway-url 'https://<Your-Akeyless-GW-URL>:8000'
```

## ignore-cache Behavior

The `ignore-cache` flag is intended to bypass cache and fetch directly from SaaS.

<!-- secret-stdout-scan:ok -->
```shell
akeyless get-secret-value --name /mysecret --ignore-cache true
```

In disconnected mode (when SaaS is unreachable), runtime still checks cache first even when `ignore-cache=true`. If the value is not cached, the request fails.
