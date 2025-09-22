---
title: Salesforce Shield
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
To set up Akeyless KMS Integration with Salesforce Shield, follow these steps:

1. Create a new Salesforce Target in the Akeyless Platfrom. You can do it either from the [Akeyless CLI](https://docs.akeyless.io/docs/cloud-targets#create-a-salesforce-target-from-the-cli) or in the Akeyless Console. Make sure you have a Salesforce OAuth2.0 app to target.

2. Create a [Classic Key](doc:classic-keys) in the Akeyless Platform. You can do it either from the Akeyless CLI or in the Akeyless console. Alternatively, You can also use an existing Classic Key if it fits the target's accepted algorithm types.

Salesforce supports only `AES256GCM` keys.

> 👍 Note
>
> Any classic key will be protected using the Akeyless DFC key (you can select a DFC key with Zero-Knowledge Encryption).

3. [Associate](doc:classic-keys) the key with the Salesforce Target. When you attach a key, a copy of the key material is securely transferred to the Salesforce KMS in accordance with its key import specification. 

If you are using the CLI in order to associate the key and the target, please note to use all of the Salesforce mandatory parameters as described in the [CLI Reference](https://docs.akeyless.io/docs/cli-reference#p-stylecolorblueassociate-a-classic-keyp):

* **tenant-secret-type:** The tenant secret type. Possible values: Data, SearchIndex, Analytics. There should be only one key of each type in Salesforce.
