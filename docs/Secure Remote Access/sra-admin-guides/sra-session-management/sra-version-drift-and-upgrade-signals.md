---
title: Version Drift and Upgrade Signals
slug: sra-version-drift-and-upgrade-signals
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
Use this page to detect version drift between Gateway and SRA components and to plan upgrades with reduced operational risk.

## Detect Version Drift

Use these signals together:

* Bastion instance versions from `list-sra-bastions` output.
* Gateway and SRA component image tags in deployment manifests.
* Session failure patterns after recent configuration or image updates.

A mixed-version fleet can be temporarily expected during rolling updates, but sustained mismatch windows should be investigated.

### Implementation: Drift Baseline and Detection Loop

Run this baseline before any upgrade window:

```shell
akeyless list-sra-bastions
```

Capture and persist these fields per cluster:

* Cluster name
* Instance IDs
* Version values
* Last report timestamp

Then run the same command repeatedly during rollout and compare with the baseline.

A practical operating threshold is:

1. Mixed versions are acceptable only during the active rolling window.
2. If mixed versions persist beyond the expected rollout time for your environment, treat this as drift and stop further promotion.

## Helm and Compose Version Controls

For Kubernetes deployments, pin chart version and values intentionally during rollout planning.

For Docker Compose deployments, pin image tags and update all related SRA and Gateway services in the same change window.

Avoid partial, long-lived drift between gateway and bastion components.

### Implementation: Kubernetes (Helm)

Use a pinned chart version and a reviewed values file:

```shell
helm repo update
helm dependency update charts/akeyless-gateway
helm upgrade <release-name> akeyless/akeyless-gateway \
  --namespace <namespace> \
  --version <chart-version> \
  -f <values-file> \
  --atomic --wait
```

Use `helm get values <release-name> -n <namespace>` before and after upgrade to confirm that only intended values changed.

### Implementation: Docker Compose

Pin explicit image tags for gateway and SRA-related services in the compose file, then apply in one window:

```shell
docker compose -f <compose-file> config
docker compose -f <compose-file> pull
docker compose -f <compose-file> up -d
```

Do not update only one service family and leave other SRA components on older tags for extended periods.

## Rolling Upgrade Sequence

A practical rollout order is:

1. Upgrade Gateway components first.
2. Upgrade SRA web and SSH components.
3. Validate session establishment and inventory signals.
4. Complete remaining bastion or dispatcher workers.

This order reduces control-plane and config translation mismatches during rollout.

### Implementation: Promotion Gates per Step

After each step, verify all of the following before continuing:

1. `list-sra-bastions` shows expected instance registration and version movement.
2. New sessions can be created successfully.
3. Existing sessions are not failing at abnormal rates.

If any gate fails, stop rollout and stabilize before proceeding.

## Compatibility and Known Boundaries

Use release notes and CLI reference updates to confirm compatibility expectations before production rollout.

Known operational examples in current docs include:

* Some older OpenSSH targets require legacy SSH algorithm compatibility settings.
* Older Gateway environments can require SSH issuer `session_*` compatibility behavior for SRA session users.

For command and flag details, see [CLI Reference - Gateway Secure Remote Access](https://docs.akeyless.io/docs/cli-reference-sra).

## Upgrade Validation Checklist

1. Confirm cluster inventory and instance versions are consistent after rollout.
2. Confirm `list-sra-sessions` shows expected active and completed lifecycle behavior.
3. Confirm RDP recording and storage upload paths still operate as expected.
4. Confirm session failure rate remains within baseline after upgrade.

## Rollback Trigger Criteria

Execute rollback when one or more conditions are sustained:

* Session creation failures above baseline after rollout.
* `list-sra-bastions` shows unresolved mixed-version state after the rollout window.
* Recording or forwarding pipelines fail and cannot be corrected quickly in-place.

Rollback should restore the last known-good chart/image set and values package, then rerun the upgrade checklist.
