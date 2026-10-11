---
title: Certificate Provisioning
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
Certificate Provisioning is a process in which a certificate is injected into a remote endpoint. Currently, Akeyless supports provisioning certificates to a [Linux](https://docs.akeyless.io/docs/ssh-target) or a [Windows](https://docs.akeyless.io/docs/windows-target) and [F5](https://www.f5.com/) endpoints utilizing [Targets](https://docs.akeyless.io/docs/targets), as well as directly into a Java Key Store (JKS) on the target.

<Callout icon="📘" theme="info">
  ### F5 Certificate Type

  For F5 target, the certificate type is Traffic by default.
</Callout>

Any [stored](https://docs.akeyless.io/docs/certificate-storage) certificate can be provisioned through the [Gateway](https://docs.akeyless.io/docs/gateway-overview), whereupon successful provisioning, future renewals of the certificate will be provisioned automatically.

Setting up certificate provisioning requires **Target** permissions on the Gateway.

<Callout icon="ℹ️" theme="info">
  ### **Provisioning Permissions on Target:**

  To prevent partial files, the Gateway first saves new items (certificates, keys, and so on) in a temporary folder on your server, then atomically renames them into the final paths you specify. Ensure the temporary folder is writable by the user defined in the Target.
</Callout>

## Provisioning a Certificate Using the Akeyless CLI

Run the following CLI command to provision a certificate:

```shell
akeyless assoc-target-item \
--name <Certificate name> \
--target-name <Target Name> \
--gateway-url 'https://<Your-Akeyless-GW-URL>:8000' \
--certificate-path <Where to save the certificate> \
--post-provision-command <"echo Akeyless"> \
--f5-certificate-type[=traffic] <Certificate Type> \
--certificate-format[=pem] <Certificate Format>
```

Where:

- `name`: The **Certificate** item name.

- `target-name` The **Target** item name, to provision the certificate.

- `gateway-url`: Akeyless Gateway URL (port `8000`).

- `certificate-path`: A path on the **Target** to save the certificate PEM file can be used as well with `chain-path` and `private-key-path` flags to save those on different locations.

- `certificate-format`: Optional, the file format to provision the certificate in. Supported values are `pem` (default) and `pfx`.

- `post-provision-command`: Optional, a custom command to run on the remote target after successful provisioning, for example, restarting a service.

For F5 BIG-IP, SSL profiles can be bound using the `--bind-ssl-profiles` flag. The partition segment of this flag can now include a subfolder path within the administrative partition (for example, `client-ssl:Common/my-subfolder:my-profile`), in addition to a top-level partition such as `Common`.

### Provisioning a Certificate to a Java Key Store

To provision a certificate into a Java Key Store (JKS/PKCS12) instead of as standalone files, use the `--keystore-path` flag together with the other `--keystore-*`/`--key-*` flags, for example:

```shell
akeyless assoc-target-item \
--name <Certificate name> \
--target-name <Target Name> \
--gateway-url 'https://<Your-Akeyless-GW-URL>:8000' \
--keystore-path <Path to the .jks/.p12 file on the target> \
--keystore-password <Keystore password> \
--key-alias <Alias the cert+key entry is stored/updated under> \
--keystore-type[=jks] <jks/pkcs12> \
--key-password <Per-entry password, if different from the keystore password> \
--overwrite-alias \
--create-keystore
```

Where:

- `keystore-path`: Path on the target to the `.jks`/`.p12` keystore file (for example, `/opt/app/config/keystore.jks`).

- `keystore-password`: Needed to open and write to the keystore.

- `key-alias`: The alias the certificate and private key entry is stored/updated under.

- `keystore-type`: Optional, the keystore format: `jks` or `pkcs12`. Defaults to `jks`.

- `key-password`: Optional, a per-entry password, only needed if it differs from the keystore password.

- `overwrite-alias`: Optional, overwrites the entry if the alias already exists. Without this flag, a renewal onto an existing alias has no defined behavior.

- `create-keystore`: Optional, creates a new keystore at the specified path if none exists. Without this flag, a typo'd path will result in an error rather than silently creating an empty keystore.

You can find the complete list of additional parameters for this command, including `--bind-ssl-profiles` and the JKS-related flags above, in the [CLI Reference - Encryption Keys](https://docs.akeyless.io/docs/cli-reference-encryption-keys#assoc-target-item) section.

## Provisioning a Certificate Using the Akeyless Console

1. Log in to the Akeyless Console, and go to **Items**, find the certificate you wish to provision.
2. Click on the **Certificate** item, click on the **Provisioning** tab, and then **Attach**.
3. Enter the following parameters:

- **Target Name** - **Choose an existing Target** from the drop-down list to select the existing [SSH](https://docs.akeyless.io/docs/ssh-target)/ [Windows](https://docs.akeyless.io/docs/windows-target) Target.

- **Gateway** - **Choose an existing Gateway** from the drop-down list to select the relevant Gateway.

- **Certificate Remote Path** - The path where the certificate will be provisioned to in the remote machine.

- **Certificate Format** - Choose the file format the certificate will be provisioned in: **PEM** (default) or **PFX**.

- **Private Key Remote Path** - A path on the target to store the private key.

- **Certificate Chain Path** - A path on the target to store the full chain.

- **Post Provision Command** - A custom command of your choice that will be executed on the remote machine as part of the provisioning process.

- **Bind to SSL Profile(s) **- If set, the certificate will be bound to an existing SSL profile (relevant only for **F5**).
  - **Profile Type **- Select **Client SSL** or **Server SSL**.
  - **Partition** - The partition where the profile exists. By default, the partition is taken from the **Certificate Remote Path**.
  - **Profile Name **- The name of the **SSL profile**.

### Provisioning a Certificate to a Java Key Store

In addition to provisioning certificates as standalone files, you can provision a certificate directly into a Java Key Store (JKS) on the target.

1. Log in to the Akeyless Console, and go to **Items**, find the certificate you wish to provision.
2. Click on the **Certificate** item, click on the **Provisioning** tab, and then **Attach**.
3. Select **Java Key Store** as the provisioning destination, and enter the following parameters:

- **Keystore Remote Path** - Path to the `.jks`/`.p12` file on the target (for example, `/opt/app/config/keystore.jks`).

- **Keystore Password** - Needed to open and write to the keystore.

- **Key Alias** - The alias the certificate and private key entry is stored/updated under.

- **Keystore Type** - Optional, dropdown: **JKS** or **PKCS12**. Defaults to **PKCS12**.

- **Key Password** - Optional, a per-entry password, only needed if it differs from the keystore password.

- **Overwrite Existing Alias** - Optional toggle. Without it, a renewal onto an existing alias has no defined behavior.

- **Create Keystore If Missing** - Optional toggle. Without it, a typo'd path will result in an error instead of silently creating an empty keystore.
