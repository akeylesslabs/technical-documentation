---
title: Zero Knowledge
excerpt: ''
deprecated: false
hidden: false
metadata:
  title: ''
  description: ''
  robots: index
next:
  description: ''
  pages:
    - type: basic
      slug: gateway-caching
      title: Caching
---

<GatewayConfigManagementNote />

Gateway Zero-Knowledge enables customer-fragment participation for protected Gateway operations.

For architecture concepts, threat model, and distributed cryptographic workflow details, see [Zero-Knowledge Encryption SaaS Architecture](https://docs.akeyless.io/docs/zero-knowledge-architecture) and [DFC Deep Dive](https://docs.akeyless.io/docs/dfc-deep-dive).

Use this page for implementation tasks:

* Prepare prerequisites.
* Generate and back up a Customer Fragment.
* Attach the Customer Fragment to Gateway deployment.
* Create DFC keys with Customer Fragment binding.
* Configure machine-identity authentication for Gateway service-to-service flows.
* Validate and troubleshoot deployment behavior.

## Prerequisites

Before implementing Gateway Zero-Knowledge, confirm the following:

* A Gateway deployment is running and reachable from the required workloads. For deployment options, see [Gateway Overview](https://docs.akeyless.io/docs/gateway-overview).
* A Gateway authentication method and access policy are configured. For access configuration details, see [Gateway Authentication and Access](https://docs.akeyless.io/docs/gateway-authentication-and-access).
* The identity used for key creation and Gateway operations has the required permissions for DFC key management and Gateway access.
* A secure backup process is defined for Customer Fragment files and values.
* Required network routes to Gateway and Akeyless SaaS services are available. For connectivity requirements, see [Gateway Network Connectivity](https://docs.akeyless.io/docs/gateway-network-connectivity).

## Implementation

Use the following sequence to implement Gateway Zero-Knowledge across interfaces and infrastructures.

### Step 1: Generate a Customer Fragment (CLI)

```shell
akeyless gen-customer-fragment --name <CF-Name> --description MyFirstCF --json
```

For command parameters and additional examples, see [CLI Reference: gen-customer-fragment](https://docs.akeyless.io/docs/cli-reference-encryption-keys#gen-customer-fragment).

Example output:

```json
{
  "customer_fragments": [
    {
      "id": "cf-xyzxyzxyzxyzxyzxyz",
      "value": "SomE/CUstOmer/FrAGMenTvALue==",
      "description": "MyFirstCF",
      "name": "<CF-Name>"
    }
  ]
}
```

Save the output as `customer_fragments.json`.

Customer Fragments are generated through CLI workflows (or the HSM integration flow), then referenced by Gateway and key-creation workflows. Gateway Console key-creation flows select existing Customer Fragments.

> ⚠️ **Warning:**
>
> Back up Customer Fragments securely. Encryption keys created with a Customer Fragment cannot be reconstructed without it.

### Step 2: Attach the Customer Fragment to the Gateway

Use these deployment-specific implementation anchors for direct navigation:

* Docker: [Authentication](https://docs.akeyless.io/docs/gateway-docker-advanced-configuration#authentication), [API Key Authentication](https://docs.akeyless.io/docs/gateway-docker-advanced-configuration#api-key-authentication), [Certificates Authentication](https://docs.akeyless.io/docs/gateway-docker-advanced-configuration#certificates-authentication)
* Helm: [Authentication](https://docs.akeyless.io/docs/gateway-deploy-kubernetes-helm#authentication), [API Key Authentication](https://docs.akeyless.io/docs/gateway-deploy-kubernetes-helm#api-key-authentication), [Certificates](https://docs.akeyless.io/docs/gateway-deploy-kubernetes-helm#certificates)
* Serverless AWS: [Authentication](https://docs.akeyless.io/docs/gateway-deploy-serverless-aws#authentication), [Customer Fragment](https://docs.akeyless.io/docs/gateway-deploy-serverless-aws#customer-fragment)
* Serverless Azure: [Authentication](https://docs.akeyless.io/docs/gateway-deploy-serverless-azure#authentication), [Customer Fragment](https://docs.akeyless.io/docs/gateway-deploy-serverless-azure#customer-fragment)
* Docker Compose: [Authentication](https://docs.akeyless.io/docs/gateway-deploy-docker-compose#authentication), [API Key Authentication](https://docs.akeyless.io/docs/gateway-deploy-docker-compose#api-key-authentication), [Certificates Authentication](https://docs.akeyless.io/docs/gateway-deploy-docker-compose#certificates-authentication)

#### Standalone Docker

Mount `customer_fragments.json` into `/home/akeyless/.akeyless/customer_fragments.json`:

```shell
docker run -d -p 8000:8000 -p 5696:5696 \
  -v /path/to/customer_fragments.json:/home/akeyless/.akeyless/customer_fragments.json \
  -e GATEWAY_ACCESS_ID="identity-access-id" \
  -e GATEWAY_ACCESS_KEY="identity-access-key" \
  --name akeyless-gw akeyless/base:latest-akeyless
```

For compatibility with older deployments, legacy variables such as `ADMIN_ACCESS_ID` and `ADMIN_ACCESS_KEY` can still appear.

#### Kubernetes with Helm

Create a Kubernetes Secret that contains the `customer-fragments` key:

```shell
kubectl create secret generic gateway-customer-fragments \
  --from-file=customer-fragments=./customer_fragments.json
```

Reference that secret in Helm values:

```yaml values.yaml
globalConfig:
  customerFragmentsExistingSecret: gateway-customer-fragments
```

For full platform setup flows, see [Kubernetes with Helm Deployment](https://docs.akeyless.io/docs/gateway-deploy-kubernetes-helm).

#### Other Infrastructures

* [Docker Compose Deployment](https://docs.akeyless.io/docs/gateway-deploy-docker-compose)
* [Serverless AWS Deployment](https://docs.akeyless.io/docs/gateway-deploy-serverless-aws)
* [Serverless Azure Deployment](https://docs.akeyless.io/docs/gateway-deploy-serverless-azure)
* [Azure Container App Deployment](https://docs.akeyless.io/docs/gateway-deploy-azure-container-app)

### Step 3: Create a DFC Key Bound to the Customer Fragment

> ⚠️ **Warning:**
>
> To create a DFC key with Customer Fragment, the identity in use must be allowed in the Gateway access policy.

### Create DFC Key from the Akeyless Console

1. Open the Gateway Console at `https://<gateway-url>:8000/console`.
2. Go to **Items**.
3. Select **New**, then **Encryption Key**, then **DFC**.
4. Specify key parameters, then select the Customer Fragment.
5. Select **Save**.

### Create Zero Knowledge Key from the Akeyless CLI

```shell
akeyless create-dfc-key --name MyKeyWithMyCF --alg AES256GCM -f <customer-fragment-id>
```

Where:

* `name`: DFC key name.
* `alg`: DFC key algorithm.
* `customer-frg-id`: Customer Fragment ID used for the DFC key.

For command parameters and additional examples, see [CLI Reference: create-dfc-key](https://docs.akeyless.io/docs/cli-reference-encryption-keys#create-dfc-key).

Example output:

```text
A new AES256GCM key named MyKeyWithMyCF was successfully created
```

### Step 4 (Optional): Set a Default Encryption Key in Gateway

Set a default encryption key in Gateway configuration when all newly created items in this Gateway context should use a specific key by default.

> ℹ️ **Note:**
>
> Only symmetric keys with `AESGCM` algorithm can be set as default encryption keys.

1. Go to **Gateways**, then the relevant Gateway, then **Manage Gateway**.
2. Go to **Defaults**.
3. Select a key in **Default Encryption Key**.
4. Select **Save Changes**.

## Machine Identity Authentication Mapping

This section lists the supported machine-identity authentication methods for Gateway Zero-Knowledge service-to-service flows.

Authentication methods not listed in this mapping are outside this Gateway service-to-service scope.

Use this mapping to select a supported method and jump to the corresponding implementation guidance:

| Method | Typical workload context | Implementation reference |
| --- | --- | --- |
| API key | Workloads that can securely store and rotate access keys | [Authenticate with API key](https://docs.akeyless.io/docs/auth-with-api-key) |
| Cloud IAM (AWS, Azure, GCP) | Cloud-native services using platform identity | [Authenticate with AWS](https://docs.akeyless.io/docs/auth-with-aws), [Authenticate with Azure](https://docs.akeyless.io/docs/auth-with-azure), [Authenticate with GCP](https://docs.akeyless.io/docs/auth-with-gcp) |
| Kubernetes service account | In-cluster workloads using Kubernetes-native identity | [Authenticate with Kubernetes](https://docs.akeyless.io/docs/auth-with-kubernetes) |
| Certificate-based authentication | Workloads using client certificate trust chains | [Authenticate with certificate](https://docs.akeyless.io/docs/auth-with-certificate) |
| Universal Identity | Workloads requiring token-based machine identity across environments | [Authenticate with Universal Identity](https://docs.akeyless.io/docs/auth-with-universal-identity) |

For Gateway-specific access delegation controls, see [Gateway Authentication and Access](https://docs.akeyless.io/docs/gateway-authentication-and-access).

## Troubleshooting

### 1. Missing Customer Fragment Mount or Secret Key Name

Symptoms include missing fragment errors during CF-protected operations or deployment startup warnings.

Check these items:

* Docker: confirm `customer_fragments.json` is mounted to `/home/akeyless/.akeyless/customer_fragments.json`.
* Helm: confirm the referenced secret exists and includes key name `customer-fragments`.
* Serverless: confirm `customer_fragments` payload is valid JSON and mapped to the deployment parameter.

### 2. Insufficient Gateway Allowed Access

Symptoms include denied Gateway management actions or inability to complete required operations.

Check these items:

* Confirm the active identity is included in Gateway Allowed Access policy.
* Confirm required Gateway permissions are assigned for the intended operation scope.
* Confirm RBAC policy path permissions also allow the same operation.

### 3. Authentication Method Mismatch

Symptoms include authentication failures at Gateway startup or request-time authorization errors.

Check these items:

* Confirm auth method type matches deployment configuration (for example `access_key`, cloud IAM, certificate, or universal identity).
* Confirm required credentials, secrets, or certificates are present and mapped to expected configuration keys.
* For legacy deployments, confirm variable naming consistency when mixing `GATEWAY_*` and `ADMIN_*` conventions.

## Related Pages

* [Zero-Knowledge Encryption SaaS Architecture](https://docs.akeyless.io/docs/zero-knowledge-architecture)
* [Platform Components Overview](https://docs.akeyless.io/docs/components)
* [Gateway Overview](https://docs.akeyless.io/docs/gateway-overview)
* [Gateway Network Connectivity](https://docs.akeyless.io/docs/gateway-network-connectivity)
* [Akeyless Gateway Best Practices](https://docs.akeyless.io/docs/gateway-best-practices)
