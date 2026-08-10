---
title: Akeyless SCP Script
deprecated: false
hidden: true
metadata:
  robots: index
---
## Legacy: Akeyless SCP Script

<Callout icon="⚠️" theme="warn">
  ### **Legacy:**

  `akeyless-scp` is a legacy script maintained for existing workflows. For new deployments, use `akeyless file`.
</Callout>

### Legacy Prerequisites

- Akeyless [Remote Access](https://docs.akeyless.io/docs/sra-setup-overview).
- An [SSH certificate issuer](https://docs.akeyless.io/docs/sra-ssh-certificates).
- OpenSSH v7.3 or higher on target servers.
- Unix-like operating system support.

### Install the Legacy Script

```shell
curl -o akeyless-scp https://download.akeyless.io/Akeyless_Artifacts/Linux/SSH/akeyless-scp
chmod +x akeyless-scp
mv akeyless-scp /usr/local/bin
```

### Legacy Usage

```shell
Usage: /usr/local/bin/akeyless-scp <user@remote-server[:port]> -v <bastion-server[:port]> [options]

optional arguments:
    -i, --identity_file     Selects a file from which the identity (private key) for public key authentication is read [default is '~/.ssh/id_rsa']
    -c, --cert-issuer-name  Akeyless certificate issuer name [mandatory]
    -l, --local-file        File to copy [mandatory]
    -r, --remote-file       File to copy [default is '~/']
    -d, --direction         Transfer direction, can be: upload/download [default is 'upload']
    --profile               Use a specific profile from your Akeyless CLI
    --ssh-extra-args        Use to add official SSH arguments (except -i)
```

Example upload:

```shell
akeyless-scp user@destination-server -v <sra-bastion-ssh-service> --local-file /full/local/location/file --remote-file /remote/location/file
```
