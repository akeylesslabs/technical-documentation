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

## Configuration Scope

Automatic migration configuration usually includes:

* Source system connection parameters.
* Authentication credentials or identity settings.
* Migration mode and target path strategy.
* Conflict handling behavior for existing items.

## Operational Guidance

Use a phased rollout:

1. Start with a limited migration scope in a non-production environment.
2. Validate resulting items, permissions, and application integration.
3. Expand migration scope after successful validation.
4. Monitor Gateway logs during migration and remediation.

## Security Guidance

* Use least-privilege credentials for source access.
* Avoid broad admin permissions when migration-specific permissions are sufficient.
* Rotate temporary migration credentials after the migration window closes.

## CLI Reference

For command-level usage and flags, use the Automatic Migration CLI reference:

* [Automatic Migration CLI Reference](https://docs.akeyless.io/docs/cli-reference-automatic-migration)
