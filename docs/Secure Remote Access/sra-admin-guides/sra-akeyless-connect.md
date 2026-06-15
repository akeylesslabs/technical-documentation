---
title: Akeyless Connect
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
Akeyless connect provides you with secure CLI access to resources or a secure tunnel from any Unix terminal.

## Prerequisites

To use Akeyless Connect you need:

* Akeyless [CLI](https://docs.akeyless.io/docs/cli)
* An [SSH certificate issuer](https://docs.akeyless.io/docs/sra-ssh-certificates)
* An [Akeyless Gateway](https://docs.akeyless.io/docs/gateway-overview) with Remote Access enabled.
* A local SSH client on the end-user machine (for example, OpenSSH).
* OpenSSH v7.2 or higher on target servers.

For the unified Gateway `akeyless connect` flow (Gateway URL plus SSH host discovery), use these minimum versions:

* CLI `v1.135.0` or later
* Gateway `v4.42.0` or later
* Unified Gateway deployment (Kubernetes or equivalent)

Akeyless Connect does not replace the local SSH client. To use a non-default SSH executable, set `SSH_EXTERNAL_CLIENT` in `~/.akeyless-connect.rc`.

> ℹ️ **Note:**
>
> Starting from Windows 10, Microsoft supports the native feature "Windows Subsystem for Linux."
> This feature enables users to use their Windows OS environment as a Unix-like system.
>
> To work with the `akeyless-connect` command from a Windows machine, place the `.akeyless-connect.rc` script in your home directory.

## Set Up Akeyless Connect

Install the latest version of [Akeyless Command Line Interface (CLI)](https://docs.akeyless.io/docs/cli) or run `akeyless update` to ensure you're using the latest version.

**Optional**: Download the [akeyless-connect.rc file](https://rest.akeyless.io/Akeyless_Artifacts/Linux/SSH/.akeyless-connect.rc) and open it in your preferred file editor. This file can be used to hold default variables, shortening your connect command. It can also be helpful for customizing information to your needs.

> ℹ️ **Note (RC File Notes):**
>
> The `~/.akeyless-connect.rc` file must be placed in your local `$HOME` directory to work.
> The RC file still uses `BASTION_*` variable names for historical reasons, but the CLI flags are now `--sra-ctrl-*`.

```shell akeyless-connect.rc
# ---------------------------------------------------------------------
# Copyright © 2019-2023  Akeyless Security LTD.
#
# All rights reserved
# ----------------------------------------------------------------------

#
# This file is a user-specific configuration file for `akeyless connect` CLI command, part of Akeyless Secure Remote Access
# This file should be located under the user's home directory, named explicitly: .akeyless-connect.rc
#

# IDENTITY_FILE - the path to the ssh-key to be signed and used for Zero Trust session (if empty, default ssh-key is used)
IDENTITY_FILE=""

# CERT_ISSUER_NAME - full path to the Akeyless SSH Cert Issuer to use for Zero Trust session
CERT_ISSUER_NAME=""

# AKEYLESS_PROFILE - Akeyless CLI profile to be used
AKEYLESS_PROFILE="default"

# Akeyless CLI binary (if needed)
AKEYLESS_CLI=akeyless

# AKEYLESS_GW_SSH_URL - URL for Akeyless Gateway SSH service
AKEYLESS_GW_SSH_URL=""

# AKEYLESS_GW_REST_API - URL for Akeyless API Gateway (REST API)
AKEYLESS_GW_REST_API=""

# Following are used for control service, to configure the temporary session:
# ${BASTION_API_PROTO}://"${BASTION_API_PREFIX}${BASTION_HOST}${BASTION_API_PATH}":"${BASTION_API_PORT}
#
BASTION_API_PREFIX=""
BASTION_API_PATH=""
BASTION_API_PROTO=http
BASTION_API_PORT=9900
BASTION_SSH_PORT=22

# Allow caching of temp session creds
SESSION_CACHING=no

# Display connection stages
DISPLAY_STAGES=yes

# Use SSH Agent to store user's identity keys.
# This has been removed and no longer supported
# USE_SSH_AGENT=no

SSH_EXTRA_ARGS=""

USE_SSH_LEGACY_ALG=no

# Path to SSH executable. For example, /usr/bin/ssh
SSH_EXTERNAL_CLIENT="ssh"
```

Edit the settings as follows:

`IDENTITY_FILE` - Default is `~/.ssh/id_rsa`. Full path to the public key to be signed and used for the Zero Trust session.

`CERT_ISSUER_NAME` - Full path to the Akeyless [SSH Certificates Issuer](https://docs.akeyless.io/docs/sra-ssh-certificates) item.

`AKEYLESS_PROFILE` - Set the default profile that will be used from your Akeyless [Command Line Interface (CLI)](https://docs.akeyless.io/docs/cli). By default, it's using the `default` profile of your Akeyless CLI. For profile creation, precedence, and default-profile behavior, see [CLI Profiles](https://docs.akeyless.io/docs/cli-profiles).

`AKEYLESS_CLI` - Akeyless CLI binary (if needed).

`AKEYLESS_GW_SSH_URL` - Set your Akeyless SRA SSH endpoint in your local connection configuration (for example, `my.sra-server:22`).

`AKEYLESS_GW_REST_API` - Set your Akeyless Gateway REST API endpoint (for example, `https://rest.akeyless.io`).

`BASTION_API_PROTO` - Default is `http`. Set to `https` when your [Remote Access](https://docs.akeyless.io/docs/sra-setup-k8s) is configured with TLS. This corresponds to the SRA control API protocol (CLI flag `--sra-ctrl-proto`).

`BASTION_API_PORT` - Default is `9900`. Set your matching `ssh-sra` cluster service port. This corresponds to the SRA control API port (CLI flag `--sra-ctrl-port`).

`BASTION_SSH_PORT` - Default is set to `22`. Set your matching `ssh-sra` cluster service port.

**Optional**: When working with Application Load Balancers, you can set the exact path of your `ssh-sra` service, which listens to the bastion `api` control port:

`BASTION_API_PREFIX` - Set your path prefix as your load balancer settings. This corresponds to the SRA control API port (CLI flag `--sra-ctrl-subdomain`).

`BASTION_API_PATH` - Set your path as your load balancer settings. This corresponds to the SRA control API port (CLI flag `--sra-ctrl-path`).

Where the URL will be set as follows:

`${BASTION_API_PROTO}://"${BASTION_API_PREFIX}${BASTION_HOST}${BASTION_API_PATH}":"${BASTION_API_PORT}`

`SSH_EXTRA_ARGS` - Add any official SSH arguments.

`USE_SSH_LEGACY_ALG`- Specifies whether to use ssh-legacy-signing-algorithm. The default is No

> **Note (Compatibility Issue with Legacy SSH Versions (7.4 and 7.6)):**
>
> Customers who have upgraded their Secure Remote Access (SRA) to the latest may experience SSH connection failures when using Akeyless Connect to access remote machines running OpenSSH version 7.4 or 7.6. This occurs both in CLI and the Web portal.
>
> It is possible to bypass this issue by setting the following environment variable in the Web bastion deployment, to all outgoing SSH connections:
>
> ```shell values.yaml
> env:
>   - name: SSH_EXTRA_ARGS
>     value: -o PubkeyAcceptedKeyTypes=+ssh-rsa-cert-v01@openssh.com
> ```
>
> This workaround explicitly enables legacy SSH key types that are deprecated and **not aligned** with modern security best practices.

## Usage

Use the `akeyless connect` command to connect to a resource through the Gateway's Remote Access (more examples below). If you are using the `akeyless-connect.rc` file with a `CERT_ISSUER_NAME`, you don't need to add the `-c <cert-issuer-name>` flag in the command:

```shell General Template
akeyless connect -t <[user@]target/hostname/ip[:port]> -g <your-gateway-ip[:port]> -c <cert-issuer-name>
```

For unified Gateway deployments, configure **Allowed SSH URL** in **Manage Gateway**, then **Remote Access**, then **Configuration**. After it is set, the recommended command is to pass `-g` for the Gateway service URL and let the Gateway apply the SSH address automatically.

> ℹ️ **Note (Legacy SRA Deployments):**
>
> For legacy deployments, users still run:
>
> `akeyless connect -t <[user@]target/hostname/ip[:port]> -v <your-gateway-ip[:port]> -c <cert-issuer-name>`
>
> For backward compatibility, `-v` can still be used in unified Gateway deployments. If **Allowed SSH URL** is configured, make sure the `-v` value matches it.

For the complete `akeyless connect` flag reference, see [CLI Reference - Connect](https://docs.akeyless.io/docs/cli-reference-connect).

## Examples

### SSH

For SSH access through the SSH component, use both `-g <gateway-url>` and `-c <cert-issuer-name>`. Note that end-users require `read` permission on the cert issuer item which enables them access to the service.

```shell
akeyless connect -t user@ssh-server[:port] -g <gateway-url> -c "<Path to SSH Cert Issuer>"
```

> ℹ️ **Info:**
>
> For using different SSH cert-issuers that enable access to target-servers **without** providing `read` permission to the end-users (only `list` permission on the cert-issuers), you will need to also pass the flag: `-n cert-issuer-name` for the **other** cert-issuer. This will enable access through SRA based on its allowed-users list, where the bastion will read the secret (request the cert) on their behalf.
>
> ℹ️ **Info (Extract From Mode):**
>
> If the SSH certificate issuer is configured with externally provided usernames and a claim key name, Akeyless Connect supports **Extract From** mode. In this mode, the username is extracted from JWT sub-claims by the bastion.

### AWS

```shell
akeyless connect -t us-east-1 -c my-ssh-cert-issuer -g <gateway-url> -n "<Path to AWS Dynamic Secret>"
```

If you already defined the `Cert Issuer` inside the `akeyless-connect.rc` file, you can use:

```shell
akeyless connect -t us-east-1 -g <gateway-url> -n "<Path to AWS Dynamic Secret>"
```

### MongoDB

```shell
akeyless connect -t <mongo server IP>:27017 -g <gateway-url> -n "<Path to MongoDB Dynamic Secret>"
```

### MySQL

```shell
akeyless connect -t <mysql-server>:3306 -g <gateway-url> -n "<Path to MySQL Dynamic Secret>"
```

> ℹ️ **Note (CLI v1.146.0+):**
>
> The `connect` command supports MySQL interactive flags. For the current supported options, run `akeyless connect -h`.

MySQL interactive flags are passed through the `-C` argument using the `pre:` prefix.

Example with the long-form MySQL flag:

```shell
akeyless connect -t <mysql-server>:3306 -g <gateway-url> -n "<Path to MySQL Dynamic Secret>" -C "pre:--disable-auto-rehash"
```

Example with the short alias (`-A`) plus a post-connect SQL statement:

```shell
akeyless connect -t <mysql-server>:3306 -g <gateway-url> -n "<Path to MySQL Dynamic Secret>" -C "pre:-A; post:SELECT NOW();"
```

### Amazon EKS

```shell
akeyless connect -t <namespace>@<eks cluster endpoint without https:// > -g <gateway-url> -n "<Path to EKS Dynamic secret>"
```

### Non-interactive connection to Kubernetes

Linux:

```shell
AKEYLESS_PARAM='get pod' akeyless connect -t <k8 cluster endpoint> -g <gateway-url> -n "Path To Kubernetes DynamicSecret" --ssh-extra-args "non-interactive"
```

Windows:

```shell
$env:AKEYLESS_PARAM = 'get pods'; .\akeyless.exe connect -t <k8 cluster endpoint> -g <gateway-url> -n "Path To Kubernetes DynamicSecret" --ssh-extra-args "non-interactive"
```
