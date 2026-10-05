---
title: Kubernetes Scanner
deprecated: false
hidden: false
metadata:
  robots: index
---
# Kubernetes Scanner

The Kubernetes Scanner is a native scanner type that inspects a connected Kubernetes cluster and discovers its identities, Secrets, and certificates, along with the relationships between them. It discovers ServiceAccounts and the `User` and `Group` subjects of RoleBindings and ClusterRoleBindings, together with the Roles and ClusterRoles bound to them, as well as Secrets and the certificates stored in Secrets of type `kubernetes.io/tls`. Each discovered object is evaluated against Identity & Secrets Intelligence security policies, which assess its risk posture and surface the resulting findings for review.

## What the Kubernetes Scanner Discovers

Each scanner covers one or more object types, selected when the scanner is created:

| Object Type      | What is discovered                                                                                                                             |
| ---------------- | ---------------------------------------------------------------------------------------------------------------------------------------------- |
| **Secrets**      | Kubernetes Secrets in every namespace the scanner can read, with their namespace, type, labels, annotations, and key names                     |
| **Certificates** | Certificates stored in `kubernetes.io/tls` Secrets, with their subject, issuer, serial number, and expiration date                             |
| **Identities**   | Service accounts, and the users and groups named in role bindings, with the Roles and ClusterRoles bound to them and the Secrets they can read |

## Prerequisites

- An Akeyless account with the Identity & Secrets Intelligence license.
- A deployed and connected [Akeyless Gateway](doc:gateway-overview) version `5.1.0` and later.
- A Gateway with [Akeyless AI Insights](doc:akeyless-ai-insight) configured.
- A [Kubernetes Target](https://docs.akeyless.io/docs/kubernetes-targets) representing the service account that will scan the cluster.
- The credentials used by the Target granted the permissions listed under [Required Kubernetes Permissions](#required-kubernetes-permissions) below.
- Access to configure and run the scanner, granted via:
  1. `Manage ISI Scanners `or `Admin` [Gateway Permission](https://docs.akeyless.io/docs/gateway-access-permissions-reference).
  2. `Identity & Secrets Intelligence` [Administrative Rule](https://docs.akeyless.io/docs/rbac#administrative-rules) set to `Scoped` or `All`.
  3. `List` permission on the Kubernetes Target.

## Required Kubernetes Permissions

The credentials used by the Target need `list` access to the Kubernetes resources behind each object type selected on the scanner. Every table in this section has an **Object Type** column, so you can grant only what the selected object types need.

There are two ways to grant it:

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

For each object type selected on the scanner, the ClusterRole grants `list` on the resources listed below:

| Object Type                       | Resources                                                                                       |
| --------------------------------- | ----------------------------------------------------------------------------------------------- |
| **Secrets**<br />**Certificates** | `namespaces`, `secrets`                                                                         |
| **Identities**                    | `namespaces`, `serviceaccounts`, `roles`, `rolebindings`, `clusterroles`, `clusterrolebindings` |

Create the ClusterRole below. Keep the rules for each object type you selected, and remove the others:

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: akeyless-isi-scanner
rules:
  # Secrets and Certificates
  - apiGroups: [""]
    resources: ["namespaces", "secrets"]
    verbs: ["list"]
  # Identities
  - apiGroups: [""]
    resources: ["namespaces", "serviceaccounts"]
    verbs: ["list"]
  - apiGroups: ["rbac.authorization.k8s.io"]
    resources: ["roles", "rolebindings", "clusterroles", "clusterrolebindings"]
    verbs: ["list"]
```

Then bind the ClusterRole, with a ClusterRoleBinding, to the identity the Target authenticates as:

| Target                                     | Bind the ClusterRole to                                                                                                                 |
| ------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------- |
| Generic Kubernetes, **Bearer Token**       | The service account the token belongs to                                                                                                |
| Generic Kubernetes, **Client Certificate** | The user named in the certificate's Common Name (CN)                                                                                    |
| Generic Kubernetes, **GW Service Account** | The Gateway's service account                                                                                                           |
| EKS                                        | The Kubernetes user or group mapped to the Target's IAM identity, see [Managed-Cluster Authentication](#managed-cluster-authentication) |
| GKE                                        | The Target's Google service account, see [Managed-Cluster Authentication](#managed-cluster-authentication)                              |

For example, to bind it to a service account:

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: akeyless-isi-scanner
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: akeyless-isi-scanner
subjects:
  - kind: ServiceAccount
    name: <service account name>
    namespace: <service account namespace>
```

To bind it to a user or a group, replace the subject with `kind: User` or `kind: Group`, its `name`, and `apiGroup: rbac.authorization.k8s.io`.

### Granular Permissions

All permissions below are **list-only**. The scanner never requires read, write, or exec access to your cluster, and never reads secret _values_, only metadata.

#### Required Permissions

The permissions listed below are required for the scan to complete successfully. If any one of them is missing, the corresponding scan will fail.

| Requirement                                                                                                                | Used for                           | If missing                                                          |
| -------------------------------------------------------------------------------------------------------------------------- | ---------------------------------- | ------------------------------------------------------------------- |
| Valid cluster credentials and a reachable API server (EKS, GKE)                                                            | All scan types                     | Scan fails                                                          |
| `list` on `secrets` cluster-wide, or `list` on `namespaces`, or an explicit namespace allow-list configured on the scanner | Secrets and certificates discovery | Secrets/certificates scan fails when none of the three is available |

#### Additional Permissions for Complete Coverage

These permissions are optional. If missing, the scan still completes, but with reduced visibility, and any gaps are reported in the Access Status field within the scan details.

| Permission (verb / resource)                    | API group                   | What it adds                                                                                                    |
| ----------------------------------------------- | --------------------------- | --------------------------------------------------------------------------------------------------------------- |
| `list namespaces`\*                             | core                        | Namespace discovery (enables per-namespace fallback when cluster-wide secret listing is restricted)             |
| `list secrets`                                  | core                        | Secrets and TLS certificates in each namespace                                                                  |
| `list serviceaccounts`                          | core                        | Identity discovery                                                                                              |
| `list roles`, `list rolebindings`               | `rbac.authorization.k8s.io` | Namespace-scoped access mapping                                                                                 |
| `list clusterroles`, `list clusterrolebindings` | `rbac.authorization.k8s.io` | Cluster-scoped access mapping (no namespace fallback - denying these blinds the whole RBAC graph for that kind) |

### Managed-Cluster Authentication

For clusters running on a managed Kubernetes service, the scanner's credentials also need cloud-level access to reach the cluster:

- EKS: The AWS IAM Role used by the Target needs `sts:GetCallerIdentity` and `eks:DescribeCluster`.

## Create a Kubernetes Scanner

1. Log in to the Akeyless Console, and go to **Products > Identity & Secrets Intelligence > Scanners**.
2. Click **New**, and select the scanner type **Kubernetes**, then click **Next**.
3. Define a **Name** for the scanner.
4. Select the **Gateway** that will execute the scans, and the **Target** representing the cluster to scan, then click **Next**.
5. Use the **Object Type** drop-down list to select the scanner's scope, and click **Finish**.

## Run a Scan

1. Log in to the Akeyless Console, and go to **Products > Identity & Secrets Intelligence > Scanners**.
2. Click the Kubernetes scanner.
3. Click **Start Scan**.

Once the scan completes, results appear in **Inventory** for review.
