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
slug: terraform-provider
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

To use your own [Gateway](https://docs.akeyless.io/docs/gateway-overview), set the `api_gateway_address` to your Gateway API endpoint:  `https://Your-Gateway-URL:8000/api/v2`:

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

## Upgrading to v2.0

Provider v2.0.0 removed resources and parameters that were deprecated in v1.5.0. Before upgrading from v1.x, update your configuration as follows:

| Deprecated (removed in v2.0)        | Replacement                                |
| ----------------------------------- | ------------------------------------------ |
| `akeyless_producer_*` resources     | `akeyless_dynamic_secret_*` resources      |
| `akeyless_rotated_secret` (generic) | `akeyless_rotated_secret_<type>` resources |
| `metadata` and `comment` parameters | `description` parameter                    |

## Changelog

For the full version history, see the [Akeyless Terraform Provider Changelog](https://changelog.akeyless.io/tf).
