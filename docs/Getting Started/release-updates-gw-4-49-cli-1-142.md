---
title: Release Updates - Gateway 4.49.0 and CLI 1.142.0
excerpt: ''
deprecated: false
hidden: false
metadata:
  title: ''
  description: ''
  robots: index
---
This page summarizes documentation updates for Akeyless Gateway `4.49.0` and Akeyless CLI `1.142.0`.

## Feature updates

### Target delete protection

Targets support delete protection to help prevent accidental deletion.

For configuration details, see:

* [Targets](https://docs.akeyless.io/docs/targets)
* [Secret and Target Locking](https://docs.akeyless.io/docs/secret-and-target-locking)

### Password item separation from Static Secret

Password items are documented as an independent item type and should be managed separately from Static Secrets.

For related documentation, see:

* [Passwords](https://docs.akeyless.io/docs/passwords)
* [Static Secrets](https://docs.akeyless.io/docs/static-secrets)

### Universal Secrets Connector filtering and scale improvements

Universal Secrets Connector supports:

* Pagination support for Azure Universal Secrets Connector list operations.
* Prefix-based filtering for all Universal Secrets Connectors.
* Tag-based filtering for Azure Universal Secrets Connector.

For command usage, see:

* [Azure Universal Secrets Connector](https://docs.akeyless.io/docs/azure-universal-secrets-connector)
* [CLI Reference - Universal Secrets Connector](https://docs.akeyless.io/docs/cli-reference-universal-secrets-connector)

### CLI default profile commands

CLI now includes profile-selection commands to manage the active profile.

For command details, see:

* [CLI](https://docs.akeyless.io/docs/cli)

## Bug fix updates

### Certificate Store config watcher behavior

Gateway behavior for Certificate Store change handling has been stabilized to avoid indefinite polling.

For Certificate Store operations, see:

* [Certificate Store](https://docs.akeyless.io/docs/gateway-certificate-store)

### /api/auth-url/token request handling

Gateway proxy behavior for `/api/auth-url/token` avoids oversized-header failures by relying on request body payloads.

### Universal Secrets Connector value display in read mode

Read-mode value display behavior for Universal Secrets Connector has been corrected.

For usage details, see:

* [Azure Universal Secrets Connector](https://docs.akeyless.io/docs/azure-universal-secrets-connector)

### Custom TLS with non-root Gateway image

Gateway stability with custom TLS certificates on non-root images has been improved.

For deployment and operational guidance, see:

* [Gateway best practices](https://docs.akeyless.io/docs/gateway-best-practices)
* [Gateway troubleshooting](https://docs.akeyless.io/docs/gateway-troubleshooting-the-gateway)

## UX and UI updates

Creation wizard experience has been updated as part of this release cycle.
