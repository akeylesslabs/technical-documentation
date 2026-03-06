---
title: Gateway Overview
excerpt: Akeyless Gateway Overview
deprecated: false
hidden: false
metadata:
  title: ''
  description: ''
  robots: index
next:
  pages:
    - slug: deploy-gateway
      title: Deploy Gateway
      type: basic
    - slug: configure-gateway
      title: Configure Gateway
      type: basic
---
Akeyless offers a unique Gateway, which adds an extra level of protection between your **private network** and the cloud.

Acting as a SaaS extension of our core services, our **stateless** Gateway enables transparent internal operation with a robust mechanism to ensure service continuity and recovery while you are not required to change any network infrastructure to work with your internal resources.

Our unique approach enables a variety of capabilities relying on our [DFC Encryption Technology](https://docs.akeyless.io/docs/dfc-overview). You can securely use [Dynamic Secrets](https://docs.akeyless.io/docs/how-to-create-dynamic-secret), [Rotated Secrets](https://docs.akeyless.io/docs/rotated-secrets), [KMIP Server](https://docs.akeyless.io/docs/kmip-server), and more [Advanced Data Protection](https://docs.akeyless.io/docs/classic-keys) capabilities without exposing internal resources to the public network.

## Deployment Models

You can deploy Akeyless Gateway in several operating models, depending on your infrastructure and scaling requirements:

* [Standalone Docker](https://docs.akeyless.io/docs/gateway-installation-quickstart-standalone-docker)
* [Docker Compose](https://docs.akeyless.io/docs/gateway-installation-quickstart-docker-compose)
* [Kubernetes with Helm](https://docs.akeyless.io/docs/gateway-installation-quickstart-kubernetes-helm)
* [Cloud-managed Kubernetes platforms](https://docs.akeyless.io/docs/gateway-cloud-platform-deployments)
* [Serverless deployments](https://docs.akeyless.io/docs/gateway-cloud-serverless-deployments)

For deployment planning and comparison details, see [Choose a Deployment Model](https://docs.akeyless.io/docs/deploy-gateway).

With this Gateway, Akeyless offers:

* Live fallback for network connectivity issues: [Gateway Network Connectivity](https://docs.akeyless.io/docs/gateway-network-connectivity)

* Service continuity through local in-memory caching and offline access patterns: [Gateway Caching](https://docs.akeyless.io/docs/gateway-caching)

* Log forwarding to an existing SIEM server: [Gateway Log Forwarding](https://docs.akeyless.io/docs/gateway-log-forwarding)

* Zero-Knowledge encryption support: [Gateway Zero Knowledge](https://docs.akeyless.io/docs/gateway-zero-knowledge)

![Akeyless Gateway Architecture](https://files.readme.io/eaaa39e-Gateway_2.png)

## Tutorial

Check out our tutorial video on [Installing and Configuring the Gateway](https://tutorials.akeyless.io/docs/installing-and-configuring-akeyless-gateway).
