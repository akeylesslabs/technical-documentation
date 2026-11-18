---
title: FedRAMP Gateway Deployment
deprecated: false
hidden: true
metadata:
  robots: index
---
Deploy the Akeyless Gateway in your own environment and connect it to the FedRAMP control plane.

The Gateway for the FedRAMP environment is the same image and the same Helm chart as the commercial Gateway. You deploy and operate it in your own landing zones (GovCloud VPCs, on-premises, or other networks). The only required change is the URL of the control plane that the Gateway connects to.

<Callout icon="📘" theme="info">
  ### Note

  A Gateway connects only to its own environment. A Gateway deployed for the FedRAMP environment cannot serve commercial accounts, and a commercial Gateway cannot serve FedRAMP accounts. Deploy separate Gateways for each.
</Callout>

## What Changes for the Gateway

| Setting                 | Commercial                                                                                                        | FedRAMP                           |
| ----------------------- | ----------------------------------------------------------------------------------------------------------------- | --------------------------------- |
| Control plane (API) URL | `https://api.akeyless.io`                                                                                         | `https://api.fedramp.akeyless.io` |
| Admin Access ID and key | From the commercial account                                                                                       | From the FedRAMP account          |
| Outbound connectivity   | `*.akeyless.io`, TCP 443                                                                                          | `*.fedramp.akeyless.io`, TCP 443  |
| Inbound connectivity    | From your clients, per [Gateway Network Connectivity](https://docs.akeyless.io/docs/gateway-network-connectivity) | Same                              |
| Gateway image           | Latest stable or quarterly LTS                                                                                    | Same image. FIPS mode is optional |

Everything else, including authentication methods, targets, dynamic and rotated secrets, Secure Remote Access, and Kubernetes integrations, is configured the same way.

## Prerequisites

- A FedRAMP account, with an Auth Method and an Access ID for the Gateway. See [FedRAMP Account Onboarding](https://docs.akeyless.io/docs/fedramp-account-onboarding).
- A Kubernetes cluster in your landing zone, with enough capacity for three or more Gateway replicas across availability zones.
- Outbound HTTPS (443) from the cluster to `*.fedramp.akeyless.io`. See [FedRAMP Network Connectivity](https://docs.akeyless.io/docs/fedramp-network-connectivity).
- Network access from your clients and Console users to the Gateway.

## Deploy With Helm

1. Add the Akeyless Helm repository:

   ```shell
   helm repo add akeyless https://akeylesslabs.github.io/helm-charts
   helm repo update
   ```

2. Create a `values.yaml` file that sets the FedRAMP Access ID and control plane URL:

   values.yaml

   ```yaml
   # Gateway admin identity: an Auth Method in the FedRAMP account
   akeylessUserAuth:
     adminAccessId: "<FEDRAMP_ADMIN_ACCESS_ID>"
     adminAccessKey: "<FEDRAMP_ADMIN_ACCESS_KEY>"

   clusterName: "fedramp-gateway"

   # Control plane URL: set to the FedRAMP API endpoint
   # TODO: confirm the exact chart key / environment variable for the control plane URL
   <CONTROL_PLANE_URL_SETTING>: "https://api.fedramp.akeyless.io"
   ```

3. Install the Gateway:

   ```shell
   helm install gw akeyless/akeyless-api-gateway -f values.yaml
   ```

4. Verify that the Gateway is healthy and registered. In the FedRAMP Console, go to **Gateways**, and confirm that the Gateway appears with a connected status.

## Deploy With Environment Variables (Docker)

For non-Kubernetes deployments, set the same value as an environment variable on the container.

```shell
# TODO: confirm the exact environment variable name for the control plane URL
-e <CONTROL_PLANE_URL_VARIABLE>="https://api.fedramp.akeyless.io"
```

## Customer Fragment

On first key creation, the Gateway generates your Customer Fragment. It is custodied in your environment and is never sent to the hosted control plane, so the control plane cannot assemble a complete key. You can optionally anchor the Customer Fragment to a FIPS 140-3 Level 3 HSM.

## Resilience

- Deploy three or more replicas across availability zones, with autoscaling.
- Enable **Cluster Cache** so that the Gateway continues to serve cached static secrets, issue dynamic secrets, and validate existing sessions during a control plane outage.
- New workloads that authenticate for the first time still depend on the authentication service in the FedRAMP environment. During an outage, administration is degraded, but application access to cached secrets continues.

## Audit Logs and SIEM

Forward audit logs from each Gateway directly to your SIEM, and manage retention there. See the Gateway log forwarding guide for the available destinations.

## Upgrades

Gateway releases are applied by you, on your schedule. They are not gated by the hosting provider's validation pipeline, because the Gateway runs in your environment, outside the hosted authorization boundary. Review the Gateway release notes before you upgrade.

## Troubleshooting

| Symptom                                    | Likely cause                                                                            | Action                                                                                         |
| ------------------------------------------ | --------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------- |
| The Gateway does not appear in the Console | It is connecting to the commercial URL, or the Access ID belongs to another environment | Check the control plane URL and the Access ID                                                  |
| Authentication fails at startup            | The Auth Method, Access ID, or key is wrong, or was created in the other environment    | Create the Auth Method in the FedRAMP account and update the values                            |
| Gateway logs show timeouts to `kfm` hosts  | Egress to `*.fedramp.akeyless.io` is blocked                                            | See [FedRAMP Network Connectivity](https://docs.akeyless.io/docs/fedramp-network-connectivity) |
| Console features that use the Gateway fail | The browser cannot reach the Gateway URL                                                | Allow access from user networks to the Gateway                                                 |