---
title: Cloud Serverless Deployments
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
    - type: link
      title: AWS
      url: https://docs.akeyless.io/docs/serverless-aws
    - type: link
      title: Azure
      url: https://docs.akeyless.io/docs/azure-serverless
---
The **Serverless Gateway** is a deployment model for teams that want Akeyless Gateway capabilities without managing a long-running Kubernetes or VM-based runtime.

In this model, cloud-managed serverless services handle runtime scaling, while you configure identity, networking, and Gateway settings for your environment.

## When to Use Serverless Deployments

Use serverless deployment patterns when you need:

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

* [Gateway Network Connectivity](https://docs.akeyless.io/docs/api-gateway-network-connectivity)

## Platform Guides

| Platform Guide | Runtime Model | Typical Identity Integration |
| --- | --- | --- |
| [AWS Serverless Deployment](https://docs.akeyless.io/docs/serverless-aws) | AWS Lambda and API Gateway | AWS IAM |
| [Azure Serverless Deployment](https://docs.akeyless.io/docs/azure-serverless) | Azure Functions and API Management | Azure AD managed identity |

## What Stays the Same Across Providers

Across AWS and Azure serverless deployments, the operational model remains consistent:

* Gateway authentication and access permissions.
* TLS and certificate trust configuration.
* Log forwarding and telemetry integration.
* Zero-Knowledge and encryption-related configuration.

After deployment, continue with [Configure Gateway](https://docs.akeyless.io/docs/configure-gateway).
