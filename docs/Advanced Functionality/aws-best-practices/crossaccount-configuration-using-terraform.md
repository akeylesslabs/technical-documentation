---
title: CrossAccount configuration Using Terraform
excerpt: ''
deprecated: false
hidden: true
metadata:
  title: ''
  description: ''
  robots: index
next:
  description: ''
---
This guide will demonstrate how to use **Terraform** in order to create 2 roles in AWS in different accounts, and using one Akeyless Gateway to create resources as a cross-account deployment.

# Prerequisites

- Akeyless Gateway
- Terraform installed

# Management Account Configuration

First, we will create the [IAM-Role](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles.html) in the resource account using terraform:

```yaml main.tf
terraform {
  required_version = ">= 1.3.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 5.0"
    }
  }
}

provider "aws" {
  region  = var.region
  profile = var.profile
}

#############################
# TRUST POLICY 
#############################
data "aws_iam_policy_document" "trust" {
  statement {
    sid     = "AllowAssumeRole"
    effect  = "Allow"
    actions = ["sts:AssumeRole"]

    principals {
      type        = "AWS"
      identifiers = ["arn:aws:iam::${var.management_account}:root"]
    }

    condition {
      test     = "ArnEquals"
      variable = "aws:PrincipalArn"
      values   = ["arn:aws:iam::${var.management_account}:role/${var.role_name}"]
    }
  }

  statement {
    sid     = "AllowDestinationToAssume"
    effect  = "Allow"
    actions = ["sts:AssumeRole"]

    principals {
      type        = "AWS"
      identifiers = ["arn:aws:iam::${var.destination_account_id}:root"]
    }
  }

  # Allow EC2 to assume
  statement {
    sid     = "AllowEC2Assume"
    effect  = "Allow"
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["ec2.amazonaws.com"]
    }
  }
}

#################
# CREATE THE ROLE
#################
resource "aws_iam_role" "this" {
  name               = var.role_name
  assume_role_policy = data.aws_iam_policy_document.trust.json
}

##############################################
# PERMISSIONS POLICY (mirrors your permissions)
##############################################
data "aws_iam_policy_document" "permissions" {
  statement {
    sid     = "AssumeSelf"
    effect  = "Allow"
    actions = ["sts:AssumeRole"]
    resources = [
      "arn:aws:iam::${var.management_account}:role/${var.role_name}"
    ]
  }

  statement {
    sid     = "AssumeDestinationRole"
    effect  = "Allow"
    actions = ["sts:AssumeRole"]
    resources = [
      "arn:aws:iam::${var.destination_account_id}:role/${var.destination_role_name}"
    ]
  }

  statement {
    sid     = "ManageTmpUsersInAccountA"
    effect  = "Allow"
    actions = [
      "iam:DeleteAccessKey",
      "iam:AttachUserPolicy",
      "iam:DeleteUser",
      "iam:ListUserPolicies",
      "iam:CreateUser",
      "iam:TagUser",
      "iam:CreateAccessKey",
      "iam:CreateLoginProfile",
      "iam:RemoveUserFromGroup",
      "iam:AddUserToGroup",
      "iam:ListGroupsForUser",
      "iam:ListAttachedUserPolicies",
      "iam:DetachUserPolicy",
      "iam:GetLoginProfile",
      "iam:DeleteLoginProfile",
      "iam:ListUserTags",
      "iam:ListAccessKeys"
    ]
    resources = [
      "arn:aws:iam::${var.management_account}:user/tmp.*"
    ]
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
}

#############################
# CREATE & ATTACH THE POLICY
#############################
resource "aws_iam_policy" "this" {
  name   = "${var.role_name}-policy"
  policy = data.aws_iam_policy_document.permissions.json
}

resource "aws_iam_role_policy_attachment" "attach" {
  role       = aws_iam_role.this.name
  policy_arn = aws_iam_policy.this.arn
}

######################
# Output: ROLE ARN
######################
output "role_arn" {
  value       = aws_iam_role.this.arn
  description = "Created IAM Role ARN"
}

```
```yaml vars.tf
variable "management_account" {
  description = "AWS Management Account ID"
  type        = string
  default     = ""
}

variable "region" {
  description = "AWS region"
  type        = string
  default     = ""
 }

variable "role_name" {
  description = "IAM role name that will be created in the Management Account"
  type        = string
  default     = ""
}

variable "destination_account_id" {
  description = "Destination Account ID"
  type        = string
  default     = ""
}

variable "destination_role_name" {
  description = "Role name that will be created in the destination Account"
  type        = string
  default     = ""
}



```

Run `terraform init` and `terraform apply`.

Once finish, you will have a new role in the source Account that trusts itself and the role from Account B.

In order to work with this role from Akeyless, an [AWS Target](https://docs.akeyless.io/docs/aws-targets) is required:

1. Navigate to **Targets** > **New** > **AWS**, press **Next**.
2. Give the Target a **Name** and optionally, a **Location**, Press **Next**.
3. Choose **Use Gateway's Cloud Identity** and click **Finish**

# Destination Account Configuration

In order to have a centralized Gateway that will be able to manage resources in multiple AWS Accounts, A target in Akeyless with an [External ID](https://aws.amazon.com/blogs/apn/securely-using-external-id-for-accessing-aws-accounts-owned-by-others/) is required. 

1. Navigate to **Targets** > **New** > **AWS**, press **Next**.
2. Give the Target a **Name** and optionally, a **Location**, Press **Next**.
3. Choose **Use Gateway's Cloud Identity** and check the **External ID** option.

A new **External ID** will be generated.

> 👍 Role ARN
> 
> Once the role will be created, we will add it to the target.

## Creating the Role in the Destination Account

**In a new directory**, create the following files:

```yaml main.tf
terraform {
  required_version = ">= 1.3.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 5.0"
    }
  }
}

# Point this provider at **Destination Account**
provider "aws" {
  region  = var.region
  profile = var.profile
}

########################################
# TRUST POLICY (Destination Account, creation-safe)
########################################
data "aws_iam_policy_document" "trust" {
  statement {
    sid     = "AllowRoleBAssumeWithExternalId"
    effect  = "Allow"
    actions = ["sts:AssumeRole"]

    principals {
      type        = "AWS"
      identifiers = ["arn:aws:iam::${var.management_account}:root"] # Destination Account root
    }

    condition {
      test     = "ArnEquals"
      variable = "aws:PrincipalArn"
      values   = ["arn:aws:iam::${var.management_account}:role/${var.role_name}"]
    }

    condition {
      test     = "StringEquals"
      variable = "sts:ExternalId"
      values   = [var.external_id]
    }
  }

  statement {
    sid     = "AllowRoleAAssume"
    effect  = "Allow"
    actions = ["sts:AssumeRole"]

    principals {
      type        = "AWS"
      identifiers = ["arn:aws:iam::${var.source_account_id}:role/${var.source_role_name}"]
    }
  }

  statement {
    sid     = "AllowSelfAssume"
    effect  = "Allow"
    actions = ["sts:AssumeRole"]

    principals {
      type        = "AWS"
      identifiers = ["arn:aws:iam::${var.management_account}:root"] # Destination Account root
    }

    condition {
      test     = "ArnEquals"
      variable = "aws:PrincipalArn"
      values   = ["arn:aws:iam::${var.management_account}:role/${var.role_name}"]
    }
  }
}

#################
# CREATE THE ROLE
#################
resource "aws_iam_role" "this" {
  name               = var.role_name
  assume_role_policy = data.aws_iam_policy_document.trust.json
}

##############################################
# PERMISSIONS POLICY (mirrors your permissions)
##############################################
data "aws_iam_policy_document" "permissions" {
  statement {
    sid     = "AssumeSelf"
    effect  = "Allow"
    actions = ["sts:AssumeRole"]
    resources = [
      "arn:aws:iam::${var.management_account}:role/${var.role_name}"
    ]
  }

  statement {
    sid     = "AssumeSourceRole"
    effect  = "Allow"
    actions = ["sts:AssumeRole"]
    resources = [
      "arn:aws:iam::${var.source_account_id}:role/${var.source_role_name}"
    ]
  }

  statement {
    sid     = "ManageTmpUsersInDestinationAccount"
    effect  = "Allow"
    actions = [
      "iam:DeleteAccessKey",
      "iam:AttachUserPolicy",
      "iam:DeleteUser",
      "iam:ListUserPolicies",
      "iam:CreateUser",
      "iam:TagUser",
      "iam:CreateAccessKey",
      "iam:CreateLoginProfile",
      "iam:RemoveUserFromGroup",
      "iam:AddUserToGroup",
      "iam:ListGroupsForUser",
      "iam:ListAttachedUserPolicies",
      "iam:DetachUserPolicy",
      "iam:GetLoginProfile",
      "iam:DeleteLoginProfile",
      "iam:ListUserTags",
      "iam:ListAccessKeys"
    ]
    resources = [
      "arn:aws:iam::${var.management_account}:user/tmp.*"
    ]
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
}

#############################
# CREATE & ATTACH THE POLICY
#############################
resource "aws_iam_policy" "this" {
  name   = "${var.role_name}-policy"
  policy = data.aws_iam_policy_document.permissions.json
}

resource "aws_iam_role_policy_attachment" "attach" {
  role       = aws_iam_role.this.name
  policy_arn = aws_iam_policy.this.arn
}

######################
# OPTIONAL: ROLE ARN
######################
output "role_arn" {
  value       = aws_iam_role.this.arn
  description = "Created IAM Role ARN (Destination Account)"
}

```
```yaml vars.tf
variable "role_name" {
  description = "IAM role name for Destination Account (the one being created)"
  type        = string
  default     = ""
}

variable "source_role_name" {
  description = "Name of the IAM role in Source Account that this role should trust"
  type        = string
  default     = ""
}

variable "management_account" {
  description = "AWS Account ID where this role is created (Destination Account)"
  type        = string
  default     = ""
}

variable "source_account_id" {
  description = "AWS Account ID for Source Account (trusted account)"
  type        = string
  default     = ""
}

variable "external_id" {
  description = "ExternalId required for Destination Role assumption"
  type        = string
  default     = ""
}

variable "region" {
  description = "AWS region"
  type        = string
  default     = ""
}

variable "profile" {
  description = "AWS CLI profile for Destination Account (optional if using env creds)"
  type        = string
  default     = ""
}

```

> 👍 Note
> 
> `external_id` - take the value of the external id from the new target.

At this point, we have created the following resources:

- An IAM-Role in the source Account.
- An IAM-Role in the destination account Account.
- A target in Akeyless with an External ID

# CrossAccount Deployment

Now, we will use the roles that were created in order to manage the destination AWS account.

> 👍 Akeyless Gateway
> 
> The following Actions will take place from the Gateway that has the IAM-User from the source account assigned.
> 
> Make sure you have an [Akeyless Gateway](https://docs.akeyless.io/docs/api-gw) with the IAM Role from the source account atttached.

Connect to your Gateway - `https://public-ip>:8000`, this will automatically update the URL of your Gateway in Akelyess. 

Then, enter the GW console - `https://public-ip>:8000/console`

## Create the Dynamic Secret

This example will use **IAM_USER** mode, this will create a new temporary user in the destination account in AWS.

In Akeyless, Navigate to **Items** > **New** > **Dynamic Secret** > **AWS**.

1. Give the Dynamic Secret a name and press **Next**.
2. Choose the **Target** that was created with the **External ID**.
3. For **Access Mode**, choose **IAM_USER**.
4. For **Gateway**, choose **This Gateway** and click **Finish**.

Once the Dynamic Secret is created, press **Get Dynamic Secret**

You will get the credentials of the new temporary user that was created in the destination account, save the credentials as it will be used for the next step.

## Create a Rotated Secret

Now, we will use an AWS [Rotated Secret](https://docs.akeyless.io/docs/create-an-aws-rotated-secret).

In Akeyless, Navigate to **Items** > **New** > **Rotated Secret** > **AWS**.

1. Give the Dynamic Secret a name and press **Next**.
2. Choose the **Target** that was created with the **External ID**.
3. For **Rotator Type**, choose **API Key**.
4. For **Authenticate with the following credentials**, choose **Target Credentialds**.
5. Enter the **Access Key ID** and the **Access Key** from the last step.
6. For **Gateway**, choose **This Gateway** and click **Finish**.

Once the Rotated Secret is created, press **Rotate Secret**, and the credentials of the user that was created earlier will be rotated.