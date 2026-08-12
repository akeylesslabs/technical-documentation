---
title: F5 Rotated Secret
deprecated: false
hidden: false
metadata:
  robots: index
---
You can create a Rotated Secret for an F5 BIG-IP admin user password.&#x20;

When a client requests a Rotated Secret value, the Akeyless Platform connects to the F5 BIG-IP device through your [Gateway](https://docs.akeyless.io/docs/gateway-overview) to rotate the user password on your target device.

# Prerequisites

- An [Akeyless Gateway](https://docs.akeyless.io/docs/gateway-overview)
- An F5 Target&#x20;

## Create a Rotated F5 Secret with the CLI

To create a Rotated F5 Secret using the Akeyless CLI, run the following command:

```shell
akeyless rotated-secret create f5-big-ip \
--name <Rotated Secret name> \
--target-name <F5 target name to associate> \
--authentication-credentials[=use-user-creds] [use-user-creds/use-target-creds]
--rotator-type [target/password] \
--rotated-username <username> \
--rotated-password <password> \
--gateway-url 'https://<Your-Akeyless-GW-URL>:8000' 
```

Where:

- `name`: A unique name of the Rotated Secret. The name can include the path to the virtual folder where you want to create the new Rotated Secret, using slash `/` separators. If the folder does not exist, it will be created together with the Rotated Secret.

- `gateway-url`: Akeyless Gateway URL (port `8000`).

- `target-name`: The name of the [F5 Target](https://docs.akeyless.io/docs/f5-target) with which the Rotated Secret should be associated.

- `authentication-credentials`: Determines how to connect to the target device.

  - `use-user-creds` - Use the credentials defined on the Rotated Secret item.
  - `use-target-creds` - Use the credentials defined on the [F5 Target](https://docs.akeyless.io/docs/f5-target) item.

<Callout icon="📘" theme="info">
  ### Note:

  Select `use-target-creds`if the Rotated Secret user is not authorized to change their own password, and a privileged user, like the [F5 Target](https://docs.akeyless.io/docs/f5-target) user, is required to change the password on behalf of the Rotated Secret user.
</Callout>

- `rotator-type`: The type of credentials to be rotated. For [F5 Target](https://docs.akeyless.io/docs/f5-target), choose:
  - `password` : Rotate the password of the user specified in `--rotated-username`.
  - `target` - Rotate the password for the user specified in the F5 Target.

You can find the complete list of parameters for this command in the [CLI Reference - Rotated Secrets](https://docs.akeyless.io/docs/cli-reference-rotated-secrets#f5-big-ip) section.

## Create a Rotated F5 Secret in the Akeyless Console

<Callout icon="📘" theme="info">
  ### Note:

  To start working with Rotated Secrets from the Akeyless Console, you need to configure the [Gateway](https://docs.akeyless.io/docs/gateway-overview) URL thus enabling communication between the Akeyless SaaS and the Akeyless Gateway.
</Callout>

1. Log in to the Akeyless Console, and go to **Items > New > Rotated Secret > Infra (F5 BIG-IP)**.

2. Define a **Name** of the Rotated Secret, and specify the **Location** as a path to the virtual folder where you want to create the new Rotated Secret, using slash `/` separators. If the folder does not exist, it will be created together with the Rotated Secret.

3. Define the remaining settings as follows:

- **Delete Protection:** When enabled, it protects the Rotated Secret from accidental deletion.

- **Target:** The name of the [F5 Target](https://docs.akeyless.io/docs/f5-target) with which the Rotated Secret should be associated.

- **Authenticate with the following credentials:** Determines how to connect to the target device:
  - **User credentials:** Use the credentials defined inside the Rotated Secret item.

  - **Target credentials:** Use the credentials defined on the [F5 Target](https://docs.akeyless.io/docs/f5-target) item.

- **Rotator type:** Determines the rotator type:
  - **Password**: Rotates the password defined inside the Rotated Secret item.

  - **Target**: Rotates the password for the user specified in the [F5 Target](https://docs.akeyless.io/docs/f5-target).

- **Username:** Defines the F5 username whose password should be rotated.

- **Password:** Defines the password to rotate.

- **Password Policy**: Set the password policy.&#x20;

- **Gateway:** Select the Gateway through which the secret will be rotated.

- **Protection key**: To enable zero-Knowledge, select a key with a Customer Fragment. For more information, [read here](https://docs.akeyless.io/docs/gateway-zero-knowledge).

- **Auto rotate:** Determines if automatic rotation is enabled.

- **Rotation interval (in days):** Defines the number of days (1-365) to wait between automatic password rotations when **Auto Rotate** is enabled.

- **Rotation hour (local time zone):** Defines the time when the password should be rotated if **Auto Rotate** is enabled.

- **Rotation Notification**: If you wish to get a notification before the next **Automatic Rotation**, click **⊕ Add Notification** and adjust the day count to any number you prefer. This can be done multiple times to be notified more than once.

4. Click **Finish**.
