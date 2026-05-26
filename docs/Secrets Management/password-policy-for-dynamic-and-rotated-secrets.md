---
title: Password Policy for Dynamic and Rotated Secrets
slug: password-policy-for-dynamic-and-rotated-secrets
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

## Common Password Policy Controls

Depending on the producer or rotated secret type, available controls can include:

* Password length
* Whether password policy is enabled
* Character class requirements, such as uppercase, lowercase, numbers, and special characters

> ℹ️ **Info:**
>
> Available fields vary by producer and rotated secret type. Use the relevant command reference for your secret type to confirm exact flags.

## Dynamic Secrets

For Dynamic Secrets, configure password policy options in the create or update command for the specific producer you are using.

For command syntax and producer-specific flags, see [CLI Reference - Dynamic Secrets](https://docs.akeyless.io/docs/cli-reference-dynamic-secrets#create).

## Rotated Secrets

For Rotated Secrets, configure password policy options in the create or update command for the specific rotated secret type.

For command syntax and type-specific flags, see [CLI Reference - Rotated Secrets](https://docs.akeyless.io/docs/cli-reference-rotated-secrets#create).
