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

Set the subject to the identity the Target authenticates as:

- **Bearer Token**: the ServiceAccount the token belongs to.
- **Client Certificate**: a `User` subject named after the certificate's Common Name (CN), with `apiGroup: rbac.authorization.k8s.io`.
- **GW Service Account**: the Gateway's ServiceAccount.
- **EKS** and **GKE**: see [Managed-Cluster Authentication](#managed-cluster-authentication).&#x20;

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

All permissions below are **list-only**. The scanner never requires read or write access to your cluster, and never reads secret _values_, only metadata.

#### Required Permissions

The permissions listed below are required for the scan to complete successfully. If one is missing for an object type selected on the scanner, the scan fails, in the cases described below:

| Requirement                                                                                                                | Used for                           | If missing                                                          |
| -------------------------------------------------------------------------------------------------------------------------- | ---------------------------------- | ------------------------------------------------------------------- |
| Valid cluster credentials and a reachable API server (EKS, GKE)                                                            | All scan types                     | Scan fails                                                          |
| `list` on `secrets` cluster-wide, or `list` on `namespaces`, or an explicit namespace allow-list configured on the scanner | Secrets and certificates discovery | Secrets/certificates scan fails when none of the three is available |

| Object Type                                           | Used for                                                                        | Permission                                          | If missing                                                                       |
| ----------------------------------------------------- | ------------------------------------------------------------------------------- | --------------------------------------------------- | -------------------------------------------------------------------------------- |
| **Secrets**<br />**Certificates**<br />**Identities** | Connecting to the cluster                                                       | Valid Target credentials and a reachable API server | The scan fails                                                                   |
| **Secrets**<br />**Certificates**                     | Discovering Secrets, and the certificates stored in `kubernetes.io/tls` Secrets | `list secrets`, cluster-wide                        | The scan fails if `list namespaces` is also missing; otherwise reported as a gap |

If `list secrets` is granted only in some namespaces, the scanner reads Secrets namespace by namespace, and each namespace it can't read is reported as a gap.&#x20;

#### Additional Permissions for Complete Coverage

These permissions are optional. If missing, the scan still completes, but with reduced visibility, and the policies that depend on them are not evaluated.

| Object Type                                           | Permission                                      | What it adds                                                                                              |
| ----------------------------------------------------- | ----------------------------------------------- | --------------------------------------------------------------------------------------------------------- |
| **Secrets**<br />**Certificates**<br />**Identities** | `list namespaces`                               | Namespace discovery, so the scanner can read each namespace separately when a cluster-wide list is denied |
| **Identities**                                        | `list serviceaccounts`                          | Service accounts                                                                                          |
| **Identities**                                        | `list roles`, `list rolebindings`               | Access granted within a namespace                                                                         |
| **Identities**                                        | `list clusterroles`, `list clusterrolebindings` | Access granted across the cluster. These have no per-namespace fallback                                   |

Each gap entry names the skipped resource, the namespaces it affects, and the missing RBAC permission.

### Managed-Cluster Authentication

For clusters running on a managed Kubernetes service, the scanner's credentials also need cloud-level access to reach the cluster:

- EKS: The AWS IAM Role used by the Target needs `sts:GetCallerIdentity` and `eks:DescribeCluster`.

For EKS and GKE clusters, the Target's cloud identity must also be allowed into the cluster:

- **EKS**: no AWS IAM permissions are required. Map the IAM identity the Target uses to a Kubernetes user or group with an [EKS access entry](https://docs.aws.amazon.com/eks/latest/userguide/access-entries.html), or with the `aws-auth` ConfigMap, and bind the ClusterRole to that user or group.
- **GKE**: grant the Target's Google service account the `container.clusters.get` IAM permission on the cluster's project, for example through the `roles/container.clusterViewer` role. Bind the ClusterRole to the service account's unique ID, not its email.

When **Use Gateway's Cloud Identity** is selected on the Target, these apply to the Gateway's IAM identity or Google service account instead.

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
