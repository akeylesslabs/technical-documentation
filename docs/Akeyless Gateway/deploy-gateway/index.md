---
title: Choose a Deployment Model
slug: deploy-gateway
excerpt: ''
deprecated: false
hidden: false
metadata:
  title: ''
  description: ''
  robots: index
---
Use this section to select a deployment model that matches your infrastructure, operational maturity, and scaling requirements.

## Deployment Models at a Glance

Akeyless Gateway supports self-managed runtime options, cloud-managed Kubernetes platforms, and cloud-managed serverless platforms.

* **Self-managed runtime options** are fastest to start with and work well for local environments, virtual machines, cloud compute instances (for example, Amazon EC2 and Google Compute Engine), and self-managed Kubernetes.
* **Cloud-managed Kubernetes platforms** are best when you need high availability, policy-driven operations, and managed control-plane capabilities.
* **Cloud-managed serverless platforms** are best when your priority is minimizing infrastructure operations and scaling elastically with traffic.

## Deployment Options

| Option | Type |
| --- | --- |
| [Standalone Docker Deployment](https://docs.akeyless.io/docs/gateway-deploy-standalone-docker) | Self-managed runtime |
| [Docker Compose Deployment](https://docs.akeyless.io/docs/gateway-deploy-docker-compose) | Self-managed runtime |
| [Kubernetes with Helm Deployment](https://docs.akeyless.io/docs/gateway-deploy-kubernetes-helm) | Self-managed runtime |
| [Amazon EKS Deployment](https://docs.akeyless.io/docs/gateway-deploy-amazon-eks) | Cloud-managed Kubernetes platform |
| [Azure Kubernetes Service Deployment](https://docs.akeyless.io/docs/gateway-deploy-azure-kubernetes-service) | Cloud-managed Kubernetes platform |
| [Google Kubernetes Engine Deployment](https://docs.akeyless.io/docs/gateway-deploy-google-kubernetes-engine) | Cloud-managed Kubernetes platform |
| [AWS Serverless Deployment](https://docs.akeyless.io/docs/gateway-deploy-serverless-aws) | Cloud-managed serverless platform |
| [Azure Serverless Deployment](https://docs.akeyless.io/docs/gateway-deploy-serverless-azure) | Cloud-managed serverless platform |

## Advantages and Disadvantages by Model

### Self-Managed Runtime Options

_Advantages:_

* Fastest path to deployment and testing.
* Low operational complexity.
* Good fit for development, labs, and small production environments.

_Disadvantages:_

* Limited native high availability.
* Manual operational workflows compared to managed platforms.
* Less suitable for large, multi-team platforms.

### Self-Managed Kubernetes with Helm

_Advantages:_

* Strong scalability and high availability capabilities.
* Better fit for GitOps and policy-based operations.
* Integrates with existing cluster-level security and observability patterns.

_Disadvantages:_

* Higher operational complexity than managed Kubernetes platforms.
* Requires Kubernetes and Helm expertise.
* Initial setup is longer than container-only deployment.

### Cloud-Managed Kubernetes Platforms

_Advantages:_

* Aligns with cloud-native identity and service integrations.
* Simplifies platform alignment for cloud-specific operational teams.
* Supports multi-cluster and enterprise patterns.

_Disadvantages:_

* Tighter coupling to a specific cloud platform.
* Additional cloud-service configuration overhead.
* Portability can require extra planning.

### Cloud-Managed Serverless Platforms

_Advantages:_

* Minimal infrastructure management.
* Elastic scaling for variable workloads.
* Can reduce idle infrastructure cost.

_Disadvantages:_

* Service limitations compared to full Gateway deployments.
* Platform-specific architecture and dependencies.
* Operational behavior differs from long-running cluster/container deployments.

## After Deployment

* Configure runtime settings in [Configure Gateway](https://docs.akeyless.io/docs/configure-gateway).
* Plan observability and incident response in [Operate Gateway](https://docs.akeyless.io/docs/operate-gateway).
* Validate required egress paths in [Gateway Network Connectivity](https://docs.akeyless.io/docs/gateway-network-connectivity).
