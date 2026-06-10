---
title: Session TTL and Security Controls
slug: sra-session-ttl-and-security-controls
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
Use this page to configure session lifetime and key runtime security controls for Secure Remote Access.

## Session TTL

Gateway remote access supports a default session time-to-live (TTL) value in minutes.

Example:

```shell
akeyless gateway update remote-access \
  --default-session-ttl-minutes <TTL_MINUTES> \
  --gateway-url https://<YOUR_AKEYLESS_GW_URL>:8000
```

For standalone bastion behavior and deployment considerations, see [Session Management](https://docs.akeyless.io/docs/sra-session-management).

## Network Idle Timeout Alignment

In addition to session TTL, ingress and load balancer idle timeout values must align with expected session duration.

For platform-specific timeout guidance, see [SRA Requirements](https://docs.akeyless.io/docs/sra-requirements#session-timeout-and-ttl-alignment).

## SSH Key Exchange Security

Gateway remote access configuration supports explicit key exchange algorithm control:

```shell
akeyless gateway update remote-access \
  --kexalgs <ALGORITHM_1>,<ALGORITHM_2> \
  --gateway-url https://<YOUR_AKEYLESS_GW_URL>:8000
```

Use only approved algorithms required by your organization.

## DLP Attachment (ZTWA)

For web session controls, ZTWA supports DLP integration under dispatcher and worker deployment configuration.

DLP settings include enablement, host and path configuration, mode, log level, and audit forwarding.

For configuration structure, see [Zero Trust Web Access on K8s Advanced Configuration](https://docs.akeyless.io/docs/sra-web-access-on-k8s-adv-config).

## Fullscreen and Browser Control Context

ZTWA worker runtime can disable fullscreen mode and expose internal browser address bar by setting `DISABLE_FULLSCREEN=true` in the worker environment configuration.

Use this control when operations teams require explicit browser chrome visibility for support or policy reasons.

## Additional Runtime Controls

Additional controls commonly configured with these settings include:

* Keyboard layout mapping for remote desktop sessions.
* Maximum unauthenticated startup connection thresholds.
* Proxy and no-proxy configuration for bastion runtime egress.

See [Kubernetes Advanced Configuration](https://docs.akeyless.io/docs/sra-advanced-configuration-k8s) and [Docker Compose Advanced Configuration](https://docs.akeyless.io/docs/sra-advanced-configuration-docker).
