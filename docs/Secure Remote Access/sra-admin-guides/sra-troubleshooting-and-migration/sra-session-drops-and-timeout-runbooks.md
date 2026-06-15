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
3. Confirm session state with `list-sra-sessions` using both active and completed or terminated filters.

```shell
akeyless list-sra-sessions --status-type connecting --status-type connected --status-type completed --status-type terminated --status-type failed
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

## Runbook 5: RDP Tab Closes Without Error

### Diagnostics

1. Verify that the `UAM_ADDR` environment variable in your bastion deployment matches your account's region (for example, MEU for European accounts).
2. Check bastion authentication logs for errors during the RDP session initiation flow.
3. Confirm WebSocket connectivity between the browser and bastion by inspecting browser console errors and network traffic.
4. Verify that the account region and authentication service endpoint are correctly configured in Gateway console settings.

### Resolution

1. Ensure `UAM_ADDR` environment variable aligns with your account's region. Update the bastion deployment configuration if needed.
2. Verify account settings in Gateway console under Remote Access configuration.
3. Test browser WebSocket connectivity to the bastion endpoint.
4. Re-initiate the RDP session after configuration changes.

### Minimum Incident Data for RDP Failures

When escalating RDP connection failures, collect in addition to the above:

* Bastion deployment `UAM_ADDR` environment variable value.
* Account region setting from Gateway console.
* Bastion authentication log excerpts around the time of RDP session initiation.

## Runbook 6: Active SSH Sessions Drop at Fixed Short Intervals

Use this runbook when SSH sessions disconnect around a fixed short interval (for example, 30 to 60 seconds) even while users are continuously active.

### Diagnostics

1. Compare direct client-to-target SSH behavior with SSH through SRA. If direct SSH is stable but SRA SSH drops, focus on ingress or load balancer path.
2. Measure the disconnect interval. A consistent interval often indicates an ingress or backend timeout, not an SSH daemon issue.
3. Review ingress controller configuration and annotations for timeout values on the Gateway and bastion routes.
4. In Kubernetes environments that use GKE ingress, check whether backend timeout is still on the default `30s` value.

### Resolution

1. Increase ingress or load balancer timeout values to match expected SSH session duration.
2. For GKE ingress, configure `BackendConfig` or `GCPBackendPolicy` `timeoutSec` for SRA services.
3. If multiple ingress controllers or site-specific ingress resources are used, verify timeout settings are consistent across all SRA-related ingress objects.
4. Re-test sustained SSH activity sessions after timeout updates.

For platform timeout baselines, see [SRA Requirements](https://docs.akeyless.io/docs/sra-requirements#session-timeout-and-ttl-alignment).
