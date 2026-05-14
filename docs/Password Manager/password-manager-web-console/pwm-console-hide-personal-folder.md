---
title: Hide Personal Folder

slug: pwm-console-hide-personal-folder
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
The Hide Personal Folder feature provides administrators with the ability to control the visibility of the Personal Folder for end users. This setting is accessible through a simple toggle in the Akeyless Password Manager console, and is also configurable by way of the [CLI](https://docs.akeyless.io/docs/cli-reference#update-account-settings).

Use this control to enforce organization-wide folder visibility policy.

## Behavior

### Admin-Only Control

Only users with admin privileges can manage the visibility of the personal folder across the organization. This ensures centralized and secure control over sensitive areas of the interface.

### Default States

* **Existing Users:** The personal folder toggle will be enabled by default, meaning the folder is visible. Admins can disable it at any time.
* **New Users:** The toggle will be disabled by default, hiding the personal folder unless explicitly enabled by an admin.

### How to Use

1. In the Akeyless Web Console (UI) Navigate to Account Settings in the Password Manager Console.
2. Locate the “Show Personal Folder” toggle.
3. Toggle the setting on or off to control visibility for your organization.
