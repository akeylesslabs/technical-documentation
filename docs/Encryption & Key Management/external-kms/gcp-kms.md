---
title: GCP KMS
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
To set up Akeyless KMS Integration with GCP KMS, follow these steps:

1. Create a new [GCP Target ](https://docs.akeyless.io/docs/gcp-targets)in the Akeyless Platform. You can do it either from the [Akeyless CLI](https://docs.akeyless.io/docs/cloud-targets#create-a-gcp-target-from-the-cli) or in the Akeyless Console. Make sure you have a GCP Keyring to target.

> 👍 Note
> 
> Remember to give the GCP Target the cloud KMS admin permissions to manage the keyring.

2. Create a [Classic Key](doc:classic-keys) in the Akeyless Platform. You can do it either from the Akeyless CLI or in the Akeyless console. Alternatively, You can also use an existing Classic Key if it fits the target's accepted algorithm types.

GCP supports the following algorithm types: `AES256GCM`, `RSA2048`, `RSA3072`, `RSA4096`, `EC256`, `EC384`.

> 👍 Note
> 
> Any classic key will be protected using the Akeyless DFC key (you can select a DFC key with Zero-Knowledge Encryption).

3. [Associate](doc:classic-keys) the key with the GCP Target. When you attach a key, a copy of the key material is securely transferred to the GCP Keyring KMS in accordance with its key import specification. 

If you are using the CLI in order to associate the key and the target, please note to use all of the GCP mandatory parameters as described in the [CLI Reference](https://docs.akeyless.io/docs/cli-reference#p-stylecolorblueassociate-a-classic-keyp):

- **project-id:** A project ID of the GCP KMS (from the keyring created in the first step).
- **location-id:**  A location ID of the GCP KMS (from the keyring created in the first step).
- **keyring-name:** A keyring name of the GCP KMS (from the keyring created in the first step).
- **purpose:**  A purpose of the key in GCP KMS.
- **kms-algorithm:** An algorithm of the key in GCP KMS.

The value of the `--purpose` parameter depends on the key type:

- For AES keys, possible values are: `ENCRYPT_DECRYPT`,`MAC`

- For RSA keys, possible values are: `ASYMMETRIC_SIGN`, `ASYMMETRIC_DECRYPT`

- For EC keys, possible values is: `ASYMMETRIC_SIGN`

The value of the `--kms-algorithm` parameter depends on the key type, key size, and the selected purpose:

[block:parameters]
{
  "data": {
    "h-0": "Key Type + Purpose",
    "h-1": "KMS Algorithm",
    "0-0": "`AES ENCRYPT_DECRYPT`",
    "0-1": "`GOOGLE_SYMMETRIC_ENCRYPTION`",
    "1-0": "`AES MAC`",
    "1-1": "`HMAC_SHA256`",
    "2-0": "`RSA ASYMMETRIC_SIGN`",
    "2-1": "`RSA_SIGN_PSS_2048_SHA256`  \n`RSA_SIGN_PSS_3072_SHA256`  \n`RSA_SIGN_PSS_4096_SHA256`  \n`RSA_SIGN_PSS_4096_SHA512`  \n`RSA_SIGN_PKCS1_2048_SHA256`  \n`RSA_SIGN_PKCS1_3072_SHA256`  \n`RSA_SIGN_PKCS1_4096_SHA256`  \n`RSA_SIGN_PKCS1_4096_SHA256`  \n`RSA_SIGN_PKCS1_4096_SHA512`  \n`RSA_SIGN_RAW_PKCS1_2048`  \n`RSA_SIGN_RAW_PKCS1_3072`  \n`RSA_SIGN_RAW_PKCS1_4096`",
    "3-0": "`RSA ASYMMETRIC_DECRYPT`",
    "3-1": "`RSA_DECRYPT_OAEP_2048_SHA256`  \n`RSA_DECRYPT_OAEP_3072_SHA256`  \n`RSA_DECRYPT_OAEP_4096_SHA256`  \n`RSA_DECRYPT_OAEP_4096_SHA512`  \n`RSA_DECRYPT_OAEP_2048_SHA1`  \n`RSA_DECRYPT_OAEP_3072_SHA1`  \n`RSA_DECRYPT_OAEP_4096_SHA1`",
    "4-0": "`ECC SYMMETRIC_SIGN`",
    "4-1": "`EC_SIGN_P256_SHA256`  \n`EC_SIGN_P384_SHA384`"
  },
  "cols": 2,
  "rows": 5,
  "align": [
    "left",
    "left"
  ]
}
[/block]