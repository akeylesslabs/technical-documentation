---
title: Certificate Provisioning to F5 BIG-IP
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
Certificate Provisioning to F5 BIG-IP lets you push a certificate stored in Akeyless directly to an F5 BIG-IP device, using an existing [F5 Target](https://docs.akeyless.io/docs/f5-target). This is one of the [certificate provisioning](https://docs.akeyless.io/docs/certificate-provisioning) destinations supported by Akeyless.

Provisioning uploads the certificate, the private key, and optionally the chain to the F5 as traffic certificate and key objects. You can also bind the certificate to existing SSL profiles.

<Callout icon="far fa-triangle-exclamation" theme="warn">
  ### Not Supported for F5 BIG-IP

  The `post-provision-command` parameter and the PFX certificate format aren't supported for F5 BIG-IP. Certificates are always uploaded as traffic certificates.
</Callout>

## Provisioning a Certificate Using the Akeyless CLI

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

You can find the complete list of parameters for `assoc-target-item` in the [CLI Reference - Encryption Keys](https://docs.akeyless.io/docs/cli-reference-encryption-keys#assoc-target-item) section.

## Provisioning a Certificate Using the Akeyless Console

1. Log in to the Akeyless Console, go to **Items**, and find the certificate you wish to provision.
2. Click on the **Certificate** item, and click on the **Provisioning** tab.
3. Click **Attach** to add a new row to the table.
4. Enter the following parameters:

- **Target Name** - Choose an existing F5 Target from the drop-down list.
- **Gateway** - Choose the Gateway that provisions the certificate.
- **Certificate Remote Path** - The certificate object, in the `/<partition>/<name>` format.
- **Private Key Remote Path** - The private key object, in the same format.
- **Certificate Chain Path** - The chain object, in the same format.
- **Bind to SSL Profile(s)** - If set, the certificate is bound to an existing SSL profile.
  - **Profile Type** - Select **Client SSL** or **Server SSL**.
  - **Partition** - The partition where the profile exists. By default, the partition is taken from the **Certificate Remote Path**.
  - **Profile Name** - The name of the SSL profile.

5. Click **Save**. The target is added as a new row in the **Provisioning** table.