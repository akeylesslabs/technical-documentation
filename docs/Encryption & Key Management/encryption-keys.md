---
title: Encryption Keys
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
# Introduction

The Akeyless Platform combines the capabilities of an HSM and a KMS to provide enhanced key-life cycle management, including cryptographic key generation, protection, versioning/rotation (more on this subject on the key rotation guide [Key Rotation](doc:key-rotation)), and using keys with Encryption-as-a-Service and Digital Signing functions.

## Key Types

Akeyless supports a wide range of encryption keys, including:

* AES128GCM 
* AES256GCM
* AES128SIV
* AES256SIV
* RSA1024
* RSA2048
* RSA3072
* RSA4096
* AES128CBC
* AES256CBC

> 📘 Info
>
> CBC type algorithms are easy to misuse, require additional data to be supplied when used, and are not authenticated. We recommend using a different type of algorithm unless there is a clear use case for it.

## Key States

A key can be in one of three states, **Enabled**, **Disabled**, or **Pending Deletion**. The default state of a key is enabled unless stated otherwise, and can be transferred between states by any user with the appropriate permissions.\
Any keys that are not in an **Enabled** state cannot be used for any cryptographic operations (**Encrypt** or **Decrypt**). Attempting to set a key that is protecting a different item in the system into a **Disabled** or **Pending Deletion** state will fail.

# Key Use in CLI

## Creating an Encryption Key

To create an encryption key, use these commands with the following parameters:

`n`: The desired name for the key\
`a`: The desired encryption algorithm for the key

```shell AES128GCM
akeyless create-dfc-key -n MyAES128GCMKey -a AES128GCM
```
```shell AES256GCM
akeyless create-dfc-key -n MyAES256GCMKey -a AES256GCM
```
```shell AES128SIV
akeyless create-dfc-key -n MyAES128SIVKey -a AES128SIV
```
```shell AES256SIV
akeyless create-dfc-key -n MyAES256SIVKey -a AES256SIV
```
```shell RSA1024
akeyless create-dfc-key -n MyRSAKey -a RSA1024
```
```shell RSA2048
akeyless create-dfc-key -n MyRSAKey -a RSA2048
```
```shell AES256CBC
akeyless create-dfc-key -n MyCBC -a AES256CBC
```

> 📘 Info
>
> To list all available options for key creation run this command: `akeyless create-dfc-key -h`

## Managing an Encryption Key

* Delete an Encryption Key: Delete an obsolete Encryption Key or an obsolete version of an Encryption Key.\
  You may schedule a later deletion date by adding a `delete-in-days` parameter.

```shell Delete Immidiately
akeyless delete-item -n MyAES256GCMKey
```
```shell Scheduled Delete
akeyless delete-item -n MyAES128GCMKey --delete-in-days=30
```

* Get the public key from your RSA encryption key: 

```shell Get RSA Public Key
akeyless get-rsa-public -n MyRSAKey
```

* Disabling a Key: Changes a key's state to `disabled`.\
  This command can also be used to cancel a pending `delete` command, changing the key to the disabled state, from which it can be re-enabled.

```shell Disabling a Key
akeyless set-item-state -n MyAES256GCMKey -s disabled
```

* Enabling a Key: This can be used to return a disabled key to an enabled state.

```shell Enabling a Key
akeyless set-item-state -n MyAES256GCMKey -s enabled
```

## Using the Encryption Key

After creating a key, you can use it to encrypt values using this command with the following parameters:\
`k`: The name of the key to encrypt with.\
`p`: The string to encrypt.

> 📘 Info
>
> When using a CBC type encryption algorithm, there will be an additional parameter called the initialization vector, a 16 bytes of random data, encoded in base64 format, which must be unique to each encryption operation, and must be saved in order to decrypt the value, marked with the parameter -X.

```shell AES128GCM
akeyless encrypt -k MyAES256GCMKey -p 12345
```
```shell AES256CBC
akeyless encrypt -k cbc -p 12345 -X iv=7iBxRZ3NvucULGXgpsUFGw==
```

The output should look like a jumbled string of characters

```shell AES128GCM
AQAAAAEIAacq7xBbq3PYFnTmuUwqdRHclYjti/5u/MvVacv7mtFjlJQtUIpY13YF
```
```shell AES256CBC
AQAAAAEIAWj/BDSTdvCHMG1aqBW+r+u41nEvN1qTRQ==
```

Similarly, you can use it in order to Decrypt values using this command with the following parameters:\
`k`: The name of the key to encrypt with.\
`c`: The string to decrypt.

```shell AES128GCM
akeyless decrypt -k MyAES256GCMKey -c AQAAAAEIAacq7xBbq3PYFnTmuUwqdRHclYjti/5u/MvVacv7mtFjlJQtUIpY13YF
```
```shell AES256CBC
akeyless decrypt -k cbc -c AQAAAAEIAWj/BDSTdvCHMG1aqBW+r+u41nEvN1qTRQ== -X iv=7iBxRZ3NvucULGXgpsUFGw==
```

The output should be the message you encrypted beforehand:

```shell AES128GCM
12345
```
```shell AES256CBC
12345
```

Using **HMAC** with encryption:\
You may choose to add a hash function encryption over a key with the following command:

```shell
akeyless hmac -p <plaintext> -f <hash function> -k <key>
```

selecting a hash function between sha-256 and sha-512. The full parameters for this command can be found [here](https://docs.akeyless.io/docs/cli-reference-encryption-keys#p-stylecolorbluehmacp).

# Key Use in the Console

## Creating an Encryption Key

1. Log in to the Akeyless Console, and go to **Items** > **New** > **Encryption Key** > **DFC™**.

2. Define a **Name** for the key.

3. Define the remaining parameters as follows:

* **Location:** The path to the virtual folder in which you want to create the new key, using slash `/` separators.
  > 👍 Note
  >
  > If the folder does not exist, it will be created together with the authentication method.

* **Description:** General description of the key (optional).

* **Tags:** Assign tags to the key (optional).

* **Delete Protection:** When enabled, protects the Encryption Key from accidental deletion.

* **Type:** The algorithm type of key to be created (`AESxxxGCM`, `AESxxxSIV`, `AESxxxCBC`, `RSAxxxx`).

* **Customer Fragment:** If you have an existing [customer fragment](https://docs.akeyless.io/docs/dfc), you may attach it to the key. If you wish to generate one, please refer to [these instructions](https://docs.akeyless.io/docs/cli-reference-encryption-keys#p-stylecolorbluegen-customer-fragmentp).

* **Protection level (For classic keys targeting GCP):** Users can select either "software" (default) or "hardware" (HSM) options for key creation. Choosing "hardware" generates keys within a Hardware Security Module for enhanced security. For classic keys targeting GCP, you can select the protection level (hardware or software) after creating the key. In the "Provision to an external KMS" section, click "Attach," select the GCP target, and choose the appropriate protection level.\
  .

## Managing an Encryption Key

* To delete the key, go to the key's location in your repository, select it and tap the trash icon. You will get the option to choose if you wish to delete it immediately or in a set amount of days. The key must be set to be disabled via the edit options before doing so. A scheduled deletion can be canceled by re-selecting the delete option.
* To view the public key for RSA keys, go to the folder in Akeyless where you saved the desired key, select it, and tap **get public RSA key**.

## Using the Encryption Key

1. Go to the folder in Akeyless where you saved the desired key and select it.

2. Tap the **Encrypt/Decrypt text** button

3. Select the desired operation and enter the required text

> 📘 Info
>
> When using a CBC type encryption algorithm, there will be an additional parameter called the initialization vector, 16 bytes of random data, encoded in base64 format, which must be unique to each encryption operation, and must be saved in order to decrypt the value, marked with the parameter -X.

# Tutorial

Check out our tutorial video on <a href="https://tutorials.akeyless.io/docs/creating-and-rotating-encryption-keys" target="_blank" style="color: #00e">Creating and Rotating Encryption Keys</a>.
