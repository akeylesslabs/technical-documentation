---
title: Overview
excerpt: Akeyless Gateway Overview
deprecated: false
hidden: false
metadata:
  title: ''
  description: ''
  robots: index
next:
  pages:
    - slug: install-and-configure-the-gateway
      title: Standalone Gateway
      type: basic
    - slug: gateway-chart
      title: Gateway on Kubernetes
      type: basic
---
Akeyless offers a unique Gateway, which adds an extra level of protection between your **private network** and the cloud.

Acting as a SaaS extension of our core services, our **stateless** Gateway enables transparent internal operation with a robust out-of-the-box mechanism to ensure service continuity and recovery while you are not required to change any network infrastructure to work with your internal resources.

Our unique approach enables a variety of capabilities relying on our state-of-the-art [Encryption Technology](https://docs.akeyless.io/docs/dfc-overview) you can securely use our [Dynamic Secrets](https://docs.akeyless.io/docs/how-to-create-dynamic-secret), [Rotated Secrets](https://docs.akeyless.io/docs/rotated-secrets) along with [KMIP Server](https://docs.akeyless.io/docs/kmip-server) and more [Advanced Data Protection](https://docs.akeyless.io/docs/classic-keys) flavors, without exposing any internal resources to the public network.

With this Gateway, Akeyless offers:

* Live fallback for network connectivity issues

* Service continuity by way of secrets snapshots

* Local in-memory cache for continuous service

* Log forwarding to an existing SIEM server.

* [Zero-Knowledge Encryption](https://docs.akeyless.io/docs/zero-knowledge)

![Akeyless Gateway Architecture](https://files.readme.io/eaaa39e-Gateway_2.png)

## Quickstarts

For faster, platform-specific deployment flows, use the **Gateway Deployment Quickstarts** section in the Akeyless Gateway documentation.

This section includes quickstarts for:

* Amazon Elastic Kubernetes Service (EKS)
* Google Kubernetes Engine (GKE)
* Azure Kubernetes Service (AKS)
* Docker Compose (Unified Gateway + Secure Remote Access)

## Gateway Options at a Glance

Use this table to distinguish Gateway product options from deployment options:

| Option | What it means | When to use | Documentation |
| --- | --- | --- | --- |
| Unified Gateway | The current Akeyless Gateway model, deployed with the `akeyless-gateway` chart/configuration patterns. | Default choice for new deployments. | [Gateway on Kubernetes](https://docs.akeyless.io/docs/gateway-chart), [Docker Compose](https://docs.akeyless.io/docs/gateway-compose), [Gateway Deployment Quickstarts](https://docs.akeyless.io/docs/gateway-quickstarts) |
| Legacy Gateway | The previous Kubernetes Gateway model, documented for backward compatibility. | Existing environments that still run the legacy deployment model. | [Gateway on Kubernetes (Legacy)](https://docs.akeyless.io/docs/gateway-k8s) |
| Deployment option | The infrastructure/runtime where the Gateway is deployed (for example Kubernetes, Docker Compose, serverless, or Azure Container Apps). | Based on your platform and operational requirements. | [Gateway Overview](https://docs.akeyless.io/docs/api-gw) |

## Tutorial

Check out our tutorial video on [Installing and Configuring the Gateway](https://tutorials.akeyless.io/docs/installing-and-configuring-akeyless-gateway).
