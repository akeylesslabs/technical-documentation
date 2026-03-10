---
title: Overview
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
Akeyless Secure Remote Access is part of the [Gateway](https://docs.akeyless.io/docs/gateway-overview). Users can deploy Remote Access components alongside the Gateway or can use the same chart to deploy Remote Access components after the Gateway is deployed.

The Remote Access solution can be deployed in one of two methods:

1. [Kubernetes by way of Helm](https://docs.akeyless.io/docs/remote-access-setup-k8s)
2. [Docker by way of Docker Compose](https://docs.akeyless.io/docs/remote-access-docker)

In this section, we will cover how to deploy Remote Access on each solution along with advanced configuration options.

We will also cover deploying the [Zero Trust Web Access](https://docs.akeyless.io/docs/web-access-on-k8s) component for connecting to web application targets from within an isolated browser.

Other features in this section include:

* [Session Management](https://docs.akeyless.io/docs/remote-access-session-management) with Session Forwarding and RDP Recordings
* [Akeyless Connect](https://docs.akeyless.io/docs/remote-access-akeyless-connect) for native CLI remote SSH access
* [Akeyless SCP](https://docs.akeyless.io/docs/akeyless-scp-1) for native CLI Secure Copy access
* [SSH Certificates](https://docs.akeyless.io/docs/ssh-certificates) for accessing remote machines using just-in-time, temporary certificates instead of SSH Keys.
