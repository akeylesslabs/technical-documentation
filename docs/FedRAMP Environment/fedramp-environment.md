---
title: FedRAMP Environment
deprecated: false
hidden: true
metadata:
  robots: index
---
Run Akeyless in a dedicated, federal-only environment hosted on a FedRAMP High authorized platform.

The Akeyless FedRAMP environment is a separate instance of the Akeyless Platform that runs on the Game Warden platform (operated by Second Front Systems) in AWS GovCloud (US). It is intended for U.S. federal agencies and for organizations that must keep specific workloads inside a FedRAMP boundary.

Apart from **how users first sign in** and **which URLs your tools and Gateways connect to**, working with Akeyless in the FedRAMP environment is the same as in the commercial environment: the same Console, CLI, API, SDKs, Terraform provider, and Gateway.

<Callout icon="📘" theme="info">
  ### Note

  The FedRAMP environment is a **separate environment**, not a region of the commercial SaaS. Accounts, Access IDs, Gateways, hostnames, and credentials are not shared between the two. Plan on one set of accounts per environment.
</Callout>

## What Changes and What Stays the Same

| Area                                                      | Commercial environment                         | FedRAMP environment                                                                                                                                                                                                                               |
| --------------------------------------------------------- | ---------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Account registration                                      | Self-service or via Akeyless                   | Account is created for you by Akeyless in the FedRAMP tenant                                                                                                                                                                                      |
| Console sign-in                                           | Akeyless login (or your SAML/OIDC auth method) | Users are onboarded first into the hosted-provider identity layer (Game Warden), then access the FedRAMP Console. See [FedRAMP Account Onboarding](https://docs.akeyless.io/docs/fedramp-account-onboarding)                                      |
| Endpoints                                                 | `*.akeyless.io`                                | `*.fedramp.akeyless.io`. See [FedRAMP Network Connectivity](https://docs.akeyless.io/docs/fedramp-network-connectivity)                                                                                                                           |
| CLI, SDKs, Terraform                                      | Default API endpoint                           | Same tools, with the API/Gateway URL changed. See [FedRAMP CLI Configuration](https://docs.akeyless.io/docs/fedramp-cli-configuration) and [FedRAMP API, SDKs, and Integrations](https://docs.akeyless.io/docs/fedramp-api-sdks-and-integrations) |
| Gateway                                                   | Connects to the commercial control plane       | Same Gateway image, deployed in your environment and pointed at the FedRAMP control plane. See [FedRAMP Gateway Deployment](https://docs.akeyless.io/docs/fedramp-gateway-deployment)                                                             |
| Secrets, certificates, keys, auth methods, roles, targets | Available                                      | Same concepts and workflows. See [FedRAMP Feature Availability](https://docs.akeyless.io/docs/fedramp-feature-availability) for the differences                                                                                                   |
| Hosting                                                   | Commercial regions                             | AWS GovCloud (US-East), three availability zones                                                                                                                                                                                                  |

## Architecture Overview

The FedRAMP environment keeps the Akeyless Zero-Knowledge model: the hosted control plane stores ciphertext and metadata, while plaintext secrets and your Customer Fragment exist only inside the Gateway running in your environment.

![](https://files.readme.io/7d79764414c5520f83e7ff21bae0e1878cfdfde89f7c4ff9a6f0b56013e42819-image_2.png)

<br />Key points:

- **Outbound only.** Gateways and clients connect outbound to the FedRAMP domain over HTTPS (443). The hosted environment never initiates a connection into yours.
- **Gateways stay with you.** You deploy and operate Gateways in your own landing zones (GovCloud VPCs, on-premises, or other networks).
- **One Gateway, one environment.** A Gateway connects only to its own control plane. Do not reuse a commercial Gateway for FedRAMP workloads, or the reverse.

## Environments

The FedRAMP environment offers a **Staging** and a **Production** environment, both inside the FedRAMP boundary. Accounts are created in Staging first, and then in Production.

| Environment | Purpose                                                            |
| ----------- | ------------------------------------------------------------------ |
| Staging     | Validate onboarding, federation, Gateway deployment, and migration |
| Production  | Federal workloads                                                  |

The Akeyless Customer Success team provides the exact hostnames and the Account details for each environment during onboarding.

## Shared Responsibility

| Akeyless and the hosting provider                                           | Customer                                                                           |
| --------------------------------------------------------------------------- | ---------------------------------------------------------------------------------- |
| Operate the hosted control plane in AWS GovCloud, with U.S.-based operators | Deploy and operate Gateways (lifecycle, upgrades, scaling)                         |
| Platform monitoring, security operations, and incident response             | Custody of the Customer Fragment (optionally anchored to a FIPS 140-3 Level 3 HSM) |
| Hosted-provider identity layer and Console availability                     | Your IdP, user lifecycle, and MFA enforcement                                      |
| Release validation for the FedRAMP environment                              | Role and policy design                                                             |
| FedRAMP package, assessment artifacts, and Customer Responsibility Matrix   | Audit log retention in your SIEM, and your target systems                          |

## Get Started

1. Review [FedRAMP Network Connectivity](https://docs.akeyless.io/docs/fedramp-network-connectivity) and allow outbound HTTPS (443) to the FedRAMP domain.
2. Complete [FedRAMP Account Onboarding](https://docs.akeyless.io/docs/fedramp-account-onboarding) so that your administrators can sign in to the FedRAMP Console.
3. Deploy one or more Gateways. See [FedRAMP Gateway Deployment](https://docs.akeyless.io/docs/fedramp-gateway-deployment).
4. Point the CLI, SDKs, Terraform, and integrations at the FedRAMP endpoints. See [FedRAMP CLI Configuration](https://docs.akeyless.io/docs/fedramp-cli-configuration) and [FedRAMP API, SDKs, and Integrations](https://docs.akeyless.io/docs/fedramp-api-sdks-and-integrations).
5. Review [FedRAMP Feature Availability](https://docs.akeyless.io/docs/fedramp-feature-availability), and then continue with the standard Akeyless guides to create auth methods, roles, secrets, and targets.

## In This Section

- [FedRAMP Account Onboarding](https://docs.akeyless.io/docs/fedramp-account-onboarding)
- [FedRAMP Network Connectivity](https://docs.akeyless.io/docs/fedramp-network-connectivity)
- [FedRAMP CLI Configuration](https://docs.akeyless.io/docs/fedramp-cli-configuration)
- [FedRAMP Gateway Deployment](https://docs.akeyless.io/docs/fedramp-gateway-deployment)
- [FedRAMP API, SDKs, and Integrations](https://docs.akeyless.io/docs/fedramp-api-sdks-and-integrations)
- [FedRAMP Feature Availability](https://docs.akeyless.io/docs/fedramp-feature-availability)