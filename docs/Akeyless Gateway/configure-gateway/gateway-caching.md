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
Upon network outage, the Gateway cache can still handle requests for Secrets retrievals (read-only). The cache will start working only after the Gateway is successfully operated. Only users already authenticated can get service from the Gateway cache, where the following [Authentication Methods](https://docs.akeyless.io/docs/access-and-authentication-methods) can keep authenticating on offline modes: **K8s**, **email**, **API Key**, **LDAP**, **Certificate** and **JWT**.

> ℹ️ **Note (Offline Authentication Cache):**
>
> Offline authentication cache is only supported in [Cluster Cache](https://docs.akeyless.io/docs/gateway-caching#cluster-cache-mode) mode and requires the user being authenticated to have at least list permission on the relevant Authentication Method.

The most straightforward use cases are the following:

* The Gateway Cache is used to improve performance when fetching secrets.

* The Proactive Cache enables storing secrets in the Gateway Cache in advance upon successful user authentication.

The Gateway cache uses two primary types of caches: a **Local In-Memory Cache** for individual Gateway instances and a **Cluster Cache** for high availability in Kubernetes environments. This architecture ensures that secrets are readily available to applications while minimizing the load on the Akeyless SaaS platform.

In a high-availability configuration, secrets are stored in a **Cluster Cache**, typically backed by an internal database instance. This shared cache ensures every pod has a consistent view of the cached data. This model is crucial for resilience, as it allows the Gateway to continue serving cached secrets even during a complete Akeyless SaaS outage. Authentication can also persist during an outage for methods that can be validated locally, such as Kubernetes ServiceAccount authentication, where the Gateway can verify the token against the cluster's Kubernetes API server without needing to contact the SaaS.

## Gateway Cache

To enable and configure the Gateway Cache:

1. Open the **Akeyless Gateway Configuration Manager** at `https://Your_Akeyless_Gateway_URL:8000/console`.

2. On the menu bar at the left, click **Gateways > Your-Gateway > Manage Gateway > Caching Configuration**.

3. Select the **Enable Caching** checkbox.

4. Set the **Stale Timeout** value. This is the time (in minutes) during which a secret should be kept in the cache. The secret is deleted from the cache at the end of this period. By default, cached secrets will expire after 60 minutes.

5. Click **Save Changes**.

> ℹ️ **Note:**
>
> Usually, after the Stale Timeout period expires for a secret, the secret is deleted from the Gateway Cache.
>
> If there is no internet connection, the Gateway Cache won’t delete old items until the internet connection is restored.

## Proactive Gateway Cache

The Proactive Cache fetches all secrets from the Akeyless Cloud and stores them in the Gateway Cache upon successful authentication (based on the user access policy). To manage each user's access policy, the [Gateway's default Auth Method](https://docs.akeyless.io/docs/gateway-deploy-kubernetes-helm#authentication) must have **List** permissions for **Auth-Methods** and **Roles**, as well as **Read** permission for the secret intended to be saved in the cache.

The Gateway uses a proactive caching model with a delta-based update process to avoid the resource-intensive task of re-fetching all secrets periodically. This is managed by two parallel background processes:

* **Refresh-TTL Ticker**: This process runs at a configurable interval (by default every 5 minutes) and queries the Akeyless SaaS platform only for secrets that have been modified within that time window. By checking just for the delta of updated secrets, the Gateway significantly reduces the overhead of keeping the cache synchronized.
* **Cleanup-TTL Ticker:** This independent process periodically compares the cache with the SaaS to remove entries for secrets that have been deleted or for which the Gateway's access permissions have been revoked.

This dual-ticker system ensures the cache remains fresh and accurate with minimal performance impact. When a user updates a secret in the Akeyless UI, the change is picked up by the next refresh cycle, and the updated value is propagated to the cache and subsequently to the workload without requiring any manual intervention. This provides a highly efficient and scalable solution for secrets management.

The following diagram illustrates the key phases of the Akeyless Gateway's proactive caching mechanism, showing how it efficiently populates and maintains its cache, and how an application consumes secrets from it.
In this example, the user set the Refresh-TTL Ticker to 2 minutes.

![Illustration for: The following diagram illustrates the key phases of the Akeyless Gateway's proactive caching mechanism, showing how it efficiently populates and maintains its cache, and how an…](https://files.readme.io/1fdc1d01ea89e625913853199b7ed1aba17bdebdd713ce3b708af7c1fa9b2e77-Cache_Diagaram.png)

To enable and configure the Proactive Cache:

1. Open the **Akeyless Gateway Configuration Manager** at `https://Your_Akeyless_Gateway_URL:8000/console`.

2. On the menu bar at the left, click **Gateways > Your-Gateway > Manage Gateway > Caching Configuration**.

3. Select the **Enable Proactive Caching** checkbox.

    > 🚧 Using Legacy Mode
    >
    > Once you disable **Legacy Mode**, you won't be able to re-enable it.

4. Set the **Refresh TTL** value. This setting instructs the system to update secrets in the cache if they are older than the specified value. By default, each secret kept in the cache for more than 5 minutes will be re-requested from the Akeyless Cloud or the local Gateway.

5. Set the **Cleanup TTL** value. Compares the cache with the SaaS to remove entries for secrets that have been deleted or for which the Gateway's access permissions have been revoked.

6. Click **Save Changes**.

## Cluster Cache Mode

When deploying Gateway on Kubernetes, a Cluster Cache can be set in addition to support offline authentication, this results in an additional service that syncs all pods and has a shared storage, to keep the secrets encrypted at rest, this mode requires a Kubernetes encryption key. This feature can be set **only** during deployment. To set this follow the installation guide under the [cache](https://docs.akeyless.io/docs/advanced-k8s-gateway-configuration#cache-configuration) section.

## Bypass Cache

When Cache is enabled by default, any client that requests a secret from the relevant Gateway will receive the latest cached value of the secret. To work directly with the Akeyless SaaS, to ensure you are retrieving the latest value of the secret, you can specify the `ignore-cache` setting as part of the request to by-pass the cache mechanism:

```shell
akeyless get-secret-value -n /mysecret --ignore-cache true
```

## How does cluster cache affect communication and authentication?

This section explains how the Gateway behaves during normal operations (BAU) and during Akeyless SaaS outages when cluster cache is enabled.

When a Gateway with **cluster cache** is deployed, it significantly enhances resilience and efficiency by acting as a high-availability layer in front of the Gateway. The client's primary point of contact remains the Gateway, but the behavior changes to prioritize the cache. Here is how communication and authentication are handled in different situations.

**Business As Usual (BAU) operations**:
During normal operations, the communication flow is optimized for speed and reduced load on the Akeyless SaaS.

1. **Initial Request**: The client needs a secret and sends an authenticated request to the Akeyless Gateway.
2. **Authentication**: The Gateway forwards the initial request to the SaaS auth service, and the token and credentials (JWT) are stored in the Gateway cache.

**Akeyless SaaS outage**:
The primary benefit of cluster cache is realized during a SaaS outage. The goal shifts from efficiency to business continuity.

1. **Initial Request**: The client needs a secret and sends an authenticated request to the Akeyless Gateway.
2. **Authentication**: Authentication requests to the Gateway still succeed because the client's authentication information is already stored in cache and can be validated.

Generating new tokens is not possible during an outage because this capability resides with SaaS. The system can only issue tokens that were previously retrieved and cached before the outage.

## What are the supported cache types?

The Akeyless Gateway uses two cache types to ensure both performance and service continuity.

1. **Local In-Memory Cache**: Speeds up day-to-day secret retrieval by keeping the latest value locally.
2. **Cluster Cache Mode (Kubernetes only)**: Provides a shared, highly available encrypted cache service for all Gateway pods in a Kubernetes deployment. Helm chart deployment spins up a `cache` service, and all pods `read/write` through it so every pod sees the same cached objects. Secrets are stored encrypted at rest. You provide a Kubernetes Secret for the cluster cache encryption key and can optionally enable TLS between pods and cache. Because cache is external to any single pod, rolling upgrades or pod restarts do not clear the cache. An optional cache HA flag turns the service itself into a multi-replica set backed by a `ReadWriteOnce` StorageClass (`Gateway version v4.34 and later`).

## How proactive cache works

When proactive cache is enabled, the Gateway stays current through one startup action and two background tickers:

1. **Startup full-sync (one-off)**: On startup (or after cache restore), the Gateway authenticates with its administrative identity and pulls every secret it is entitled to read. This warms local cache so first requests are served quickly and the Gateway is ready for offline operation.
2. **Refresh-TTL ticker**: At a configurable interval, the Gateway asks SaaS only for secrets whose last-modified timestamp falls within that window. Changed items are overwritten in cache.
3. **Cleanup-TTL ticker**: Independently, every configured interval, the Gateway compares cache with SaaS and removes entries for deleted secrets or permissions that were revoked.

The two tickers run in parallel. If Akeyless cloud services become unreachable, they pause while the Gateway continues serving requests from existing cache. Default intervals are typically five minutes for refresh and sixty minutes for cleanup, and can be tuned to balance freshness, bandwidth, and security requirements.

## Behavior during Gateway outage

### Local in-memory cache

If a single Gateway instance goes down, its in-memory cache is lost. Secrets and authentication data stored only in that instance become unavailable until a healthy Gateway can fetch them again.

Clients targeting that failed instance will fail. If other Gateway instances are healthy, requests can still be served by them. If no Gateway is healthy, requests fail until at least one instance is restored.

### Cluster cache

If a Gateway instance in a cluster fails, shared cluster cache remains available to other healthy Gateway instances. Secrets and authentication data persisted in cluster cache are not lost.

Other active Gateway instances can continue to serve requests by retrieving data from cluster cache.

## Behavior during SaaS outage

### Local in-memory cache

The Gateway serves requests for secrets and authentication from local cache if values exist. Minimum fetching interval is effectively ignored while SaaS is unreachable. Gateway can continue to authenticate existing sessions for supported methods (Kubernetes, API Key, Password, LDAP, Certificate, JWT) when credentials and auth data are cached.

In offline mode, credential expiration is ignored.

### Cluster cache

Similar to local cache behavior, the Gateway leverages shared cluster cache so all Gateway instances can access the same cached data. This provides a stronger offline mode for multi-instance deployments.

## Behavior during both Gateway and SaaS outage

If all Gateway instances are down, no requests can be served regardless of cache status.

If Gateways restart while SaaS is still down, they try to load configuration, identities, secrets, and auth data from cluster cache. If cluster cache is unavailable, Gateways start without cached data and cannot serve requests until SaaS or cluster cache is restored.

If cluster cache is available, Gateways warm from cluster cache and can operate in degraded offline mode for cached secrets and authentication.

## Do behaviors differ by client type (for example, Injector versus ESO)?

Core caching behavior and outage impact on Gateway are the same regardless of client type. Both Akeyless Injector and External Secrets Operator (ESO) call Gateway REST APIs.

ESO's sync model generally provides more resilience for applications during Gateway or SaaS outages, since applications consume local Kubernetes Secret objects. Injector may cause pod startup failures or stale values if an outage occurs during injection and `AKEYLESS_CRASH_POD_ON_ERROR` is enabled.

## Gateway cache deployment configuration options

| Name | Description |
| --- | --- |
| `CACHE_ENABLE` | Whether cache is enabled. |
| `PROACTIVE_CACHE_ENABLE` | Whether proactive caching is enabled. |
| `NEW_PROACTIVE_CACHE_ENABLE` | Whether to use the newer proactive cache mechanism. |
| `PREFER_CLUSTER_CACHE_FIRST` | Whether to read cluster cache before local cache. |
| `CACHE_MAX_ITEMS` | Maximum number of proactive cache items (overrides default 50K). |
| `IGNORE_REDIS_HEALTH` | Whether `/health` should ignore Redis outage and still return `200 OK`. |

These settings apply consistently to both Kubernetes/Helm and VM/Docker deployments.

## Behavior when caching is enabled and a user updates a secret in UI

When a secret is updated in UI, value retrieval by CLI/API may initially return the cached value, then sync and return the new value after cache refresh. Gateway updates local cache first, then cluster cache.

If `PREFER_CLUSTER_CACHE_FIRST` is enabled, values are fetched from cluster cache first, which helps return newer values when multiple Gateway instances exist.

If no request is made immediately, proactive cache updates values on its next refresh interval.

## When SaaS is considered down for token validation and expiration

Gateway continuously monitors SaaS connectivity. On failed connectivity checks, it switches to offline mode. While SaaS is unreachable, token validation and expiration checks are suspended. Cached tokens remain valid until SaaS connectivity is restored.

## `Ignore Cache` behavior in disconnected mode

By default, Gateway caches secrets for performance and resilience. `Ignore Cache` is intended to bypass cache and fetch the latest secret from SaaS.

In disconnected mode, Gateway cannot reach SaaS. Therefore:

* With `Ignore Cache` enabled, Gateway still checks local cache first.
* If secret exists in cache, Gateway returns cached value.
* If secret does not exist in cache, request fails because SaaS cannot be reached.
