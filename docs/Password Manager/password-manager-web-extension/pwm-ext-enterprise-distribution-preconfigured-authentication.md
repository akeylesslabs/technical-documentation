---
title: Enterprise Distribution with Preconfigured Authentication

slug: pwm-ext-enterprise-distribution-preconfigured-authentication
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
Use this enterprise deployment pattern to prefill authentication fields in the Akeyless Password Manager browser extension. The workflow helps IT teams reduce first-login friction and guide users to approved authentication methods.

The workflow in this page is based on internal guidance captured in DOCS-688 and is validated for managed Chromium deployments.

## Prerequisites

Before preparing a managed extension package, confirm the following:

* The organization has a validated browser-extension distribution method.
* The required Akeyless authentication method is enabled in the target account.
* The IT team has the Access ID and target authentication method values.
* The IT team has a staging environment to validate sign-in before broad rollout.

## Configuration File Example

The following example pre-fills Access ID and restricts authentication to OIDC:

```json
{
  "enabled": true,
  "prefillAccessId": "<ACCESS_ID>",
  "preferredAuthMethod": "oidc",
  "allowedAuthMethods": ["oidc"],
  "installationSource": "bundled_prefill"
}
```

## Chromium-Based Browsers (Chrome and Edge)

Use this flow for Chrome, Edge, and other Chromium-based browsers:

1. Install the Akeyless Password Manager extension from the browser store.
2. Open `chrome://version/` and copy the profile path.
3. Open the profile directory on the local machine.
4. Locate the folder for the Akeyless extension ID.
5. Open the folder for the installed extension version.
6. Copy the version folder to a working directory.
7. Update `preconfigured_install.json` with organization-specific values.
8. Package the updated folder and distribute it with the internal software-delivery process.
9. Validate first-login behavior in a test user profile.

> ⚠️ **Warning:**
>
> Repackaged browser extensions should be distributed only through approved internal enterprise channels.

Browser-signing requirements, update-channel behavior, and endpoint-management policy configuration are outside the scope of this workflow.

## Firefox

Firefox support should be validated separately through the organization's Firefox enterprise deployment process.

At this stage, this page does not prescribe a Firefox-specific file path, packaging method, or policy key set.

## Validation Checklist

After deployment, verify the following outcomes:

* The extension opens with prefilled authentication values.
* Only approved authentication methods are available.
* Users can complete authentication without manual endpoint customization.
* Login telemetry and audit behavior match organizational requirements.

## Troubleshooting

If prefilled authentication does not appear, check these areas:

* The deployed package includes the updated `preconfigured_install.json` file.
* JSON syntax is valid and values are in lowercase where required.
* The configured authentication method is enabled for the target account.
* The browser is running the expected extension build and version.
* Internal endpoint or policy restrictions are not overriding extension behavior.

## Scope Notes

The extension-level pre-configured authentication workflow does not define browser-signing requirements, browser policy templates, or endpoint-management platform configuration.
