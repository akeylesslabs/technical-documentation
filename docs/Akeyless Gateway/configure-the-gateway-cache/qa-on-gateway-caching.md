---
title: Q&A on Gateway Caching
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
## How does the communication behavior change when there is a Cluster Cache, and how is authentication handled during BAU situations and SaaS outages?

When a Gateway with **cluster cache** is deployed, it significantly enhances resilience and efficiency by acting as a high-availability layer in front of the Gateway. The client's primary point of contact remains the Gateway, but the behavior changes to prioritize the cache. Here’s how communication and authentication are handled in different situations.

**Business As Usual (BAU) Operations**:\
During normal operations, the communication flow is optimized for speed and reduced load on the Akeyless SaaS.

1. **Initial Request**: The client needs a secret, sends an authenticated request to the Akeyless Gateway.
2. **Authentication**: Gateway will forward the initial request to the SaaS auth service, and the token and creds (JWT) will be stored in the Gateway cache.

**Akeyless SaaS Outage**:\
The primary benefit of the cluster cache is realized during a SaaS outage. The goal shifts from efficiency to business continuity.

1. **Initial Request**: The client needs a secret and sends an authenticated request to the Akeyless Gateway
2. **Authentication**: Authentication requests to the Gateway will still succeed. Since the client’s authentication information is already stored in the cache, the gateway can successfully validate the client.\
   However, generating new `tokens` isn’t possible during the outage, as this capability resides with the SaaS. The system can only issue tokens that were previously retrieved and cached before the outage occurred.

## What are the supported cache types?

The Akeyless Gateway utilizes two distinct types of caches to ensure both high performance and robust service continuity between your network and the Akeyless SaaS platform.

The types of caches are:

1. **Local In Memory Cache** Speed up day-to-day secret retrieval by keeping the last value locally.
2. **Cluster Cache Mode (K8S only)**: Provide a shared, highly available, encrypted cache service for all Gateway pods in a Kubernetes deployment. Helm chart spins up a `cache` service, all pods `read/write` through it, so every pod sees the same cached objects. Secrets are stored encrypted at rest, you supply a `K8s` Secret cluster cache encryption key (and optional TLS between pod and cache). Because the cache is external to any single pod, rolling upgrades or pod restarts do not clear the cache. An optional cache HA flag turns the service itself into a multi-replica set backed by a `ReadWriteOnce` storage class (`Gateway version v4.34 and higher`).

## How Proactive cache works?

When Proactive Cache is turned on, the Gateway keeps itself current through one startup action and two background tickers:

1. **Startup full-sync (one-off)**: As soon as the Gateway boots (or after a cache restore), it authenticates with its administrative identity and pulls every secret it is entitled to read. That initial sweep “warms” the local cache so that first requests are served instantly and the Gateway is ready for offline operation.
2. **Refresh-TTL ticker**: At a fixed interval that you configure (x minutes), the Gateway asks SaaS only for secrets whose Last-Modified timestamp falls within that window. Any items that were changed are overwritten in the cache. This keeps secrets fresh while avoiding the cost of re-downloading everything.
3. **Cleanup-TTL ticker**: Independently, every `X` minutes the Gateway compares its cache with SaaS. It removes entries whose underlying secret has been deleted or for which the admin identity no longer has read permission. This prevents the Gateway from serving stale or unauthorized data and keeps the cache footprint small.

The two tickers run in parallel. If the Akeyless cloud services become unreachable, they pause automatically while the Gateway continues servicing requests from whatever data is already cached. Default intervals are typically five minutes for refresh and sixty minutes for cleanup, but you can adjust them to balance freshness, bandwidth, and security requirements.

## What would be the behavior of each caching mechanism during a Gateway outage?

**Local In-Memory Cache:**

Behavior: If a single Gateway instance goes down, its in-memory cache is lost. Any secrets and authentication data stored solely in that instance's local cache will become unavailable until a new or surviving Gateway instance can fetch them.\
Impact: Clients (Injector, ESO, or direct API calls) attempting to reach this specific downed Gateway instance will fail. If there are other healthy Gateway instances, requests will be routed to them. If the failed Gateway was the only one, or if all Gateway instances in a standalone setup fail, all requests will fail until a Gateway is restored.

**Cluster Cache:**

Behavior: If a Gateway instance in a cluster fails, the shared cluster cache remains available to other healthy Gateway instances. Secrets and authentication data persisted in the cluster cache are not lost.\
Impact: Other active Gateway instances can continue to serve requests by retrieving data from the cluster cache. This significantly enhances the high availability of the Gateway layer. Clients communicating with the healthy Gateway instances will experience continuous service for cached data. 

## What would be the behavior of each caching mechanism during a SaaS Outage?

**Local In-Memory Cache**:

Behavior: The Gateway will attempt to serve requests for secrets and authentication from its local in-memory cache. If a secret is present in the cache, the Gateway will serve it from the cache. The Minimum Fetching Interval will be ignored as the SaaS is unreachable. The Gateway can continue to authenticate existing sessions for supported authentication methods (K8s, API Key, Password, LDAP, Certificate, JWT) if the credentials and authentication data are cached. Crucially, in offline mode, credentials' expiration is ignored.

Impact: Read-only operations for cached secrets will succeed. If the curl\_proxy has cached the necessary authentication data (e.g., system credentials for a K8S Auth Method), new authentications succeed.

**Cluster Cache**:

Behavior: Similar to the local cache, the Gateway will leverage the shared cluster cache to serve secrets and authentication data. This means all Gateway instances in the cluster will have access to the same cached data. The curl\_proxy processes on each Gateway instance will also utilize this shared cache for authentication data.

Impact: The cluster cache provides a more robust offline mode. All active Gateway instances can provide consistent cached data.

## What would be the behavior of each caching mechanism during both Gateway and SaaS outage?

Behavior: If all Gateway instances are down, no requests can be served, regardless of cache status, as there's no active component to process them. If the Gateways restart while the SaaS is still down, they will try to load configurations, cluster identities, secrets, and authentication data from the Cluster Cache (cluster cache). If the cluster cache is also down or unreachable, the Gateways will start with no cached data and will be unable to serve any requests until both the Gateway instances are operational and either the SaaS or cluster cache is restored. If cluster cache is operational, the Gateways will warm their caches from cluster cache and can then operate in a degraded "offline" mode for cached secrets and authentication, as described in the SaaS outage scenario.

Impact: Complete service interruption until at least one Gateway instance is restored and can access either the SaaS or a populated cluster cache (cluster cache).

## Will there be any behavioral changes based on the type of clients for example, Injector vs. ESO?

The core caching behavior and outage impact on the Gateway remain the same regardless of the client connecting to the Gateway. Both the Akeyless Injector and External Secrets Operator (ESO) interact with the Akeyless Gateway via HTTP calls to its REST API.

While both clients rely on the Gateway for secret retrieval, ESO's model of synchronizing secrets into Kubernetes Secret objects generally provides a higher degree of resilience for applications during Gateway or SaaS outages, as applications consume a local, replicated copy of the secret. The Injector, especially when injecting directly into files or environment variables, might lead to pod startup failures or stale secrets if an outage occurs during its secret injection phase and `AKEYLESS_CRASH_POD_ON_ERROR` is set.

## What are the Akeyless Gateway Cache deployment configuration options?

The different Gateway Cache configuration options related to caching are:

| Name                         | Description                                                                                              |
| :--------------------------- | :------------------------------------------------------------------------------------------------------- |
| `CACHE_ENABLE`               | Whether the cache is enabled                                                                             |
| `PROACTIVE_CACHE_ENABLE`     | Whether to enable proactive caching                                                                      |
| `NEW_PROACTIVE_CACHE_ENABLE` | Whether to use the new/more efficient proactive cache mechanism                                          |
| `PREFER_CLUSTER_CACHE_FIRST` | Whether to rely first on the cluster cache and then the local cache                                      |
| `CACHE_MAX_ITEMS`            | Control the maximum amount of proactive cache items. This will override the default value of 50K objects |
| `IGNORE_REDIS_HEALTH`        | `/health` check will ignore if Redis is down, and reply with `Health Check Ok` and `200 OK`              |

There are no differences between the `Kubernetes/Helm chart` options and the `VM-based/Docker` deployment methods. All configurations listed above can be used and function identically in both deployment types.\
Additional specific settings could be found in the Gateway k8s configuration page

## What's the behavior when caching is enabled and a user updates the secret in UI?

When a secret is updated in the UI, its value is immediately updated if accessed via the`get-secret-value` CLI command or API. In this scenario, the command will initially display the old value from the cache but will then sync with the SaaS to retrieve the new value. It will first update the local Gateway cache and then the Cluster cache.

If the flag `PREFER_CLUSTER_CACHE_FIRST` is enabled, the value will be fetched from the cluster cache first and not from the Gateway local cache. This option improves the ability of the system to provide the most updated value when there are several Gateway instances.

If the command is not executed, the cache will update after the proactive cache interval (e.g., 5 minutes) has elapsed. No user actions will be required for the secret’s updated values to be read in that case.

## When is the SaaS considered "down" for the purposes of validating/expiring tokens

The gateway continuously monitors its connection to the SaaS. If a connectivity check fails, it transitions into offline mode. In this state, while the SaaS remains unreachable, token validation and expiration are suspended. Cached tokens will remain valid regardless of their expiration time until the connection to the SaaS is restored.

## The Behavior of "Ignore Cache" in disconnected mode

By default, Akeyless Gateways cache secrets in memory to enhance performance and provide resiliency. This caching mechanism is crucial as it allows secrets to remain available even during network interruptions that lead to a disconnected (offline) mode. The `Ignore Cache` option is intended to force the Gateway to bypass its local cache and fetch a fresh version of the secret directly from the Akeyless SaaS platform. This ensures the client receives the most up-to-date value.\
However, this behavior is conditional on the Gateway's ability to communicate with the SaaS. In a disconnected mode, the Gateway's primary function is to maintain availability. Since there is no communication with the SaaS, the Gateway cannot fulfill a request for a fresh secret.\
Consequently, when the Gateway is disconnected:

* Even if a request is sent with the `Ignore Cache` flag enabled, the Gateway will first check its local cache.
* If the secret is found in the cache, it will be returned from the cache, as this is the only version available.
* If the secret is not in the cache, the request will fail because the Gateway cannot connect to the SaaS to retrieve it.
