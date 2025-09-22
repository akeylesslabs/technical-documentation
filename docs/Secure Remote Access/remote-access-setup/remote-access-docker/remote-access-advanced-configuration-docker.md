---
title: Advanced Configuration
excerpt: ''
deprecated: false
hidden: true
metadata:
  title: ''
  description: ''
  robots: index
next:
  description: ''
---
# SSH Configuration

## SSH Legacy Algorithm

As both classic SSH and RDP access are based on SSH certificates, to support legacy algorithms for SSH signing, you can set the SSH Legacy Algorithm to `true` via the CLI to sign SSH certificates using the legacy '[ssh-rsa-cert-v01@openssh.com](mailto:ssh-rsa-cert-v01@openssh.com)' signing algorithm.

This can also be done via the console by going to **Gateways** -> **Your-Gateway** -> **Manage Gateway** -> **Remote Access**. 

```shell
akeyless gateway update remote-access --legacy-ssh-algorithm true --gateway-url <your-gateway-url:8000>
```

## Key Exchange Algorithm

A Key Exchange Algorithm is a method used to securely exchange cryptographic keys between parties over an insecure channel such as a public network. The primary goal of these algorithms is to enable two or more parties to securely establish a shared secret key, which can then be used for encrypting and decrypting messages during communication.

This can also be done via the console by going to **Gateways** -> **Your-Gateway** -> **Manage Gateway** -> **Remote Access**.

```shell
akeyless gateway update remote-access --kexalgs <algorithm-name> --gateway-url <your-gateway-url:8000>
```

The options for this are:

* curve25519-sha256
* diffie-hellman-group-exchange-sha1
* diffie-hellman-group-exchange-sha256
* diffie-hellman-group14-sha1
* diffie-hellman-group14-sha256
* diffie-hellman-group16-sha512
* diffie-hellman-group18-sha512
* ecdh-sha2-nistp256
* ecdh-sha2-nistp384
* ecdh-sha2-nistp521

## Concurrent Unauthenticated Connections

To specify the maximum number of concurrent unauthenticated connections to the SSH component, set the  `CONFIG_MAX_STARTUPS` variable:

```yaml
CONFIG_MAX_STARTUPS="200:30:300"
```

## SSH Fingerprint

Use this parameter to store fingerprint information in a specific folder within your Akeyless account. This approach prevents the need to manually re-accept the SSH host key fingerprint after upgrades or other changes. In the example below, the fingerprints will be stored in the `/MY_SSH_REMOTE_ACCESS_HOST_KEYS` folder.

> 📘 Permissions
>
> Ensure your remote access default Auth Method has the following permissions on that folder: `create`,`read`, `list`

```yaml
SSH_HOST_KEYS_PATH=/MY_SSH_REMOTE_ACCESS_HOST_KEYS
```

# RDP / SSH User Acces

Set the RDP / SSH Authentication with the relevant attribute that exists inside your IDP JWT, e.g. `email`, to set the connection to your target server using the current authenticated username. This can be done as follows from the CLI. 

RDP:

```yaml
akeyless gateway update remote-access --rdp-target-configuration <your-sub-claim> --ssh-target-configuration <your-sub-claim>
```

SSH:

```yaml
akeyless gateway update remote-access --ssh-target-configuration <your-sub-claim> --ssh-target-configuration <your-sub-claim>
```

This can also be done via the console by going to **Gateways** -> **Your-Gateway** -> **Manage Gateway** -> **Remote Access**

This will take effect on all SSH-based sessions, both for RDP and Linux-based systems.

## Support for Other Keyboard Layouts

To enable a keyboard layout in your remote sessions (ie Windows), use the following command (the default is `en-us-qwerty`):

This can also be done via the console by going to **Gateways** -> **Your-Gateway** -> **Manage Gateway** -> **Remote Access**

```shell
akeyless gateway update remote-access --keyboard-layout <layout-option>
```
```yaml Layout Options
value: da-dk-qwerty # Danish (Qwerty)
value: de-ch-qwertz # Swiss German (Qwertz)
value: de-de-qwertz # German (Qwertz)
value: en-gb-qwerty # UK English (Qwerty)
value: en-us-qwerty # US English (Qwerty) default
value: es-es-qwerty # Spanish (Qwerty)
value: es-latam-qwerty # Latin American (Qwerty)
value: fr-be-azerty # Belgian French (Azerty)
value: fr-ch-qwertz # Swiss French (Qwertz)
value: fr-fr-azerty # French (Azerty)
value: hu-hu-qwertz # Hungarian (Qwertz)
value: it-it-qwerty # Italian (Qwerty)
value: ja-jp-qwerty # Japanese (Qwerty)
value: no-no-qwerty # Norwegian (Qwerty)
value: pl-pl-qwerty # Polish (Qwerty)
value: pt-br-qwerty # Portuguese Brazilian (Qwerty)
value: sv-se-qwerty # Swedish (Qwerty)
value: tr-tr-qwerty # Turkish-Q (Qwerty)
```

For further configuration, please refer to the Akeyless official [repository](https://github.com/akeylesslabs/helm-charts/blob/main/charts/akeyless-secure-remote-access/README.md#akeyless-secure-remote-access).
