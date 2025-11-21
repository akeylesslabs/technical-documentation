---
title: AWS Best practices
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
This guide outlines best practices for deploying the Akeyless [Gateway](https://docs.akeyless.io/docs/gateway-chart) following AWS security standards, with a primary focus on managing secrets cross-account AWS environments. It highlights recommended deployment models, their trade-offs, and how to manage [Dynamic Secrets](https://docs.akeyless.io/docs/aws-producer), [Rotated Secrets](https://docs.akeyless.io/docs/create-an-aws-rotated-secret), and the [Universal Secrets Connector](https://docs.akeyless.io/docs/aws-universal-secrets-connector)  using **only IAM roles** without relying on long-lived credentials.

At its core, the **Akeyless Gateway** serves as a secure execution layer that facilitates a range of operations from cryptographic processing to secure network access on behalf of the **Akeyless SaaS platform**, without exposing sensitive workloads to the public network.

When managing environments across multiple AWS accounts, the key requirement is to establish a consistent and automated approach for deploying and operating the **Akeyless Gateway** across the organization. This ensures reliable configuration, centralized control, and seamless integration of Gateway capabilities throughout all AWS member accounts.

> 👍 AWS Partner
>
> Akeyless is an [official AWS partner](https://partners.amazonaws.com/partners/0018a00001orv7AAAQ/) recognized with the Security ISV Competency.

# How Akeyless Gateway authenticates using IAM

AWS compute resources can authenticate directly to Akeyless using supported identity mechanisms. These include:\
EC2 instances, Lambda functions, ECS (Elastic Container Service) tasks, EKS (Elastic Kubernetes Service) pods (if using IAM roles for service accounts)\
These resources use AWS IAM roles to obtain temporary credentials, which Akeyless uses to validate their identity. 

When the **Gateway** is running on such a resource, it utilizes the existing identity to authenticate to Akeyless SaaS services. 

## How is this authentication implemented securely?

Akeyless supports IAM-based authentication through its [AWS IAM](https://docs.akeyless.io/docs/aws-iam) Auth method, which leverages AWS’s native **STS** (Security Token Service) and identity documents. The process is as follows:

1. The AWS resource retrieves temporary credentials from its IAM role.
2. The resource sends these credentials to Akeyless using the auth API endpoint
3. Akeyless validates the request using **AWS STS** by calling the `GetCallerIdentity` API to verify the authenticity and identity of the requester. This exchange does not expose long-term credentials and relies on short-lived tokens, ensuring secure communication. This secure flow avoids needing to manage static secrets or access keys within AWS services.

![](https://files.readme.io/f8e683e1aaa94a88ebda40de04504f4c56c8126bec5760a3289ba9a97f958444-image.png)

# How Akeyless Target should be used

All deployment patterns are working **without** any AWS long-lived credentials and should be set **only** using **AWS roles** leveraging the Akeyless [AWS Target](https://docs.akeyless.io/docs/aws-targets) via **cloud ID** option that uses the AWS role. 

When using an [AWS Target](https://docs.akeyless.io/docs/aws-targets)with the **Gateway Cloud ID** option, the Akeyless **Gateway** leverages the IAM role associated with the underlying compute service it’s running on, such as a service account role in EKS or an instance profile role attached to an EC2 instance. To extend access beyond the AWS account the Gateway is running on, the Target can be explicitly set with a **role ARN** with **External ID**, overriding the default identity behavior and allowing secure, cross-account operations. This means a single **Target** can be shared across multiple **Gateways**, with each **Gateway** operating under the permissions granted to its own associated AWS role.

> 📘 AWS Configuration and credential precedence
>
> Akelyess uses AWS official SDK, hence the role that will be used is according to [AWS precedence](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-authentication.html#cli-chap-authentication-precedence).

# Deployment patterns

As the Akelyess Gateway is a light, stateless application, it might be deployed using the following patterns according to your preference while managing an AWS organization with multiple accounts: 

* [Centralized Gateway](https://docs.akeyless.io/docs/terraform-centralized-deployment): Deploy a single **Gateway** in a “security-services” or “shared-tools” account. In each member account, create an **IAM role** that the [Gateway](https://docs.akeyless.io/docs/gateway-chart) can assume, protected with an **External ID**. Register each role as an [AWS Target](https://docs.akeyless.io/docs/aws-targets) in Akeyless. Where [Dynamic Secrets](https://docs.akeyless.io/docs/aws-producer), [Rotated Secrets](https://docs.akeyless.io/docs/create-an-aws-rotated-secret), [USC](https://docs.akeyless.io/docs/aws-universal-secrets-connector), etc., will point to that Target. This will end with 1 or more **Gateways** to manage and monitor, while keeping member accounts isolated.

<Image align="center" src="https://files.readme.io/603ecd924daae82ebfff8e8153f147779849a6d0d616e42888e8e965ba07bd2d-Flows_for_Akelyess_Target_with_Cloud_ID_and_external_ID_1.jpg" />

* [Distributed Gateways](https://docs.akeyless.io/docs/terraform-distributed-deployment): Deploy different **Gateways** in every account. Each **Gateway** works only on its local AWS account, but is managed from the same Akeyless account.

<Image align="center" src="https://files.readme.io/a3ee87d843bbeed8d385418b8e87cb87af8a574672cf3d434ce0adedad180350-Flows_for_Akelyess_Target_with_Cloud_ID_and_external_ID.jpg" />

You can find a Terraform example with the required IAM roles for these deployments in the following links:

* [AWS Roles for Centralized Gateway Using Terraform](https://docs.akeyless.io/docs/terraform-centralized-deployment)
* [AWS Roles for Distributed Gateway Using Terraform](https://docs.akeyless.io/docs/terraform-distributed-deployment)
