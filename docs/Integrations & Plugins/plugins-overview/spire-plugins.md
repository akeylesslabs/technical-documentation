---
title: SPIRE Plugins
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
The Secure Production Identity Framework for Everyone [(SPIFFE)](https://spiffe.io/docs/latest/spiffe-about/overview/) is a set of open-source standards for securely identifying software systems in dynamic and heterogeneous environments.  
Systems that adopt SPIFFE can easily and reliably mutually authenticate wherever they are running.

[SPIRE](https://spiffe.io/docs/latest/spire-about/) is a production-ready implementation of the SPIFFE APIs that performs node and workload [attestation](https://spiffe.io/docs/latest/spire-about/spire-concepts/#attestation) in order to securely issue [SVIDs](https://spiffe.io/docs/latest/spiffe-about/spiffe-concepts/#spiffe-verifiable-identity-document-svid) to workloads, and verify the SVIDs of other workloads, based on a predefined set of conditions.

Akeyless provides four plugins that can be used with SPIRE:

[SPIRE Key Manager](doc:spire-keymanager) plugin - responsible for generating, storing, and managing encryption keys inside Akeyless. Those private keys are being used to sign X.509-SVIDs and JWT-SVIDs

[SPIRE Secret Manager](doc:spire-secret-manager) plugin - stores workload X509-SVIDs inside Akeyless.

[SPIRE Upstream Authority](https://docs.akeyless.io/docs/spire-upstream-authority) plugin - Allows the SPIRE server to integrate with existing PKI systems, which means that it will be possible to use the Akeyless PKI Certificate Issuer in order to generate certificates.

[SPIRE Upstream Authority SM](https://docs.akeyless.io/docs/spire-upstream-authority-sm) plugin - Allows the SPIRE server to integrate with existing Secret Management systems, which means that it will be possible to use Akeyless as Certificate storage in order to generate certificates and maintain SPIRE Upstream Authority native plugin.