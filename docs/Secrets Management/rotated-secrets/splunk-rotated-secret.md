---
title: Splunk Rotated Secret
deprecated: false
hidden: false
metadata:
  robots: index
---
You can create a Splunk Rotated Secret for common Splunk credentials. You can configure a Splunk Rotated Secret to rotate a Splunk user **password**, a Splunk **token**, or an **HTTP Event Collector (HEC) token**, helping you reduce credential exposure and maintain continuous compliance with minimal operational effort.

## Prerequisites

* An [Akeyless Gateway](https://docs.akeyless.io/docs/api-gw).
* [Splunk Target](https://docs.akeyless.io/v1.0/docs/splunk-target) which holds a **Username** and **Password** or a **token** to authenticate.

## Create a Rotated Splunk Secret with the CLI

To create a Splunk Rotated Secret using the Akeyless CLI, run the following command:

```shell
akeyless rotated-secret create splunk \
--name <Rotated secret name> \
--gateway-url 'https://<Your-Akeyless-GW-URL>:8000' \
--target-name <target name to associate> \
--authentication-credentials <use-user-creds|use-target-creds> \
--rotator-type <target|token|Username|hec-token> \
--token <splunk token> \
--username <splunk username> \
--password <splunk password> \
--hec-token <splunk hec-token>
--auto-rotate <true|false> \
--rotation-interval <1-365> \
--rotation-hour <hour in UTC>
```

Where:

* `name`: A unique name of the Rotated Secret. The name can include the path to the virtual folder where you want to create the new Rotated Secret, using slash `/` separators. If the folder does not exist, it will be created together with the Rotated Secret.

* `gateway-url`: Akeyless Gateway Configuration Manager URL (port `8000`).

* `target-name`: The name of the [Splunk Target](https://docs.akeyless.io/v1.0/docs/splunk-target)with which the Rotated Secret should be associated.

* `authentication-credentials`: Determines how to connect to the target Splunk account.
    * `use-user-creds` - Use the credentials defined on the Rotated Secret item.
    * `use-target-creds` - Use the credentials defined on the [Splunk Target](https://docs.akeyless.io/v1.0/docs/splunk-target) item.

* `rotator-type`: The type of credentials to be rotated. For [Splunk Target](https://docs.akeyless.io/v1.0/docs/splunk-target), choose:
    * `target` - to rotate the **Token** specified in the [Splunk Target](https://docs.akeyless.io/v1.0/docs/splunk-target).
    * `token` - to rotate the **Token** specified in the Rotated Secret.
    * `username` - to rotate the **Username** specified in the Rotated Secret.
    * `hec-token` - to rotate the **HEC-Token** specified in the Rotated Secret.

* `auto-rotate`: Enable auto-rotation if you need to update the API Key regularly. If this value is set to **true**, specify the `rotation-interval` in days, and optionally also the `rotation-hour`.

## Create a Rotated Splunk Secret in the Akeyless Console

> ℹ️ **Note:**
>
> To start working with Rotated Secrets from the Akeyless Console, you need to configure the [Gateway](https://docs.akeyless.io/docs/api-gw) URL thus enabling communication between the Akeyless SaaS and the Akeyless Gateway.

1. Log in to the Akeyless Console, and go to **Items > New > Rotated Secret > Splunk**.

2. Define a **Name** of the Rotated Secret, and specify the **Location** as a path to the virtual folder where you want to create the new Rotated Secret, using slash `/` separators. If the folder does not exist, it will be created together with the Rotated Secret.

3. Define the remaining settings as follows:

    * **Delete Protection:** When enabled, protects the Rotated Secret from accidental deletion.

    * **Target:** Defines the name of the [Splunk Target](https://docs.akeyless.io/v1.0/docs/splunk-target) to be associated with the Rotated Secret.

    * **Authenticate with the following credentials:** Determines how to connect to the target Splunk account:
        * **User credentials:** Use the credentials defined inside the Rotated Secret item.
        * **Target credentials:** Use the credentials defined inside the [Splunk Target](https://docs.akeyless.io/v1.0/docs/splunk-target) item.

    * **Rotator type:** Determines the rotator type:
        * **Target**: Rotates the Token defined inside the [Splunk Target](https://docs.akeyless.io/v1.0/docs/splunk-target) item.
        * **Token**: Rotates the Token defined inside the Rotated Secret item.
        * **Username**: Rotates the Username defined inside the Rotated Secret item.
        * **HEC-Token**: Rotates the HEC-Token defined inside the Rotated Secret item.

    * **Gateway:** Select the Gateway through which the secret will be rotated.

    * **Protection key**: To enable zero-Knowledge, select a key with a Customer Fragment. For more information, [read here](https://docs.akeyless.io/docs/implement-zero-knowledge).

    * **Auto rotate:** Determines if automatic rotation is enabled.

    * **Rotation interval (in days):** Defines the number of days (1-365) to wait between automatic API Key rotations when **Auto Rotate** is enabled.

    * **Rotation hour (local time zone):** Defines the time when the API Key should be rotated if **Auto Rotate** is enabled.

    * **Rotation Notification**: If you wish to get a notification before the next **Automatic Rotation**, click **⊕ Add Notification** and adjust the day count to any number you prefer. This can be done multiple times to be notified more than once.

4. Click **Finish**.
