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
Akeyless connect provides you with secure CLI access to resources or a secure tunnel from any UNIX terminal.

# Prerequisites

To use Akeyless Connect  you need:

* Akeyless CLI v1.42.0 or higher. 

* An [SSH certificate issuer](https://docs.akeyless.io/docs/ssh-certificates) for certificate authentication.

* An [Akeyless Gateway](doc:api-gw) with Remote Access enabled.

* OpenSSH v7.2 or higher on target servers.

> 👍 Note
>
> Starting from Windows 10, Microsoft supports the native feature "Windows Subsystem for Linux."\
> This feature enables users to utilize their Windows OS environment as a UNIX-like system.
>
> To work with the `akeyless-connect` command from a Windows machine, place the <code>.akeyless-connect.rc</code> script in your home directory.

# Set Up Akeyless Connect

Install the latest version of [Akeyless Command Line Interface (CLI)](doc:cli). Or run `akeyless update` to ensure you're using the latest version.

**Optional**: Download the `akeyless-connect.rc` file from [here](https://rest.akeyless.io/Akeyless_Artifacts/Linux/SSH/.akeyless-connect.rc) and open it in your preferred file editor. This file can be used to hold default variables, shortening your connect command. It can also be helpful for customizing information to your needs. If you prefer to get started without this, go straight to the Usage section below.

> 📘 RC file location
>
> Note that the `~/.akeyless-connect.rc` file must be placed in your local $HOME directory to work.

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

# AKEYLESS_GW_SSH_URL - URL for Akeyless GW SSH service
AKEYLESS_GW_SSH_URL=""

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
# This has been removed and no longer supported
# USE_SSH_AGENT=no

SSH_EXTRA_ARGS=""

USE_SSH_LEGACY_ALG=no

# Path to SSH executable. e.g. /usr/bin/ssh
SSH_EXTERNAL_CLIENT="ssh"
```

Edit the settings as follows: 

`IDENTITY_FILE` - Default is `~/.ssh/id_rsa`. Full path to the private key to be signed and used for the Zero Trust session.

`CERT_ISSUER_NAME` - Full path to the Akeyless [SSH Certificates Issuer](https://docs.akeyless.io/docs/ssh-certificates) item. 

`AKEYLESS_PROFILE` - Set the default profile that will be used from your Akeyless [Command Line Interface (CLI)](doc:cli). By default, it's using the `default` profile of your Akeyless CLI.

`AKEYLESS_CLI` - Akeyless CLI binary (if needed).

`AKEYLESS_GW_SSH_URL` - Set your Akeyless Gateway URL for the SSH service on port `8000`. The K8s service name will start with `ssh-`.

`AKEYLESS_GW_REST_API` - Set your Akeyless Gateway URL on port `8080` for [Zero-Knowledge](doc:zero-knowledge) items and for internal network access.

`BASTION_API_PROTO` - Default is `http`. Set to `https` when your [Remote Access](https://docs.akeyless.io/docs/remote-access-setup-k8s) is configured with TLS.  

`BASTION_API_PORT` - Default is set to `9900`. Set your matching `ssh-sra` cluster service port. 

`BASTION_SSH_PORT` - Default is set to `22`. Set your matching `ssh-sra` cluster service port. 

**Optional**: When working with Application Load Balancers, you can set the exact path of your `ssh-sra` service, which listens to the bastion `api` control port: 

`BASTION_API_PREFIX` - Set your path prefix as your load balancer settings.

`BASTION_API_PATH` - Set your path as your load balancer settings.

Where the URL will be set as follows: 

`${BASTION_API_PROTO}://"${BASTION_API_PREFIX}${BASTION_HOST}${BASTION_API_PATH}":"${BASTION_API_PORT}`

`SSH_EXTRA_ARGS` - Add any official SSH arguments.

`USE_SSH_LEGACY_ALG`- Specifies whether to use ssh-legacy-signing-algorithm. The default is No

> 🚧 Compatibility Issue with Legacy SSH Versions (7.4 & 7.6)
>
> Customers who have upgraded their Secure Remote Access (SRA) to the latest may experience SSH connection failures when using Akeyless Connect to access remote machines running OpenSSH version 7.4 or 7.6. This occurs both in CLI and the Web portal.
>
> It is possible to bypass this issue by setting the following environment variable in the Web bastion deployment, to all outgoiing SSH connections:
>
> ```shell values.yaml
> env:
>   - name: SSH_EXTRA_ARGS
>     value: -o PubkeyAcceptedKeyTypes=+ssh-rsa-cert-v01@openssh.com
> ```
>
> NOTE that this workaround explicitly enables legacy SSH key types that are deprecated and **not aligned** with modern security best practices.

# Usage

Use the `akeyless connect` command to connect to a resource through the Gateway's Remote Access (more examples below). If you are using the `akeyless-connect.rc` file with a `CERT_ISSUER_NAME`, you don't need to add the `-c <cert-issuer-name>` flag in the command:

```shell General Template
akeyless connect -t <[user@]target/hostname/ip[:port]> -g <your-gateway-ip[:port]> -c <cert-issuer-name>
```

> 📘 Legacy SRA Deployments
>
> For legacy deployments, users will still run:
>
> `akeyless connect -t <[user@]target/hostname/ip[:port]> -v <your-gateway-ip[:port]> -c <cert-issuer-name>`

Full options list:

```shell akeyless connect -h
-t, --target                           Target resource, example formats: user@ssh-server[:port], us-east-2, mysql-server:3306, etc.
-v, --via-bastion                      Bastion host, which the connection will go through. e.g.: bastion-host:port.
-g, --gateway-url                      The Gateway URL (configuration management) address of the ssh service, e.g. http://localhost:8000
-c, --cert-issuer-name                 Akeyless Certificate Issuer Name. If not specified will be taken from ~/.akeyless-connect.rc 
-i, --identity-file                    Selects a file from which the identity (private key) for public key authentication is read.  The default is ~/.ssh/id_dsa, ~/.ssh/id_ecdsa, ~/.ssh/id_ed25519 and ~/.ssh/id_rsa.
-n, --name                             Path to Secret, based on the required connection
    --ssh-extra-args                   Additional SSH arguments (except -i)
    --bastion-ctrl-proto[=http]        Bastion API Protocol [http/https]
    --bastion-ctrl-subdomain           Bastion control API URL prefix. e.g. https://<prefix>.bastion-host
    --bastion-ctrl-path                Bastion control API path. e.g. https://bastion-host/<path>
    --bastion-ctrl-port[=9900]         Bastion control API port. e.g. https://bastion-host:<7777>
    --gateway-rest-endpoint            Gateway RestAPI URL. e.g. https://rest.akeyless.io
-V, --ssh-version                      Output local SSH client version
    --ssh-legacy-signing-alg[=false]   Set this option to output legacy ('ssh-rsa-cert-v01@openssh.com') signing algorithm name in the ssh certificate.
    --ssh-command                      Path to SSH executable. e.g. /usr/bin/ssh
-T, --tunnel                           SSH tunnel param. e.g. -T='-L :5555:0.0.0.0:5555' 
-C, --command                          Command to execute on the target (useful for non interactive-mode). e.g. -C='ls -al'
-J, --justification                    User connection justification    
    --debug                            Output debug prints
    --profile, --token                 Use a specific profile (located at $HOME/.akeyless/profiles) or a temp access token
    --uid-token                        The universal identity token, Required only for universal_identity authentication
-h, --help                             display help information
    --json[=false]                     Set output format to JSON
    --jq-expression                    JQ expression to filter result output
    --no-creds-cleanup[=false]         Do not clean local temporary expired creds
```

## Examples

**SSH:**

For SSH access through the SSH component, please use both the `-g <gw-ssh-url>` and `-c <cert-issuer-name>` options. Note that end-users require `read` permission on the cert issuer item which enables them access to the service.

```shell Akeyless connect for SSH
akeyless connect -t user@ssh-server[:port] -g <gw-ssh-url> -c "<Path to SSH Cert Issuer>"
```

> 📘 Info
>
> For using different SSH cert-issuers that enable access to target-servers **without** providing `read` permission to the end-users (only `list` permission on the cert-issuers), you will need to also pass the flag: `-n cert-issuer-name` for the **other** cert-issuer. This will enable access through the bastion based on its allowed-users list, where the bastion will read the secret (request the cert) on their behalf.

**AWS:**

```shell Akeyless CLI
akeyless connect -t us-east-1 -c my-ssh-cert-issuer -g <gw-ssh-url>:<port> -n "<Path to AWS Dynamic Secret>"
```

In case you already defined the `Cert Issuer` inside the `akeyless-connect.rc` file you can use: 

```shell Akeyless CLI
akeyless connect -t us-east-1 -g <gw-ssh-url>:<port> -n "<Path to AWS Dynamic Secret>"
```

**MongoDB:** 

```shell Akeyless CLI
akeyless connect -t <mongo server IP>:27017 -g <gw-ssh-url>:<port> -n "<Path to MongoDB Dynamic Secret>"
```

**MySQL:**

```shell Akeyless CLI
akeyless connect -t <mysql-server>:3306 -g <gw-ssh-url>:<port> -n "<Path to MySQL Dynamic Secret>"
```

**EKS:**

```shell Akeyless CLI
akeyless connect -t <namespace>@<eks cluster endpoint without https:// > -g <gw-ssh-url>:<port> -n "<Path to EKS Dynamic secret>"
```

**Non-interactive connection to K8s:**

Linux:

```shell
AKEYLESS_PARAM='get pod' akeyless connect -t <k8 cluster endpoint> -g <gw-ssh-url> -n "Path To K8s Dynamnic Secret" --ssh-extra-args "non-interactive"
```

Windows: 

```shell
$env:AKEYLESS_PARAM = 'get pods'; .\akeyless.exe connect -t <k8 cluster endpoint> -g <gw-ssh-url> -n "Path To K8s Dynamnic Secret" --ssh-extra-args "non-interactive"
```
