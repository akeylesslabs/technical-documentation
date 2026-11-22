---
title: Certificate Provisioning to Windows Servers
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
Certificate Provisioning to Windows servers lets you push a certificate stored in Akeyless directly to a Windows server over WinRM, using an existing [Windows Target](https://docs.akeyless.io/docs/windows-target). This is one of the [certificate provisioning](https://docs.akeyless.io/docs/certificate-provisioning) destinations supported by Akeyless.

## Provisioning a Certificate Using the Akeyless CLI

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

- The `certificate-path`, `private-key-path`, `chain-path`, `certificate-format`, `pfx-password`, and `post-provision-command` parameters work the same way as for [SSH Servers](https://docs.akeyless.io/docs/certificate-provisioning-to-ssh).
- `certificate-path` can be a file path or a Windows certificate store path, such as `Cert:\LocalMachine\My`. A PFX is imported into the certificate store using its password.

**Linked Targets:** Same as for SSH Servers, the certificate is provisioned to every host in a [Linked Target](https://docs.akeyless.io/docs/linked-target).

You can find the complete list of parameters for `assoc-target-item` in the [CLI Reference - Encryption Keys](https://docs.akeyless.io/docs/cli-reference-encryption-keys#assoc-target-item) section.

## Provisioning a Certificate Using the Akeyless Console

1. Log in to the Akeyless Console, go to **Items**, and find the certificate you wish to provision.
2. Click on the **Certificate** item, and click on the **Provisioning** tab.
3. Click **Attach** to add a new row to the table.
4. Enter the following parameters:

- **Target Name** - Choose an existing Windows Target from the drop-down list.
- **Gateway** - Choose the Gateway that provisions the certificate.
- **Certificate Remote Path** - The path, or Windows certificate store path, where the certificate is provisioned.
- **Certificate Format** - The file format the certificate is provisioned in: **PEM** (default) or **PFX**.
- **Private Key Remote Path** - A path on the target to store the private key.
- **Certificate Chain Path** - A path on the target to store the full chain.
- **Post Provision Command** - A custom command that runs on the server after each successful provisioning, for example, to reset IIS.

5. Click **Save**. The target is added as a new row in the **Provisioning** table.
