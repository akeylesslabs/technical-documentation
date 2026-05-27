---
title: Akeyless File Transfer and Akeyless SCP
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
Use this page to transfer files securely through Akeyless Secure Remote Access (SRA), including both upload and download operations through the SRA bastion.

For current deployments, use `akeyless file upload` and `akeyless file download`, which are built into the Akeyless CLI.

This page also includes legacy `akeyless-scp` guidance for existing automation that still depends on the script.

## Akeyless File Transfer

The `akeyless file` command enables secure file transfer to and from remote targets through the SRA bastion. It is built into the Akeyless CLI and supports both upload and download operations without requiring additional scripts.

These commands run on the client machine and invoke the local `scp`/`ssh` tooling to perform transfer over an SRA tunnel.

At runtime, the CLI resolves target and bastion connection parameters (from command flags or profile), requests short-lived access by way of the configured SSH certificate issuer, and then establishes the tunnel used by `scp` for upload/download.

If local `scp`/`ssh` binaries are missing or not available in `PATH`, file transfer commands fail on the client before transfer starts.

> ℹ️ **Note:**
>
> `akeyless file` currently supports only Unix-like operating systems. On Windows, use [Windows Subsystem for Linux (WSL)](https://learn.microsoft.com/windows/wsl/) and run the command from your Linux shell.

### Prerequisites

* Akeyless [CLI](https://docs.akeyless.io/docs/cli) (latest version recommended; run `akeyless update` to upgrade).
* An [SSH certificate issuer](https://docs.akeyless.io/docs/sra-ssh-certificates).
* An [Akeyless Gateway](https://docs.akeyless.io/docs/gateway-overview) with Remote Access enabled.
* A local `ssh` and `scp` client (for example, OpenSSH).
* OpenSSH v7.3 or higher on target servers.
* The appropriate SRA permission on your certificate issuer:
    * **Upload**: `sra_upload_files`.
    * **Download**: `sra_download_files`.

### Permission Model

`akeyless file` enforces SRA access control through the [SSH certificate issuer](https://docs.akeyless.io/docs/sra-ssh-certificates) item, not against the raw target host. Before transfer, the command performs a best-effort permission pre-flight against the certificate issuer path to verify that the caller holds the required capability (`sra_upload_files` or `sra_download_files`).

Certificate issuance by the SRA bastion is the authoritative enforcement gate.

If `--cert-issuer-name` is omitted, the CLI resolves it from the active profile or `~/.akeyless-connect.rc`. In that case, the pre-flight is skipped and permission is enforced at certificate issuance time.

### Usage

Upload a local file to a remote target:

```shell
akeyless file upload \
  -t <user@ssh-server[:port]> \
  -T '-L <local-port>:<remote-host>:<remote-port>' \
  --source-path /local/path/to/file \
  --destination-path /remote/path/to/file \
  -g <gateway-url> \
  -c <cert-issuer-name>
```

Download a remote file to a local destination:

```shell
akeyless file download \
  -t <user@ssh-server[:port]> \
  -T '-L <local-port>:<remote-host>:<remote-port>' \
  --source-path /remote/path/to/file \
  --destination-path /local/path/to/file \
  -g <gateway-url> \
  -c <cert-issuer-name>
```

> ℹ️ **Note:**
>
> `akeyless file upload` and `akeyless file download` are also available as the aliases `akeyless file-upload` and `akeyless file-download`.

### Options

```shell
akeyless file upload -h
Uploads a local file to a remote target through SRA

Options:

  -t, --target             Target resource, example format user@ssh-server[:port]  (required)
  -T, --tunnel             SSH tunnel param. e.g. -T='-L :5555:0.0.0.0:5555'  (required)
      --source-path        Source file path  (required)
      --destination-path   Destination file path  (required)
  -g, --gateway-url        The Gateway URL (configuration management) address, e.g. http://localhost:8000. If not specified, the value is taken from the CLI profile.
  -c, --cert-issuer-name   Akeyless Certificate Issuer Name. If not specified, the value is taken from the CLI profile.
  -v, --via-sra            SRA host, which the connection will go through. e.g.: sra-host:port. If not specified, the value is taken from the CLI profile.
      --debug              Print debug output
  -h, --help               display help information
```

```shell
akeyless file download -h
Downloads a file from a remote target through SRA

Options:

  -t, --target             Target resource, example format user@ssh-server[:port]  (required)
  -T, --tunnel             SSH tunnel param. e.g. -T='-L :5555:0.0.0.0:5555'  (required)
      --source-path        Source file path  (required)
      --destination-path   Destination file path  (required)
  -g, --gateway-url        The Gateway URL (configuration management) address, e.g. http://localhost:8000. If not specified, the value is taken from the CLI profile.
  -c, --cert-issuer-name   Akeyless Certificate Issuer Name. If not specified, the value is taken from the CLI profile.
  -v, --via-sra            SRA host, which the connection will go through. e.g.: sra-host:port. If not specified, the value is taken from the CLI profile.
      --debug              Print debug output
  -h, --help               display help information
```

## Legacy: Akeyless SCP Script

> ⚠️ **Legacy:**
>
> `akeyless-scp` is a legacy script maintained for existing workflows. For new deployments, use `akeyless file`.

### Legacy Prerequisites

* Akeyless [Remote Access](https://docs.akeyless.io/docs/sra-setup-overview).
* An [SSH certificate issuer](https://docs.akeyless.io/docs/sra-ssh-certificates).
* OpenSSH v7.3 or higher on target servers.
* Unix-like operating system support.

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

### Legacy SSH Key Flow

When the remote host does not support SSH certificates, you can use `akeyless-scp` with SSH keys by storing the private key as a [Static Secret](https://docs.akeyless.io/docs/static-secrets).

```shell
akeyless-scp <username>@<target-host> -v <sra-bastion-ssh-service> --local-file demo_file --remote-file /home/ubuntu/demo_file --name "/path/to/static-secret-of-ssh_private_key"
```

For this flow, `--name` points to the static secret that holds the private key. Users should have `list` permission on the secret, and the bastion should have `read` permission.
