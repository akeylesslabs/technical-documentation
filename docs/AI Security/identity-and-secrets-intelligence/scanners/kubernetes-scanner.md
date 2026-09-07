---
title: Kubernetes Scanner
deprecated: false
hidden: false
metadata:
  robots: index
---
# Kubernetes Scanner

The Kubernetes Scanner is a native scanner type that inspects a connected Kubernetes cluster, discovering the full inventory of identities (service accounts and their RBAC bindings) and secrets, including certificates, which Kubernetes stores as `kubernetes.io/tls`-typed Secrets rather than as a separate object type , along with the relationships between them. Each discovered object is evaluated against Identity & Secrets Intelligence security policies, which assess its risk posture and surface the resulting findings for review.

## Prerequisites

- An Akeyless account with the Identity & Secrets Intelligence license.
- A deployed and connected [Akeyless Gateway](doc:gateway-overview) version `5.1.0` and later.
- A Gateway with [Akeyless AI Insights](doc:akeyless-ai-insight) configured.
- A [Kubernetes Target](https://docs.akeyless.io/docs/kubernetes-targets) representing the service account that will scan the cluster.
- The credentials used by the Target granted the permissions listed under [Required Kubernetes Permissions](#required-kubernetes-permissions) below.
- Access to configure and run the scanner, granted via:
  1. "Manage ISI Scanners" or "Admin" [Gateway Permission](https://docs.akeyless.io/docs/gateway-access-permissions-reference).
  2. "Identity & Secrets Intelligence" [Administrative Rule](https://docs.akeyless.io/docs/rbac#administrative-rules) set to Scoped or All.
  3. "List" permission on the Kubernetes Target.

## Required Kubernetes Permissions

The credentials used by the Target need list-only access to your cluster's API resources. There are two ways to grant it:

- **Quick Setup** - bind a single predefined ClusterRole covering everything the scanner can use. Fastest to configure, but grants more access than a narrowly-scoped scan configuration strictly needs.
- **Granular Permissions** - bind only the specific list verbs your scan configuration needs, following the principle of least privilege.

Both produce a complete scan, the difference is privilege scope, not scan coverage.

### Quick Setup

Bind this ClusterRole to the scanner's service account. All access is **list-only**.

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: akeyless-isi-scanner
rules:
  - apiGroups: [""]
    resources: ["namespaces", "serviceaccounts", "secrets"]
    verbs: ["list"]
  - apiGroups: ["rbac.authorization.k8s.io"]
    resources: ["roles", "rolebindings", "clusterroles", "clusterrolebindings"]
    verbs: ["list"]
```

### Granular Permissions

All permissions below are **list-only**. The scanner never requires read, write, or exec access to your cluster, and never reads secret _values_, only metadata.

#### Required Permissions

Without these, the scan **fails** and no results are produced.

| Requirement                                                                                                                  | Used for                           | If missing                                                          |
| ---------------------------------------------------------------------------------------------------------------------------- | ---------------------------------- | ------------------------------------------------------------------- |
| Valid cluster credentials and a reachable API server (EKS, GKE, or native token)                                             | All scan types                     | Scan fails                                                          |
| `list` on `secrets` (cluster-wide), or `list` on `namespaces`, or an explicit namespace allow-list configured on the scanner | Secrets and certificates discovery | Secrets/certificates scan fails when none of the three is available |

#### Extended Visibility Permissions

Without these, the scan still **completes**, but with reduced visibility. Missing permissions are reported in the scan's _Access Status_ (visible in scan details).

| Permission (verb / resource)                    | API group                   | What it adds                                                                                                    |
| ----------------------------------------------- | --------------------------- | --------------------------------------------------------------------------------------------------------------- |
| `list namespaces`\*                             | core                        | Namespace discovery (enables per-namespace fallback when cluster-wide secret listing is restricted)             |
| `list secrets`                                  | core                        | Secrets and TLS certificates in each namespace                                                                  |
| `list serviceaccounts`                          | core                        | Identity discovery                                                                                              |
| `list roles`, `list rolebindings`               | `rbac.authorization.k8s.io` | Namespace-scoped access mapping                                                                                 |
| `list clusterroles`, `list clusterrolebindings` | `rbac.authorization.k8s.io` | Cluster-scoped access mapping (no namespace fallback — denying these blinds the whole RBAC graph for that kind) |

### Managed-Cluster Authentication

For clusters running on a managed Kubernetes service, the scanner's credentials also need cloud-level access to reach the cluster:

- EKS: The AWS IAM Role used by the Target needs sts:GetCallerIdentity andeks:DescribeCluster.
- GKE: The service account used by the Target needs a cloud-platform-scoped OAuth token.

**(need to validate this part)**

## Create a Kubernetes Scanner

1. Log in to the Akeyless Console, and go to **Products > Identity & Secrets Intelligence > Scanners**.
2. Click **New**, and select the scanner type **Kubernetes**, then click **Next**.
3. Define a **Name** for the scanner.
4. Select the **Target** representing the cluster to scan, and the **Gateway** that will execute the scans, then click **Next**.
5. Use the **Object Type** drop-down list to select the scanner's scope, and click **Finish**.

## Run a Scan

1. Log in to the Akeyless Console, and go to **Products > Identity & Secrets Intelligence > Scanners**.
2. Click the Kubernetes scanner.
3. Click **Start Scan**.

Once the scan completes, results appear in [Inventory](doc:identity-and-secrets-intelligence#inventory) for review.
