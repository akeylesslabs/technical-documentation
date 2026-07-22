---
title: Copy of Legacy to Unified Migration
deprecated: false
hidden: true
metadata:
  robots: index
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

### Implementation Details for Each Step

1. Inventory current split deployment values and runtime endpoints.
  Export current values and service endpoints from the active environment.

  ```shell
  helm get values <legacy-release> -n <namespace> -o yaml
  kubectl get svc -n <namespace>
  kubectl get ingress -n <namespace>
  ```

1. Map legacy values to unified chart keys under gateway and SRA sections.
  Build a mapping worksheet with three columns: legacy key, unified key, migration decision.

2. Prepare DNS and load balancer traffic transition for unified entrypoints.
  Stage all listeners, health checks, and TLS bindings before moving user traffic.

3. Deploy unified chart in a controlled rollout window.

  ```shell
  helm upgrade <unified-release> akeyless/akeyless-gateway \
    --namespace <namespace> \
    --version <chart-version> \
    -f <unified-values-file> \
    --atomic --wait
  ```

1. Validate sessions, bastion inventory, and recording and forwarding behavior.

  ```shell
  akeyless list-sra-bastions
  akeyless list-sra-sessions --status-type connecting --status-type connected --status-type completed --status-type failed --status-type terminated
  ```

1. Decommission legacy deployment only after stability confirmation.
  Keep legacy resources intact until at least one full business-cycle validation window completes without critical drift or session regressions.

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

### Implementation: Traffic Transition Procedure

Use this sequence to reduce traffic-transition risk:

1. Lower DNS TTL before migration day.
2. Deploy unified services and verify health checks while traffic still points to legacy.
3. Shift a limited percentage of traffic to unified endpoints.
4. Validate session creation, active session stability, and recording or forwarding behavior.
5. Complete traffic shift only after partial-transition checks pass.

For baseline port and timeout requirements, see [SRA Requirements](https://docs.akeyless.io/docs/sra-requirements).

## Rollback Path

If post-transition issues occur:

1. Re-point DNS and load balancer routes to legacy endpoints.
2. Restore the last known-good legacy values package.
3. Reconfirm session establishment and bastion health.
4. Capture drift findings before retrying migration.

### Implementation: Fast Rollback Checklist

1. Revert DNS or load balancer target groups to legacy endpoints.
2. Confirm legacy pods and services are healthy.
3. Re-run quick session smoke tests for SSH, web, and RDP paths used by your environment.
4. Freeze additional config changes until root cause is identified.

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

For the full drift detection and upgrade gating workflow, use [Version Drift and Upgrade Signals](https://docs.akeyless.io/docs/sra-version-drift-and-upgrade-signals).

Before production traffic transition:

1. Pin chart and image versions for the migration window.
2. Validate `list-sra-bastions` output and session behavior in pre-production.
3. Confirm no sustained version drift remains after rollout.

### Implementation: Acceptance Criteria Before Legacy Decommission

Decommission legacy deployment only when all criteria are met:

1. Unified deployment shows stable bastion inventory with no unresolved version mismatch.
2. Session success rates are within baseline for all critical access modes.
3. Recording and forwarding pipelines are validated in production-like load.
4. On-call rollback instructions are documented and tested.