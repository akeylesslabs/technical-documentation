---
title: Infrastructure and Capacity Planning
slug: sra-infrastructure-and-capacity-planning
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
Infrastructure and Capacity Planning provides deployment-level guidance for runtime topology, scaling guardrails, recording storage growth, and incident troubleshooting.

Use this section to design SRA environments that remain stable as concurrent session volume grows, and to recover quickly when runtime issues occur.

## Start Here by Objective

1. Validate runtime topology and required ports: [Runtime Components and Ports](https://docs.akeyless.io/docs/sra-runtime-components-and-ports)
2. Configure autoscaling and scale-in safeguards: [Scaling and HPA Patterns](https://docs.akeyless.io/docs/sra-scaling-and-hpa-patterns)
3. Plan recording storage, retention, and backend lifecycle policy: [Storage and Recording Capacity](https://docs.akeyless.io/docs/sra-storage-and-recording-capacity)

## Troubleshooting and Migration

1. Diagnose dropped sessions and timeout failures: [Session Drops and Timeout Runbooks](https://docs.akeyless.io/docs/sra-session-drops-and-timeout-runbooks)
2. Validate ingress and affinity behavior: [Sticky Sessions and Ingress Patterns](https://docs.akeyless.io/docs/sra-sticky-sessions-and-ingress-patterns)
3. Plan migration from legacy split chart to unified chart: [Legacy to Unified Migration](https://docs.akeyless.io/docs/sra-legacy-to-unified-migration)

## Operational Scope

Use this section together with:

* [SRA Requirements](https://docs.akeyless.io/docs/sra-requirements) for baseline ports, platform prerequisites, and deployment constraints.
* [Session Management](https://docs.akeyless.io/docs/sra-session-management) for runtime monitoring and recording review workflows.
