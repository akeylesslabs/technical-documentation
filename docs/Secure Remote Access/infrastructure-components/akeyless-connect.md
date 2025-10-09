---
title: Akeyless Connect
excerpt: ''
deprecated: false
hidden: true
metadata:
  title: ''
  description: ''
  robots: index
next:
  description: ''
  pages:
    - type: basic
      slug: akeyless-scp
      title: Akeyless SCP
---
Akeyless connect provides you with secure CLI access to resources or a secure tunnel from any UNIX terminal. 

# Prerequisites

To use Akeyless Connect you need:

* Akeyless CLI v1.42.0 or higher. 

* An [SSH certificate issuer](https://docs.akeyless.io/docs/how-to-configure-ssh) for certificate authentication.

* A [Secure Remote Access Bastion](https://docs.akeyless.io/docs/secure-remote-access-bastion).

* OpenSSH v7.9  and OpenSSL 1.1.1 or higher on target servers.

> 👍 Note
>
> `Akeyless connect` command supports legacy `~/.akeyless-sphere.rc` configuration file.
>
> Starting from Windows 10, Microsoft supports the native feature "Windows Subsystem for Linux."\
> This feature enables users to utilize their Windows OS environment as a UNIX-like system. 
>
> To work with the `akeyless-connect` command from a Windows machine, place the <code>.akeyless-connect.rc</code> script in your home directory.

# Set Up Akeyless Connect

1. Download the latest version of [Akeyless Command Line Interface (CLI)](https://docs.akeyless.io/docs/cli).

2. Create a resource file called **\~/.akeyless-connect.rc** as follows: 

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
USE_SSH_AGENT=no

SSH_EXTRA_ARGS=""

# Path to SSH executable. e.g. /usr/bin/ssh
SSH_EXTERNAL_CLIENT="ssh"
```

The latest version of this file can be found in [Akeyless official artifacts](https://rest.akeyless.io/Akeyless_Artifacts/Linux/SSH/). 

Edit the settings as follows: 

`IDENTITY_FILE` - Default is `~/.ssh/id_rsa`. Full path to the private key to be signed and used for the Zero Trust session.

`CERT_ISSUER_NAME` - Full path to the Akeyless [SSH Certificates Issuer](https://docs.akeyless.io/docs/ssh-and-pkitls-certificates) item. 

`AKEYLESS_PROFILE` - Set the default profile that will be used from your Akeyless [Command Line Interface (CLI)](https://docs.akeyless.io/docs/cli). By default, it's using the `default` profile of your Akeyless CLI.

`AKEYLESS_CLI` - Akeyless CLI binary (if needed).

`AKEYLESS_GW_REST_API` - Set your Akeyless Gateway URL on port `8080` for [Zero-Knowledge](https://docs.akeyless.io/docs/zero-knowledge) items and for internal network access.

`BASTION_API_PROTO` - Default is `http`. Set to `https` when your [Secure Remote Access Bastion](https://docs.akeyless.io/docs/secure-remote-access-bastion) is configured with TLS.  

`BASTION_API_PORT` - Default is set to `9900`. Set your matching `ssh-sra` cluster service port. 

`BASTION_SSH_PORT` - Default is set to `22`. Set your matching `ssh-sra`  cluster service port. 

**Optional** when working with Application Load Balancers, you can set the exact path of your `ssh-sra` service, which listens to the bastion `api` control port: 

`BASTION_API_PREFIX` - Set your path prefix as your load balancer settings.

`BASTION_API_PATH` - Set your path as your load balancer settings.

Where the URL will be set as follow: 

`${BASTION_API_PROTO}://"${BASTION_API_PREFIX}${BASTION_HOST}${BASTION_API_PATH}":"${BASTION_API_PORT}`

`SSH_EXTRA_ARGS` - Add any official SSH arguments.

3. Use the `akeyless connect` command to connect to a resource through the [Secure Remote Access Bastion](https://docs.akeyless.io/docs/secure-remote-access-bastion):

```shell General Template
akeyless connect -t <[user@]target/hostname/ip[:port]> -v <sra-bastion-ssh-sra-service/ip[:port]>
```

Full options list:

```shell akeyless connect -h
-t, --target                           Target resource, example formats: user@ssh-server[:port], us-east-2, mysql-server:3306, etc.
  -v, --via-bastion                      Bastion host, which the connection will go through. e.g.: bastion-host:port. 
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
      --use-ssh-agent										 Enable ssh-agent
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

For SSH access through the bastion, please use both `-v ssh-bastion` and the `-c cert_issuer_name` option. Notice the end-users require `read` permission on the cert issuer item which enables them access to the bastion.

```shell Akeyless connect for SSH
akeyless connect -t user@ssh-server[:port] -v <via-sra-bastion-ssh-service> -c "<Path to SSH Cert Issuer>"
```

> 📘 Info
>
> For using different SSH cert-issuers that enable access to target-servers **without** providing `read` permission to the end-users (only `list` permission on the cert-issuers), you will need to also pass the flag: `-n cert_issuer_name` for the **other** cert-issuer. This will enable access through the bastion based on its allowed-users list, where the bastion will read the secret (request the cert) on their behalf.

**AWS:**

```shell Akeyless CLI
akeyless connect -t us-east-1 -c my-ssh-cert-issuer -v <via-sra-bastion-ssh-service>:<port> -n "<Path to AWS Dynamic Secret>"
```

In case you already defined the `Cert Issuer` inside the `akeyless-connect.rc` file you can use: 

```shell Akeyless CLI
akeyless connect -t us-east-1 -v <via-sra-bastion-ssh-service>:<port> -n "<Path to AWS Dynamic Secret>"
```

**MongoDB:** 

```shell Akeyless CLI
akeyless connect -t <mongo server IP>:27017 -v <via-sra-bastion-ssh-service>:<port> -n "<Path to MongoDB Dynamic Secret>"
```

**MySQL:**

```shell Akeyless CLI
akeyless connect -t <mysql-server>:3306 -v <via-sra-bastion-ssh-service>:<port> -n "<Path to MySQL Dynamic Secret>"
```

**EKS:**

```shell Akeyless CLI
akeyless connect -t <namespace>@<eks cluster endpoint without https:// > -v <via-sra-bastion-ssh-service>:<port> -n "<Path to EKS Dynamic secret>"
```

**Non-interactive connection to K8s:**

Linux:

```shell
AKEYLESS_PARAM='get pod' akeyless connect -t <k8 cluster endpoint> -v <via-sra-bastion-ssh-service> -n "Path To K8s Dynamnic Secret" --ssh-extra-args "non-interactive"
```

Windows: 

```shell
$env:AKEYLESS_PARAM = 'get pods'; .\akeyless.exe connect -t <k8 cluster endpoint> -v <via-sra-bastion-ssh-service> -n "Path To K8s Dynamnic Secret" --ssh-extra-args "non-interactive"
```
