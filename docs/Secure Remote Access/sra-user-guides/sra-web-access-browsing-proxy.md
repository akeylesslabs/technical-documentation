---
title: Web Access (Browsing / Proxy)
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
Use this page to choose between isolated web browsing and proxy-based web access for Secure Remote Access (SRA).

## Access Modes

### Secure Web Browsing

Secure web browsing runs the target website in an isolated browser session managed by the SRA web stack.

Use this mode when you want tighter isolation and stronger control over browser context during the active session.

### Secure Web Proxy

Secure web proxy mode routes user browser traffic through the dispatcher proxy path while users remain in their local browser.

Use this mode when users need direct browser interaction with internal web applications by way of approved proxy endpoints.

## Configuration Inputs

For both modes, verify these settings before user rollout:

1. Dispatcher URL (typically on port `9000`).
2. Web proxy URL when proxy mode is enabled (typically on port `19414`).
3. Allowed bastion and proxy URL allowlists in your SRA and ZTWA configuration.

For deployment-level setup details, see [Zero Trust Web Access on Kubernetes](https://docs.akeyless.io/docs/sra-web-access-on-k8s) and [SRA Requirements](https://docs.akeyless.io/docs/sra-requirements).

## Resource Discovery Scope

Web-access-capable targets appear in the portal based on your authenticated identity, SRA permissions, and target configuration.

For resource onboarding details by target type, see [Supported Resource Types](https://docs.akeyless.io/docs/sra-resource-types).

## Related Pages

* [Portal Login and Target Discovery](https://docs.akeyless.io/docs/sra-portal)
* [Request Access and Approval Flow](https://docs.akeyless.io/docs/sra-request-access-and-approval-flow)
