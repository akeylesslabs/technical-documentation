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
The Terraform provider enables Terraform to utilize secrets, roles, authentication methods, and other entities from the Akeyless Platform.

Terraform can be used to configure Akeyless and populate it with secrets, as well as ensure that the state and any plans associated with the configuration are stored and communicated with care, as they will contain any values written into Akeyless in plain text.

For more information on the Terraform provider, see the <a href="https://github.com/akeyless-community/terraform-provider-akeyless" target="_blank">Akeyless GitHub Repository</a> and the <a href="https://registry.terraform.io/providers/akeyless-community/akeyless/latest" target="_blank">Terraform Registry</a>.

# Configuration

1. Install Akeyless as a provider in your Terraform Registry by adding the following code to your Terraform configuration (Terraform V0.13).

```shell
terraform {
  required_providers {
    akeyless = {
      source = "akeyless-community/akeyless"
      version = "1.3.1"
    }
  }
}
```

2. Run:

```shell
terraform init
```

2. Select an Akeyless [Authentication Method](doc:access-and-authentication-methods) to use with the  Terraform Provider, such as an **API Key** or Cloud Identity (CSP IAM) like **AWS IAM**, **Azure AD**.

# Usage Example

The following example creates an API Key authentication method called **auth-method-api-key-demo** in the **terraform-tests** folder, and a static secret called **secret** in the same folder. It uses **AWS IAM** for authentication.

To use your own [Gateway](https://docs.akeyless.io/docs/api-gw), set the `api_gateway_address`to your Gateway API port, i.e.`8081` or `8000/api/v2`:

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

To apply this request, run:

```shell
terraform apply
```

Resources can be imported from Akeyless, for example, import a static secret:

```shell
terraform import akeyless_static_secret.resorce-name /full-secret-name-in-akeyless
```