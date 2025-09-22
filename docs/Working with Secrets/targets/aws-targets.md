---
title: AWS Target
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
You can define an AWS target that contains an AWS IAM principal to be used with an [AWS dynamic secrets](https://docs.akeyless.io/docs/aws-producer) or an [AWS rotated secrets](https://docs.akeyless.io/docs/create-an-aws-rotated-secret). 

In case working with an explicit **Access Key**, to follow [AWS best practices](https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html#update-access-keys), ensure to create an automatic rotation for this **Access Key** using  [AWS rotated secrets](https://docs.akeyless.io/docs/create-an-aws-rotated-secret). 

When working with [Gateway](doc:api-gw) Cloud Identity, Akeyless will use AWS SDK and its default credentials precedence. In addition, in case [External ID ](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_common-scenarios_third-party.html) is used,  make sure to add to the **AWS Role** your Gateway is using permission to assume the relevant roles in the account.

> 👍 AWS IAM Best Practices
> 
> The best practice for using IAM roles in AWS is to leverage them for granting temporary, least-privilege access to resources, rather than relying on long-term access keys for users. Use your **Gateway cloud ID** to use IAM roles.

# Create an AWS Target in the CLI

To create an AWS target from the CLI, run the following command:

```shell GW Cloud ID
akeyless target create aws \
--name <target name> \
--use-gw-cloud-identity
```
```shell Expilict creds
akeyless target create aws \
--name <target name> \
--access-key-id <AWS Access ID> \
--access-key <AWS Access Key> \
--region <AWS region>
```

Where:

- `name`: A unique name of the target. The name can include the path to the virtual folder where you want to create the new target, using slash `/` separators. If the folder does not exist, it will be created together with the target.

- `use-gw-cloud-identity`: A boolean flag to use the Gateway cloud ID to use an existing IAM role.
  - `generate-external-id[=false]`: Optional, a unique auto-generated value used in your AWS account when configuring your AWS IAM role to securely delegate access to Akeyless. Relevant only when using the Gateway cloud ID.
  - `role-arn`: Optional, AWS IAM role identifier that Gateway will assume in your AWS account, relevant only when using an external ID

Alternatively, to use IAM explicit credentials: 

- `access-key-id`: The access key ID assigned to an admin user that will be used to authenticate Akeyless with AWS.

- `access-key`: The Access Key of the admin user.

- `region`: The AWS region.

You can find the complete list of parameters for this command in the [CLI Reference - Akeyless Targets](https://docs.akeyless.io/docs/cli-ref-targets#p-stylecolorblueawsp) section.

> 👍 Use Gateway's Cloud Identity
> 
> Is relevant for cases where your Gateway is hosted on an AWS resource (i.e., EC2, EKS, ECS Fargate) that has some IAM role associated to it. Make sure the relevant IAM Role has enough permissions to perform the required actions as described in the relevant guides e.g. [AWS Dynamic Secrets](doc:aws-producer), [AWS Rotated Secret](doc:create-an-aws-rotated-secret), [AWS Universal Secrets Connector](doc:aws-universal-secrets-connector) etc.
> 
> In case you are working with explicit credentials, make sure to set a [Rotated Secret](doc:create-an-aws-rotated-secret) to meet AWS best practices.

# Create an AWS Target in the Console

1. Log in to the Akeyless Console, and go to **Targets > New > Cloud (AWS)**.

2. Define a **Name** of the target, and specify the **Location** as a path to the virtual folder where you want to create the new target, using slash `/` separators. If the folder does not exist, it will be created together with the target.

3. Select a **Protection key** with a Customer Fragment to enable Zero-Knowledge and click **Next**.  
   For more information, [read here](doc:implement-zero-knowledge).

4. Choose your preferred authentication mode by selecting one of the options:

   - Check the **Use Credentials** radio button to authenticate with the AWS admin user credentials.

   - Check the **Use Gateway's Cloud Identity** option to authenticate with local Gateway's Cloud IAM.

> 👍 Note
> 
> **Use Gateway's Cloud Identity**  is relevant for cases where your Gateway is hosted on an AWS resource (i.e., EC2, EKS, ECS Fargate) that has some IAM role associated to it. Make sure the relevant IAM Role has enough permissions to perform the required actions as described in the relevant guides e.g. [AWS Dynamic Secrets](doc:aws-producer), [AWS Rotated Secret](doc:create-an-aws-rotated-secret), [AWS Universal Secrets Connector](doc:aws-universal-secrets-connector) etc.

5. Define the remaining parameters as follows:

- **Access Key ID:** If you selected the **Use Credentials** option in the previous step, specify the Access ID assigned to the admin user you created to authenticate Akeyless with AWS. 

- **Secret Access Key:** Specify the Access Key assigned to the admin user you created to authenticate Akeyless with AWS.

- **Region:** Enter the AWS region that the temporary credentials are permitted to access.

- **Session Token:** Token is required only for temporary security credentials retrieved via STS. Otherwise, it can be left empty.

- **External ID:** Optional, A unique auto-generated value used in your AWS account when configuring your AWS IAM role to securely delegate access to Akeyless, read more [here](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_common-scenarios_third-party.html).

- **Role ARN:** Optional, when using External ID, the Role-ARN that the gateway will use. If not provided, the default role according to [AWS precedence](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-authentication.html#cli-chap-authentication-precedence) will be used.

6. Click **Finish**.

# Tutorial

Check out our tutorial video on <a href="https://tutorials.akeyless.io/docs/creating-targets" target="_blank">Creating and Configuring AWS Targets</a>.