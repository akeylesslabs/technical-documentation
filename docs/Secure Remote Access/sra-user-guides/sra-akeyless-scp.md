---
title: 'Akeyless File Transfer '
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

For interactive SSH, database access, and generic tunnel workflows, use [Akeyless Connect](https://docs.akeyless.io/docs/sra-akeyless-connect).

For current deployments, use `akeyless file upload` and `akeyless file download`, which are built into the Akeyless CLI.

These commands use SFTP as the transfer protocol, for improved reliability and transfer performance.

## CLI Path Selection

Use the command family that matches your access goal:

1. `akeyless connect` for interactive sessions and tunnel-oriented workflows.
2. `akeyless file upload` and `akeyless file download` for secure file transfer through SRA.

Depending on your session type, files will be transferred to and from the following locations:

| Session | Upload (Your PC → Remote)                                        | Download (Remote → Your PC)                           |
| ------- | ---------------------------------------------------------------- | ----------------------------------------------------- |
| RDP     | Files are saved directly to`This PC\file-share on Guacamole RDP` | Move file to `\tsclient\file-share\Download`          |
| SSH     | Files are uploaded straight to`/home/<user`                      | Move file to `akl-downloads`, then click **Download** |

Effective access is controlled by SRA permissions, issuer policy, and target configuration.

## File Transfer

The `akeyless file` command enables secure file transfer to and from remote targets through the SRA bastion. It is built into the Akeyless CLI and supports both upload and download operations without requiring additional scripts.

These commands run on the client machine and use SFTP over an SRA tunnel.

At runtime, the CLI resolves target and bastion connection parameters (from command flags or profile), requests short-lived access by way of the configured SSH certificate issuer, and then establishes the tunnel used by SFTP for upload and download.

The client must support SFTP; file transfer commands fail if SFTP capability is not available.

<Callout icon="ℹ️" theme="info">
  ### **Note:**

  `akeyless file` currently supports only Unix-like operating systems. On Windows, use [Windows Subsystem for Linux (WSL)](https://learn.microsoft.com/windows/wsl/) and run the command from your Linux shell.
</Callout>

### Prerequisites

- Akeyless [CLI](https://docs.akeyless.io/docs/cli) (latest version recommended; run `akeyless update` to upgrade).
- An [SSH certificate issuer](https://docs.akeyless.io/docs/sra-ssh-certificates).
- An [Akeyless Gateway](https://docs.akeyless.io/docs/gateway-overview) with Remote Access enabled.
- A local `ssh` client with SFTP support (for example, OpenSSH).
- OpenSSH v7.3 or higher on target servers.
- The appropriate SRA permission on your certificate issuer:
  - **Upload**: `sra_upload_files`.
  - **Download**: `sra_download_files`.

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

<Callout icon="ℹ️" theme="info">
  ### **Note:**

  `akeyless file upload` and `akeyless file download` are also available as the aliases `akeyless file-upload` and `akeyless file-download`.
</Callout>

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

###
