---
title: gateway-cloud-serverless-deployments
excerpt: ''
deprecated: false
hidden: false
metadata:
  title: ''
  description: ''
  robots: index
next:
  description: 'Deploy the Serverless Gateway on:'
  pages:
    - type: basic
      title: AWS Serverless Deployment
      slug: gateway-deploy-serverless-aws
    - type: basic
      title: Azure Serverless Deployment
      slug: gateway-deploy-serverless-azure
---
The **Serverless Gateway** is a deployment model for teams that want Akeyless Gateway capabilities without managing a long-running Kubernetes or VM-based runtime.

In this model, cloud-managed serverless services handle runtime scaling, while you configure identity, networking, and Gateway settings for your environment.

## When to Use Cloud-Managed Serverless Platforms

Use cloud-managed serverless platform patterns when you need:

* Elastic scaling with low infrastructure management overhead.
* Fast environment provisioning for cloud-native teams.
* Provider-managed runtime operations.

Choose Kubernetes-based deployment when you need deep platform-level control, custom runtime topology, or consistent multi-cluster operations.

## Shared Prerequisites

Before choosing AWS or Azure, validate the following:

* Required cloud account permissions are available.
* Outbound connectivity to required Akeyless SaaS services is allowed.
* Gateway authentication method and access permissions are prepared.
* Runtime identity model is selected for the target provider.

Reference:

* [Gateway Network Connectivity](https://docs.akeyless.io/docs/gateway-network-connectivity)

## Platform Guides

| Platform Guide | Runtime Model | Typical Identity Integration |
| --- | --- | --- |
| [AWS Serverless Deployment](https://docs.akeyless.io/docs/gateway-deploy-serverless-aws) | AWS Lambda and API Gateway | AWS IAM |
| [Azure Serverless Deployment](https://docs.akeyless.io/docs/gateway-deploy-serverless-azure) | Azure Functions and API Management | Azure AD managed identity |

## What Stays the Same Across Providers

Across AWS and Azure cloud-managed serverless platforms, the operational model remains consistent:

* Gateway authentication and access permissions.
* TLS and certificate trust configuration.
* Log forwarding and telemetry integration.
* Zero-Knowledge and encryption-related configuration.

After deployment, continue with:

* [Gateway Authentication](https://docs.akeyless.io/docs/gateway-authentication-and-access)
* [Log Forwarding](https://docs.akeyless.io/docs/gateway-log-forwarding)
* [Telemetry and Monitoring](https://docs.akeyless.io/docs/monitor-akeyless)
