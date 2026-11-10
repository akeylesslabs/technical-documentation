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
Certificate Provisioning is a process in which a certificate is injected into a remote endpoint. Currently, Akeyless supports provisioning certificates to a [Linux](https://docs.akeyless.io/docs/ssh-target) or a [Windows](https://docs.akeyless.io/docs/windows-target) and [F5](https://www.f5.com/) endpoints utilizing [Targets](https://docs.akeyless.io/docs/targets).

A single certificate can be provisioned to **multiple targets**. Each target that the certificate is provisioned to is configured independently (its own path, certificate format, post-provision command, and so on), and every provisioning is tracked as its own row in the certificate's **Provisioning** table. Future renewals of the certificate are provisioned automatically to all of the targets listed in that table.

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

You can find the complete list of additional parameters for this command, including `--bind-ssl-profiles`, in the [CLI Reference - Encryption Keys](https://docs.akeyless.io/docs/cli-reference-encryption-keys#assoc-target-item) section.

To provision the same certificate to multiple targets, run the `assoc-target-item` command again with a different `--target-name` (and, if needed, different path or format flags). Each run adds a new row to the certificate's **Provisioning** table rather than replacing the previous one.

## Provisioning a Certificate Using the Akeyless Console

1. Log in to the Akeyless Console, and go to **Items**, find the certificate you wish to provision.
2. Click on the **Certificate** item, and click on the **Provisioning** tab. The **Provisioning** tab lists a table of all the targets the certificate is currently provisioned to.
3. Click **Attach** to add a new row to the table for provisioning the certificate to another target. Repeat this step for each additional target you want to provision the certificate to.
4. Enter the following parameters:

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

5. Click **Save**. The target is added as a new row in the **Provisioning** table, alongside any other targets the certificate is already provisioned to.
6. To provision the certificate to additional targets, repeat steps 3-5. Each target in the table can be configured with its own path, format, and post-provision settings.
