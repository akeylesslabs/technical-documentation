---
title: AliCloud Rotated Secret
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
You can create a Rotated Secret for an AliCloud RAM user. Before you get started, ensure you create an [AliCloud Target](https://docs.akeyless.io/docs/alicloud-targets) that includes a RAM user for a privileged account authorized to rotate credentials.

When a client requests a Rotated Secret value, the Akeyless Platform connects to AliCloud through your [Gateway](https://docs.akeyless.io/docs/gateway-overview) to rotate the Access Key on your target AliCloud account.

## Prerequisites

* An [Akeyless Gateway](https://docs.akeyless.io/docs/gateway-overview)
* [AliCloud Target](https://docs.akeyless.io/docs/alicloud-targets) which holds an AliCloud RAM principal with the following RAM permissions:

```json
{
    "Version": "1",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "ram:DeleteAccessKey",
                "ram:CreateAccessKey",
                "ram:ListAccessKeys",
                "ram:ListUsers",
                "ram:GetUser"
            ],
            "Resource": "acs:ram:*:*:user/*"
        }
    ]
}
```

Where those permissions are required to rotate the RAM user Access Keys, Akeyless Rotated Secret will create a new Access Key, and revoke the old Access Key, depending on the rotation settings.

## Create a Rotated AliCloud Secret with the CLI

To create a Rotated AliCloud Secret using the Akeyless CLI, run the following command:

```shell
akeyless rotated-secret create alicloud \
--name <Rotated secret name> \
--gateway-url 'https://<Your-Akeyless-GW-URL>:8000' \
--target-name <target name to associate> \
--authentication-credentials <use-user-creds|use-target-creds> \
--rotator-type <access-key|target> \
--access-key-id <access key id> \
--access-key-secret <access key secret> \
--grace-rotation <true|false>
--auto-rotate <true|false> \
--rotation-interval <1-365> \
--rotation-hour <hour in UTC>
```

Where:

* `name`: A unique name of the Rotated Secret. The name can include the path to the virtual folder where you want to create the new Rotated Secret, using slash `/` separators. If the folder does not exist, it will be created together with the Rotated Secret.

* `gateway-url`: Akeyless Gateway URL (port `8000`).

* `target-name`: The name of the [AliCloud Target](https://docs.akeyless.io/docs/alicloud-targets) with which the Rotated Secret should be associated.

* `authentication-credentials`: Determines how to connect to the target AliCloud account.
    * `use-user-creds` - Use the credentials defined on the Rotated Secret item.
    * `use-target-creds` - Use the credentials defined on the [AliCloud Target](https://docs.akeyless.io/docs/alicloud-targets) item.

> ℹ️ **Note:**
>
> Select `use-target-creds` if the Rotated Secret RAM user is not authorized to change their own Access Key, and a privileged AliCloud RAM principal, like the [AliCloud Target](https://docs.akeyless.io/docs/alicloud-targets), is required to change the Access Key on behalf of the Rotated Secret user.

* `rotator-type`: The type of credentials to be rotated. For [AliCloud Targets](https://docs.akeyless.io/docs/alicloud-targets), choose:
    * `access-key` - to rotate the Access Key specified in the Rotated Secret.
    * `target` - to rotate the Access Key for the RAM user specified in the [AliCloud Target](https://docs.akeyless.io/docs/alicloud-targets).

* `access-key-id`: The Access Key ID of the AliCloud RAM user whose Access Key should be rotated. If left empty, the Rotated Secret will create a new key and manage its rotation. **Note** When `access-key-id` is not provided, upon successful creation, the AliCloud Access Key will be automatically created, and upon deletion of the Rotated Secret item using the `rotated-secret delete` command, the AliCloud Access Key will be deleted from the cloud as well.

* `access-key-secret`: The Access Key Secret to rotate.

* `grace-rotation`: A boolean flag, when enabled, a graceful mode of rotation will be conducted, where only the older AliCloud Access Key will be rotated. When there is only one Access Key, a new version will be created - to maintain 2 values at the same time.

* `auto-rotate`: Enable auto-rotation if you need to update the Access Key regularly. If this value is set to **true**, specify the `rotation-interval` in days, and optionally also the `rotation-hour`.
    * `grace-rotation-interval` and `grace-rotation-hour` define the second interval following the main rotation settings and are relevant only when `grace-rotation` is **enabled**.
    * `grace-rotation-interval` must be lower than `rotation-interval`.
    * When `grace-rotation-timing` is `before`, `rotation-interval` must be higher than `2 × grace-rotation-interval` with at least one day.

You can find the complete list of parameters for this command in the [CLI Reference - Rotated Secrets](https://docs.akeyless.io/docs/cli-reference-rotated-secrets#alicloud) section.

## Create a Rotated AliCloud Secret in the Akeyless Console

> ℹ️ **Note:**
>
> To start working with Rotated Secrets from the Akeyless Console, you need to configure the [Gateway](https://docs.akeyless.io/docs/gateway-overview) URL thus enabling communication between the Akeyless SaaS and the Akeyless Gateway.

1. Log in to the Akeyless Console, and go to **Items > New > Rotated Secret > AliCloud**.

2. Define a **Name** of the Rotated Secret, and specify the **Location** as a path to the virtual folder where you want to create the new Rotated Secret, using slash `/` separators. If the folder does not exist, it will be created together with the Rotated Secret.

3. Define the remaining settings as follows:

    * **Delete Protection:** When enabled, protects the Rotated Secret from accidental deletion.

    * **Target:** Defines the name of the [AliCloud Target](https://docs.akeyless.io/docs/alicloud-targets) to be associated with the Rotated Secret.

    * **Authenticate with the following credentials:** Determines how to connect to the target AliCloud account:
        * **User credentials:** Use the credentials defined inside the Rotated Secret item.
        * **Target credentials:** Use the credentials defined inside the [AliCloud Target](https://docs.akeyless.io/docs/alicloud-targets) item.

    > 👍 Note
    >
    > Select **Target credentials** if the Rotated Secret RAM user is not authorized to change their own Access Key, and a privileged AliCloud RAM principal, like the [AliCloud Target](https://docs.akeyless.io/docs/alicloud-targets) user, is required to change the Access Key on behalf of the Rotated Secret user.

    * **Rotator type:** Determines the rotator type:
        * **Access Key**: Rotates the Access Key defined inside the Rotated Secret item.
        * **Target**: Rotates the Access Key defined inside the [AliCloud Target](https://docs.akeyless.io/docs/alicloud-targets) item.

    * **Access Key ID:** Defines the Access Key ID of the AliCloud RAM user whose Access Key should be rotated.

    * **Access Key Secret:** Defines the Access Key Secret to rotate.

    > 👍 Note
    >
    > You can rotate the Access Key for the [AliCloud Target](https://docs.akeyless.io/docs/alicloud-targets) too, by creating a Rotated Secret with the **Rotator type** set to **Target**. When you're using a **Target** rotator, the access role with which this Rotated Secret is associated must have read and update permissions on the corresponding Target.

    * **Gateway:** Select the Gateway through which the secret will be rotated.

    * **Protection key**: To enable zero-Knowledge, select a key with a Customer Fragment. For more information, [read here](https://docs.akeyless.io/docs/gateway-zero-knowledge).

    * **Graceful Rotation:** When enabled, a graceful mode of rotation will be conducted, where only the older AliCloud Access Key will be rotated. When there is only one Access Key, a new version will be created to maintain 2 values at the same time.

    * **Auto rotate:** Determines if automatic rotation is enabled.

    * **Rotation interval (in days):** Defines the number of days (1-365) to wait between automatic Access Key rotations when **Auto Rotate** is enabled.

    * **Rotation hour (local time zone):** Defines the time when the Access Key should be rotated if **Auto Rotate** is enabled.

    * **Graceful Rotation Interval (in days):** Specifies the number of days (range: 1–365) to wait between the main **Rotation Interval** and the **Grace Rotation**. This setting is applicable only when both Auto Rotate and Graceful Rotation are enabled. If left empty, the system will apply the main **Rotation Interval** to both versions of the secret.

    * **Rotation Notification**: If you wish to get a notification before the next **Automatic Rotation**, click **⊕ Add Notification** and adjust the day count to any number you prefer. This can be done multiple times to be notified more than once.

4. Click **Finish**.