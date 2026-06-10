---
title: sra-Scaling and HPA Patterns
slug: sra-scaling-and-hpa-patterns
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
Use this page to configure autoscaling behavior for SRA components while protecting active sessions during scale events.

## HPA Configuration Surfaces

For Helm-based deployments, HPA controls are available for gateway and SRA components.

Common settings include:

* `minReplicas`
* `maxReplicas`
* CPU target utilization (for example `cpuAvgUtil`)
* Memory target utilization (for example `memAvgUtil`)

In unified gateway chart deployments, these are configured under gateway and SRA component values (`gateway.hpa`, `sra.webConfig.hpa`, `sra.sshConfig.hpa`).

In Zero Trust Web Access chart deployments, dispatcher and worker scaling controls are configured under `HPA.dispatcher` and `HPA.webWorker`.

## Sticky Session Requirement

Session-oriented protocols require affinity controls at the ingress or load balancer layer.

For environments with database-style and other long-lived interactive sessions, configure sticky session behavior on your ingress or cloud load balancer so traffic stays pinned appropriately while sessions are active.

For platform-specific affinity patterns, see [Sticky Sessions and Ingress Patterns](https://docs.akeyless.io/docs/sra-sticky-sessions-and-ingress-patterns).

## Scale-In Risk and Session Protection

Scale-in events can terminate pods that still hold active user sessions.

Use these safeguards together:

* Configure a conservative scale-in window before terminating pods.
* Add PodDisruptionBudget resources to reduce voluntary disruption during maintenance and autoscaler actions.
* Roll out capacity changes gradually and watch active-session counts during each step.

For ZTWA deployments, use the HPA session termination grace setting (`sessionTerminationGracePeriodSeconds`) to defer termination and reduce active session interruption.

## Session-Based Autoscaling Signals

CPU and memory are baseline autoscaling signals. If your monitoring stack supports it, add session-aware custom metrics to improve scaling accuracy.

Example metrics to consider:

* Active sessions per bastion or dispatcher pod.
* Busy worker percentage for ZTWA worker pools.
* Session queue growth and wait time.

Validate metric quality before attaching it to production HPA policies.

## Multi-Cluster Scaling Pattern

For multi-cluster operations:

1. Deploy gateway and bastion/dispatcher components with unique cluster naming per environment.
2. Register and verify each bastion fleet by using `list-sra-bastions`.
3. Scale clusters independently based on local load profile.
4. Keep configuration parity across clusters for policy and session controls.

Use [Cluster and Instance Health](https://docs.akeyless.io/docs/sra-cluster-and-instance-health) and [Version Drift and Upgrade Signals](https://docs.akeyless.io/docs/sra-version-drift-and-upgrade-signals) to validate post-scale stability.
