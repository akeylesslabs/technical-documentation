---
title: TeamCity Plugin
excerpt: ''
deprecated: false
hidden: false
metadata:
  title: ''
  description: ''
  robots: index
---
The TeamCity Plugin integrates TeamCity with Akeyless so your builds can retrieve secrets directly from the Akeyless API without storing sensitive values in TeamCity.

If you are deciding between TeamCity integration paths:

* [TeamCity Plugin](https://docs.akeyless.io/docs/teamcity-akeyless-plugin): Native Akeyless TeamCity plugin that connects directly to the Akeyless API.
* [TeamCity Plugin by way of HashiCorp Vault Proxy](https://docs.akeyless.io/docs/teamcity-hcv-plugin): HashiCorp Vault-compatible integration path through the Akeyless HashiCorp Vault Proxy.

Use the native plugin for new implementations.

Use the HashiCorp Vault Proxy plugin path if you need compatibility with existing Vault-based TeamCity workflows.

JetBrains Marketplace: [Akeyless Secrets Management](https://plugins.jetbrains.com/plugin/30559-akeyless-secrets-management)

Repository: [akeyless-community/teamcity-akeyless-plugin](https://github.com/akeyless-community/teamcity-akeyless-plugin)

## Features

* Native TeamCity integration for Akeyless secrets retrieval
* Support for static, dynamic, and rotated secrets
* Per-build token flow
* Sensitive value masking in TeamCity logs
* Input validation for API URL and secret path

## Prerequisites

1. TeamCity Server 2024.12 or later.
2. Akeyless authentication method with permissions to read the target secrets.
3. Network connectivity from TeamCity Server to your Akeyless API endpoint.

## Install the Plugin

### Install from TeamCity Marketplace

Marketplace page: [Akeyless Secrets Management](https://plugins.jetbrains.com/plugin/30559-akeyless-secrets-management)

1. In TeamCity, go to **Administration > Plugins**.
2. Select **Browse plugins repository**.
3. Search for `Akeyless Secrets Management`.
4. Install the plugin and restart TeamCity Server.

### Install from ZIP

1. Build or download the plugin ZIP.
2. In TeamCity, go to **Administration > Plugins**.
3. Select **Upload plugin zip**.
4. Upload the ZIP file and restart TeamCity Server.

## Configure a TeamCity Connection

1. Open your TeamCity project.
2. Go to **Connections**.
3. Select **Add Connection**.
4. Choose **Akeyless Secrets Management**.
5. Configure the connection values:

* **Display Name**: Friendly name for the TeamCity connection.
* **API URL**: Akeyless API endpoint (default: `https://api.akeyless.io`).
* **Access ID**: Akeyless Access ID.
* **Authentication Method**: Select one of the supported methods.
* **Credentials**: Provide fields required by the selected method.

## Supported Authentication Methods

* Access Key
* Kubernetes
* AWS IAM
* Azure AD
* GCP
* Certificate (Certificate Data or Certificate File Path)

## Use Secrets in Build Parameters

Use the `akeyless:` prefix for remote secret parameters.

The same parameter structure is used for static, dynamic, and rotated secrets.

Example:

```text
akeyless:/production/database-password
```

Kotlin DSL example:

```kotlin
params {
    param("env.DATABASE_PASSWORD", "akeyless:/production/database-password")
    param("env.API_KEY", "akeyless:/production/api-key")
}
```

## Troubleshooting

### Authentication fails

* Verify `Access ID` and credential values.
* Verify the authentication method is configured in Akeyless and has the required role permissions.
* Verify the API URL is reachable from TeamCity Server.

### Secret resolution fails

* Verify the secret path is correct and starts with `/`.
* Verify the connection identity has access to the target secret.
* Review TeamCity Server logs for plugin-side errors.

### API URL validation errors

* Use a valid API host URL.
* Use `https` for production endpoints.
* If testing with localhost, use `http://localhost`.

## Restored Visuals

![Restored visual: TC Dynamic3](https://files.readme.io/fb23889-TC-Dynamic3.png)

![Restored visual: TC GenSettings](https://files.readme.io/359e8ae-TC-GenSettings.png)
