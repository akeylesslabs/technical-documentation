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

### Built-in IIS Provisioning

Instead of using `post-provision-command` to reset IIS manually, you can use the built-in IIS option to automatically bind the newly provisioned certificate to an IIS website. This requires `certificate-format` to be set to `pfx`.

```shell
akeyless assoc-target-item \
--name <Certificate name> \
--target-name <Windows Target name> \
--gateway-url 'https://<Your-Akeyless-GW-URL>:8000' \
--certificate-path <C:\certs\cert.pfx> \
--certificate-format pfx \
--pfx-password <PFX password> \
--iis-website-name <IIS website name> \
--iis-create-binding \
--iis-binding-ip-address <Binding IP address> \
--iis-binding-port 443 \
--iis-binding-hostname <Binding hostname> \
--iis-restart-website
```

Where:

- `iis-website-name` - The name of the IIS website whose HTTPS binding will be updated with the new certificate.
- `iis-create-binding` - If set, a new HTTPS binding is created on the website when no matching binding exists. If not set and no matching binding is found, provisioning fails.
- `iis-binding-ip-address` - The IP address for the binding (use `*` to bind all IP addresses). Required when creating a new binding.
- `iis-binding-port` - The port for the binding. Defaults to `443`.
- `iis-binding-hostname` - The hostname for the binding. Optional, used when creating a new binding.
- `iis-restart-website` - If set, the IIS website is restarted after the certificate is provisioned.

If `certificate-format` is not set to `pfx`, provisioning fails with the error: `IIS configuration requires PFX format. To enable IIS, set the certificate format to PFX`.

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
- **IIS** - Instead of a post provision command, you can enable the built-in IIS option to automatically replace the certificate on an IIS website binding. This option is only available when **Certificate Format** is set to **PFX**. When enabled, configure:
  - **IIS Website Name** - The name of the IIS website to update. Mandatory.
  - **Create binding if not found** - If selected, a new HTTPS binding is created when no matching binding exists on the website; otherwise, provisioning fails if no matching binding is found.
  - **Binding IP Address** - The IP address to bind to, or all IP addresses. Mandatory if creating a new binding.
  - **Binding Port** - The port to bind to. Mandatory if creating a new binding, defaults to `443`.
  - **Binding Hostname** - The hostname to bind to. Optional, used if creating a new binding.
  - **Restart IIS website after provisioning** - If selected, the IIS website is restarted after the certificate is provisioned.

5. Click **Save**. The target is added as a new row in the **Provisioning** table.
