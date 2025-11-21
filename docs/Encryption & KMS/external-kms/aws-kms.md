---
title: AWS KMS
excerpt: AWS Key Management Service (AWS KMS)
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
To set up Akeyless KMS Integration with AWS KMS, follow these steps:

1. Create a new [AWS Target](https://docs.akeyless.io/docs/aws-targets) in the Akeyless Platform. You can do it either from the [Akeyless CLI](https://docs.akeyless.io/docs/aws-targets#create-an-aws-target-from-the-cli) or in the [Akeyless Console](https://docs.akeyless.io/docs/aws-targets#create-an-aws-target-in-the-akeyless-console).

> 👍 Note
>
> Remember to give the AWS Target's credentials permissions to manage keys in AWS KMS regions.

2. Create a [Classic Encryption Key](https://docs.akeyless.io/docs/classic-keys) in Akeyless. You can do it either from the Akeyless CLI or in the Akeyless console. Alternatively, You can also use an existing Classic Key if it fits the target's accepted algorithm types.

AWS targets only support **AES256GCM** type keys.

> 👍 Note
>
> Any classic key will be protected using the Akeyless DFC key (you can select a DFC key with Zero-Knowledge Encryption).

3. [Associate](https://docs.akeyless.io/docs/classic-keys#associating-a-key-and-a-target-1) the key with the AWS Target. When you attach a key, a copy of the key material is securely transferred to the AWS KMS in accordance with its key import specification.

> 🚧 Warning
>
> When you associate a key with AWS, make sure to reference the **alias** when using the key in AWS. Otherwise, the association will break when you rotate the key.

You can export the key into multi-regions within AWS KMS, where the default region will be based on the [AWS Target](https://docs.akeyless.io/docs/aws-targets) region, for later replication you can set the option without specifying the extra regions for later use, for example:

```shell Multi region
akeyless assoc-target-item --target-name <target-name> --name <classic key name> --multi-region="true" --regions us-east-1 --regions us-west-1
```
