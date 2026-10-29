---
title: Alibaba Cloud Rotated Secret
deprecated: false
hidden: false
metadata:
  robots: index
---
You can create a Rotated Secret for an Alibaba Cloud RAM user AccessKey pair. Before you get started, ensure you create an [AliCloud Target](https://docs.akeyless.io/docs/alicloud-targets) that holds a RAM identity authorized to rotate AccessKeys.

When a Rotated Secret is rotated, manually or on schedule, the Akeyless Platform connects to Alibaba Cloud through your [Gateway](https://docs.akeyless.io/docs/gateway-overview), creates a new AccessKey pair for the RAM user, verifies it, and then deactivates and deletes the old one.

## Prerequisites

- An [Akeyless Gateway](https://docs.akeyless.io/docs/gateway-overview)
- An [AliCloud Target](https://docs.akeyless.io/docs/alicloud-targets) that holds a RAM user or RAM role (not an Alibaba Cloud root account) with the following RAM permissions:

```json
{
  "Version": "1",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "ram:ListAccessKeys",
        "ram:CreateAccessKey",
        "ram:UpdateAccessKey",
        "ram:DeleteAccessKey",
        "ram:GetUser"
      ],
      "Resource": "acs:ram:*:<your-alicloud-account-id>:user/*"
    }
  ]
}
```

These permissions let the Rotated Secret create a new AccessKey, deactivate the old AccessKey, and delete it, depending on the rotation settings. Scope `Resource` down to specific RAM users where possible.

## Create a Rotated AliCloud Secret with the CLI

To create a Rotated AliCloud Secret using the Akeyless CLI, run the following command:

```shell
akeyless rotated-secret create alicloud \
--name <Rotated secret name> \
--gateway-url 'https://<Your-Akeyless-GW-URL>:8000' \
--target-name <target name to associate> \
--authentication-credentials <use-user-creds|use-target-creds> \
--rotator-type <access-key|target> \
--access-key-id <AccessKey ID> \
--access-key <AccessKey secret> \
--grace-rotation <true|false> \
--auto-rotate <true|false> \
--rotation-interval <1-365> \
--rotation-hour <hour in UTC>
```

Where:

- `name`: A unique name of the Rotated Secret. The name can include the path to the virtual folder where you want to create the new Rotated Secret, using slash `/` separators. If the folder does not exist, it will be created together with the Rotated Secret.
- `gateway-url`: Akeyless Gateway URL (port `8000`).
- `target-name`: The name of the [AliCloud Target](https://docs.akeyless.io/docs/alicloud-targets) with which the Rotated Secret should be associated.
- `authentication-credentials`: Determines how to connect to the target Alibaba Cloud account.
  - `use-user-creds` - Use the credentials defined on the Rotated Secret item.
  - `use-target-creds` - Use the credentials defined on the [AliCloud Target](https://docs.akeyless.io/docs/alicloud-targets) item.

<Callout icon="ℹ️" theme="info">
  ### **Note:**

  Select `use-target-creds` if the Rotated Secret RAM user is not authorized to change their own AccessKey, and a privileged RAM identity, like the [AliCloud Target](https://docs.akeyless.io/docs/alicloud-targets), is required to change the AccessKey on behalf of the Rotated Secret user.
</Callout>

- `rotator-type`: The type of credentials to be rotated. For [AliCloud Targets](https://docs.akeyless.io/docs/alicloud-targets), choose:
  - `access-key` - to rotate the AccessKey pair specified in the Rotated Secret.
  - `target` - to rotate the AccessKey of the RAM user specified in the [AliCloud Target](https://docs.akeyless.io/docs/alicloud-targets). Not available when the target uses the Gateway's cloud identity.
- `access-key-id`: The AccessKey ID of the RAM user whose AccessKey should be rotated. Relevant only for `rotator-type`=`access-key`.
- `access-key`: The AccessKey secret to rotate. Relevant only for `rotator-type`=`access-key`.
- `grace-rotation`: A boolean flag. When enabled, a graceful mode of rotation is conducted, where only the older AccessKey is rotated. When there is only one AccessKey, a new one is created to maintain 2 valid values at the same time. Alibaba Cloud allows a maximum of 2 AccessKeys per RAM user.
- `auto-rotate`: Enable auto-rotation if you need to update the AccessKey regularly. If this value is set to **true**, specify the `rotation-interval` in days, and optionally also the `rotation-hour`.
  - `grace-rotation-interval` and `grace-rotation-hour` define the second interval following the main rotation settings and are relevant only when `grace-rotation` is **enabled**.
  - `grace-rotation-interval` must be lower than `rotation-interval`.
  - When `grace-rotation-timing` is `before`, `rotation-interval` must be higher than `2 × grace-rotation-interval` with at least one day.
- `alicloud-region`: Optional. The Alibaba Cloud region used to select the regional STS endpoint, for example `cn-hangzhou`. If empty, the global endpoint is used.

You can find the complete list of parameters for this command in the [CLI Reference - Rotated Secrets](https://docs.akeyless.io/docs/cli-reference-rotated-secrets#alicloud) section.

## Create a Rotated AliCloud Secret in the Akeyless Console

<Callout icon="ℹ️" theme="info">
  ### **Note:**

  To start working with Rotated Secrets from the Akeyless Console, you need to configure the [Gateway](https://docs.akeyless.io/docs/gateway-overview) URL, enabling communication between the Akeyless SaaS and the Akeyless Gateway.
</Callout>

1. Log in to the Akeyless Console, and go to **Items > New > Rotated Secret > Alibaba Cloud**.
2. Define a **Name** of the Rotated Secret, and specify the **Location** as a path to the virtual folder where you want to create the new Rotated Secret, using slash `/` separators. If the folder does not exist, it will be created together with the Rotated Secret.
3. Define the remaining settings as follows:

   - **Delete Protection:** When enabled, protects the Rotated Secret from accidental deletion.
   - **Target:** Defines the name of the [AliCloud Target](https://docs.akeyless.io/docs/alicloud-targets) to be associated with the Rotated Secret.
   - **Authenticate with the following credentials:** Determines how to connect to the target Alibaba Cloud account:
     - **User credentials:** Use the credentials defined inside the Rotated Secret item.

     - **Target credentials:** Use the credentials defined inside the [AliCloud Target](https://docs.akeyless.io/docs/alicloud-targets) item.

   <Callout icon="👍" theme="okay">
     ### Note

     Select **Target credentials** if the Rotated Secret RAM user is not authorized to change their own AccessKey, and a privileged RAM identity, like the [AliCloud Target](https://docs.akeyless.io/docs/alicloud-targets) user, is required to change the AccessKey on behalf of the Rotated Secret user.
   </Callout>

   - **Rotator type:** Determines the rotator type:
     - **AccessKey**: Rotates the AccessKey pair defined inside the Rotated Secret item.
     - **Target**: Rotates the AccessKey defined inside the [AliCloud Target](https://docs.akeyless.io/docs/alicloud-targets) item.

   - **Access Key ID:** Defines the AccessKey ID of the RAM user whose AccessKey should be rotated.

   - **Access Key Secret:** Defines the AccessKey secret to rotate.

   <Callout icon="👍" theme="okay">
     ### Note

     You can rotate the AccessKey for the [AliCloud Target](https://docs.akeyless.io/docs/alicloud-targets) too, by creating a Rotated Secret with the **Rotator type** set to **Target**. When you're using a **Target** rotator, the access role with which this Rotated Secret is associated must have read and update permissions on the corresponding Target.
   </Callout>

   - **Region:** Optional. Selects the regional STS endpoint. If empty, the global endpoint is used.
   - **Gateway:** Select the Gateway through which the secret will be rotated.
   - **Protection key**: To enable Zero-Knowledge, select a key with a Customer Fragment. For more information, [read here](https://docs.akeyless.io/docs/gateway-zero-knowledge).
   - **Graceful Rotation:** When enabled, a graceful mode of rotation will be conducted, where only the older AccessKey will be rotated. When there is only one AccessKey, a new one will be created to maintain 2 valid values at the same time.
   - **Auto rotate:** Determines if automatic rotation is enabled.
   - **Rotation interval (in days):** Defines the number of days (1-365) to wait between automatic AccessKey rotations when **Auto Rotate** is enabled.
   - **Rotation hour (local time zone):** Defines the time when the AccessKey should be rotated if **Auto Rotate** is enabled.
   - **Graceful Rotation Interval (in days):** Specifies the number of days (range: 1–365) to wait between the main **Rotation Interval** and the **Grace Rotation**. This setting is applicable only when both Auto Rotate and Graceful Rotation are enabled. If left empty, the system will apply the main **Rotation Interval** to both versions of the secret.
   - **Rotation Notification**: If you wish to get a notification before the next **Automatic Rotation**, click **⊕ Add Notification** and adjust the day count to any number you prefer. This can be done multiple times to be notified more than once.
4. Click **Finish**.

##