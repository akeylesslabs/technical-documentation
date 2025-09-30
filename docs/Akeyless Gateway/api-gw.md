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
  description: ''
  pages:
    - type: basic
      slug: install-and-configure-the-gateway
      title: Standalone Gateway
    - type: basic
      slug: gateway-k8s
      title: Gateway on K8s
---
Akeyless offers a unique Gateway, which adds an extra level of protection between your **private network** and the cloud.

Acting as a SaaS extension of our core services, our **stateless** Gateway enables a transparent internal operation with a robust out-of-the-box mechanism to ensure service continuity and recovery while you are not required to change any network infrastructure in order to work with your internal resources.

Our unique approach enables a variety of capabilities relying on our state-of-the-art [Encryption Technology](doc:dfc) you can securely use our [Dynamic Secrets](doc:how-to-create-dynamic-secret), [Rotated Secrets](doc:rotated-secrets) along with [KMIP Server](doc:kmip-server) and more [Advanced Data Protection](doc:classic-keys) flavors, without exposing any internal resources to the public network.

With this Gateway, Akeyless offers:

* Live fallback for network connectivity issues

* Service continuity via secrets snapshots

* Local in-memory cache for continuous service

* Log forwarding to an existing SIEM server.

* [Zero-Knowledge Encryption](doc:zero-knowledge)

<Image align="center" alt="Akeyless Gateway Architecture" border={false} caption="Akeyless Gateway Architecture" src="https://files.readme.io/eaaa39e-Gateway_2.png" />

# Tutorial

Check out our tutorial video on [Installing and Configuring the Gateway](https://tutorials.akeyless.io/docs/installing-and-configuring-akeyless-gateway).
