---
title: SSH Rotated Secret
excerpt: ''
deprecated: false
hidden: false
metadata:
  title: ''
  description: ''
  robots: index
next:
  description: ''
  pages:
    - type: basic
      slug: add-a-rotated-secret-to-a-role
      title: Add a Rotated Secret to a Role
---
You can create a Rotated Secret for an SSH password. Before you get started, ensure you have an [SSH Target](doc:ssh-target) that includes the hostname and connection settings, as well as credentials for a privileged user authorized to rotate credentials.

When a client requests a Rotated Secret value, the Akeyless Platform connects to the SSH server through your [Gateway](https://docs.akeyless.io/docs/api-gw) to rotate the user password on your target server.

> 👍 Note
>
> **Linux Distribution**
>
> While the Akeyless Rotated Secret can work by default with many popular Unix OS, some distributions like **RedHat** etc, requires a customization of the default rotation statement. For those cases you can set a **Custom Rotation** command as desribed [here](https://docs.akeyless.io/docs/create-an-ssh-rotated-secret#custom-rotation-statement)

# Create a Rotated SSH Secret from the CLI

To create a Rotated SSH Secret using the Akeyless CLI, run the following command:

```shell Akeyless CLI
akeyless rotated-secret create ssh \
--name <Rotated Secret name>
--gateway-url 'https://<Your-Akeyless-GW-URL:8000>' \
--target-name <target name> \
--authentication-credentials <use-user-creds|use-target-creds> \
--password-length 16 \
--rotator-type <password|target> \
--rotated-username <username> \
--rotated-password <password> \
--auto-rotate <true|false> \
--rotation-interval <1-365> \
--rotation-hour <hour in UTC> 
```

Where:

* `name`: A unique name of the Rotated Secret. The name can include the path to the virtual folder where you want to create the new Rotated Secret, using slash `/` separators. If the folder does not exist, it will be created together with the Rotated Secret.

* `gateway-url`: Akeyless Gateway Configuration Manager URL (port `8000`).

* `target-name`: The name of the [SSH Target](doc:ssh-target) with which the Rotated Secret should be associated.

* `authentication-credentials`: Determines how to connect to the target server.
  * `use-user-creds` - Use the credentials defined on the Rotated Secret item.
  * `use-target-creds` - Use the credentials defined on the [SSH Target](doc:ssh-target) item.

> 👍 Note
>
> Select `use-target-creds` if the Rotated Secret user is not authorized to change their own password, and a privileged user, like the [SSH Target](doc:ssh-target) user is required to change the password on behalf of the Rotated Secret user.

* `password-length`: **Optional**, The user's password length.
* `rotator-type`: The type of credentials to be rotated. For [SSH Targets](doc:ssh-target), choose:
  * `password` - to rotate the SSH user password specified in the Rotated Secret
  * `target` - to rotate the password for the user specified in the [SSH Target](doc:ssh-target).
* `rotated-username`: The SSH user whose password should be rotated.
* `rotated-password`: The password to rotate.
* `auto-rotate`: Enable auto-rotation if you need to update the password regularly. If this value is set to **true**, specify the `rotation-interval` in days, and optionally also the `rotation-hour`.

You can find the complete list of parameters for this command in the [CLI Reference - Rotated Secrets](https://docs.akeyless.io/docs/cli-reference-rotated-secrets#p-stylecolorbluesshp) section.

# Create a Rotated SSH Secret in the Akeyless Console

> 👍 Note
>
> To start working with Rotated Secrets from the [Akeyless Console](https://docs.akeyless.io/docs/create-an-ssh-rotated-secret#create-a-rotated-ssh-secret-in-the-akeyless-console), you need to configure the [Gateway](https://docs.akeyless.io/docs/api-gw) URL thus enabling communication between the Akeyless SaaS and the Akeyless Gateway.

1. Log in to the Akeyless Console, and go to **Items > New > Rotated Secret > SSH**.

2. Define a **Name** of the Rotated Secret, and specify the **Location** as a path to the virtual folder where you want to create the new Rotated Secret, using slash `/` separators. If the folder does not exist, it will be created together with the Rotated Secret.

3. Define the remaining settings as follows:

* **Delete Protection:** When enabled, it protects the Rotated Secret from accidental deletion.

* **Target:** Defines the name of the [SSH Target](doc:ssh-target) to be associated with the Rotated Secret.

* **Authenticate with the following credentials:** Determines how to connect to the target server:
  * **User credentials:** Use the credentials defined inside the Rotated Secret item.
  * **Target credentials:** Use the credentials defined inside the [SSH Target](doc:ssh-target) item.

> 👍 Note
>
> Select **Target credentials** if the Rotated Secret user is not authorized to change their own password, and a privileged user, like the [SSH Target](doc:ssh-target) user, is required to change the password on behalf of the Rotated Secret user.

* **Rotator type:** Determines the rotator type:
  * **Password**: Rotates the password defined inside the Rotated Secret item.
  * **Target**: Rotates the password defined inside the [SSH Target](doc:ssh-target) item.

* **Username:** Defines the SSH username which password should be rotated.

* **Password:** Defines the password to rotate.

> 👍 Note
>
> You can rotate the password for the [SSH Target](doc:ssh-target) too, by creating a Rotated Secret with the **Rotator type** set to **Target**. When you're using a **Target** rotator, the access role with which this Rotated Secret is associated must have read and update permissions on the corresponding Target.

* **Rotation Statement:** In this field you can provide a [Custom Rotation Statement](doc:create-an-ssh-rotated-secret#custom-rotation-statement).

* **Password Length**: Set the user's password length.

* **Gateway:** Select the Gateway through which the secret will be rotated.

* **Protection key**: To enable zero-Knowledge, select a key with a Customer Fragment. For more information, [read here](doc:implement-zero-knowledge).

* **Auto rotate:** Determines if automatic rotation is enabled.

* **Rotation interval (in days):** Defines the number of days (1-365) to wait between automatic password rotations when **Auto Rotate** is enabled.

* **Rotation hour (local time zone):** Defines the time when the password should be rotated if **Auto Rotate** is enabled.

* **Rotation Notification**: If you wish to get a notification before the next **Automatic Rotation**, click on ⊕ Add Notification and adjust the day count to any number you desire. This can be done multiple times to be notified more than once.

4. Click **Finish**.

# Custom Rotation Statement

Akeyless Rotated Secret for an [SSH Target](doc:ssh-target) supports a Custom Rotation Statement. This script or command will be executed on the target server after the secret rotation operation completes. You can specify any command you need.

For example, you can provide a command that will be executed instead of the default command to perform a secret rotation operation and specify three different arguments for it: **USERNAME, NEW_PASSWORD, OLD_PASSWORD**.

Where:

* `USERNAME`: The configured username within the [SSH Target](doc:ssh-target) or Rotated Secret which password should be rotated.

* `OLD_PASSWORD`: The username old password.

* `NEW_PASSWORD`: The new password generated by Akeyless.

(These arguments can also be used within any command or script that will run upon a password rotation attempt on the target server. )

Upon successful execution of your script, the Rotated Secret will be updated.

Syntax:

```shell Custom Rotation Statement
exec_command {{USERNAME}} {{NEW_PASSWORD}} {{OLD_PASSWORD}}
```

Where `exec_command` should be replaced with the path to your script or any existing command your target OS supports.

For example, to rotate a user on some Linux distribution like **RedHat**, the following statement can be used:

```shell shell
echo '{{USERNAME}}:{{NEW_PASSWORD}}'| chpasswd
```

Another example of rotating Windows service password :

```shell
net user /domain "{{USERNAME}}" {{NEW_PASSWORD}} && sc config "lfsvc" obj= "ad\{{USERNAME}}" password=  "{{NEW_PASSWORD}}" && net stop lfsvc && net start lfsvc
```

# Tutorial

Check out our tutorial video on [Creating and Using SSH Rotated Secrets](https://tutorials.akeyless.io/docs/creating-and-using-rotated-secrets) .
