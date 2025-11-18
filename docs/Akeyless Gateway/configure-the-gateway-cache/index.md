---
title: Gateway Cache
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

> 👍 Offline Authentication Cache
>
> Offline authentication cache is only supported in [Cluster Cache](https://docs.akeyless.io/docs/configure-the-gateway-cache#cluster-cache-mode) mode and requires the user being authenticated to have at least list permission on the relevant Authentication Method.

The most straightforward use cases are the following:

* The Gateway Cache is used to improve performance when fetching secrets.

* The Proactive Cache enables storing secrets in the Gateway Cache in advance upon successful user authentication.

The Gateway cache utilizes two primary types of caches: a **Local In-Memory Cache** for individual Gateway instances and a **Cluster Cache** for high availability in Kubernetes environments. This architecture ensures that secrets are readily available to applications while minimizing the load on the Akeyless SaaS platform.

In a high-availability configuration, secrets are stored in a **Cluster Cache**, typically backed by an internal database instance. This shared cache ensures every pod has a consistent view of the cached data. This model is crucial for resilience, as it allows the Gateway to continue serving cached secrets even during a complete Akeyless SaaS outage. Authentication can also persist during an outage for methods that can be validated locally, such as Kubernetes Service Account authentication, where the Gateway can verify the token against the cluster's K8s API server without needing to contact the SaaS.

# Gateway Cache

To enable and configure the Gateway Cache:

1. Open the **Akeyless Gateway Configuration Manager** at `https://Your_Akeyless_Gateway_URL:8000/console`.

2. On the menu bar at the left, click **Gateways > Your-Gateway > Manage Gateway > Caching Configuration**.

3. Select the **Enable Caching** checkbox.

4. Set the **Stale Timeout**  value. This is the time (in minutes) during which a secret should be kept in the cache. The secret is deleted from the cache at the end of this period. By default, cached secrets will expire after 60 minutes.

5. Click **Save Changes**.

> 👍 Note
>
> Usually, after the Stale Timeout period expires for a secret, the secret is deleted from the Gateway Cache.
>
> In case there is no internet connection, the Gateway Cache won’t delete old items until the internet connection is restored.

# Proactive Gateway Cache

The Proactive Cache fetches all secrets from the Akeyless Cloud and stores them in the Gateway Cache upon successful authentication (based on the user access policy). To manage each user's access policy, the [Gateway's default Auth Method ](https://docs.akeyless.io/docs/gateway-k8s#authentication) must have **List** permissions for **Auth-Methods** and **Roles**, as well as **Read** permission for the secret intended to be saved in the cache.

The Gateway utilizes a proactive caching model with a delta-based update process to avoid the resource-intensive task of re-fetching all secrets periodically. This is managed by two parallel background processes:

* **Refresh-TTL Ticker** : This process runs at a configurable interval (by default every 5 minutes) and queries the Akeyless SaaS platform only for secrets that have been modified within that time window. By checking just for the delta of updated secrets, the Gateway significantly reduces the overhead of keeping the cache synchronized.
* **Cleanup-TTL Ticker:** This independent process periodically compares the cache with the SaaS to remove entries for secrets that have been deleted or for which the Gateway's access permissions have been revoked.

This dual-ticker system ensures the cache remains fresh and accurate with minimal performance impact. When a user updates a secret in the Akeyless UI, the change is picked up by the next refresh cycle, and the updated value is propagated to the cache and subsequently to the workload without requiring any manual intervention. This provides a highly efficient and scalable solution for secrets management.

The following diagram illustrates the key phases of the Akeyless Gateway's proactive caching mechanism, showing how it efficiently populates and maintains its cache, and how an application consumes secrets from it.
In this example, the user set the Refresh-TTL Ticker to 2 minutes.

<Image align="center" border={false} src="https://files.readme.io/1fdc1d01ea89e625913853199b7ed1aba17bdebdd713ce3b708af7c1fa9b2e77-Cache_Diagaram.png" />

To enable and configure the Proactive Cache:

1. Open the **Akeyless Gateway Configuration Manager** at `https://Your_Akeyless_Gateway_URL:8000/console`.

2. On the menu bar at the left, click **Gateways > Your-Gateway > Manage Gateway > Caching Configuration**.

3. Select the **Enable Proactive Caching** checkbox.

> 🚧 Using Legacy Mode
>
> Once you disable **Legacy Mode**, you won't be able to re-enable it.

4. Set the **Refresh TTL** value. This setting instructs the system to update secrets in the cache if they are older than the specified value. By default, each secret kept in the cache for more than 5 minutes will be re-requested from the Akeyless Cloud or the local Gateway.
5. Set the **Cleanup TTL** value.  Compares the cache with the SaaS to remove entries for secrets that have been deleted or for which the Gateway's access permissions have been revoked.
6. Click **Save Changes**.

# Cluster Cache Mode

When deploying Gateway on K8s, a Cluster Cache can be set in addition to support offline authentication, this results in an additional service that syncs all pods and has a shared storage, to keep the secrets encrypted at rest, this mode requires a K8s encryption key. This feature can be set **only** during deployment.  To set this follow the installation guide under the [cache](https://docs.akeyless.io/docs/advanced-k8s-gateway-configuration#cache-configuration) section.

# Bypass Cache

When Cache is enabled by default, any client that requests a secret from the relevant Gateway will receive the latest cached value of the secret. To work directly with the Akeyless SaaS, to ensure you are retrieving the latest value of the secret, you can specify the `ignore-cache`  setting as part of the request to by-pass the cache mechanism :

```shell Akeyless CLI
akeyless get-secret-value -n /mysecret --ignore-cache true
```
