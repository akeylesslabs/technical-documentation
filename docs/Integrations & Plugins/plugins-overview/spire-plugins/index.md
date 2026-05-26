---
title: spire-plugins
excerpt: Overview
deprecated: false
hidden: false
metadata:
  title: ''
  description: ''
  robots: index
next:
  description: ''
---
The Secure Production Identity Framework for Everyone [(SPIFFE)](https://spiffe.io/docs/latest/spiffe-about/overview/) is a set of open-source standards for securely identifying software systems in dynamic and heterogeneous environments. Systems that adopt SPIFFE can easily and reliably mutually authenticate wherever they are running.

[SPIRE](https://spiffe.io/docs/latest/spire-about/) is a production-ready implementation of the SPIFFE APIs that performs node and workload [attestation](https://spiffe.io/docs/latest/spire-about/spire-concepts/#attestation) to securely issue [SPIFFE Verifiable Identity Documents (SVIDs)](https://spiffe.io/docs/latest/spiffe-about/spiffe-concepts/#spiffe-verifiable-identity-document-svid) to workloads, and verify the SVIDs of other workloads, based on a predefined set of conditions.

## When to Use Each Plugin

Use this page as a quick decision guide for selecting the correct plugin.

1. If SPIRE should use Akeyless to generate and manage signing keys for X.509-SVID and JWT-SVID, use [SPIRE Key Manager](https://docs.akeyless.io/docs/spire-keymanager).
2. If issued workload X.509-SVIDs should be stored in Akeyless, use [SPIRE Secret Manager](https://docs.akeyless.io/docs/spire-secret-manager).
3. If SPIRE Server should use Akeyless PKI issuer flows for upstream CA operations and JWT-SVID key publication, use [SPIRE Upstream Authority](https://docs.akeyless.io/docs/spire-upstream-authority).
4. If SPIRE Server should use a certificate item from Akeyless for upstream X.509 CA operations only, use [SPIRE Upstream Authority SM](https://docs.akeyless.io/docs/spire-upstream-authority-sm).

## Plugin Comparison

| Plugin | Primary Purpose | When to Choose It |
| --- | --- | --- |
| [SPIRE Key Manager](https://docs.akeyless.io/docs/spire-keymanager) | Generate, store, and manage SPIRE signing keys in Akeyless | Select this plugin when Akeyless should be the key management backend for SPIRE signing operations. |
| [SPIRE Secret Manager](https://docs.akeyless.io/docs/spire-secret-manager) | Store workload X.509-SVID material in Akeyless | Select this plugin when workload certificates should be persisted in Akeyless. |
| [SPIRE Upstream Authority](https://docs.akeyless.io/docs/spire-upstream-authority) | Integrate SPIRE upstream CA flows with Akeyless PKI issuer and JWT-SVID key publication | Select this plugin for full upstream authority coverage, including JWT-SVID related settings. |
| [SPIRE Upstream Authority SM](https://docs.akeyless.io/docs/spire-upstream-authority-sm) | Integrate SPIRE upstream X.509 CA flows using an Akeyless certificate item | Select this plugin when only certificate-item based upstream X.509 CA behavior is required. |
