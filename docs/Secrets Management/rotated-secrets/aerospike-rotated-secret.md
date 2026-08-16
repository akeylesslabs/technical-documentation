---
title: Aerospike Rotated Secret
deprecated: false
hidden: false
metadata:
  robots: index
---
You can create a Rotated Secret for an Aerospike user. Before you get started, ensure creating an [Aerospike Target](https://docs.akeyless.io/docs/aerospike-target) that includes the hostname, connection settings, and credentials for a privileged user authorized to rotate credentials.

When a client requests a Rotated Secret value, the Akeyless Platform connects to the Aerospike cluster through your [Gateway](https://docs.akeyless.io/docs/gateway-overview) to rotate the user password on your target Aerospike cluster.

## Create a Rotated Aerospike Secret with the CLI

To create a rotated Aerospike secret using the Akeyless CLI, run the following command:

```shell
akeyless rotated-secret create aerospike \
--name <Rotated Secret name> \
--gateway-url 'https://<Your-Akeyless-GW-URL>:8000' \
--target-name <target name to associate> \
--authentication-credentials <use-user-creds|use-target-creds> \
--rotator-type <password|target> \
--rotated-username <username> \
--rotated-password <password to rotate> \
--auto-rotate <true|false> \
--rotation-interval <1-365> \
--rotation-hour <hour in UTC>
```

Where:

- `name`: A unique name of the Rotated Secret. The name can include the path to the virtual folder where you want to create the new Rotated Secret, using slash `/` separators. If the folder does not exist, it will be created together with the Rotated Secret.

- `gateway-url`: Akeyless Gateway URL (port `8000`).

- `target-name`: The name of the [Aerospike Target](https://docs.akeyless.io/docs/aerospike-target) with which the Rotated Secret should be associated.

- `authentication-credentials`: Determines how to connect to the target Aerospike cluster.

  - `use-user-creds` - Use the credentials defined on the Rotated Secret item.
  - `use-target-creds` - Use the credentials defined on the [Aerospike Target](https://docs.akeyless.io/docs/aerospike-target) item.

<Callout icon="📘" theme="info">
  ### Note:

  Select `use-target-creds` if the Rotated Secret user is not authorized to change their own password, and a privileged user, like the Aerospike Target, is required to change the password on behalf of the Rotated Secret user.
</Callout>

- `password-length`: **Optional**, The user's password length.
- `rotator-type`: The type of credentials to be rotated. For [Aerospike Targets](https://docs.akeyless.io/docs/aerospike-target), choose:
  - `password` - to rotate the Aerospike user password specified in the Rotated Secret
  - `target` - to rotate the password for the user specified in the [Aerospike Target](https://docs.akeyless.io/docs/aerospike-target).
- `rotated-username`: The Aerospike user whose password should be rotated.
- `rotated-password`: The password to rotate.
- `auto-rotate`: Enable auto-rotation if you need to update the password regularly. If this value is set to **true**, specify the `rotation-interval` in days, and optionally also the `rotation-hour`.&#x20;

You can find the complete list of parameters for this command in the [CLI Reference - Rotated Secrets](https://docs.akeyless.io/docs/cli-reference-rotated-secrets#aerospike) section.

## Create a Rotated Aerospike Secret in the Akeyless Console

<Callout icon="📘" theme="info">
  ### Note:

  To start working with Rotated Secrets from the Akeyless Console, you need to configure the [Gateway](https://docs.akeyless.io/docs/gateway-overview) URL thus enabling communication between the Akeyless SaaS and the Akeyless Gateway.
</Callout>

1. Log in to the Akeyless Console, and go to **Items > New > Rotated Secret > Aerospike**.

2. Define a **Name** of the Rotated Secret, and specify the **Location** as a path to the virtual folder where you want to create the new Rotated Secret, using slash `/` separators. If the folder does not exist, it will be created together with the Rotated Secret.

3. Define the remaining settings as follows:

- **Delete Protection:** When enabled, it protects the Rotated Secret from accidental deletion.

- **Target:** Defines the name of the [Aerospike Target](https://docs.akeyless.io/docs/aerospike-target) to be associated with the Rotated Secret.

- **Authenticate with the following credentials:** Determines how to connect to the target Aerospike cluster:

  - **User credentials:** Use the credentials defined inside the Rotated Secret item.

  - **Target credentials:** Use the credentials defined inside the [Aerospike Target](https://docs.akeyless.io/docs/aerospike-target) item.

<Callout icon="👍" theme="success">
  ### Note

  Select **Target credentials** if the Rotated Secret user is not authorized to change their own password, and a privileged user, like the Aerospike Target user, is required to change the password on behalf of the Rotated Secret user.
</Callout>

- **Rotator type:** Determines the rotator type:
  - **Password**: Rotates the password defined inside the Rotated Secret item.
  - **Target**: Rotates the password defined inside the [Aerospike Target](https://docs.akeyless.io/docs/aerospike-target) item.

* **Username:** Defines the Aerospike username whose password should be rotated.

* **Password:** Defines the password to rotate.

* **Password Policy**: Set the password policy.

- **Gateway:** Select the Gateway through which the secret will be rotated.

- **Protection key**: To enable zero-Knowledge, select a key with a Customer Fragment. For more information, [read here](https://docs.akeyless.io/docs/gateway-zero-knowledge).

- **Auto rotate:** Determines if automatic rotation is enabled.

- **Rotation interval (in days):** Defines the number of days (1-365) to wait between automatic password rotations when **Auto Rotate** is enabled.

- **Rotation hour (local time zone):** Defines the time when the password should be rotated if **Auto Rotate** is enabled.

- **Rotation Notification**: If you wish to get a notification before the next **Automatic Rotation**, click **⊕ Add Notification** and adjust the day count to any number you prefer. This can be done multiple times to be notified more than once.

4. Click **Finish**.
