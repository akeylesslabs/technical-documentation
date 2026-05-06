---
title: Configure Custom/Specific Tenant
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

![Illustration for: This innovative feature enables users to personalize their web browser extension by configuring a custom or specific tenant URL. This customization is designed to tailor the…](https://files.readme.io/72e4da3-Screenshot_2024-03-20_at_11.10.38.png)

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
