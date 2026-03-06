---
title: Choose a Deployment Model
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

Akeyless Gateway supports local container deployments, Kubernetes-based deployments, and serverless patterns.

* **Container-based deployments** are fastest to start with and work well for single environment or smaller scale footprints.
* **Kubernetes-based deployments** are best when you need high availability, policy-driven operations, and platform standardization.
* **Serverless deployments** are best when your priority is minimizing infrastructure operations and scaling elastically with traffic.

## Deployment Options

| Option | Type |
| --- | --- |
| [Standalone Docker Deployment](https://docs.akeyless.io/docs/install-and-configure-the-gateway) | Container |
| [Docker Compose Deployment](https://docs.akeyless.io/docs/gateway-compose) | Container |
| [Kubernetes with Helm Deployment](https://docs.akeyless.io/docs/gateway-chart) | Kubernetes |
| [Amazon EKS Deployment](https://docs.akeyless.io/docs/gateway-k8s#aws-iam) | Kubernetes (AWS) |
| [Azure Kubernetes Service Deployment](https://docs.akeyless.io/docs/gateway-k8s#azure-active-directory) | Kubernetes (Azure) |
| [Google Kubernetes Engine Deployment](https://docs.akeyless.io/docs/gateway-k8s#gcp) | Kubernetes (GCP) |
| [AWS Serverless Deployment](https://docs.akeyless.io/docs/serverless-aws) | Serverless (AWS) |
| [Azure Serverless Deployment](https://docs.akeyless.io/docs/azure-serverless) | Serverless (Azure) |

## Advantages and Disadvantages by Model

### Standalone Docker and Docker Compose

_Advantages:_

* Fastest path to deployment and testing.
* Low operational complexity.
* Good fit for development, labs, and small production environments.

_Disadvantages:_

* Limited native high availability.
* Manual operational workflows compared to Kubernetes.
* Less suitable for large, multi-team platforms.

### Kubernetes with Helm

_Advantages:_

* Strong scalability and high availability capabilities.
* Better fit for GitOps and policy-based operations.
* Integrates with existing cluster-level security and observability patterns.

_Disadvantages:_

* Higher operational complexity.
* Requires Kubernetes and Helm expertise.
* Initial setup is longer than container-only deployment.

### Cloud Platform-Specific Kubernetes Variants (EKS, AKS, GKE)

_Advantages:_

* Aligns with cloud-native identity and service integrations.
* Simplifies platform alignment for cloud-specific operational teams.
* Supports multi-cluster and enterprise patterns.

_Disadvantages:_

* Tighter coupling to a specific cloud platform.
* Additional cloud-service configuration overhead.
* Portability can require extra planning.

### Serverless Deployments

_Advantages:_

* Minimal infrastructure management.
* Elastic scaling for variable workloads.
* Can reduce idle infrastructure cost.

_Disadvantages:_

* Service limitations compared to full Gateway deployments.
* Platform-specific architecture and dependencies.
* Operational behavior differs from long-running cluster/container deployments.
