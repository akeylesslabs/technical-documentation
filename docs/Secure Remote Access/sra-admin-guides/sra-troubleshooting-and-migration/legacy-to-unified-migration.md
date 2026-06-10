---
title: sra-Legacy to Unified Migration
slug: sra-legacy-to-unified-migration
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
Use this page to migrate Secure Remote Access from legacy split deployment patterns to the unified Gateway chart model.

## Architecture Change Summary

Legacy deployments commonly used separate SRA deployment units and chart surfaces.

Unified deployments run SRA components through the `akeyless-gateway` chart configuration surface, with shared gateway-managed control paths.

Operationally, migrate with explicit checks for internal service wiring, ingress behavior, and runtime security controls.

## Migration Steps

1. Inventory current split deployment values and runtime endpoints.
2. Map legacy values to unified chart keys under gateway and SRA sections.
3. Prepare DNS and load balancer traffic transition for unified entrypoints.
4. Deploy unified chart in a controlled rollout window.
5. Validate sessions, bastion inventory, and recording/forwarding behavior.
6. Decommission legacy deployment only after stability confirmation.

## Configuration Items That Need Explicit Carryover

The following settings do not reliably carry over unless you map them intentionally:

* Custom TLS certificates and ingress TLS bindings.
* Environment variable overrides for internal routing and proxy behavior.
* Redirect allowlists such as `allowedBastionUrls` and `allowedProxyUrls`.
* Redis endpoint and connection settings (for example `REDIS_ADDR` patterns).

## DNS and Load Balancer Transition Guidance

During migration:

1. Reduce DNS TTL ahead of planned traffic transition.
2. Ensure new load balancer listeners and health checks are ready before traffic switch.
3. Validate required ports and timeout settings before full user rollout.
4. Keep a rollback route available until session stability is confirmed.

For baseline port and timeout requirements, see [SRA Requirements](https://docs.akeyless.io/docs/sra-requirements).

## Rollback Path

If post-transition issues occur:

1. Re-point DNS and load balancer routes to legacy endpoints.
2. Restore the last known-good legacy values package.
3. Reconfirm session establishment and bastion health.
4. Capture drift findings before retrying migration.

Use [Cluster and Instance Health](https://docs.akeyless.io/docs/sra-cluster-and-instance-health) and [Version Drift and Upgrade Signals](https://docs.akeyless.io/docs/sra-version-drift-and-upgrade-signals) during rollback and retry decisions.

## Legacy and Unified Compatibility Matrix

Use this matrix to assess migration readiness by deployment state.

| Current state | Target state | Compatibility signal | Recommended action |
| --- | --- | --- | --- |
| Legacy split SRA chart with stable sessions | Unified `akeyless-gateway` chart | Supported migration path | Stage values mapping and perform phased traffic transition |
| Legacy split chart with custom TLS and allowlists | Unified chart with equivalent security controls | Supported when controls are re-mapped | Pre-validate TLS and allowlist parity before traffic transition |
| Legacy split chart with custom env overrides | Unified chart defaults only | High drift risk | Port required overrides explicitly and validate runtime wiring |
| Mixed legacy and unified components running long-term | Fully unified deployment | Operational drift boundary | Minimize mixed-mode window and complete migration quickly |

## Version Compatibility Handling

Because legacy and unified charts are released independently over time, validate compatibility by rollout signals rather than by assuming fixed version pairs.

Before production traffic transition:

1. Pin chart and image versions for the migration window.
2. Validate `list-sra-bastions` output and session behavior in pre-production.
3. Confirm no sustained version drift remains after rollout.
