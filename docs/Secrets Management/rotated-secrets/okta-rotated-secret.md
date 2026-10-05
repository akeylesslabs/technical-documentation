---
title: Okta Rotated Secret
deprecated: false
hidden: true
metadata:
  robots: index
---
You can create an Okta Rotated Secret to rotate the password of an [Okta](https://www.okta.com/) user, helping you reduce credential exposure and maintain continuous compliance with minimal operational effort.

When a client requests a Rotated Secret value, the Akeyless Platform connects to your Okta account through your [Akeyless Gateway](https://docs.akeyless.io/docs/gateway-overview) to rotate the user password.

<Callout icon="ℹ️" theme="success">
  ### **Note:**

  Okta Rotated Secrets rotate user passwords only. The API token defined in the [Okta Target](https://docs.akeyless.io/docs/okta-target) is not rotated by this item.
</Callout>

## Prerequisites

* An [Akeyless Gateway](https://docs.akeyless.io/docs/gateway-overview).
* An [Okta Target](https://docs.akeyless.io/docs/okta-target) which holds the Okta URL and an API token with permission to reset user passwords.

## Create a Rotated Okta Secret with the CLI

To create an Okta Rotated Secret using the Akeyless CLI, run the following command:

```shell
akeyless rotated-secret create okta \
--name <Rotated secret name> \
--target-name <Okta target name to associate> \
--gateway-url 'https://<Your-Akeyless-GW-URL>:8000' \
--rotator-type password \
--rotated-username <Okta username> \
--rotated-password <current password> \
--password-length 16 \
--auto-rotate <true|false> \
--rotation-interval <1-365> \
--rotation-hour <hour in UTC>
```

Where:

* `name`: A unique name of the Rotated Secret. The name can include the path to the virtual folder where you want to create the new Rotated Secret, using slash `/` separators. If the folder does not exist, it will be created together with the Rotated Secret.

* `target-name`: The name of the [Okta Target](https://docs.akeyless.io/docs/okta-target) with which the Rotated Secret should be associated.

* `gateway-url`: Akeyless Gateway URL (port `8000`).

* `rotator-type`: The type of credentials to be rotated. For Okta, `password` is the only available option - it rotates the password of the user defined in the Rotated Secret.

* `rotated-username`: The Okta username whose password should be rotated.

* `rotated-password`: The current password of that user.

* `password-length`: **Optional**, the user's password length.

* `auto-rotate`: Enable auto-rotation if you need to update the password regularly. If this value is set to **true**, specify the `rotation-interval` in days, and optionally also the `rotation-hour`.

You can find the complete list of parameters for this command in the [CLI Reference - Rotated Secrets](https://docs.akeyless.io/docs/cli-reference-rotated-secrets) section.

## Create a Rotated Okta Secret in the Akeyless Console

<Callout icon="ℹ️" theme="success">
  ### **Note:**

  To start working with Rotated Secrets from the Akeyless Console, you need to configure the [Gateway](https://docs.akeyless.io/docs/gateway-overview) URL thus enabling communication between the Akeyless SaaS and the Akeyless Gateway.
</Callout>

1. Log in to the Akeyless Console, and go to **Items > New > Rotated Secret > Okta**.

2. Define a **Name** of the Rotated Secret, and specify the **Location** as a path to the virtual folder where you want to create the new Rotated Secret, using slash `/` separators. If the folder does not exist, it will be created together with the Rotated Secret.

3. Define the remaining settings as follows:

   * **Delete Protection:** When enabled, protects the Rotated Secret from accidental deletion.

   * **Target:** Defines the name of the [Okta Target](https://docs.akeyless.io/docs/okta-target) to be associated with the Rotated Secret.

   * **Rotator type:** Determines the rotator type:
     * **Password**: Rotates the password of the user defined inside the Rotated Secret item. This is the only rotator type available for Okta.

   * **Username:** The Okta username whose password should be rotated.

   * **Password:** The current password of that user.

   * **Password Length**: Set the user's password length.

   * **Gateway:** Select the Gateway through which the secret will be rotated.

   * **Protection key**: To enable zero-Knowledge, select a key with a Customer Fragment. For more information, [read here](https://docs.akeyless.io/docs/gateway-zero-knowledge).

   * **Auto rotate:** Determines if automatic rotation is enabled.

   * **Rotation interval (in days):** Defines the number of days (1-365) to wait between automatic credential rotations when **Auto Rotate** is enabled.

   * **Rotation hour (local time zone):** Defines the time when credentials should be rotated if **Auto Rotate** is enabled.

   * **Rotation Notification**: If you wish to get a notification before the next **Automatic Rotation**, click **⊕ Add Notification** and adjust the day count to any number you prefer. This can be done multiple times to be notified more than once.

4. Click **Finish**.