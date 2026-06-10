---
title: sra-Akeyless Connect and SCP (CLI)
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
Use this page as the entry point for CLI-based secure access and file transfer workflows.

## Primary CLI Paths

1. `akeyless connect` for interactive SSH, database, and tunnel-oriented access paths.
2. `akeyless file upload` and `akeyless file download` for secure file transfer through SRA.
3. Legacy `akeyless-scp` only for existing automation that has not moved to `akeyless file` yet.

## Start Here

* For interactive and tunnel workflows, see [Akeyless Connect](https://docs.akeyless.io/docs/sra-akeyless-connect).
* For file transfer workflows, see [Akeyless File Transfer and Akeyless SCP](https://docs.akeyless.io/docs/sra-akeyless-scp).

## Access Behavior Notes

* Unified gateway deployments typically use `-g <gateway-url>` based workflows.
* Legacy flows can still use direct bastion routing parameters where required.
* Effective access is controlled by SRA permissions, issuer policy, and target configuration.

For resource-type specifics, continue with [Supported Resource Types](https://docs.akeyless.io/docs/sra-resource-types).
