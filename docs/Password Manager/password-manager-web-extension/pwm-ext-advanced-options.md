---
title: Advanced Options

slug: pwm-ext-advanced-options
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
Advanced Options provides environment-specific settings for the Password Manager Web Extension.

## Available Settings

The extension provides the following Advanced Options sections:

* Passkey Authentication
* LDAP
* Vault URL

The extension also displays the current extension version on the Advanced Options page.

## Open Advanced Options

1. Open the extension sign-in screen.
2. Open the three-dot menu.
3. Select **Advanced Options**.

## Passkey Authentication

The Passkey Authentication toggle controls whether the extension can provide passkey-based login suggestions and related authentication support.

Use this setting when the organization wants to enable or disable passkey support in the extension.

## LDAP

The LDAP section allows users to turn on LDAP-specific configuration and provide the LDAP gateway URL required for that environment.

For step-by-step instructions, see [Configure LDAP gateway URL](https://docs.akeyless.io/docs/pwm-ext-configure-ldap-gateway-url).

## Vault URL

The Vault URL section allows users to turn on a custom tenant or vault endpoint and provide the required URL.

For step-by-step instructions, see [Configure Custom/Specific Tenant](https://docs.akeyless.io/docs/pwm-ext-configure-custom-specific-tenant).

## Validation

After saving Advanced Options changes, return to the sign-in flow and confirm that the extension uses the expected environment and authentication behavior.
