---
title: Terraform Provider
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
The Terraform provider enables Terraform to use secrets, roles, authentication methods, and other entities from the Akeyless Platform.

Terraform can be used to configure Akeyless and populate it with secrets, as well as ensure that the state and any plans associated with the configuration are stored and communicated with care, as they will contain any values written into Akeyless in plain text.

For more information on the Terraform provider, see the [Akeyless GitHub Repository](https://github.com/akeyless-community/terraform-provider-akeyless) and the [Terraform Registry](https://registry.terraform.io/providers/akeyless-community/akeyless/latest).

## Configuration

1. Install Akeyless as a provider in your Terraform Registry by adding the following code to your Terraform configuration (Terraform V0.13).

    ```shell
    terraform {
    required_providers {
        akeyless = {
        source = "akeyless-community/akeyless"
        version = "2.0.1"
        }
    }
    }
    ```

2. Run:

    ```shell
    terraform init
    ```

3. Select an Akeyless [Authentication Method](https://docs.akeyless.io/docs/access-and-authentication-methods) to use with the Terraform Provider, such as an **API Key** or Cloud Identity (CSP IAM) like **AWS IAM**, **Azure AD**.

## Usage Example

The following example creates an API Key authentication method called **auth-method-api-key-demo** in the **terraform-tests** folder, and a static secret called **secret** in the same folder. It uses **AWS IAM** for authentication.

To use your own [Gateway](https://docs.akeyless.io/docs/gateway-overview), set the `api_gateway_address` to your Gateway API port, which is `8081` or `8000/api/v2`:

```shell
provider "akeyless" {
  api_gateway_address = "https://api.akeyless.io"
  
  aws_iam_login {
    access_id = "YOUR AWS IAM access ID"
  }
}

resource "akeyless_auth_method_api_key" "api_key" {
  name = "/terraform-tests/auth-method-api-key-demo"
}

resource "akeyless_static_secret" "secret" {
  path = "/terraform-tests/secret"
  value = "this value was set from terraform"
}

data "akeyless_static_secret" "secret" {
  depends_on = [
    akeyless_static_secret.secret
  ]
  path = "/terraform-tests/secret"
}

output "secret" {
  value     = data.akeyless_static_secret.secret
  sensitive = true
}

output "auth_method" {
  value     = akeyless_auth_method_api_key.api_key
  sensitive = true
}
```

To apply this configuration, run:

```shell
terraform apply
```

Resources can be imported from Akeyless, for example, import a static secret:

```shell
terraform import akeyless_static_secret.resource-name /full-secret-name-in-akeyless
```

## DigiCert Target

Provider version 2.0.1 introduces the `akeyless_target_digicert` resource, which allows you to manage a DigiCert ACME target in Akeyless.

### Required arguments

| Argument | Type | Description |
| --- | --- | --- |
| `name` | String | Target name |
| `email` | String | Email address for ACME account registration |

### Optional arguments

| Argument | Type | Description |
| --- | --- | --- |
| `acme_challenge` | String | ACME challenge type. Options: `dns` |
| `description` | String | Description of the object |
| `digicert_url` | String | DigiCert ACME endpoint. Options: `us-production`, `eu-production`, `us-demo`, `eu-demo` |
| `dns_target_creds` | String | Name of an existing cloud target for DNS credentials. Required when challenge type is `dns`. Supported providers: AWS, Azure, GCP |
| `eab_hmac_key` | String (Sensitive) | External Account Binding HMAC key (required for ACME account bootstrap on create) |
| `eab_key_id` | String | External Account Binding key identifier (required for ACME account bootstrap on create) |
| `gcp_project` | String | GCP Cloud DNS project ID (optional; can be derived from service account) |
| `hosted_zone` | String | AWS Route53 hosted zone ID. Required when DNS credentials target is AWS |
| `keep_prev_version` | String | Whether to keep the previous version (`true`/`false`). If not set, uses account default |
| `key` | String | Name of a key used to encrypt the target secret value. If empty, the account default protection key is used |
| `max_versions` | String | Maximum number of versions, limited by account settings defaults |
| `resource_group` | String | Azure resource group name. Required when DNS credentials target is Azure |
| `timeout` | String | Timeout for challenge validation |

### Example

```shell
resource "akeyless_target_digicert" "digicert_target" {
  name           = "/targets/digicert-prod"
  email          = "admin@example.com"
  digicert_url   = "us-production"
  acme_challenge = "dns"
  dns_target_creds = "/targets/aws-dns-creds"
  hosted_zone    = "Z1234567890ABC"
  eab_key_id     = "your-eab-key-id"
  eab_hmac_key   = "your-eab-hmac-key"
}
```

## Upgrading to v2.0

Provider v2.0.0 removed resources and parameters that were deprecated in v1.5.0. Before upgrading from v1.x, update your configuration as follows:

| Deprecated (removed in v2.0) | Replacement |
| --- | --- |
| `akeyless_producer_*` resources | `akeyless_dynamic_secret_*` resources |
| `akeyless_rotated_secret` (generic) | `akeyless_rotated_secret_<type>` resources |
| `metadata` and `comment` parameters | `description` parameter |

## Changelog

For the full version history, see the [Akeyless Terraform Provider Changelog](https://changelog.akeyless.io/tf).
