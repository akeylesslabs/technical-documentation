---
title: AWS Dynamic Secrets
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
You can define a dynamic AWS secret to generate AWS access credentials based on IAM policies dynamically. Those credentials are time-based and automatically get revoked when a dynamic secret's time to live expires.

You can create dynamic access credentials for AWS in two modes:

- **iam_user** mode: When a client requests a dynamic secret value, a **temporary** IAM user is created for the requested AWS account, and an access key is returned to the client. The temporary users should be assigned to an existing policy in the AWS account. Temporary IAM users can only be created with access to a single AWS account. If you have multiple AWS accounts, you will need to create a separate dynamic secret for each account for IAM user mode.
- **assumed_role** mode: When a client requests the dynamic secret value, an [AssumeRole](https://docs.aws.amazon.com/STS/latest/APIReference/API_AssumeRole.html) operation is performed to return an access key, secret key, and session token. Although a single dynamic secret can assume roles for multiple accounts, due to AWS limitations, once access is granted, it cannot be revoked before its defined expiration time (a minimum of 15 minutes and a maximum of 12 hours). Assume role is more convenient for immediate actions, as the **STS** credentials are available immediately as described in AWS [official](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_temp.html) docs.

## Prerequisites

- An [Akeyless Gateway](https://docs.akeyless.io/docs/gateway-overview)
- An [AWS Target](https://docs.akeyless.io/docs/aws-targets)
- If you are using `iam_user` mode, the minimum required policy for the user should include the following permissions:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
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
            ],
            "Resource": "arn:aws:iam::<accountID>:user/tmp.*"
        }
    ]
}
```

This role will grant the dynamic secret permissions to manage the lifecycle of the temporary IAM users' Access Keys, including creation and deletion. It will also support the setup of a temporary user with console login, adding users to groups, and utilizing AWS tags as well.

_Note:_ `tmp.*` is the default template prefix of the temporary users Akeyless creates. If you are working with a [custom username template](https://docs.akeyless.io/docs/dynamic-secrets-user-templating), make sure to adjust the allowed resource accordingly.

- If you are using `assumed_role` mode, grant the user **AssumeRole** permissions to the requested IAM roles. For more information, see the [AWS Assume Role](https://aws.amazon.com/premiumsupport/knowledge-center/iam-assume-role-cli/) documentation. The required policy for the user should include the following permissions:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": "sts:AssumeRole",
            "Resource": "arn:aws:iam::<accountID>:role/<RoleName>"
        }
    ]
}
```

where the `<RoleName>` should be replaced with the role that will be assumed.

_Note:_ Make sure that the target AWS role that will be part of the roles that this dynamic secret should be able to assume must include a trust policy with the principal of the role you created.

## Create a Dynamic AWS Secret with the CLI

<Callout icon="ℹ️" theme="info">
  ### **Note:**

  We recommend using Dynamic Secrets with [Targets](https://docs.akeyless.io/docs/aws-targets). While it saves time for multiple secret-level configurations by not requiring you to provide an [inline connection string](https://docs.akeyless.io/docs/aws-producer#inline-connection-strings) each time, it is also important for security streamlining. Using a target allows you to rotate credentials without breaking the credential chain for the objects connected to the server used, using inline will force you to go and change the credentials in each individual item instead of just the target.
</Callout>

To create a dynamic AWS secret with the CLI using an existing [AWS Target](https://docs.akeyless.io/docs/aws-targets), run the following command:

```shell
akeyless dynamic-secret create aws \
--name <secret name> \
--target-name <Target Name> \
--gateway-url 'https://<Your-Akeyless-GW-URL>:8000' \
--aws-access-mode <iam_user|assumed_role> \
--aws-user-policies <Policy ARN> \
--aws-user-groups <UserGroup name> \
--aws-role-arns <AWS Role ARNs>
```

Where:

- `name` A unique name of the dynamic secret. The name can include the path to the virtual folder where you want to create the new dynamic secret, using the slash `/` separators. If the folder does not exist, it will be created together with the dynamic secret.

- `target-name`: A name of the target that enables connection to the AWS. The name can include the path to the virtual folder where this target resides.

- `gateway-url`: Akeyless Gateway URL (port `8000`).

- `aws-access-mode`: The types of credentials to retrieve from AWS. The following options are available:

  `iam_user` or `assume_role`.

- `aws-user-policies`: Policy ARN(s). Multiple values should be separated by a comma. User will be granted these policies when the dynamic secret is created.

- `aws-user-groups`: UserGroup name(s). Multiple values should be separated by a comma.

- `aws-role-arns`: AWS Role ARNs to be used in the Assume Role operation. Multiple values should be separated by a comma.

## Fetch a Dynamic AWS Secret Value with the CLI

To fetch a dynamic AWS secret value with the CLI, run the following command:

```shell
akeyless dynamic-secret get-value --name <Path to your dynamic secret>
```

## Create a Dynamic AWS Secret in the Akeyless Console

<Callout icon="ℹ️" theme="info">
  ### **Note:**

  To start working with Dynamic Secrets from the [Akeyless Console](https://docs.akeyless.io/docs/aws-producer#create-a-dynamic-aws-secret-in-the-akeyless-console), you need to configure the Gateway URL thus enabling communication between the Akeyless SaaS and the Akeyless Gateway.
</Callout>

1. Log in to the Akeyless Console, and go to **Items > New > Dynamic Secret**.

2. Select the AWS secret type and click **Next**.

3. Define a **Name** of the dynamic secret, and specify the **Location** as a path to the virtual folder where you want to create the new dynamic secret, using slash `/` separators. If the folder does not exist, it will be created together with the dynamic secret.

4. Define the remaining parameters as follows:

   - **Delete Protection:** When enabled, protects the secret from accidental deletion.

   - **Target:** Select an existing [AWS Target](https://docs.akeyless.io/docs/aws-targets).

     - Use the **Choose an existing target** drop-down list to select the existing [AWS Target](https://docs.akeyless.io/docs/aws-targets).

     - Check the **Explicitly specify target properties** to provide details of the target AWS account in the next step.

   - **Access Mode:** Select the AWS access mode, either **IAM User** or **Assume Role**.

   - **Policies:** Provide the individual Policy ARN(s) available for this dynamic secret. Multiple values should be separated by a comma.

   - **Groups:** Provide the UserGroup name(s). Multiple values should be separated by a comma.

   - **AWS Role ARNs:** Provide the allowed AWS Role ARNs to be used in the **Assume Role** mode.

   - **AWS External ID:** The AWS External ID associated with the AWS role, relevant only for **Assume Role** mode, read more [here](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_common-scenarios_third-party.html).

   - **User Programmatic Access:** Check to enable an Access ID and Access Key for the AWS API, CLI, SDK.

   - **User Console Access:** Check to enable access to the AWS management console. (The returned object will include a username and password to connect to the AWS Management Console).

   - **Session Tags:** Key-value pair attributes that you pass when you assume an IAM role or federate a user in AWS STS. Additionally, they can be used with [Sub-Claims](https://docs.akeyless.io/docs/sub-claims) templates, for example `Key=MyTag,Value={{username}}`, where `username` is the sub-claim name. Relevant only for **Assume Role** mode.

   - **Transitive Tag Keys:** STS Transitive [session tag](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_session-tags.html#id_session-tags_adding-assume-role) keys, relevant only for **Assume Role** mode.

   - **User TTL:** Provide a time-to-live value for a dynamic secret (that is, a token). When TTL expires, the token becomes obsolete.

   - **Custom Username Template:** Set a [custom username template](https://docs.akeyless.io/docs/dynamic-secrets-user-templating) for the generated user.

   - **Temporary Password Length:** Set the length of the temporary password. Relevant only for **IAM User** access mode.

   - **Time Unit:** Select the time unit (seconds, minutes, hours) for the TTL value.

   - **Gateway:** Select the Gateway through which the dynamic secret will create users.

   - **Protection key**: To enable zero-Knowledge, select a key with a Customer Fragment. For more information, [read here](https://docs.akeyless.io/docs/gateway-zero-knowledge).

5. Click **Finish**.

## Fetch a Dynamic AWS Secret Value from the Akeyless Console

1. Log in to the Akeyless Console, and go to **Items**.

2. Browse to the folder where you created a dynamic secret.

3. Select the secret and click the **Get Dynamic Secret** button.

## Tutorial

Check out our tutorial video on [Creating and Using AWS Dynamic Secrets](https://tutorials.akeyless.io/docs/creating-and-fetching-dynamic-secrets).
