---
title: ESO and AKS Workload Identity
excerpt: 'Using AKS Workload Identity with `accessType: azure_ad`'
deprecated: false
hidden: false
metadata:
  robots: index
---
This page explains how the Akeyless ESO provider works with **Azure AD Workload Identity** on AKS, and clarifies how ESO obtains Azure tokens when configured with:

```yaml
accessType: azure_ad
```

Unlike the Azure Key Vault ESO provider, the Akeyless provider does **not** use a dedicated field such as:

```yaml
authType: WorkloadIdentity
```

Instead, it relies on Azure’s **native workload identity token flow**, which is handled transparently by AKS and Microsoft’s token exchange system.

***

## Does the Akeyless ESO Provider Support AKS Workload Identity?

**Yes.**  
When using `accessType: azure_ad`, the ESO controller pod uses Azure’s native MSI / federated identity system to obtain an Azure AD token. This works automatically when the ESO pod is bound to an AKS Workload Identity.

Akeyless validates the resulting Azure token using:

* **Issuer**
* **Tenant ID**
* **JWKS**
* **Sub‑claims** (`xms_mirid`, `oid`, etc.)

No special ESO provider fields are required beyond the normal Azure AD authentication parameters.

***

## How ESO Obtains an Azure AD Token Under Workload Identity

When AKS Workload Identity is configured for a Kubernetes ServiceAccount, Kubernetes automatically mounts a **projected OIDC token** into pods using that SA.

Token acquisition process:

1. The ESO controller (or namespace‑scoped ESO pod) runs under a **ServiceAccount bound to a Federated Identity** in Azure.
2. Kubernetes injects a **projected OIDC token** for that ServiceAccount.
3. The Azure workload identity webhook exchanges that token for an Azure AD access token associated with the Managed Identity or Service Principal.
4. ESO uses that Azure token to authenticate against the Akeyless Azure AD Auth Method.

This flow is automatic and requires **no custom logic in the Akeyless ESO provider**.

***

## Required Configuration

### 1. Annotate the Kubernetes ServiceAccount

```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: eso-sa
  namespace: akeyless-demo
  annotations:
    azure.workload.identity/client-id: "<UAMI-or-SPN-client-id>"
```

### 2. Ensure Azure Federated Identity Trust Is Configured

Your Azure Federated Identity Credential must trust:

* Your AKS OIDC issuer
* The ESO ServiceAccount identity (`system:serviceaccount:<namespace>:<name>`)

### 3. Use Normal `azure_ad` Credentials in SecretStore

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
  accessTypeParam: ""   # optional when using sub-claims such as xms_mirid
```

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

***

## What You _Do Not_ Need

* **No `serviceAccountRef`**  
  → Only used by the _Kubernetes Auth_ method (`accessType: k8s`).

* **No custom workload identity field**  
  → Akeyless provider does not require an `authType: WorkloadIdentity` block.

* **No manual Azure token fetching**  
  → Token acquisition is automatically handled by the Azure workload identity webhook.

***

## Akeyless Authorization with Sub‑Claims

Azure AD-issued tokens may include the following claims:

* `xms_mirid` — Managed Identity resource ID
* `oid` — Azure AD Object ID

These can be used in Akeyless role associations, for example:

```json
"auth_method_sub_claims": {
  "xms_mirid": [
    "/subscriptions/.../userAssignedIdentities/my-uami"
  ]
}
```

This ensures only workloads using the correct Managed Identity can access secrets.

***

## Summary

| Question                                                   | Answer                                       |
| ---------------------------------------------------------- | -------------------------------------------- |
| Does Akeyless ESO support AKS Workload Identity?           | **Yes**                                      |
| Is a special ESO provider field required?                  | **No**                                       |
| Does ESO automatically use the pod’s projected OIDC token? | **Yes**                                      |
| Should `serviceAccountRef` be used for Azure AD auth?      | **No**                                       |
| How is access restricted?                                  | Via Akeyless sub‑claims (`xms_mirid`, `oid`) |

***

If you'd like, I can also produce a **diagram**, **inline example in the main docs**, or **matching troubleshooting section**.
