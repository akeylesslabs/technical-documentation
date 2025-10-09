---
title: AWS Roles for Distributed Gateway Using Terraform
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
# Overview

This article outlines the steps to integrate your AWS account with Akeyless [Gateway](https://docs.akeyless.io/docs/api-gw), along with instructions for AWS Organization integration with relevant member accounts. This guide provides a [Terraform](https://developer.hashicorp.com/terraform) script to create the required AWS IAM roles that grant the Gateway IAM permissions in your AWS environment when operating in a distributed deployment, where each Gateway manages a single AWS account.

# Prerequisites

To successfully integrate your AWS accounts with Akelyess, ensure the following prerequisites are met:

For Organization integration, ensure you have an existing AWS environment with AWS Organizations enabled. If you need to create one, refer to the [AWS Organizations](https://docs.aws.amazon.com/organizations/latest/userguide/orgs_getting-started.html) user guide.

1. Access to the AWS management account. Ensure you have access to your AWS management account.

2. AWS IAM sign-in permissions.

3. [Terraform](https://developer.hashicorp.com/terraform) Installed.

4. An [AWS IAM](https://docs.akeyless.io/docs/aws-iam) authentication method & [Access Role](https://docs.akeyless.io/docs/rbac) on your Akeyless account, this [Authentication Method](https://docs.akeyless.io/docs/access-and-authentication-methods) can support many AWS accounts. Alternatively, you can create a dedicated auth method per account, ending with a unique access ID per account. In both cases, the [RBAC](https://docs.akeyless.io/docs/rbac) in Akeyless can isolate the access permissions inside Akeyless per account. 

# Create the required IAM roles

In this step, you will connect to your AWS management account to apply using a Terraform template that will create the IAM role that enables the **Akeyless Gateway** to:

* Create and manage [AWS Dynamic Secrets](https://docs.akeyless.io/docs/aws-producer)
* Rotate existing IAM credentials using [AWS Rotated Secret](https://docs.akeyless.io/docs/create-an-aws-rotated-secret)
* Operate the [AWS Universal Secrets Connector](https://docs.akeyless.io/docs/aws-universal-secrets-connector)

## Provide the parameters to identify your AWS Organization

Sign in to the AWS Management Console of your management account. Navigate to **Organizations** → **Organize accounts**.

Copy your **AWS Management Account ID** and paste it into the field.`management_account`

# Configuration

The following steps will be used to deploy a distributed deployment.

## Terraform variables

Set the `env_vars.tf` file to set your AWS account details, as well as declaring the name of the AWS Role that will be created.

```yaml env_vars.tf
variable "role_name" {
  description = "The AWS IAM Role name to be created and managed by Terraform"
  type        = string
  default     = "terraform-akeyless-role"
}

variable "region" {
  description = "The AWS region where the IAM role will be provisioned"
  type        = string
  default     = "<aws-region>"
}

variable "management_account" {
  description = "The AWS account ID in which the IAM role will be created"
  type        = string
  default     = "123456789012"
}
```

## Terraform module

The `main.tf` file will create an AWS Role with permissions for managing secrets using [USC](https://docs.akeyless.io/docs/aws-universal-secrets-connector) as well as creating [Dynamic](https://docs.akeyless.io/docs/aws-producer) and [Rotated](https://docs.akeyless.io/docs/create-an-aws-rotated-secret) secrets:

```yaml main.tf
data "aws_iam_policy_document" "trust" {
  # Management account root + self-assume (via condition)
  statement {
    effect  = "Allow"
    actions = ["sts:AssumeRole"]

    principals {
      type        = "AWS"
      identifiers = ["arn:aws:iam::${var.management_account}:root"]
    }

    condition {
      test     = "StringEquals"
      variable = "aws:PrincipalArn"
      values   = [
        "arn:aws:iam::${var.management_account}:role/${var.role_name}"
      ]
    }
  }

  # Allow EC2 service
  statement {
    effect  = "Allow"
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["ec2.amazonaws.com"]
    }
  }
}

resource "aws_iam_role" "this" {
  name               = var.role_name
  assume_role_policy = data.aws_iam_policy_document.trust.json
}

data "aws_iam_policy_document" "unified" {
  statement {
    sid    = "AkeylessSecrets"
    effect = "Allow"
    actions = [
      "iam:CreateUser", "iam:DeleteUser", "iam:TagUser", "iam:UntagUser",
      "iam:CreateAccessKey", "iam:DeleteAccessKey", "iam:ListAccessKeys",
      "iam:CreateLoginProfile", "iam:GetLoginProfile", "iam:DeleteLoginProfile",
      "iam:AttachUserPolicy", "iam:DetachUserPolicy",
      "iam:ListUserPolicies", "iam:ListAttachedUserPolicies",
      "iam:AddUserToGroup", "iam:RemoveUserFromGroup", "iam:ListGroupsForUser",
      "iam:ListUserTags", "iam:ListUsers"
    ]
    resources = ["arn:aws:iam::${var.management_account}:user/*"]
  }

  statement {
    sid     = "AkeylessUSC"
    effect  = "Allow"
    actions = [
      "secretsmanager:ListSecrets",
      "secretsmanager:GetSecretValue",
      "secretsmanager:DescribeSecret",
      "secretsmanager:CreateSecret",
      "secretsmanager:UpdateSecret",
      "secretsmanager:DeleteSecret",
      "secretsmanager:PutSecretValue",
      "secretsmanager:UntagResource",
      "secretsmanager:TagResource"
    ]
    resources = ["*"]
  }

  statement {
    sid     = "AkeylessUSCAccess"
    effect  = "Allow"
    actions = [
      "secretsmanager:UntagResource", "secretsmanager:DescribeSecret",
      "secretsmanager:GetSecretValue", "secretsmanager:PutSecretValue",
      "secretsmanager:CreateSecret", "secretsmanager:UpdateSecret",
      "secretsmanager:DeleteSecret", "secretsmanager:TagResource"
    ]
    resources = [
      "arn:aws:secretsmanager:${var.region}:${var.management_account}:secret:*"
    ]
  }

  # Self-assume permissions
  statement {
    sid    = "SelfAssume"
    effect = "Allow"
    actions = ["sts:AssumeRole"]
    resources = [
      "arn:aws:iam::${var.management_account}:role/${var.role_name}"
    ]
  }
}

resource "aws_iam_policy" "this" {
  name   = "${var.role_name}-policy"
  policy = data.aws_iam_policy_document.unified.json
}

resource "aws_iam_role_policy_attachment" "attach" {
  role       = aws_iam_role.this.name
  policy_arn = aws_iam_policy.this.arn
}

```

## Run the Deployment

1. Run `terraform init && terraform apply`.  
2. Create an [AWS Target](https://docs.akeyless.io/docs/aws-targets) in Akeyless using the **Gateway Cloud ID** option.  
3. Use that target whenever you create a **Dynamic Secret**, **Rotated Secret**, or **USC** .
