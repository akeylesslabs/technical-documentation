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
Akeyless Gateway is a customer-hosted runtime component that sits between internal workloads and the Akeyless SaaS.

In practice, the Gateway is a stateless service that receives requests from applications, authenticates and authorizes those requests, brokers access to Akeyless services, and enforces local controls such as TLS settings, caching, and forwarding rules.

This allows internal systems to consume Akeyless capabilities such as [Dynamic Secrets](https://docs.akeyless.io/docs/how-to-create-dynamic-secret), [Rotated Secrets](https://docs.akeyless.io/docs/rotated-secrets), [KMIP Server](https://docs.akeyless.io/docs/kmip-server), and [Classic Keys](https://docs.akeyless.io/docs/classic-keys) without directly exposing internal resources to the public network.

## What the Gateway Does

The Gateway provides a local control plane and data path for secrets and encryption operations.

Key responsibilities include:

* Brokering requests from workloads to Akeyless APIs.
* Enforcing local authentication and access behavior.
* Managing local cache behavior for resilience during SaaS connectivity issues.
* Applying local transport security and certificate trust settings.
* Forwarding logs and telemetry into enterprise observability systems.

## How It Fits in Your Architecture

At a high level, workloads call the Gateway, and the Gateway communicates with Akeyless SaaS services over outbound connectivity.

For SaaS service endpoint and connectivity requirements, see [Gateway Network Connectivity](https://docs.akeyless.io/docs/api-gateway-network-connectivity).

## Deployment Models

You can deploy Akeyless Gateway in several operating models, depending on your infrastructure and scaling requirements:

* [Standalone Docker](https://docs.akeyless.io/docs/install-and-configure-the-gateway)
* [Docker Compose](https://docs.akeyless.io/docs/gateway-compose)
* [Kubernetes with Helm](https://docs.akeyless.io/docs/gateway-chart)
* [Cloud-managed Kubernetes platforms](https://docs.akeyless.io/docs/gateway-k8s)
* [Serverless deployments](https://docs.akeyless.io/docs/serverless-gateway)

With this Gateway, Akeyless offers:

* Live fallback for network connectivity issues: [Gateway Network Connectivity](https://docs.akeyless.io/docs/api-gateway-network-connectivity)

* Service continuity through local in-memory caching and offline access patterns: [Gateway Caching](https://docs.akeyless.io/docs/configure-the-gateway-cache)

* Log forwarding to an existing SIEM server: [Gateway Log Forwarding](https://docs.akeyless.io/docs/log-forwarding)

* Zero-Knowledge encryption support: [Gateway Zero Knowledge](https://docs.akeyless.io/docs/zero-knowledge)

![Akeyless Gateway Architecture](https://files.readme.io/eaaa39e-Gateway_2.png)

## Tutorial

Check out our tutorial video on [Installing and Configuring the Gateway](https://tutorials.akeyless.io/docs/installing-and-configuring-akeyless-gateway).
