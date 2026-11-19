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
> ⚠️ **Warning:**
>
> The `~/.akeyless-connect.rc` file is deprecated. Set Akeyless Connect defaults in your CLI profile with `akeyless configure` instead. If you still use the rc file, see [Akeyless Connect RC File (Legacy)](https://docs.akeyless.io/docs/sra-akeyless-connect-rc-legacy).

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

Akeyless Connect does not replace the local SSH client. To use a non-default SSH executable, set `--ssh-command` in your CLI profile (see [Set Defaults in the CLI Profile](#set-defaults-in-the-cli-profile)).

## Set Up Akeyless Connect

Install the latest version of [Akeyless Command Line Interface (CLI)](https://docs.akeyless.io/docs/cli) or run `akeyless update` to ensure you're using the latest version.

## Set Defaults in the CLI Profile

`akeyless connect` reads its defaults from the active Akeyless CLI profile. Use `akeyless configure` to set them once, instead of passing the same flags on every `akeyless connect` command. For profile creation, precedence, and default-profile behavior, see [CLI Profiles](https://docs.akeyless.io/docs/cli-profiles).

`akeyless configure` flags:

`--cert-issuer-name` - Full path to the Akeyless [SSH Certificates Issuer](https://docs.akeyless.io/docs/sra-ssh-certificates) item. `akeyless connect` falls back to this value when `-c` isn't passed.

`--sra-ctrl-proto` - Default is `http`. Set to `https` when your [Remote Access](https://docs.akeyless.io/docs/sra-setup-k8s) is configured with TLS. This corresponds to the SRA control API protocol.

`--sra-ctrl-port` - Default is `9900`. Set your matching `ssh-sra` cluster service port. This corresponds to the SRA control API port.

`--sra-ctrl-subdomain` - SRA control API URL prefix, for use with Application Load Balancers. This corresponds to the SRA control API subdomain.

`--sra-ctrl-path` - SRA control API path, for use with Application Load Balancers. This corresponds to the SRA control API path.

`--sra-ssh-port` - Default is `22`. Used when `--via-sra` has no port. Set your matching `ssh-sra` cluster service port.

`--ssh-command` - Path to the SSH executable. For example, `/usr/bin/ssh`.

`--ssh-extra-args` - Any SSH arguments except `-i`.

`--session-caching` - Whether to cache temporary session credentials (`true` or `false`).

`--display-stages` - Whether to display connection stages (`true` or `false`).

`--legacy-signing-alg-name` - Specifies whether to use the legacy SSH signing algorithm.

For example:

```shell
akeyless configure --profile default --cert-issuer-name /my-ssh-cert-issuer --sra-ctrl-proto https --session-caching true
```

All settings in this example are stored in the `default` CLI profile.

The Gateway REST endpoint, identity file, generate key, and Kubernetes tunnel settings aren't stored in the CLI profile. Set them with `akeyless connect --gateway-rest-endpoint`, `-i`/`--identity-file`, `--generate-key`, and `--k8s-tunnel` respectively.

> **Compatibility Issue with Legacy SSH Versions (7.4 and 7.6):**
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

Use the `akeyless connect` command to connect to a resource through the Gateway's Remote Access (more examples below). If `--cert-issuer-name` is set in your CLI profile, you don't need to add the `-c <cert-issuer-name>` flag in the command:

```shell General Template
akeyless connect -t <[user@]target/hostname/ip[:port]> -g <your-gateway-ip[:port]> -c <cert-issuer-name>
```

For unified Gateway deployments, configure **Allowed SSH URL** in **Manage Gateway**, then **Remote Access**, then **Configuration**. After it is set, the recommended command is to pass `-g` for the Gateway service URL and let the Gateway apply the SSH address automatically.

> ℹ️ **Legacy SRA Deployments:**
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
> ℹ️ **Extract From Mode:**
>
> If the SSH certificate issuer is configured with externally provided usernames and a claim key name, Akeyless Connect supports **Extract From** mode. In this mode, the username is extracted from JWT sub-claims by the bastion.

### AWS

```shell
akeyless connect -t us-east-1 -c my-ssh-cert-issuer -g <gateway-url> -n "<Path to AWS Dynamic Secret>"
```

If the certificate issuer is set in your CLI profile, you can use:

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

> ℹ️ **CLI v1.146.0+:**
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
