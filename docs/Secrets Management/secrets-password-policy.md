---
title: Password Policy for Dynamic and Rotated Secrets
slug: secrets-password-policy
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
This page describes password policy options for supported Dynamic Secrets producers and Rotated Secret types.

Password policy controls define how generated or rotated passwords should be constructed, such as minimum length and character requirements.

## What Password Policy Controls

Password policy controls help you enforce organization standards for automatically generated credentials. Depending on secret type, you can control:

* Password length
* Character composition requirements (uppercase, lowercase, numbers, special characters)
* Whether policy enforcement is enabled for the item

Use these controls to reduce weak-password risk while keeping generation and rotation automated.

## Common Control Types

Depending on the producer or rotated secret type, available controls can include:

* Password length
* Whether password policy is enabled
* Character class requirements, such as uppercase, lowercase, numbers, and special characters

> ℹ️ **Info:**
>
> Available fields vary by producer and rotated secret type. Use the relevant command reference for your secret type to confirm exact flags.

## How To Apply Password Policy

For both Dynamic and Rotated secrets:

1. Choose the producer or rotated secret type.
2. Configure policy settings in the create or update command.
3. Validate behavior by generating credentials or triggering a rotation.

When policy settings are stricter than target-system constraints, operation failures can occur. In those cases, align password policy values with the target platform's accepted password rules.

## Dynamic Secrets

For Dynamic Secrets, configure password policy options in the create or update command for the specific producer you are using.

### Supported Dynamic Secrets Producers

The following Dynamic Secrets producer docs explicitly include password-length support:

* [Database Dynamic Secrets](https://docs.akeyless.io/docs/create-dynamic-secret-to-sql-db)
* [Azure AD Dynamic Secrets](https://docs.akeyless.io/docs/azure-ad-dynamic-secrets)
* [LDAP Dynamic Secrets](https://docs.akeyless.io/docs/ldap-dynamic-secret)
* [RabbitMQ Dynamic Secrets](https://docs.akeyless.io/docs/rabbitmq-producer)
* [Snowflake Dynamic Secrets](https://docs.akeyless.io/docs/snowflake-dynamic-secrets)
* [RDP Dynamic Secrets](https://docs.akeyless.io/docs/rdp-dynamic-secrets)
* [Chef Infra Dynamic Secrets](https://docs.akeyless.io/docs/chef-infra-producer)

### Dynamic Secrets Example

The example below demonstrates setting password length for a Dynamic Secret (when supported by the selected producer):

```shell
akeyless dynamic-secret create postgresql \
  --name /path/to/dynamic-secret \
  --target-name /path/to/target \
  --user-name <db-user-name> \
  --password-length 20
```

You can also update an existing item:

```shell
akeyless dynamic-secret update postgresql \
  --name /path/to/dynamic-secret \
  --password-length 24
```

For command syntax and producer-specific flags, see [CLI Reference - Dynamic Secrets](https://docs.akeyless.io/docs/cli-reference-dynamic-secrets#create).

## Rotated Secrets

For Rotated Secrets, configure password policy options in the create or update command for the specific rotated secret type.

### Supported Rotated Secret Types

The following Rotated Secret docs explicitly include password-length support:

* [Database Rotated Secret](https://docs.akeyless.io/docs/create-a-database-rotated-secret)
* [Docker Hub Rotated Secret](https://docs.akeyless.io/docs/create-a-docker-hub-rotated-secret)
* [LDAP Rotated Secret](https://docs.akeyless.io/docs/create-an-ldap-rotated-secret)
* [SSH Rotated Secret](https://docs.akeyless.io/docs/create-an-ssh-rotated-secret)
* [Windows Rotated Secret](https://docs.akeyless.io/docs/windows-rotated-secret)
* [Custom Rotated Secret](https://docs.akeyless.io/docs/create-a-custom-rotated-secret)

### Rotated Secrets Example

For Rotated Secrets, you can combine length and composition controls where supported:

```shell
akeyless rotated-secret create custom \
  --name /path/to/rotated-secret \
  --target-name /path/to/target \
  --password-length 20 \
  --enable-password-policy true \
  --password-policy-contains-capital-letters true \
  --password-policy-contains-lower-letters true \
  --password-policy-contains-numbers true \
  --password-policy-contains-special-characters true
```

To update policy on an existing rotated secret:

```shell
akeyless rotated-secret update custom \
  --name /path/to/rotated-secret \
  --password-length 24 \
  --enable-password-policy true
```

## Operational Notes

* Use higher password length for privileged or externally exposed systems.
* Start with target-system-compatible rules, then tighten complexity requirements gradually.
* If a rotation fails after policy changes, verify the target system supports the selected character classes.
* Keep policy rules consistent across similar environments to reduce operational drift.

For command syntax and type-specific flags, see [CLI Reference - Rotated Secrets](https://docs.akeyless.io/docs/cli-reference-rotated-secrets#create).
