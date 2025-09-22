---
title: Windows Rotated Secret
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
You can create a Rotated Secret for a Windows user password. Before you get started, ensure that you create a [Windows Target](doc:windows-target) that includes the hostname and connection settings, as well as credentials for a privileged user authorized to rotate credentials.

When a client requests a Rotated Secret value, the Akeyless Platform connects to the Windows server through your [Gateway](https://docs.akeyless.io/docs/api-gw) to rotate the user password on your target server.

# Create a Rotated Windows Secret from the CLI

To create a Rotated Windows Secret using the Akeyless CLI, run the following command:

```shell Akeyless CLI
akeyless rotated-secret create windows \
--name <Rotated Secretsecret name> \
--gateway-url 'https://<Your-Akeyless-GW-URL:8000>' \
--target-name <Windows target name to associate> \
--authentication-credentials <use-target-creds> \
--password-length 16 \
--rotator-type <password> \
--rotated-username <username> \
--rotated-password <password> \
--user-dn <Base DN to perform user search> \ 
--auto-rotate <true|false> \
--rotation-interval <1-365> \
--rotation-hour <hour in UTC>
```

Where:

* `name`: A unique name of the Rotated Secret. The name can include the path to the virtual folder where you want to create the new Rotated Secret, using slash `/` separators. If the folder does not exist, it will be created together with the Rotated Secret.

* `gateway-url`: Akeyless Gateway Configuration Manager URL (port `8000`).

* `target-name`: The name of the [Windows Target](doc:windows-target) with which the Rotated Secret should be associated.

* `authentication-credentials`: Determines how to connect to the target server.
  * `use-user-creds` - Use the credentials defined on the Rotated Secret item. 
  * `use-target-creds` - Use the credentials defined on the [Windows Target](doc:windows-target) item.

> 👍 Note
>
> Select `use-target-creds` if the Rotated Secret user is not authorized to change their own password, and a privileged user, like the [Windows Target](doc:windows-target) user is required to change the password on behalf of the Rotated Secret user.

* `password-length`: **Optional**,  The user's password length.
* `rotator-type`: The type of credentials to be rotated. For [Windows Target](doc:windows-target) , choose:
  * `password` - to rotate the Windows user password specified in the Rotated Secret.
  * `target` - to rotate the password for the user specified in the [Windows Target](doc:windows-target)
* `rotated-username`: The Windows user whose password should be rotated.
* `rotated-password`: The password to rotate.
* `auto-rotate`: Enable auto-rotation if you need to update the password regularly. If this value is set to **true**, specify the `rotation-interval` in days, and optionally also the `rotation-hour`.

You can find the complete list of parameters for this command in the [CLI Reference - Rotated Secrets](https://docs.akeyless.io/docs/cli-reference-rotated-secrets#p-stylecolorbluewindowsp) section.

# Create a Rotated Windows Secret in the Akeyless Console

> 👍 Note
>
> To start working with Rotated Secrets from the [Akeyless Console](https://docs.akeyless.io/docs/create-an-ssh-rotated-secret#create-a-rotated-ssh-secret-in-the-akeyless-console), you need to configure the [Gateway](https://docs.akeyless.io/docs/api-gw) URL thus enabling communication between the Akeyless SaaS and the Akeyless Gateway.

1. Log in to the Akeyless Console, and go to **Items > New > Rotated Secret > Windows**.

2. Define a **Name** of the Rotated Secret, and specify the **Location** as a path to the virtual folder where you want to create the new Rotated Secret, using slash `/` separators. If the folder does not exist, it will be created together with the Rotated Secret.

3. Define the remaining settings as follows:

* **Delete Protection:** When enabled, it protects the Rotated Secret from accidental deletion.

* **Target:** The name of the [Windows Target](doc:windows-target) with which the Rotated Secret should be associated.

* **Authenticate with the following credentials:** Determines how to connect to the target server:
  * **User credentials:** Use the credentials defined inside the Rotated Secret item.
  * **Target credentials:**  Use the credentials defined on the [Windows Target](doc:windows-target) item.

> 👍 Note
>
> Select **Target credentials** if the Rotated Secret user is not authorized to change their own password, and a privileged user, like the [Windows Target](doc:windows-target) user is required to change the password on behalf of the Rotated Secret user.

* **Password length**: **Optional**, Set the user's password length.
* **Rotator type:** Determines the rotator type:
  * **Password**: Rotates the password defined inside the Rotated Secret item.
  * **Target**: Rotate the password for the user specified in the [Windows Target](doc:windows-target)
* **Username:** Defines the Windows username which password should be rotated.
* **Password:** Defines the password to rotate.
* **Gateway:** Select the Gateway through which the secret will be rotated.
* **Protection key**: To enable zero-Knowledge, select a key with a Customer Fragment. For more information, [read here](doc:implement-zero-knowledge).
* **Auto rotate:** Determines if automatic rotation is enabled.
* **Rotation interval (in days):** Defines the number of days (1-365) to wait between automatic password rotations when **Auto Rotate** is enabled.
* **Rotation hour (local time zone):** Defines the time when the password should be rotated if **Auto Rotate** is enabled.
* **Rotation Notification**: If you wish to get a notification before the next **Automatic Rotation**, click on ⊕ Add Notification and adjust the day count to any number you desire. This can be done multiple times to be notified more than once.

4. Click **Finish**.
