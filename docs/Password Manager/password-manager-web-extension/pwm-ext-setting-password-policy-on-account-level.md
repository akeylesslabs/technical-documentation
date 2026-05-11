---
title: Setting Password Policy

slug: pwm-ext-setting-password-policy-on-account-level
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
Use the following steps to view and configure the password generation policy for your account in the web extension.

## Access the Password Generation Policy

![Password generation policy setting in the web extension](https://files.readme.io/dcc11c6-Screenshot_2024-01-10_at_16.43.35.png)

1. Open the extension.
2. Open the three-dot menu.
3. Select **Password generation policy**.
4. Review and update the default password-generation settings.

## Set the Account-Level Default Policy

**Character Length**: Set the default password length.

**Include Uppercase Letters (A-Z):** Require uppercase letters.

**Include Lowercase Letters (a-z):** Require lowercase letters.

**Include Numbers (0-9):** Require numbers.

**Include Special Characters (!@#):** Require special characters.

The extension supports password-generation guidance and tuning allowed special characters during generation.

These settings provide the default generation behavior. Users can still work within the limits allowed by the configured policy.

## Set the Policy for a Specific Password

You can adjust password-generation settings while creating or editing an individual password, as long as the selected values stay within the organization-level policy.

![Password policy configuration screen in the web extension](https://files.readme.io/c6ca311-Screenshot_2024-01-10_at_16.41.08.png)

### Configure Password Settings During Creation

1. Start creating a new password.
2. Open the password-generation settings.
3. Adjust the available password parameters.
4. Generate or enter the password.
5. Save the item.

### Update Password Settings During Editing

1. Open the existing password.
2. Select **Edit**.
3. Adjust the password-related settings that are available for the item.
4. Save the changes.

## Important

Item-level password settings cannot reduce the effective requirements below the account-level policy.
