---
title: FedRAMP Feature Availability
deprecated: false
hidden: true
metadata:
  robots: index
---
Differences between the commercial and FedRAMP environments.

The FedRAMP environment is based on the same core technology as the commercial environment. Secrets, certificates, and key management are available. The differences below come from hosting inside the FedRAMP boundary.

## Comparison

| Dimension         | Commercial                              | FedRAMP                                                                                                               |
| ----------------- | --------------------------------------- | --------------------------------------------------------------------------------------------------------------------- |
| Regions           | US, EU, Azure US                        | AWS GovCloud (US-East) only                                                                                           |
| Data residency    | Per region                              | U.S. only                                                                                                             |
| High availability | Multi-region active-active              | Single region, three availability zones. Service level per your federal agreement                                     |
| Operations        | Global                                  | U.S.-based operators, with 24x7 platform monitoring and incident response from the hosting provider                   |
| Release path      | Continuous delivery                     | Each release is hardened, scanned, and validated by the hosting provider before deployment                            |
| Support           | Global follow-the-sun                   | U.S.-based federal support queue, plus 24x7 platform support from the hosting provider                                |
| Gateway           | Latest stable or quarterly LTS          | Same image, deployed in your environment. FIPS mode is optional                                                       |
| Console sign-in   | Akeyless login or SAML/OIDC Auth Method | Hosted-provider IdP first. See [FedRAMP Account Onboarding](https://docs.akeyless.io/docs/fedramp-account-onboarding) |
| Endpoints         | `*.akeyless.io`                         | `*.fedramp.akeyless.io`                                                                                               |

## Feature Availability

| Capability                                                                          | Availability in FedRAMP                                                         |
| ----------------------------------------------------------------------------------- | ------------------------------------------------------------------------------- |
| Static secrets, dynamic secrets, rotated secrets                                    | Available                                                                       |
| PKI, certificate management, and key management (DFC)                               | Available                                                                       |
| Secure Remote Access, Kubernetes, and CI/CD integrations that run from your Gateway | Available. They run from the Gateway, inside your network                       |
| Integrations initiated by the hosted control plane                                  | Subject to the boundary's egress policy. Declare targets to Akeyless in advance |
| Identity and Secrets Intelligence (ISI)                                             | Not available                                                                   |

## New Features and Fixes

* **Security fixes** are prioritized under FedRAMP vulnerability remediation timelines.
* **New features** ship to the commercial environment first, then go through the hosting provider's validation pipeline. They typically reach the FedRAMP environment within a quarter of the commercial release.
* **Boundary changes** follow the FedRAMP significant change process and can take longer.
* **Gateway releases** are not gated by the hosting provider's pipeline. You can upgrade Gateways when you choose.

Check the release notes and ask your Akeyless Customer Success team to confirm whether a specific feature is available in your environment.

## Related Pages

* [FedRAMP Environment](https://docs.akeyless.io/docs/fedramp-environment)
* [FedRAMP Network Connectivity](https://docs.akeyless.io/docs/fedramp-network-connectivity)
