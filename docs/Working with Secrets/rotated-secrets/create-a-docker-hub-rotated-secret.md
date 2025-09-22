---
title: Docker Hub Rotated Secret
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
You can create a Rotated Secret for Docker Hub that will rotate privileged user credentials. Before you get started, make sure you have created a [Docker Hub Target](doc:docker-hub-target).

# Create a Rotated Docker Hub Secret from the CLI

To create a Rotated Docker Hub Secret using the Akeyless CLI, run the following command:

```shell
akeyless rotated-secret create dockerhub \
--name <Rotated Secret name> \
--gateway-url 'https://<Your-Akeyless-GW-URL:8000>' \
--target-name <target name to associate> \
--password-length 16 \
--rotator-type target
--auto-rotate <true|false> \
--rotation-interval <1-365> \
--rotation-hour <hour in UTC>
```

Where:

- `name`: A unique name of the Rotated Secret. The name can include the path to the virtual folder where you want to create the new Rotated Secret, using slash `/` separators. If the folder does not exist, it will be created together with the Rotated Secret.

- `gateway-url`: Akeyless Gateway Configuration Manager URL (port `8000`).

- `target-name`: The name of the [Docker Hub Target](doc:docker-hub-target) with which the Rotated Secret should be associated.

- `password-length`: **Optional**, The user's password length.

- `rotator-type`: Must be set to `target`.

- `auto-rotate`: Enable auto-rotation if you need to update the Access Key regularly. If this value is set to **true**, specify the `rotation-interval` in days, and optionally also the `rotation-hour`.

You can find the complete list of parameters for this command in the [CLI Reference - Rotated Secrets](https://docs.akeyless.io/docs/cli-reference-rotated-secrets#p-stylecolorbluedockerhubp) section.

> 🚧 Warning
> 
> Rotating the [Target](doc:targets) credentials (i.e., changing your Docker Hub password) will invalidate all existing personal access tokens.

# Create a Rotated Docker Hub Secret in the Akeyless Console.

> 👍 Note
> 
> To start working with Rotated Secrets from the [Akeyless Console](https://docs.akeyless.io/docs/create-a-docker-hub-rotated-secret#create-a-rotated-docker-hub-secret-in-the-akeyless-console), you need to configure the [Gateway](https://docs.akeyless.io/docs/api-gw) URL thus enabling communication between the Akeyless SaaS and the Akeyless Gateway.

1. Log in to the Akeyless Console, and go to **Items > New > Rotated Secret > Docker**.

2. Define a **Name** of the Rotated Secret, and specify the **Location** as a path to the virtual folder where you want to create the new Rotated Secret, using slash `/` separators. If the folder does not exist, it will be created together with the Rotated Secret.

3. Define the remaining settings as follows:

- **Delete Protection:** When enabled, it protects the Rotated Secret from accidental deletion.

- **Target:** Defines the name of the [Docker Hub Target](doc:docker-hub-target) to be associated with the Rotated Secret. 

- **Password Length**: Set the length of the user's password

- **Rotator type:** Determines the rotator type:
  - **Target**: Rotates the privileged user credentials defined inside the [Docker Hub Target](doc:docker-hub-target) item.

> 👍 Note
> 
> When you're using a **Target** rotator, the access role with which this Rotated Secret is associated must have read and update permissions on the corresponding Target.

- **Gateway:** Select the Gateway through which the secret will be rotated.

- **Protection key**: To enable zero-Knowledge, select a key with a Customer Fragment. For more information, [read here](doc:implement-zero-knowledge).

- **Auto rotate:** Determines if automatic rotation is enabled.

- **Rotation interval (in days):** Defines the number of days (1-365) to wait between automatic rotations when **Auto Rotate** is enabled.

- **Rotation hour (local time zone):** Defines the time when credentials should be rotated if **Auto Rotate** is enabled.

- **Rotation Notification**: If you wish to get a notification before the next **Automatic Rotation**, click on ⊕ Add Notification and adjust the day count to any number you desire. This can be done multiple times to be notified more than once.

4. Click **Finish**.