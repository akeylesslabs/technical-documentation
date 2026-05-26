---
title: kubernetes-plugins
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
      slug: akeyless-kubernetes-secrets-injector
      title: Akeyless Kubernetes Secrets Injector
---
The Akeyless Kubernetes plugins enable containerized applications to use [Static](https://docs.akeyless.io/docs/static-secrets), [Dynamic](https://docs.akeyless.io/docs/how-to-create-dynamic-secret), and [Rotated](https://docs.akeyless.io/docs/rotated-secrets) secrets as well as [Certificates](https://docs.akeyless.io/docs/auth-with-certificate) sourced from the Akeyless Platform.

The following plugins are available for Kubernetes:

* [Akeyless Kubernetes Secrets Injector](https://docs.akeyless.io/docs/akeyless-kubernetes-secrets-injector)
* [Kubernetes External Secret Operator (ESO)](https://docs.akeyless.io/docs/external-secrets-operator)
* [Kubernetes Secrets Store Container Storage Interface (CSI)](https://docs.akeyless.io/docs/kubernetes-secrets-store-csi-provider)
* [Kubernetes Cert Manager](https://docs.akeyless.io/docs/cert-manager)

> ℹ️ **Note:** The documentation, configuration, and examples for Akeyless Kubernetes plugins are also applicable to Red Hat OpenShift environments.

## Feature Compatibility Matrix

Akeyless provides multiple ways to consume secrets from Kubernetes. The following matrix compares the most common integrations:

| Capability / Feature | External Secrets Operator (ESO) | Akeyless Kubernetes Secrets Injector | Akeyless Secrets Store CSI Provider | Cert Manager (Akeyless issuer) |
| --- | --- | --- | --- | --- |
| _Primary use case_ | Sync Akeyless secrets into Kubernetes Secrets | Inject secrets directly into pods at runtime | Mount secrets as volumes in pods | Issue TLS certs from Akeyless |
| _Secret storage in Kubernetes_ | Yes (Kubernetes Secret objects) | No (file/env in pod only) | No (mounted files only) | Partial (only certificates as Kubernetes secrets) |
| _Secret injection method_ | Controller reconciles `ExternalSecret` CRDs | Mutating Admission Webhook (init and optional sidecar) | CSI driver mounts secrets into container filesystem | Certificate issuance and renewal |
| _Supported Secret Types_ | Static, Rotated, Dynamic, Certificates | Static, Rotated, Dynamic, Certificates, USC | Static, Rotated, Certificates | Certificates |
| _Push secrets from Kubernetes to Akeyless_ | Yes (`PushSecret`) | No | No | No |
| _Native JSON extraction and templating_ | Yes (`dataFrom.extract`, templating support) | No (app reads raw file/env values) | No | N/A |
| Ideal for | GitOps, configurations as code, multi-tenant clusters | App-centric injection with no Kubernetes Secret persistence | File-based consumption, legacy apps expecting files | TLS for Ingress and Service objects |

## Tutorial

Check out our tutorial video on [Injecting Secrets into a Kubernetes Cluster](https://tutorials.akeyless.io/docs/injecting-secrets-into-a-kubernetes-cluster).
