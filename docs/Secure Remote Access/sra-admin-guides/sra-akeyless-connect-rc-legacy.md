---
title: Akeyless Connect RC File (Legacy)
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
> The `~/.akeyless-connect.rc` file is deprecated. It's still read by the CLI, after the CLI profile, but new deployments should set defaults with `akeyless configure` instead. See [Akeyless Connect](https://docs.akeyless.io/docs/sra-akeyless-connect) for the current setup instructions.

**Optional**: Download the [akeyless-connect.rc file](https://rest.akeyless.io/Akeyless_Artifacts/Linux/SSH/.akeyless-connect.rc) and open it in your preferred file editor. This file can be used to hold default variables, shortening your connect command. It can also be helpful for customizing information to your needs.

> ℹ️ **RC File Notes:**
>
> The `~/.akeyless-connect.rc` file must be placed in your local `$HOME` directory to work.
> The RC file still uses `BASTION_*` variable names for historical reasons, but the CLI flags are now `--sra-ctrl-*`.

> ℹ️ **Note:**
>
> Starting from Windows 10, Microsoft supports the native feature "Windows Subsystem for Linux."
> This feature enables users to use their Windows OS environment as a Unix-like system.
>
> To work with the `akeyless-connect` command from a Windows machine, place the `.akeyless-connect.rc` script in your home directory.

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

## Precedence and sudo Behavior

Every `akeyless connect` command reads settings in this order, with each level overriding the one after it:

1. The `akeyless connect` flag.
2. The CLI profile (set with `akeyless configure`).
3. The `~/.akeyless-connect.rc` file (or the older `~/.akeyless-sphere.rc`).
4. The built-in default.

When `akeyless connect` runs under `sudo`, the CLI ignores `ssh_command` and `ssh_extra_args` from the CLI profile, and `SSH_EXTERNAL_CLIENT`, `SSH_EXTRA_ARGS`, `IDENTITY_FILE`, and `SRA_SSH_PORT` from the rc file.

Every `akeyless connect` run prints a warning telling you to move these settings to the CLI profile with `akeyless configure` (run `akeyless configure -h` for the full list of options), or to pass them as `akeyless connect` flags, and then delete the rc file.

## Migrating to the CLI Profile

Use `akeyless configure` to store the equivalent of each rc setting in your CLI profile:

| rc key | Replacement |
| --- | --- |
| `CERT_ISSUER_NAME` | `akeyless configure --cert-issuer-name` (`akeyless connect` falls back to the CLI profile), or `akeyless connect -c` |
| `AKEYLESS_PROFILE` (`profile`) | `akeyless connect --profile` |
| `SRA_API_PROTO` (`BASTION_API_PROTO`) | `akeyless configure --sra-ctrl-proto` (`http` or `https`) |
| `SRA_API_PORT` (`BASTION_API_PORT`) | `akeyless configure --sra-ctrl-port` |
| `SRA_API_PREFIX` (`BASTION_API_PREFIX`) | `akeyless configure --sra-ctrl-subdomain` |
| `SRA_API_PATH` (`BASTION_API_PATH`) | `akeyless configure --sra-ctrl-path` |
| `SRA_SSH_PORT` (`BASTION_SSH_PORT`) | `akeyless configure --sra-ssh-port` (used when `--via-sra` has no port) |
| `SSH_EXTERNAL_CLIENT` | `akeyless configure --ssh-command` (path to the SSH executable, for example `/usr/bin/ssh`) |
| `SSH_EXTRA_ARGS` | `akeyless configure --ssh-extra-args` (any SSH arguments except `-i`) |
| `SESSION_CACHING` | `akeyless configure --session-caching true` or `false` |
| `DISPLAY_STAGES` | `akeyless configure --display-stages true` or `false` |
| `USE_SSH_LEGACY_ALG` | `akeyless configure --legacy-signing-alg-name` |
| `AKEYLESS_GW_REST_API` (`AKEYLESS_API_GW`) | `akeyless connect --gateway-rest-endpoint` (no CLI profile setting) |
| `IDENTITY_FILE` | `akeyless connect -i` / `--identity-file` (no CLI profile setting) |
| `GENERATE_KEY` | `akeyless connect --generate-key` (no CLI profile setting) |
| `K8S_TUNNEL` | `akeyless connect --k8s-tunnel` (no CLI profile setting) |
| `USE_SSH_AGENT` | No longer supported |

For example:

```shell
akeyless configure --profile default --cert-issuer-name /my-ssh-cert-issuer --sra-ctrl-proto https --session-caching true
```

All settings in this example are stored in the `default` CLI profile.

> ℹ️ **Note:**
>
> The current CLI doesn't read `AKEYLESS_GW_SSH_URL` or the Akeyless CLI binary path (`AKEYLESS_CLI`) from the rc file.
