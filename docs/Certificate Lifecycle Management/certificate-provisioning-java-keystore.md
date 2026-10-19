---
title: Certificate Provisioning to Java Key Store
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
In addition to [provisioning certificates](https://docs.akeyless.io/docs/certificate-provisioning) as standalone PEM/PFX files, Akeyless supports provisioning a certificate directly into a **Java Key Store** (`.jks` / `.p12`) on a [Linux](https://docs.akeyless.io/docs/ssh-target) or [Windows](https://docs.akeyless.io/docs/windows-target) target, utilizing the `keytool` storetypes `JKS` and `PKCS12`.

Any [stored](https://docs.akeyless.io/docs/certificate-storage) certificate can be provisioned to a Java Key Store through the [Gateway](https://docs.akeyless.io/docs/gateway-overview), whereupon successful provisioning, future renewals of the certificate will be provisioned automatically to the same keystore entry.

Setting up certificate provisioning requires **Target** permissions on the Gateway.

<Callout icon="ℹ️" theme="info">
  ### **Provisioning Permissions on Target:**

  To prevent partial files, the Gateway first saves new items (certificates, keys, and so on) in a temporary folder on your server, then atomically renames them into the final paths you specify. Ensure the temporary folder is writable by the user defined in the Target.
</Callout>

## Provisioning a Certificate to a Java Key Store Using the Akeyless CLI

Run the following CLI command to provision a certificate into a Java Key Store:

```shell
akeyless assoc-target-item \
--name <Certificate name> \
--target-name <Target Name> \
--gateway-url 'https://<Your-Akeyless-GW-URL>:8000' \
--keystore-path <Path on the target to the .jks/.p12 keystore file> \
--keystore-password <Keystore password> \
--key-alias <Alias the cert+key entry is stored/updated under> \
--keystore-type[=pkcs12] <Keystore format> \
--key-password <Key password> \
--overwrite-alias \
--create-keystore
```

Where:

- `name`: The **Certificate** item name.

- `target-name`: The **Target** item name, to provision the certificate.

- `gateway-url`: Akeyless Gateway URL (port `8000`).

- `keystore-path`: Path on the target to the `.jks`/`.p12` keystore file (for example, `/opt/app/config/keystore.jks`).

- `keystore-password`: The keystore password, needed to open and write to the keystore.

- `key-alias`: The alias the cert+key entry is stored/updated under.

- `keystore-type`: Optional, the keystore format: `jks` or `pkcs12`. Defaults to `pkcs12`.

- `key-password`: Optional, a per-entry password, only needed if it differs from the keystore password.

- `overwrite-alias`: Optional, overwrite the entry if the alias already exists. Without it, a renewal onto an existing alias has no defined behavior.

- `create-keystore`: Optional, create a new keystore at the path if none exists. Without it, a typo'd path could silently fail instead of erroring.

All of these flags are only relevant for certificate provisioning to Java Key Store endpoints.

You can find the complete list of additional parameters for this command in the [CLI Reference - Encryption Keys](https://docs.akeyless.io/docs/cli-reference-encryption-keys#assoc-target-item) section.

## Provisioning a Certificate to a Java Key Store Using the Akeyless Console

1. Log in to the Akeyless Console, and go to **Items**, find the certificate you wish to provision.
2. Click on the **Certificate** item, click on the **Provisioning** tab, and then **Attach**.
3. Enter the following parameters:

- **Target Name** - Choose an existing [SSH](https://docs.akeyless.io/docs/ssh-target)/ [Windows](https://docs.akeyless.io/docs/windows-target) Target from the drop-down list.

- **Gateway** - Choose an existing Gateway from the drop-down list.

- **Keystore Remote Path** - Path to the `.jks`/`.p12` file on the target (for example, `/opt/app/config/keystore.jks`).

- **Keystore Password** - Needed to open and write to the keystore.

- **Key Alias** - The alias the cert+key entry is stored/updated under.

- **Keystore Type** - Dropdown: **JKS** or **PKCS12**. Defaults to **PKCS12**.

- **Key Password** - Optional, a per-entry password, only needed if it differs from the keystore password.

- **Overwrite Existing Alias** - Optional toggle. Without it, a renewal onto an existing alias has no defined behavior.

- **Create Keystore If Missing** - Optional toggle. Without it, a typo'd path could silently spawn an empty keystore instead of erroring.

<Callout icon="📘" theme="info">
  ### Inspecting a Keystore

  You can inspect the entries of a provisioned keystore on the target using the `keytool` command, for example:

  ```shell
  keytool -list -v -keystore mykeystore.jks
  ```

  This lists each alias stored in the keystore, along with its certificate chain, validity period, and fingerprints.
</Callout>