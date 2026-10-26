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

## Provisioning a Certificate to a Cloud Certificate Manager

In addition to host-based [SSH](https://docs.akeyless.io/docs/ssh-target)/[Windows](https://docs.akeyless.io/docs/windows-target)/[F5](https://www.f5.com/) targets, a certificate can be provisioned directly to **Azure Key Vault**, **AWS Certificate Manager (ACM)**, or **GCP Certificate Manager**, using an [Azure Target](https://docs.akeyless.io/docs/azure-targets), [AWS Target](https://docs.akeyless.io/docs/aws-targets), or [GCP Target](https://docs.akeyless.io/docs/gcp-targets) as a credential container to sign the API request.

Unlike host-based targets, cloud targets do not expose a shell: there is no **Post Provision Command**, and because each cloud certificate manager stores the private key, public certificate, and chain together as a single object rather than as separate local files, the **Private Key Remote Path**, **Certificate Remote Path**, and **Certificate Chain Path** fields do not apply. To trigger downstream actions after provisioning (for example, reloading a web server or flushing a CDN edge), configure your cloud provider's native eventing, such as Azure Event Grid, AWS EventBridge, or a GCP Cloud Logging sink, on the certificate-created event.

Every certificate provisioned to a cloud certificate manager through Akeyless is tagged `provisioned-by: akeyless`.

### Azure Key Vault

- **Certificate Name** - The certificate name in Azure Key Vault.

- **Key Vault Name** - **Required**, the Azure Key Vault where the certificate object will be stored.

### AWS Certificate Manager (ACM)

- **Certificate Name** - The certificate name in ACM.

- **Certificate ARN** - Optional, relevant only when renewing or overwriting an existing certificate. If left blank, ACM automatically provisions a new certificate resource.

### GCP Certificate Manager

- **Certificate Name** - The certificate name in GCP Certificate Manager.

- **Location Scope** - **Required**, defines whether the certificate is deployed to the `global` namespace or a specific region (for example, `us-central1`).

### Provisioning a Certificate to a Cloud Certificate Manager Using the CLI

Run the `assoc-target-item` command, pointed at an Azure, AWS, or GCP target, with the relevant fields for that cloud provider:

```shell
akeyless assoc-target-item \
--name <Certificate name> \
--target-name <Azure/AWS/GCP Target Name> \
--gateway-url 'https://<Your-Akeyless-GW-URL>:8000' \
--certificate-name <Certificate name in the cloud destination> \
--vault-name <Azure Key Vault name> \
--certificate-arn <Existing ACM Certificate ARN, optional> \
--location-id <GCP Location Scope: global or a region>
```

Where `vault-name`, `certificate-arn`, and `location-id` are relevant only for their respective cloud provider, as described above. You can find the complete list of additional parameters for this command, including `--bind-ssl-profiles`, in the [CLI Reference - Encryption Keys](https://docs.akeyless.io/docs/cli-reference-encryption-keys#assoc-target-item) section.
