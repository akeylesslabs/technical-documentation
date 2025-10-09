---
title: Azure KMS
excerpt: ''
deprecated: false
hidden: false
metadata:
  title: ''
  description: ''
  robots: index
next:
  description: ''
  pages:
    - type: basic
      slug: key-lifecycle-management
      title: Key Lifecycle Management
---
To set up Akeyless KMS Integration with Azure KMS, follow these steps:

1. Create a new [Azure Target](https://docs.akeyless.io/docs/azure-targets) in the Akeyless Platfrom. You can do it either from the Akeyless CLI or in the Akeyless Console. Make sure you have an Azure Key Vault to target.

> 👍 Note
>
> Remember to give the Azure Target the [Key Vault Administrator](https://docs.microsoft.com/en-us/azure/key-vault/general/rbac-guide?tabs=azure-cli#azure-built-in-roles-for-key-vault-data-plane-operations) permissions to manage the Azure Key Vault.

2. Create a [Classic Key](https://docs.akeyless.io/docs/classic-keys) in the Akeyless Platform. You can do it either from the Akeyless CLI or in the Akeyless console. Alternatively, You can also use an existing Classic Key if it fits the target's accepted algorithm types.

Azure supports the following algorithm types: `RSA1024`, `RSA2048`, `RSA3072`, `RSA4096`, `EC256`, `EC384`.

For RSA keys, allowed key operations are: `decrypt`, `encrypt`, `sign`, `unwrap`, `verify`, `wrap`.

For EC keys, allowed key operations are: `sign`, `verify`.

> 👍 Note
>
> Any classic key will be protected using the Akeyless DFC key (you can select a DFC key with Zero-Knowledge Encryption).

3. [Associate](https://docs.akeyless.io/docs/classic-keys) the key with the [Azure Target](https://docs.akeyless.io/docs/azure-targets). When you attach a key, a copy of the key material is securely transferred to the Azure Key Vault KMS by its key import specification. 

If you are using the CLI in order to associate the key and the target, please note to use all of the Azure mandatory parameters as described in the [CLI Reference](https://docs.akeyless.io/docs/cli-reference#p-stylecolorblueassociate-a-classic-keyp):

* **vault-name:** The name of the Azure Vault you are targeting.
* **key-operations:** An array with allowed operations

```shell
akeyless assoc-target-item --target-name azurev --name classickey --vault-name myvault --key-operations sign
```
