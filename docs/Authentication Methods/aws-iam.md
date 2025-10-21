---
title: AWS IAM
excerpt: AWS Identity and Access Management (IAM)
deprecated: false
hidden: false
metadata:
  title: AWS IAM
  description: ''
  robots: index
next:
  description: >-
    Make sure to associate your new Authentication Method with an Access Role to
    grant the relevant permissions within Akeyless
---
[AWS IAM](https://aws.amazon.com/iam/) authentication method provides an automated flow to retrieve an Akeyless token for IAM principals and AWS services or resources.

<Image align="center" border={false} src="https://files.readme.io/c1f9c5b-Role_new_design.png" />

# Create an AWS IAM Authentication Method from the CLI

Let's create a new AWS IAM authentication method using the Akeyless CLI. (You can do this also from the [Akeyless Console](https://docs.akeyless.io/docs/cli-ref-auth#p-stylecolorblueaws-iamp).)

To create an AWS IAM authentication method from the CLI, run the following command:

```shell Akeyless CLI
akeyless auth-method create aws-iam \
--name <Auth Method Name> \
--bound-aws-account-id <AWS Account ID>
```

Where:

* `name`: A unique name for the authentication method. The name can include the path to the virtual folder where you want to create the new authentication method, using slash `/` separators. If the folder does not exist, it will be created together with the authentication method.

* `bound-aws-account-id`: An AWS account ID that is allowed to authenticate to Akeyless using this authentication method. (You can provide more than one AWS account ID by using this parameter in the following format: `--bound-aws-account-id AWS-ID-1 --bound-aws-account-id AWS-ID-2`.)

You can find the complete list of additional parameters for this command in the [CLI Reference - Authentication](https://docs.akeyless.io/docs/cli-reference-authentication#p-stylecolorbluecreate-auth-method-aws-iamp) section.

# Configure Akeyless CLI with the AWS IAM authentication method

To configure your CLI to work with AWS IAM authentication, run the following command **from an AWS resource**:

```shell Akeyless CLI
akeyless configure --profile default --access-id <AccessID>  --access-type aws_iam 
akeyless get-cloud-identity --cloud-provider aws_iam
```

> 📘 Least Privileged Permissions
>
> AWS IAM authentication doesn't require any privileged permissions. Ensure you have an IAM role without any privileged permissions and attach it to the resource you want to authenticate (e.g., EC2 instance).

# Create an AWS IAM authentication method in the Akeyless Console

1. Log in to the Akeyless Console and go to **Users & Auth Methods > New > AWS IAM**.

2. Define a **Name** for the authentication method, and specify the **Location** as a path to the virtual folder where you want to create the new authentication method, using slash `/` separators. If the folder does not exist, it will be created together with the authentication method.

3. Define the remaining parameters as follows:

* **Expiration Date:** Select the access expiration date. This parameter is optional. Leave it empty for access to continue without an expiration date.

* **Allowed Client IPs:** Enter a comma-separated list of CIDR blocks from which the client can issue calls to the proxy. By "client," we mean CURL, SDK, etc. This parameter is optional. Leave it empty for unrestricted access.

* **Allowed Trusted Gateway IPs:** Comma separated CIDR blocks. If specified, the Gateway using this IP range will be trusted to forward the original client IP. If empty, the Gateway's IP address will be used.

* **Audit Log Sub Claims:** Enter a comma-separated list of sub-claims keys to be included in the audit logs.

* **Bounded AWS Account IDs:** Enter a comma-separated list of AWS account IDs for which access is allowed.

* **Bounded ARNs:** Enter a comma-separated list of full IAM role ARNs for which access is allowed. For example: `arn:aws:sts:{account-id}:assumed-role/{role-name}/{resource-id}, arn:aws:iam::{account-id}:user/{user-name}`. Or use wildcard characters like `*` or `?`  to grant multiple roles within a single ARN Role. For example,`arn:aws:sts:us-east-?:123456789012:*` would allow any IAM role in the AWS account to login to `us-east` regions. This parameter is optional. Leave it empty for unrestricted access.

* **Bounded Role Names:** Enter a comma-separated list of AWS role names for which access is allowed. This parameter is optional. Leave it empty for unrestricted access.

* **Bounded Role IDs:** Enter a comma-separated list of AWS role IDs for which access is allowed. This parameter is optional. Leave it empty for unrestricted access.

* **Bounded User names:** Enter a comma-separated list of usernames for which access is allowed. This parameter is optional. Leave it empty for unrestricted access.

* **Custom STS Endpoint:** Default value is `https://sts.amazonaws.com`.

* **Unique Identifier:** Optional, a unique identifier (ID) value that contains details uniquely identifying that resource. This sub-claim name is used to distinguish between different identities.

4. Click **Finish**.

# AWS Instance Metadata Service

By default, [Instance Metadata Service](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/configuring-instance-metadata-service.html) (IMDSv2) enforces a hop limit of 1, which means the metadata token used for cloud identity (such as IAM role credentials) must be accessed directly from the **EC2 instance** that initiated the session.

If the Akeyless Gateway runs in a different network context (e.g., inside a container), it may fail to authenticate using the `aws_iam` authentication method because this hop limitation.

To resolve this, you can increase the allowed number of network hops by modifying the `http-put-response-hop-limit` parameter. This can be done via the **AWS CLI** or the **AWS Management Console**.

The following command increases Hop Limit to `2`:

```shell
aws ec2 modify-instance-metadata-options \
  --instance-id <instance-id>  \
  --http-put-response-hop-limit 2
```

This allows the metadata token to be accessed from within nested network environments, such as containers, while still maintaining **IMDSv2's** security benefits.

# Tutorial

Check out our tutorial video on [AWS IAM Authentication and Access](https://tutorials.akeyless.io/docs/aws-iam-authentication-and-access).
