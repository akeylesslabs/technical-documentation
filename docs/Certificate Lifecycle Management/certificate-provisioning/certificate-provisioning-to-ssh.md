---
title: Certificate Provisioning to SSH Servers
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
Certificate Provisioning to SSH servers lets you push a certificate stored in Akeyless directly to a Linux server, or a Windows server over SSH, using an existing [SSH Target](https://docs.akeyless.io/docs/ssh-target). This is one of the [certificate provisioning](https://docs.akeyless.io/docs/certificate-provisioning) destinations supported by Akeyless.

Provisioning copies the certificate, its private key, and its full chain to files on the server.

<Callout icon="ℹ️" theme="info">
  ### **Provisioning Permissions on Target:**

  To prevent partial files, the Gateway first saves new items (certificates, keys, and so on) in a temporary folder in the home directory of the user defined in the Target, then moves them into the final paths you specify. Ensure the temporary folder is writable by that user.
</Callout>

## Provisioning a Certificate Using the Akeyless CLI

```shell
akeyless assoc-target-item \
--name <Certificate name> \
--target-name <SSH Target name> \
--gateway-url 'https://<Your-Akeyless-GW-URL>:8000' \
--certificate-path </path/to/cert.pem> \
--private-key-path </path/to/key.pem> \
--chain-path </path/to/chain.pem> \
--certificate-format pem \
--post-provision-command <"systemctl reload nginx">
```

Where:

- `name`: The **Certificate** item name.
- `target-name`: The **SSH Target** name.
- `gateway-url`: Akeyless Gateway URL (port `8000`).
- `certificate-path`: A path on the server to save the certificate.
- `private-key-path`: Optional, a path on the server to save the private key.
- `chain-path`: Optional, a path on the server to save the full chain. At least one path is required, and the paths can't overlap.
- `certificate-format`: Optional, `pem` (default), `pfx`, or `jks`. With `pfx` or `jks`, a single file that bundles the certificate, chain, and private key is saved to `certificate-path`, so `private-key-path` and `chain-path` can't be used. `jks` requires Gateway version 5.8.0 or higher.
- `pfx-password`: Required with `--certificate-format pfx`. The password that protects the PFX file.
- `jks-password`: Required with `--certificate-format jks`. The password that protects the JKS keystore.
- `key-alias`: Optional, the alias the certificate and key entry is stored under in the JKS keystore (up to 128 characters). Defaults to `certificate`. Only relevant with `--certificate-format jks`.
- `post-provision-command`: Optional, a command to run on the server after each successful provisioning, for example, to reload a web server.

**Windows servers over SSH:** `certificate-path` can also be a Windows certificate store path, such as `Cert:\LocalMachine\My`. PFX and JKS aren't supported for certificate store paths over SSH. To import a PFX into a certificate store, use a [Windows Target](https://docs.akeyless.io/docs/certificate-provisioning-to-windows) instead.

**Linked Targets:** When the Target is a [Linked Target](https://docs.akeyless.io/docs/linked-target), the certificate is provisioned to every host in it, using the parent Target's credentials.

You can find the complete list of parameters for `assoc-target-item` in the [CLI Reference - Encryption Keys](https://docs.akeyless.io/docs/cli-reference-encryption-keys#assoc-target-item) section.

## Provisioning a Certificate Using the Akeyless Console

1. Log in to the Akeyless Console, go to **Items**, and find the certificate you wish to provision.
2. Click on the **Certificate** item, and click on the **Provisioning** tab.
3. Click **Attach** to add a new row to the table.
4. Enter the following parameters:

- **Target Name** - Choose an existing SSH Target from the drop-down list.
- **Gateway** - Choose the Gateway that provisions the certificate.
- **Certificate Remote Path** - The path where the certificate is provisioned.
- **Certificate Format** - The file format the certificate is provisioned in: **PEM** (default), **PFX**, or **JKS**.
- **Keystore Password** - Required when **Certificate Format** is **JKS**. The password that protects the keystore.
- **Key Alias** - Optional, the alias the certificate and key entry is stored under in the JKS keystore. Defaults to `certificate`. Only shown when **Certificate Format** is **JKS**.
- **Private Key Remote Path** - A path on the target to store the private key.
- **Certificate Chain Path** - A path on the target to store the full chain.
- **Post Provision Command** - A custom command that runs on the server after each successful provisioning, for example, to reload a web server.

5. Click **Save**. The target is added as a new row in the **Provisioning** table.
