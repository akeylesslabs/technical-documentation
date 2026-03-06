---
title: Cloud Platform Deployments
excerpt: ''
deprecated: false
hidden: false
metadata:
  title: ''
  description: ''
  robots: index
next:
  description: 'Choose a cloud-managed Kubernetes deployment guide:'
  pages:
    - type: link
      title: Amazon EKS
      url: https://docs.akeyless.io/docs/gateway-k8s#aws-iam
    - type: link
      title: Azure Kubernetes Service
      url: https://docs.akeyless.io/docs/gateway-k8s#azure-active-directory
    - type: link
      title: Google Kubernetes Engine
      url: https://docs.akeyless.io/docs/gateway-k8s#gcp
---
This page groups cloud-managed Kubernetes deployment patterns for the Akeyless Gateway.

Use this section when your organization runs Kubernetes on a cloud provider and wants a Gateway deployment aligned with cloud-native identity and platform controls.

## When to Use Cloud Platform Deployments

Cloud platform deployment patterns are a good fit when you need:

* Managed Kubernetes control planes.
* Cloud-native workload identity integration.
* Standardized platform operations across cloud environments.

If you need provider-agnostic deployment guidance, use [Kubernetes with Helm Deployment](https://docs.akeyless.io/docs/gateway-chart) first, then apply provider-specific settings.

## Shared Prerequisites

Before selecting a platform-specific flow, validate the following:

* Kubernetes cluster and Helm are installed and operational.
* Outbound connectivity to required Akeyless SaaS services is available.
* A Gateway authentication method is prepared with required permissions.
* Platform-specific identity bindings are planned for runtime access.

Reference:

* [Gateway Network Connectivity](https://docs.akeyless.io/docs/api-gateway-network-connectivity)

## Platform Guides

Choose the guide that matches your cluster platform:

| Platform Guide | Typical Identity Integration |
| --- | --- |
| [Amazon EKS Deployment](https://docs.akeyless.io/docs/gateway-k8s#aws-iam) | AWS IAM roles |
| [Azure Kubernetes Service Deployment](https://docs.akeyless.io/docs/gateway-k8s#azure-active-directory) | Azure AD workload identity |
| [Google Kubernetes Engine Deployment](https://docs.akeyless.io/docs/gateway-k8s#gcp) | GCP workload identity |

## What Stays the Same Across Platforms

Across EKS, AKS, and GKE, the core Gateway model is consistent:

* Gateway authentication and access permissions.
* TLS and certificate configuration.
* Cache and offline behavior.
* Log forwarding and telemetry configuration.

After deployment, continue with [Configure Gateway](https://docs.akeyless.io/docs/configure-gateway).
