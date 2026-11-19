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
Certificate Provisioning delivers a [stored](https://docs.akeyless.io/docs/certificate-storage) certificate to a remote destination through the [Gateway](https://docs.akeyless.io/docs/gateway-overview), using [Targets](https://docs.akeyless.io/docs/targets). Akeyless supports provisioning certificates to:

- **SSH servers**: Linux, or Windows over SSH, using an [SSH Target](https://docs.akeyless.io/docs/ssh-target).
- **Windows servers**: over WinRM, using a [Windows Target](https://docs.akeyless.io/docs/windows-target).
- **F5 BIG-IP**: using an [F5 Target](https://docs.akeyless.io/docs/f5-target).
- **Cloud certificate managers**: AWS Certificate Manager, Azure Key Vault, and GCP Certificate Manager, using an [AWS](https://docs.akeyless.io/docs/aws-targets), [Azure](https://docs.akeyless.io/docs/azure-targets), or [GCP](https://docs.akeyless.io/docs/gcp-targets) Target.

<Callout icon="📘" theme="info">
  ### Post-Provision Command for Web Servers

  When you provision a certificate to a server (an SSH or Windows Target), you can set a custom **post-provision command** that runs on the server after each successful provisioning. For example, use it to reload or restart a web server so it serves the new certificate.

  The post-provision command isn't supported for F5 BIG-IP or cloud certificate managers.
</Callout>

## How Provisioning Works

- **Multiple targets per certificate:** A certificate can be provisioned to several targets. Each target is a separate row in the certificate's **Provisioning** table, with its own settings. Adding a target adds a row and doesn't replace the existing ones. Each target can be added to a certificate only once.
- **Immediate provisioning:** When you add a target, the certificate is provisioned to it right away. If that first provisioning fails, the target isn't added.
- **Automatic provisioning after renewal:** After every renewal, the certificate is provisioned again to every target in the **Provisioning** table. Each target is provisioned through its own Gateway, and a failure on one target doesn't stop the others.
- **Events:** Every provisioning raises a `certificate-provisioning-success` or `certificate-provisioning-failure` event, which you can forward with the [Event Center](https://docs.akeyless.io/docs/event-center).

Setting up certificate provisioning requires **Target** permissions on the Gateway.

### Provisioning on Demand

To provision a certificate again without renewing it, run:

```shell
akeyless provision-certificate --name <Certificate name>
```

Without `--target-name`, the certificate is provisioned to every target in its **Provisioning** table. Add `--target-name <Target name>` to provision it to that target only.

## SSH Servers

Provisioning to an [SSH Target](https://docs.akeyless.io/docs/ssh-target) copies the certificate, its private key, and its full chain to files on the server.

<Callout icon="ℹ️" theme="info">
  ### **Provisioning Permissions on Target:**

  To prevent partial files, the Gateway first saves new items (certificates, keys, and so on) in a temporary folder in the home directory of the user defined in the Target, then moves them into the final paths you specify. Ensure the temporary folder is writable by that user.
</Callout>

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
- `certificate-format`: Optional, `pem` (default) or `pfx`. With `pfx`, a single PFX file that bundles the certificate, chain, and private key is saved to `certificate-path`, so `private-key-path` and `chain-path` can't be used.
- `pfx-password`: Required with `--certificate-format pfx`. The password that protects the PFX file.
- `post-provision-command`: Optional, a command to run on the server after each successful provisioning, for example, to reload a web server.

**Windows servers over SSH:** `certificate-path` can also be a Windows certificate store path, such as `Cert:\LocalMachine\My`. PFX isn't supported for certificate store paths over SSH. To import a PFX into a certificate store, use a [Windows Target](#windows-servers) instead.

**Linked Targets:** When the Target is a [Linked Target](https://docs.akeyless.io/docs/linked-target), the certificate is provisioned to every host in it, using the parent Target's credentials.

## Windows Servers

Provisioning to a [Windows Target](https://docs.akeyless.io/docs/windows-target) delivers the certificate over WinRM.

```shell
akeyless assoc-target-item \
--name <Certificate name> \
--target-name <Windows Target name> \
--gateway-url 'https://<Your-Akeyless-GW-URL>:8000' \
--certificate-path <C:\certs\cert.pfx> \
--certificate-format pfx \
--pfx-password <PFX password> \
--post-provision-command <"iisreset">
```

Where:

- The `certificate-path`, `private-key-path`, `chain-path`, `certificate-format`, `pfx-password`, and `post-provision-command` parameters work the same way as for [SSH Servers](#ssh-servers).
- `certificate-path` can be a file path or a Windows certificate store path, such as `Cert:\LocalMachine\My`. A PFX is imported into the certificate store using its password.

**Linked Targets:** Same as for SSH Servers, the certificate is provisioned to every host in a [Linked Target](https://docs.akeyless.io/docs/linked-target).

## F5 BIG-IP

Provisioning to an [F5 Target](https://docs.akeyless.io/docs/f5-target) uploads the certificate, the private key, and optionally the chain to the F5 as traffic certificate and key objects. You can also bind the certificate to existing SSL profiles.

```shell
akeyless assoc-target-item \
--name <Certificate name> \
--target-name <F5 Target name> \
--gateway-url 'https://<Your-Akeyless-GW-URL>:8000' \
--certificate-path </Common/my-cert> \
--private-key-path </Common/my-key> \
--chain-path </Common/my-chain> \
--bind-ssl-profiles client-ssl:Common:my-profile \
--f5-save-config \
--f5-sync-device-group <Device group name>
```

Where:

- `certificate-path`: Required. The certificate object, in the format `/<partition>/<name>`, for example `/Common/my-cert`. Nested sub-paths aren't supported for file objects.
- `private-key-path`: Optional, the private key object, in the same format. If not set, the key uses the certificate's path.
- `chain-path`: Optional, the chain object, in the same format.
- `bind-ssl-profiles`: Optional, binds the certificate to an existing SSL profile, in the format `<type>:<partition>:<name>`, where `<type>` is `client-ssl` or `server-ssl`. Leave the partition empty to use the certificate's partition, or add a folder for a profile under an application folder, for example `client-ssl:Common/Shared:my-profile`. To bind several profiles, repeat the flag. Binding requires both the certificate and the private key. Without this flag, only the certificate and key objects are uploaded, and no SSL profile is changed.
- `f5-save-config`: Optional, saves the F5 running configuration after each successful provisioning, so the certificate survives a reboot. This also saves any other unsaved change on the device.
- `f5-sync-device-group`: Optional, syncs the configuration to this device group after each successful provisioning, so the HA peer serves the same certificate. This implies `f5-save-config`, and it overwrites unsynced changes on the other members of the group. If the device group doesn't exist, provisioning fails before anything is uploaded.

<Callout icon="❗️" theme="error">
  ### Not Supported for F5 BIG-IP

  The `post-provision-command` parameter and the PFX certificate format aren't supported for F5 BIG-IP. Certificates are always uploaded as traffic certificates.
</Callout>

## Cloud Certificate Managers

Provisioning to AWS Certificate Manager, Azure Key Vault, or GCP Certificate Manager uploads the certificate, private key, and chain as a single certificate object in the cloud provider. The cloud Target holds only the credentials used to call the provider's API.

```shell AWS ACM
akeyless assoc-target-item \
--name <Certificate name> \
--target-name <AWS Target name> \
--gateway-url 'https://<Your-Akeyless-GW-URL>:8000' \
--certificate-name <Certificate name in ACM> \
--certificate-arn <Existing ACM certificate ARN>
```
```shell Azure Key Vault
akeyless assoc-target-item \
--name <Certificate name> \
--target-name <Azure Target name> \
--gateway-url 'https://<Your-Akeyless-GW-URL>:8000' \
--certificate-name <Certificate name in Key Vault> \
--key-vault <Key Vault name>
```
```shell GCP Certificate Manager
akeyless assoc-target-item \
--name <Certificate name> \
--target-name <GCP Target name> \
--gateway-url 'https://<Your-Akeyless-GW-URL>:8000' \
--certificate-name <Certificate ID in GCP> \
--location-scope <global|region>
```

Where:

- `certificate-name`: Required. The name of the certificate in the cloud provider.
- `certificate-arn`: AWS only, optional. The ARN of an existing imported ACM certificate to re-import into, which replaces its certificate and key.
- `key-vault`: Azure only, required. The Azure Key Vault to provision the certificate to.
- `location-scope`: GCP only, required. `global`, or a region such as `us-central1`.

<Callout icon="far fa-triangle-exclamation" theme="warn">
  ### AWS: Set the Certificate ARN to Avoid Duplicates

  Without `certificate-arn`, a new ACM certificate is created on every provisioning, including after each renewal.
</Callout>

- The `certificate-path`, `private-key-path`, `chain-path`, and `post-provision-command` parameters, the PFX format, and the F5 parameters aren't supported for cloud certificate managers.
- Every certificate provisioned by Akeyless is tagged or labeled `provisioned-by=akeyless` in the cloud provider.
- **GCP:** If a certificate with the same ID already exists, Akeyless updates it only if it has the `provisioned-by=akeyless` label. Otherwise, provisioning fails. Choose another name, or add the label to the existing certificate.

For required cloud permissions, Console fields, and post-provisioning actions, see [Certificate Provisioning to Cloud Providers](https://docs.akeyless.io/docs/certificate-provisioning-to-cloud-providers).

You can find the complete list of parameters for `assoc-target-item` in the [CLI Reference - Encryption Keys](https://docs.akeyless.io/docs/cli-reference-encryption-keys#assoc-target-item) section.

## Provisioning a Certificate Using the Akeyless Console

1. Log in to the Akeyless Console, go to **Items**, and find the certificate you wish to provision.
2. Click on the **Certificate** item, and click on the **Provisioning** tab. The **Provisioning** tab lists all the targets the certificate is currently provisioned to.
3. Click **Attach** to add a new row to the table.
4. Enter the following parameters:

- **Target Name** - Choose an existing Target from the drop-down list: an SSH, Windows, F5, AWS, Azure, or GCP Target.

- **Gateway** - Choose the Gateway that provisions the certificate.

- **Certificate Remote Path** - SSH, Windows, and F5. The path where the certificate is provisioned. For F5, use the `/<partition>/<name>` format.

- **Certificate Format** - SSH and Windows. The file format the certificate is provisioned in: **PEM** (default) or **PFX**.

- **Private Key Remote Path** - SSH, Windows, and F5. A path on the target to store the private key.

- **Certificate Chain Path** - SSH, Windows, and F5. A path on the target to store the full chain.

- **Post Provision Command** - SSH and Windows. A custom command that runs on the server after each successful provisioning, for example, to reload a web server.

- **Bind to SSL Profile(s)** - F5 only. If set, the certificate is bound to an existing SSL profile.
  - **Profile Type** - Select **Client SSL** or **Server SSL**.
  - **Partition** - The partition where the profile exists. By default, the partition is taken from the **Certificate Remote Path**.
  - **Profile Name** - The name of the SSL profile.

- **Cloud fields** - AWS, Azure, and GCP. Fill in the fields that match the CLI parameters above. For details, see [Certificate Provisioning to Cloud Providers](https://docs.akeyless.io/docs/certificate-provisioning-to-cloud-providers).

5. Click **Save**. The target is added as a new row in the **Provisioning** table.
6. To provision the certificate to additional targets, repeat steps 3-5. Each target can be configured with its own settings.
