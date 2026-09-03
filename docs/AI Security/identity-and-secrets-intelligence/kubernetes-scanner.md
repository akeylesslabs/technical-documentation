---
title: Kubernetes Scanner
excerpt: Setup & Required Permissions
deprecated: false
hidden: false
metadata:
  robots: index
---
# Quick Setup

Bind the ClusterRole below to the scanner's service account. All access is `list`-only.

All permissions below are **read-only**. The scanner never requires write access to your cluster, and never reads secret _values_ — only metadata.

***

## Must-Have Permissions

Without these, the scan **fails** and no results are produced.

| Requirement                                                                                                                          | Used for                           | If missing                                                          |
| ------------------------------------------------------------------------------------------------------------------------------------ | ---------------------------------- | ------------------------------------------------------------------- |
| Valid cluster credentials and a reachable API server (EKS, GKE, or native token)                                                     | All scan types                     | Scan fails                                                          |
| `list` on `secrets` (cluster-wide), **or** `list` on `namespaces`, **or** an explicit namespace allow-list configured on the scanner | Secrets and certificates discovery | Secrets/certificates scan fails when none of the three is available |

***

## Additional Permissions for a Full Scan

Without these, the scan still **completes**, but with reduced visibility. Missing permissions are reported in the scan's _Access Status_ (visible in scan details).

| Permission (verb / resource)                 | API group                 | What it adds                                                                                                    |
| -------------------------------------------- | ------------------------- | --------------------------------------------------------------------------------------------------------------- |
| `list` `namespaces`                          | core                      | Namespace discovery (enables per-namespace fallback when cluster-wide secret listing is restricted)             |
| `list` `secrets`                             | core                      | Secrets and TLS certificates in each namespace                                                                  |
| `list` `serviceaccounts`                     | core                      | Identity discovery                                                                                              |
| `list` `roles`, `rolebindings`               | rbac.authorization.k8s.io | Namespace-scoped access mapping                                                                                 |
| `list` `clusterroles`, `clusterrolebindings` | rbac.authorization.k8s.io | Cluster-scoped access mapping (no namespace fallback — denying these blinds the whole RBAC graph for that kind) |

***

## Reference ClusterRole

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: akeyless-sdr-scanner
rules:
  - apiGroups: [""]
    resources: ["namespaces", "serviceaccounts", "secrets"]
    verbs: ["list"]
  - apiGroups: ["rbac.authorization.k8s.io"]
    resources: ["roles", "rolebindings", "clusterroles", "clusterrolebindings"]
    verbs: ["list"]
```

***

## Managed-Cluster Authentication

- **EKS:** the AWS credential needs `sts:GetCallerIdentity`, plus `eks:DescribeCluster` unless the cluster endpoint and CA certificate are supplied explicitly in the scanner settings.
- **GKE:** the GCP credential needs a `cloud-platform`-scoped OAuth token; the cluster endpoint and CA certificate must be supplied in the scanner settings.

***

## Scope Note

Replacing the ClusterRole secret rule with namespace-scoped Roles limits discovery to those namespaces — anything out of scope is simply reported as a gap in the Access Status.
