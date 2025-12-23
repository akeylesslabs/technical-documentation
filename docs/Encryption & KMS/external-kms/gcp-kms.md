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

1. Create a new [GCP Target](https://docs.akeyless.io/docs/gcp-targets) in the Akeyless Platform. You can do it either from the [Akeyless CLI](https://docs.akeyless.io/docs/cloud-targets#create-a-gcp-target-from-the-cli) or in the Akeyless Console. Make sure you have a GCP Keyring to target.

> 👍 Note
>
> Remember to give the GCP Target the Cloud KMS admin permissions to manage the keyring.

2. Create a [Classic Key](https://docs.akeyless.io/docs/classic-keys) in the Akeyless Platform. You can do it either from the Akeyless CLI or in the Akeyless Console. Alternatively, You can also use an existing Classic Key if it fits the target's accepted algorithm types.

GCP supports the following algorithm types: `AES256GCM`, `RSA2048`, `RSA3072`, `RSA4096`, `EC256`, `EC384`.

> 👍 Note
>
> Any classic key will be protected using the Akeyless DFC key (you can select a DFC key with Zero-Knowledge Encryption).

3. [Associate](https://docs.akeyless.io/docs/classic-keys) the key with the GCP Target. When you attach a key, a copy of the key material is securely transferred to the GCP Keyring KMS in accordance with its key import specification.

If you are using the CLI in order to associate the key and the target, please note to use all of the GCP mandatory parameters as described in the [CLI Reference](https://docs.akeyless.io/docs/cli-reference#p-stylecolorblueassociate-a-classic-keyp):

* **project-id:** A project ID of the GCP KMS (from the keyring created in the first step).
* **location-id:** A location ID of the GCP KMS (from the keyring created in the first step).
* **keyring-name:** A keyring name of the GCP KMS (from the keyring created in the first step).
* **purpose:** A purpose of the key in GCP KMS.
* **kms-algorithm:** An algorithm of the key in GCP KMS.

The value of the `--purpose` parameter depends on the key type:

* For AES keys, possible values are: `ENCRYPT_DECRYPT`,`MAC`

* For RSA keys, possible values are: `ASYMMETRIC_SIGN`, `ASYMMETRIC_DECRYPT`

* For EC keys, possible values is: `ASYMMETRIC_SIGN`

The value of the `--kms-algorithm` parameter depends on the key type, key size, and the selected purpose:

| Key Type + Purpose | KMS Algorithm |
|---|---|
| `AES ENCRYPT_DECRYPT` | `GOOGLE_SYMMETRIC_ENCRYPTION` |
| `AES MAC` | `HMAC_SHA256` |
| `RSA ASYMMETRIC_SIGN` | `RSA_SIGN_PSS_2048_SHA256`, `RSA_SIGN_PSS_3072_SHA256`, `RSA_SIGN_PSS_4096_SHA256`, `RSA_SIGN_PSS_4096_SHA512`, `RSA_SIGN_PKCS1_2048_SHA256`, `RSA_SIGN_PKCS1_3072_SHA256`, `RSA_SIGN_PKCS1_4096_SHA256`, `RSA_SIGN_PKCS1_4096_SHA256`, `RSA_SIGN_PKCS1_4096_SHA512`, `RSA_SIGN_RAW_PKCS1_2048`, `RSA_SIGN_RAW_PKCS1_3072`, `RSA_SIGN_RAW_PKCS1_4096` |
| `RSA ASYMMETRIC_DECRYPT` | `RSA_DECRYPT_OAEP_2048_SHA256`, `RSA_DECRYPT_OAEP_3072_SHA256`, `RSA_DECRYPT_OAEP_4096_SHA256`, `RSA_DECRYPT_OAEP_4096_SHA512`, `RSA_DECRYPT_OAEP_2048_SHA1`, `RSA_DECRYPT_OAEP_3072_SHA1`, `RSA_DECRYPT_OAEP_4096_SHA1` |
| `ECC SYMMETRIC_SIGN` | `EC_SIGN_P256_SHA256`, `EC_SIGN_P384_SHA384` |
