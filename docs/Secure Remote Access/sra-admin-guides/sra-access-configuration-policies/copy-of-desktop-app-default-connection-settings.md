---
title: Copy of Desktop App Default Connection Settings
deprecated: false
hidden: true
metadata:
  robots: index
---
Use this page to configure Gateway-managed defaults for Secure Remote Access (SRA) Desktop Application connectivity.

These defaults are exposed through the SRA desktop-app configuration surface and are used by desktop clients as fallback connection values.

Use these defaults to keep desktop connectivity behavior consistent when target-level values are missing or incomplete.

## Configuration Scope

Desktop-app defaults include:

* Default SSH Certificate Issuer.
* Secure Web Access URL.
* Secure Web Proxy URL.

In Gateway configuration, these are managed under the desktop-app SRA path.

## Before You Configure

Confirm the following first:

1. You are using the unified Gateway control API endpoint (`:8000`).
2. The SSH Certificate Issuer you plan to set as default is SRA-enabled.
3. Dispatcher and proxy URLs match your active Zero Trust Web Access (ZTWA) topology.
4. Desktop clients in your environment are expected to use fallback defaults.

If target items already define full desktop connection fields, those item-level values can still take precedence in user flows.

## API Endpoints

Desktop-app configuration uses these API endpoints:

* GET `https://<gateway-url>:8000/config/sra/desktop_app`
* PUT `https://<gateway-url>:8000/config/sra/desktop_app`

For API request and response structure, see [Update Gateway Remote Access Desktop App](https://docs.akeyless.io/reference/gatewayupdateremoteaccessdesktopapp).

## Recommended Configuration Flow

Use this sequence for rollout:

1. Read current desktop defaults from Gateway.
2. Decide and validate the default SSH Certificate Issuer.
3. Set dispatcher and proxy URLs used by desktop web-access workflows.
4. Update desktop-app defaults through the `PUT` endpoint.
5. Validate from at least one Windows client and one macOS client in your environment.

### Example Workflow

```shell
# 1) Read existing desktop defaults
curl -X GET "https://<gateway-url>:8000/config/sra/desktop_app"

# 2) Update desktop defaults
curl -X PUT "https://<gateway-url>:8000/config/sra/desktop_app" \
  -H "Content-Type: application/json" \
  -d '{
    "sshCertIssuer": "<ssh-cert-issuer-name>",
    "secureWebAccessUrl": "https://<dispatcher-host>:9000",
    "secureWebProxyUrl": "https://<dispatcher-host>:19414"
  }'
```

Adjust field names and payload shape to match the current API reference for your deployed version.

## Practical Usage Pattern

Use Gateway-managed desktop defaults when:

1. You want consistent desktop connection bootstrap values across teams.
2. You need a centrally managed fallback certificate issuer for desktop SSH flows.
3. You want to predefine Web Access and Web Proxy URLs for desktop users.

These values complement, not replace, item-level SRA policy and user authorization controls.

## Validation Checklist

After configuration update:

1. Re-run `GET /config/sra/desktop_app` and confirm expected values.
2. Launch a desktop SSH flow and confirm the default issuer is used when item-level issuer is absent.
3. Launch a desktop web-access flow and confirm dispatcher or proxy URL behavior matches expected mode.
4. Confirm users with valid permissions can connect without manually overriding defaults.

If validation fails, verify URL reachability, issuer configuration, and user permissions before changing additional settings.

## Operational Notes

* Keep desktop default URLs aligned with your active SRA and ZTWA topology.
* Validate that the selected default certificate issuer is SRA-enabled and policy-compatible.
* Revalidate desktop defaults after migration from legacy split deployment to unified Gateway deployment.

## Troubleshooting Pointers

If desktop connections fail after a default update:

1. Check whether the fallback defaults were actually used for the attempted target.
2. Verify dispatcher or proxy URL reachability from user networks.
3. Confirm issuer permissions and SRA enablement state.
4. Review desktop client logs and compare with gateway-side session signals.

For client-side setup and mapping behavior, see [Desktop Application](https://docs.akeyless.io/docs/sra-desktop-application).

For runtime diagnostics and health signals, see [Cluster and Instance Health](https://docs.akeyless.io/docs/sra-cluster-and-instance-health).