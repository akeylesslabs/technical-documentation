---
title: ESO and AKS Workload Identity
excerpt: 'Using AKS Workload Identity with `accessType: azure_ad`'
deprecated: false
hidden: true
link:
  new_tab: false
metadata:
  robots: index
---
This guide explains how the Akeyless External Secrets Operator (ESO) integrates with **Azure AD Workload Identity** on AKS, how authentication works when using `accessType: azure_ad` and what configuration is required both in Kubernetes and Azure.

Unlike the Azure Key Vault ESO provider, the Akeyless provider does not require or expose any dedicated value such as `authType: WorkloadIdentity`.

Instead, it relies entirely on the **native Azure Workload Identity token exchange flow** handled by AKS and Microsoft Entra ID.

## How the Akeyless ESO Provider Uses Workload Identity

When `accessType: azure_ad` is used, ESO does **not** fetch or exchange Azure tokens itself.  
Azure’s Workload Identity system automatically mounts a projected OIDC token into any pod running under a `ServiceAccount` that is federated with an Azure Managed Identity or Service Principal.

ESO:

1. Runs under a Kubernetes `ServiceAccount`
2. Receives the projected OIDC token for that `ServiceAccount`
3. Has Azure’s Workload Identity webhook exchange that token for an Azure AD access token
4. Sends that Azure token to Akeyless to authenticate to an Azure AD Auth Method

**ESO never performs Azure token exchange internally.** It only uses the token provided by the pod’s environment.

***

## What Makes Workload Identity Work With Akeyless

When an Azure AD Auth Method is configured in Akeyless, it validates Azure tokens based on:

* Issuer (`https://sts.windows.net/<tenant-id>/`)
* JWKS validation via the Microsoft discovery endpoint
* Tenant ID
* Optional sub‑claims such as:
  * `xms_mirid` (Managed Identity resource ID)
  * `oid` (Azure object ID for MI / SPN / user accounts)

This enables very fine-grained identity binding between AKS workloads and Akeyless roles.

***

## Required Components

### 1. Kubernetes `ServiceAccount` With Workload Identity Annotation

This `ServiceAccount` determines _which_ Managed Identity ESO will use.

```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: eso-akeyless-sa
  namespace: akeyless-demo
  annotations:
    azure.workload.identity/client-id: "<UAMI-client-id>"
```

### 2. Azure Federated Identity Credential

In Azure, the federated credential must trust:

* The AKS OIDC issuer
* The exact ServiceAccount identity:
  * `system:serviceaccount:<namespace>:<sa-name>`

This is what enables Azure to issue the correct identity token to ESO.

### 3. Akeyless Azure AD Auth Method

You must configure an Azure AD Auth Method in Akeyless using:

* Your Azure tenant
* JWKS endpoint
* Optional sub-claims for identity restrictions

Akeyless will provide an **Access ID** (e.g. `p-xxxxx`).

***

## Minimal Authentication Configuration in Kubernetes

### Credentials Secret for ESO

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: akeyless-azure-creds
  namespace: akeyless-demo
type: Opaque
stringData:
  accessId: "p-xxxxx"
  accessType: "azure_ad"
  accessTypeParam: ""   # optional when using sub‑claims
```

### SecretStore Using Azure AD

```yaml
apiVersion: external-secrets.io/v1
kind: SecretStore
metadata:
  name: akeyless-store
  namespace: akeyless-demo
spec:
  provider:
    akeyless:
      akeylessGWApiURL: "https://api.akeyless.io"
      authSecretRef:
        secretRef:
          accessID:
            name: akeyless-azure-creds
            key: accessId
          accessType:
            name: akeyless-azure-creds
            key: accessType
          accessTypeParam:
            name: akeyless-azure-creds
            key: accessTypeParam
```

**Important:**  
Do **not** use `serviceAccountRef` in the SecretStore when using `accessType: azure_ad`.  
Identity selection happens only through the `ServiceAccount` set on the `ExternalSecret`.

***

## Running ExternalSecrets Under the Right Identity

To ensure ESO uses the correct Managed Identity, you must specify which ServiceAccount executes each ExternalSecret.

```yaml
apiVersion: external-secrets.io/v1
kind: ExternalSecret
metadata:
  name: my-secret
  namespace: akeyless-demo
spec:
  serviceAccountName: eso-akeyless-sa
  secretStoreRef:
    kind: SecretStore
    name: akeyless-store
  target:
    name: my-secret
  data:
    - secretKey: api-key
      remoteRef:
        key: /app/api-key
```

The identity used to authenticate to Akeyless will be the **Managed Identity** associated with `eso-akeyless-sa`.

***

## Using Sub‑Claims for Identity Enforcement

Akeyless Azure AD Auth Methods may require sub‑claims to match. Example:

```json
{
  "auth_method_sub_claims": {
    "xms_mirid": [
      "/subscriptions/.../resourcegroups/.../providers/Microsoft.ManagedIdentity/userAssignedIdentities/my-identity"
    ]
  }
}
```

This ensures only workloads using the specific Managed Identity are allowed to access secrets.

***

## Troubleshooting Workload Identity

To verify that the pod is receiving the correct Azure AD identity token:

1. Enter a pod running under the same ServiceAccount as your ExternalSecret:
   * `kubectl exec -it <pod> -- sh`
2. Run: `akeyless get-cloud-identity`

Expected result:

* Output includes the correct `xms_mirid` or `oid` matching your Managed Identity.

If it fails:

* The pod is not being issued a correct Azure token.
* Re-check:
  * Federated credential settings
  * ServiceAccount annotations
  * AKS OIDC issuer
  * Namespace/name used in federation

***

## Summary

* ESO fully supports AKS Workload Identity using `accessType: azure_ad`.
* ESO does not implement Azure token exchange; it consumes the identity projected by the pod's environment.
* `serviceAccountName` on `ExternalSecret` determines which identity is used.
* `serviceAccountRef` in the SecretStore is **not** used for Azure AD auth.
* Identity restrictions are enforced through Akeyless sub-claims.

***

If you'd like, I can also generate a version with diagrams or add ready-to-copy YAML bundles.
