---
title: AWS Serverless
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
This guide describes how to run a Serverless Gateway on AWS based on [AWS Lambda Functions](https://aws.amazon.com/pm/lambda/?gclid=CjwKCAiAudG5BhAREiwAWMlSjCcu0SVmDSXTv2B4JNN2hmpAa_w0DedQG4CLVB66ZYibg2wcw1ny8xoCgVIQAvD_BwE\&trk=3da65280-58c3-4e9f-8d04-5402461fedce\&sc_channel=ps\&ef_id=CjwKCAiAudG5BhAREiwAWMlSjCcu0SVmDSXTv2B4JNN2hmpAa_w0DedQG4CLVB66ZYibg2wcw1ny8xoCgVIQAvD_BwE:G:s\&s_kwcid=AL!4422!3!651612444455!e!!g!!amazon%20lambda!19836376555!148728891764) using HashiCorp Terraform.

# Prerequisites

* [Terraform](https://learn.hashicorp.com/tutorials/terraform/install-cli) (version 1.0.0 or later)

* Amazon AWS account

* Network port `8000` on the cluster must be open _only for internal network access_. This allows access to the following service endpoints:

| Service                                              | Endpoint   |
| :--------------------------------------------------- | :--------- |
| [Gateway Console](doc:gateway-configuration-manager) | `/console` |
| [HashiCorp Vault Proxy](doc:hashicorp-vault-proxy)   | `/hvp`     |
| Akeyless V1 REST API                                 | `/api/v1`  |
| Akeyless V2 REST API                                 | `/api/v2`  |
| [KMIP Server](doc:kmip-server)                       | `5696`     |

For example, to get to the `/api/v2` service, use this endpoint: `https://<your_serverless_gateway_url>.com/api/v2`

<Callout icon="❗️">
  _**Warning:** Make sure that this server is not globally open to the public network. The Akeyless Gateway only requires connections to Akeyless SaaS Core Services._
</Callout>

# Pre-Installation Configuration

Clone the **Serverless Gateway** repository locally:

```shell Shell
git clone https://github.com/akeyless-community/akeyless-serverless-gateway.git
```

Edit the `akeyless-serverless-gateway/terraform/AWS/serverless-gateway/lambda_env_vars.tf` file according to the sections below.

## Authentication

Set your Akeyless Gateway with a default [Authentication Method](doc:access-and-authentication-methods) to control the level of access your Akeyless Gateway will have to your Akeyless account.

The following Authentication Methods are supported for serverless mode:

* [AWS IAM](https://docs.akeyless.io/docs/aws-iam)
* [API Key](https://docs.akeyless.io/docs/api-key)

When using [AWS IAM](https://docs.akeyless.io/docs/aws-iam) as the `admin_access_id` of the Gateway, make sure to also set a list of users that are able to manage your Akeyless Gateway configuration using the `allowed_access_permissions` variable. For example:

```shell AWS_IAM
variable "admin_access_id_type" {
  description = "Set the Admin Auth Type for the Gateway"
  type        = string
  default     = "aws_iam"
}

variable "admin_access_id" {
  description = "Akeyless AWS IAM Auth Access ID"
  type        = string
  default     = "<Access ID>"
}

variable "allowed_access_permissions" {
  description =  "Akeyless allowed_access_permissions"
  type        = string
  default     = "[{\"name\": \"\", \"<Access ID>\": \"\", \"permissions\": [\"admin\"]}]"
}
```
```shell API Key
variable "admin_access_id_type" {
  description = "Set the Admin Auth Type for the Gateway"
  type        = string
  default     = "access_key"
}

variable "admin_access_id" {
  description = "Akeyless API Key Auth Access ID"
  type        = string
  default     = "<Access ID>"
}

variable "admin_access_key" {
  description = "Akeyless Admin Access Key"
  default     = "<Access Key>"
}

variable "allowed_access_permissions" {
  description = "Akeyless allowed_access_permissions"
  type        = string
  default     = "[{\"name\": \"\", \"access_id\": \"\", \"permissions\": [\"admin\"]}]"
}
```

Where:

* `admin_access_id_type`: The Auth Method type for the Gateway either  `access_key` or  `aws_iam`.

* `admin_access_id`: The **Access ID** of the Gateway default Auth Method.

* `admin_access_key`: The **Access Key** of the `admin_access_id`. **Relevant only** when `admin_access_id_type` is `access_key`.

* `allowed_access_permissions`:  A list of allowed **Access IDs**, to delegate [permissions](doc:gateway-access-permissions) users will have on your Gateway components. **Required** when `admin_access_id_type` is `aws_iam`. For example, it can be used with [API Key](https://docs.akeyless.io/docs/api-key) or [SAML](doc:saml), etc.

## Customer Fragment

To work with [Zero-Knowledge Encryption](https://docs.akeyless.io/docs/implement-zero-knowledge) edit the `customer_fragments` variable:

```shell
variable "customer_fragments"{
  type        = map(any)
  sensitive   = true
  description = ""
  default     =  {
    "customer_fragments": [
      {
        "id": "<Customer Fragment ID>",
        "value": "<Customer Fragment Value>",
        "description": "My Serverless Fragment",
        "name": "ServerLessFragment"
      }
    ]
  }
}
```

# Installation

To install the module, run the following commands:

```shell Shell
terraform init
terraform apply
```

Upon successful installation of the **Akeyless Serverless Gateway**, the following output will be generated:

```shell Shell
Outputs:

akeyless_serverless_gateway_url = "https://uh4i3r4.execute-api.<region>.amazonaws.com/default/console"
aws_api_gateway_rest_api = "arn:aws:apigateway:<region>::/restapis/uh4i3r4"
aws_lambda_function = "arn:aws:lambda:<region>:<aws-acct-id>:function:<your-serverless-gateway>"
repository_url = "<aws-acct-id>.dkr.ecr.<region>.amazonaws.com/<your>-serverless-gateway-repo-for-lambda"
```

**Note:**  If the Akeyless Serverless Gateway settings need to be updated after installation, edit the relevant values in the [Terraform files](https://github.com/akeyless-community/akeyless-serverless-gateway/tree/main/terraform/AWS/serverless-gateway) and run `terraform apply`.

# Additional Gateway Configuration

To configure your Akeyless Serverless Gateway:

1. On your browser, navigate to the URL in the first output above labeled: `akeyless_serverless_gateway_url`.
2. Enter your credentials to log in.

> 📘 Akeyless Gateway URL
>
> The default value of the `akeyless_serverless_gateway_url` ends with `/default/console` which will route you to **Akeyless Gateway Console** (Port `18888`).
>
> To connect to **Akeyless Gateway Configuration Manager** (Port `8000`) use: `/default/config`

For more information in regards to the **Serverless Gateway**, refer to the [Serverless Gateway repository](https://github.com/akeyless-community/akeyless-serverless-gateway)

**Note:** After installing the **Serverless Gateway,** it becomes accessible as a **Lambda Function** within your **AWS account**. This enables you to access comprehensive information, monitor its performance, and gain a complete overview of its functionality,  while it's possible to edit the Gateway directly from the **Lambda function**, any changes made will be overwritten during the next `terraform apply` command.

## AWS Configuration

While the `lammbda_env_vars.tf` file contains the basic configuration required for deploying the **Serverless Gateway**, You can also configure the `variables.tf` file to match your **AWS account** needs. Below are examples of configurable settings:

* `aws_profile` - Set the **AWS Profile** for authentication, the default value is `default`

* `region` - Set the **AWS region**, the default value is `us-east-2`

* `api_gw_name` Set the name of the gateway in **AWS**, default value: `akeyless-serverless-gateway-api-gateway`

* `lambda_func_name` Set the name of the lambda function in **AWS**, the default value is `akeyless-serverless-gateway`

Find more information about the available terraform [configuration files](https://github.com/akeyless-community/akeyless-serverless-gateway/tree/main/terraform/AWS/serverless-gateway).

# Upgrading the Gateway

The **Serverless Gateway** version can be updated to different versions based on your preferences, follow these steps to update the Gateway:

* Enter the [Serverless Gateway](https://github.com/akeyless-community/akeyless-serverless-gateway) repo in **GitHub**
* Go to **Lambda Docker Image Configuration** > **Selecting a Different Version**
* [View available versions](https://gallery.ecr.aws/akeyless/serverless-gateway)
* In `variables.tf` file, change the field `image-tag` to the version you desire
* Run `terraform apply`

The **Serverless Gateway** will boot with the version you chose.

# Limitations

The Akeyless Serverless Gateway does not support:

* [Kubernetes](https://docs.akeyless.io/docs/kubernetes-auth) and [LDAP](https://docs.akeyless.io/docs/ldap) Authentication Methods
* [Caching](https://docs.akeyless.io/docs/configure-the-gateway-cache)
* [Automatic Migration](https://docs.akeyless.io/docs/automatic-migration)
* Event on Gateway status change
* [TLS Configuration](doc:tls-certificate)
