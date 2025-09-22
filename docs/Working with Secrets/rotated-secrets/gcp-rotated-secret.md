---
title: GCP Rotated Secret
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
You can create a Rotated Secret for GCP Service Account. Before you start, create a [GCP Target](doc:gcp-targets) that includes the relevant information with a privileged service account assigned with the GCP service account key admin role.

When a client requests a Rotated Secret value, the Akeyless Platform connects to the GCP Cloud through your [Gateway](https://docs.akeyless.io/docs/api-gw) to rotate the service account key.

# Prerequsites

* An [Akeyless Gateway](https://docs.akeyless.io/docs/api-gw).
* [GCP Service Account](https://cloud.google.com/iam/docs/service-account-overview) with the [Service Account Key Admin](https://cloud.google.com/iam/docs/understanding-roles#iam.serviceAccountKeyAdmin) role assigned. 

# Create a Rotated GCP Service Account Secret from the CLI

To create a Rotated GCP Secret using the Akeyless CLI, run the following command:

```shell Akeyless CLI
akeyless rotated-secret create gcp \
--name <Rotated Secret name> \
--gateway-url 'https://<Your-Akeyless-GW-URL:8000>' \
--target-name <target name to associate> \
--authentication-credentials <use-user-creds|use-target-creds> \
--rotator-type <service-account-rotator|target> \
--gcp-key-file-path <path to service account private key> \
--auto-rotate <true|false> \
--rotation-interval <1-365> \
--rotation-hour <hour in UTC>
```

Where:

* `name`: A unique name of the Rotated Secret. The name can include the path to the virtual folder where you want to create the new Rotated Secret, using slash `/` separators. If the folder does not exist, it will be created together with the Rotated Secret.

* `gateway-url`: Akeyless Gateway Configuration Manager URL (port `8000`).

* `target-name`: The name of the [Target](doc:gcp-targets) with which the Rotated Secret should be associated.

* `authentication-credentials`: Determines how to connect to the target GCP account.
  * `use-user-creds` - Use the credentials defined on the Rotated Secret item.
  * `use-target-creds` - Use the credentials defined on the [GCP Target](doc:gcp-targets) item.

> 👍 Note
>
> Select `use-target-creds` if the Rotated Secret Service Account is not authorized to change their Key, and a privileged user, like the [GCP Target](doc:gcp-targets) service account, is required to change the Service Account Key on behalf of the Rotated Secret service account.

* `rotator-type`: The type of credentials to be rotated. For [GCP Targets](doc:gcp-targets), choose:
  * `service-account-rotator` - to rotate the GCP Service Account Key specified in the Rotated Secret.
  * `target` - to rotate the Access Key for the user specified in the [GCP Target](doc:gcp-targets).

* `gcp-key-file-path`: A path to the GCP Service account credentials file of the GCP Service Account whose Key should be rotated.

* `grace-rotation`: A boolean flag, when enabled, a graceful mode of rotation will be conducted, where only the older service account key will be rotated. When there is only one key, a new version will be created to maintain 2 values at the same time. 

* `auto-rotate`: Enable auto-rotation if you need to update the Service Account Key regularly. If this value is set to **true**, specify the `rotation-interval` in days, and optionally also the `rotation-hour`.
  * `grace-rotation-interval` and `grace-rotation-hour` relevant only when `grace-rotation` is **enabled**, if not provided, the main `rotation-interval` settings will take place.

You can find the complete list of parameters for this command in the [CLI Reference - Rotated Secrets](https://docs.akeyless.io/docs/cli-reference-rotated-secrets#p-stylecolorbluegcpp) section.

# Create a Rotated GCP Secret in the Akeyless Console

> 👍 Note
>
> To start working with Rotated Secrets from the Akeyless Console, you need to configure the [Gateway](https://docs.akeyless.io/docs/api-gw) URL thus enabling communication between the Akeyless SaaS and the Akeyless Gateway.

1. Log in to the Akeyless Console, and go to **Items > New > Rotated Secret > GCP**.

2. Define a **Name** of the Rotated Secret, and specify the **Location** as a path to the virtual folder where you want to create the new Rotated Secret, using slash `/` separators. If the folder does not exist, it will be created together with the Rotated Secret.

3. Define the remaining settings as follows:

* **Delete Protection:** When enabled, protects the Rotated Secret from accidental deletion.

* **Target:** Defines the name of the [GCP Target](doc:gcp-targets) to be associated with the Rotated Secret.

* **Rotator type:** Determines the rotator type:
  * **Service Account**: Rotates the Key defined inside the Rotated Secret item.
  * **Target**: Rotates the Key defined inside the [GCP Target](doc:gcp-targets) item.

* **Authenticate with the following credentials:** Determines how to connect to the target GCP account:
  * **User credentials:** Use the credentials defined inside the Rotated Secret item.
  * **Target credentials:** Use the credentials defined inside the [GCP Target](doc:gcp-targets) item.

> 👍 Note
>
> Select **Target credentials** if the Rotated Secret Service Account is not authorized to change their own Key, and a privileged user, like the [GCP Target](doc:gcp-targets) Service Account, is required to change the Key on behalf of the Rotated Secret user.

* **SA Credentials:** Relevant only for Service Account Rotator Type, provide the exact Key to rotate.
* **SA Details:** Relevant only for Service Account Rotator Type, provide the Service Account details in order to rotate the Service Account Key, **SA Email** , and  **SA Key ID**.  **Note** When **Key ID**  is not provided, upon successful creation, a new Key will be automatically created for the relevant Service Account, and upon deletion of the Rotated Secret, the Service Account Key will be deleted from GCP as well.
* **Gateway:** Select the Gateway through which the secret will be rotated.
* **Protection key**: To enable zero-Knowledge, select a key with a Customer Fragment. For more information, [read here](doc:implement-zero-knowledge).
* **Graceful Rotation:**  When enabled, a graceful mode of rotation will be conducted, where only the older Service Account Key will be rotated. When there is only one Key, a new version will be created to maintain 2 keys at the same time.
* **Auto rotate:** Determines if automatic rotation is enabled.
* **Rotation interval (in days):** Defines the number of days (1-365) to wait between automatic Access Key rotations when **Auto Rotate** is enabled.
* **Rotation hour (local time zone):** Defines the time when the Access Key should be rotated if **Auto Rotate** is enabled.
* **Graceful Rotation Interval (in days):**  Specifies the number of days (range: 1–365) to wait between the main **Rotation Interval** and the **Grace Rotation**. This setting is applicable only when both Auto Rotate and Graceful Rotation are enabled. If left empty, the system will apply the main **Rotation Interval** to both versions of the secret.
* **Rotation Notification**: If you wish to get a notification before the next **Automatic Rotation**, click on ⊕ Add Notification and adjust the day count to any number you desire. This can be done multiple times to be notified more than once.

4. Click **Finish**.
