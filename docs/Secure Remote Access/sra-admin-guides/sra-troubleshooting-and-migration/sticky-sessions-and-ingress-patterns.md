---
title: Sticky Sessions and Ingress Patterns
slug: sra-sticky-sessions-and-ingress-patterns
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
Use this page to configure session affinity for SRA traffic paths that require backend consistency across multi-step request flows.

## Why Sticky Sessions Matter for SRA

SRA traffic can include multi-step session state where requests must continue to hit the same backend while a session is active.

When traffic is re-routed mid-session, users can experience dropped connections, failed status checks, or interrupted portal flows.

## Platform Patterns

### NGINX Ingress

For NGINX ingress, use cookie affinity annotations:

```yaml
nginx.ingress.kubernetes.io/affinity: "cookie"
nginx.ingress.kubernetes.io/session-cookie-expires: "172800"
nginx.ingress.kubernetes.io/session-cookie-max-age: "172800"
```

### AWS Load Balancing

For AWS ALB, configure target-group stickiness and align idle timeout with expected session duration.

For AWS NLB, use TCP keep-alive and timeout tuning for long-running SSH and proxy sessions.

### Google Cloud Load Balancing

For GKE HTTP(S) Load Balancer paths, configure backend timeout values (`timeoutSec`) to avoid early disconnects. Apply backend policy consistently across services participating in long-lived sessions.

## Cookie-Based and IP-Based Affinity

| Affinity mode | Strengths | Tradeoffs |
| --- | --- | --- |
| Cookie-based | Better user/session stickiness in shared NAT environments and browser workflows | Requires cookie handling across proxy layers and TLS policies |
| IP-based | Simple for some L4 flows | Less reliable when many users share egress IP, and can concentrate traffic unevenly |

For browser-driven SRA and ZTWA workflows, cookie-based affinity is usually preferred.

## ZTWA Proxy Mode Considerations

In ZTWA proxy mode, users enter through dispatcher endpoints (typically `9000` and `19414`).

Recommended controls:

1. Keep dispatcher affinity behavior consistent during active web sessions.
2. Ensure proxy and ingress timeout values match session duration targets.
3. Use `allowedBastionUrls` and `allowedProxyUrls` controls so redirect and callback destinations stay deterministic.

For baseline timeout and allowlist requirements, see [SRA Requirements](https://docs.akeyless.io/docs/sra-requirements).

## Verification Checklist

1. Start a long-lived SSH or web session.
2. Confirm backend identity consistency during the active session window.
3. Validate no mid-session disconnect under normal ingress or load balancer behavior.
4. Re-test after ingress-controller, load balancer, or HPA policy changes.
