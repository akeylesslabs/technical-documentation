---
title: Encryption Key Policy
deprecated: false
hidden: true
metadata:
  robots: index
---
Additionally to manage encryption keys access based on the existing **RBAC**, you can set custom encryption key policies in order to validate that users can access only encryption keys with settings you configured in advance, where only Admins can set those policies based on paths. 

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
