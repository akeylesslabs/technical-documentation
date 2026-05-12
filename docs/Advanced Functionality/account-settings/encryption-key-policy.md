---
title: Encryption Key Policies
deprecated: false
hidden: false
metadata:
  robots: index
---
Encryption Key Policies let you centrally control how encryption keys are created and used across your Akeyless account. With these policies, you can define guardrails, such as:

* Which key types are allowed as protection keys ([Classic Keys](https://docs.akeyless.io/docs/classic-keys) or [DFC](https://docs.akeyless.io/docs/dfc-overview))
* Which encryption algorithms may be used
* The maximum supported rotation interval for symmetric keys so teams can move fast without drifting from your security standards.

Policies are applied at the folder level and can automatically inherit to all subfolders, giving you consistent enforcement at scale. This makes it easy to set strict rules for sensitive environments while allowing different folders (and teams) to operate with the right level of flexibility, all while keeping key usage aligned with your organization’s governance and compliance requirements.

> ✅ **Tip:** This feature is **Early Access** and is available only when using a [Gateway](https://docs.akeyless.io/docs/gateway-overview) running version `4.46.0` or later.

## Set an Encryption Key Policy with the CLI

To set an encryption key policy using the CLI, run the following command:

```shell
akeyless policy create keys \
--path /my-key-policy \
--max-rotation-interval-days 15 \
--allowed-algorithms RSA2048 \
--allowed-key-types dfc \
--object-types items
```

Where:

* `path`: **Required.** The path the policy refers to.

* `max-rotation-interval-days`: The maximum value for the automatic rotation interval in the specified path.

* `allowed-algorithms`: Allowed key algorithms (`RSA2048`, `AES128GCM`).

* `allowed-key-types`: Allowed key protection types (`dfc`, `classic-key`).

* `allowed-key-names`: Allowed protection key names. To enforce the account default protection key, use `default-account-key`.

* `object-types`: The object types this policy applies to (`items`, `targets`). If not provided, it defaults to both `items` and `targets`.

* **Important**: `allowed-key-types` and `allowed-key-names` are mutually exclusive. Use only one of these flags in a command.
* **Note**: `max-rotation-interval-days` is not allowed when `object-types` is set to `targets` only.

## Set an Encryption Key Policy with the Console

1. Log in to the Akeyless Console, and go to **Account Settings**, then **Key Management**.
2. In the **Key Management Policies** section, press **Add**.
3. Define the remaining parameters as follows:
    * **Object Type**: Choose either **Item** or **Target**.
    * **Access Path**: Choose a path where the policy will be applied (check **Apply Recursively** to set this policy for items in folders under the specified app).
    * **Max Rotation Interval**: The maximum allowed rotation interval for keys in the specified path.
    * **Algorithm Key Types**: The allowed algorithm key types in the specified path.
    * **Protection Key Type**: **DFC**, **Classic**, or both (if **Exclusively use default key** is checked, **Classic** is irrelevant and grayed out).
    * **Protection Key Name**: The allowed protection key in the specified path (if **Exclusively use default key** is checked, this option is irrelevant and grayed out).

## Update an Existing Policy with the CLI

  To update an existing policy, run:

  ```shell
  akeyless policy update keys \
  --id p-1234567890 \
  --allowed-algorithms RSA2048 \
  --object-types items
  ```

  Use the same constraints described above for `allowed-key-types`, `allowed-key-names`, and `max-rotation-interval-days`.
