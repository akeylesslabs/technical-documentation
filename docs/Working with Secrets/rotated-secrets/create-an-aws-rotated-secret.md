---
title: AWS Rotated Secret
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
You can create a Rotated Secret for an AWS user. Before you get started, ensure you create an [AWS Target](doc:aws-targets) that includes the AWS region, as well as a role for a privileged user authorized to rotate credentials.

When a client requests a Rotated Secret value, the Akeyless Platform connects to the AWS Cloud through your [Gateway](https://docs.akeyless.io/docs/api-gw) to rotate the user password on your target AWS account.

# Prerequisites

* An [Akeyless Gateway](doc:api-gw).
* [AWS Target](doc:aws-targets) which holds an AWS IAM principal with the following IAM permissions:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "iam:DeleteAccessKey",
                "iam:CreateAccessKey",
                "iam:ListUserTags",
                "iam:ListAccessKeys",
                "iam:ListUsers"
            ],
            "Resource": "arn:aws:iam::<your-aws-account-id>:user/*"
        }
    ]
}
```

Where those permissions are required to rotate the IAM user AccessKeys, Akeyless Rotated secret will create a new Access Key, and revoke the old Access Key, depending on the rotation settings. 

# Create a Rotated AWS Secret from the CLI

To create a Rotated AWS Secret using the Akeyless CLI, run the following command:

```shell Akeyless CLI
akeyless rotated-secret create aws \
--name <Rotated secret name> \
--gateway-url 'https://<Your-Akeyless-GW-URL:8000>' \
--target-name <target name to associate> \
--authentication-credentials <use-user-creds|use-target-creds> \
--rotator-type <api-key|target> \
--api-id <access id> \
--api-key <access key> \
--grace-rotation <true|false>
--auto-rotate <true|false> \
--rotation-interval <1-365> \
--rotation-hour <hour in UTC>
```

Where:

* `name`: A unique name of the Rotated Secret. The name can include the path to the virtual folder where you want to create the new Rotated Secret, using slash `/` separators. If the folder does not exist, it will be created together with the Rotated Secret.

* `gateway-url`: Akeyless Gateway Configuration Manager URL (port `8000`).

* `target-name`: The name of the [AWS Target](doc:aws-targets) with which the Rotated Secret should be associated.

* `authentication-credentials`: Determines how to connect to the target AWS account.
  * `use-user-creds` - Use the credentials defined on the Rotated Secret item.
  * `use-target-creds` - Use the credentials defined on the [AWS Target](doc:aws-targets) item.

> 👍 Note
>
> Select `use-target-creds` if the Rotated Secret user is not authorized to change their own Access Key, and a privileged AWS IAM principal, like the [AWS Target](doc:aws-targets) , is required to change the Access Key on behalf of the Rotated Secret user.

* `rotator-type`: The type of credentials to be rotated. For [AWS Targets](doc:aws-targets), choose:
  * `api-key` - to rotate the Access Key specified in the Rotated Secret.
  * `target` - to rotate the Access Key for the user specified in the [AWS Target](doc:aws-targets).

* `api-id`: The Access Key ID of the AWS user whose Access Key should be rotated. If left empty, the Rotated Secret will create a new key and manage its rotation. **Note** When  `api-id` is not provided, upon successful creation, the AWS Access Key will be automatically created, and upon deletion of the Rotated Secret item using the `rotated-secret delete` command. , the AWS Access Key will be deleted from the cloud as well. 

* `api-key`: The Access Key to rotate.

* `grace-rotation`: A boolean flag, when enabled, a graceful mode of rotation will be conducted, where only the older AWS Access Key will be rotated. When there is only one Access Key, a new version will be created - to maintain 2 values at the same time, following AWS [best practice](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html#Using_RotateAccessKey).

* `auto-rotate`: Enable auto-rotation if you need to update the Access Key regularly. If this value is set to **true**, specify the `rotation-interval` in days, and optionally also the `rotation-hour`.
  * `grace-rotation-interval` and `grace-rotation-hour` defines the 2nd interval following the main rotation settings, relevant only when `grace-rotation` is **enabled**, if not provided, the main `rotation-interval` settings will take place. 

You can find the complete list of parameters for this command in the [CLI Reference - Rotated Secrets](https://docs.akeyless.io/docs/cli-reference-rotated-secrets#p-stylecolorblueawsp) section.

# Create a Rotated AWS Secret in the Akeyless Console

> 👍 Note
>
> To start working with Rotated Secrets from the Akeyless Console, you need to configure the [Gateway](https://docs.akeyless.io/docs/api-gw) URL thus enabling communication between the Akeyless SaaS and the Akeyless Gateway.

1. Log in to the Akeyless Console, and go to **Items > New > Rotated Secret > AWS**.

2. Define a **Name** of the Rotated Secret, and specify the **Location** as a path to the virtual folder where you want to create the new Rotated Secret, using slash `/` separators. If the folder does not exist, it will be created together with the Rotated Secret.

3. Define the remaining settings as follows:

* **Delete Protection:** When enabled, protects the Rotated Secret from accidental deletion.

* **Target:** Defines the name of the [AWS Target](doc:aws-targets) to be associated with the Rotated Secret.

* **Authenticate with the following credentials:** Determines how to connect to the target AWS account:
  * **User credentials:** Use the credentials defined inside the Rotated Secret item.
  * **Target credentials:** Use the credentials defined inside the [AWS Target](doc:aws-targets) item.

> 👍 Note
>
> Select **Target credentials** if the Rotated Secret user is not authorized to change their own Access Key, and a privileged AWS IAM principal, like the [AWS Target](doc:aws-targets) user, is required to change the Access Key on behalf of the Rotated Secret user.

* **Rotator type:** Determines the rotator type:
  * **API Key**: Rotates the Access Key defined inside the Rotated Secret item.
  * **Target**: Rotates the Access Key defined inside the [AWS Target](doc:aws-targets) item.

* **Access Key ID:** Defines the Access Key ID of the AWS user whose Access Key should be rotated.

* **Access Key:** Defines the Access Key to rotate.

> 👍 Note
>
> You can rotate the Access Key for the [AWS Target](doc:aws-targets) too, by creating a Rotated Secret with the **Rotator type** set to **Target**. When you're using a **Target** rotator, the access role with which this Rotated Secret is associated must have read and update permissions on the corresponding Target.

* **Gateway:** Select the Gateway through which the secret will be rotated.

* **Protection key**: To enable zero-Knowledge, select a key with a Customer Fragment. For more information, [read here](doc:implement-zero-knowledge).

* **Graceful Rotation:**  When enabled, a graceful mode of rotation will be conducted, where only the older AWS Access Key will be rotated. When there is only one Access Key, a new version will be created to maintain 2 values at the same time, following AWS [best practice](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html#Using_RotateAccessKey).

* **Auto rotate:** Determines if automatic rotation is enabled.

* **Rotation interval (in days):** Defines the number of days (1-365) to wait between automatic Access Key rotations when **Auto Rotate** is enabled.

* **Rotation hour (local time zone):** Defines the time when the Access Key should be rotated if **Auto Rotate** is enabled.

* **Graceful Rotation Interval (in days):**  Specifies the number of days (range: 1–365) to wait between the main **Rotation Interval** and the **Grace Rotation**. This setting is applicable only when both Auto Rotate and Graceful Rotation are enabled. If left empty, the system will apply the main **Rotation Interval** to both versions of the secret.

* **Rotation Notification**: If you wish to get a notification before the next **Automatic Rotation**, click on ⊕ Add Notification and adjust the day count to any number you desire. This can be done multiple times to be notified more than once.

4. Click **Finish**.
