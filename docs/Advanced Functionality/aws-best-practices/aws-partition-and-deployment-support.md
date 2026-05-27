---
title: AWS Partition and Deployment Support
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
This page documents AWS partition guidance and deployment pattern coverage for AWS IAM authentication with Akeyless.

## AWS Partition Support

Akeyless supports AWS IAM authentication across the following AWS partitions:

| AWS partition | Support status | ARN partition prefix example | STS endpoint guidance |
| --- | --- | --- | --- |
| `aws` | Supported | `arn:aws:iam::<AWS_ACCOUNT_ID>:role/<IAM_ROLE_NAME>` | If `--sts-url` is not set, Akeyless uses `https://sts.amazonaws.com`. |
| `aws-us-gov` | Expected compatible | `arn:aws-us-gov:iam::<AWS_ACCOUNT_ID>:role/<IAM_ROLE_NAME>` | Set a regional GovCloud endpoint, for example `https://sts.us-gov-west-1.amazonaws.com` or `https://sts.us-gov-east-1.amazonaws.com`. |
| `aws-cn` | Supported | `arn:aws-cn:iam::<AWS_ACCOUNT_ID>:role/<IAM_ROLE_NAME>` | Set a regional China endpoint, for example `https://sts.cn-north-1.amazonaws.com.cn` or `https://sts.cn-northwest-1.amazonaws.cn`. |

When you configure bounded ARNs (for example, `--bound-arn`), the ARN partition prefix must match the partition where the IAM principal exists.

## AWS Deployment Pattern Support

AWS IAM authentication support depends on whether the runtime can provide AWS IAM workload credentials and can reach both Akeyless and the relevant AWS STS endpoint.

| Deployment pattern | Support status | Notes |
| --- | --- | --- |
| Amazon EC2 | Supported | Uses the instance profile role through the Instance Metadata Service. If IMDSv2 is enabled, ensure the hop limit is compatible with your runtime path. |
| AWS Lambda | Supported (credential-path compatible) | Uses the function execution role credentials provided to the Lambda runtime. Ensure the function can reach Akeyless and STS. |
| Amazon EKS | Supported | Use node IAM role or IRSA (IAM role for service account). Ensure the pod can access IAM credentials and STS. |
| Amazon ECS | Supported (credential-path compatible) | Uses standard AWS SDK credential resolution. Ensure task IAM role credentials are available to the runtime and STS is reachable. |
| AWS Fargate | Supported (credential-path compatible) | Applies to Amazon ECS and Amazon EKS Fargate profiles when task or pod IAM role credentials are available to the runtime. |
| AWS Batch | Supported (credential-path compatible) | Works when the underlying compute environment exposes IAM role credentials to the job runtime and STS is reachable. |
| AWS App Runner | Supported (credential-path compatible) | Works when the service runtime has IAM role credentials and can reach STS and Akeyless endpoints. |
| Amazon EC2 Outposts | Expected compatible | Uses the same IAM and metadata model as EC2. Validate endpoint routing and STS reachability in your Outposts network design. |
| AWS Snow Family | Conditionally supported | Supported when the workload can reach Akeyless and STS from the Snow environment. Disconnected or fully offline scenarios are not supported for AWS IAM authentication. |

Support status definitions:

* **Supported**: Explicitly validated by Akeyless.
* **Supported (credential-path compatible)**: Uses the same AWS SDK credential flow used by validated scenarios.
* **Expected compatible**: Architecture is expected to work with the same IAM/STS model, but scenario-specific validation is environment-dependent.

Additional AWS compute platforms not listed in the table (for example, AWS Elastic Beanstalk or Amazon EMR) are not currently called out in this documentation. Treat them as credential-path compatibility cases and validate runtime IAM credential availability, network routing, and STS reachability in your environment.

## AWS Scope and Coverage Sources

AWS service and region availability changes over time. To keep your deployment planning accurate, use AWS as the source of truth:

* **AWS partitions:** `aws`, `aws-us-gov`, and `aws-cn`. See [AWS Partitions](https://docs.aws.amazon.com/whitepapers/latest/aws-fault-isolation-boundaries/partitions.html).
* **AWS Regions:** See [AWS Regions](https://docs.aws.amazon.com/global-infrastructure/latest/regions/aws-regions.html).
* **AWS services by Region:** See [AWS Services by Region](https://aws.amazon.com/about-aws/global-infrastructure/regional-product-services/).
* **Compute service catalog:** See [AWS Compute Services](https://aws.amazon.com/products/compute/).
