---
title: Splunk Rotated Secret
deprecated: false
hidden: false
metadata:
  robots: index
---
You can create a Splunk Rotated Secret for common Splunk credentials. You can configure a Splunk Rotated Secret to rotate a Splunk user **password**, a Splunk **token**, or an **HTTP Event Collector (HEC) token**, helping you reduce credential exposure and maintain continuous compliance with minimal operational effort.

## Prerequisites

* An [Akeyless Gateway](https://docs.akeyless.io/docs/gateway-overview).
* [Splunk Target](https://docs.akeyless.io/docs/splunk-target) which holds a **Username** and **Password** or a **token** to authenticate.

## Create a Rotated Splunk Secret with the CLI

To create a Splunk Rotated Secret using the Akeyless CLI, run the following command:

```shell
akeyless rotated-secret create splunk \
--name <Rotated secret name> \
--target-name <target name to associate> \
--gateway-url 'https://<Your-Akeyless-GW-URL>:8000' \
--rotator-type <target|password|token|hec-token>
```

You can find the complete list of parameters for this command in the [CLI Reference - Rotated Secrets section](https://docs.akeyless.io/docs/cli-reference-rotated-secrets#splunk).

Use `rotator-type` based on what you want to rotate:

* `target`: Rotates the token defined in the [Splunk Target](https://docs.akeyless.io/docs/splunk-target).
* `password`: Rotates the password defined in the Rotated Secret.
* `token`: Rotates the token defined in the Rotated Secret.
* `hec-token`: Rotates the HEC token defined in the Rotated Secret.

To set credential source, token ownership fields, HEC fields, and rotation schedule flags, use the options listed on the CLI reference page.

## Create a Rotated Splunk Secret in the Akeyless Console

> ℹ️ **Note:**
>
> To start working with Rotated Secrets from the Akeyless Console, you need to configure the [Gateway](https://docs.akeyless.io/docs/gateway-overview) URL thus enabling communication between the Akeyless SaaS and the Akeyless Gateway.

1. Log in to the Akeyless Console, and go to **Items > New > Rotated Secret > Splunk**.

2. Define a **Name** of the Rotated Secret, and specify the **Location** as a path to the virtual folder where you want to create the new Rotated Secret, using slash `/` separators. If the folder does not exist, it will be created together with the Rotated Secret.

3. Define the remaining settings as follows:

   * **Delete Protection:** When enabled, protects the Rotated Secret from accidental deletion.

   * **Target:** Defines the name of the [Splunk Target](https://docs.akeyless.io/docs/splunk-target) to be associated with the Rotated Secret.

   * **Authenticate with the following credentials:** Determines how to connect to the target Splunk account:
     * **User credentials:** Use the credentials defined inside the Rotated Secret item.
     * **Target credentials:** Use the credentials defined inside the [Splunk Target](https://docs.akeyless.io/docs/splunk-target) item.

   * **Rotator type:** Determines the rotator type:
     * **Target**: Rotates the Token defined inside the [Splunk Target](https://docs.akeyless.io/docs/splunk-target) item.
     * **Token**: Rotates the Token defined inside the Rotated Secret item.
     * **Password**: Rotates the Password defined inside the Rotated Secret item.
     * **HEC-Token**: Rotates the HEC-Token defined inside the Rotated Secret item.

   * **Gateway:** Select the Gateway through which the secret will be rotated.

   * **Protection key**: To enable zero-Knowledge, select a key with a Customer Fragment. For more information, [read here](https://docs.akeyless.io/docs/implement-zero-knowledge).

   * **Auto rotate:** Determines if automatic rotation is enabled.

   * **Rotation interval (in days):** Defines the number of days (1-365) to wait between automatic credential rotations when **Auto Rotate** is enabled.

   * **Rotation hour (local time zone):** Defines the time when credentials should be rotated if **Auto Rotate** is enabled.

   * **Rotation Notification**: If you wish to get a notification before the next **Automatic Rotation**, click **⊕ Add Notification** and adjust the day count to any number you prefer. This can be done multiple times to be notified more than once.

4. Click **Finish**.
