---
title: Akeyless SCP
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
Akeyless SCP enables secure copy via [Secure Remote Access Bastion](doc:secure-remote-access-bastion).

> 👍 Note
> 
> Akeyless SCP currently supports only UNIX-like OS.

## Prerequisite

- Akeyless [Secure Remote Access Bastion](doc:secure-remote-access-bastion).

- [SSH Issuer](doc:how-to-configure-ssh).

- OpenSSH V7.3 or higher on target servers.

## Usage

1. Download Akeyless SCP script: 

```curl Akeyless SCP
curl -o akeyless-scp https://download.akeyless.io/Akeyless_Artifacts/Linux/SSH/akeyless-scp
chmod +x akeyless-scp
mv akeyless-scp /usr/local/bin
```

2. Create a resource file called **~/.akeyless-connect.rc** as follows:

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

# AKEYLESS_GW_REST_API - URL for Akeyless API Gateway (RestAPI)
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
USE_SSH_AGENT=yes

SSH_EXTRA_ARGS=""

# Path to SSH executable. e.g. /usr/bin/ssh
SSH_EXTERNAL_CLIENT="ssh"
```

The latest version of this file can be found in [Akeyless official artifacts](https://rest.akeyless.io/Akeyless_Artifacts/Linux/SSH/). 

Edit the settings as follows: 

`IDENTITY_FILE` - Default is `~/.ssh/id_rsa`. Full path to the private key to be signed and used for the Zero Trust session.

`CERT_ISSUER_NAME` - Full path to the Akeyless [SSH Certificates Issuer](doc:ssh-and-pkitls-certificates) item. 

`AKEYLESS_PROFILE` - Set the default profile that will be used from your Akeyless [Command Line Interface (CLI)](doc:cli). By default, it's using the `default` profile of your Akeyless CLI.

`AKEYLESS_CLI` - Akeyless CLI binary (if needed).

`AKEYLESS_GW_REST_API` - Set your Akeyless Gateway URL on port `8080` for [Zero-Knowledge](doc:zero-knowledge) items and for internal network access.

`BASTION_API_PROTO` - Default is `http`. Set to `https` when your [Secure Remote Access Bastion](doc:secure-remote-access-bastion) is configured with TLS.  

`BASTION_API_PORT` - Default is set to `9900`. Set your matching `ssh-sra` cluster service port. 

`BASTION_SSH_PORT` - Default is set to `22`. Set your matching `ssh-sra`  cluster service port. 

**Optional** when working with Application Load Balancers, you can set the exact path of your `ssh-sra` service, which listens to the bastion `api` control port: 

`BASTION_API_PREFIX` - Set your path prefix as your load balancer settings.

`BASTION_API_PATH` - Set your path as your load balancer settings.

Where the URL will be set as follow: 

`${BASTION_API_PROTO}://"${BASTION_API_PREFIX}${BASTION_HOST}${BASTION_API_PATH}":"${BASTION_API_PORT}`

`SSH_EXTRA_ARGS` - Add any official SSH arguments.

3. Use the `akeyless-scp` command to perform secure copy to remote target server via Akeyless Secure Remote Access Bastion:

Full options list:

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

For example, this command will copy a local file to a remote server.

```shell
akeyless-scp user@destination-server -v <sra-bastion-ssh-service> --local-file /full/local/location/file --remote-file /remote/location/file
```

## Working With SSH Keys

When the remote host doesn’t support SSH Certificates, you can still work with **Akeyless SCP** utilizing SSH Keys where the relevant private key is stored as a [Static Secret](doc:static-secrets) within Akeyless, where the connection from the client to the Akeyless Bastion is established over short-lived SSH certificate, and from the Akeyless Bastion, the connection is established over SSH using keys, for example: 

```shell
akeyless-scp <username>@<target-host> -v <sra-bastion-ssh-service> --local-file demo_file --remote-file /home/ubuntu/demo_file --name "/path/to/static-secret-of-ssh_private_key"
```

The `--name` should point to a **static secret** in Akeyless holding the SSH private key. Users should have **only** `list` permission on this item, while the Bastion should have `read` permission.

In that case, a tunnel will be established, and the Akeyless Bastions will fetch the key and allow the client to use it without exposing it to them.