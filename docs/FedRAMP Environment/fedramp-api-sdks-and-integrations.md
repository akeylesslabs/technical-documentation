---
title: FedRAMP API, SDKs, and Integrations
deprecated: false
hidden: false
metadata:
  robots: index
---
Change the endpoint in the Akeyless API, SDKs, Terraform, and integrations to work with the FedRAMP environment.

Every Akeyless client that talks to the platform has a configurable API or Gateway URL. For the FedRAMP environment, set that URL to the FedRAMP API endpoint, or to your Gateway, and use credentials from your FedRAMP account. No other change to your code is required.

| Value        | Commercial                    | FedRAMP                                              |
| ------------ | ----------------------------- | ---------------------------------------------------- |
| API endpoint | `https://api.akeyless.io`     | `https://api.fedramp.akeyless.io`                    |
| Gateway URL  | `https://<gateway-host>:8000` | `https://<gateway-host>:8000` (your FedRAMP Gateway) |

## REST API

Send requests to the FedRAMP API endpoint.

```shell
curl -X POST https://api.fedramp.akeyless.io/auth \
  -H "Content-Type: application/json" \
  -d '{"access-id": "<FEDRAMP_ACCESS_ID>", "access-type": "api_key", "access-key": "<FEDRAMP_ACCESS_KEY>"}'
```

## SDKs

Set the host or base URL when you create the client.

Python

```python
import akeyless

configuration = akeyless.Configuration(host="https://api.fedramp.akeyless.io")
client = akeyless.ApiClient(configuration)
api = akeyless.V2Api(client)
```

Go

```go
client := akeyless.NewAPIClient(&akeyless.Configuration{
    Servers: []akeyless.ServerConfiguration{
        {URL: "https://api.fedramp.akeyless.io"},
    },
}).V2Api
```

Node.js

```javascript
const akeyless = require('akeyless');

const client = new akeyless.ApiClient();
client.basePath = 'https://api.fedramp.akeyless.io';
const api = new akeyless.V2Api(client);
```

## Terraform

Set the provider's API Gateway address.

```hcl
provider "akeyless" {
  api_gateway_address = "https://api.fedramp.akeyless.io"

  api_key_login {
    access_id  = var.fedramp_access_id
    access_key = var.fedramp_access_key
  }
}
```

If the Terraform workflow manages Gateway-backed items (targets, dynamic secrets, rotated secrets), point the provider at your Gateway URL instead.

## Kubernetes, CI/CD, and Other Integrations

For integrations that run in your environment, such as the Kubernetes Secrets Injector, the External Secrets Operator provider, and CI/CD plugins:

1. Create the Auth Method in the **FedRAMP** account.
2. Set the integration's API or Gateway URL to the FedRAMP endpoint or your FedRAMP Gateway.
3. Make sure the runner or cluster can reach `*.fedramp.akeyless.io` over HTTPS (443). See [FedRAMP Network Connectivity](https://docs.akeyless.io/docs/fedramp-network-connectivity).

<Callout icon="📘" theme="info">
  ### Note

  Use the Gateway URL, rather than the hosted API endpoint, for integrations that read secrets at high volume. Reads of cached secrets are served by the Gateway inside your network.
</Callout>

## Authentication Methods for Workloads

Workloads authenticate directly with Akeyless, not through the hosted-provider IdP. Choose the Auth Method that matches the workload. See [FedRAMP Feature Availability](https://docs.akeyless.io/docs/fedramp-feature-availability) for the methods available in your environment.

| Workload                             | Typical Auth Method                                  |
| ------------------------------------ | ---------------------------------------------------- |
| Scripts and CI/CD                    | API Key                                              |
| Workloads running on AWS             | AWS IAM                                              |
| Clients that use client certificates | Certificate, through `auth-cert.fedramp.akeyless.io` |

## Troubleshooting

| Symptom                               | Likely cause                                            | Action                                                                                                                              |
| ------------------------------------- | ------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------- |
| `401` or invalid Access ID            | A commercial Access ID, or a commercial URL             | Use FedRAMP credentials and the FedRAMP URL together                                                                                |
| Certificate authentication fails      | Wrong endpoint, or static IPs not allowed               | Use `auth-cert.fedramp.akeyless.io`. See [FedRAMP Network Connectivity](https://docs.akeyless.io/docs/fedramp-network-connectivity) |
| Works in Staging, fails in Production | Staging credentials or hostnames are used in Production | Use the Access ID and endpoints for the target environment                                                                          |
