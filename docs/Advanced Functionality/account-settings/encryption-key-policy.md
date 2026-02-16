---
title: Encryption Key Policies
deprecated: false
hidden: false
metadata:
  robots: index
---
Encryption Key Policies let you centrally control how encryption keys are created and used across your Akeyless account. With these policies, you can define guardrails such as which key types are allowed as protection keys [Classic Keys](https://docs.akeyless.io/docs/classic-keys) vs [DFC](https://docs.akeyless.io/docs/dfc-deep-dive), which encryption algorithms may be used, and the maximum supported rotation interval for symmetric keys so teams can move fast without drifting from your security standards.

Policies are applied at the folder level and can automatically inherit to all subfolders, giving you consistent enforcement at scale. This makes it easy to set strict rules for sensitive environments while allowing different folders (and teams) to operate with the right level of flexibility, all while keeping key usage aligned with your organization’s governance and compliance requirements.

<Callout icon="👍" theme="okay">
  **Early Access & Gateway version requirement**

  This feature is **Early Access** and is available only when using a [Gateway](https://docs.akeyless.io/docs/api-gw)
  running version `4.46.0` or later.
</Callout>

# Settings an Encryption Key Policy via the CLI

In order to set an encryption key policy using the CLI, run the following command:

```shell
akeyless policies create
```

# Settings an Encryption Key Policy via the Console

1. Log in to the Akeyless Console, and go to **Account Settings** > **Key Management**.
2. In the **Key Management Policies** section, press **Add**.
3. Define the remaining parameters as follows:
   * **Object Type**: Choose either **Item** or **Target**.
   * **Access Path**: Choose a path where the policy will be applied at (check the **Apply Recursively** in order to set this policy for items exists in folder under the specified app).
   * **Max Rotation Interval**: The allowed max rotation interval for keys in the specified path.
   * **Algorithm Key Types**: The allowed algorithm key types in the specified path.
   * **Protection Key Type**:  **DFC** or **Classic** or both, (If , (In case **Exclusively use default key** is checked, **Classic** is irrelevant and grayed out).
   * **Protection Key Type**: The allowed protection key in the specified path, (In case **Exclusively use default key** is checked, this option is irrelevant and grayed out).
