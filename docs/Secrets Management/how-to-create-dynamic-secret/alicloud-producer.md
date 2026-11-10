---
title: Alibaba Cloud Dynamic Secret
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
You can define a dynamic Alibaba Cloud (AliCloud) secret to generate RAM AccessKey credentials dynamically, based on RAM policies. Those credentials are time-based and automatically get revoked when a dynamic secret's time to live expires.

You can create dynamic access credentials for AliCloud in two modes:

- **ram_user** mode: When a client requests a dynamic secret value, a **temporary** RAM user is created in the requested Alibaba Cloud account, and an AccessKey is returned to the client. The temporary users should be assigned to an existing policy in the Alibaba Cloud account. Temporary RAM users can only be created with access to a single Alibaba Cloud account. If you have multiple Alibaba Cloud accounts, you will need to create a separate dynamic secret for each account for RAM user mode.
- **assume_role** mode: When a client requests the dynamic secret value, an [AssumeRole](https://www.alibabacloud.com/help/en/ram/user-guide/assume-a-ram-role) operation is performed to return an AccessKey ID, AccessKey secret, and security token. Although a single dynamic secret can assume roles for multiple accounts, once access is granted, it cannot be revoked before its defined expiration time. Assume role is more convenient for immediate actions, as the **STS** credentials are available immediately.

## Prerequisites

- An [Akeyless Gateway](https://docs.akeyless.io/docs/gateway-overview)
- An [AliCloud Target](https://docs.akeyless.io/docs/alicloud-targets)
- If you are using `ram_user` mode, the minimum required policy for the RAM user should include the following permissions:

```json
{
  "Version": "1",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "ram:CreateUser",
        "ram:GetUser",
        "ram:DeleteUser",
        "ram:TagResources",
        "ram:UntagResources",
        "ram:ListTagResources",
        "ram:CreateAccessKey",
        "ram:DeleteAccessKey",
        "ram:ListAccessKeys",
        "ram:AttachPolicyToUser",
        "ram:DetachPolicyFromUser",
        "ram:ListPoliciesForUser",
        "ram:CreateLoginProfile",
        "ram:GetLoginProfile",
        "ram:UpdateLoginProfile",
        "ram:DeleteLoginProfile",
        "ram:AddUserToGroup",
        "ram:RemoveUserFromGroup",
        "ram:ListGroupsForUser"
      ],
      "Resource": "acs:ram:*:<your-alicloud-account-id>:user/tmp.*"
    }
  ]
}
```

This policy grants the dynamic secret permissions to manage the lifecycle of the temporary RAM users' AccessKeys, including creation and deletion. It will also support the setup of a temporary user with console login, adding users to groups, and utilizing Alibaba Cloud tags as well.

_Note:_ `tmp.*` is the default template prefix of the temporary users Akeyless creates. If you are working with a [custom username template](https://docs.akeyless.io/docs/dynamic-secrets-user-templating), make sure to adjust the allowed resource accordingly.

- If you are using `assume_role` mode, grant the RAM identity associated with your [AliCloud Target](https://docs.akeyless.io/docs/alicloud-targets) **AssumeRole** permissions to the requested RAM roles. The required policy should include the following permissions:

```json
{
  "Version": "1",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "sts:AssumeRole",
      "Resource": "acs:ram::<your-alicloud-account-id>:role/<RoleName>"
    }
  ]
}
```

where the `<RoleName>` should be replaced with the role that will be assumed.

_Note:_ Make sure that the target RAM role that will be part of the roles that this dynamic secret should be able to assume must include a trust policy with the principal of the RAM identity used by your [AliCloud Target](https://docs.akeyless.io/docs/alicloud-targets).

## Create a Dynamic AliCloud Secret with the CLI

<Callout icon="ℹ️" theme="info">
  ### **Note:**

  We recommend using Dynamic Secrets with [Targets](https://docs.akeyless.io/docs/alicloud-targets). While it saves time for multiple secret-level configurations by not requiring you to provide the connection details each time, it is also important for security streamlining. Using a target allows you to rotate credentials without breaking the credential chain for the objects connected to the server used.
</Callout>

To create a dynamic AliCloud secret with the CLI using an existing [AliCloud Target](https://docs.akeyless.io/docs/alicloud-targets), run the following command:

```shell
akeyless dynamic-secret create alicloud \
--name <secret name> \
--target-name <Target Name> \
--gateway-url 'https://<Your-Akeyless-GW-URL>:8000' \
--alicloud-access-mode <ram_user|assume_role> \
--alicloud-user-policies <Policy name> \
--alicloud-role-arns <AliCloud Role ARNs>
```

Where:

- `name` A unique name of the dynamic secret. The name can include the path to the virtual folder where you want to create the new dynamic secret, using the slash `/` separators. If the folder does not exist, it will be created together with the dynamic secret.

- `target-name`: A name of the [AliCloud Target](https://docs.akeyless.io/docs/alicloud-targets) that enables connection to Alibaba Cloud. The name can include the path to the virtual folder where this target resides.

- `gateway-url`: Akeyless Gateway URL (port `8000`).

- `alicloud-access-mode`: The types of credentials to retrieve from Alibaba Cloud. The following options are available:

  `ram_user` or `assume_role`.

- `alicloud-user-policies`: Policy name(s). Multiple values should be separated by a comma. The RAM user will be granted these policies when the dynamic secret is created.

- `alicloud-role-arns`: RAM Role ARNs to be used in the Assume Role operation. Multiple values should be separated by a comma.

## Fetch a Dynamic AliCloud Secret Value with the CLI

To fetch a dynamic AliCloud secret value with the CLI, run the following command:

```shell
akeyless dynamic-secret get-value --name <Path to your dynamic secret>
```

## Create a Dynamic AliCloud Secret in the Akeyless Console

<Callout icon="ℹ️" theme="info">
  ### **Note:**

  To start working with Dynamic Secrets from the [Akeyless Console](https://docs.akeyless.io/docs/alicloud-producer#create-a-dynamic-alicloud-secret-in-the-akeyless-console), you need to configure the Gateway URL thus enabling communication between the Akeyless SaaS and the Akeyless Gateway.
</Callout>

1. Log in to the Akeyless Console, and go to **Items > New > Dynamic Secret**.

2. Select the AliCloud secret type and click **Next**.

3. Define a **Name** of the dynamic secret, and specify the **Location** as a path to the virtual folder where you want to create the new dynamic secret, using slash `/` separators. If the folder does not exist, it will be created together with the dynamic secret.

4. Define the remaining parameters as follows:

   - **Delete Protection:** When enabled, protects the secret from accidental deletion.

   - **Target:** Select an existing [AliCloud Target](https://docs.akeyless.io/docs/alicloud-targets).

   - **Access Mode:** Select the AliCloud access mode, either **RAM User** or **Assume Role**.

   - **Policies:** Provide the individual Policy name(s) available for this dynamic secret. Multiple values should be separated by a comma.

   - **RAM Role ARNs:** Provide the allowed RAM Role ARNs to be used in the **Assume Role** mode.

   - **User Programmatic Access:** Check to enable an AccessKey ID and AccessKey secret for the Alibaba Cloud API, CLI, SDK.

   - **User Console Access:** Check to enable access to the Alibaba Cloud console. (The returned object will include a username and password to connect to the Alibaba Cloud console).

   - **User TTL:** Provide a time-to-live value for a dynamic secret (that is, a token). When TTL expires, the token becomes obsolete.

   - **Custom Username Template:** Set a [custom username template](https://docs.akeyless.io/docs/dynamic-secrets-user-templating) for the generated user.

   - **Temporary Password Length:** Set the length of the temporary password. Relevant only for **RAM User** access mode.

   - **Time Unit:** Select the time unit (seconds, minutes, hours) for the TTL value.

   - **Gateway:** Select the Gateway through which the dynamic secret will create users.

   - **Protection key**: To enable zero-Knowledge, select a key with a Customer Fragment. For more information, [read here](https://docs.akeyless.io/docs/gateway-zero-knowledge).

5. Click **Finish**.

## Fetch a Dynamic AliCloud Secret Value from the Akeyless Console

1. Log in to the Akeyless Console, and go to **Items**.

2. Browse to the folder where you created a dynamic secret.

3. Select the secret and click the **Get Dynamic Secret** button.
