---
title: sra-Desktop App Default Connection Settings
slug: sra-desktop-app-default-connection-settings
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
Use this page to configure Gateway-managed defaults for Secure Remote Access (SRA) Desktop Application connectivity.

These defaults are exposed through the SRA desktop-app configuration surface and are used by desktop clients as fallback connection values.

## Configuration Scope

Desktop-app defaults include:

* Default SSH Certificate Issuer.
* Secure Web Access URL.
* Secure Web Proxy URL.

In Gateway configuration, these are managed under the desktop-app SRA path.

## API Endpoints

Desktop-app configuration uses these API endpoints:

* GET `https://<gateway-url>:8000/config/sra/desktop_app`
* PUT `https://<gateway-url>:8000/config/sra/desktop_app`

For API request and response structure, see [Update Gateway Remote Access Desktop App](https://docs.akeyless.io/reference/gatewayupdateremoteaccessdesktopapp).

## Practical Usage Pattern

Use Gateway-managed desktop defaults when:

1. You want consistent desktop connection bootstrap values across teams.
2. You need a centrally managed fallback certificate issuer for desktop SSH flows.
3. You want to predefine Web Access and Web Proxy URLs for desktop users.

These values complement, not replace, item-level SRA policy and user authorization controls.

## Operational Notes

* Keep desktop default URLs aligned with your active SRA and ZTWA topology.
* Validate that the selected default certificate issuer is SRA-enabled and policy-compatible.
* Revalidate desktop defaults after migration from legacy split deployment to unified Gateway deployment.

For user-side desktop setup and local client mapping, see [Desktop Application](https://docs.akeyless.io/docs/sra-desktop-application).
