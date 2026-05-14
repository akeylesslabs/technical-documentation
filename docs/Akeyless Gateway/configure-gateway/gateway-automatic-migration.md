---
title: Automatic Migration
excerpt: ''
deprecated: false
hidden: false
metadata:
  title: ''
  description: ''
  robots: index
---
Use this page to configure and operate automatic migration workflows through Akeyless Gateway.

## What Automatic Migration Does

Automatic migration helps move supported assets from external systems into Akeyless with less manual effort.

Typical workflows include:

* Defining source connection settings.
* Running migration commands.
* Validating migrated items and access behavior.

## Prerequisites

Before running migration workflows:

* Deploy and register Akeyless Gateway.
* Configure Gateway authentication and access permissions.
* Validate network connectivity from Gateway to source systems and Akeyless services.
* Prepare destination paths and required encryption settings.

## Security Guidance

* Use least-privilege credentials for source access.
* Avoid broad admin permissions when migration-specific permissions are sufficient.
* Rotate temporary migration credentials after the migration window closes.

## Configuration Scope

Automatic migration configuration usually includes:

* Source system connection parameters.
* Authentication credentials or identity settings.
* Migration mode and target path strategy.
* [HashiCorp Vault metadata preservation mode](#hashicorp-vault-metadata-preservation-mode) (`full`, `minimal`, or `none`) when configuring HashiCorp Vault migrations.
* Conflict handling behavior for existing items.

## HashiCorp Vault Metadata Preservation Mode

When migrating from HashiCorp Vault, Akeyless supports Key/Value (KV) v2 secret engines, which store metadata alongside each secret value. The `--hashi-metadata-mode` flag controls how much of that metadata is carried over to Akeyless.

If the flag is omitted on `gateway-create-migration`, the mode defaults to `full`. On `gateway-update-migration`, omitting the flag leaves the existing mode unchanged.

| Mode | What is migrated |
| --- | --- |
| `full` | The complete KV v2 metadata block, trimmed to only the secret versions being imported. |
| `minimal` | Only the [custom_metadata](https://developer.hashicorp.com/vault/docs/secrets/kv/kv-v2#custom-metadata) field from the KV v2 metadata block. All other metadata fields are discarded. |
| `none` | No metadata. Only the secret values are migrated. |

### When to choose each mode

* Use `full` when you need to preserve as much Vault context as possible, for example, when keeping version history alignment or retaining all metadata fields for auditing.
* Use `minimal` when only your own custom key–value annotations (stored in [custom_metadata](https://developer.hashicorp.com/vault/docs/secrets/kv/kv-v2#custom-metadata)) are needed in Akeyless and you want to reduce migration payload size.
* Use `none` when metadata is not relevant to your use case and you want the smallest possible migration footprint.

Set the mode with the `--hashi-metadata-mode` flag on `gateway-create-migration` or `gateway-update-migration`. For full flag reference, see the [Automatic Migration CLI Reference](https://docs.akeyless.io/docs/cli-reference-automatic-migration).

## Operational Guidance

Use a phased rollout:

1. Start with a limited migration scope in a non-production environment.
2. Validate resulting items, permissions, and application integration.
3. Expand migration scope after successful validation.
4. Monitor Gateway logs during migration and remediation.

## CLI Reference

For command-level usage and flags, use the Automatic Migration CLI reference:

* [Automatic Migration CLI Reference](https://docs.akeyless.io/docs/cli-reference-automatic-migration)
