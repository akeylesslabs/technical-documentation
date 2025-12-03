---
title: Kubernetes Plugins
excerpt: ''
deprecated: false
hidden: false
metadata:
  title: ''
  description: ''
  robots: index
next:
  description: ''
  pages:
    - type: basic
      slug: how-to-provision-secret-to-your-k8s
      title: Akeyless K8s Secrets Injector
---
The Akeyless Kubernetes plugins enable containerized applications to use [Static](https://docs.akeyless.io/docs/static-secrets), [Dynamic](https://docs.akeyless.io/docs/how-to-create-dynamic-secret), and [Rotated](https://docs.akeyless.io/docs/rotated-secrets) secrets as well as [Certificates](https://docs.akeyless.io/docs/certificate-based-authentication) sourced from the Akeyless Platform.

The following plugins are available for Kubernetes:

* [Akeyless Kubernetes Secrets Injector](https://docs.akeyless.io/docs/how-to-provision-secret-to-your-k8s)
* [Kubernetes External Secret Operator (ESO)](https://docs.akeyless.io/docs/external-secret-operator)
* [Kubernetes Secrets Store Container Storage Interface (CSI)](https://docs.akeyless.io/docs/kubernetes-secrets-store-csi-provider)
* [Kubernetes Cert Manager](https://docs.akeyless.io/docs/kubernetes-cert-manager)

<Callout icon="📘" theme="info">
  _Note:_ The documentation, configuration and examples for Akeyless Kubernetes plugins are also applicable to Red Hat OpenShift environment.
</Callout>

## Feature Compatibility Matrix

Akeyless provides multiple ways to consume secrets from Kubernetes. The following matrix compares the most common integrations:

| Capability / Feature                            | External Secrets Operator (ESO)                       | Akeyless Kubernetes Secrets Injector                 | Akeyless Secrets Store CSI Provider                 | Cert Manager (Akeyless issuer)      |
| ----------------------------------------------- | ----------------------------------------------------- | ---------------------------------------------------- | --------------------------------------------------- | ----------------------------------- |
| Primary use case                                | Sync Akeyless secrets into **Kubernetes Secrets**     | Inject secrets directly into pods at runtime         | Mount secrets as **volumes** in pods                | Issue TLS certs from Akeyless       |
| Secret storage in Kubernetes                    | **Yes** (K8s Secret objects)                          | **No** (file/env in pod only)                        | **No** (mounted files only)                         | Only certificates as K8s secrets    |
| Secret injection method                         | Controller reconciles `ExternalSecret` CRDs           | Mutating Admission Webhook (init + optional sidecar) | CSI driver mounts secrets into container filesystem | Certificate issuance & renewal      |
| Supports Static / Rotated / Dynamic / Certs     | Static, Rotated, Dynamic, Certificates                | Static, Rotated, Dynamic, Certificates, USC          | Static, Rotated, Certificates                       | Certificates                        |
| Push secrets from K8s → Akeyless                | **Yes** (`PushSecret`)                                | No                                                   | No                                                  | No                                  |
| Auth methods (K8s, API Key, Azure AD, AWS, GCP) | Kubernetes Auth, API Key, Azure AD, AWS IAM, GCP      | Kubernetes Auth, API Key, Azure AD, AWS IAM, GCP     | Kubernetes Auth, API Key, Azure AD, AWS IAM, GCP    | Typically API Key / K8s / cloud IDs |
| Requires Akeyless Gateway                       | Required for K8s/Auth & some private deployments      | Yes (for K8s Auth and secure connectivity)           | Yes (for K8s Auth and secure connectivity)          | Yes                                 |
| Native JSON extraction / templating             | Yes (`dataFrom.extract`, templating support)          | No (app reads raw file/env values)                   | No                                                  | N/A                                 |
| Ideal for                                       | GitOps, configurations as code, multi-tenant clusters | App-centric injection with no K8s Secret persistence | File-based consumption, legacy apps expecting files | TLS for Ingress / services          |

### When to Choose Which

* **Use ESO** when you:
  * Want Kubernetes Secrets as first-class objects (for example, for existing Helm charts).
  * Need **PushSecret** capabilities from Kubernetes back to Akeyless.
  * Prefer a strong GitOps workflow with CRDs (`ExternalSecret`, `SecretStore`).

* **Use Akeyless Kubernetes Secrets Injector** when you:
  * Want secrets **only in pod memory / file system**, never stored as Kubernetes Secrets.
  * Need per-pod annotations and rollout restarts when secrets change.

* **Use Akeyless CSI Provider** when you:
  * Want secrets mounted as files without changing application code.
  * Prefer the Kubernetes CSI ecosystem for secret volumes.

* **Use Cert Manager + Akeyless** when you:
  * Need automatic TLS certificate issuance and renewal from Akeyless.

In many real-world deployments, teams combine these approaches (for example, ESO for app config and Cert Manager for TLS certificates).

## Tutorial

Check out our tutorial video on [Injecting Secrets into a Kubernetes Cluster](https://tutorials.akeyless.io/docs/injecting-secrets-into-a-kubernetes-cluster).
