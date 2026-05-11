---
title: Configure Custom and Specific Tenant

slug: pwm-ext-configure-custom-specific-tenant
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
Use this setting when the extension should connect to a specific tenant URL instead of the default environment.

![Custom tenant URL field in web extension settings](https://files.readme.io/72e4da3-Screenshot_2024-03-20_at_11.10.38.png)

## Configure a Custom Tenant URL

1. Open the extension sign-in screen.
2. Open the three-dot menu.
3. Go to **Advanced Options**.
4. Turn on **Vault URL**.
5. Enter the tenant URL required for the environment.
6. Click **Save**.

## When to Use This Setting

Use a custom tenant URL when:

* The organization uses a specific vault endpoint.
* Users must connect to a non-default environment.
* The sign-in flow should be directed to an environment-specific hostname.

## Validation

After saving the setting, return to the sign-in flow and confirm that authentication uses the intended tenant endpoint.

> 📘 **For admins**
>
> To pre-configure the tenant URL for managed browser deployments, see [Enterprise Distribution and Pre-Configured Authentication](https://docs.akeyless.io/docs/pwm-ext-enterprise-distribution-preconfigured-authentication).
