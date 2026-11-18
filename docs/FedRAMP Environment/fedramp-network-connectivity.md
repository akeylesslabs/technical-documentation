---
title: FedRAMP Network Connectivity
deprecated: false
hidden: true
metadata:
  robots: index
---
Endpoints, ports, and firewall rules for connecting to the Akeyless FedRAMP environment.

The Akeyless FedRAMP environment is reached through its own domain, `fedramp.akeyless.io`, instead of the commercial `akeyless.io` domain. Gateways, the CLI, SDKs, and the Console connect outbound over HTTPS (443). Nothing is initiated from the hosted environment into your network.

For Gateway ports in your own network (inbound from your clients), see [Gateway Network Connectivity](https://docs.akeyless.io/docs/gateway-network-connectivity). Those ports are the same in both environments.

## Summary of Requirements

| Requirement                         | Value                              |
| ----------------------------------- | ---------------------------------- |
| Direction                           | Outbound from your network only    |
| Destination                         | `*.fedramp.akeyless.io`            |
| Port and protocol                   | TCP 443, HTTPS                     |
| TLS                                 | TLS 1.2 minimum, TLS 1.3 preferred |
| Inbound from the hosted environment | None                               |

<Callout icon="📘" theme="info">
  ### Note

  Allow the single wildcard domain `*.fedramp.akeyless.io` rather than individual IP addresses. Hostnames resolve to infrastructure in AWS GovCloud, and IP addresses can change. The certificate authentication endpoint is the exception, because it uses static IP addresses. See [Certificate Authentication Endpoint](#certificate-authentication-endpoint).
</Callout>

## FedRAMP Endpoints

Replace the commercial `akeyless.io` domain with `fedramp.akeyless.io`. Hostnames follow the pattern `<service>.fedramp.akeyless.io`.

| Service                    | Endpoint                                                                                                           | Port | Description                                                                                                                                           |
| -------------------------- | ------------------------------------------------------------------------------------------------------------------ | ---- | ----------------------------------------------------------------------------------------------------------------------------------------------------- |
| Console                    | `https://console.fedramp.akeyless.io`                                                                              | 443  | Web Console. Sign-in goes through the hosted-provider IdP. See [FedRAMP Account Onboarding](https://docs.akeyless.io/docs/fedramp-account-onboarding) |
| API                        | `https://api.fedramp.akeyless.io`                                                                                  | 443  | REST API endpoint used by the CLI, SDKs, Terraform, and Gateways                                                                                      |
| REST (legacy)              | `https://rest.fedramp.akeyless.io`                                                                                 | 443  | Legacy REST endpoint                                                                                                                                  |
| Vault                      | `https://vault.fedramp.akeyless.io`                                                                                | 443  | User and access management endpoint                                                                                                                   |
| Authentication             | `https://auth.fedramp.akeyless.io`                                                                                 | 443  | Authentication service                                                                                                                                |
| Certificate authentication | `https://auth-cert.fedramp.akeyless.io`                                                                            | 443  | Mutual-TLS (client certificate) authentication. Uses static IP addresses                                                                              |
| Audit                      | `https://audit.fedramp.akeyless.io`                                                                                | 443  | Audit log API                                                                                                                                         |
| Gateway services           | `https://gator.fedramp.akeyless.io`                                                                                | 443  | Request routing                                                                                                                                       |
| Key fragment services      | `https://kfm1.fedramp.akeyless.io`<br />`https://kfm2.fedramp.akeyless.io`<br />`https://kfm3.fedramp.akeyless.io` | 443  | Required for Zero-Knowledge and DFC-backed operations                                                                                                 |
| Vault proxy                | `https://hvp.fedramp.akeyless.io`                                                                                  | 443  | Hashicorp Vault Proxy endpoint, also used for the documentation redirect                                                                              |
| Auth relay                 | `https://auth-relay.fedramp.akeyless.io`                                                                           | 443  | Authentication relay                                                                                                                                  |

Read-only variants of some services are also published under the same domain, and are covered by the wildcard rule.

<Callout icon="📘" theme="info">
  ### Note

  Akeyless Customer Success confirms the exact hostnames for Staging and Production in your onboarding package. Verify them against this table before changing your firewall.
</Callout>

## Certificate Authentication Endpoint

Client-certificate authentication terminates mutual TLS on a dedicated endpoint with static IP addresses:

```text
https://auth-cert.fedramp.akeyless.io
```

If your clients use the certificate Auth Method and egress through an IP-based allow list, request the current static IP addresses from your Akeyless Customer Success team. For all other endpoints, allow the domain.

## Connectivity From Your Environment

| Source                      | Destination                                        | Port               | Notes                                                                                    |
| --------------------------- | -------------------------------------------------- | ------------------ | ---------------------------------------------------------------------------------------- |
| Gateway                     | `*.fedramp.akeyless.io`                            | 443                | Outbound only. A Gateway connects only to its own environment's control plane            |
| CLI, SDKs, Terraform, CI/CD | `api.fedramp.akeyless.io` or your Gateway URL      | 443                | See [FedRAMP CLI Configuration](https://docs.akeyless.io/docs/fedramp-cli-configuration) |
| Console users (browser)     | `console.fedramp.akeyless.io` and your Gateway URL | 443 / Gateway port | The browser must also reach your Gateway for Gateway-backed Console features             |
| Gateway                     | Your targets, SIEM, and cloud providers            | Per target         | Traffic to targets stays inside your network                                             |
| Audit logs                  | Gateway to your SIEM                               | Per SIEM           | Forwarded directly from each Gateway                                                     |

## Optional Integrations and Egress Policy

Integrations that run **from your Gateway** reach your targets from inside your network, so they work as they do in the commercial environment.

Integrations that would run **from the hosted control plane** are subject to the FedRAMP boundary's egress policy. Share the list of such targets with Akeyless before onboarding so that the connections can be declared. See [FedRAMP Feature Availability](https://docs.akeyless.io/docs/fedramp-feature-availability).

## Proxies and TLS Inspection

- If your network uses an HTTP(S) proxy, configure the Gateway and CLI to use it, and allow `*.fedramp.akeyless.io` through it.
- Do not perform TLS inspection on traffic to `*.fedramp.akeyless.io`, because it breaks the client-certificate authentication and can break Gateway connectivity.
- Requests pass through a web application firewall, and excessive request rates can be rate limited. If you see `429` or `403` responses from a CI/CD job that authenticates in a tight loop, reuse tokens until they expire.

## Verify Connectivity

From a host in the network that will run the Gateway or the CLI:

```shell
curl -sS -o /dev/null -w "%{http_code}\n" https://api.fedramp.akeyless.io
```

A successful TLS handshake and an HTTP response confirm that the endpoint is reachable. Repeat for `console.fedramp.akeyless.io` and the key fragment hosts (`kfm1`, `kfm2`, `kfm3`).

## Troubleshooting

| Symptom                                | Likely cause                                                                        | Action                                                                                                                  |
| -------------------------------------- | ----------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------- |
| Connection times out                   | Egress to `*.fedramp.akeyless.io` is blocked                                        | Allow outbound TCP 443 to the domain                                                                                    |
| TLS errors or unknown certificate      | TLS inspection or an outdated trust store                                           | Exempt the domain from inspection, and update the CA bundle                                                             |
| Gateway cannot reach the control plane | The Gateway is configured with a commercial URL, or `kfm` hosts are blocked         | Check the Gateway's API URL. See [FedRAMP Gateway Deployment](https://docs.akeyless.io/docs/fedramp-gateway-deployment) |
| Certificate authentication fails       | Static IPs not allowed, or the client certificate is not trusted by the Auth Method | Allow the static IPs and verify the certificate configuration                                                           |
