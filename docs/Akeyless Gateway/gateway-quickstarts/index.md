---
title: Gateway Deployment Quickstarts
excerpt: ''
deprecated: false
hidden: false
metadata:
  title: ''
  description: ''
  robots: index
next:
  pages:
    - slug: eks-unified-gateway-quickstart
      title: EKS Unified Gateway Quickstart
      type: basic
---
These quickstarts provide platform-specific deployment flows for the Akeyless Unified Gateway. Each guide is task-focused and designed for teams that want a faster setup path than the full reference pages.

## Available Quickstarts

* [Amazon Elastic Kubernetes Service (EKS) Quickstart](https://docs.akeyless.io/docs/eks-unified-gateway-quickstart)
* [Google Kubernetes Engine (GKE) Quickstart](https://docs.akeyless.io/docs/gke-unified-gateway-quickstart)
* [Azure Kubernetes Service (AKS) Quickstart](https://docs.akeyless.io/docs/aks-unified-gateway-quickstart)
* [Docker Compose Quickstart (Unified Gateway + Secure Remote Access)](https://docs.akeyless.io/docs/docker-compose-unified-gateway-quickstart)

Use the Docker Compose quickstart when you need a local or single-host deployment flow for evaluation, integration testing, or small non-production environments.

## Related Getting Started Quickstarts

If you are new to Akeyless, complete these quickstarts first:

* [Quickstarts overview](https://docs.akeyless.io/docs/getting-started-quickstarts)
* [Creating an Akeyless Account Quickstart](https://docs.akeyless.io/docs/account-quickstart)
* [API Key Creation Quickstart](https://docs.akeyless.io/docs/api-key-creation-quickstart)
* [Akeyless Gateway with Kubernetes Quickstart](https://docs.akeyless.io/docs/gateway-k8s-quickstart)

## Before You Begin

Each quickstart includes prerequisites for its platform. In all cases, deployment requires:

* An Akeyless Authentication Method with access permissions to manage the required resources.
* Connectivity from the deployed Gateway to Akeyless SaaS core services.
* Internal-only access to Gateway management endpoints.

For full configuration detail and advanced options, continue to the related reference pages under Gateway on Kubernetes and Docker Compose.
