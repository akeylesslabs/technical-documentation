---
title: sra-Version Drift and Upgrade Signals
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

## Helm and Compose Version Controls

For Kubernetes deployments, pin chart version and values intentionally during rollout planning.

For Docker Compose deployments, pin image tags and update all related SRA and Gateway services in the same change window.

Avoid partial, long-lived drift between gateway and bastion components.

## Rolling Upgrade Sequence

A practical rollout order is:

1. Upgrade Gateway components first.
2. Upgrade SRA web and SSH components.
3. Validate session establishment and inventory signals.
4. Complete remaining bastion or dispatcher workers.

This order reduces control-plane and config translation mismatches during rollout.

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
