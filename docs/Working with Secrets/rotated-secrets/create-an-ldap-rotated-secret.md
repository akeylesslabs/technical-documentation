---
title: LDAP Rotated Secret
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
You can create a Rotated Secret for an LDAP user. Before you get started, ensure creating an [LDAP Target](https://docs.akeyless.io/docs/ldap-target) that includes the LDAP server information, as well as credentials for a privileged user authorized to rotate credentials.

When a client requests a Rotated Secret value, the Akeyless Platform connects to the LDAP server through your [Akeyless Gateway](https://docs.akeyless.io/docs/api-gw) to rotate the user password on your target server.

# Create a Rotated LDAP Secret from the CLI

To create a Rotated LDAP Secret using the Akeyless CLI, run the following command:

```shell Akeyless CLI
akeyless rotated-secret create ldap \
--name <secret name> \
--gateway-url 'https://<Your-Akeyless-GW-URL:8000>' \
--target-name <LDAP target name to associate> \
--authentication-credentials <use-target-creds> \
--password-length 16
--rotator-type <ldap> \
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

* `target-name`: The name of the [LDAP Target](https://docs.akeyless.io/docs/ldap-target) with which the Rotated Secret should be associated.

* `authentication-credentials`: Determines how to connect to the target server.
  * `use-target-creds` - Use the credentials defined on the [LDAP Target](https://docs.akeyless.io/docs/ldap-target) item. For LDAP targets, this is the only available option.

* `password-length`: **Optional**, the user's password length.

* `rotator-type`: The type of credentials to be rotated. For [LDAP Target](https://docs.akeyless.io/docs/ldap-target), choose:
  * `ldap` - to rotate the password for the user specified in the [LDAP Target](https://docs.akeyless.io/docs/ldap-target).

* `rotated-username`: The LDAP user whose password should be rotated.

* `rotated-password`: The password to rotate.

* `auto-rotate`: Enable auto-rotation if you need to update the password regularly. If this value is set to **true**, specify the `rotation-interval` in days, and optionally also the `rotation-hour`.

You can find the complete list of parameters for this command in the [CLI Reference - Rotated Secrets](https://docs.akeyless.io/docs/cli-reference-rotated-secrets#p-stylecolorblueldapp) section.

# Create a Rotated LDAP Secret in the Akeyless Console

> 👍 Note
>
> To start working with Rotated Secrets from the [Akeyless Console](https://docs.akeyless.io/docs/create-an-ldap-rotated-secret#create-a-rotated-ldap-secret-in-the-akeyless-console), you need to configure the [Gateway](https://docs.akeyless.io/docs/api-gw) URL thus enabling communication between the Akeyless SaaS and the Akeyless Gateway.

1. Log in to the Akeyless Console, and go to **Items > New > Rotated Secret > LDAP**.

2. Define a **Name** of the Rotated Secret, and specify the **Location** as a path to the virtual folder where you want to create the new Rotated Secret, using slash `/` separators. If the folder does not exist, it will be created together with the Rotated Secret.

3. Define the remaining settings as follows:

* **Delete Protection:** When enabled, it protects the Rotated Secret from accidental deletion.

* **Target:** Defines the name of the [LDAP Target](https://docs.akeyless.io/docs/ldap-target) to be associated with the Rotated Secret.

* **Authenticate with the following credentials:** Determines how to connect to the target server:
  * **Target credentials:** Use the credentials defined inside the [LDAP Target](https://docs.akeyless.io/docs/ldap-target) item. For LDAP targets, this is the only available option.

* **Password Length**: Set the user's password length.

* **Rotator type:** Determines the rotator type:
  * **LDAP**: Rotates the password defined inside the [LDAP Target](https://docs.akeyless.io/docs/ldap-target).

* **Username:** Defines the LDAP username which password should be rotated.

* **Password:** Defines the password to rotate.

* **User Base DN:** Defines LDAP Base DN settings.

* **LDAP User Attribute:** Defines the LDAP user attribute. The default value is `cn`.

* **Gateway:** Select the Gateway through which the secret will be rotated.

* **Protection key**: To enable zero-Knowledge, select a key with a Customer Fragment. For more information, [read here](https://docs.akeyless.io/docs/implement-zero-knowledge).

* **Auto rotate:** Determines if automatic rotation is enabled.

* **Rotation interval (in days):** Defines the number of days (1-365) to wait between automatic password rotations when **Auto Rotate** is enabled.

* **Rotation hour (local time zone):** Defines the time when the password should be rotated if **Auto Rotate** is enabled.

* **Rotation Notification**: If you wish to get a notification before the next **Automatic Rotation**, click on ⊕ Add Notification and adjust the day count to any number you desire. This can be done multiple times to be notified more than once.

4. Click **Finish**.
