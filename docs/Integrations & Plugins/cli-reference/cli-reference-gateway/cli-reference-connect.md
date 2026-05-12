---
title: CLI Reference - Connect
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
This page covers the `connect` command, which initiates a Secure Remote Access (SRA) session with the CLI.

<CLIGeneralFlags />

## `connect`

Performs secure remote access to a target resource through an Akeyless SRA gateway. Supports SSH, RDP, database, Kubernetes, and tunnel connections.

### Usage

```shell
akeyless connect [flags]
```

### Key flags

`-t, --target`: Target resource. Examples: `user@ssh-server[:port]`, `us-east-2`, `mysql-server:3306`

`-v, --via-sra`: SRA host the connection routes through. Format: `sra-host:port`

`-g, --gateway-url`: Gateway URL (Configuration Management port). Example: `http://localhost:8000`

`-c, --cert-issuer-name`: Akeyless SSH certificate issuer name. Falls back to `~/.akeyless-connect.rc` or item details if not specified

`-n, --name`: Path to the secret or dynamic secret (producer) name used for the connection

`-i, --identity-file`: Private key file for public key authentication. Defaults to `~/.ssh/id_rsa`, `~/.ssh/id_ecdsa`, `~/.ssh/id_ed25519`, or `~/.ssh/id_dsa`

`--generate-key`: Generate a one-time RSA private key for the session, deleted after the session ends

`-J, --justification`: User-supplied connection justification

`--sra-ctrl-proto[=http]`: SRA control API protocol (`http` or `https`)

`--sra-ctrl-port[=9900]`: SRA control API port

`--sra-ctrl-subdomain`: SRA control API URL prefix. Example: `https://<prefix>.sra-host`

`--sra-ctrl-path`: SRA control API path. Example: `https://sra-host/<path>`

`--gateway-rest-endpoint`: Gateway REST API URL. Example: `https://rest.akeyless.io`

`--ssh-legacy-signing-alg[=false]`: Use legacy `ssh-rsa-cert-v01@openssh.com` signing algorithm in the SSH certificate

`--ssh-command`: Path to the SSH executable. Example: `/usr/bin/ssh`

`--ssh-extra-args`: Additional arguments to pass to the SSH client (except `-i`)

`-T, --tunnel`: SSH tunnel parameters. Example: `-T='-L :5555:0.0.0.0:5555'`

`-C, --command`: Command to execute on the target (non-interactive mode). Example: `-C='ls -al'`

`--k8s-tunnel`: Create an SSH tunnel with a Kubernetes proxy on a specific local port (`1024`–`65535`). Overrides `--tunnel` and `--command` when set

`-V, --ssh-version`: Print the local SSH client version and exit

`--debug`: Output debug information

### RC file

Default values for most flags can be set in `~/.akeyless-connect.rc`. See [Akeyless Connect](https://docs.akeyless.io/docs/sra-akeyless-connect) for the full RC file reference and setup instructions.

### Examples

SSH to a remote host through an SRA gateway:

```shell
akeyless connect \
  -t user@my-server.example.com \
  -c /SRA/my-ssh-cert-issuer \
  -v my-sra-host.example.com:22 \
  -g http://my-gw.example.com:8000
```

Connect to a database dynamic secret:

```shell
akeyless connect \
  -t postgres-server:5432 \
  -n /producers/my-postgres \
  -v my-sra-host.example.com:22 \
  -g http://my-gw.example.com:8000
```

Open a Kubernetes tunnel on local port 8443:

```shell
akeyless connect \
  -t my-namespace@k8s-cluster.example.com \
  -n /dynamic-secrets/my-k8s-secret \
  --k8s-tunnel 8443 \
  -v my-sra-host.example.com:22
```
