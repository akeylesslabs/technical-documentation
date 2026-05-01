---
title: Zero Trust Web Access Topology
excerpt: ''
deprecated: false
hidden: false
metadata:
  title: ''
  description: ''
  robots: index
next:
  description: ''
---
This page describes the Zero Trust Web Access (ZTWA) runtime topology and the key deployment settings for Kubernetes and Docker Compose.

## Architecture and Traffic Flow

ZTWA uses two primary services:

* **Dispatcher**: Entry point that authenticates requests and dispatches session traffic
* **Web-worker**: Isolated browser runtime that serves user sessions

Traffic flow:

1. User requests access from the SRA portal.
2. Dispatcher validates policy and authentication context.
3. Dispatcher routes the session to a web-worker.
4. Web-worker runs the isolated browser session to the target web application.

## Required Topology Settings

### Service Discovery

Set `SERVICE_DNS` so dispatcher can discover and route traffic to workers.

### Proxy Mode and Ports

* `WEB_PROXY_TYPE` controls proxy mode (`http` or default socks mode).
* Port `19414` is used for proxy-mode traffic.

### HTTP Deployments

For HTTP deployments, set `DISABLE_SECURE_COOKIE=true`.

### Privileged Access Pattern

Configure:

* `PRIVILEGED_ACCESS_ID` as the privileged machine identity used by the bastion
* `ALLOWED_ACCESS_IDS` as the identities allowed to request access

This pattern allows users to keep list-level permissions while the bastion fetches target credentials on their behalf after authorization.

## Platform Guides

* Kubernetes deployment and values: [Zero Trust Web Access on K8s](https://docs.akeyless.io/docs/sra-web-access-on-k8s)
* Docker Compose deployment and env values: [Zero Trust Web Access on Docker](https://docs.akeyless.io/docs/web-access-on-docker)
* Extended browser policies, DLP, private CA certificate handling, and advanced options: [Zero Trust Web Access Advanced Configuration](https://docs.akeyless.io/docs/sra-web-access-on-k8s-adv-config)
