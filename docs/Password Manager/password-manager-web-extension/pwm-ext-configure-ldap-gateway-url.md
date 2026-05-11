---
title: Configure LDAP Gateway URL

slug: pwm-ext-configure-ldap-gateway-url
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
Use this setting when the extension should authenticate through an LDAP gateway.

## Configure the LDAP Gateway URL

![LDAP Gateway URL field in web extension settings](https://files.readme.io/51e6e76-Screenshot_2024-02-25_at_14.48.30.png)

1. Open the extension sign-in screen.
2. Open the three-dot menu.
3. Go to **Advanced Options**.
4. Turn on **LDAP**.
5. Enter the required LDAP gateway URL.
6. Click **Save**.

![Save button for LDAP gateway URL settings](https://files.readme.io/2914cb3-Screenshot_2024-02-25_at_14.47.48.png)

## Use the LDAP Sign-In Flow

After saving the LDAP gateway URL, return to the sign-in flow and use the authentication option that matches the organization's LDAP configuration.

## Validation

Confirm that the extension reaches the expected LDAP-backed sign-in flow and that users can authenticate with the expected credentials.

> 📘 **For admins**
>
> To configure the LDAP authentication method on the Akeyless platform, see [LDAP Authentication Method](https://docs.akeyless.io/docs/auth-with-ldap).
