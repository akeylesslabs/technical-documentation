---
title: Gateway Best Practices
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
This page provides recommended practices for the Akeyless Gateway across cloud and on-premises platforms.

## Recommended deployment path

Use this path for production deployments:

1. Prepare a trusted, dedicated runtime environment.
2. Create the Gateway authentication method and associated access role before deployment.
3. Deploy Gateway using the method that matches your platform.
4. Configure cluster naming, encryption, administrators, and observability before go-live.
5. Use explicit image or package versions mapped to GA releases, and validate upgrades in lower environments.

## Deployment model selection

Choose one deployment model based on your platform and operating model:

* Kubernetes with Helm: [Gateway on Kubernetes](https://docs.akeyless.io/docs/gateway-deploy-kubernetes-helm)
* Docker deployment: [Install and Configure the Gateway](https://docs.akeyless.io/docs/gateway-deploy-standalone-docker)
* Docker Compose deployment: [Gateway with Docker Compose](https://docs.akeyless.io/docs/gateway-deploy-docker-compose)
* Serverless deployment: [Serverless Gateway](https://docs.akeyless.io/docs/gateway-cloud-serverless-deployments)
* Azure Container Apps: [Gateway on Azure Container Apps](https://docs.akeyless.io/docs/gateway-deploy-azure-container-app)

## Environment and network requirements

* Deploy Gateway in a trusted, dedicated environment. A dedicated runtime reduces lateral movement risk from unrelated workloads.
* Restrict and audit access to the hosting environment, orchestration platform, and deployment pipelines.
* Allow outbound HTTPS (`443`) from Gateway to the required Akeyless SaaS endpoints, as documented in [Akeyless SaaS core service connectivity](https://docs.akeyless.io/docs/gateway-network-connectivity), [US SaaS Core Services](https://docs.akeyless.io/docs/akeyless-saas-core-services-us), and [EU SaaS Core Services](https://docs.akeyless.io/docs/akeyless-saas-core-services-eu).
* Expose inbound ports according to the selected deployment model. For most Gateway deployments, `8000` is used for internal client access, but exact ingress requirements can differ by runtime and feature set.
* Validate deployment-specific inbound port requirements in:
    * [Gateway on Kubernetes](https://docs.akeyless.io/docs/gateway-deploy-kubernetes-helm)
    * [Install and Configure the Gateway](https://docs.akeyless.io/docs/gateway-deploy-standalone-docker)
    * [Gateway with Docker Compose](https://docs.akeyless.io/docs/gateway-deploy-docker-compose)
    * [Gateway on Azure Container Apps](https://docs.akeyless.io/docs/gateway-deploy-azure-container-app)
* Configure TLS at the ingress or load balancer layer at minimum. End-to-end TLS is recommended for strict environments.
* Plan for additional egress requirements when connecting Gateway to private targets and integrations, including dynamic secrets, rotated secrets, Secure Remote Access (SRA), and certificate workflows.
* Additional ports can be required in future deployments based on runtime features and target integration patterns.

### Image and versioning guidance

* If direct pulls from external repositories are restricted, use the Gateway image from Docker Hub: [akeyless/gateway](https://hub.docker.com/r/akeyless/gateway).
* Use explicit image or package versions that match GA releases published in the [Akeyless changelog](https://changelog.akeyless.io/).
* The Gateway container image is compatible with non-root runtime policies, including OpenShift-style controls.
* Validate effective runtime user and group settings in your deployment policy. In Kubernetes, explicitly set `runAsNonRoot`, `runAsUser`, `runAsGroup`, and `fsGroup` according to your platform requirements.

## Platform-specific operational guidance

Apply these controls according to the selected platform:

* Kubernetes:
    * Set minimum resource requests of `1` vCPU and `2Gi` memory per pod.
    * Enable Horizontal Pod Autoscaler (HPA) and ensure Kubernetes Metrics Server is installed.
    * Manage chart values and lifecycle through GitOps workflows.
    * Set [resource requests and limits](https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/) for predictable scheduling and protection from noisy-neighbor workloads.
    * Use [PodDisruptionBudgets](https://kubernetes.io/docs/concepts/workloads/pods/disruptions/) to reduce downtime during voluntary disruptions.
    * Distribute pods with [pod anti-affinity](https://kubernetes.io/docs/concepts/scheduling-eviction/assign-pod-node/#affinity-and-anti-affinity) and [topology spread constraints](https://kubernetes.io/docs/concepts/scheduling-eviction/topology-spread-constraints/) for resilience.
    * Use [network policies](https://kubernetes.io/docs/concepts/services-networking/network-policies/) to restrict pod-to-pod traffic to required paths only.
    * Apply Kubernetes [RBAC](https://kubernetes.io/docs/reference/access-authn-authz/rbac/) and [service account](https://kubernetes.io/docs/concepts/security/service-accounts/) least privilege for Gateway workloads and automation.
* Virtual machines or bare metal:
    * Use host hardening baselines and restrict local administrative access.
    * Isolate Gateway runtime users and service credentials from other workloads.
* Serverless and managed containers:
    * Use workload identity where available instead of static long-lived secrets.
    * Enforce least-privilege egress and private networking controls.

## Pod scheduling for high availability (Kubernetes)

Akeyless recommends using Kubernetes [topology spread constraints](https://kubernetes.io/docs/concepts/scheduling-eviction/topology-spread-constraints/) and [pod anti-affinity](https://kubernetes.io/docs/concepts/scheduling-eviction/assign-pod-node/#affinity-and-anti-affinity) to improve availability when running multiple Gateway or Injector pods. Spreading pods across nodes and availability zones reduces the blast radius of node or zone failures.

Configuration details vary by cloud provider and cluster topology:

* [AWS: Amazon Elastic Kubernetes Service (EKS) reliability best practices](https://docs.aws.amazon.com/eks/latest/best-practices/reliability.html)
* [Azure: Azure Kubernetes Service (AKS) — configure availability zones](https://learn.microsoft.com/en-us/azure/aks/reliability-availability-zones-configure)
* [GCP: Google Kubernetes Engine (GKE) regional clusters](https://cloud.google.com/kubernetes-engine/docs/concepts/regional-clusters)
* [OCI: Oracle Kubernetes Engine (OKE) — node placement across availability domains and fault domains](https://docs.oracle.com/en-us/iaas/Content/ContEng/Tasks/create-cluster.htm)
* On-premises: consult your Kubernetes distribution documentation for zone and node topology configuration.

The following example shows a generic, platform-agnostic configuration for pod anti-affinity and topology spread constraints. For effective zone spread, set `replicaCount` to at least 3 — with fewer replicas, spread constraints may schedule unevenly across zones. The Gateway Helm chart requires `affinity.enabled: true` for `topologySpreadConstraints` to be applied. Replace `<release-name>` with your Helm release name:

```yaml values.yaml
gateway:
  deployment:
    replicaCount: 3

    affinity:
      enabled: true
      data:
        podAntiAffinity:
          preferredDuringSchedulingIgnoredDuringExecution:
            - weight: 100
              podAffinityTerm:
                labelSelector:
                  matchLabels:
                    app.kubernetes.io/name: akeyless-gateway
                    app.kubernetes.io/instance: <release-name>
                topologyKey: kubernetes.io/hostname

    topologySpreadConstraints:
      - maxSkew: 1
        topologyKey: topology.kubernetes.io/zone
        whenUnsatisfiable: ScheduleAnyway
        labelSelector:
          matchLabels:
            app.kubernetes.io/name: akeyless-gateway
            app.kubernetes.io/instance: <release-name>
      - maxSkew: 1
        topologyKey: kubernetes.io/hostname
        whenUnsatisfiable: ScheduleAnyway
        labelSelector:
          matchLabels:
            app.kubernetes.io/name: akeyless-gateway
            app.kubernetes.io/instance: <release-name>
```

For the complete set of scheduling values and chart options, see [Helm Values Reference](https://docs.akeyless.io/docs/gateway-kubernetes-helm-values-reference#pod-scheduling).

## Gateway application settings

* A Gateway cluster identity is defined by the combination of Gateway authentication method `Access ID` and `clusterName`.
* Changing either value creates a new logical Gateway cluster. Set a descriptive `clusterName` from day one.
* All instances in the same Gateway cluster are expected to share equivalent client-facing access and target-facing network reachability.
* Use a customer fragment for data fragment cryptography (DFC) and zero-knowledge workflows when required.
* Use HSM integration where hardware-backed key protection is required.
* Evaluate [Gateway cache](https://docs.akeyless.io/docs/gateway-caching) modes for continuity and latency requirements.
* Review advanced deployment options for your selected runtime before production rollout.

## Caching strategy considerations

Caching is optional and should be enabled based on business continuity, performance, and risk requirements.

* Consider enabling Gateway caching to improve resilience during temporary SaaS connectivity interruptions and to reduce latency for repeated reads.
* Consider enabling proactive cache when read performance and reduced first-read latency are priorities.
* For proactive cache, prefer the recommended implementation (`NEW_PROACTIVE_CACHE_ENABLE=true`) to get shared `429` backoff handling and leadership-cycle worker restart behavior.
* Consider cluster cache when running multiple Gateway instances that should share cache state.
* Evaluate security and operational tradeoffs before enabling caching:
    * Operational benefits: improved continuity, lower read latency, and reduced repeated upstream calls.
    * Operational costs: additional configuration, lifecycle management, monitoring, and capacity planning.
    * Security considerations: cache persistence policy, encryption controls, and data retention boundaries.
* Scope cache behavior to your environment and workload profile, then validate with telemetry and failure testing.

For implementation details and behavior, see:

* [Configure the Gateway Cache](https://docs.akeyless.io/docs/gateway-caching)
* [QA on Gateway Caching](https://docs.akeyless.io/docs/gateway-caching)

## Gateway authentication method

Gateway requires an identity to communicate with the Akeyless identity security platform for non-interactive operations, such as secret rotation and revocation workflows.

> ℹ️ **Note:**
>
> Gateway runtime identity does not override end-user RBAC. End-user permissions are evaluated independently.

### Cloud deployments

* For managed cloud platforms, prefer cloud-native IAM authentication.
* For Kubernetes deployments, follow the cloud IAM flow in [Gateway on Kubernetes](https://docs.akeyless.io/docs/gateway-deploy-kubernetes-helm), including provider-specific workload identity setup.
* In managed Kubernetes services, implementation details can differ when workload identities are enabled or disabled.
* Configure workload identity integration according to platform-specific guidance.

### On-premises deployments

For on-premises deployments, use one of the following methods:

* API key authentication:
    * Suitable for initial rollout and controlled environments.
    * Restrict client source networks with allowed IP ranges.
    * Set key expiry and automate rotation through operational workflows.
* Universal Identity:
    * Uses short-lived tokens and periodic rotation.
    * Configure TTL to balance resiliency and security.
    * Use a Redis-backed shared token flow across Gateway pods, with in-memory token handling for normal operation.
    * Keep token persistence enabled in each Gateway pod, and use persistent storage where possible to improve recovery after infrastructure failures.
    * If the token expires or is lost, restore the token and reset the Gateway identity flow. This can be automated.
    * Use persistent storage and automation to reduce manual recovery during infrastructure outages.
* Certificate-based authentication:
    * Store PEM certificate and private key in platform secrets storage.
    * Register the root certificate authority (CA) in the corresponding certificate auth method.
    * Use certificate claims to strengthen RBAC, and monitor certificate expiration and renewal.

## Gateway access role

* Associate the Gateway authentication method with a dedicated access role that grants least privilege.
* For audit forwarding use cases, configure audit permissions explicitly with the required scope (`own` or `all`).
* For centralized SIEM forwarding, set Audit Log permission to `all` on one dedicated log-forwarding Gateway deployment.
* For Universal Secrets Connector (USC):
    * Grant `read` access to the target used by USC.
    * If secret sync is enabled, grant `read` and `list` permissions to the relevant secret paths.

### Permission baseline by use case

For Gateway-specific permission semantics and operational scope guidance, see [Permission Scope Guidance](https://docs.akeyless.io/docs/gateway-authentication-and-access#permission-scope-guidance).

Use this matrix as a working baseline for permission planning. Keep scopes limited to required paths and targets per environment.

| Use case | Object type | Create | Read | Update | Delete | List | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Caching | Items |  | ✔️ |  |  | ✔️ | Read and list on cached paths only. |
| Dynamic or rotated secrets | Items |  | ✔️ | ✔️ |  | ✔️ | Required for rotation status and value updates. |
| Automatic migration | Items | ✔️ | ✔️ | ✔️ |  | ✔️ | Migration creates and updates destination items. |
| Caching | Access Roles |  |  |  |  | ✔️ | List only for role resolution. |
| Caching | Auth Methods |  |  |  |  | ✔️ | List only for auth method discovery. |
| Dynamic or rotated secrets | Targets |  | ✔️ | ✔️ |  | ✔️ | Read, update, and list on relevant targets only. |

Current guidance snapshots:

* Core Gateway identity:
    * Baseline permissions required for the deployed Gateway capabilities only.
    * Reference: [RBAC](https://docs.akeyless.io/docs/rbac)
* Audit forwarding Gateway:
    * Option 1: Use one dedicated forwarding Gateway with Audit Log permission scope `all`.
    * Option 2: Use multiple forwarding Gateways with scoped Audit Log permissions, where scopes are mutually exclusive.
    * References: [Log forwarding configuration](https://docs.akeyless.io/docs/gateway-log-forwarding), [Audit Logs](https://docs.akeyless.io/docs/audit-logs)
* USC-enabled Gateway:
    * `read` on the USC target and `read` or `list` on synced secret paths.
    * Reference: [Universal Secret Connector](https://docs.akeyless.io/docs/universal-secrets-connector)
* Gateway administrative users:
    * Assign only required Gateway access permissions per admin group.
    * Reference: [Gateway access permissions](https://docs.akeyless.io/docs/gateway-authentication-and-access)

## Gateway administrators

* Define a controlled list of human Access IDs (for example, SAML or OIDC) that can administer Gateway configuration.
* Configure administrator sub-claims and only the Gateway access permissions required for each admin group.
* Use separate admin groups for operations, security, and read-only review when possible.
* Review the permissions matrix in [Gateway access permissions](https://docs.akeyless.io/docs/gateway-authentication-and-access).

## Resource planning for Kubernetes proactive cache

These recommendations apply to Kubernetes deployments where Gateway proactive cache is enabled.

When Akeyless Kubernetes Secrets Injector is also deployed in the same cluster, plan Gateway and Injector capacity as separate workloads. For Injector-specific scaling guidance, see [Akeyless Kubernetes Secrets Injector](https://docs.akeyless.io/docs/akeyless-kubernetes-secrets-injector#scalability-guidance-for-gateway-and-injector).

> ℹ️ **Note (Scope):**
>
> The sizing guidance in this section is focused on secret retrieval, caching, and delivery workloads. Large-scale encryption and decryption workloads require separate capacity planning with higher CPU allocation.

For baseline Kubernetes controls, see [Platform-specific operational guidance](https://docs.akeyless.io/docs/gateway-best-practices#platform-specific-operational-guidance).

### Cache architecture and behavior

* Cluster cache allows Gateway pods to share cached data through Redis.
* Proactive cache pre-fetches and refreshes eligible secrets to reduce read latency.
* Startup and refresh behavior can temporarily increase CPU and memory consumption during warm-up windows.
* For detailed cache behavior and failure modes, see [QA on Gateway Caching](https://docs.akeyless.io/docs/gateway-caching).

### Kubernetes cache-related configuration

The following settings have direct resource impact in proactive cache environments:

* `PREFER_CLUSTER_CACHE_FIRST`: Prioritizes cluster cache over local in-memory cache.
* `CACHE_MAX_ITEMS`: Controls maximum number of proactive cache items in Gateway in-memory cache.
* `IGNORE_REDIS_HEALTH`: Keeps `/health` returning `200 OK` even when Redis is unavailable.

### Baseline sizing guidelines by item count

The following baselines were collected from real Kubernetes environments and should be used as a starting point. Adjust based on observed traffic, item size distribution, and growth rate.

Applicable baseline: Gateway `4.46.0` and later.

#### How to use the sizing baselines

Use the tables as directional capacity-planning input, not as guaranteed performance targets.

* Treat each row as an initial sizing profile, then validate in your own environment.
* Size for steady-state plus burst behavior, cache warm-up, and maintenance windows.
* Recalculate limits and replica count as item count and request rate grow.
* Validate with load testing before production rollout and after major configuration changes.

#### Gateway pod sizing

> ℹ️ **Note:**
>
> The values below are reference baselines, not SLA commitments. Workload shape, secret size distribution, and integration mix can change resource requirements.

| Items | Pods | CPU Limit | CPU Request | Memory Limit | Memory Request |
| --- | --- | --- | --- | --- | --- |
| 1K | 2 | 0.5 | 0.5 | 512Mi | 128Mi |
| 10K | 2-3 | 1.0 | 0.5 | 768Mi | 192Mi |
| 20K | 3 | 1.2 | 0.5 | 1Gi | 256Mi |
| 30K | 3-4 | 1.5 | 0.5 | 1Gi | 256Mi |
| 50K | 4 | 1.5 | 1.0 | 1.25Gi | 320Mi |
| 100K | 4-5 | 2.0 | 1.0 | 1.5Gi | 384Mi |
| 500K | 6-8 | 2.5 | 1.0 | 2.5Gi | 640Mi |
| 1M | 8-10 | 3.0 | 1.0 | 3.5Gi | 896Mi |
| 2M | 10-12 | 3.5 | 1.5 | 5Gi | 1.25Gi |

#### Cache pod sizing

> ℹ️ **Note:**
>
> Cache pod sizing depends on cached item characteristics, auth and RBAC matrix size, and active client footprint. Validate with runtime telemetry.

| Items | CPU Limit | CPU Request | Memory Limit | Memory Request |
| --- | --- | --- | --- | --- |
| 1K | 0.5 | 0.5 | 32Mi | 16Mi |
| 10K | 0.5 | 0.5 | 64Mi | 32Mi |
| 20K | 0.5 | 0.5 | 96Mi | 64Mi |
| 30K | 0.5 | 0.5 | 128Mi | 96Mi |
| 50K | 0.5 | 0.5 | 192Mi | 128Mi |
| 100K | 0.5 | 0.5 | 256Mi | 192Mi |
| 500K | 1.0 | 1.0 | 1Gi | 640Mi |
| 1M | 1.0 | 1.0 | 1.5Gi | 1Gi |
| 2M | 1.0 | 1.0 | 2.5Gi | 2Gi |

### Memory and CPU limit behavior

Use the following operational model when setting limits:

* Memory limits are enforced as hard limits. If container working-set memory exceeds the configured limit, Kubernetes can terminate the pod with `OOMKilled`. For behavior details, see [Resource Management for Pods and Containers](https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/).
* CPU limits do not terminate pods. When CPU usage exceeds the configured limit, Kubernetes throttles CPU allocation, which can increase request latency. For behavior details, see [Resource Management for Pods and Containers](https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/).
* For proactive cache environments, use an operational loop:
    1. Capture baseline memory and CPU during steady state and immediately after proactive warm-up.
    2. Alert on sustained memory growth, repeated CPU throttling, and pod restarts.
    3. If warm-up pressure is sustained, first reduce `PROACTIVE_CACHE_WORKERS` and increase `PROACTIVE_CACHE_MINIMUM_FETCHING_TIME`, then scale replicas or increase resource limits as needed.

### Operational recommendations

* Run at least 2 Gateway pods for availability. For most production environments with proactive cache, 3-4 pods is a practical baseline.
* Keep memory and CPU headroom above observed peaks to absorb cache warm-up, burst traffic, and maintenance operations.
* A practical starting buffer is 125%-150% of observed peak utilization.
* Set alerts before hard limits are reached:
    * 70% utilization: trend review and scaling plan.
    * 80% utilization: alert and capacity action window.
    * 90% utilization: immediate resource or replica increase.

### Key metrics to monitor for resource planning

In addition to the observability metrics listed below, monitor:

* Memory utilization against limits for Gateway and cache pods.
* OOMKill events and restart rates.
* CPU usage and throttling rates.
* Gateway request rates, response latency, and error trends.
* Cache growth trends correlated with item count growth.

For full monitoring guidance and alerting context, see [Gateway observability](https://docs.akeyless.io/docs/gateway-best-practices#gateway-observability).

For telemetry implementation details and metric export options, see:

* [Telemetry metrics on Kubernetes](https://docs.akeyless.io/docs/gateway-telemetry-and-metrics)
* [Telemetry metrics](https://docs.akeyless.io/docs/gateway-telemetry-and-metrics)

## Gateway observability

* Monitor Gateway and host or cluster health continuously.
* Consume Gateway metrics using [Kubernetes telemetry metrics](https://docs.akeyless.io/docs/gateway-telemetry-and-metrics) and [Telemetry metrics](https://docs.akeyless.io/docs/gateway-telemetry-and-metrics) for non-Kubernetes deployments.
* Prioritize baseline platform metrics documented in telemetry pages:
    * `akeyless.gw.system.cpu.*`
    * `akeyless.gw.system.memory.*`
    * `akeyless.gw.system.load.*`
    * `akeyless.gw.system.disk.*`
    * `akeyless.gw.system.network.*`
    * `akeyless.gw.system.saas.connection_status`
    * `akeyless.gw.system.healthcheck.status`
* Track connectivity and cache resilience behavior:
    * Alert on SaaS connectivity degradation (`akeyless.gw.system.saas.connection_status`).
    * Monitor cache continuity and offline-mode behavior as documented in [Configure the Gateway Cache](https://docs.akeyless.io/docs/gateway-caching).
* Monitor Gateway logs and forwarding health:
    * Collect standard output logs through the platform logging pipeline.
    * Configure [Log forwarding configuration](https://docs.akeyless.io/docs/gateway-log-forwarding) and [Audit Logs](https://docs.akeyless.io/docs/audit-logs) forwarding to your SIEM.
    * For larger environments, use either one dedicated Gateway with `all` audit scope, or multiple Gateways with mutually exclusive scoped audit permissions.
* Monitor control-plane and automation signals surfaced by Gateway runtime behavior:
    * Leader-only workflows: log forwarding runs only on the log-forwarding leader, and periodic security-health updates run only on the rotator leader.
    * Universal Secrets Connector (USC) sync status: alert on repeated sync failures and persistent USC `last error` updates.
    * Cache and Redis health: alert on repeated cache key provisioning failures and Redis-health-related state changes.
* Add account-level monitoring and alerting by integrating [Event Center](https://docs.akeyless.io/docs/event-center) notifications for failures, expirations, and operational drift.

## Industry-aligned security practices

In addition to Akeyless-specific settings, align deployment policy with common security standards:

* Enforce pod hardening and non-root controls for Kubernetes workloads using [Kubernetes Pod Security Standards](https://kubernetes.io/docs/concepts/security/pod-security-standards/).
* Apply guidance from the Cybersecurity and Infrastructure Security Agency (CISA) for Kubernetes and cloud-native hardening.
* Configure TLS policy and certificate operations using [OWASP Transport Layer Protection guidance](https://cheatsheetseries.owasp.org/cheatsheets/Transport_Layer_Protection_Cheat_Sheet.html).
