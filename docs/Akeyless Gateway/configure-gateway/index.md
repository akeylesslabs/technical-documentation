---
title: Configure Gateway
excerpt: ''
deprecated: false
hidden: false
metadata:
  title: ''
  description: ''
  robots: index
---
Use this section to configure how Akeyless Gateway authenticates, secures transport, protects encryption material, serves secrets during outages, and integrates with operational tooling.

Configuration is typically done after deployment and adjusted over time as security, compliance, and platform requirements evolve.

For ongoing Gateway configuration, use either the Gateway Configuration Manager UI or the Akeyless CLI. Avoid using deployment-time container mounts for routine configuration changes because this can cause configuration drift and TLS misconfiguration.

## Access Gateway Settings (UI)

Use the Gateway Configuration Manager to access Gateway settings from the UI:

1. Open the Akeyless SaaS Console at `https://console.akeyless.io` and sign in.
2. Or, if needed, open the Gateway Console endpoint at `<gateway-protocol>://<gateway-host>:8000/console`.
   For example, `https://gateway.example.com:8000/console`.
3. In the Console, open the **Gateway** tab and select the relevant Gateway.
4. Select **Manage Gateway** to open and change Gateway settings.

To see a Gateway in the **Gateway** list and use **Manage Gateway**, the user must have Gateway-scoped administrative permission (`scope` or `all`). Without this permission scope, the Gateway is not visible in the list, and the user cannot manage it.

Use HTTPS for remote management whenever possible.

For permission requirements, see [Gateway Authentication and Access](https://docs.akeyless.io/docs/gateway-authentication-and-access).

For inbound port and endpoint behavior, including Configure App deprecation and redirect details, see [Gateway Network Connectivity](https://docs.akeyless.io/docs/gateway-network-connectivity).

## Access Gateway Settings (CLI)

Use the Akeyless CLI to read and update Gateway settings:

```shell
akeyless gateway-get-config \
--gateway-url 'https://<Your-Akeyless-GW-URL>:8000'
```

For Gateway CLI commands and usage details, see [CLI Reference for Gateway](https://docs.akeyless.io/docs/cli-reference-gateway).

## Available Configuration Features

The following configuration features are available:

* Configure identity and authorization controls in [Gateway Authentication and Access](https://docs.akeyless.io/docs/gateway-authentication-and-access).

* Configure HTTPS behavior and certificate usage in [TLS Settings](https://docs.akeyless.io/docs/gateway-tls-settings).

* Review cryptography profile and coverage details in [PQC Support Reference](https://docs.akeyless.io/docs/gateway-pqc-support-reference).

* Manage trusted private CAs in [Certificate Store](https://docs.akeyless.io/docs/gateway-certificate-store).

* Configure encryption posture with customer fragments in [Zero Knowledge](https://docs.akeyless.io/docs/gateway-zero-knowledge).

* Define cache and offline behavior in [Gateway Caching](https://docs.akeyless.io/docs/gateway-caching).

* Route audit and operational logs in [Log Forwarding](https://docs.akeyless.io/docs/gateway-log-forwarding).

* Integrate external hardware key management in [HSM Integration](https://docs.akeyless.io/docs/gateway-hsm-integration).

* Configure migration workflows in [Automatic Migration](https://docs.akeyless.io/docs/gateway-automatic-migration).

## Next Steps

* Set up monitoring and dashboards in [Telemetry and Metrics](https://docs.akeyless.io/docs/gateway-telemetry-and-metrics).
* Prepare incident playbooks with [Troubleshooting the Gateway](https://docs.akeyless.io/docs/gateway-troubleshooting-the-gateway).
