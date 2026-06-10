---
title: Session Drops and Timeout Runbooks
slug: sra-session-drops-and-timeout-runbooks
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
Use this page to diagnose and resolve unexpected session termination in SSH, RDP, and web-access flows.

## Common Causes

| Symptom pattern | Common cause |
| --- | --- |
| Active sessions terminate during rollout or autoscaling | Bastion pod restart or HPA scale-in terminated a pod that held active sessions |
| Sessions close after fixed idle window | Ingress or load balancer timeout shorter than expected session duration |
| New SSH sessions fail during spikes | `CONFIG_MAX_STARTUPS` threshold reached on SSH bastion |
| Session ends near a configured policy limit | Session TTL expiry from Gateway SRA configuration |

## Runbook 1: Bastion Restart or HPA Scale-In

### Diagnostics

1. Check for pod restarts and recent scale events in the bastion namespace.
2. Review bastion and gateway logs around drop time.
3. Confirm session state with `list-sra-sessions` using both active and ended filters.

```shell
akeyless list-sra-sessions --status-types active,ended,error
```

### Resolution

1. Increase scale-in protection and rollout conservatism for SRA pods.
2. Configure PodDisruptionBudgets for gateway and SRA workloads.
3. Delay disruptive operations during peak session windows.

For HPA guardrails, see [Scaling and HPA Patterns](https://docs.akeyless.io/docs/sra-scaling-and-hpa-patterns).

## Runbook 2: Timeout Misalignment

### Diagnostics

1. Compare configured session TTL with ingress and load balancer idle/response timeout values.
2. Check platform defaults for your ingress or load balancer tier.
3. Correlate timeout interval with user-reported disconnect timing.

### Resolution

1. Set ingress and load balancer timeout values to match or exceed expected SRA session duration.
2. If a custom TTL is used, align network timeout values to that TTL.
3. Re-test long-lived sessions after timeout changes.

For platform-specific timeout references, see [SRA Requirements](https://docs.akeyless.io/docs/sra-requirements#session-timeout-and-ttl-alignment).

## Runbook 3: `CONFIG_MAX_STARTUPS` Saturation

### Diagnostics

1. Inspect SSH bastion logs for rejected unauthenticated connection bursts.
2. Verify current `CONFIG_MAX_STARTUPS` value in deployment environment configuration.
3. Check concurrent unauthenticated connection patterns during incident windows.

### Resolution

1. Increase `CONFIG_MAX_STARTUPS` based on observed burst profile.
2. Reduce unauthenticated connection storms by smoothing client retry behavior.
3. Combine with ingress and scaling controls to avoid repeated saturation.

Example deployment value:

```yaml
sra:
  env:
    - name: CONFIG_MAX_STARTUPS
      value: "200:30:300"
```

## Runbook 4: Session TTL Expiry

### Diagnostics

1. Review effective Gateway SRA config for default session TTL.
2. Compare session start/end timestamps to TTL policy.
3. Confirm whether expiration behavior matches intended security policy.

### Resolution

1. Update default session TTL if current policy is too short for operational use.
2. Reconfirm timeout alignment across ingress, load balancer, and session policy.
3. Communicate policy changes to operators and users.

For TTL policy configuration, see [Session TTL and Security Controls](https://docs.akeyless.io/docs/sra-session-ttl-and-security-controls).

## Minimum Incident Dataset to Capture

When escalating an incident, collect:

* Affected cluster name and deployment mode (unified or split).
* Session ID samples and status transitions.
* Bastion/gateway restart evidence and scale-event timestamps.
* Ingress or load balancer timeout values.
* Effective `CONFIG_MAX_STARTUPS` setting.
