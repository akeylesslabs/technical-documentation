---
title: Enterprise Distribution with Preconfigured Authentication

slug: pwm-ext-enterprise-distribution-preconfigured-authentication
excerpt: 'Deploy the Akeyless Password Manager browser extension with preconfigured authentication fields for managed enterprise environments.'
deprecated: false
hidden: false
metadata:
  title: ''
  description: ''
  robots: index
next:
  description: ''
---
Use this enterprise deployment pattern to prefill authentication fields in the Akeyless Password Manager browser extension. This approach helps IT teams reduce first-login friction and guide users to approved authentication methods.

The process described on this page is validated for managed Chromium deployments.

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

### Configuration Fields

| Field | Type | Description |
| --- | --- | --- |
| `enabled` | boolean | Activates the preconfigured authentication feature. Set to `true` to enable. |
| `prefillAccessId` | string | The Akeyless Access ID to prefill on the sign-in screen. |
| `preferredAuthMethod` | string | The authentication method shown by default. Must be one of the values listed in `allowedAuthMethods`. Use lowercase (for example, `oidc`, `saml`, `ldap`). |
| `allowedAuthMethods` | array of strings | The set of authentication methods available to users. Valid values (use lowercase): `oidc`, `saml`, `ldap`, `email_pass`, `access_key`, `github`, `google`, `certificate`. |
| `installationSource` | string | Identifies the deployment origin. Use `bundled_prefill` for enterprise-packaged deployments. |

## Chromium-Based Browsers (Chrome and Edge)

Use this flow for Chrome, Edge, and other Chromium-based browsers:

1. Install the Akeyless Password Manager extension:
   * **Chrome**: [Akeyless Password Manager on Chrome Web Store](https://chromewebstore.google.com/)
   * **Edge**: [Akeyless Password Manager on Microsoft Edge Add-ons](https://microsoftedge.microsoft.com/addons)

   Note the extension ID (`<EXTENSION_ID>`) displayed in your browser's extensions management page.

2. Locate your browser profile directory:
   * **Chrome/Chromium**: Open `chrome://settings/help` (or `edge://settings/help` for Edge). The Profile Path is displayed in the About tab.
   * **Alternative**: Open the browser's settings, navigate to **About → About Chrome** (or Edge), and copy the Profile Path shown.
3. Open the profile directory on your local machine.
4. Navigate to `\Extensions\<EXTENSION_ID>\` (replace `<EXTENSION_ID>` with the ID from step 1).
5. Open the version folder (the numeric folder inside; for example, `\1.2.3.0\`).
6. Copy this version folder to a working directory.
7. In the copied version folder, locate the file `preconfigured_install.json`. If it does not exist, create it. Edit the file to include the configuration fields (see Configuration Fields table above), and update all values with your organization-specific settings.
8. Package the updated folder and distribute it with the internal software-delivery process.
9. Validate first-login behavior in a test user profile.

> ⚠️ **Warning:**
>
> Repackaged browser extensions should be distributed only through approved internal enterprise channels.

Browser-signing requirements, update-channel behavior, and endpoint-management policy configuration are outside the scope of this page.

## Firefox

Firefox enterprise extension deployment uses the `policies.json` file or an enterprise policy service (such as Group Policy or Jamf). The configuration storage mechanism differs from Chromium.

### Firefox Configuration Overview

Firefox managed extensions use a managed storage API instead of direct file modification. The configuration is managed through:

* **Group Policy (Windows)**: For domain-joined devices, define managed storage settings in Group Policy.
* **Jamf (macOS)**: For managed macOS devices, define managed storage settings via Jamf configuration profiles.
* **Standalone Firefox ESR**: For unmanaged deployments, place a `policies.json` file in the Firefox installation directory.

The configuration keys and format for managed storage differ from the Chromium `preconfigured_install.json` structure. The Akeyless Password Manager extension on Firefox uses the managed storage API to read configuration values.

### Steps

1. Consult the official [Firefox for Enterprise](https://support.mozilla.org/en-US/products/firefox-enterprise) documentation to determine the appropriate deployment method for your environment (Group Policy, Jamf, or standalone `policies.json`).
2. Configure the managed storage using the same field names and values as the Chromium configuration table above (for example, `enabled`, `prefillAccessId`, `preferredAuthMethod`, `allowedAuthMethods`).
3. Deploy via your enterprise policy service or update the Firefox `policies.json` file.
4. Validate that the extension reads the configuration on first launch.

## Authentication Method Selection Guide

When choosing allowed authentication methods, consider these use cases:

* **OIDC (OpenID Connect)**: Enterprise identity providers, modern cloud deployments.
* **SAML**: Legacy enterprise SSO systems, often paired with on-premises Active Directory.
* **LDAP**: On-premises LDAP/Active Directory environments without SSO gateway.
* **Email + Password**: Legacy fallback; less secure, not recommended as sole method.
* **Access Key**: Service accounts or programmatic access; restricted to specific roles.
* **GitHub, Google**: Development teams using public identity providers; less suitable for regulated environments.
* **Certificate**: Mutual TLS or certificate-based authentication; requires client certificate distribution.

Restricting to a single method (set `allowedAuthMethods` to one value) simplifies support and reduces configuration errors.

## Validation Checklist

After deployment, verify the following outcomes:

* The extension opens with prefilled authentication values on first launch.
* Only approved authentication methods appear in the sign-in dropdown.
* Users can complete authentication without manual endpoint customization.
* Check the browser's extension logs for errors: Open the extension's popup, right-click → **Inspect**, and review the Console tab for any configuration-related warnings.
* Verify that failed login attempts are logged in your identity provider's audit logs as expected.

## Troubleshooting

If prefilled authentication does not appear, check these areas:

* The deployed package includes the updated `preconfigured_install.json` file in the correct extension version folder.
* JSON syntax is valid. Use a JSON validator if needed.
* All method names and string values are **lowercase** (for example, `"preferredAuthMethod": "oidc"`, not `"Oidc"` or `"OIDC"`).
* The configured authentication method (`preferredAuthMethod`) is enabled for the target Akeyless account.
* The configured authentication method is included in the `allowedAuthMethods` array.
* The browser is running the expected extension build and version (verify in the extension's details page).
* No browser policies or security software are blocking the extension from reading the configuration file.
* For Firefox: Verify that managed storage is correctly deployed via your enterprise policy service (Group Policy, Jamf, or `policies.json`).
