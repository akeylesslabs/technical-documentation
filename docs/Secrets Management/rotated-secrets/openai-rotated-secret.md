---
title: OpenAI Rotated Secret
deprecated: false
hidden: false
metadata:
  robots: index
---
You can create a Rotated Secret for an OpenAI [Admin API Key](https://platform.openai.com/docs/api-reference/admin-api-keys). Before you get started, ensure you create an [OpenAI Target](https://docs.akeyless.io/docs/openai-target) that includes the Organization ID, as well as an OpenAI Admin API Key.

## Prerequisites

* An [Akeyless Gateway](https://docs.akeyless.io/docs/api-gw)
* [OpenAI Target](https://docs.akeyless.io/docs/openai-target) which holds an OpenAI Admin API Key.

## Create a Rotated OpenAI Secret with the CLI

To create a OpenAI Rotated Secret using the Akeyless CLI, run the following command:

```shell
akeyless rotated-secret create openai \
--name <Rotated secret name> \
--gateway-url 'https://<Your-Akeyless-GW-URL>:8000' \
--target-name <target name to associate> \
--authentication-credentials <use-user-creds|use-target-creds> \
--rotator-type <api-key|target> \
--api-key-id <api key id> \
--api-key <api key> \
--auto-rotate <true|false> \
--rotation-interval <1-365> \
--rotation-hour <hour in UTC>
```

Where:

* `name`: A unique name of the Rotated Secret. The name can include the path to the virtual folder where you want to create the new Rotated Secret, using slash `/` separators. If the folder does not exist, it will be created together with the Rotated Secret.

* `gateway-url`: Akeyless Gateway Configuration Manager URL (port `8000`).

* `target-name`: The name of the [OpenAI Target](https://docs.akeyless.io/docs/openai-target)with which the Rotated Secret should be associated.

* `authentication-credentials`: Determines how to connect to the target OpenAI account.
    * `use-user-creds` - Use the credentials defined on the Rotated Secret item.
    * `use-target-creds` - Use the credentials defined on the [OpenAI Target](https://docs.akeyless.io/docs/openai-target) item.

* `rotator-type`: The type of credentials to be rotated. For [OpenAI Target](https://docs.akeyless.io/docs/openai-target), choose:
    * `api-key` - to rotate the API Key specified in the Rotated Secret.
    * `target` - to rotate the API Key for the user specified in the [OpenAI Target](https://docs.akeyless.io/docs/openai-target).

* `api-key-id`: The Admin API key ID to rotate.

* `api-key`: The Admin API Key to rotate.

* `auto-rotate`: Enable auto-rotation if you need to update the API Key regularly. If this value is set to **true**, specify the `rotation-interval` in days, and optionally also the `rotation-hour`.

## Create a Rotated OpenAI Secret in the Akeyless Console

> ℹ️ **Note:**
>
> To start working with Rotated Secrets from the Akeyless Console, you need to configure the [Gateway](https://docs.akeyless.io/docs/api-gw) URL thus enabling communication between the Akeyless SaaS and the Akeyless Gateway.

1. Log in to the Akeyless Console, and go to **Items > New > Rotated Secret > OpenAI**.

2. Define a **Name** of the Rotated Secret, and specify the **Location** as a path to the virtual folder where you want to create the new Rotated Secret, using slash `/` separators. If the folder does not exist, it will be created together with the Rotated Secret.

3. Define the remaining settings as follows:

    * **Delete Protection:** When enabled, protects the Rotated Secret from accidental deletion.

    * **Target:** Defines the name of the [OpenAI Target](https://docs.akeyless.io/docs/openai-target) to be associated with the Rotated Secret.

    * **Authenticate with the following credentials:** Determines how to connect to the target OpenAI account:
        * **User credentials:** Use the credentials defined inside the Rotated Secret item.
        * **Target credentials:** Use the credentials defined inside the [OpenAI Target](https://docs.akeyless.io/docs/openai-target) item.

    * **Rotator type:** Determines the rotator type:
        * **API Key**: Rotates the API Key defined inside the Rotated Secret item.
        * **Target**: Rotates the API Key defined inside the [OpenAI Target](https://docs.akeyless.io/docs/openai-target) item.

    * **API Key ID:** Defines the API Key ID whose API Key should be rotated.

    * **API Key:** Defines the API Key to rotate.

    * **Gateway:** Select the Gateway through which the secret will be rotated.

    * **Protection key**: To enable zero-Knowledge, select a key with a Customer Fragment. For more information, [read here](https://docs.akeyless.io/docs/implement-zero-knowledge).

    * **Auto rotate:** Determines if automatic rotation is enabled.

    * **Rotation interval (in days):** Defines the number of days (1-365) to wait between automatic API Key rotations when **Auto Rotate** is enabled.

    * **Rotation hour (local time zone):** Defines the time when the API Key should be rotated if **Auto Rotate** is enabled.

    * **Rotation Notification**: If you wish to get a notification before the next **Automatic Rotation**, click **⊕ Add Notification** and adjust the day count to any number you prefer. This can be done multiple times to be notified more than once.

4. Click **Finish**.
