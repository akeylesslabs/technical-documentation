---
title: Database Rotated Secret
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
You can create a Rotated Secret for a database user. Currently, Akeyless Rotated Secrets can be created for the following databases:

* Amazon Redshift

* Cassandra

* Microsoft SQL Server

* MongoDB

* MySQL

* Oracle Database

* PostgreSQL

* Redis

* SAP HANA

* Snowflake

> 🚧 Warning
>
> Before you get started, ensure creating a [Database Target](doc:database-targets) that includes the hostname, connection settings, and credentials for a privileged user authorized to rotate credentials.

When a client requests a Rotated Secret value, the Akeyless Platform connects to the database server through your [Gateway](https://docs.akeyless.io/docs/api-gw) to rotate the user password on your target database.

# Create a Rotated Database Secret from the CLI

To create a rotated database secret using the Akeyless CLI, run the following command:

```shell Akeyless CLI
akeyless rotated-secret create <DB type> \
--name <Rotated Secret name> \
--gateway-url 'https://<Your-Akeyless-GW-URL:8000>' \
--target-name <target name to associate> \
--authentication-credentials <use-user-creds|use-target-creds> \
--password-length 16 \
--rotator-type <password|target> \
--rotated-username <username> \
--rotated-password <password to rotate> \
--auto-rotate <true|false> \
--rotation-interval <1-365> \
--rotation-hour <hour in UTC> 
```

Where:

* `name`: A unique name of the Rotated Secret. The name can include the path to the virtual folder where you want to create the new Rotated Secret, using slash `/` separators. If the folder does not exist, it will be created together with the Rotated Secret.

* `gateway-url`: Akeyless Gateway Configuration Manager URL (port `8000`).

* `target-name`: The name of the [Database Target](doc:database-targets) with which the Rotated Secret should be associated.

* `authentication-credentials`: Determines how to connect to the target database.
  * `use-user-creds` - Use the credentials defined on the Rotated Secret item.
  * `use-target-creds` - Use the credentials defined on the [Database Target](doc:database-targets) item.

> 👍 Note
>
> Select `use-target-creds` if the Rotated Secret user is not authorized to change their own password, and a privileged user, like the [Database Target](doc:database-targets) user is required to change the password on behalf of the Rotated Secret user.

* `password-length`: **Optional**, The user's password length.
* `rotator-type`: The type of credentials to be rotated. For [Database Targets](doc:database-targets), choose:
  * `password` - to rotate the DB user password specified in the Rotated Secret
  * `target` - to rotate the password for the user specified in the [Database Target](doc:database-targets).
* `rotated-username`: The DB user whose password should be rotated.
* `rotated-password`: The password to rotate.
* `auto-rotate`: Enable auto-rotation if you need to update the password regularly. If this value is set to **true**, specify the `rotation-interval` in days, and optionally also the `rotation-hour`. Default `rotation-hour` is 14:00 UTC if not specified.

You can find the complete list of parameters for this command in the [CLI Reference - Rotated Secrets](https://docs.akeyless.io/docs/cli-reference-rotated-secrets-copy) section.

# Create a Rotated Database Secret in the Akeyless Console

> 👍 Note
>
> To start working with Rotated Secrets from the [Akeyless Console](https://docs.akeyless.io/docs/create-a-database-rotated-secret#create-a-rotated-database-secret-in-the-akeyless-console), you need to configure the [Gateway](https://docs.akeyless.io/docs/api-gw) URL thus enabling communication between the Akeyless SaaS and the Akeyless Gateway.

1. Log in to the Akeyless Console, and go to **Items > New > Rotated Secret > Database Type**.

2. Define a **Name** of the Rotated Secret, and specify the **Location** as a path to the virtual folder where you want to create the new Rotated Secret, using slash `/` separators. If the folder does not exist, it will be created together with the Rotated Secret.

3. Define the remaining settings as follows:

* **Delete Protection:** When enabled, it protects the Rotated Secret from accidental deletion.

* **Target:** Defines the name of the [Database Target](doc:database-targets) to be associated with the Rotated Secret.

* **Authenticate with the following credentials:** Determines how to connect to the target database:
  * **User credentials:** Use the credentials defined inside the Rotated Secret item.
  * **Target credentials:** Use the credentials defined inside the [Database Target](doc:database-targets) item.

> 👍 Note
>
> Select **Target credentials** if the Rotated Secret user is not authorized to change their own password, and a privileged user, like the [Database Target](doc:database-targets) user, is required to change the password on behalf of the Rotated Secret user.

* **Password-length**: Set the user's password length.
* **Rotator type:** Determines the rotator type:
  * **Password**: Rotates the password defined inside the Rotated Secret item.
  * **Target**: Rotates the password defined inside the [Database Target](doc:database-targets) item.
* **Username:** Defines the DB username which password should be rotated.
* **Password:** Defines the password to rotate.

> 👍 Note
>
> You can rotate the password for the [Database Target](doc:database-targets) too, by creating a Rotated Secret with the **Rotator type** set to **Target**. When you're using a **Target** rotator, the access role with which this Rotated Secret is associated must have read and update permissions on the corresponding Target.

* **Gateway:** Select the Gateway through which the secret will be rotated.

* **Protection key**: To enable zero-Knowledge, select a key with a Customer Fragment. For more information, [read here](doc:implement-zero-knowledge).

* **Auto rotate:** Determines if automatic rotation is enabled.

* **Rotation interval (in days):** Defines the number of days (1-365) to wait between automatic password rotations when **Auto Rotate** is enabled.

* **Rotation hour (local time zone):** Defines the time when the password should be rotated if **Auto Rotate** is enabled.

* **Rotation Notification**: If you wish to get a notification before the next **Automatic Rotation**, click on ⊕ Add Notification and adjust the day count to any number you desire. This can be done multiple times to be notified more than once.

4. Click **Finish**.

# Tutorial

Check out our tutorial video on <a href="https://tutorials.akeyless.io/docs/creating-and-using-rotated-secrets" target="_blank">Creating and Using MySQL Rotated Secrets</a>.
